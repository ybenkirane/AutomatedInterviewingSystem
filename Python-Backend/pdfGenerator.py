from pylatex import Document, Section, Subsection, Command, Itemize, Enumerate, Description
from pylatex.utils import italic, NoEscape
import openai, json, os, re


class MyDocument(Document):

    def __init__(self):
        import interview
        super().__init__()

        self.preamble.append(Command('title', f'{interview.Industry} {interview.Position} Interview Report'))
        self.preamble.append(Command('author', f'Nbody Labs, {interview.Company}'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        self.append(NoEscape(r'\maketitle'))

    def fill_document(self):  

        import interview

        def remove_control_characters(s):
            return re.sub(r'[\x00-\x1F\x7F]', '', s)
        
        n = interview.n_topics

        question_list = []
        difficulty_list = []
        topic_list = []

        feedback_list = []
        score_list = []
        correct_solution_list = []
        rubric_list = []

        with open("mainInterviewTopic.json", "r") as f:
            data_questions = json.load(f)

        for i in range(n):
            question_list.append(data_questions["questions"][i]["Question"])
            difficulty_list.append(data_questions["questions"][i]["Difficulty"])
            topic_list.append(data_questions["questions"][i]["Topic"])

            with open(f"score{i}.json", "r") as sc:
                file_content = sc.read().translate(str.maketrans("", "", "\r\n\t"))
                grade = json.loads(file_content)            
            score_list.append(grade["grade"][0]["Score"])
            feedback_list.append(grade["grade"][0]["Remarks"])

            with open(f"solution{i}.json", "r") as sl:
                file_content = sl.read()
                cleaned_content = remove_control_characters(file_content)
                escaped_content = cleaned_content.replace('\\', '\\\\')
                solution_i = json.loads(escaped_content)
            correct_solution_list.append(solution_i["solution"][0]["Answer"])

            with open(f"rubric{i}.json", "r") as ru:
                file_content = ru.read().translate(str.maketrans("", "", "\r\n\t"))
                rubric_i = json.loads(file_content)
            rubric_list.append(rubric_i)

        """Add a section, a subsection and some text to the document."""

        with self.create(Section('Interview Transcript')):
            self.append('Below is the complete transcript of the interview. ')
                #Include Transcript here... 
            self.append('The topics covered in the interview are: Topic 1, ..., Topic n.')

        with self.create(Section('Technical Interview')):
            self.append('Below are the questions and solutions generated by NBodyLabs.')
            with self.create(Subsection(f"Question #{i}: ")):
                for i in range(n):
                    with self.create(Description()) as desc:
                        desc.add_item(f"Problem: ", f"{question_list[i]}")
                        desc.add_item(f"Difficulty: ", f"{difficulty_list[i]}")
                        desc.add_item(f"Topic: ", f"{topic_list[i]}")
                        desc.add_item(f"Reference Solution: ", f"{correct_solution_list[i]}")
                        desc.add_item(f"Grading Rubric: ", f"{rubric_list[i]}")
                        # desc.add_item(f"Candidate Solution: ", f"{score_list[i]}")
                        desc.add_item(f"Feedback on Candidate Solution: ", f"{feedback_list[i]}")
                        desc.add_item(f"Candidate Score: ", f"{score_list[i]}")
def pdfGeneration():
    doc = MyDocument()
    doc.fill_document()

    doc.generate_pdf('InterviewReport', clean_tex=False)

if __name__ == "__main__":
    pdfGeneration()
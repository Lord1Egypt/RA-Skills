import subprocess
import os

def run_code(file_path):
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return None


def grade_homework(student_dir, template_dir):
    student_file = None
    answer_file = None

    for f in os.listdir(student_dir):
        if f.endswith(".py"):
            student_file = os.path.join(student_dir, f)

    for f in os.listdir(template_dir):
        if f.endswith(".py"):
            answer_file = os.path.join(template_dir, f)

    if not student_file or not answer_file:
        return 0

    student_output = run_code(student_file)
    answer_output = run_code(answer_file)

    if student_output == answer_output:
        return 100
    elif student_output:
        return 60
    else:
        return 0
from modules.email_fetcher import fetch_attachments
from modules.attachment_parser import parse_filename
from modules.extractor import unzip_file
from modules.grader import grade_homework
from modules.excel_writer import save_to_excel
from modules.template_manager import get_template

import os

def run(inputs):
    assignment_id = inputs["assignment_id"]
    email_user = inputs["email_user"]
    email_auth_code = inputs["email_auth_code"]

    attachments = fetch_attachments(email_user, email_auth_code)

    results = []

    for file_path in attachments:
        info = parse_filename(file_path)

        if not info:
            continue

        name, student_id, hw_id = info

        if hw_id != assignment_id:
            continue

        extracted_path = unzip_file(file_path)

        template_path = get_template(assignment_id)

        from modules.ai_grader import ai_grade

        score, comment = ai_grade(extracted_path, template_path)

        results.append({
            "姓名": name,
            "学号": student_id,
            "作业": hw_id,
            "成绩": score,
            "评语": comment
        })

    excel_path = save_to_excel(results, assignment_id)

    return {"excel_path": excel_path}
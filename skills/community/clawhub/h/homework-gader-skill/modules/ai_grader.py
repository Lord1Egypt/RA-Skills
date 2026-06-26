import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_code(folder):
    content = ""
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    content += f"\n# 文件: {f}\n" + file.read()
    return content


def ai_grade(student_dir, template_dir):
    student_code = read_code(student_dir)
    template_code = read_code(template_dir)

    prompt = f"""
你是一个严格但公平的编程老师，请根据参考答案给学生作业评分。

【评分标准】
1. 功能是否正确（50分）
2. 代码结构（20分）
3. 代码规范（20分）
4. 可读性（10分）

【参考答案】
{template_code}

【学生作业】
{student_code}

请输出：
1. 分数（0-100）
2. 简短评语（不超过50字）

格式：
分数: xx
评语: xxx
"""

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    try:
        score = int(text.split("分数:")[1].split("\n")[0].strip())
        comment = text.split("评语:")[1].strip()
    except:
        score = 60
        comment = "评分解析失败"

    return score, comment
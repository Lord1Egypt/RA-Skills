#!/usr/bin/env python3
"""
OCR Helper - 作业答案识别辅助工具
使用 pytesseract 进行 OCR 识别
"""

import os
import json
import re
from typing import List, Dict, Optional

# 尝试导入所需库
try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("请安装依赖: pip install pillow pytesseract")
    print("同时需要安装 tesseract-ocr")
    exit(1)


def extract_text_from_image(image_path: str) -> str:
    """从图片中提取文字"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        return text
    except Exception as e:
        return f"[OCR识别失败: {str(e)}]"


def parse_answers(text: str) -> List[Dict]:
    """
    解析答案文本，返回题目列表
    格式支持：
    1. 答案
    2. 答案
    或者：
    1) 答案
    2) 答案
    """
    answers = []
    lines = text.strip().split('\n')
    
    # 匹配题号的正则表达式
    pattern = r'^\s*(\d+)[.)、]\s*(.+)$'
    
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            question_num = int(match.group(1))
            answer = match.group(2).strip()
            answers.append({
                'question': question_num,
                'answer': answer
            })
    
    return answers


def save_answers(answers: List[Dict], output_path: str):
    """保存答案到 JSON 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)
    print(f"答案已保存到: {output_path}")


def load_answers(input_path: str) -> List[Dict]:
    """从 JSON 文件加载答案"""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def grade_homework(student_answers: List[Dict], correct_answers: List[Dict]) -> Dict:
    """
    批改作业
    返回批改结果
    """
    result = {
        'correct': [],
        'incorrect': [],
        'total': len(correct_answers),
        'correct_count': 0,
        'incorrect_count': 0
    }
    
    # 建立正确答案字典
    answer_dict = {a['question']: a['answer'] for a in correct_answers}
    
    for student_answer in student_answers:
        q_num = student_answer['question']
        if q_num in answer_dict:
            is_correct = student_answer['answer'].strip() == answer_dict[q_num].strip()
            question_result = {
                'question': q_num,
                'student_answer': student_answer['answer'],
                'correct_answer': answer_dict[q_num],
                'correct': is_correct
            }
            if is_correct:
                result['correct'].append(question_result)
                result['correct_count'] += 1
            else:
                result['incorrect'].append(question_result)
                result['incorrect_count'] += 1
    
    return result


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法:")
        print("  python ocr_helper.py recognize <图片路径>")
        print("  python ocr_helper.py grade <学生答案json> <正确答案json>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'recognize':
        image_path = sys.argv[2]
        text = extract_text_from_image(image_path)
        print("识别结果:")
        print(text)
        
        # 尝试解析答案
        answers = parse_answers(text)
        if answers:
            print("\n解析出的答案:")
            for a in answers:
                print(f"  第{a['question']}题: {a['answer']}")
            
            # 保存到文件
            output_path = os.path.splitext(image_path)[0] + '_answers.json'
            save_answers(answers, output_path)
    
    elif command == 'grade':
        student_file = sys.argv[2]
        correct_file = sys.argv[3]
        
        student_answers = load_answers(student_file)
        correct_answers = load_answers(correct_file)
        
        result = grade_homework(student_answers, correct_answers)
        
        print(f"批改结果: {result['correct_count']}/{result['total']} 正确")
        print(f"错误题目: {[i['question'] for i in result['incorrect']]}")
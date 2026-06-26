#!/usr/bin/env python3
"""
生成4个版本的完整PDF报告
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from lib.pdf_combined import create_pdf_report
from lib.scorer import calculate_type, calculate_clarity
from lib.question_pool import sample_questions
from datetime import datetime

def generate_version_report(version_num, version_name):
    """生成指定版本的完整报告"""
    print(f"\n{'='*50}")
    print(f"生成 {version_name} ({version_num}题) 报告")
    print('='*50)
    
    # 生成随机答案
    questions = sample_questions(version_num)
    answers = []
    for i, q in enumerate(questions):
        # 模拟随机选择
        choice = 'A' if (i * 7) % 2 == 0 else 'B'
        answers.append((q['id'], choice))
    
    # 计算结果
    type_code, scores = calculate_type(answers)
    clarity = {dim: calculate_clarity(score) for dim, score in scores.items()}
    
    # 生成PDF
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"MBTI-v{version_num}-{type_code}-{today}.pdf"
    output_path = create_pdf_report(type_code, scores, clarity, filename)
    
    size = os.path.getsize(output_path)
    print(f"生成: {filename} ({size} bytes)")
    print(f"类型: {type_code}")
    print(f"维度得分: {scores}")
    
    return output_path, type_code

def main():
    versions = [
        (70, "快速版"),
        (93, "标准版"),
        (144, "扩展版"),
        (200, "专业版"),
    ]
    
    pdfs = []
    for version_num, version_name in versions:
        try:
            pdf_path, mbti_type = generate_version_report(version_num, version_name)
            pdfs.append((version_name, version_num, pdf_path, mbti_type))
        except Exception as e:
            print(f"生成 {version_name} 失败: {e}")
    
    print("\n" + "="*50)
    print("生成完成!")
    print("="*50)
    for name, num, path, mtype in pdfs:
        print(f"  {name} ({num}题): {path} -> {mtype}")
    
    return pdfs

if __name__ == "__main__":
    main()

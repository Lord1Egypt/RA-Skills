#!/usr/bin/env python3
"""
MBTI PDF Report Generator - Combined (Page 1 + Page 2)
第一页保持原版，第二页新增深度分析
"""

import os
import sys

def create_pdf_report(type_code: str, scores: dict, clarity_levels: dict, output_path: str = "mbti_report.pdf"):
    """
    生成完整的MBTI报告（两页）
    - Page 1: 核心报告（原版v1.0.3布局）
    - Page 2: 深度分析（新增）
    """
    sys.path.insert(0, os.path.dirname(__file__))
    
    from lib.pdf_page1 import create_pdf_page1
    from lib.pdf_page2 import create_pdf_page2
    
    # 生成第一页
    page1_path = output_path.replace('.pdf', '_p1.pdf')
    create_pdf_page1(type_code, scores, clarity_levels, page1_path)
    
    # 生成第二页
    page2_path = output_path.replace('.pdf', '_p2.pdf')
    create_pdf_page2(type_code, page2_path)
    
    # 合并两页
    try:
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        merger.append(page1_path)
        merger.append(page2_path)
        merger.write(output_path)
        merger.close()
    except ImportError:
        # 如果没有PyPDF2，只保留第一页
        import shutil
        shutil.copy(page1_path, output_path)
    
    # 清理临时文件
    if os.path.exists(page1_path):
        os.remove(page1_path)
    if os.path.exists(page2_path):
        os.remove(page2_path)
    
    return output_path


if __name__ == "__main__":
    from lib.scorer import calculate_type, calculate_clarity
    from lib.questions import get_questions
    from datetime import datetime
    
    questions = get_questions(70)
    answers = []
    for q in questions:
        if q["dimension"] == "EI":
            choice = "B" if q["id"] <= 14 else "A"
        elif q["dimension"] == "SN":
            choice = "B" if q["id"] <= 30 else "A"
        elif q["dimension"] == "TF":
            choice = "B" if q["id"] <= 42 else "A"
        else:
            choice = "B" if q["id"] <= 62 else "A"
        answers.append((q["id"], choice))
    
    type_code, scores = calculate_type(answers)
    clarity_levels = {dim: calculate_clarity(score) for dim, score in scores.items()}
    
    today = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"MBTI-{type_code}-{today}.pdf"
    
    output = create_pdf_report(type_code, scores, clarity_levels, output_filename)
    print(f"PDF created: {output}")

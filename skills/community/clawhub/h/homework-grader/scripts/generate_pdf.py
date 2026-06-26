#!/usr/bin/env python3
"""
PDF Generator - 生成作业分析PDF报告
"""

import os
import json
from datetime import datetime
from typing import List, Dict

try:
    from weasyprint import HTML
except ImportError:
    print("请安装依赖: pip install weasyprint")
    exit(1)


def generate_pdf_report(
    students_data: List[Dict],
    correct_answers: List[Dict],
    stats: Dict,
    output_path: str,
    threshold: float = 40
) -> str:
    """生成PDF分析报告"""
    
    # 准备数据
    total_students = stats['total_students']
    total_questions = stats['total_questions']
    question_stats = stats['questions']
    student_stats = stats['students']
    
    # 计算班级整体数据
    total_correct = sum(s['correct_count'] for s in student_stats)
    total_possible = total_questions * total_students
    avg_correct_rate = round(total_correct / total_possible * 100, 1) if total_possible > 0 else 0
    
    # 获取重点错题
    key_questions = []
    for q_num, q_stat in question_stats.items():
        if q_stat['error_rate'] >= threshold:
            key_questions.append({
                'question': q_num,
                'error_rate': q_stat['error_rate'],
                'incorrect_count': q_stat['incorrect_count'],
                'correct_answer': correct_answers[q_num - 1]['answer'] if q_num <= len(correct_answers) else ''
            })
    
    # 按错误率排序
    key_questions.sort(key=lambda x: x['error_rate'], reverse=True)
    
    # 生成HTML内容
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>作业分析报告</title>
    <style>
        body {{ font-family: "Microsoft YaHei", "SimHei", sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 10px; margin-top: 30px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .summary-item {{ display: inline-block; margin: 10px 20px; }}
        .summary-label {{ font-weight: bold; color: #7f8c8d; }}
        .summary-value {{ font-size: 1.5em; color: #2c3e50; font-weight: bold; }}
        
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 12px; text-align: center; }}
        th {{ background: #3498db; color: white; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        
        .key-question {{ background: #fff3cd; }}
        .key-badge {{ background: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.8em; }}
        
        .suggestion {{ background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .suggestion-title {{ font-weight: bold; color: #155724; }}
        
        .footer {{ text-align: center; color: #95a5a6; margin-top: 40px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>📊 作业分析报告</h1>
    
    <div class="summary">
        <div class="summary-item">
            <div class="summary-label">班级人数</div>
            <div class="summary-value">{total_students}</div>
        </div>
        <div class="summary-item">
            <div class="summary-label">题目总数</div>
            <div class="summary-value">{total_questions}</div>
        </div>
        <div class="summary-item">
            <div class="summary-label">平均正确率</div>
            <div class="summary-value">{avg_correct_rate}%</div>
        </div>
        <div class="summary-item">
            <div class="summary-label">重点错题</div>
            <div class="summary-value">{len(key_questions)}</div>
        </div>
    </div>
    
    <h2>📈 错题统计</h2>
    <table>
        <tr>
            <th>题号</th>
            <th>错题人数</th>
            <th>错误率</th>
            <th>标记</th>
        </tr>
"""
    
    # 添加错题统计行
    for q_num in sorted(question_stats.keys()):
        q_stat = question_stats[q_num]
        is_key = q_stat['error_rate'] >= threshold
        row_class = 'class="key-question"' if is_key else ''
        badge = '<span class="key-badge">⭐ 重点</span>' if is_key else ''
        
        html_content += f"""
        <tr {row_class}>
            <td>第{q_num}题</td>
            <td>{q_stat['incorrect_count']}</td>
            <td>{q_stat['error_rate']}%</td>
            <td>{badge}</td>
        </tr>
"""
    
    html_content += """
    </table>
"""
    
    # 添加重点错题讲解建议
    if key_questions:
        html_content += """
    <h2>⭐ 重点错题讲解建议</h2>
"""
        for kq in key_questions:
            html_content += f"""
    <div class="suggestion">
        <div class="suggestion-title">第{kq['question']}题 (错误率: {kq['error_rate']}%)</div>
        <p><strong>正确答案:</strong> {kq['correct_answer']}</p>
        <p><strong>讲解建议:</strong> 该题错误人数较多，建议老师在课堂上详细讲解此题目。</p>
    </div>
"""
    
    # 添加学生详情（可选）
    html_content += f"""
    <h2>👥 学生得分明细</h2>
    <table>
        <tr>
            <th>学生</th>
            <th>正确题数</th>
            <th>错误题数</th>
            <th>正确率</th>
        </tr>
"""
    
    for student in student_stats:
        html_content += f"""
        <tr>
            <td>{student['name']}</td>
            <td>{student['correct_count']}</td>
            <td>{student['incorrect_count']}</td>
            <td>{100 - student['error_rate']}%</td>
        </tr>
"""
    
    html_content += """
    </table>
    
    <div class="footer">
        <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        <p>作业批改助手 | Homework Grader</p>
    </div>
</body>
</html>
"""
    
    # 生成PDF
    HTML(string=html_content).write_pdf(output_path)
    print(f"PDF 报告已生成: {output_path}")
    
    return output_path


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print("用法: python generate_pdf.py <学生数据json> <正确答案json> <统计结果json> [输出路径] [阈值]")
        sys.exit(1)
    
    student_file = sys.argv[1]
    correct_file = sys.argv[2]
    stats_file = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) > 4 else "作业分析报告.pdf"
    threshold = float(sys.argv[5]) if len(sys.argv) > 5 else 40
    
    with open(student_file, 'r', encoding='utf-8') as f:
        students_data = json.load(f)
    
    with open(correct_file, 'r', encoding='utf-8') as f:
        correct_answers = json.load(f)
    
    with open(stats_file, 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    generate_pdf_report(students_data, correct_answers, stats, output_path, threshold)
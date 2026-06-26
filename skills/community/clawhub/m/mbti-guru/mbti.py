#!/usr/bin/env python3
"""
MBTI Personality Test - Main Entry Point
"""
import sys
import os

# Add lib to path
sys.path.insert(0, os.path.dirname(__file__))

from lib.questions import get_questions, get_question_count
from lib.scorer import calculate_type, calculate_clarity
from lib.reports import generate_report, generate_summary_report
from lib.types import get_type

def main():
    print("=" * 60)
    print("MBTI Personality Test")
    print("MBTI 人格测试")
    print("=" * 60)
    
    print("""
请选择测试版本 / Select test version:
1. 快速版 (70题 ~10分钟) Quick
2. 标准版 (93题 ~15分钟) Standard  
3. 扩展版 (144题 ~25分钟) Extended
4. 专业版 (200题 ~35分钟) Professional
""")
    
    version_map = {"1": 70, "2": 93, "3": 144, "4": 200}
    
    version = input("输入数字选择 / Enter number: ").strip()
    
    if version not in version_map:
        print("无效选择，使用快速版")
        version = 70
    else:
        version = version_map[version]
    
    questions = get_questions(version)
    total = len(questions)
    
    print(f"\n开始测试，共{total}题")
    print(f"每个问题请输入 A 或 B\n")
    
    answers = []
    
    for i, q in enumerate(questions, 1):
        print(f"\n问题 {i}/{total}")
        print(f"{q['option_a']}")
        print(f"A) {q['option_a']}")
        print(f"B) {q['option_b']}")
        
        while True:
            choice = input("选择 / Choice (A/B): ").strip().upper()
            if choice in ["A", "B"]:
                break
            print("请输入 A 或 B")
        
        answers.append((q["id"], choice))
        
        # Progress every 10 questions
        if i % 10 == 0:
            print(f"进度: {i}/{total} ({i*100//total}%)")
    
    # Calculate results
    print("\n计算中...")
    type_code, scores = calculate_type(answers)
    
    # Generate report
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    report = generate_summary_report(type_code, scores)
    print(report)
    
    # Full report
    print("\n输入任意键查看完整报告...")
    input()
    full_report = generate_report(type_code, scores, 
                                  {dim: calculate_clarity(score) 
                                   for dim, score in scores.items()})
    print(full_report)

if __name__ == "__main__":
    main()

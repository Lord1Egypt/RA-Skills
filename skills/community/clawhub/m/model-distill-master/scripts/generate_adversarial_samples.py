#!/usr/bin/env python3
"""对抗性样本挖掘器 - 找出学生易错的样本"""

import json
import random

def is_teacher_correct(question):
    """模拟教师正确率95%"""
    return random.random() < 0.95

def is_student_correct(question):
    """模拟学生正确率60%"""
    return random.random() < 0.60

def mine_adversarial(input_file, output_file, target_num=100):
    """挖掘对抗样本"""
    with open(input_file, 'r') as f:
        questions = [json.loads(line) for line in f]

    adversarial = []
    tested = 0

    random.shuffle(questions)

    for q in questions:
        if len(adversarial) >= target_num:
            break

        tested += 1
        question_text = q.get('input', '')

        # 教师对且学生错 = 对抗样本
        if is_teacher_correct(question_text) and not is_student_correct(question_text):
            q['metadata'] = {'type': 'adversarial', 'note': '学生易错样本'}
            adversarial.append(q)

    # 保存
    with open(output_file, 'w') as f:
        for item in adversarial:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"对抗样本挖掘完成:")
    print(f"  测试: {tested}")
    print(f"  找到: {len(adversarial)} ({len(adversarial)/tested:.1%})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--num", type=int, default=100)
    args = parser.parse_args()

    mine_adversarial(args.input, args.output, args.num)

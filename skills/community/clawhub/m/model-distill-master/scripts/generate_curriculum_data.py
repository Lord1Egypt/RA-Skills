#!/usr/bin/env python3
"""课程式数据生成器 - 三级难度分级"""

import json
import random

def assess_difficulty(question, task_type):
    """评估问题难度"""
    if task_type == "math":
        if len(question) > 50 or "积分" in question or "导数" in question:
            return "LEVEL_3"
        elif len(question) > 30 or "方程" in question:
            return "LEVEL_2"
        return "LEVEL_1"
    return "LEVEL_2"

def generate_curriculum(input_file, output_file, task_type):
    """生成课程式数据"""
    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]

    # 分级
    levels = {"LEVEL_1": [], "LEVEL_2": [], "LEVEL_3": []}
    for item in data:
        level = assess_difficulty(item.get('input', ''), task_type)
        item['difficulty'] = level
        levels[level].append(item)

    # 按比例采样 30/40/30
    result = []
    total = len(data)
    target = {"LEVEL_1": int(total*0.3), "LEVEL_2": int(total*0.4), "LEVEL_3": int(total*0.3)}

    for level, items in levels.items():
        n = min(len(items), target[level])
        result.extend(random.sample(items, n))

    # 打乱
    random.shuffle(result)

    # 保存
    with open(output_file, 'w') as f:
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"课程式数据生成完成: {len(result)}条")
    print(f"  LEVEL_1: {len([x for x in result if x['difficulty']=='LEVEL_1'])}")
    print(f"  LEVEL_2: {len([x for x in result if x['difficulty']=='LEVEL_2'])}")
    print(f"  LEVEL_3: {len([x for x in result if x['difficulty']=='LEVEL_3'])}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--task", default="math")
    args = parser.parse_args()

    generate_curriculum(args.input, args.output, args.task)

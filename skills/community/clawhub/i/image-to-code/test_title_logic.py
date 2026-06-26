#!/usr/bin/env python3
"""
测试标题识别逻辑（不依赖 OCR 库）
"""

import re

# 标题识别模式
title_patterns = {
    1: [  # 一级标题模式
        r'^第.+章',  # 第一章、第 1 章
        r'^第.+部分',  # 第一部分
        r'^[一二三四五六七八九十]+、',  # 一、二、三、
    ],
    2: [  # 二级标题模式
        r'^第.+节',  # 第一节、第 1 节
        r'^[0-9]+\.[0-9]+(?!\.[0-9])',  # 1.1, 1.2 (但不匹配 1.1.1)
        r'^\([0-9]+\)',  # (1), (2)
        r'^[（][一二三四五六七八九十]+[）]',  # （一）、（二）
    ],
    3: [  # 三级标题模式
        r'^[0-9]+\.[0-9]+\.[0-9]+',  # 1.1.1
        r'^[0-9]+、',  # 1、2、3、
    ],
}

def detect_title_level(text: str):
    """检测标题级别"""
    text = text.strip()
    
    # 按顺序检查：3 级 -> 2 级 -> 1 级（更具体的先匹配）
    for level in [3, 2, 1]:
        patterns = title_patterns[level]
        for pattern in patterns:
            if re.search(pattern, text):
                return level
    
    return None

# 测试用例
test_cases = [
    # (输入文本，预期级别)
    ("第一章 项目概述", 1),
    ("第一部分 总则", 1),
    ("一、项目背景", 1),
    ("二、市场分析", 1),
    ("1.1 项目目标", 2),
    ("1.2 技术方案", 2),
    ("第一节 技术方案", 2),
    ("(1) 减少成本", 2),
    ("(2) 提高效率", 2),
    ("（一）战略规划", 2),
    ("1.1.1 技术路线", 3),
    ("1.2.3 实施步骤", 3),
    ("1、具体步骤", 3),
    ("2、注意事项", 3),
    ("这是普通文字", None),
    ("E = mc²", None),
    ("本项目旨在开发", None),
]

print("="*60)
print("标题识别逻辑测试")
print("="*60)

all_passed = True
for text, expected_level in test_cases:
    result = detect_title_level(text)
    status = "✅" if result == expected_level else "❌"
    
    if result != expected_level:
        all_passed = False
    
    print(f"{status} '{text}' -> {result} (预期：{expected_level})")

print("="*60)
if all_passed:
    print("✅ 所有测试通过！")
else:
    print("❌ 部分测试失败")
print("="*60)

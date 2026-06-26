#!/usr/bin/env python3
"""
测试标题文本提取功能
"""

import re
from typing import Optional

# 标题识别模式
title_patterns = {
    1: [
        r'^第.+章',
        r'^第.+部分',
        r'^[一二三四五六七八九十]+、',
    ],
    2: [
        r'^第.+节',
        r'^[0-9]+\.[0-9]+(?!\.[0-9])',
        r'^\([0-9]+\)',
        r'^[（][一二三四五六七八九十]+[）]',
    ],
    3: [
        r'^[0-9]+\.[0-9]+\.[0-9]+',
        r'^[0-9]+、',
    ],
}

def detect_title_level(text: str) -> Optional[int]:
    text = text.strip()
    for level in [3, 2, 1]:
        patterns = title_patterns[level]
        for pattern in patterns:
            if re.search(pattern, text):
                return level
    return None

def extract_title_text(text: str, level: int) -> str:
    """提取标题中的纯文本内容"""
    text = text.strip()
    
    if level == 1:
        patterns = [
            r'^第.+章\s*',  # 第 X 章
            r'^第.+部分\s*',  # 第 X 部分
            r'^[一二三四五六七八九十]+、\s*',  # 一、
        ]
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return text[match.end():].strip()
    
    elif level == 2:
        patterns = [
            r'^第.+节\s*',  # 第 X 节
            r'^[0-9]+\.[0-9]+(?!\.[0-9])\s*',  # 1.1
            r'^\([0-9]+\)\s*',  # (1)
            r'^[（][一二三四五六七八九十]+[）]\s*',  # （一）
        ]
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return text[match.end():].strip()
    
    elif level == 3:
        patterns = [
            r'^[0-9]+\.[0-9]+\.[0-9]+\s*',  # 1.1.1
            r'^[0-9]+、\s*',  # 1、
        ]
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                return text[match.end():].strip()
    
    return text

# 测试用例
test_cases = [
    # (输入文本，预期级别，预期提取文本)
    ("第一章 总述", 1, "总述"),
    ("第一部分 总则", 1, "总则"),
    ("一、项目背景", 1, "项目背景"),
    ("二、市场分析", 1, "市场分析"),
    ("1.1 项目背景", 2, "项目背景"),
    ("1.2 技术方案", 2, "技术方案"),
    ("第一节 技术方案", 2, "技术方案"),
    ("(1) 减少成本", 2, "减少成本"),
    ("(2) 提高效率", 2, "提高效率"),
    ("(3) 优化流程", 2, "优化流程"),
    ("（一）战略规划", 2, "战略规划"),
    ("1.1.1 前端架构", 3, "前端架构"),
    ("1.2.3 实施步骤", 3, "实施步骤"),
    ("1、需求分析", 3, "需求分析"),
    ("2、系统设计", 3, "系统设计"),
]

print("="*60)
print("标题文本提取测试")
print("="*60)

all_passed = True
for text, expected_level, expected_extract in test_cases:
    level = detect_title_level(text)
    if level:
        extracted = extract_title_text(text, level)
    else:
        extracted = text
    
    level_ok = level == expected_level
    extract_ok = extracted == expected_extract
    status = "✅" if (level_ok and extract_ok) else "❌"
    
    if not (level_ok and extract_ok):
        all_passed = False
    
    print(f"{status} '{text}'")
    print(f"    级别：{level} (预期：{expected_level})")
    print(f"    提取：'{extracted}' (预期：'{expected_extract}')")
    print()

print("="*60)
if all_passed:
    print("✅ 所有测试通过！")
else:
    print("❌ 部分测试失败")
print("="*60)

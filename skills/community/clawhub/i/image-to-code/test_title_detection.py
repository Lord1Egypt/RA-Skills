#!/usr/bin/env python3
"""
测试标题识别功能
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/image-to-code')

from image_to_code import ImageToCodeConverter

# 创建转换器
converter = ImageToCodeConverter()

# 测试标题识别
test_cases = [
    # (输入文本，预期级别)
    ("第一章 项目概述", 1),
    ("第一部分 总则", 1),
    ("一、项目背景", 1),
    ("1.1 项目目标", 2),
    ("第一节 技术方案", 2),
    ("(1) 减少成本", 2),
    ("(2) 提高效率", 2),
    ("1.1.1 技术路线", 3),
    ("1、具体步骤", 3),
    ("这是普通文字", None),
    ("E = mc²", None),
]

print("="*60)
print("标题识别测试")
print("="*60)

all_passed = True
for text, expected_level in test_cases:
    result = converter.detect_title_level(text)
    status = "✅" if result == expected_level else "❌"
    
    if result != expected_level:
        all_passed = False
    
    print(f"{status} '{text}' -> {result} (预期：{expected_level})")

print("="*60)
if all_passed:
    print("✅ 所有测试通过！")
else:
    print("❌ 部分测试失败")

#!/usr/bin/env python3
"""测试交互模式"""

import sys
from io import StringIO
from pathlib import Path

# 模拟用户输入
test_input = """
1
产品名称，价格，库存，状态，操作
4
4
1
"""

# 重定向 stdin
sys.stdin = StringIO(test_input)

# 导入主程序
sys.path.insert(0, str(Path(__file__).parent))
from main import parse_user_input, generate_clarifying_questions, collect_answers

# 测试
user_input = "创建一个产品列表页"
parsed = parse_user_input(user_input)

print("📋 解析结果:")
print(f"  页面类型：{parsed['page_type']}")
print(f"  关键词：{parsed['keywords']}")
print()

questions = generate_clarifying_questions(parsed)
print(f"📝 生成 {len(questions)} 个问题:\n")

for i, q in enumerate(questions, 1):
    print(f"{i}. {q['id']}: {q['question'][:50]}...")

print("\n" + "=" * 60)
print("开始收集答案...\n")

answers = collect_answers(questions)

print("\n✅ 收集到的答案:")
for key, value in answers.items():
    print(f"  {key}: {value}")

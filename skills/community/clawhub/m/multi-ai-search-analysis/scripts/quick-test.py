#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速测试数据提取功能"""

from extractor import DataExtractor

extractor = DataExtractor()

# 测试文本
text = """
根据最新数据，2026 年全球油价预计将上涨 15%，达到每桶 95 美元。
国际能源署（IEA）预测，到 2026 年底，布伦特原油价格可能突破 100 美元大关。

关键洞察：
1. 中东局势紧张是主要推动因素
2. 全球需求增长 3.2%
3. OPEC+ 减产协议延长至 2026 年 12 月

据高盛报告，油价上涨可能导致全球通胀率上升 0.5 个百分点。
"""

print("=" * 50)
print("数据提取测试")
print("=" * 50)

data = extractor.extract_all(text)

print(f"\n提取结果：")
print(f"  百分比：{len(data['percentages'])} 个")
for p in data['percentages'][:3]:
    print(f"    - {p['value']}%")

print(f"\n  数据点：{len(data['data_points'])} 个")
for d in data['data_points'][:5]:
    print(f"    - {d['value']}{d['unit']}")

print(f"\n  关键洞察：{len(data['key_insights'])} 条")
for i in data['key_insights'][:3]:
    print(f"    - {i[:50]}...")

# 质量评分
print("\n" + "=" * 50)
print("质量评分")
print("=" * 50)

quality = extractor.calculate_quality_score(text, 'Test')
print(f"\n总分：{quality['total_score']} ({quality['level']})")
print(f"\n详细评分:")
for dim, info in quality['breakdown'].items():
    print(f"  {dim}: {info['score']} (权重：{int(info['weight']*100)}%)")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)

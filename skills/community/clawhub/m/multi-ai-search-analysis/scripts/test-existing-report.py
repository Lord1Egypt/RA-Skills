#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试已有报告的数据提取功能"""

import os
from pathlib import Path
from extractor import DataExtractor

# 设置 UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

extractor = DataExtractor()
reports_dir = Path(__file__).parent.parent / 'reports'

print("=" * 60)
print("测试已有报告的数据提取功能")
print("=" * 60)

# 获取最新报告
reports = list(reports_dir.glob("*.md"))
if not reports:
    print("未找到报告文件")
    exit(1)

# 按修改时间排序
reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)
latest_report = reports[0]

print(f"\n最新报告：{latest_report.name}")
print(f"文件大小：{latest_report.stat().st_size} 字节")

# 读取报告内容
try:
    with open(latest_report, 'r', encoding='utf-8') as f:
        content = f.read(5000)  # 读取前 5000 字
    
    print(f"\n读取内容：{len(content)} 字")
    
    # 数据提取
    print("\n" + "=" * 60)
    print("数据提取结果")
    print("=" * 60)
    
    data = extractor.extract_all(content)
    
    print(f"\n提取到:")
    print(f"  百分比：{len(data['percentages'])} 个")
    for p in data['percentages'][:5]:
        print(f"    - {p['value']}%")
    
    print(f"\n  日期：{len(data['dates'])} 个")
    for d in data['dates'][:3]:
        print(f"    - {d['value']}")
    
    print(f"\n  预测：{len(data['predictions'])} 条")
    for p in data['predictions'][:3]:
        print(f"    - {p['text']}")
    
    print(f"\n  关键洞察：{len(data['key_insights'])} 条")
    for i in data['key_insights'][:3]:
        text = i.replace('\n', ' ').strip()
        print(f"    - {text[:60]}...")
    
    print(f"\n  数据点：{len(data['data_points'])} 个")
    
    # 质量评分
    print("\n" + "=" * 60)
    print("质量评分")
    print("=" * 60)
    
    quality = extractor.calculate_quality_score(content, 'Report')
    
    print(f"\n总分：{quality['total_score']} ({quality['level']})")
    print(f"\n详细评分:")
    for dim, info in quality['breakdown'].items():
        print(f"  {dim}: {info['score']} (权重：{int(info['weight']*100)}%)")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
except Exception as e:
    print(f"错误：{e}")

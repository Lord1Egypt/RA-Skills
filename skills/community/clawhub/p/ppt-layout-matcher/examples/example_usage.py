#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT Layout Matcher - 使用示例

演示如何使用版式匹配系统分析内容并获得推荐
"""

import sys
sys.path.insert(0, '.')
from ppt_layout_matcher import recommend_layout, list_all_layouts, get_layout_by_slide

print("=" * 60)
print("PPT 版式匹配系统 - 使用示例")
print("=" * 60)

# 示例 1: 封面推荐
print("\n📘 示例 1: 报告封面")
print("-" * 40)
results = recommend_layout("2024年度产品设计总结报告 - 封面", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")
    print(f"     结构: {t.structure[:80]}...")

# 示例 2: 数据展示
print("\n📊 示例 2: 核心数据指标")
print("-" * 40)
results = recommend_layout("用户增长65%，营收增长33%，利润率25%，客户满意度92%", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 示例 3: 流程展示
print("\n🔄 示例 3: 四步流程")
print("-" * 40)
results = recommend_layout("项目四个阶段：需求分析 → 方案设计 → 开发实施 → 上线运营", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 示例 4: 方案对比
print("\n⚖️ 示例 4: 三大方案对比")
print("-" * 40)
results = recommend_layout("方案A/B/C对比：成本、性能、可扩展性三方面分析", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 示例 5: SWOT分析
print("\n🎯 示例 5: SWOT分析")
print("-" * 40)
results = recommend_layout("SWOT分析：优势、劣势、机会、威胁四个维度", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 示例 6: 时间线
print("\n📅 示例 6: 发展历程")
print("-" * 40)
results = recommend_layout("公司发展历程：2019年创立 → 2021年A轮 → 2023年B轮 → 2024年上市", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 示例 7: 章节过渡
print("\n📖 示例 7: 章节过渡")
print("-" * 40)
results = recommend_layout("Part 2 - 市场分析与竞争格局", top_k=2)
for i, (t, s, a) in enumerate(results):
    print(f"  {'🥇🥈'[i]} {t.name} (Slide {t.slide_ref}) - 匹配度: {s:.2f}")

# 列出所有版式
print("\n\n" + "=" * 60)
print("全部版式列表")
print("=" * 60)
templates = list_all_layouts()
from collections import Counter
families = Counter()
for t in templates:
    if '封面' in t.name:
        families['封面'] += 1
    elif '过渡' in t.name:
        families['过渡'] += 1
    elif any(kw in ' '.join(t.keywords) for kw in ['数据','指标','图表','表格','大字报']):
        families['数据展示'] += 1
    elif '流程' in t.name or 'STEP' in t.name:
        families['流程'] += 1
    elif '对比' in t.name:
        families['对比'] += 1
    elif '网格' in t.name or '象限' in t.name or '矩阵' in t.name or '卡片' in t.name:
        families['网格/卡片'] += 1
    elif '画廊' in t.name or '图片' in t.name or '时间轴' in t.name:
        families['图片展示'] += 1
    elif '列表' in t.name or '要点' in t.name:
        families['列表'] += 1
    elif '全景' in t.name:
        families['综合'] += 1
    else:
        families['特殊'] += 1

for cat, count in families.most_common():
    print(f"  {cat}: {count}")

print(f"\n  总计: {len(templates)} 个版式")
print("\n✅ 示例运行完成")

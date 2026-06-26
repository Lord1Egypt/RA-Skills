#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试豆瓣 API"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from douban_api import search_movie, get_top250, format_movie_info

print("=" * 60)
print("🎬 豆瓣 API 测试")
print("=" * 60)

print("\n🔍 搜索测试：星际穿越")
r = search_movie("星际穿越")
print(f"找到 {len(r)} 部")
if r:
    print(format_movie_info(r[0]))

print("\n\n🏆 Top250 前 5 名:")
top = get_top250()
for i, m in enumerate(top[:5], 1):
    print(f"{i}. 《{m['title']}》 - {m['rating']}分 ({m.get('year', '')})")

print("\n✅ 测试完成!")

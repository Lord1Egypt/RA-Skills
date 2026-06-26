#!/usr/bin/env python3
"""列出系统可用的中文字体"""

import matplotlib.font_manager as fm

# 中文字体关键词
chinese_keywords = ['hei', 'song', 'kai', 'fang', 'ming', 'ping', 'yuan', 'shu', 'fang', 'cn', 'sc', 'tc', 'hk']

# 获取所有字体
all_fonts = fm.fontManager.ttflist

# 筛选中文字体
chinese_fonts = []
for font in all_fonts:
    name_lower = font.name.lower()
    if any(kw in name_lower for kw in chinese_keywords):
        chinese_fonts.append(font.name)

# 去重并排序
chinese_fonts = sorted(set(chinese_fonts))

if chinese_fonts:
    print("系统可用中文字体:")
    for font in chinese_fonts:
        print(f"  - {font}")
    print(f"\n共 {len(chinese_fonts)} 个中文字体")
else:
    print("未找到中文字体")

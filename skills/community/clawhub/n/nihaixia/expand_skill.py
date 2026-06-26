#!/usr/bin/env python3
"""Expand SKILL.md - strict 5000-8000 line budget."""
import os

BASE = "D:/CW/Data/Skills/nihaisha-perspective"

with open(os.path.join(BASE, "SKILL.full.md"), "r", encoding="utf-8") as f:
    full = f.readlines()

with open(os.path.join(BASE, "SKILL.md"), "r", encoding="utf-8") as f:
    current = f.readlines()

insert_idx = None
for i, line in enumerate(current):
    if "## 深度内容模块（按需加载）" in line:
        insert_idx = i
        break

# Budget breakdown (~6500 lines):
# Current SKILL.md: ~470 lines
# 太阳病条文1-45: ~1300 lines (核心中的核心)
# 太阳病条文46-129: ~3600 lines (完整太阳病)
# 六经各篇总结+十问: ~650 lines
# 金匮精选(浸淫疮+胸痹+妇人): ~500 lines
# 医案精选: ~300 lines
# 针灸+本草核心: ~500 lines
# 闭门课精选: ~200 lines
sections = [
    # 太阳病条文1-45 (最核心) ~1295行
    ("太阳病篇·条文1-45（总纲/中风/伤寒/桂枝汤/麻黄汤/大小青龙）", [
        (124, 354),    # 1-8
        (354, 610),    # 9-24
        (610, 1419),   # 24-45
    ]),
    # 太阳病条文46-129 ~3614行
    ("太阳病篇·条文46-129（小青龙/五苓散/真武汤/小柴胡汤/大柴胡汤）", [
        (1419, 5033),
    ]),
    # 六经各篇 + 总结 + 十问 ~652行
    ("六经各篇·总结·诊病十问", [(5269, 5921)]),
    # 医案精选 (只取前500行) ~500行
    ("医案精选", [(5921, 6421)]),
    # 金匮精选: 只取最关键章节
    # 浸淫疮/黄连粉 (疮痈肠痈篇) + 胸痹心痛 + 妇人妊娠/产后
    ("金匮精选·浸淫疮/胸痹/妇人", [
        (22347, 22966),  # 疮痈肠痈 (含浸淫疮黄连粉!)
        (17617, 18748),  # 胸痹心痛
        (22966, 23574),  # 趾蹶蚘虫+妇人妊娠
        (23574, 24329),  # 妇人产后
    ]),
    # 针灸+本草核心 (取前500行)
    ("针灸·本草核心", [(24926, 25426)]),
    # 闭门课精选 (取前200行)
    ("闭门课精选", [(28131, 28331)]),
]

expanded = []
expanded.extend(current[:insert_idx])

total = 0
for title, ranges in sections:
    expanded.append(f"\n---\n\n## {title}\n\n")
    for start, end in ranges:
        s, e = max(0, start), min(len(full), end)
        expanded.extend(full[s:e])
        total += (e - s)

expanded.extend(current[insert_idx:])

content = "".join(expanded)
lines = content.count("\n")
size_kb = len(content.encode("utf-8")) / 1024

out = os.path.join(BASE, "SKILL.expanded.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Extracted: {total} lines")
print(f"Total: {lines} lines, {size_kb:.1f}KB ({size_kb/1024:.2f}MB)")
print(f"Written to: {out}")

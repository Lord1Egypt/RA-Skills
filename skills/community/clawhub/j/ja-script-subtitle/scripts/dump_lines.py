#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 3a —— 把台本导出为「连续序号 + 原文」清单，供逐条翻译

用法:
    python dump_lines.py <script.txt> [start] [end]

输出:
    <序号>\t<原文>
序号 = 非空行连续编号（1-based），与 align_gen.py / make_srt.py 完全一致。
翻译时照此编号写 zh.json，可彻底避免「台本行号 vs 非空行号」错位。
"""
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
script = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9

n = 0
for raw in open(script, encoding="utf-8"):
    line = raw.strip()
    if not line:
        continue                      # 空行不占号
    n += 1
    if lo <= n <= hi:
        print(f"{n}\t{line}")
print(f"# 共 {n} 条非空行")

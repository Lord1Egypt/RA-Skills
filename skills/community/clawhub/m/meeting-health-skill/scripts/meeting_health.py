#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""会议健康度分析 - 离线脚本。

读取参会发言名册(CSV)与可选纪要(Markdown)，输出会议健康度报告：
发言均衡度、沉默成员、决策产出率，并给改进建议。

纯标准库实现，零第三方依赖。支撑 meeting-health-skill 的"可独立运行"。
"""

import argparse
import csv
import os
import re
import sys
from datetime import date


def load_roster(path):
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                mins = float(r.get("发言分钟") or r.get("minutes") or 0)
            except ValueError:
                mins = 0.0
            rows.append({
                "name": (r.get("成员") or r.get("name") or "").strip(),
                "mins": mins,
                "role": (r.get("角色") or r.get("role") or "").strip(),
            })
    return rows


def analyze(rows):
    if not rows:
        return None
    total = sum(r["mins"] for r in rows) or 1
    avg = total / len(rows)
    mx = max(r["mins"] for r in rows)
    silent = [r["name"] for r in rows if r["mins"] < 2]
    balance = round(mx / avg, 2) if avg > 0 else 0
    return {"total": total, "avg": round(avg, 1), "max": mx,
            "balance": balance, "silent": silent, "n": len(rows)}


def count_decisions(path):
    if not path or not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8", errors="ignore").read()
    return len(re.findall(r"决策|决定|拍板", text))


def render(name, a, dec=None):
    lines = [f"# 会议健康度报告 · {name or date.today()}", ""]
    lines.append(f"- 参会人数：{a['n']}")
    lines.append(f"- 总发言时长：{a['total']} 分钟，人均 {a['avg']} 分钟")
    lines.append(f"- 发言均衡度（最高/人均）：{a['balance']}（>2 提示存在主导者）")
    lines.append(f"- 沉默成员（<2分钟）：{', '.join(a['silent']) if a['silent'] else '无'}")
    if dec is not None:
        per = a["total"] / max(dec, 1)
        lines.append(f"- 决策产出：纪要识别决策/结论 {dec} 处，约每 {per:.0f} 分钟 1 个决策")
    lines.append("")
    lines.append("## 改进建议")
    if a["balance"] > 2:
        lines.append(f"- 控制 {a['max']:.0f} 分钟主导者的发言占比，主动点名沉默成员：{', '.join(a['silent'])}")
    if a["silent"]:
        lines.append(f"- 会前为 {', '.join(a['silent'])} 分配专属议题，明确发言分工")
    if dec is not None and dec == 0:
        lines.append("- 本场未见明确决策，建议会末增加决策确认环节")
    if not a["silent"] and a["balance"] <= 2:
        lines.append("- 发言分布均衡，维持当前节奏")
    lines.append("")
    lines.append("> 由 meeting-health-skill 离线生成，指标为启发式统计（发言时长≠贡献质量），供改进参考。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="会议健康度分析")
    ap.add_argument("--roster", required=True)
    ap.add_argument("--minutes", default=None)
    ap.add_argument("--output", default="健康度报告.md")
    ap.add_argument("--name", default="")
    args = ap.parse_args()

    if not os.path.isfile(args.roster):
        print(f"错误：名册不存在 {args.roster}", file=sys.stderr)
        sys.exit(1)

    rows = load_roster(args.roster)
    a = analyze(rows)
    if a is None:
        print("错误：名册为空", file=sys.stderr)
        sys.exit(1)
    dec = count_decisions(args.minutes)
    out = render(args.name, a, dec)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成健康度报告：{args.output}")


if __name__ == "__main__":
    main()

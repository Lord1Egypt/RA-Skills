#!/usr/bin/env python3
"""内容衰减评分——给老文打分并产出更新优先级。

纯标准库。对齐 references/content-strategy-playbook.md 的「内容衰减检测」。
衰减分 = 发布天数/365*0.4 + 流量跌幅*0.4 + 是否核心*0.2。

用法:
    # 默认内置示例
    python3 scripts/decay_score.py

    # 自定义（每组一一对应，可重复 --title/--days/--drop/--core）
    python3 scripts/decay_score.py \
        --title "出海支付指南" --days 540 --drop 0.62 --core 1 \
        --title "工具横评"     --days  *  --drop 0.45 --core 0

    # 从 STDIN 读：每行 "标题|发布天数|流量跌幅(0-1)|是否核心(1/0)"
    echo "出海支付指南|540|0.62|1" | python3 scripts/decay_score.py
"""
from __future__ import annotations

import argparse
import sys

DEFAULT_ROWS = [
    ("出海支付指南", 540, 0.62, 1),
    ("冷启动复盘", 300, 0.20, 1),
    ("工具横评", 720, 0.45, 0),
]


def score(days: int, drop: float, core: int) -> float:
    """越老、跌越多、越核心 → 分越高，越该更新。"""
    return round(days / 365 * 0.4 + drop * 0.4 + core * 0.2, 2)


def render(rows):
    print("# 内容衰减优先级\n")
    for title, days, drop, core in sorted(rows, key=lambda r: -score(*r[1:])):
        s = score(days, drop, core)
        pri = "高" if s >= 0.6 else ("中" if s >= 0.35 else "低")
        print(f"[{pri}] {title}: 衰减分={s}（天={days}, 跌={int(drop * 100)}%, 核心={core}）")


def main() -> None:
    ap = argparse.ArgumentParser(description="内容衰减评分与更新优先级")
    ap.add_argument("--title", action="append", help="标题（与下面参数配对，可多次）")
    ap.add_argument("--days", type=int, action="append", help="发布天数")
    ap.add_argument("--drop", type=float, action="append", help="流量跌幅 0-1")
    ap.add_argument("--core", type=int, action="append", help="是否核心 1/0")
    args = ap.parse_args()

    rows = DEFAULT_ROWS
    if (args.title and args.days and args.drop and args.core
            and len({len(args.title), len(args.days), len(args.drop), len(args.core)}) == 1):
        rows = list(zip(args.title, args.days, args.drop, args.core))

    if not sys.stdin.isatty():
        extra = []
        for line in sys.stdin:
            line = line.strip()
            if not line or "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4:
                try:
                    extra.append((parts[0], int(parts[1]), float(parts[2]), int(parts[3])))
                except ValueError:
                    continue
        if extra:
            rows = extra

    render(rows)


if __name__ == "__main__":
    main()

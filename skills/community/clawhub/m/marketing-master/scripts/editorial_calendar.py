#!/usr/bin/env python3
"""编辑日历生成器——按主题集群与发布频率输出 Markdown 编辑日历。

纯标准库实现。对齐 references/content-strategy-playbook.md 的「编辑日历生成」。
内容策略先定「结构」（主题集群），再定「节奏」（编辑日历），最后定「维护」（衰减更新）。

用法:
    # 默认：4 个支柱、每 7 天一篇、12 周
    python3 scripts/editorial_calendar.py

    # 自定义
    python3 scripts/editorial_calendar.py --weeks 12 --freq 7 --start 2026-09-01 \
        --pillars "SEO 入门" "文案框架" "着陆页转化" "内容策略"

    # 从 STDIN 读 JSON: {"pillars": [...], "freq": 7, "start": "2026-09-01", "weeks": 12}
    echo '{"weeks":4,"freq":14}' | python3 scripts/editorial_calendar.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta


def build_calendar(pillars, freq, start, weeks):
    cur = start
    lines = [f"# 编辑日历（{start} 起 {weeks} 周，每 {freq} 天一篇）\n"]
    for w in range(weeks):
        pillar = pillars[w % len(pillars)]
        lines.append(f"- **{cur}** · 第 {w + 1} 周 · 主题集群：{pillar}")
        lines.append(f"  - 支柱/支撑：撰写或更新 1 篇，并内链回对应根页面")
        cur += timedelta(days=freq)
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="按主题集群与频率生成 Markdown 编辑日历")
    ap.add_argument("--pillars", nargs="+",
                    default=["SEO 入门", "文案框架", "着陆页转化", "内容策略"],
                    help="主题集群列表")
    ap.add_argument("--freq", type=int, default=7, help="发布间隔天数")
    ap.add_argument("--start", default="2026-09-01", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--weeks", type=int, default=12, help="生成周数")
    args = ap.parse_args()

    pillars = list(args.pillars)
    freq = args.freq
    start = date.fromisoformat(args.start)
    weeks = args.weeks

    # 支持 STDIN 覆盖（JSON）
    if not sys.stdin.isatty():
        try:
            cfg = json.loads(sys.stdin.read() or "{}")
            pillars = cfg.get("pillars", pillars)
            freq = cfg.get("freq", freq)
            start = date.fromisoformat(cfg.get("start", args.start))
            weeks = cfg.get("weeks", weeks)
        except (json.JSONDecodeError, ValueError):
            pass  # 解析失败则沿用参数默认值

    print(build_calendar(pillars, freq, start, weeks))


if __name__ == "__main__":
    main()

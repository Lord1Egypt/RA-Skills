#!/usr/bin/env python3
"""
信号追踪器：比较两日扫描结果，追踪信号变化。

功能：
- 加载今日与昨日信号 JSON 文件
- 分类为 NEW / GONE / UPGRADED / DOWNGRADED / SAME
- 输出带颜色差异报告
- 记录差异历史到 signal_history.jsonl
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colors import RED, GREEN, YELLOW, CYAN, BOLD, GRAY, RESET

# 变体强度排名（越小越弱，E与D同级）
VARIANT_RANK = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 4}


def load_signals(filepath: str) -> dict[str, dict]:
    """从 JSON 文件加载信号，按 code 建索引。每行一个 JSON 对象。"""
    signals = {}
    if not os.path.exists(filepath):
        print(f"{YELLOW}警告：文件不存在 — {filepath}{RESET}", file=sys.stderr)
        return signals

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                print(f"{YELLOW}警告：跳过无效 JSON 行 — {line[:80]}{RESET}", file=sys.stderr)
                continue
            code = obj.get("code")
            if code:
                signals[code] = obj
    return signals


def variant_stronger(new_variant: str, old_variant: str) -> bool:
    """判断新变体是否比旧变体更强。"""
    return VARIANT_RANK.get(new_variant, 0) > VARIANT_RANK.get(old_variant, 0)


def variant_weaker(new_variant: str, old_variant: str) -> bool:
    """判断新变体是否比旧变体更弱。"""
    return VARIANT_RANK.get(new_variant, 0) < VARIANT_RANK.get(old_variant, 0)


def compare_signals(today: dict, yesterday: dict) -> dict:
    """比较两日信号，返回分类结果。"""
    all_codes = set(today.keys()) | set(yesterday.keys())

    new_signals = []
    gone_signals = []
    upgraded = []
    downgraded = []
    same = []

    for code in sorted(all_codes):
        in_today = code in today
        in_yesterday = code in yesterday

        if in_today and not in_yesterday:
            new_signals.append(today[code])
        elif not in_today and in_yesterday:
            gone_signals.append(yesterday[code])
        else:
            t_var = today[code].get("variant", "")
            y_var = yesterday[code].get("variant", "")
            t_score = today[code].get("score", 0)
            y_score = yesterday[code].get("score", 0)

            if variant_stronger(t_var, y_var):
                upgraded.append({
                    "code": code,
                    "name": today[code].get("name", ""),
                    "old_variant": y_var,
                    "new_variant": t_var,
                    "old_score": y_score,
                    "new_score": t_score,
                    "anchor_date": today[code].get("anchor_date", ""),
                })
            elif variant_weaker(t_var, y_var):
                downgraded.append({
                    "code": code,
                    "name": today[code].get("name", ""),
                    "old_variant": y_var,
                    "new_variant": t_var,
                    "old_score": y_score,
                    "new_score": t_score,
                    "anchor_date": today[code].get("anchor_date", ""),
                })
            else:
                same.append({
                    "code": code,
                    "name": today[code].get("name", ""),
                    "variant": t_var,
                    "old_score": y_score,
                    "new_score": t_score,
                    "anchor_date": today[code].get("anchor_date", ""),
                })

    return {
        "new": new_signals,
        "gone": gone_signals,
        "upgraded": upgraded,
        "downgraded": downgraded,
        "same": same,
    }


def print_report(diff: dict, today_label: str, yesterday_label: str):
    """输出带颜色差异报告。"""
    new_count = len(diff["new"])
    gone_count = len(diff["gone"])
    up_count = len(diff["upgraded"])
    down_count = len(diff["downgraded"])
    same_count = len(diff["same"])
    total = sum([new_count, gone_count, up_count, down_count, same_count])

    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  信号追踪报告  {today_label} vs {yesterday_label}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print()
    print(f"  {GREEN}NEW         {new_count:>4}{RESET}")
    print(f"  {RED}GONE         {gone_count:>4}{RESET}")
    print(f"  {CYAN}UPGRADED     {up_count:>4}{RESET}")
    print(f"  {YELLOW}DOWNGRADED   {down_count:>4}{RESET}")
    print(f"  {GRAY}SAME         {same_count:>4}{RESET}")
    print(f"  {'─' * 22}")
    print(f"  TOTAL        {total:>4}")
    print()

    # NEW
    if diff["new"]:
        print(f"{GREEN}{BOLD}  NEW ({new_count}){RESET}")
        print(f"  {GREEN}{'─' * 55}{RESET}")
        for s in diff["new"]:
            print(f"  {GREEN}+ {s['code']}  {s['name']:<8s}  [{s['variant']}] {s['label']:<8s}  score={s['score']:.0f}{RESET}")
        print()

    # GONE
    if diff["gone"]:
        print(f"{RED}{BOLD}  GONE ({gone_count}){RESET}")
        print(f"  {RED}{'─' * 55}{RESET}")
        for s in diff["gone"]:
            print(f"  {RED}- {s['code']}  {s['name']:<8s}  [{s['variant']}] {s['label']:<8s}  score={s['score']:.0f}{RESET}")
        print()

    # UPGRADED
    if diff["upgraded"]:
        print(f"{CYAN}{BOLD}  UPGRADED ({up_count}){RESET}")
        print(f"  {CYAN}{'─' * 55}{RESET}")
        for s in diff["upgraded"]:
            print(
                f"  {CYAN}^ {s['code']}  {s['name']:<8s}"
                f"  {s['old_variant']}→{s['new_variant']}"
                f"  {s['old_score']:.0f}→{s['new_score']:.0f}{RESET}"
            )
        print()

    # DOWNGRADED
    if diff["downgraded"]:
        print(f"{YELLOW}{BOLD}  DOWNGRADED ({down_count}){RESET}")
        print(f"  {YELLOW}{'─' * 55}{RESET}")
        for s in diff["downgraded"]:
            print(
                f"  {YELLOW}v {s['code']}  {s['name']:<8s}"
                f"  {s['old_variant']}→{s['new_variant']}"
                f"  {s['old_score']:.0f}→{s['new_score']:.0f}{RESET}"
            )
        print()

    # SAME (compact)
    if diff["same"]:
        print(f"{GRAY}  SAME ({same_count}): ", end="")
        codes = [s["code"] for s in diff["same"]]
        if len(codes) <= 20:
            print(", ".join(codes), end="")
        else:
            print(", ".join(codes[:10]) + f" ... (+{len(codes) - 10} more)", end="")
        print(f"{RESET}")
        print()


def append_history(data_dir: str, date_str: str, diff: dict):
    """将当日差异追加写入 signal_history.jsonl。"""
    history_path = os.path.join(data_dir, "signal_history.jsonl")
    record = {
        "date": date_str,
        "new_count": len(diff["new"]),
        "gone_count": len(diff["gone"]),
        "upgraded_count": len(diff["upgraded"]),
        "downgraded_count": len(diff["downgraded"]),
        "same_count": len(diff["same"]),
        "new": [s["code"] for s in diff["new"]],
        "gone": [s["code"] for s in diff["gone"]],
        "upgraded": [
            {"code": s["code"], "old": s["old_variant"], "new": s["new_variant"]}
            for s in diff["upgraded"]
        ],
        "downgraded": [
            {"code": s["code"], "old": s["old_variant"], "new": s["new_variant"]}
            for s in diff["downgraded"]
        ],
    }
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def extract_date_from_path(filepath: str) -> Optional[str]:
    """从文件路径中提取 YYYYMMDD 日期。"""
    basename = os.path.basename(filepath)
    parts = basename.replace(".json", "").split("_")
    for part in parts:
        if len(part) == 8 and part.isdigit():
            return part
    return None


def yesterday_from_today(today_date: str) -> str:
    """从今日日期推算前一个自然日（简单减1天）。"""
    dt = datetime.strptime(today_date, "%Y%m%d")
    prev = dt - timedelta(days=1)
    return prev.strftime("%Y%m%d")


def auto_detect_yesterday(today_path: str) -> Optional[str]:
    """根据今日文件路径自动检测昨日文件。"""
    today_date = extract_date_from_path(today_path)
    if not today_date:
        return None

    data_dir = os.path.dirname(today_path) or "data"
    yesterday_date = yesterday_from_today(today_date)

    candidate = os.path.join(data_dir, f"signals_{yesterday_date}.json")
    if os.path.exists(candidate):
        return candidate
    return None


def main():
    parser = argparse.ArgumentParser(
        description="信号追踪器 — 比较两日扫描结果，追踪信号变化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python signal_tracker.py --today data/signals_20260803.json --yesterday data/signals_20260802.json
  python signal_tracker.py --today data/signals_20260803.json        # 自动检测昨日
        """,
    )
    parser.add_argument(
        "--today", required=True, help="今日信号 JSON 文件路径"
    )
    parser.add_argument(
        "--yesterday", default=None, help="昨日信号 JSON 文件路径（可选，自动检测）"
    )
    parser.add_argument(
        "--no-history", action="store_true", help="不写入 signal_history.jsonl"
    )
    args = parser.parse_args()

    # 确定昨日文件
    yesterday_path = args.yesterday
    if not yesterday_path:
        yesterday_path = auto_detect_yesterday(args.today)
        if not yesterday_path:
            print(
                f"{RED}错误：未指定 --yesterday 且无法自动检测昨日文件{RESET}",
                file=sys.stderr,
            )
            sys.exit(1)

    today_label = extract_date_from_path(args.today) or args.today
    yesterday_label = extract_date_from_path(yesterday_path) or yesterday_path

    print(f"{GRAY}今日文件：{args.today}{RESET}")
    print(f"{GRAY}昨日文件：{yesterday_path}{RESET}")

    # 加载信号
    today_signals = load_signals(args.today)
    yesterday_signals = load_signals(yesterday_path)

    if not today_signals:
        print(f"{RED}错误：今日文件中无有效信号{RESET}", file=sys.stderr)
        sys.exit(1)

    # 比较
    diff = compare_signals(today_signals, yesterday_signals)

    # 输出报告
    print_report(diff, today_label, yesterday_label)

    # 写入历史
    if not args.no_history:
        data_dir = os.path.dirname(args.today) or "data"
        append_history(data_dir, today_label, diff)
        print(
            f"{GRAY}差异历史已追加至 {os.path.join(data_dir, 'signal_history.jsonl')}{RESET}"
        )

    # 返回码
    has_changes = (
        diff["new"] or diff["gone"] or diff["upgraded"] or diff["downgraded"]
    )
    if has_changes:
        print(f"{BOLD}状态：有变化{RESET}")
    else:
        print(f"{GRAY}状态：无变化{RESET}")


if __name__ == "__main__":
    main()

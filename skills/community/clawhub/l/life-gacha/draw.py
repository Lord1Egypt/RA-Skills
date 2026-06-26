#!/usr/bin/env python3
"""每日抽卡 — 随机抽取今日任务，写入周记，通知用户

用法：
    python3 draw.py              # 按 config 正常抽卡
    python3 draw.py -n 2         # 指定抽 2 张（覆盖 config 数量）
    python3 draw.py --extra 1    # 在今日已有卡基础上再抽 1 张
    python3 draw.py --reroll     # 重抽今日（替换已有记录）
"""

import argparse
import random
import re
import sys
from datetime import date
from pathlib import Path

import yaml

CONFIG_FILE = Path(__file__).parent / "config.yaml"
DATA_DIR = Path(__file__).parent / "data"
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_holiday(today: date) -> bool:
    return today.weekday() >= 5


def get_week_file(today: date) -> Path:
    week_num = today.isocalendar()[1]
    month_dir = DATA_DIR / today.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    return month_dir / f"week-{week_num:02d}.md"


def day_label(today: date) -> str:
    return f"{today.strftime('%Y-%m-%d')} {WEEKDAY_CN[today.weekday()]}"


def get_existing_cards(week_file: Path, today: date) -> list[str]:
    """读取今日已有的扭蛋卡片列表"""
    if not week_file.exists():
        return []
    content = week_file.read_text(encoding="utf-8")
    marker = f"## {day_label(today)}"
    if marker not in content:
        return []
    idx = content.index(marker)
    section = content[idx:]
    # 截到下一个 ## 或文件尾
    next_section = re.search(r"\n## ", section[3:])
    if next_section:
        section = section[: next_section.start() + 3]
    cards = re.findall(r"^- (.+)$", section, re.MULTILINE)
    return cards


def write_entry(week_file: Path, today: date, cards: list[str]):
    """新增今日条目到文件末尾"""
    cards_md = "\n".join(f"- {c}" for c in cards)
    entry = (
        f"## {day_label(today)}\n\n"
        f"**今日扭蛋**\n\n{cards_md}\n\n"
        f"**今日小记**\n\n（待填写）\n\n---\n\n"
    )
    with open(week_file, "a", encoding="utf-8") as f:
        f.write(entry)


def replace_today_entry(week_file: Path, today: date, cards: list[str]):
    """替换已有的今日条目（reroll 用）"""
    content = week_file.read_text(encoding="utf-8")
    marker = f"## {day_label(today)}"
    idx = content.index(marker)
    before = content[:idx]
    after = content[idx:]
    # 截掉今日段落，保留后续内容
    next_section = re.search(r"\n## ", after[3:])
    remaining = after[next_section.start() + 3 :] if next_section else ""

    cards_md = "\n".join(f"- {c}" for c in cards)
    new_entry = (
        f"## {day_label(today)}\n\n"
        f"**今日扭蛋**\n\n{cards_md}\n\n"
        f"**今日小记**\n\n（待填写）\n\n---\n\n"
    )
    week_file.write_text(before + new_entry + remaining, encoding="utf-8")


def append_cards_to_today(week_file: Path, today: date, new_cards: list[str]):
    """在今日已有卡片列表末尾追加新卡（extra 用）"""
    content = week_file.read_text(encoding="utf-8")
    marker = f"## {day_label(today)}"
    idx = content.index(marker)
    # 找到 **今日扭蛋** 块的末尾（第一个空行后的位置）
    cards_block_end = re.search(
        r"(\*\*今日扭蛋\*\*\n\n(?:- .+\n)+)",
        content[idx:],
    )
    if not cards_block_end:
        print("❌ 今日扭蛋区块格式异常，无法追加")
        sys.exit(1)
    insert_pos = idx + cards_block_end.end()
    addition = "".join(f"- {c}\n" for c in new_cards)
    week_file.write_text(content[:insert_pos] + addition + content[insert_pos:], encoding="utf-8")


def print_cards(today: date, cards: list[str], day_type: str, mode: str = ""):
    label = f"（{mode}）" if mode else ""
    print(f"🎴 {today.strftime('%Y年%m月%d日')}（{day_type}）今日扭蛋{label}：")
    for card in cards:
        print(f"  ✨ {card}")


def main():
    parser = argparse.ArgumentParser(description="人生扭蛋 — 每日抽卡")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--count", type=int, help="指定抽卡数量（覆盖 config）")
    group.add_argument("--extra", type=int, metavar="N", help="在今日已有基础上再抽 N 张")
    group.add_argument("--reroll", action="store_true", help="重抽今日（替换已有记录）")
    args = parser.parse_args()

    today = date.today()
    config = load_config()
    rules = config["draw_rules"]
    holiday = is_holiday(today)
    raw_pool = config["holiday_pool"] if holiday else config["workday_pool"]
    day_type = "休息日" if holiday else "工作日"
    week_file = get_week_file(today)

    def weighted_sample(pool: list, count: int, exclude: list[str] = None) -> list[str]:
        """按权重无放回抽样，排除 exclude 中已有的项"""
        candidates = [e for e in pool if e["item"] not in (exclude or [])]
        items = [e["item"] for e in candidates]
        weights = [e.get("weight", 3) for e in candidates]
        result = []
        for _ in range(min(count, len(items))):
            chosen = random.choices(items, weights=weights, k=1)[0]
            idx = items.index(chosen)
            result.append(chosen)
            items.pop(idx)
            weights.pop(idx)
        return result

    if args.extra:
        # 再抽 N 张：排除已有卡片，避免重复
        existing = get_existing_cards(week_file, today)
        if not existing:
            print("❌ 今日还没有抽卡记录，请先运行 draw.py 正常抽卡")
            sys.exit(1)
        new_cards = weighted_sample(raw_pool, args.extra, exclude=existing)
        append_cards_to_today(week_file, today, new_cards)
        print_cards(today, new_cards, day_type, mode=f"再抽 {args.extra} 张")
        print(f"已追加到今日记录：{week_file}")

    elif args.reroll:
        # 重抽：替换今日记录
        existing = get_existing_cards(week_file, today)
        count = rules["holiday"] if holiday else rules["workday"]
        cards = weighted_sample(raw_pool, count)
        if existing:
            replace_today_entry(week_file, today, cards)
            print_cards(today, cards, day_type, mode="重抽")
        else:
            write_entry(week_file, today, cards)
            print_cards(today, cards, day_type)
        print(f"已更新到：{week_file}")

    else:
        # 正常抽卡
        count = args.count if args.count else (rules["holiday"] if holiday else rules["workday"])
        existing = get_existing_cards(week_file, today)
        if existing:
            print(f"⚠️  今日已抽过卡，如需重抽请用 --reroll，再抽请用 --extra N")
            print_cards(today, existing, day_type, mode="已有")
            sys.exit(0)
        cards = weighted_sample(raw_pool, count)
        write_entry(week_file, today, cards)
        print_cards(today, cards, day_type)
        print(f"\n已记录到 {week_file}")


if __name__ == "__main__":
    main()

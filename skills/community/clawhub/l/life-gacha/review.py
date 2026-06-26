#!/usr/bin/env python3
"""周回顾 — 读取本周记录，生成鼓励性总结，追加到周记末尾"""

import re
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def get_week_file(today: date) -> Path:
    week_num = today.isocalendar()[1]
    return DATA_DIR / today.strftime("%Y-%m") / f"week-{week_num:02d}.md"


def parse_entries(content: str) -> list[dict]:
    entries = []
    sections = re.split(r"(?=^## \d{4}-\d{2}-\d{2})", content, flags=re.MULTILINE)
    for section in sections:
        if not section.strip() or section.startswith("# 本周回顾"):
            continue
        cards = re.findall(r"^- (.+)$", section, re.MULTILINE)
        note_match = re.search(r"\*\*今日小记\*\*\n\n(.+?)(?:\n---|\Z)", section, re.DOTALL)
        note = note_match.group(1).strip() if note_match else ""
        header_match = re.match(r"## (.+)", section)
        day_label = header_match.group(1).strip() if header_match else ""
        if day_label:
            entries.append({"day": day_label, "cards": cards, "note": note})
    return entries


def format_review(entries: list[dict], today: date) -> str:
    week_num = today.isocalendar()[1]
    total_cards = sum(len(e["cards"]) for e in entries)
    filled_days = sum(1 for e in entries if e["note"] and e["note"] != "（待填写）")

    lines = [
        f"# 本周回顾（第 {week_num} 周）",
        "",
        f"这周你一共解锁了 **{total_cards} 个扭蛋任务**，有 **{filled_days} 天** 留下了记录。",
        "",
    ]

    for entry in entries:
        note = entry["note"]
        if not entry["cards"] and (not note or note == "（待填写）"):
            continue
        lines.append(f"**{entry['day']}**")
        for card in entry["cards"]:
            lines.append(f"  🎴 {card}")
        if note and note != "（待填写）":
            snippet = note[:60] + "..." if len(note) > 60 else note
            lines.append(f"  💬 {snippet}")
        lines.append("")

    lines += [
        "---",
        "",
        "每一件小事都算数，哪怕只是出门走了走，也是给生活留下了一个记忆点。",
        "下周继续，期待更多有趣的扭蛋 🌸",
    ]
    return "\n".join(lines)


def main():
    today = date.today()
    week_file = get_week_file(today)

    if not week_file.exists():
        print("本周暂无记录，期待下周一起扭蛋 🌟")
        return

    content = week_file.read_text(encoding="utf-8")

    if "# 本周回顾" in content:
        print("⚠️  本周回顾已生成，不重复追加")
        # 还是打印出来让用户看到
        idx = content.index("# 本周回顾")
        print(content[idx:])
        return

    entries = parse_entries(content)
    review = format_review(entries, today)

    with open(week_file, "a", encoding="utf-8") as f:
        f.write(f"\n{review}\n")

    print(review)
    print(f"\n✅ 已追加到 {week_file}")


if __name__ == "__main__":
    main()

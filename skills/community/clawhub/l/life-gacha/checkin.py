#!/usr/bin/env python3
"""每日回访 — 将用户回答填入今日周记的空白处

用法：
    python3 checkin.py "今天散步做到了，读书没来得及"
"""

import sys
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
PLACEHOLDER = "（待填写）"


def get_week_file(today: date) -> Path:
    week_num = today.isocalendar()[1]
    return DATA_DIR / today.strftime("%Y-%m") / f"week-{week_num:02d}.md"


def fill_today_checkin(response: str):
    today = date.today()
    week_file = get_week_file(today)

    if not week_file.exists():
        print(f"❌ 找不到今日记录：{week_file}")
        sys.exit(1)

    content = week_file.read_text(encoding="utf-8")

    # 找到今日的段落，把占位符替换成用户回答
    day_label = f"{today.strftime('%Y-%m-%d')} {WEEKDAY_CN[today.weekday()]}"
    marker = f"## {day_label}"

    if marker not in content:
        print(f"❌ 今日条目未找到（{day_label}），请先运行 draw.py")
        sys.exit(1)

    # 只替换今日段落内第一个占位符
    idx = content.index(marker)
    before = content[:idx]
    after = content[idx:]
    updated_after = after.replace(PLACEHOLDER, response, 1)

    if updated_after == after:
        print("⚠️  今日小记已填写，无需重复记录")
        return

    week_file.write_text(before + updated_after, encoding="utf-8")
    print(f"✅ 今日小记已记录：{week_file}")


def main():
    if len(sys.argv) < 2:
        print("用法：python3 checkin.py \"你今天的回答\"")
        sys.exit(1)

    response = " ".join(sys.argv[1:]).strip()
    fill_today_checkin(response)


if __name__ == "__main__":
    main()

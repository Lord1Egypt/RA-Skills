#!/usr/bin/env python3
"""
LeetCode 错题本管理脚本
用法:
  python3 manage_errors.py add <day> <problem_id> <problem_title> <type> <reason> <core_idea> <similar>
  python3 manage_errors.py review <today_day>
  python3 manage_errors.py list
"""

import sys
import json
import os
from datetime import datetime

ERRORSET_PATH = os.path.join(os.getcwd(), "errorset.md")


def parse_errorset():
    if not os.path.exists(ERRORSET_PATH):
        return []
    errors = []
    with open(ERRORSET_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = content.split("---")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        entry = {}
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("题号："):
                entry["problem_id"] = line[3:].strip()
            elif line.startswith("标题："):
                entry["title"] = line[3:].strip()
            elif line.startswith("类型："):
                entry["type"] = line[3:].strip()
            elif line.startswith("错误原因："):
                entry["reason"] = line[5:].strip()
            elif line.startswith("核心思路："):
                entry["core_idea"] = line[5:].strip()
            elif line.startswith("相似题："):
                entry["similar"] = line[4:].strip()
            elif line.startswith("记录日期（第"):
                day_str = line.replace("记录日期（第", "").replace("天）：", "").strip()
                try:
                    entry["record_day"] = int(day_str)
                except ValueError:
                    entry["record_day"] = 0
            elif line.startswith("待复习日（D）："):
                days_str = line[8:].strip()
                try:
                    entry["review_days"] = [int(d.strip()) for d in days_str.split(",") if d.strip()]
                except ValueError:
                    entry["review_days"] = []
        if entry.get("problem_id"):
            errors.append(entry)
    return errors


def write_errorset(errors):
    lines = ["# LeetCode 错题本\n"]
    for e in errors:
        lines.append("---\n")
        lines.append(f"题号：{e.get('problem_id', '')}\n")
        lines.append(f"标题：{e.get('title', '')}\n")
        lines.append(f"类型：{e.get('type', '')}\n")
        lines.append(f"错误原因：{e.get('reason', '')}\n")
        lines.append(f"核心思路：{e.get('core_idea', '')}\n")
        lines.append(f"相似题：{e.get('similar', '')}\n")
        lines.append(f"记录日期（第{e.get('record_day', 0)}天）：{datetime.now().strftime('%Y-%m-%d')}\n")
        review_days = e.get("review_days", [])
        lines.append(f"待复习日（D）：{', '.join(str(d) for d in review_days)}\n")
        lines.append("\n")
    with open(ERRORSET_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)


def add_error(day, problem_id, title, error_type, reason, core_idea, similar):
    errors = parse_errorset()
    day = int(day)
    review_days = [day + 1, day + 3, day + 7]
    entry = {
        "problem_id": problem_id,
        "title": title,
        "type": error_type,
        "reason": reason,
        "core_idea": core_idea,
        "similar": similar,
        "record_day": day,
        "review_days": review_days,
    }
    errors.append(entry)
    write_errorset(errors)
    print(f"已记录错题：{problem_id} {title}")
    print(f"复习计划：第 {review_days[0]} 天、第 {review_days[1]} 天、第 {review_days[2]} 天")


def get_review_for_day(today_day):
    errors = parse_errorset()
    today_day = int(today_day)
    due = [e for e in errors if today_day in e.get("review_days", [])]
    if not due:
        print(f"第 {today_day} 天没有待复习的错题。")
        return
    print(f"第 {today_day} 天待复习错题（{len(due)} 题）：\n")
    for e in due:
        print(f"  题号：{e['problem_id']}  标题：{e.get('title', '')}  类型：{e['type']}")
        print(f"  核心思路：{e['core_idea']}")
        print(f"  相似题：{e['similar']}")
        print()


def list_errors():
    errors = parse_errorset()
    if not errors:
        print("错题本为空。")
        return
    print(f"共 {len(errors)} 道错题：\n")
    for e in errors:
        review_days = ", ".join(f"D{d}" for d in e.get("review_days", []))
        print(f"  D{e.get('record_day')}  {e['problem_id']} {e.get('title', '')}  [{e['type']}]  复习：{review_days}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 9:
        add_error(*sys.argv[2:9])
    elif cmd == "review" and len(sys.argv) >= 3:
        get_review_for_day(sys.argv[2])
    elif cmd == "list":
        list_errors()
    else:
        print(__doc__)
        sys.exit(1)

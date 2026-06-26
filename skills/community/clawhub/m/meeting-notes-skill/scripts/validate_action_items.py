#!/usr/bin/env python3
"""
Validate Action Items table in meeting minutes markdown.

Hard rules:
- Must contain Action Items table with columns:
  任务项 | 负责人 | 交付物/截止日期 | 备注
- 负责人 cannot be empty/待指定
- 交付物/截止日期 cannot be empty/待确认
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EMPTY_TOKENS = {"", "-", "待指定", "待确认", "tbd", "n/a", "na"}


def normalize_cell(s: str) -> str:
    return re.sub(r"\s+", "", s.strip().lower())


def find_action_items_table(lines: list[str]) -> tuple[int, list[str]] | tuple[None, None]:
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## action items") or line.strip().lower().startswith("### action items"):
            start = i
            break
    if start is None:
        return None, None

    table = []
    for j in range(start + 1, len(lines)):
        l = lines[j].rstrip("\n")
        if l.strip().startswith("|"):
            table.append(l)
        elif table:
            break
    if not table:
        return None, None
    return start, table


def validate(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    section_line, table = find_action_items_table(lines)
    if table is None:
        print("FAIL: missing Action Items table", file=sys.stderr)
        return 2

    if len(table) < 2:
        print("FAIL: Action Items table is incomplete", file=sys.stderr)
        return 2

    header = [c.strip() for c in table[0].strip().strip("|").split("|")]
    required = ["任务项", "负责人", "交付物/截止日期", "备注"]
    if header[:4] != required:
        print(f"FAIL: invalid Action Items header: {header}", file=sys.stderr)
        print(f"Expected: {required}", file=sys.stderr)
        return 2

    issues = []
    for idx, row in enumerate(table[2:], start=3):  # markdown line index within table (1-based human-like)
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        task, owner, due, _note = cells[:4]
        # Skip fully empty template rows
        if not any(cells[:4]):
            continue
        if normalize_cell(owner) in EMPTY_TOKENS:
            issues.append(f"line {section_line + idx}: missing owner for task '{task}'")
        if normalize_cell(due) in EMPTY_TOKENS:
            issues.append(f"line {section_line + idx}: missing deliverable/deadline for task '{task}'")

    if issues:
        print("FAIL: Action Items hard gate not met", file=sys.stderr)
        for i in issues:
            print(f"- {i}", file=sys.stderr)
        return 2

    print("PASS: Action Items hard gate")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("minutes_file", help="Path to markdown meeting minutes")
    args = ap.parse_args()
    p = Path(args.minutes_file).expanduser().resolve()
    if not p.exists():
        print(f"FAIL: file not found: {p}", file=sys.stderr)
        return 2
    return validate(p)


if __name__ == "__main__":
    raise SystemExit(main())

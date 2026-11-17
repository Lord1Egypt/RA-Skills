#!/usr/bin/env python3
"""Validate JSONL primary data against its generated Markdown view.

Usage:
  python validate_dual_view.py knowledge_assets.jsonl knowledge_assets.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED = {
    "id",
    "question",
    "retrieval_text",
    "answer_text",
    "module",
    "status",
    "version",
}


def load_items(path: Path) -> list[dict]:
    items = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL 第 {line_no} 行无法解析: {exc}") from exc
        missing = sorted(REQUIRED - item.keys())
        if missing:
            raise ValueError(f"JSONL 第 {line_no} 行缺少字段: {', '.join(missing)}")
        items.append(item)
    return items


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python validate_dual_view.py <input.jsonl> <view.md>", file=sys.stderr)
        return 2
    jsonl_path, md_path = map(Path, sys.argv[1:])
    items = load_items(jsonl_path)
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("JSONL 存在重复 ID")
    md = md_path.read_text(encoding="utf-8")
    missing = [item["id"] for item in items if md.count(f"### {item['id']}｜") != 1]
    if missing:
        raise ValueError(f"Markdown 缺少或重复条目: {missing[:10]}")
    markdown_ids = re.findall(r"^### ([^｜]+)｜", md, flags=re.MULTILINE)
    extra = sorted(set(markdown_ids) - set(ids))
    if extra:
        raise ValueError(f"Markdown 出现 JSONL 没有的 ID: {extra[:10]}")
    for item in items:
        checks = {
            "question": item["question"],
            "retrieval_text": item["retrieval_text"],
            "module": f"- **模块**：{item['module']}",
            "status": f"- **状态**：`{item['status']}`",
            "version": f"- **版本**：`{item['version']}`",
        }
        for field, expected in checks.items():
            if expected not in md:
                raise ValueError(f"Markdown 未同步字段 {field}: {item['id']}")
    print(f"dual_view_validation_pass: {len(items)} items, ids and core fields synchronized")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"dual_view_validation_failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

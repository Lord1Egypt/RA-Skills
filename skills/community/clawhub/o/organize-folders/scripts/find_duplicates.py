#!/usr/bin/env python3
"""查找重复文件候选；默认只输出候选，不删除。"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from orglib import configure_stdout, markdown_table, now_iso, write_json


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(root: Path, mode: str) -> dict:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
            key = (path.name.lower(), stat.st_size)
            if mode == "hash":
                key = (stat.st_size, file_hash(path))
            groups[key].append(str(path))
        except OSError:
            continue

    duplicates = [{"key": list(key), "paths": paths, "count": len(paths)} for key, paths in groups.items() if len(paths) > 1]
    return {"version": 1, "generated_at": now_iso(), "root": str(root), "mode": mode, "groups": duplicates}


def to_markdown(data: dict) -> str:
    rows = []
    for group in data["groups"]:
        rows.append([group["count"], "<br>".join(group["paths"])])
    return "\n".join(
        [
            "# 重复文件候选",
            "",
            f"- 根目录：`{data['root']}`",
            f"- 模式：`{data['mode']}`",
            f"- 候选组数：`{len(data['groups'])}`",
            "",
            markdown_table(["数量", "路径"], rows),
            "",
            "> 此清单只用于人工确认，不自动删除。",
            "",
        ]
    )


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="查找重复文件候选。")
    parser.add_argument("path", help="要扫描的目录")
    parser.add_argument("--mode", choices=["fast", "hash"], default="fast", help="fast=文件名+大小，hash=大小+哈希")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    data = find_duplicates(Path(args.path).expanduser().resolve(), args.mode)
    text = to_markdown(data) if args.format == "markdown" else json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        if args.format == "json":
            write_json(args.output, data)
        else:
            Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""为文件夹整理规划生成只读目录清单。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_EXCLUDES = {
    "$RECYCLE.BIN",
    "System Volume Information",
    ".git",
    "node_modules",
    "__pycache__",
}


def human_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{size} B"


def iso_time(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).isoformat(timespec="seconds")


def should_exclude(name: str, excludes: set[str]) -> bool:
    return name in excludes


def safe_stat(path: Path) -> os.stat_result | None:
    try:
        return path.stat()
    except OSError:
        return None


def add_top(items: list[dict[str, Any]], item: dict[str, Any], limit: int, key: str) -> None:
    items.append(item)
    items.sort(key=lambda row: row[key], reverse=True)
    del items[limit:]


def scan(
    root: Path,
    top_limit: int,
    recent_limit: int,
    new_limit: int,
    excludes: set[str],
    since_days: int | None,
) -> dict[str, Any]:
    since_timestamp = None
    if since_days is not None:
        since_timestamp = time.time() - since_days * 24 * 60 * 60

    summary: dict[str, Any] = {
        "root": str(root),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": 0,
        "directories": 0,
        "size_bytes": 0,
        "errors": [],
        "top_level": {},
        "extensions": Counter(),
        "extension_sizes": defaultdict(int),
        "largest_files": [],
        "recent_files": [],
        "new_files": [],
        "since_days": since_days,
    }

    if not root.exists():
        raise SystemExit(f"路径不存在：{root}")

    def record_error(path: Path, error: OSError) -> None:
        summary["errors"].append({"path": str(path), "error": str(error)})

    def top_bucket(path: Path, *, is_file: bool) -> str:
        try:
            rel = path.relative_to(root)
        except ValueError:
            return "."
        if not rel.parts:
            return "."
        if is_file and len(rel.parts) == 1:
            return "[根目录文件]"
        return rel.parts[0]

    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    name = entry.name
                    if should_exclude(name, excludes):
                        continue

                    try:
                        if entry.is_dir(follow_symlinks=False):
                            summary["directories"] += 1
                            bucket = top_bucket(path, is_file=False)
                            top = summary["top_level"].setdefault(
                                bucket,
                                {
                                    "name": bucket,
                                    "path": str(root / bucket) if bucket != "." else str(root),
                                    "files": 0,
                                    "directories": 0,
                                    "size_bytes": 0,
                                    "last_modified": None,
                                },
                            )
                            top["directories"] += 1
                            stat = safe_stat(path)
                            if stat:
                                previous = top["last_modified"]
                                if previous is None or stat.st_mtime > previous:
                                    top["last_modified"] = stat.st_mtime
                            stack.append(path)
                        elif entry.is_file(follow_symlinks=False):
                            stat = safe_stat(path)
                            if not stat:
                                continue
                            size = stat.st_size
                            summary["files"] += 1
                            summary["size_bytes"] += size

                            bucket = top_bucket(path, is_file=True)
                            top = summary["top_level"].setdefault(
                                bucket,
                                {
                                    "name": bucket,
                                    "path": str(root / bucket) if bucket != "." else str(root),
                                    "files": 0,
                                    "directories": 0,
                                    "size_bytes": 0,
                                    "last_modified": None,
                                },
                            )
                            top["files"] += 1
                            top["size_bytes"] += size
                            if top["last_modified"] is None or stat.st_mtime > top["last_modified"]:
                                top["last_modified"] = stat.st_mtime

                            ext = path.suffix.lower() or "[无扩展名]"
                            summary["extensions"][ext] += 1
                            summary["extension_sizes"][ext] += size

                            file_item = {
                                "path": str(path),
                                "size_bytes": size,
                                "size": human_size(size),
                                "last_modified": iso_time(stat.st_mtime),
                                "last_modified_timestamp": stat.st_mtime,
                            }
                            add_top(summary["largest_files"], dict(file_item), top_limit, "size_bytes")
                            add_top(summary["recent_files"], dict(file_item), recent_limit, "last_modified_timestamp")
                            if since_timestamp is not None and stat.st_mtime >= since_timestamp:
                                add_top(summary["new_files"], dict(file_item), new_limit, "last_modified_timestamp")
                    except OSError as error:
                        record_error(path, error)
        except OSError as error:
            record_error(current, error)

    top_rows = []
    for row in summary["top_level"].values():
        row = dict(row)
        row["size"] = human_size(row["size_bytes"])
        row["last_modified"] = iso_time(row["last_modified"])
        top_rows.append(row)
    top_rows.sort(key=lambda row: row["size_bytes"], reverse=True)
    summary["top_level"] = top_rows

    ext_rows = []
    for ext, count in summary["extensions"].most_common():
        size = summary["extension_sizes"][ext]
        ext_rows.append({"extension": ext, "count": count, "size_bytes": size, "size": human_size(size)})
    ext_rows.sort(key=lambda row: row["size_bytes"], reverse=True)
    summary["extensions"] = ext_rows[:top_limit]
    summary["size"] = human_size(summary["size_bytes"])

    for key in ("largest_files", "recent_files", "new_files"):
        for row in summary[key]:
            row.pop("last_modified_timestamp", None)

    return summary


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def to_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# 文件夹清单：`{data['root']}`",
        "",
        f"- 生成时间：`{data['generated_at']}`",
        f"- 文件数：`{data['files']}`",
        f"- 文件夹数：`{data['directories']}`",
        f"- 总大小：`{data['size']}`",
        f"- 扫描错误：`{len(data['errors'])}`",
        "",
        "## 顶层目录",
        "",
        markdown_table(
            ["名称", "大小", "文件数", "目录数", "最近修改"],
            [
                [row["name"], row["size"], row["files"], row["directories"], row["last_modified"] or ""]
                for row in data["top_level"]
            ],
        ),
        "",
        "## 主要文件类型",
        "",
        markdown_table(
            ["扩展名", "大小", "数量"],
            [[row["extension"], row["size"], row["count"]] for row in data["extensions"]],
        ),
        "",
        "## 最大文件",
        "",
        markdown_table(
            ["大小", "最近修改", "路径"],
            [[row["size"], row["last_modified"], row["path"]] for row in data["largest_files"]],
        ),
        "",
        "## 最近文件",
        "",
        markdown_table(
            ["最近修改", "大小", "路径"],
            [[row["last_modified"], row["size"], row["path"]] for row in data["recent_files"]],
        ),
    ]

    if data["since_days"] is not None:
        lines.extend(
            [
                "",
                f"## 最近 {data['since_days']} 天新文件",
                "",
                markdown_table(
                    ["最近修改", "大小", "路径"],
                    [[row["last_modified"], row["size"], row["path"]] for row in data["new_files"]],
                ),
            ]
        )

    if data["errors"]:
        lines.extend(
            [
                "",
                "## 扫描错误",
                "",
                markdown_table(["路径", "错误"], [[row["path"], row["error"]] for row in data["errors"][:20]]),
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="生成只读目录清单。")
    parser.add_argument("path", help="要扫描的文件夹或磁盘")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="将结果写入指定文件，而不是输出到终端")
    parser.add_argument("--top-limit", type=int, default=20)
    parser.add_argument("--recent-limit", type=int, default=20)
    parser.add_argument("--new-limit", type=int, default=50)
    parser.add_argument("--since-days", type=int, help="列出最近 N 天修改的新文件，用于增量归档")
    parser.add_argument("--exclude", action="append", default=[], help="要排除的文件夹名称；可重复使用")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    data = scan(root, args.top_limit, args.recent_limit, args.new_limit, excludes, args.since_days)
    text = json.dumps(data, ensure_ascii=False, indent=2) if args.format == "json" else to_markdown(data)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

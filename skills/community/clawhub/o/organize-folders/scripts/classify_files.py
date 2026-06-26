#!/usr/bin/env python3
"""根据路径、名称、扩展名和时间生成文件归类建议。"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from orglib import classify_path, configure_stdout, load_json, markdown_table, now_iso, write_json


def collect_files(root: Path, since_days: int | None, limit: int | None) -> list[Path]:
    since_timestamp = None
    if since_days is not None:
        since_timestamp = time.time() - since_days * 24 * 60 * 60

    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        if since_timestamp is not None and stat.st_mtime < since_timestamp:
            continue
        files.append(path)
        if limit and len(files) >= limit:
            break
    return files


def classify_from_scan(scan: dict) -> list[dict]:
    paths = []
    for key in ("new_files", "recent_files", "largest_files"):
        for item in scan.get(key, []):
            value = item.get("path")
            if value and value not in paths:
                paths.append(value)
    return [classify_path(Path(path)) for path in paths]


def to_markdown(data: dict) -> str:
    rows = [
        [
            item["path"],
            item["type"],
            item["irk"],
            item["para"],
            item["suggested_dir"],
            item["confidence"],
            item["risk"],
            "是" if item["requires_confirmation"] else "否",
        ]
        for item in data["items"]
    ]
    return "\n".join(
        [
            "# 文件归类建议",
            "",
            f"- 生成时间：`{data['generated_at']}`",
            f"- 条目数：`{len(data['items'])}`",
            "",
            markdown_table(["路径", "类型", "IRK", "PARA", "建议目录", "置信度", "风险", "需确认"], rows),
            "",
        ]
    )


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="生成文件归类建议。")
    parser.add_argument("path", nargs="?", help="要归类的文件夹")
    parser.add_argument("--scan-json", help="从 scan_folder.py 的 JSON 输出中读取候选文件")
    parser.add_argument("--since-days", type=int, help="只归类最近 N 天修改的文件")
    parser.add_argument("--limit", type=int, help="最多归类多少个文件")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    if args.scan_json:
        scan = load_json(args.scan_json)
        items = classify_from_scan(scan)
        root = scan.get("root", "")
    else:
        if not args.path:
            raise SystemExit("需要提供 path 或 --scan-json")
        root_path = Path(args.path).expanduser().resolve()
        items = [classify_path(path) for path in collect_files(root_path, args.since_days, args.limit)]
        root = str(root_path)

    data = {"version": 1, "generated_at": now_iso(), "root": root, "items": items}
    text = to_markdown(data) if args.format == "markdown" else __import__("json").dumps(data, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    if args.output and args.format == "json":
        write_json(args.output, data)


if __name__ == "__main__":
    main()

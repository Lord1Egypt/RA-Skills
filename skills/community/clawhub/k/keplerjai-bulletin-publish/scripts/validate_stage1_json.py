#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate stage1 output JSON for structure completeness before stage2.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REQUIRED_FIELDS = [
    "rank",
    "english_title",
    "chinese_title",
    "source_site",
    "source_url",
    "publish_date",
    "english_body_raw",
    "image_url",
    "image_status",
    "image_note",
    "summary_cn",
]


def fail(message: str, exit_code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def extract_fenced_json(raw: str) -> str | None:
    match = re.search(r"```(?:json)?\s*(.*?)```", raw, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_first_json_object(raw: str) -> str | None:
    start = raw.find("{")
    if start < 0:
        return None

    depth = 0
    in_string = False
    escape = False

    for idx in range(start, len(raw)):
        ch = raw[idx]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return raw[start : idx + 1]

    return None


def load_json(path: Path) -> dict:
    raw = read_text(path)

    candidates = [raw]
    fenced = extract_fenced_json(raw)
    if fenced:
        candidates.append(fenced)
    extracted = extract_first_json_object(raw)
    if extracted:
        candidates.append(extracted)

    last_error: json.JSONDecodeError | None = None
    data = None
    for candidate in candidates:
        try:
            data = json.loads(candidate)
            break
        except json.JSONDecodeError as exc:
            last_error = exc

    if data is None:
        if last_error is not None:
            fail(f"JSON 非法: 行 {last_error.lineno} 列 {last_error.colno}: {last_error.msg}")
        fail("未找到可解析的 JSON 对象。")

    if not isinstance(data, dict):
        fail("顶层必须是 JSON 对象。")
    return data


def validate_payload(data: dict) -> None:
    item_count = data.get("item_count")
    items = data.get("items")

    if item_count != 7:
        fail(f"item_count 必须等于 7，当前为 {item_count!r}")
    if not isinstance(items, list):
        fail("items 必须是数组。")
    if len(items) != 7:
        fail(f"items 必须正好 7 条，当前为 {len(items)}")

    expected_rank = 1
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            fail(f"第 {idx} 条不是对象。")
        missing = [field for field in REQUIRED_FIELDS if field not in item]
        if missing:
            fail(f"第 {idx} 条缺少字段: {', '.join(missing)}")

        rank = item["rank"]
        if rank != expected_rank:
            fail(f"第 {idx} 条 rank 应为 {expected_rank}，实际为 {rank!r}")
        expected_rank += 1

        if not str(item["english_title"]).strip():
            fail(f"第 {idx} 条 english_title 为空。")
        if not str(item["chinese_title"]).strip():
            fail(f"第 {idx} 条 chinese_title 为空。")
        if not str(item["source_site"]).strip():
            fail(f"第 {idx} 条 source_site 为空。")
        if not str(item["source_url"]).strip():
            fail(f"第 {idx} 条 source_url 为空。")
        if not str(item["english_body_raw"]).strip():
            fail(f"第 {idx} 条 english_body_raw 为空。")
        if not str(item["summary_cn"]).strip():
            fail(f"第 {idx} 条 summary_cn 为空。")

        image_status = str(item["image_status"]).strip()
        if image_status not in {"usable", "skip"}:
            fail(f"第 {idx} 条 image_status 必须是 usable 或 skip，实际为 {image_status!r}")
        if image_status == "skip" and str(item["image_url"]).strip():
            fail(f"第 {idx} 条 image_status=skip 时 image_url 必须为空。")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 stage1 输出 JSON。")
    parser.add_argument("input", help="stage1 JSON 文件路径")
    parser.add_argument(
        "-o",
        "--output",
        help="可选：把归一化后的合法 JSON 写入指定文件",
    )
    args = parser.parse_args()

    path = Path(args.input).expanduser().resolve()
    if not path.exists():
        fail(f"文件不存在: {path}")

    data = load_json(path)
    validate_payload(data)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(output_path, data)
        print(f"已写入归一化 JSON: {output_path}")

    print("OK: stage1 JSON 结构合法，可进入下一步。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

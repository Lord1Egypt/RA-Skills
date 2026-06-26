#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format published bulletin records into the final three-line message block.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime
    yaml = None

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


DEFAULT_FRONTEND_URL = "https://www.keplerjai.com/bulletin?id={bulletin_id}"
DEFAULT_FOOTER = "联盟小秘书 lmxms2020"


def fail(message: str, exit_code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def parse_json_or_yaml(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    if yaml is not None:
        try:
            return yaml.safe_load(raw)
        except Exception:
            pass

    return None


def load_payload(path: Path) -> dict[str, Any]:
    raw = None
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            raw = path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    if raw is None:
        raw = path.read_text(encoding="utf-8", errors="replace")

    parsed = parse_json_or_yaml(raw)
    if isinstance(parsed, dict):
        return parsed

    match = re.search(r"```(?:yaml|yml|json)?\s*(.*?)```", raw, re.DOTALL | re.IGNORECASE)
    if match:
        parsed = parse_json_or_yaml(match.group(1))
        if isinstance(parsed, dict):
            return parsed

    fail("无法解析发布结果文件。")


def normalize_items(payload: dict[str, Any], frontend_template: str) -> list[dict[str, Any]]:
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        fail("发布结果里没有 items。")

    normalized: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        bulletin_id = item.get("bulletin_id")
        if isinstance(bulletin_id, str) and bulletin_id.isdigit():
            bulletin_id = int(bulletin_id)

        frontend_url = str(item.get("frontend_url", "")).strip()
        if not frontend_url and isinstance(bulletin_id, int):
            frontend_url = frontend_template.format(bulletin_id=bulletin_id)

        if not frontend_url:
            continue

        normalized.append(
            {
                "rank": item.get("rank", 0),
                "english_title": str(item.get("english_title", "")).strip(),
                "chinese_title": str(item.get("chinese_title", "")).strip(),
                "frontend_url": frontend_url,
            }
        )

    normalized.sort(key=lambda item: int(item.get("rank", 0) or 0))
    return normalized


def build_message(items: list[dict[str, Any]], footer: str) -> str:
    if len(items) != 7:
        fail(f"已发布条目数量不是 7 条，当前为 {len(items)} 条。")

    blocks = []
    for item in items:
        english_title = item["english_title"]
        chinese_title = item["chinese_title"]
        frontend_url = item["frontend_url"]

        if not english_title or not chinese_title or not frontend_url:
            fail("存在缺少标题或链接的已发布条目。")

        blocks.append("\n".join([english_title, chinese_title, frontend_url]))

    return "\n\n".join(blocks) + "\n\n\n" + footer + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="格式化 KeplerJAI 已发布 bulletin。")
    parser.add_argument("input", help="publish-result.json 或等价结构化结果文件")
    parser.add_argument(
        "-o",
        "--output",
        help="输出文案文件路径，默认写到输入文件同目录 final-message.txt",
    )
    parser.add_argument(
        "--frontend-url",
        default=DEFAULT_FRONTEND_URL,
        help="前台链接模板，默认 https://www.keplerjai.com/bulletin?id={bulletin_id}",
    )
    parser.add_argument(
        "--footer",
        default=DEFAULT_FOOTER,
        help="结尾固定文案，默认 '联盟小秘书 lmxms2020'",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        fail(f"输入文件不存在: {input_path}")

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else input_path.with_name("final-message.txt")
    )

    payload = load_payload(input_path)
    items = normalize_items(payload, args.frontend_url)
    message = build_message(items, args.footer)
    output_path.write_text(message, encoding="utf-8")

    print(f"结果已写入: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

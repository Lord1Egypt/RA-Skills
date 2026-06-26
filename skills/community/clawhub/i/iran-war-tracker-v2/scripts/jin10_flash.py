#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金十数据快讯抓取模块（替代 telegraph.py）

通过金十 MCP 协议获取实时快讯（Flash），支持关键词搜索和时间过滤。
替代原有的财联社+金十数据混合抓取方案，数据源更稳定、更标准化。

使用方式：
    python scripts/jin10_flash.py --keyword 伊朗 [--hours 18] [--limit 50] [--output output.json]
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 复用同目录下的金十 MCP 客户端
from jin10_mcp import Jin10McpClient, Jin10McpError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Jin10 flash news via MCP protocol."
    )
    parser.add_argument(
        "--keyword",
        default="伊朗",
        help="Search keyword for flash news. Default: 伊朗",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=datetime.now().hour,
        help="Filter records from the last N hours. Default: current hour of day (e.g., 9 at 9am). 0 means no limit.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of records to return. Default: no limit.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write JSON output. If omitted, print to stdout.",
    )
    parser.add_argument(
        "--format",
        choices=["raw", "normalized", "markdown"],
        default="normalized",
        help="Output format. Default: normalized.",
    )
    return parser.parse_args()


def parse_jin10_time(time_str: str) -> datetime | None:
    """解析金十时间字符串为 datetime 对象。"""
    if not time_str:
        return None
    # 尝试常见格式
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%H:%M",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            # 对只有时分的时间，假设为今天
            if fmt == "%H:%M":
                now = datetime.now()
                dt = dt.replace(year=now.year, month=now.month, day=now.day)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def fetch_flash_raw(keyword: str) -> list[dict[str, Any]]:
    """通过 MCP 获取原始快讯数据。"""
    client = Jin10McpClient()
    try:
        payload = client.search_flash(keyword)
        items = payload.get("data", {}).get("items", [])
        if not items:
            # 回退到 list_flash 获取最新快讯
            list_payload = client.list_flash()
            items = list_payload.get("data", {}).get("items", [])
        return items
    finally:
        client.close()


def normalize_flash_items(
    items: list[dict[str, Any]],
    hours: int = 0,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """
    将原始快讯标准化，支持时间过滤和条数限制。
    """
    normalized: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)

    for row in items:
        if not isinstance(row, dict):
            continue

        title = str(row.get("title") or row.get("content") or "").strip()
        content = str(row.get("content") or row.get("title") or "").strip()
        time_str = str(row.get("time") or row.get("created_at") or "").strip()

        # 时间过滤
        if hours > 0 and time_str:
            dt = parse_jin10_time(time_str)
            if dt:
                age_hours = (now - dt).total_seconds() / 3600
                if age_hours > hours:
                    continue

        normalized.append({
            "id": row.get("id"),
            "title": title,
            "content": content,
            "time": time_str,
            "url": row.get("url") or "",
            "important": row.get("important"),
            "channel": row.get("channel", []),
            "tags": row.get("tags", []),
            "source": "jin10_flash",
            "keyword_matched": True,
        })

    # 按时间倒序
    normalized.sort(key=lambda x: x["time"] or "", reverse=True)

    if limit:
        normalized = normalized[:limit]

    return normalized


def format_as_markdown(items: list[dict[str, Any]]) -> str:
    """将快讯格式化为 Markdown 时间线。"""
    lines: list[str] = []
    lines.append(f"## 金十快讯 ({len(items)} 条)\n")
    for item in items:
        time_label = item.get("time") or "未知时间"
        title = item.get("title") or item.get("content") or ""
        lines.append(f"- **{time_label}** {title}")
    return "\n".join(lines)


def build_payload(
    keyword: str,
    hours: int,
    limit: int | None,
    output_format: str,
) -> dict[str, Any]:
    """构建输出载荷。"""
    raw_items = fetch_flash_raw(keyword)
    normalized_items = normalize_flash_items(raw_items, hours=hours, limit=limit)

    payload: dict[str, Any] = {
        "meta": {
            "keyword": keyword,
            "hours_filter": hours,
            "limit": limit,
            "total_raw": len(raw_items),
            "returned": len(normalized_items),
            "fetched_at": datetime.now().isoformat(),
        },
    }

    if output_format == "raw":
        payload["items"] = raw_items
    elif output_format == "markdown":
        payload["markdown"] = format_as_markdown(normalized_items)
    else:
        payload["items"] = normalized_items

    return payload


def emit_output(payload: dict[str, Any], output: str | None) -> None:
    content = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Output written to: {output_path}")
    else:
        print(content)


def main() -> int:
    args = parse_args()
    payload = build_payload(
        keyword=args.keyword,
        hours=args.hours,
        limit=args.limit,
        output_format=args.format,
    )
    emit_output(payload, args.output)
    return 0


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    raise SystemExit(main())

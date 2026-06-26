"""Utility helper functions."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Any


def extract_article_id(url: str) -> str | None:
    """Extract article ID from a Juejin post URL.

    Supported formats:
        - https://juejin.cn/post/7300000000000000000
        - https://juejin.cn/post/7300000000000000000/
        - 7300000000000000000 (raw ID)
    """
    if url.isdigit():
        return url
    match = re.search(r"juejin\.cn/post/(\d+)", url)
    return match.group(1) if match else None


def extract_user_id(url: str) -> str | None:
    """Extract user ID from a Juejin user profile URL.

    Supported formats:
        - https://juejin.cn/user/123456
        - 123456 (raw ID)
    """
    if url.isdigit():
        return url
    match = re.search(r"juejin\.cn/user/(\d+)", url)
    return match.group(1) if match else None


def timestamp_to_str(ts: str | int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Convert a Unix timestamp (seconds or milliseconds) to a readable string (UTC+8)."""
    ts_int = int(ts)
    if ts_int > 1e12:
        ts_int = ts_int // 1000
    tz = timezone(timedelta(hours=8))
    dt = datetime.fromtimestamp(ts_int, tz=tz)
    return dt.strftime(fmt)


def sanitize_filename(name: str, max_len: int = 200) -> str:
    """Remove or replace characters that are unsafe for filenames."""
    name = re.sub(r'[\\/*?:"<>|\n\r\t]', "_", name)
    name = name.strip(". ")
    return name[:max_len] if len(name) > max_len else name


def load_json_file(path: str) -> Any:
    """Load JSON from a file, return None on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json_file(path: str, data: Any) -> None:
    """Save data as JSON to a file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_dir(path: str) -> str:
    """Ensure a directory exists and return its path."""
    os.makedirs(path, exist_ok=True)
    return path


def truncate_text(text: str, max_len: int = 100) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def format_number(num: int | float) -> str:
    """Format a number with K/W suffixes for readability."""
    if num >= 10000:
        return f"{num / 10000:.1f}W"
    if num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(int(num))

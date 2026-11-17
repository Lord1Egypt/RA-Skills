#!/usr/bin/env python3
"""Query and display today's hot topics from public, keyless hot-list APIs.

The skill executes once and prints a ranked "today's hot topics" list
(rank / title / hot value / source). It calls only public, authentication-free
hot-list REST endpoints over HTTPS (read-only), normalises the responses into a
single shape, and degrades across providers down to a bundled sample dataset
when the network or every provider is unavailable.

This module is pure Python 3 standard library. It never touches Huawei Cloud
resources, requires no AK/SK credentials and writes only to standard output or
a user-chosen ``--output`` file.

Public API:
    resolve_chain(source) -> list[str]
    fetch_source(name, timeout=..., retries=...) -> list[dict]
    fetch(source=None, timeout=..., retries=..., chain=None) -> dict
    load_sample() -> dict
    render_markdown(result) -> str
    render_text(result) -> str
    render_json(result) -> str
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Dict, List, Optional, Sequence

DEFAULT_SOURCE_CHAIN: Sequence[str] = ("weibo", "zhihu", "douyin")
DEFAULT_TOP = 10
DEFAULT_TIMEOUT = 20
DEFAULT_RETRIES = 2
USER_AGENT = "huawei-cloud-daily-hot-topics/1.0 (python-stdlib)"

# Provider registry: name -> label + endpoint. Every endpoint is public and
# authentication-free (no key/token required).
PROVIDERS: Dict[str, Dict[str, str]] = {
    "weibo": {"label": "微博热搜", "url": "https://60s.viki.moe/v2/weibo"},
    "zhihu": {"label": "知乎热榜", "url": "https://60s.viki.moe/v2/zhihu"},
    "douyin": {"label": "抖音热点", "url": "https://60s.viki.moe/v2/douyin"},
    "vvhan": {"label": "综合热榜", "url": "https://api.vvhan.com/api/hotlist/all"},
}

# Candidate keys used when normalising heterogeneous provider payloads.
_TITLE_KEYS = ("title", "name", "word", "hot_word", "hotword", "query", "keyword")
_HOT_KEYS = ("hot_value", "hot", "hotValue", "hot_num", "heat", "index", "value", "score")
_URL_KEYS = ("link", "url", "href", "mobileUrl", "mobile_url", "source_url")


def _default_sample_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data.json")


def _http_get(url: str, timeout: int) -> str:
    """Perform a single read-only HTTPS GET and return the decoded body.

    Kept as a module-level indirection so unit tests can mock the network
    without patching ``urllib.request`` globally.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 (public endpoints, https)
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _pick(mapping: Dict[str, object], keys: Sequence[str]):
    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", []):
            return value
    return None


def _coerce_hot(value) -> object:
    """Return an int when the hot value is numeric, otherwise a trimmed string."""
    if value is None:
        return None
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    digits = text.replace(",", "")
    if digits.isdigit():
        return int(digits)
    return text


def _extract_records(payload) -> List[Dict[str, object]]:
    """Pull a list of raw record dictionaries out of a provider payload."""
    data = payload
    if isinstance(data, dict):
        # Common envelopes: {"data": [...]} / {"result": [...]} / {"items": [...]}
        for key in ("data", "result", "list", "items", "hotList", "hot_list"):
            if key in data:
                data = data[key]
                break
    if isinstance(data, dict):
        # Some providers key the list by a date string (e.g. {"2026-10-26": [...]}).
        for value in data.values():
            if isinstance(value, list):
                data = value
                break
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def normalize(records: Sequence[Dict[str, object]], source_label: str) -> List[Dict[str, object]]:
    """Normalise raw provider records into ``{rank, title, hot, source, url}``."""
    items: List[Dict[str, object]] = []
    for record in records:
        title = _pick(record, _TITLE_KEYS)
        if title is None:
            continue
        title = str(title).strip()
        if not title:
            continue
        url = _pick(record, _URL_KEYS)
        items.append(
            {
                "rank": len(items) + 1,
                "title": title,
                "hot": _coerce_hot(_pick(record, _HOT_KEYS)),
                "source": source_label,
                "url": str(url).strip() if url else "",
            }
        )
    return items


def fetch_source(name: str, timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> List[Dict[str, object]]:
    """Fetch and normalise a single provider. Raises on any failure."""
    provider = PROVIDERS.get(name)
    if provider is None:
        raise ValueError("unknown source: %s" % name)
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            body = _http_get(provider["url"], timeout)
            payload = json.loads(body)
            if isinstance(payload, dict) and payload.get("code") not in (None, 200, "200", 0, "0"):
                raise ValueError("provider returned code=%s" % payload.get("code"))
            records = _extract_records(payload)
            if not records:
                raise ValueError("provider returned no records")
            items = normalize(records, provider["label"])
            if not items:
                raise ValueError("provider records carried no usable title")
            return items
        except (urllib.error.URLError, ValueError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last_error = exc
    raise RuntimeError("source %s failed: %s" % (name, last_error))


def load_sample(path: Optional[str] = None) -> Dict[str, object]:
    """Load the bundled sample dataset used as the final offline fallback."""
    path = path or _default_sample_path()
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    records = data.get("items", data) if isinstance(data, dict) else None
    if not isinstance(records, list) or not records:
        raise ValueError("sample dataset contains no usable items")
    label = str(data.get("source_label", "示例数据")) if isinstance(data, dict) else "示例数据"
    items = normalize(records, label)
    if not items:
        raise ValueError("sample dataset contains no usable items")
    return {
        "source": "sample",
        "source_label": label,
        "is_sample": True,
        "note": str(data.get("note", "")) if isinstance(data, dict) else "",
        "items": items,
    }


def resolve_chain(source: Optional[str]) -> List[str]:
    """Return the ordered provider chain for ``source`` (default chain when auto)."""
    base = list(DEFAULT_SOURCE_CHAIN)
    if not source or source in ("auto", "all"):
        return base
    if source not in PROVIDERS:
        raise ValueError("unknown source: %s" % source)
    return [source] + [name for name in base if name != source]


def fetch(
    source: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    chain: Optional[Sequence[str]] = None,
    offline: bool = False,
) -> Dict[str, object]:
    """Fetch today's hot list, degrading across providers and finally to sample data."""
    warnings: List[str] = []
    resolved = list(chain) if chain is not None else resolve_chain(source)
    if not offline:
        for name in resolved:
            try:
                items = fetch_source(name, timeout=timeout, retries=retries)
                return {
                    "source": name,
                    "source_label": PROVIDERS[name]["label"],
                    "is_sample": False,
                    "note": "",
                    "items": items,
                    "warnings": warnings,
                }
            except Exception as exc:  # noqa: BLE001 (degradation is the contract)
                warnings.append("%s(%s) 不可用：%s" % (PROVIDERS[name]["label"], name, exc))
    sample = load_sample()
    sample["warnings"] = warnings + ["已回退到内置示例数据（非实时榜单）"]
    return sample


def _format_hot(hot) -> str:
    if isinstance(hot, int):
        return format(hot, ",")
    if hot in (None, ""):
        return "-"
    return str(hot)


def render_markdown(result: Dict[str, object], top: int = DEFAULT_TOP) -> str:
    """Render the result as a readable Markdown table."""
    items = list(result.get("items", []))[:top]
    lines: List[str] = ["# 今日热点榜单", ""]
    lines.append("- 日期：%s" % result.get("date", _dt.date.today().isoformat()))
    lines.append("- 来源：%s" % result.get("source_label", result.get("source", "unknown")))
    lines.append("- 条数：%d" % len(items))
    if result.get("is_sample"):
        lines.append("- ⚠️ 数据源不可用，当前展示的是**示例数据**（非实时榜单）。")
    if result.get("note"):
        lines.append("- 说明：%s" % result["note"])
    lines.append("")
    lines.append("| 排名 | 标题 | 热度 | 来源 |")
    lines.append("| --- | --- | --- | --- |")
    for item in items:
        title = str(item.get("title", "")).replace("|", "\\|")
        link = item.get("url") or ""
        cell = "[%s](%s)" % (title, link) if link else title
        lines.append("| %s | %s | %s | %s |" % (item.get("rank", ""), cell, _format_hot(item.get("hot")), item.get("source", "")))
    if result.get("warnings"):
        lines.append("")
        lines.append("> 降级提示：%s" % "；".join(result["warnings"]))
    return "\n".join(lines).rstrip() + "\n"


def render_text(result: Dict[str, object], top: int = DEFAULT_TOP) -> str:
    """Render the result as aligned plain text."""
    items = list(result.get("items", []))[:top]
    lines: List[str] = ["今日热点榜单", "=" * 12]
    lines.append("日期：%s | 来源：%s | 条数：%d" % (
        result.get("date", _dt.date.today().isoformat()),
        result.get("source_label", result.get("source", "unknown")),
        len(items),
    ))
    if result.get("is_sample"):
        lines.append("⚠️ 数据源不可用，当前展示的是示例数据（非实时榜单）")
    lines.append("")
    for item in items:
        lines.append("%2s. %s  [热度 %s] (%s)" % (
            item.get("rank", ""),
            item.get("title", ""),
            _format_hot(item.get("hot")),
            item.get("source", ""),
        ))
        if item.get("url"):
            lines.append("     %s" % item["url"])
    if result.get("warnings"):
        lines.append("")
        lines.append("降级提示：%s" % "；".join(result["warnings"]))
    return "\n".join(lines).rstrip() + "\n"


def render_json(result: Dict[str, object], top: int = DEFAULT_TOP) -> str:
    """Render the result as a parseable JSON object."""
    payload = dict(result)
    payload["items"] = list(result.get("items", []))[:top]
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render(result: Dict[str, object], fmt: str = "markdown", top: int = DEFAULT_TOP) -> str:
    if fmt == "text":
        return render_text(result, top)
    if fmt == "json":
        return render_json(result, top)
    return render_markdown(result, top)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="查询并输出今日热点榜单（免鉴权公开热榜 API，只读）。",
    )
    parser.add_argument("--top", type=int, default=DEFAULT_TOP, help="展示的条数（默认：%(default)s）")
    parser.add_argument(
        "--source",
        default="auto",
        help="榜单来源：auto（默认，按序降级）| %s" % " | ".join(PROVIDERS),
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "text", "json"),
        default="markdown",
        help="输出格式（默认：markdown）",
    )
    parser.add_argument("--output", default=None, help="写入文件，缺省输出到标准输出")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="单次请求超时秒数（默认：%(default)s）")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help="单源重试次数（默认：%(default)s）")
    parser.add_argument("--offline", action="store_true", help="跳过网络，直接使用内置示例数据")
    parser.add_argument("--list-sources", action="store_true", help="列出可用来源后退出")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_sources:
        for name, provider in PROVIDERS.items():
            print("%-8s %s" % (name, provider["label"]))
        return 0
    if args.top < 1:
        print("error: --top 必须 >= 1", file=sys.stderr)
        return 2
    if args.timeout < 1:
        print("error: --timeout 必须 >= 1", file=sys.stderr)
        return 2
    try:
        chain = resolve_chain(args.source)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    try:
        result = fetch(source=args.source, timeout=args.timeout, retries=args.retries,
                       chain=chain, offline=args.offline)
    except Exception as exc:  # noqa: BLE001 (final safety net: sample data is bundled)
        print("error: 无法获取热点数据且内置示例数据不可用：%s" % exc, file=sys.stderr)
        return 1

    result["date"] = _dt.date.today().isoformat()
    result["top"] = args.top
    body = render(result, args.format, args.top)
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(body)
        except OSError as exc:
            print("error: 无法写入 %s：%s" % (args.output, exc), file=sys.stderr)
            return 2
        if args.format != "json":
            print("来源：%s | 条数：%d" % (result.get("source_label"), min(args.top, len(result.get("items", [])))))
            print("已写入 %s" % args.output)
    else:
        sys.stdout.write(body)
        if not body.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
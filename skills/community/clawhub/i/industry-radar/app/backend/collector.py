"""
M2 多源采集器：从 RSS / Atom 源拉取条目。

设计要点
--------
* 使用 requests 抓取原始字节（可自定义 UA / 超时 / 代理），再交给 feedparser 解析，
  避免 feedparser 直接联网时无法控制超时。
* 单源异常隔离：任一源失败只记录日志，不影响其它源（多源冗余原则）。
* 支持 HTTP 与 HTTPS；自动纠正源 URL。
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import feedparser
import requests

import net_guard
from config import (
    MAX_ARTICLES_PER_SOURCE, MAX_FETCH_BYTES, REQUEST_TIMEOUT, USER_AGENT,
)

log = logging.getLogger("industryradar.collector")

_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
}

# 自定义源只接受这几类 Content-Type（为空时放行，交由 feedparser 判定）
_XML_TYPES = ("xml", "rss", "atom")


def _entry_time(entry) -> str:
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            try:
                dt = datetime(*t[:6], tzinfo=timezone.utc)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:  # noqa: BLE001
                pass
    return ""


def _entry_content(entry) -> str:
    """提取条目内嵌正文（若源提供）。"""
    if entry.get("content"):
        try:
            return entry["content"][0].get("value", "") or ""
        except Exception:  # noqa: BLE001
            pass
    return entry.get("summary", "") or entry.get("description", "") or ""


def fetch_source_checked(source: Dict[str, Any], timeout: Optional[int] = None) -> tuple:
    """抓取单个源，返回 `(条目列表, 失败原因)`；成功时原因为空串。

    自定义源额外要求响应确实是 RSS/Atom（`_strict_xml=True`）：
    否则使用者可以把任意网页甚至纯文本接口挂进来，变成通用抓取代理。
    """
    url = source.get("url", "")
    if not url:
        return [], "缺少源地址"
    # 源地址哪怕来自内置配置，也统一走出站校验，避免配置被改写后横向访问内网
    if not net_guard.is_fetchable(url):
        return [], "地址未通过出站安全校验"
    try:
        resp = net_guard.safe_get(
            url, headers=_HEADERS, timeout=timeout or REQUEST_TIMEOUT,
            max_bytes=MAX_FETCH_BYTES,
        )
        resp.raise_for_status()
        raw = resp.content
    except Exception as exc:  # noqa: BLE001
        log.warning("source fetch failed: %s (%s)", source.get("name", url), exc)
        return [], str(exc)

    if source.get("_strict_xml"):
        ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype and not any(k in ctype for k in _XML_TYPES):
            return [], f"不是 RSS/Atom（Content-Type: {ctype}）"

    try:
        parsed = feedparser.parse(raw)
    except Exception as exc:  # noqa: BLE001
        log.warning("feed parse failed: %s (%s)", source.get("name", url), exc)
        return [], f"解析失败：{exc}"

    items: List[Dict[str, Any]] = []
    for e in parsed.entries[:MAX_ARTICLES_PER_SOURCE]:
        link = e.get("link", "") or ""
        title = (e.get("title", "") or "").strip()
        if not title or not link:
            continue
        items.append({
            "title": title,
            "url": link,
            "source_name": source.get("name", ""),
            "source_category": source.get("category", ""),
            "published_at": _entry_time(e),
            "raw_content": _entry_content(e),
        })
    if not items:
        return [], "未解析到条目（可能不是有效订阅源）"
    log.info("source %s -> %d items", source.get("name", url), len(items))
    return items, ""


def fetch_source(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """抓取单个源，返回标准化条目列表。失败返回空列表。"""
    return fetch_source_checked(source)[0]


def collect(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """并发采集多个源（线程池，免费源通常 <10 个，开销可控）。

    自定义源带 `_custom_id`，抓取结果会回写 `custom_source` 表，
    连续失败达到阈值后由 store 侧自动禁用。
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    import store

    enabled = [s for s in sources if s.get("enabled", True)]
    out: List[Dict[str, Any]] = []
    if not enabled:
        return out

    with ThreadPoolExecutor(max_workers=min(8, len(enabled))) as pool:
        futures = {pool.submit(fetch_source_checked, s): s for s in enabled}
        for fut in as_completed(futures):
            src = futures[fut]
            try:
                items, err = fut.result()
            except Exception as exc:  # noqa: BLE001
                log.warning("collector task error: %s", exc)
                items, err = [], str(exc)
            out.extend(items)
            cs_id = src.get("_custom_id")
            if cs_id:
                try:
                    store.record_custom_source_result(int(cs_id), not err, err)
                except Exception as exc:  # noqa: BLE001
                    log.warning("record custom source result failed: %s", exc)
    return out
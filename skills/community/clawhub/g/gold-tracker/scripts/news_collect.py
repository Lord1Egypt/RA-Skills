#!/usr/bin/env python3
"""新闻采集器：从配置的可信新闻源（RSS）自动抓取标题 + 摘要 + 链接。

把「搜索 → 抓取 → 记录来源」从 LLM 下沉到脚本（降低 LLM 负担），且来源是脚本
真实抓取的，反幻觉约束更强。来源列表在 config.yaml 的 news_sources，配置多个
独立域名以保证多样性（可信 + 多样）。

用法:
    python3 scripts/news_collect.py
"""

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from common import paths, config, atomic, heartbeat, timeutil
import log_fetch


def fetch_url(url, timeout):
    # 用浏览器 UA：部分免费源（如 mining.com）会拒绝默认 UA（HTTP 403）
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0 Safari/537.36"),
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _local(tag):
    return tag.split("}")[-1].lower()


def parse_rss(text):
    items = []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return items
    for elem in root.iter():
        if _local(elem.tag) != "item":
            continue
        item = {}
        for child in elem:
            t = _local(child.tag)
            if t in ("title", "link", "description", "pubdate"):
                item[t] = (child.text or "").strip()
        if item.get("title") and item.get("link"):
            items.append(item)
    return items


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def collect():
    cfg = config.load()
    items = []
    errors = []
    for src in (cfg.get("news_sources") or []):
        if not isinstance(src, dict) or not src.get("enabled", True):
            continue
        url = src.get("url", "")
        if not url:
            continue
        name = src.get("name", url)
        try:
            text = fetch_url(url, int(src.get("timeout", 15)))
            parsed = parse_rss(text) if src.get("type", "rss") == "rss" else []
            for it in parsed[:int(src.get("max_items", 10))]:
                it["source"] = name
                items.append(it)
        except Exception as e:  # noqa: BLE001
            errors.append("[{}] {}: {}".format(name, url, e))
    return items, errors


def record(items):
    entries = log_fetch.load_log()
    existing = {e.get("url") for e in entries}
    ts = timeutil.now_iso()
    snippets = []
    added = 0
    for it in items:
        url = it.get("link", "")
        if not url or url in existing:
            continue
        entries.append({
            "url": url,
            "domain": urlparse(url).netloc,
            "title": it.get("title", ""),
            "fetched_at": ts,
            "last_fetch_at": ts,
            "source_type": "rss",
            "source": it.get("source", ""),
        })
        existing.add(url)
        added += 1
        snippets.append({
            "source": it.get("source", ""),
            "title": it.get("title", ""),
            "link": url,
            "summary": _strip_tags(it.get("description", ""))[:300],
            "date": it.get("pubdate", ""),
        })
    log_fetch.save_log(entries)
    atomic.atomic_write_json(paths.resolve("cache") / "news_snippets.json",
                             {"collected_at": ts, "items": snippets})
    return added, snippets


def main():
    paths.ensure_env()
    items, errors = collect()
    added, snippets = record(items)
    domains = {urlparse(s["link"]).netloc for s in snippets}
    print("[信息] 采集 {} 条，新增 {} 条，覆盖 {} 个域名".format(len(items), added, len(domains)))
    for e in errors:
        print("[警告] {}".format(e), file=sys.stderr)
    for s in snippets:
        print("- [{}] {} ({})".format(s["source"], s["title"], s["link"]))
    heartbeat.record("news_collect")
    if not snippets:
        print("[信息] 无新增条目（已全部采集）")
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Ingest candidates from YouTube RSS and optional X/web JSON feeds.

This script normalizes candidate resources for discover_content.py.
"""

from __future__ import annotations
import argparse
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "learning-coach/0.3"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def youtube_feed_url(channel: str) -> str:
    c = channel.strip()
    if c.startswith("http"):
        return c
    # Accept channel id or @handle; caller can pass full URL for custom resolution.
    if c.startswith("UC"):
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={c}"
    return f"https://www.youtube.com/feeds/videos.xml?user={c}"


def parse_youtube_rss(xml_text: str, limit: int) -> list[dict]:
    ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("atom:entry", ns)[:limit]:
        title = (e.findtext("atom:title", default="", namespaces=ns) or "").strip()
        vid = (e.findtext("yt:videoId", default="", namespaces=ns) or "").strip()
        link = f"https://www.youtube.com/watch?v={vid}" if vid else ""
        out.append({
            "title": title,
            "url": link,
            "snippet": "YouTube channel feed item",
            "source": "youtube",
            "freshness": 6,
        })
    return out


def load_optional_json(path: str, source_name: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("items", [])
    out = []
    for i in items:
        out.append({
            "title": i.get("title", ""),
            "url": i.get("url", ""),
            "snippet": i.get("snippet", ""),
            "source": source_name,
            "freshness": float(i.get("freshness", 5)),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--youtube", action="append", default=[], help="YouTube channel id/user/feed URL (repeatable)")
    ap.add_argument("--x-json", help="Optional normalized JSON list from X integration")
    ap.add_argument("--web-json", help="Optional normalized JSON list from web search ingestion")
    ap.add_argument("--limit-per-source", type=int, default=10)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    candidates = []

    for ch in args.youtube:
        try:
            url = youtube_feed_url(ch)
            xml_text = fetch_text(url)
            candidates.extend(parse_youtube_rss(xml_text, args.limit_per_source))
        except Exception as e:
            candidates.append({
                "title": f"[ingest-error] youtube:{ch}",
                "url": "",
                "snippet": str(e),
                "source": "youtube",
                "freshness": 0,
            })

    if args.x_json:
        candidates.extend(load_optional_json(args.x_json, "x"))
    if args.web_json:
        candidates.extend(load_optional_json(args.web_json, "web"))

    # basic URL sanity cleanup
    for c in candidates:
        if c.get("url") and not re.match(r"^https?://", c["url"]):
            c["url"] = ""

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

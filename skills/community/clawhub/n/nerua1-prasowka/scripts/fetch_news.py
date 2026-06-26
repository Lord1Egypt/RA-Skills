#!/usr/bin/env python3
"""
fetch_news.py - Universal news fetcher for OpenClaw prasowka skills
Supports: hackernews, github, producthunt, reddit, yandex-news, baidu-hot, weibo, v2ex, wallstreetcn, all
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
import html
import re

def fetch_hackernews(limit=10, keyword=None, deep=False):
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        with urllib.request.urlopen(url, timeout=10) as r:
            ids = json.loads(r.read())[:limit*3]
        items = []
        for id_ in ids:
            if len(items) >= limit:
                break
            try:
                with urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{id_}.json", timeout=5) as r:
                    item = json.loads(r.read())
                if not item or item.get("type") != "story":
                    continue
                title = item.get("title", "")
                if keyword:
                    kws = [k.strip().lower() for k in keyword.split(",")]
                    if not any(k in title.lower() for k in kws):
                        continue
                ts = item.get("time", 0)
                dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
                items.append({
                    "source": "HackerNews",
                    "title": title,
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={id_}"),
                    "score": item.get("score", 0),
                    "time": dt,
                    "comments": item.get("descendants", 0),
                })
            except Exception:
                continue
        return items
    except Exception as e:
        return [{"error": f"HackerNews fetch failed: {e}"}]

def fetch_github_trending(limit=10, keyword=None, deep=False):
    try:
        url = "https://api.github.com/search/repositories?q=created:>2026-01-01&sort=stars&order=desc&per_page=50"
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-NewsAggregator/1.0", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        items = []
        for repo in data.get("items", []):
            if len(items) >= limit:
                break
            name = repo.get("full_name", "")
            desc = repo.get("description", "") or ""
            if keyword:
                kws = [k.strip().lower() for k in keyword.split(",")]
                if not any(k in (name + desc).lower() for k in kws):
                    continue
            items.append({
                "source": "GitHub Trending",
                "title": name,
                "url": repo.get("html_url", ""),
                "score": repo.get("stargazers_count", 0),
                "time": repo.get("pushed_at", "")[:10],
                "description": desc,
                "language": repo.get("language", ""),
            })
        return items
    except Exception as e:
        return [{"error": f"GitHub fetch failed: {e}"}]

def fetch_reddit(subreddit="technology", limit=10, keyword=None, deep=False):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit*2}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OpenClaw NewsAggregator)"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        items = []
        for post in data.get("data", {}).get("children", []):
            if len(items) >= limit:
                break
            p = post.get("data", {})
            title = p.get("title", "")
            if keyword:
                kws = [k.strip().lower() for k in keyword.split(",")]
                if not any(k in title.lower() for k in kws):
                    continue
            ts = p.get("created_utc", 0)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            items.append({
                "source": f"Reddit r/{subreddit}",
                "title": title,
                "url": p.get("url", ""),
                "score": p.get("score", 0),
                "time": dt,
                "comments": p.get("num_comments", 0),
            })
        return items
    except Exception as e:
        return [{"error": f"Reddit r/{subreddit} fetch failed: {e}"}]

def fetch_producthunt(limit=10, keyword=None, deep=False):
    return [{"source": "ProductHunt", "note": "Use web_search: 'site:producthunt.com new products today'", "url": "https://www.producthunt.com"}]

def fetch_v2ex(limit=10, keyword=None, deep=False):
    try:
        url = "https://www.v2ex.com/api/topics/hot.json"
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-NewsAggregator/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        items = []
        for topic in data[:limit*2]:
            if len(items) >= limit:
                break
            title = topic.get("title", "")
            if keyword:
                kws = [k.strip().lower() for k in keyword.split(",")]
                if not any(k in title.lower() for k in kws):
                    continue
            items.append({
                "source": "V2EX",
                "title": title,
                "url": f"https://www.v2ex.com/t/{topic.get('id', '')}",
                "score": topic.get("replies", 0),
                "time": datetime.fromtimestamp(topic.get("last_modified", 0), tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            })
        return items
    except Exception as e:
        return [{"error": f"V2EX fetch failed: {e}"}]

def fetch_wallstreetcn(limit=10, keyword=None, deep=False):
    try:
        url = "https://api-one-wscn.awtmt.com/apiv1/content/lives?channel=news-global&limit=20"
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-NewsAggregator/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        items = []
        for item in data.get("data", {}).get("items", [])[:limit*2]:
            if len(items) >= limit:
                break
            title = item.get("content_text", "")[:100]
            if keyword:
                kws = [k.strip().lower() for k in keyword.split(",")]
                if not any(k in title.lower() for k in kws):
                    continue
            items.append({
                "source": "WallStreetCN",
                "title": title,
                "url": f"https://wallstreetcn.com/articles/{item.get('id', '')}",
                "score": item.get("like_count", 0),
                "time": datetime.fromtimestamp(item.get("display_time", 0), tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            })
        return items
    except Exception as e:
        return [{"error": f"WallStreetCN fetch failed: {e}"}]

def fetch_yandex_news(limit=10, keyword=None, deep=False):
    try:
        kw = keyword or "technology"
        query = urllib.parse.quote(kw)
        url = f"https://news.yandex.ru/export/rss.xml?rubric=technology&lang=en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode("utf-8")
        items = []
        entries = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for entry in entries[:limit*2]:
            if len(items) >= limit:
                break
            title_m = re.search(r'<title>(.*?)</title>', entry)
            link_m = re.search(r'<link>(.*?)</link>', entry)
            date_m = re.search(r'<pubDate>(.*?)</pubDate>', entry)
            if not title_m:
                continue
            title = html.unescape(title_m.group(1))
            if keyword:
                kws = [k.strip().lower() for k in keyword.split(",")]
                if not any(k in title.lower() for k in kws):
                    continue
            items.append({
                "source": "Yandex News",
                "title": title,
                "url": link_m.group(1) if link_m else "https://news.yandex.ru",
                "score": 0,
                "time": date_m.group(1) if date_m else "",
            })
        return items if items else [{"source": "Yandex News", "note": "Use web_search on yandex.ru/news", "url": "https://yandex.ru/news"}]
    except Exception as e:
        return [{"source": "Yandex News", "note": f"RSS failed ({e}), use web_search on yandex.ru/news", "url": "https://yandex.ru/news"}]

def fetch_baidu_hot(limit=10, keyword=None, deep=False):
    return [{"source": "Baidu Hot", "note": "Use web_search: 'site:baidu.com 百度热搜' or 'baidu hot search today'", "url": "https://www.baidu.com/s?rn=20&wd=热搜"}]

# ROZSZERZONY SOURCE_MAP
SOURCE_MAP = {
    "hackernews": fetch_hackernews,
    "github": fetch_github_trending,
    "producthunt": fetch_producthunt,
    "reddit-tech": lambda l, k, d: fetch_reddit("technology", l, k, d),
    "reddit-science": lambda l, k, d: fetch_reddit("science", l, k, d),
    "reddit-worldnews": lambda l, k, d: fetch_reddit("worldnews", l, k, d),
    "reddit-stocks": lambda l, k, d: fetch_reddit("stocks", l, k, d),
    "reddit-investing": lambda l, k, d: fetch_reddit("investing", l, k, d),
    "reddit-singularity": lambda l, k, d: fetch_reddit("singularity", l, k, d),
    "reddit-artificial": lambda l, k, d: fetch_reddit("artificial", l, k, d),
    "reddit-programming": lambda l, k, d: fetch_reddit("programming", l, k, d),
    "reddit-space": lambda l, k, d: fetch_reddit("space", l, k, d),
    "reddit-crypto": lambda l, k, d: fetch_reddit("CryptoCurrency", l, k, d),
    "reddit-technology": lambda l, k, d: fetch_reddit("technology", l, k, d),
    "v2ex": fetch_v2ex,
    "wallstreetcn": fetch_wallstreetcn,
    "yandex": fetch_yandex_news,
    "baidu": fetch_baidu_hot,
}

def main():
    parser = argparse.ArgumentParser(description="Fetch news from multiple sources")
    parser.add_argument("--source", default="hackernews",
                        help=f"Source: {', '.join(SOURCE_MAP.keys())}, all, ai, swiat, rynek")
    parser.add_argument("--limit", type=int, default=10, help="Max items per source")
    parser.add_argument("--keyword", type=str, default=None, help="Comma-separated keywords")
    parser.add_argument("--deep", action="store_true", help="Fetch article content")
    args = parser.parse_args()

    # Preset groups
    AI_SOURCES = ["hackernews", "github", "reddit-artificial", "reddit-singularity", "v2ex"]
    SWIAT_SOURCES = ["hackernews", "reddit-worldnews", "reddit-science", "reddit-tech", "yandex"]
    RYNEK_SOURCES = ["wallstreetcn", "reddit-stocks", "reddit-investing", "yandex"]

    if args.source == "all":
        sources = list(SOURCE_MAP.keys())
    elif args.source == "ai":
        sources = AI_SOURCES
    elif args.source == "swiat":
        sources = SWIAT_SOURCES
    elif args.source == "rynek":
        sources = RYNEK_SOURCES
    elif args.source in SOURCE_MAP:
        sources = [args.source]
    else:
        print(json.dumps([{"error": f"Unknown source: {args.source}"}]))
        sys.exit(1)

    results = []
    for src in sources:
        fn = SOURCE_MAP.get(src)
        if fn:
            items = fn(args.limit, args.keyword, args.deep)
            results.extend(items)

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

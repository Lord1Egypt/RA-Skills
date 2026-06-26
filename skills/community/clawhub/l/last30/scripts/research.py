#!/usr/bin/env python3
"""
last30 — Research any topic from the last 30 days
Simplified port for OpenClaw: Reddit, X, HN, YouTube, Web
"""

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any

# ─── Config ────────────────────────────────────────────────────────────────────

BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")
CT0 = os.environ.get("CT0", "")
SAVE_DIR = os.path.expanduser("~/Documents/Last30Days")
MODE = "balanced"  # quick, balanced, deep

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    print(f"[last30] {msg}", file=sys.stderr)


def http_get(url: str, headers: dict = None, retries: int = 2) -> dict | None:
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; last30/1.0)")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)
                continue
            log(f"HTTP GET failed for {url}: {e}")
            return None
        except Exception as e:
            log(f"HTTP GET failed for {url}: {e}")
            return None
    return None


def run_cmd(cmd: list[str], timeout: int = 30) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except Exception as e:
        return f"[ERROR: {e}]"


def save_file(topic_slug: str, content: str) -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{topic_slug}-{date_str}.md"
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'^-+|-+$', '', text)[:80]


# ─── Source Queries ────────────────────────────────────────────────────────────

def search_reddit(topic: str, mode: str) -> list[dict]:
    """Search Reddit via public JSON API."""
    limit = {"quick": 10, "balanced": 25, "deep": 40}.get(mode, 25)
    query_enc = urllib.parse.quote(topic)
    
    # Search all of Reddit
    url = (
        f"https://www.reddit.com/search.json?q={query_enc}"
        f"&sort=relevance&t=month&limit={limit}"
    )
    
    data = http_get(url)
    results = []
    if not data or "data" not in data:
        return results
    
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        results.append({
            "source": "reddit",
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "subreddit": post.get("subreddit", ""),
            "author": post.get("author", ""),
            "selftext": post.get("selftext", "")[:500],
            "created_utc": post.get("created_utc", 0),
        })
    
    return results


def search_hn(topic: str, mode: str) -> list[dict]:
    """Search Hacker News via Algolia API."""
    limit = {"quick": 10, "balanced": 25, "deep": 40}.get(mode, 25)
    query_enc = urllib.parse.quote(topic)
    url = f"https://hn.algolia.com/api/v1/search?query={query_enc}&tags=story&hitsPerPage={limit}&numericFilters=created_at_i>={int((datetime.now() - timedelta(days=30)).timestamp())}"
    
    data = http_get(url)
    results = []
    if not data or "hits" not in data:
        return results
    
    for hit in data.get("hits", []):
        obj = hit.get("objectID", "")
        results.append({
            "source": "hn",
            "title": hit.get("title", ""),
            "url": hit.get("url", "") or f"https://news.ycombinator.com/item?id={obj}",
            "score": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "author": hit.get("author", ""),
            "created_at": hit.get("created_at", ""),
        })
    
    return results


def search_x(topic: str, mode: str) -> list[dict]:
    """Search X via bird (xurl). Falls back to Brave web search if not configured."""
    limit = {"quick": 10, "balanced": 25, "deep": 40}.get(mode, 25)
    
    if not AUTH_TOKEN:
        log("X auth not configured, skipping X search (set AUTH_TOKEN + CT0 for X)")
        return []
    
    cmd = [
        "bird", "search", f"{topic}", "-n", str(limit),
        "--auth-token", AUTH_TOKEN,
        "--ct0", CT0,
        "--plain"
    ]
    
    output = run_cmd(cmd, timeout=30)
    results = []
    
    # Parse bird plain output — format:
    # @handle (Name):
    # tweet text...
    # date: Mon Mar 23 19:35:38 +0000 2026
    # url: https://x.com/.../status/...
    # ───────────────────
    current_tweet = {}
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("@") and "(" in line:
            # New tweet starts
            if current_tweet:
                results.append({**current_tweet, "source": "x"})
            handle = line.split("(")[0].strip()
            current_tweet = {"handle": handle, "text": ""}
        elif line.startswith("date:"):
            current_tweet["date"] = line[5:].strip()
        elif line.startswith("url:"):
            current_tweet["url"] = line[4:].strip()
        elif line.startswith("❤ "):
            parts = line[2:].split()
            if parts:
                try:
                    current_tweet["likes"] = int(parts[0].replace(",", ""))
                except:
                    current_tweet["likes"] = 0
        elif line.startswith("🔁 "):
            parts = line[3:].split()
            if parts:
                try:
                    current_tweet["retweets"] = int(parts[0].replace(",", ""))
                except:
                    current_tweet["retweets"] = 0
        elif line.startswith("▲ "):
            parts = line[2:].split()
            if parts:
                try:
                    current_tweet["score"] = int(parts[0].replace(",", ""))
                except:
                    current_tweet["score"] = 0
        elif line.startswith("http://") or line.startswith("https://"):
            continue  # skip URL lines that are part of text
        elif current_tweet and "text" in current_tweet:
            current_tweet["text"] += " " + line
    
    if current_tweet:
        results.append({**current_tweet, "source": "x"})
    
    return results


def search_youtube(topic: str, mode: str) -> list[dict]:
    """Search YouTube via Brave API (web search with site:youtube.com)."""
    if not BRAVE_API_KEY:
        return []
    
    limit = {"quick": 5, "balanced": 10, "deep": 20}.get(mode, 10)
    query = f"{topic} site:youtube.com"
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    req_url = f"{url}?q={urllib.parse.quote(query)}&count={limit}"
    
    req = urllib.request.Request(req_url)
    for k, v in headers.items():
        req.add_header(k, v)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        log(f"YouTube search failed: {e}")
        return []
    
    results = []
    for item in data.get("web", {}).get("results", []):
        results.append({
            "source": "youtube",
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", "")[:200],
        })
    
    return results


def search_web(topic: str, mode: str) -> list[dict]:
    """Web search via Brave API."""
    if not BRAVE_API_KEY:
        return []
    
    limit = {"quick": 10, "balanced": 25, "deep": 40}.get(mode, 25)
    query_enc = urllib.parse.quote(topic)
    url = f"https://api.search.brave.com/res/v1/web/search?q={query_enc}&count={limit}"
    
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("X-Subscription-Token", BRAVE_API_KEY)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        log(f"Web search failed: {e}")
        return []
    
    results = []
    for item in data.get("web", {}).get("results", []):
        results.append({
            "source": "web",
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", "")[:200],
        })
    
    return results


def search_polymarket(topic: str, mode: str) -> list[dict]:
    """Search Polymarket prediction markets via Gamma API (no auth required)."""
    limit = {"quick": 5, "balanced": 10, "deep": 20}.get(mode, 10)
    query_enc = urllib.parse.quote(topic)
    
    # Search active markets matching the topic
    url = f"https://gamma-api.polymarket.com/markets?limit={limit}&search={query_enc}&closed=false&active=true"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; last30/1.0)")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        log(f"Polymarket search failed: {e}")
        return []
    
    results = []
    for item in data if isinstance(data, list) else []:
        # Outcomes and outcomePrices are JSON strings, not arrays
        try:
            outcomes = json.loads(item.get("outcomes", "[]"))
        except (json.JSONDecodeError, TypeError):
            outcomes = []
        try:
            prices = json.loads(item.get("outcomePrices", "[]"))
        except (json.JSONDecodeError, TypeError):
            prices = []
        vol = float(item.get("volume", 0) or 0)
        
        # Build probability string
        prob_str = ""
        if outcomes and prices:
            prob_parts = []
            for outcome, price in zip(outcomes, prices):
                try:
                    pct = float(price) * 100
                    prob_parts.append(f"{outcome}: {pct:.1f}%")
                except (ValueError, TypeError):
                    pass
            prob_str = " | ".join(prob_parts)
        
        results.append({
            "source": "polymarket",
            "question": item.get("question", ""),
            "url": f"https://polymarket.com/event/{item.get('slug', item.get('id', ''))}",
            "volume": vol,
            "probabilities": prob_str,
            "category": item.get("category", ""),
            "end_date": item.get("endDate", ""),
        })
    
    return results


# ─── Scoring ─────────────────────────────────────────────────────────────────

def score_item(item: dict) -> float:
    """Score an item by engagement signals."""
    score = 0.0
    if item["source"] == "reddit":
        score = (item.get("score", 0) * 1.0) + (item.get("num_comments", 0) * 0.5)
    elif item["source"] == "hn":
        score = (item.get("score", 0) * 1.5) + (item.get("num_comments", 0) * 0.5)
    elif item["source"] == "x":
        score = item.get("likes", 0) * 0.3 + item.get("score", 0) * 0.7
    elif item["source"] == "web":
        score = 0.5  # No engagement signals, low weight
    elif item["source"] == "youtube":
        score = 0.5
    elif item["source"] == "polymarket":
        # Volume is the strongest signal — high volume = high conviction
        score = min(float(item.get("volume", 0) or 0) / 100000, 50)  # cap at 50
    return score


def rank_results(results: list[dict]) -> list[dict]:
    return sorted(results, key=score_item, reverse=True)


# ─── Synthesis ────────────────────────────────────────────────────────────────

def format_reddit(items: list[dict]) -> str:
    if not items:
        return "No Reddit results found."
    output = []
    for item in items[:10]:
        comments = item.get("num_comments", 0)
        score = item.get("score", 0)
        sub = item.get("subreddit", "")
        title = item.get("title", "")[:120]
        url = item.get("url", "")
        output.append(f"- [{title}]({url}) (`r/{sub}` ▲{score} 💬{comments})")
    return "\n".join(output)


def format_hn(items: list[dict]) -> str:
    if not items:
        return "No Hacker News results found."
    output = []
    for item in items[:10]:
        score = item.get("score", 0)
        comments = item.get("num_comments", 0)
        title = item.get("title", "")[:120]
        url = item.get("url", "")
        output.append(f"- [{title}]({url}) (▲{score} 💬{comments})")
    return "\n".join(output)


def format_x(items: list[dict]) -> str:
    if not items:
        return "No X results found."
    output = []
    for item in items[:10]:
        handle = item.get("handle", "")
        text = item.get("text", "")[:200]
        likes = item.get("likes", 0)
        output.append(f"- @{handle}: {text} (❤{likes})")
    return "\n".join(output)


def format_youtube(items: list[dict]) -> str:
    if not items:
        return "No YouTube results found."
    output = []
    for item in items[:10]:
        title = item.get("title", "")[:100]
        url = item.get("url", "")
        output.append(f"- [{title}]({url})")
    return "\n".join(output)


def format_web(items: list[dict]) -> str:
    if not items:
        return "No web results found."
    output = []
    for item in items[:10]:
        title = item.get("title", "")[:100]
        url = item.get("url", "")
        desc = item.get("description", "")[:150]
        output.append(f"- [{title}]({url})\n  {desc}")
    return "\n".join(output)


def format_polymarket(items: list[dict]) -> str:
    if not items:
        return "No Polymarket markets found."
    output = []
    for item in items[:10]:
        question = item.get("question", "")[:100]
        url = item.get("url", "")
        prob = item.get("probabilities", "")
        vol = item.get("volume", 0)
        vol_str = f"${vol:,.0f}" if vol else "N/A"
        output.append(f"- [{question}]({url})\n  {prob} | Vol: {vol_str}")
    return "\n".join(output)


def detect_query_type(topic: str) -> str:
    topic_lower = topic.lower()
    if re.search(r'\bvs\.?\b|\bversus\b', topic_lower, re.IGNORECASE):
        return "COMPARISON"
    if re.search(r'\bbest\b|\btop\b|\brecommended\b', topic_lower):
        return "RECOMMENDATIONS"
    if re.search(r'\bnews\b|\bhappening\b|\blatest\b|\bupdate\b', topic_lower):
        return "NEWS"
    return "GENERAL"


def synthesize(topic: str, reddit_results: list, hn_results: list, 
               x_results: list, yt_results: list, web_results: list,
               polymarket_results: list,
               query_type: str, mode: str) -> str:
    """Build the final markdown report."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    slug = slugify(topic)
    
    # Cross-platform detection (simplified)
    cross_platform = []
    all_titles = {item.get("title", "")[:60]: item["source"] 
                  for item in reddit_results[:5] + hn_results[:5] + web_results[:5]
                  if item.get("title")}
    for title, src in all_titles.items():
        cross_platform.append(f"- **{title}** — found on {src.upper()}")
    
    # Also detect polymarket cross-platform
    for item in polymarket_results[:3]:
        q = item.get("question", "")[:60]
        if q:
            cross_platform.append(f"- **{q}** — Polymarket market (real-money signal)")
    
    reddit_formatted = format_reddit(reddit_results)
    hn_formatted = format_hn(hn_results)
    x_formatted = format_x(x_results)
    yt_formatted = format_youtube(yt_results)
    web_formatted = format_web(web_results)
    polymarket_formatted = format_polymarket(polymarket_results)
    
    report = f"""# 📰 Research: {topic}

**Date:** {date_str}  
**Mode:** {mode}  
**Type:** {query_type}

---

## 🔥 Cross-Platform Signals
{chr(10).join(cross_platform[:5]) if cross_platform else "No cross-platform signals detected."}

---

## Reddit 💬
{reddit_formatted}

---

## Hacker News ▲
{hn_formatted}

---

## X/Twitter 🐦
{x_formatted}

---

## YouTube 🎥
{yt_formatted}

---

## Polymarket 🎰
{polymarket_formatted}

---

## Web Search 🌐
{web_formatted}

---

## Stats

| Source | Results |
|--------|---------|
| Reddit | {len(reddit_results)} |
| Hacker News | {len(hn_results)} |
| X/Twitter | {len(x_results)} |
| YouTube | {len(yt_results)} |
| Polymarket | {len(polymarket_results)} |
| Web | {len(web_results)} |

---

*Saved to: ~/Documents/Last30Days/{slug}-{date_str[:10]}.md*
"""
    
    return report


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="last30 research script")
    parser.add_argument("topic", help="Topic to research")
    parser.add_argument("--emit", default="report", help="Output format (report, compact, json)")
    parser.add_argument("--save-dir", default=None, help="Directory to save results")
    parser.add_argument("--x-handle", default=None, help="X handle to search")
    parser.add_argument("--no-native-web", action="store_true", help="Skip native web search")
    parser.add_argument("--days", type=int, default=30, help="Days to look back")
    parser.add_argument("--quick", action="store_true", help="Quick mode")
    parser.add_argument("--deep", action="store_true", help="Deep mode")
    
    args = parser.parse_args()
    topic = args.topic
    
    global SAVE_DIR
    if args.save_dir:
        SAVE_DIR = args.save_dir
    
    mode = "quick" if args.quick else ("deep" if args.deep else "balanced")
    
    log(f"Researching: {topic} [{mode}]")
    
    query_type = detect_query_type(topic)
    log(f"Detected query type: {query_type}")
    
    # Run all searches
    log("Searching Reddit...")
    reddit_results = search_reddit(topic, mode)
    log(f"  → {len(reddit_results)} Reddit results")
    
    log("Searching Hacker News...")
    hn_results = search_hn(topic, mode)
    log(f"  → {len(hn_results)} HN results")
    
    log("Searching X/Twitter...")
    x_results = search_x(topic, mode)
    log(f"  → {len(x_results)} X results")
    
    log("Searching YouTube...")
    yt_results = search_youtube(topic, mode)
    log(f"  → {len(yt_results)} YouTube results")
    
    log("Searching Web...")
    web_results = search_web(topic, mode)
    log(f"  → {len(web_results)} web results")
    
    log("Searching Polymarket...")
    polymarket_results = search_polymarket(topic, mode)
    log(f"  → {len(polymarket_results)} Polymarket results")
    
    # Synthesize
    report = synthesize(
        topic, reddit_results, hn_results, x_results, 
        yt_results, web_results, polymarket_results, query_type, mode
    )
    
    # Save
    filepath = save_file(slugify(topic), report)
    log(f"Saved to: {filepath}")
    
    if args.emit == "json":
        print(json.dumps({
            "topic": topic,
            "query_type": query_type,
            "reddit": reddit_results,
            "hn": hn_results,
            "x": x_results,
            "youtube": yt_results,
            "polymarket": polymarket_results,
            "web": web_results,
            "report": report,
        }, indent=2))
    elif args.emit == "compact":
        # Short summary for comparison mode
        top_items = sorted(
            reddit_results[:3] + hn_results[:3] + web_results[:3],
            key=score_item, reverse=True
        )
        print(json.dumps({
            "topic": topic,
            "top": [{"source": i["source"], "title": i.get("title", i.get("text",""))[:100]} for i in top_items]
        }))
    else:
        print(report)


if __name__ == "__main__":
    main()

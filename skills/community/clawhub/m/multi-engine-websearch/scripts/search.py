#!/usr/bin/env python3
"""
Multi-engine web search aggregator for OpenClaw.
6 engines: DuckDuckGo, DDG Lite, Yahoo, Yahoo JP, Startpage, Google (headless).
Merges, deduplicates, ranks by cross-engine frequency.
No API keys required.
"""

import argparse
import json
import sys
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote_plus, unquote
from urllib.request import Request, urlopen
import re

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
]
_ua_index = 0

def next_ua():
    global _ua_index
    ua = USER_AGENTS[_ua_index % len(USER_AGENTS)]
    _ua_index += 1
    return ua

def fetch(url, extra_headers=None, timeout=8):
    """Fast HTTP fetch with short timeout."""
    h = {
        "User-Agent": next_ua(),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "identity",
        "Connection": "close",
    }
    if extra_headers:
        h.update(extra_headers)
    try:
        req = Request(url, headers=h)
        with urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return ""

def clean(text):
    """Strip HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#x27;|&#39;", "'", text)
    text = re.sub(r"&mdash;", "—", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ── Engines ───────────────────────────────────────────────────────────────────

def search_duckduckgo(query, num):
    """DuckDuckGo HTML — most reliable, no bot detection."""
    html = fetch(f"https://html.duckduckgo.com/html/?q={quote_plus(query)}")
    if not html:
        return "duckduckgo", []
    results = []
    raw_urls = re.findall(r'class="result__a"[^>]*href="//duckduckgo\.com/l/\?uddg=([^&"]+)', html)
    titles   = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
    snips    = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
    snip_idx = 0
    for i, raw in enumerate(raw_urls):
        real_url = unquote(raw)
        if "duckduckgo.com" in real_url:
            continue
        title   = clean(titles[i]) if i < len(titles) else ""
        snippet = clean(snips[snip_idx]) if snip_idx < len(snips) else ""
        snip_idx += 1
        if real_url.startswith("http") and title:
            results.append({"title": title, "url": real_url, "snippet": snippet})
        if len(results) >= num:
            break
    return "duckduckgo", results


def search_ddg_lite(query, num):
    """DuckDuckGo Lite — lightweight endpoint."""
    html = fetch(f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}")
    if not html:
        return "ddg_lite", []
    results = []
    pairs = re.findall(
        r'href="//duckduckgo\.com/l/\?uddg=([^&"]+)[^"]*"[^>]*class=[\'"]?result-link[\'"]?[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    if not pairs:
        pairs = re.findall(
            r'class=[\'"]?result-link[\'"]?[^>]*href="//duckduckgo\.com/l/\?uddg=([^&"]+)[^"]*"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
    snips = re.findall(r'class=[\'"]?result-snippet[\'"]?[^>]*>(.*?)</td>', html, re.DOTALL)
    snip_idx = 0
    for raw, title in pairs:
        real_url = unquote(raw)
        if "duckduckgo.com" in real_url:
            continue
        snippet = clean(snips[snip_idx]) if snip_idx < len(snips) else ""
        snip_idx += 1
        t = clean(title)
        if real_url.startswith("http") and t:
            results.append({"title": t, "url": real_url, "snippet": snippet})
        if len(results) >= num:
            break
    return "ddg_lite", results


def search_yahoo(query, num):
    """Yahoo Search — uses RU=/RK= redirect pattern."""
    html = fetch(f"https://search.yahoo.com/search?p={quote_plus(query)}&n={num}")
    if not html:
        return "yahoo", []
    results = []
    all_ru = re.findall(r'/RU=([^/]+)/RK=', html)
    titles = re.findall(r'class="title[^"]*"[^>]*>.*?<span[^>]*>([^<]+)</span>', html, re.DOTALL)
    titles = [t for t in titles if t.strip() and t.strip() != ' ']
    snips = re.findall(r'class="compText[^"]*"[^>]*>.*?<p[^>]*>(.*?)</p>', html, re.DOTALL)

    seen_urls = set()
    url_list = []
    for ru in all_ru:
        decoded = unquote(ru)
        if decoded.startswith("http") and decoded not in seen_urls:
            if not any(x in decoded for x in ["yahoo.com", "yimg.com", "google.com", "bing.com"]):
                seen_urls.add(decoded)
                url_list.append(decoded)

    for i, url in enumerate(url_list[:num]):
        results.append({
            "title":   clean(titles[i]) if i < len(titles) else url.split("/")[2],
            "url":     url,
            "snippet": clean(snips[i]) if i < len(snips) else "",
        })
    return "yahoo", results


def search_yahoo_jp(query, num):
    """Yahoo Japan — independent index, different results."""
    html = fetch(f"https://search.yahoo.co.jp/search?p={quote_plus(query)}&n={num}")
    if not html:
        return "yahoo_jp", []
    results = []
    items = re.findall(r'<h3[^>]*>.*?<a[^>]+href="(https?://(?!search\.yahoo\.co\.jp)[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    snips = re.findall(r'<p[^>]+class="[^"]*supplement[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    for i, (href, title) in enumerate(items[:num]):
        results.append({
            "title":   clean(title),
            "url":     href,
            "snippet": clean(snips[i]) if i < len(snips) else "",
        })
    return "yahoo_jp", results


def search_startpage(query, num):
    """Startpage — Google results with privacy."""
    html = fetch(f"https://www.startpage.com/search?q={quote_plus(query)}&cat=web&language=english")
    if not html:
        return "startpage", []
    results = []
    items = re.findall(
        r'<a[^>]+class="[^"]*result-title[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    if not items:
        items = re.findall(
            r'<a[^>]+href="([^"]+)"[^>]+class="[^"]*result-title[^"]*"[^>]*>(.*?)</a>',
            html, re.DOTALL
        )
    snips = re.findall(r'<p[^>]+class="[^"]*description[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    for i, (href, title) in enumerate(items[:num]):
        real_url = unquote(href) if not href.startswith("http") else href
        if not real_url.startswith("http"):
            continue
        results.append({
            "title":   clean(title),
            "url":     real_url,
            "snippet": clean(snips[i]) if i < len(snips) else "",
        })
    return "startpage", results


def search_google(query, num):
    """Google — headless Chromium via Playwright (renders JS)."""
    import os
    import importlib.util
    script_dir = os.path.dirname(os.path.abspath(__file__))
    headless_path = os.path.join(script_dir, "google_headless.py")
    spec = importlib.util.spec_from_file_location("google_headless", headless_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    results = mod.search_google_headless(query, num)
    return "google", results


# ── Aggregator ────────────────────────────────────────────────────────────────

ENGINES = {
    "duckduckgo": search_duckduckgo,
    "ddg_lite":   search_ddg_lite,
    "yahoo":      search_yahoo,
    "yahoo_jp":   search_yahoo_jp,
    "startpage":  search_startpage,
    "google":     search_google,
}

DEFAULT_ENGINES = ["duckduckgo", "ddg_lite", "yahoo", "yahoo_jp", "startpage", "google"]

def url_key(url):
    """Normalize URL for deduplication."""
    url = re.sub(r"^https?://(www\.)?", "", url.lower().rstrip("/"))
    # Remove tracking params
    url = re.sub(r"[?&](utm_\w+|ref|source|fbclid|gclid)=[^&]*", "", url)
    return hashlib.md5(url.encode()).hexdigest()

def aggregate(query, engines, num_per_engine=10, max_results=50):
    """Run all engines in parallel, merge and rank results."""
    seen = {}
    score = {}
    engine_hits = {}
    fns = [(name, ENGINES[name]) for name in engines if name in ENGINES]

    with ThreadPoolExecutor(max_workers=len(fns)) as pool:
        futures = {pool.submit(fn, query, num_per_engine): name for name, fn in fns}
        for future in as_completed(futures, timeout=30):
            engine_name = futures[future]
            try:
                _, results = future.result(timeout=25)
                engine_hits[engine_name] = len(results)
                for r in results:
                    if not r.get("url") or not r.get("title"):
                        continue
                    k = url_key(r["url"])
                    if k not in seen:
                        seen[k] = dict(r)
                        seen[k]["engines"] = []
                        score[k] = 0
                    seen[k]["engines"].append(engine_name)
                    score[k] += 1
                    # Keep the longest snippet
                    if len(r.get("snippet", "")) > len(seen[k].get("snippet", "")):
                        seen[k]["snippet"] = r["snippet"]
            except Exception as e:
                engine_hits[engine_name] = 0

    ranked = sorted(seen.values(), key=lambda r: (-score[url_key(r["url"])], r.get("title", "")))
    return ranked[:max_results], engine_hits

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Multi-engine web search — no API keys needed")
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--engines", "-e", default=",".join(DEFAULT_ENGINES),
                        help=f"Comma-separated engines or 'all' (default: {','.join(DEFAULT_ENGINES)})")
    parser.add_argument("--num", "-n", type=int, default=10, help="Results per engine (default: 10)")
    parser.add_argument("--max", "-m", type=int, default=50, help="Max total results (default: 50)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--list-engines", action="store_true", help="List available engines")
    args = parser.parse_args()

    if args.list_engines:
        print("Available engines:", ", ".join(ENGINES.keys()))
        print("Default engines:", ", ".join(DEFAULT_ENGINES))
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    query   = " ".join(args.query)
    engines = list(ENGINES.keys()) if args.engines == "all" else \
              [e.strip() for e in args.engines.split(",")]

    results, engine_hits = aggregate(query, engines, args.num, args.max)

    if args.json:
        print(json.dumps({
            "query":   query,
            "total":   len(results),
            "engines": engine_hits,
            "results": results,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"\n🔍 Search: {query}")
        print(f"📡 Engines: {', '.join(engine_hits.keys())}")
        print(f"✅ {len(results)} unique results\n")
        print("─" * 70)
        for i, r in enumerate(results, 1):
            cross = f"[{len(r.get('engines', []))} engines]"
            print(f"\n{i}. {r['title']}  {cross}")
            print(f"   🔗 {r['url']}")
            if r.get("snippet"):
                print(f"   {r['snippet'][:200]}")
            print(f"   📊 {', '.join(r.get('engines', []))}")

if __name__ == "__main__":
    main()

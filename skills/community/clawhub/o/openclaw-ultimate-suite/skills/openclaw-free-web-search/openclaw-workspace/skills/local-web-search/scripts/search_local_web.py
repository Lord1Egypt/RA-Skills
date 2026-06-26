#!/usr/bin/env python3
# SECURITY MANIFEST:
#   Environment variables accessed: LOCAL_SEARCH_URL (optional), LOCAL_SEARCH_FALLBACK_URL (optional),
#                                   LOCAL_SEARCH_PROXY (optional), HTTPS_PROXY/ALL_PROXY variants (optional)
#   External endpoints called: http://127.0.0.1:18080 (local SearXNG, default), https://searx.be (fallback only)
#   Local files read: ~/.openclaw/workspace/skills/local-web-search/.project_root (path hint only)
#   Local files written: none
#   Data sent externally: search query string only — no personal data, no credentials
"""
search_local_web.py  v3.1  — OpenClaw Free Web Search Skill
============================================================
Multi-engine parallel search via local SearXNG + public fallback.
Zero API keys required. 100% free and private.

New in v3.1:
  - Automatic proxy detection (env vars + common local ports 7890/7897/1080)
  - Proxy forwarded to Scrapling Fetcher for public SearXNG instances

Features from v3.0 (Scrapling integration):
  - Scrapling Fetcher used for SearXNG requests: TLS fingerprint spoofing,
    realistic browser headers, Google referer — dramatically improves
    acceptance rate on public SearXNG instances
  - stdlib urllib used as fallback when Scrapling is not installed
  - User-Agent is now a real Chrome UA (not "OpenClawFreeSearch/...")
  - Result quality score formula upgraded: title quality + snippet density added
  - Freshness filter: results older than --max-age-days are downranked
  - --browse flag: auto-call browse_page.py on top result for immediate content

Features:
  - Agent Reach        : intent-aware query expansion (2-3 sub-queries)
  - Multi-engine       : parallel Bing/DuckDuckGo/Google/Startpage/Qwant
  - Anti-hallucination : cross-engine validation + domain authority scoring
  - Invalid page filter: removes paywalls, error pages, low-quality domains
  - Deduplication      : URL-level dedup + cross-engine count
  - Fallback chain     : local SearXNG -> public fallback -> graceful error

Usage:
  python3 search_local_web.py --query "OpenAI latest model" --limit 5
  python3 search_local_web.py --query "python async" --intent tutorial
  python3 search_local_web.py --query "AI news" --intent news --freshness day
  python3 search_local_web.py --query "UW iSchool dean" --browse

Model-agnostic: works with any LLM acting as OpenClaw commander
(Claude, GPT-4, Gemini, Mistral, Llama, DeepSeek, Qwen, etc.)
"""

from __future__ import annotations
import argparse
import json
import os
import socket
import subprocess
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

# ─── Scrapling import with graceful fallback ──────────────────────────────────
try:
    from scrapling.fetchers import Fetcher as _ScraplingFetcher
    SCRAPLING_AVAILABLE = True
except Exception:
    SCRAPLING_AVAILABLE = False

# ─── Configuration ────────────────────────────────────────────────────────────
DEFAULT_LOCAL_URL   = os.environ.get("LOCAL_SEARCH_URL",          "http://127.0.0.1:18080")
PUBLIC_FALLBACK_URL = os.environ.get("LOCAL_SEARCH_FALLBACK_URL", "https://searx.be")

# Realistic Chrome User-Agent
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

ALL_ENGINES = ["bing", "duckduckgo", "google", "startpage", "qwant"]

INTENT_ENGINE_MAP = {
    "factual":    ["bing", "google", "duckduckgo"],
    "news":       ["bing", "duckduckgo", "google"],
    "research":   ["google", "startpage", "bing"],
    "tutorial":   ["google", "bing", "duckduckgo"],
    "comparison": ["google", "bing", "startpage"],
    "privacy":    ["duckduckgo", "startpage", "qwant"],
    "general":    ["bing", "duckduckgo", "google"],
}

# Domain authority scores (0-100)
AUTHORITY_TIER = {
    "github.com": 90, "stackoverflow.com": 88, "docs.python.org": 92,
    "developer.mozilla.org": 90, "arxiv.org": 88, "wikipedia.org": 82,
    "nature.com": 90, "pubmed.ncbi.nlm.nih.gov": 92,
    "openai.com": 85, "anthropic.com": 85, "huggingface.co": 83,
    "techcrunch.com": 72, "theverge.com": 72, "arstechnica.com": 75,
    "bbc.com": 80, "reuters.com": 82, "apnews.com": 82,
    "medium.com": 55, "dev.to": 58, "reddit.com": 50,
    "news.ycombinator.com": 65,
}

INVALID_URL_PATTERNS = [
    "login", "signin", "signup", "register", "subscribe", "paywall",
    "premium", "checkout", "cart", "404", "error", "not-found",
    "page-not-found", "captcha", "verify", "challenge",
]

INVALID_CONTENT_PATTERNS = [
    "access denied", "403 forbidden", "404 not found", "page not found",
    "subscribe to read", "sign in to continue", "enable javascript",
    "please enable cookies", "this content is for subscribers",
]

# Proxy auto-detection: common local proxy ports (Clash, V2Ray, Shadowsocks)
COMMON_PROXY_PORTS = ("7890", "7897", "1080")


# ─── Proxy detection ──────────────────────────────────────────────────────────

def _port_open(host: str, port: str, timeout: float = 0.3) -> bool:
    """Check if a local port is accepting connections."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def _resolve_proxy_url() -> Optional[str]:
    """
    Resolve proxy URL from environment variables or auto-detect common local proxies.
    Priority: LOCAL_SEARCH_PROXY > HTTPS_PROXY > ALL_PROXY > auto-detect ports.
    """
    for env_name in ("LOCAL_SEARCH_PROXY", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy"):
        value = os.environ.get(env_name)
        if value:
            return value
    for port in COMMON_PROXY_PORTS:
        if _port_open("127.0.0.1", port):
            return f"http://127.0.0.1:{port}"
    return None


def _should_relax_tls(proxy_url: Optional[str]) -> bool:
    """Relax TLS verification for local MITM proxies (Clash, mitmproxy, etc.)."""
    if not proxy_url:
        return False
    return proxy_url.startswith("http://127.0.0.1:") or proxy_url.startswith("http://localhost:")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _project_root() -> str:
    marker = (
        Path.home() / ".openclaw" / "workspace"
        / "skills" / "local-web-search" / ".project_root"
    )
    return marker.read_text().strip() if marker.exists() else "<your-project-directory>"


def _is_invalid_url(url: str) -> bool:
    u = url.lower()
    return any(p in u for p in INVALID_URL_PATTERNS)


def _is_invalid_content(snippet: str) -> bool:
    if not snippet:
        return False
    s = snippet.lower()
    return any(p in s for p in INVALID_CONTENT_PATTERNS)


def _domain_authority(url: str) -> float:
    try:
        host = urllib.parse.urlparse(url).netloc.lower().lstrip("www.")
        if host in AUTHORITY_TIER:
            return AUTHORITY_TIER[host]
        for d, sc in AUTHORITY_TIER.items():
            if host.endswith("." + d):
                return sc
        return 40.0
    except Exception:
        return 40.0


def _freshness_score(pub: str) -> float:
    if not pub:
        return 0.3
    try:
        import datetime
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d", "%Y/%m/%d"):
            try:
                dt = datetime.datetime.strptime(pub[:len(fmt)], fmt)
                d = (datetime.datetime.utcnow() - dt).days
                if d <= 1:   return 1.0
                if d <= 7:   return 0.9
                if d <= 30:  return 0.75
                if d <= 90:  return 0.6
                if d <= 365: return 0.45
                return 0.25
            except ValueError:
                continue
    except Exception:
        pass
    return 0.3


def _snippet_density(snippet: str) -> float:
    """Score based on snippet word count (more = better, up to 50 words)."""
    if not snippet:
        return 0.0
    wc = len(snippet.split())
    return min(wc / 50.0, 1.0)


def _title_quality(title: str) -> float:
    """Penalise very short or generic titles."""
    if not title:
        return 0.0
    wc = len(title.split())
    if wc <= 1:
        return 0.2
    if wc <= 3:
        return 0.5
    return 1.0


def _score(item: dict) -> float:
    """
    Composite quality score (0-100):
      35% domain authority
      20% freshness
      20% cross-engine validation
      15% snippet density
      10% title quality
    """
    return round(
        _domain_authority(item.get("url", "")) * 0.35
        + _freshness_score(item.get("publishedDate", "")) * 100 * 0.20
        + item.get("_engine_count", 1) * 8 * 0.20
        + _snippet_density(item.get("content", "")) * 100 * 0.15
        + _title_quality(item.get("title", "")) * 100 * 0.10,
        2,
    )


def _expand_query(query: str, intent: str) -> list:
    q = [query]
    if intent == "news":
        q += [f"{query} latest 2025 2026", f"{query} breaking news"]
    elif intent == "research":
        q += [f"{query} paper study", f"{query} github implementation"]
    elif intent == "comparison":
        q += [f"{query} pros cons difference", f"{query} which is better"]
    elif intent == "tutorial":
        q += [f"{query} how to guide example"]
    elif intent == "factual":
        q += [f"{query} official documentation"]
    # Deduplicate
    seen, result = [], []
    for x in q:
        if x not in seen:
            seen.append(x)
            result.append(x)
    return result


# ─── Fetch logic ──────────────────────────────────────────────────────────────

def _fetch_single_scrapling(base_url: str, query: str, engine: str,
                             limit: int, freshness: str) -> list:
    """Use Scrapling Fetcher for realistic browser-like requests."""
    params = {
        "q": query, "format": "json", "language": "en-US",
        "pageno": "1", "engines": engine,
    }
    if freshness:
        params["time_range"] = freshness
    url = f"{base_url}/search?{urllib.parse.urlencode(params)}"
    proxy_url = _resolve_proxy_url()
    request_kwargs = {
        "stealthy_headers": True,
        "timeout": 15,
        "follow_redirects": True,
    }
    if proxy_url and base_url.startswith("https://"):
        request_kwargs["proxy"] = proxy_url
        if _should_relax_tls(proxy_url):
            request_kwargs["verify"] = False
    try:
        page = _ScraplingFetcher.get(url, **request_kwargs)
        if page.status != 200:
            return []
        data = json.loads(page.body.decode("utf-8", errors="replace"))
        results = data.get("results", [])
        for x in results:
            x["_engines_seen"] = {engine}
        return results
    except Exception:
        return []


def _fetch_single_stdlib(base_url: str, query: str, engine: str,
                          limit: int, freshness: str) -> list:
    """stdlib urllib fallback with realistic Chrome UA."""
    params = {
        "q": query, "format": "json", "language": "en-US",
        "pageno": "1", "engines": engine,
    }
    if freshness:
        params["time_range"] = freshness
    url = f"{base_url}/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": BROWSER_UA,
        "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
            results = data.get("results", [])
            for x in results:
                x["_engines_seen"] = {engine}
            return results
    except Exception:
        return []


def _fetch_single(base_url: str, query: str, engine: str,
                  limit: int, freshness: str) -> list:
    """Route to Scrapling or stdlib based on availability."""
    if SCRAPLING_AVAILABLE:
        return _fetch_single_scrapling(base_url, query, engine, limit, freshness)
    return _fetch_single_stdlib(base_url, query, engine, limit, freshness)


def _parallel_search(base_url: str, queries: list, engines: list,
                     limit: int, freshness: str,
                     max_age_days: int = None) -> list:
    tasks = [
        (base_url, q, e, limit, freshness)
        for q in queries
        for e in engines
    ]
    raw = []
    with ThreadPoolExecutor(max_workers=min(len(tasks), 8)) as pool:
        futures = {pool.submit(_fetch_single, *t): t for t in tasks}
        for f in as_completed(futures):
            try:
                raw.extend(f.result())
            except Exception:
                pass

    # Merge by URL
    url_map: dict = {}
    for item in raw:
        url = (item.get("url") or "").strip()
        if not url:
            continue
        if url in url_map:
            url_map[url]["_engines_seen"].update(item.get("_engines_seen", set()))
            if len(item.get("content", "")) > len(url_map[url].get("content", "")):
                url_map[url]["content"] = item["content"]
            if item.get("publishedDate") and not url_map[url].get("publishedDate"):
                url_map[url]["publishedDate"] = item["publishedDate"]
        else:
            url_map[url] = dict(item)
            url_map[url].setdefault("_engines_seen", set())

    merged = []
    for _, item in url_map.items():
        seen_engines = item.pop("_engines_seen", set())
        item["_engine_count"] = len(seen_engines)
        item["_seen_in_engines"] = sorted(seen_engines)
        merged.append(item)

    valid = [
        item for item in merged
        if not _is_invalid_url(item.get("url", ""))
        and not _is_invalid_content(item.get("content", ""))
    ]

    if max_age_days:
        import datetime
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=max_age_days)

        def _is_too_old(item: dict) -> bool:
            pub = item.get("publishedDate", "")
            if not pub:
                return False
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
                try:
                    dt = datetime.datetime.strptime(pub[:len(fmt)], fmt)
                    return dt < cutoff
                except ValueError:
                    continue
            return False

        for item in valid:
            if _is_too_old(item):
                item["_age_penalty"] = True

    for item in valid:
        score = _score(item)
        if item.get("_age_penalty"):
            score *= 0.5
        item["_score"] = score

    valid.sort(key=lambda item: item["_score"], reverse=True)
    return valid[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OpenClaw Free Web Search v3.1 — multi-engine, Scrapling-powered, zero API key."
    )
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=5,
                        help="Max results to return (default: 5)")
    parser.add_argument("--intent",
                        choices=["factual", "news", "research", "tutorial",
                                 "comparison", "privacy", "general"],
                        default="general",
                        help="Query intent — selects optimal engine set")
    parser.add_argument("--engines", default=None,
                        help="Override engines (comma-separated): bing,duckduckgo,google,startpage,qwant")
    parser.add_argument("--freshness",
                        choices=["hour", "day", "week", "month", "year"],
                        default=None,
                        help="Filter results by recency")
    parser.add_argument("--max-age-days", type=int, default=None,
                        help="Downrank results older than N days")
    parser.add_argument("--no-expand", action="store_true",
                        help="Disable Agent Reach query expansion")
    parser.add_argument("--browse", action="store_true",
                        help="Auto-browse top result with browse_page.py after search")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()

    if args.engines:
        engines = [e.strip() for e in args.engines.split(",")
                   if e.strip() in ALL_ENGINES]
        if not engines:
            print(f"ERROR: No valid engines. Available: {', '.join(ALL_ENGINES)}",
                  file=sys.stderr)
            return 1
    else:
        engines = INTENT_ENGINE_MAP.get(args.intent, INTENT_ENGINE_MAP["general"])

    queries = [args.query] if args.no_expand else _expand_query(args.query, args.intent)

    results = []
    used_url = DEFAULT_LOCAL_URL
    for base_url in [DEFAULT_LOCAL_URL, PUBLIC_FALLBACK_URL]:
        if not base_url:
            continue
        results = _parallel_search(
            base_url, queries, engines, args.limit, args.freshness, args.max_age_days
        )
        if results:
            used_url = base_url
            break

    if not results:
        root = _project_root()
        print("ERROR: All search sources returned no results.", file=sys.stderr)
        print(f'Start local SearXNG: cd "{root}" && ./start_local_search.sh',
              file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, indent=2, default=str))
        return 0

    is_fallback = used_url != DEFAULT_LOCAL_URL
    fetcher_label = "Scrapling (TLS fingerprint)" if SCRAPLING_AVAILABLE else "stdlib urllib"
    print(f"Query     : {args.query}")
    print(f"Intent    : {args.intent}")
    print(f"Engines   : {', '.join(engines)}")
    print(f"Fetcher   : {fetcher_label}")
    if len(queries) > 1:
        print(f"Expanded  : {len(queries)} sub-queries (Agent Reach)")
    if args.freshness:
        print(f"Freshness : {args.freshness}")
    if args.max_age_days:
        print(f"Max age   : {args.max_age_days} days")
    source_label = f"public fallback ({used_url})" if is_fallback else "local SearXNG"
    print(f"Source    : {source_label}")
    print(f"Results   : {len(results)}")
    print()

    for idx, item in enumerate(results, 1):
        title = (item.get("title") or "").strip() or "(no title)"
        url = (item.get("url") or "").strip() or "(no url)"
        snippet = " ".join((item.get("content") or "").split())
        published = (item.get("publishedDate") or "").strip()
        seen_engines = ", ".join(item.get("_seen_in_engines", []))
        score = item.get("_score", 0)
        cross_validated = item.get("_engine_count", 1) > 1
        aged = item.get("_age_penalty", False)

        print(f"{idx}. {title}")
        print(f"   URL      : {url}")
        if published:
            print(f"   Published: {published}")
        if seen_engines:
            line = f"   Engines  : {seen_engines}"
            if cross_validated:
                line += "  [cross-validated]"
            print(line)
        score_line = f"   Score    : {score:.1f}/100"
        if aged:
            score_line += "  [age-penalised]"
        print(score_line)
        if snippet:
            print(f"   Snippet  : {snippet[:300]}{'...' if len(snippet) > 300 else ''}")
        print()

    cross_count = sum(1 for item in results if item.get("_engine_count", 1) > 1)
    print("-" * 60)
    print(f"AGENT NOTE: {cross_count}/{len(results)} results cross-validated across engines.")
    print("  -> Prefer higher Score + [cross-validated] results.")
    print("  -> Use browse_page.py to read full page before answering.")
    print("  -> Do NOT state facts from snippets alone — always verify via page content.")
    if not SCRAPLING_AVAILABLE:
        print("  -> TIP: pip install scrapling[all] for better public instance acceptance rate.")
    print("-" * 60)

    if args.browse and results:
        top_url = (results[0].get("url") or "").strip()
        if top_url:
            print()
            print(f"[--browse] Auto-fetching top result: {top_url}")
            print()
            browse_script = Path(__file__).parent / "browse_page.py"
            try:
                subprocess.run(
                    [sys.executable, str(browse_script), "--url", top_url, "--max-words", "600"],
                    check=False,
                )
            except Exception as exc:
                print(f"browse_page.py error: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

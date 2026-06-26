#!/usr/bin/env python3
"""
Polymarket Command Center — standalone CLI tool for prediction market queries.
Read-only interface to Gamma and CLOB APIs. Zero API key required.

Usage:
    polymarket_commands.py trending [category]
    polymarket_commands.py odds <slug>
    polymarket_commands.py search <query>
    polymarket_commands.py watchlist

Examples:
    polymarket_commands.py trending
    polymarket_commands.py trending politics
    polymarket_commands.py odds will-trump-win-2024
    polymarket_commands.py search "bitcoin 100k"
    polymarket_commands.py watchlist
"""

import json
import time
import sys
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import threading


# ── Configuration ────────────────────────────────────────────────────────────

GAMMA_BASE = "https://gamma-api.polymarket.com"
CLOB_BASE = "https://clob.polymarket.com"

# State directory for config and watchlist
STATE_DIR = Path.home() / ".openclaw" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)
WATCHLIST_FILE = STATE_DIR / "polymarket_watchlist.json"


def _load_watchlist() -> list:
    """Load watchlist from JSON file or return empty list."""
    if WATCHLIST_FILE.exists():
        try:
            with open(WATCHLIST_FILE) as f:
                data = json.load(f)
                return data.get("slugs", []) if isinstance(data, dict) else []
        except (json.JSONDecodeError, IOError):
            return []
    return []


WATCHLIST = _load_watchlist()


# ── In-Memory Cache (thread-safe, bounded) ──────────────────────────────────

_cache: dict = {}
_cache_lock = threading.Lock()
_CACHE_MAX_SIZE = 100


def _cache_get(key: str, ttl: int = 120) -> Optional[dict]:
    """Get cached value if not expired. Default 2min TTL. Thread-safe."""
    with _cache_lock:
        entry = _cache.get(key)
        if entry and time.time() - entry["ts"] < ttl:
            return entry["data"]
        if entry:
            del _cache[key]
        return None


def _cache_set(key: str, data):
    """Set cache entry. Evicts oldest if over max size. Thread-safe."""
    with _cache_lock:
        _cache[key] = {"data": data, "ts": time.time()}
        if len(_cache) > _CACHE_MAX_SIZE:
            sorted_keys = sorted(_cache.keys(), key=lambda k: _cache[k]["ts"])
            for k in sorted_keys[:len(_cache) - _CACHE_MAX_SIZE]:
                del _cache[k]


# ── HTTP Client ──────────────────────────────────────────────────────────────

def _gamma_get(path: str, params: dict = None, timeout: int = 10) -> Optional[list | dict]:
    """GET request to Gamma API. Returns parsed JSON or None on failure."""
    url = f"{GAMMA_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-Polymarket/1.0",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def _clob_get(path: str, params: dict = None, timeout: int = 10) -> Optional[dict]:
    """GET request to CLOB API. Returns parsed JSON or None on failure."""
    url = f"{CLOB_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-Polymarket/1.0",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError):
        return None


# ── Parsing Helpers ──────────────────────────────────────────────────────────

def _parse_outcome_prices(raw: str) -> list:
    """Parse outcomePrices field — comes as stringified JSON array."""
    if not raw:
        return []
    try:
        if isinstance(raw, list):
            return [float(p) for p in raw]
        return [float(p) for p in json.loads(raw)]
    except (json.JSONDecodeError, ValueError, TypeError):
        return []


def _parse_outcomes(raw: str) -> list:
    """Parse outcomes field — comes as stringified JSON array."""
    if not raw:
        return ["Yes", "No"]
    try:
        if isinstance(raw, list):
            return raw
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError, TypeError):
        return ["Yes", "No"]


def _format_volume(vol) -> str:
    """Format volume number for display."""
    try:
        v = float(vol)
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M"
        if v >= 1_000:
            return f"${v / 1_000:.0f}K"
        return f"${v:.0f}"
    except (ValueError, TypeError):
        return "$?"


def _days_until(end_date_str: str) -> Optional[int]:
    """Calculate days until market closes."""
    if not end_date_str:
        return None
    try:
        clean = end_date_str.replace("Z", "+00:00")
        end = datetime.fromisoformat(clean)
        now = datetime.now(timezone.utc)
        delta = (end - now).days
        return max(0, delta)
    except (ValueError, AttributeError, TypeError):
        return None


def _pct(price: float) -> str:
    """Format price as percentage string."""
    return f"{price * 100:.0f}%"


# ── Command Functions ────────────────────────────────────────────────────────

def trending_command(category: str = "") -> str:
    """Get trending/high-volume active markets from Polymarket.

    Args:
        category: optional category filter (e.g. "politics", "crypto", "sports")
    """
    cache_key = f"trending:{category}"
    cached = _cache_get(cache_key, ttl=180)
    if cached:
        return cached

    params = {
        "active": "true",
        "closed": "false",
        "limit": "15",
        "order": "volume",
        "ascending": "false",
    }

    tag = (category or "").strip().lower()
    if tag:
        params["tag"] = tag

    markets = _gamma_get("/markets", params)
    if not markets:
        return "❌ Couldn't reach Polymarket. Try again in a minute."

    if not isinstance(markets, list) or len(markets) == 0:
        return f"❌ No active markets found{' for ' + tag if tag else ''}."

    lines = []
    header = f"🔮 Polymarket Trending" + (f" ({tag})" if tag else "")
    lines.append(header)
    lines.append("")

    for i, mkt in enumerate(markets[:10], 1):
        question = (mkt.get("question") or "?")[:65]
        prices = _parse_outcome_prices(mkt.get("outcomePrices", ""))
        outcomes = _parse_outcomes(mkt.get("outcomes", ""))
        vol = _format_volume(mkt.get("volumeNum") or mkt.get("volume", 0))
        days = _days_until(mkt.get("endDate", ""))
        days_str = f"{days}d" if days is not None else "?"
        slug = mkt.get("slug", "")

        # Format prices for binary markets
        if len(prices) >= 2 and len(outcomes) >= 2:
            yes_pct = _pct(prices[0])
            lines.append(f"{i}. {question}")
            lines.append(f"   {outcomes[0]}: {yes_pct} | Vol: {vol} | Closes: {days_str}")
        elif len(prices) >= 1:
            lines.append(f"{i}. {question}")
            lines.append(f"   {_pct(prices[0])} | Vol: {vol} | Closes: {days_str}")
        else:
            lines.append(f"{i}. {question}")
            lines.append(f"   Vol: {vol} | Closes: {days_str}")

        if slug:
            lines.append(f"   📎 {slug}")
        lines.append("")

    lines.append("💡 Say 'odds [slug]' for detailed odds on any market")

    result = "\n".join(lines)
    _cache_set(cache_key, result)
    return result


def odds_command(slug_or_query: str = "") -> str:
    """Get detailed odds for a specific market by slug or search query.

    Args:
        slug_or_query: market slug (from trending) or a search term
    """
    if not slug_or_query.strip():
        return "❌ Give me a market slug or search term. Try 'trending' first to see options."

    query = slug_or_query.strip()

    # Try exact slug match first
    market = _gamma_get(f"/markets/{query}")

    # If that fails, search by slug parameter
    if not market or isinstance(market, list):
        results = _gamma_get("/markets", {"slug": query, "limit": "1"})
        if results and isinstance(results, list) and len(results) > 0:
            market = results[0]
        else:
            # Fall back to text search
            results = _gamma_get("/markets", {
                "active": "true",
                "closed": "false",
                "limit": "5",
            })
            if results and isinstance(results, list):
                query_lower = query.lower()
                matched = [m for m in results if query_lower in (m.get("question", "") + m.get("slug", "")).lower()]
                if matched:
                    market = matched[0]

    if not market or isinstance(market, list):
        return f"❌ No market found for '{query}'. Try 'trending' to see active markets."

    # Build detailed view
    question = market.get("question", "?")
    prices = _parse_outcome_prices(market.get("outcomePrices", ""))
    outcomes = _parse_outcomes(market.get("outcomes", ""))
    vol = _format_volume(market.get("volumeNum") or market.get("volume", 0))
    liq = _format_volume(market.get("liquidityNum") or market.get("liquidity", 0))
    days = _days_until(market.get("endDate", ""))
    days_str = f"{days} days" if days is not None else "?"
    end_date = market.get("endDate", "?")[:10]
    slug = market.get("slug", "")
    description = (market.get("description") or "")[:200]

    lines = [f"🔮 {question}", ""]

    # Outcome prices with visual bars
    for j, outcome in enumerate(outcomes):
        if j < len(prices):
            bar_len = int(prices[j] * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"{outcome}: {_pct(prices[j])} {bar}")

    lines.append("")
    lines.append(f"📊 Volume: {vol} | Liquidity: {liq}")
    lines.append(f"📅 Closes: {end_date} ({days_str})")

    if description:
        lines.append(f"\n📝 {description}")

    # Try to get CLOB data for live bid/ask
    clob_tokens = market.get("clobTokenIds", "")
    if clob_tokens:
        try:
            if isinstance(clob_tokens, str):
                clob_tokens = json.loads(clob_tokens)
            if clob_tokens and len(clob_tokens) > 0:
                mid = _clob_get(f"/midpoint", {"token_id": clob_tokens[0]})
                if mid and "mid" in mid:
                    lines.append(f"\n💹 Live midpoint: {float(mid['mid']) * 100:.1f}%")
        except Exception:
            pass

    lines.append(f"\n🔗 polymarket.com/event/{slug}")

    return "\n".join(lines)


def search_command(query: str = "") -> str:
    """Search Polymarket for markets matching a query.

    Args:
        query: search terms (e.g. "bitcoin 100k", "trump", "fed rate")
    """
    if not query.strip():
        return "❌ Give me something to search for. e.g. 'search bitcoin' or 'search election'"

    cache_key = f"search:{query.strip().lower()}"
    cached = _cache_get(cache_key, ttl=120)
    if cached:
        return cached

    # Gamma API doesn't have text search endpoint — fetch and filter client-side
    params = {
        "active": "true",
        "closed": "false",
        "limit": "100",
        "order": "volume",
        "ascending": "false",
    }

    markets = _gamma_get("/markets", params)
    if not markets:
        return "❌ Couldn't reach Polymarket. Try again in a minute."

    if not isinstance(markets, list):
        return "❌ Couldn't reach Polymarket. Try again in a minute."

    # Client-side search across question + slug + description
    query_lower = query.strip().lower()
    terms = query_lower.split()

    def matches(mkt):
        text = (
            (mkt.get("question") or "") + " " +
            (mkt.get("slug") or "") + " " +
            (mkt.get("description") or "")
        ).lower()
        return all(t in text for t in terms)

    matched = [m for m in markets if matches(m)]

    if not matched:
        return f"❌ No active markets matching '{query}'. Try broader terms."

    lines = [f"🔍 Polymarket search: '{query}'", ""]

    for i, mkt in enumerate(matched[:8], 1):
        question = (mkt.get("question") or "?")[:65]
        prices = _parse_outcome_prices(mkt.get("outcomePrices", ""))
        vol = _format_volume(mkt.get("volumeNum") or mkt.get("volume", 0))
        slug = mkt.get("slug", "")

        yes_pct = _pct(prices[0]) if prices else "?"
        lines.append(f"{i}. {question}")
        lines.append(f"   Yes: {yes_pct} | Vol: {vol}")
        if slug:
            lines.append(f"   📎 {slug}")
        lines.append("")

    lines.append("💡 Say 'odds [slug]' for details on any market")

    result = "\n".join(lines)
    _cache_set(cache_key, result)
    return result


def watchlist_command() -> str:
    """Check odds on your watchlist markets."""
    slugs = WATCHLIST
    if not slugs:
        return "❌ No watchlist configured. Create ~/.openclaw/state/polymarket_watchlist.json with market slugs."

    lines = ["👀 Polymarket Watchlist", ""]

    for slug in slugs:
        results = _gamma_get("/markets", {"slug": slug, "limit": "1"})
        if not results or not isinstance(results, list) or len(results) == 0:
            lines.append(f"❌ {slug}: not found")
            continue

        mkt = results[0]
        question = (mkt.get("question") or "?")[:55]
        prices = _parse_outcome_prices(mkt.get("outcomePrices", ""))
        vol = _format_volume(mkt.get("volumeNum") or mkt.get("volume", 0))

        yes_pct = _pct(prices[0]) if prices else "?"
        lines.append(f"🔮 {question}")
        lines.append(f"   Yes: {yes_pct} | Vol: {vol}")
        lines.append("")

    return "\n".join(lines)


def get_market_summary(slug: str) -> dict:
    """Get market summary dict for use in morning briefs and proactive triggers.

    Returns dict with: question, yes_pct, volume, days_left, slug
    or empty dict on failure.
    """
    results = _gamma_get("/markets", {"slug": slug, "limit": "1"})
    if not results or not isinstance(results, list) or len(results) == 0:
        return {}

    mkt = results[0]
    prices = _parse_outcome_prices(mkt.get("outcomePrices", ""))
    days = _days_until(mkt.get("endDate", ""))

    return {
        "question": mkt.get("question", "?"),
        "yes_pct": round(prices[0] * 100, 1) if prices else None,
        "no_pct": round(prices[1] * 100, 1) if len(prices) > 1 else None,
        "volume": mkt.get("volumeNum") or mkt.get("volume", 0),
        "volume_fmt": _format_volume(mkt.get("volumeNum") or mkt.get("volume", 0)),
        "days_left": days,
        "slug": mkt.get("slug", ""),
        "active": mkt.get("active", False),
    }


def get_trending_summary(limit: int = 5) -> list:
    """Get top trending markets as summary dicts for morning briefs.

    Returns list of dicts with: question, yes_pct, volume_fmt, slug
    """
    markets = _gamma_get("/markets", {
        "active": "true",
        "closed": "false",
        "limit": str(limit),
        "order": "volume",
        "ascending": "false",
    })

    if not markets or not isinstance(markets, list):
        return []

    summaries = []
    for mkt in markets[:limit]:
        prices = _parse_outcome_prices(mkt.get("outcomePrices", ""))
        summaries.append({
            "question": (mkt.get("question") or "?")[:60],
            "yes_pct": round(prices[0] * 100, 1) if prices else None,
            "volume_fmt": _format_volume(mkt.get("volumeNum") or mkt.get("volume", 0)),
            "slug": mkt.get("slug", ""),
        })

    return summaries


# ── Main Entry Point ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Polymarket Command Center — prediction market query tool",
        epilog="Examples: %(prog)s trending politics | %(prog)s odds will-trump-win-2024 | %(prog)s search bitcoin",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # trending command
    trending_parser = subparsers.add_parser("trending", help="Get trending markets by volume")
    trending_parser.add_argument("category", nargs="?", default="", help="Optional category filter (politics, crypto, sports, etc.)")

    # odds command
    odds_parser = subparsers.add_parser("odds", help="Get detailed odds for a market")
    odds_parser.add_argument("slug", help="Market slug or search term")

    # search command
    search_parser = subparsers.add_parser("search", help="Search for markets")
    search_parser.add_argument("query", nargs="+", help="Search terms")

    # watchlist command
    watchlist_parser = subparsers.add_parser("watchlist", help="Check odds on your watchlist")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "trending":
        result = trending_command(args.category)
        print(result)
        return 0

    elif args.command == "odds":
        result = odds_command(args.slug)
        print(result)
        return 0

    elif args.command == "search":
        query = " ".join(args.query)
        result = search_command(query)
        print(result)
        return 0

    elif args.command == "watchlist":
        result = watchlist_command()
        print(result)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

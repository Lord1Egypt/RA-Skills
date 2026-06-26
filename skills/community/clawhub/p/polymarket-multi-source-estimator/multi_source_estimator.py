#!/usr/bin/env python3
"""
Multi-Source LLM Estimator for Prediction Markets
===================================================
A self-contained trading bot that enriches an LLM with real-time data from
10+ sources to estimate true probabilities. Trades when the LLM's estimate
diverges significantly from the current market price.

Sources: RSS news, FRED economic data, GDELT geopolitical sentiment,
Odds API (sports), FiveThirtyEight polling, Congress.gov bills, OpenFDA
drug approvals, Open-Meteo weather, USGS earthquakes, Finnhub earnings,
plus cross-platform prices from Manifold and Kalshi.

Usage:
    python multi_source_estimator.py              # dry-run
    python multi_source_estimator.py --live        # live trading
    python multi_source_estimator.py --quiet       # errors only
    python multi_source_estimator.py --max-markets 20
"""

import os
import re
import sys
import json
import time
import hashlib
import logging
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_SLUG = "polymarket-multi-source-estimator"
TRADE_SOURCE = SKILL_SLUG

log = logging.getLogger(SKILL_SLUG)

# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------

def get_client() -> SimmerClient:
    """Create a Simmer client for the configured trading venue."""
    venue = os.environ.get("TRADING_VENUE", "sim").strip().lower()
    api_key = os.environ.get("SIMMER_API_KEY", "")
    return SimmerClient(api_key=api_key, venue=venue)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: Cache infrastructure
# ═══════════════════════════════════════════════════════════════════════════
_cache: dict = {}  # key -> {"data": ..., "ts": float}


def _get_cached(key: str, ttl: int):
    """Return cached data if fresh, else None."""
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < ttl:
        return entry["data"]
    return None


def _set_cache(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}


def _safe_get(url: str, params: dict = None, headers: dict = None,
              timeout: int = 15):
    """HTTP GET with error handling. Returns parsed JSON or None."""
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        if resp.ok:
            return resp.json()
    except Exception:
        pass
    return None


def _safe_get_text(url: str, params: dict = None, headers: dict = None,
                   timeout: int = 15):
    """HTTP GET returning raw text or None."""
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        if resp.ok:
            return resp.text
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: Category detection
# ═══════════════════════════════════════════════════════════════════════════
_CATEGORY_KEYWORDS = {
    "politics": [
        "president", "election", "vote", "senate", "congress", "democrat",
        "republican", "trump", "biden", "governor", "impeach", "cabinet",
        "primary", "nominee", "legislation", "bill", "law", "veto",
        "supreme court", "scotus", "executive order", "inaugurat",
    ],
    "economics": [
        "fed", "federal reserve", "rate cut", "rate hike", "interest rate",
        "inflation", "cpi", "gdp", "recession", "unemployment", "jobs",
        "tariff", "trade war", "treasury", "bond", "yield", "deficit",
        "debt ceiling", "stimulus", "quantitative",
    ],
    "crypto": [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "solana", "sol",
        "defi", "nft", "binance", "coinbase", "sec crypto", "etf",
        "halving", "stablecoin", "usdc", "usdt", "blockchain",
    ],
    "sports": [
        "nba", "nfl", "mlb", "nhl", "ufc", "mma", "soccer", "football",
        "basketball", "baseball", "tennis", "boxing", "champion",
        "playoff", "super bowl", "world cup", "finals", "match",
        "premier league", "la liga", "serie a", "bundesliga",
        "olympics", "medal", "tournament", "grand slam",
    ],
    "geopolitics": [
        "war", "conflict", "nato", "military", "missile", "nuclear",
        "sanction", "ceasefire", "invasion", "territory", "border",
        "ukraine", "russia", "china", "taiwan", "iran", "israel",
        "gaza", "north korea", "coup", "regime",
    ],
    "weather": [
        "temperature", "hurricane", "tornado", "flood", "drought",
        "wildfire", "earthquake", "tsunami", "storm", "heat wave",
        "cold", "snow", "rainfall", "climate", "el nino", "la nina",
    ],
    "pharma": [
        "fda", "drug", "vaccine", "approval", "clinical trial", "pharma",
        "medicine", "treatment", "therapy", "biotech", "pfizer",
        "moderna", "mrna", "medical",
    ],
    "entertainment": [
        "oscar", "grammy", "emmy", "golden globe", "movie", "film",
        "album", "spotify", "netflix", "disney", "box office",
        "eurovision", "awards", "celebrity", "concert",
    ],
}


def detect_categories(question: str) -> list:
    """Detect relevant categories from question text. Returns top 3 by score."""
    q_lower = question.lower()
    scores = {}
    for cat, keywords in _CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q_lower)
        if score > 0:
            scores[cat] = score
    return [cat for cat, _ in sorted(scores.items(), key=lambda x: -x[1])][:3]


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: Team aliases for sports matching
# ═══════════════════════════════════════════════════════════════════════════
_TEAM_ALIASES = {
    # NBA
    "lakers": "los angeles lakers", "celtics": "boston celtics",
    "warriors": "golden state warriors", "bucks": "milwaukee bucks",
    "76ers": "philadelphia 76ers", "sixers": "philadelphia 76ers",
    "knicks": "new york knicks", "nets": "brooklyn nets",
    "heat": "miami heat", "nuggets": "denver nuggets",
    "suns": "phoenix suns", "clippers": "los angeles clippers",
    "mavs": "dallas mavericks", "mavericks": "dallas mavericks",
    "thunder": "oklahoma city thunder", "cavaliers": "cleveland cavaliers",
    "cavs": "cleveland cavaliers", "pacers": "indiana pacers",
    "magic": "orlando magic", "hawks": "atlanta hawks",
    "bulls": "chicago bulls", "raptors": "toronto raptors",
    "rockets": "houston rockets", "grizzlies": "memphis grizzlies",
    "pelicans": "new orleans pelicans", "kings": "sacramento kings",
    "spurs": "san antonio spurs", "blazers": "portland trail blazers",
    "jazz": "utah jazz", "pistons": "detroit pistons",
    "hornets": "charlotte hornets", "wizards": "washington wizards",
    # NFL
    "chiefs": "kansas city chiefs", "eagles": "philadelphia eagles",
    "bills": "buffalo bills", "49ers": "san francisco 49ers",
    "cowboys": "dallas cowboys", "ravens": "baltimore ravens",
    "lions": "detroit lions", "dolphins": "miami dolphins",
    "bengals": "cincinnati bengals", "steelers": "pittsburgh steelers",
    "jets": "new york jets", "giants": "new york giants",
    "packers": "green bay packers", "bears": "chicago bears",
    "vikings": "minnesota vikings", "saints": "new orleans saints",
    "chargers": "los angeles chargers", "rams": "los angeles rams",
    "seahawks": "seattle seahawks", "commanders": "washington commanders",
    "patriots": "new england patriots", "broncos": "denver broncos",
    "raiders": "las vegas raiders", "jaguars": "jacksonville jaguars",
    "texans": "houston texans", "titans": "tennessee titans",
    "colts": "indianapolis colts", "panthers": "carolina panthers",
    "falcons": "atlanta falcons", "cardinals": "arizona cardinals",
    "browns": "cleveland browns", "buccaneers": "tampa bay buccaneers",
    # MLB
    "yankees": "new york yankees", "dodgers": "los angeles dodgers",
    "red sox": "boston red sox", "astros": "houston astros",
    "braves": "atlanta braves", "mets": "new york mets",
    "cubs": "chicago cubs", "white sox": "chicago white sox",
    "phillies": "philadelphia phillies", "padres": "san diego padres",
    # NHL
    "bruins": "boston bruins", "maple leafs": "toronto maple leafs",
    "oilers": "edmonton oilers", "avalanche": "colorado avalanche",
    "hurricanes": "carolina hurricanes", "rangers": "new york rangers",
    "penguins": "pittsburgh penguins", "lightning": "tampa bay lightning",
    "wild": "minnesota wild", "stars": "dallas stars",
    "canadiens": "montreal canadiens", "flames": "calgary flames",
    "canucks": "vancouver canucks", "blackhawks": "chicago blackhawks",
    "red wings": "detroit red wings", "kraken": "seattle kraken",
    "golden knights": "vegas golden knights",
}


def _expand_team_names(question: str) -> set:
    """Expand team nicknames to full names for better matching."""
    q_lower = question.lower()
    q_words = set(re.sub(r"[^a-z0-9\s]", "", q_lower).split())
    expanded = set(q_words)
    for alias, full_name in _TEAM_ALIASES.items():
        if alias in q_lower:
            expanded.update(full_name.lower().split())
    return expanded


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: Data sources (1-10)
# ═══════════════════════════════════════════════════════════════════════════

# --- Source 1: RSS News (20 feeds, keyword pre-filter) ---
# Top 10 high-credibility RSS feeds covering news, finance, politics, and crypto.
# Add more feeds here to expand coverage (any RSS/Atom URL works).
RSS_FEEDS = {
    "reuters": "https://feeds.reuters.com/reuters/topNews",
    "bbc_world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
    "cnbc": "https://www.cnbc.com/id/20910258/device/rss/rss.html",
    "wsj": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "politico": "https://www.politico.com/rss/politicopicks.xml",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "guardian": "https://www.theguardian.com/world/rss",
    "cointelegraph": "https://cointelegraph.com/rss",
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
}
_RSS_TTL = 300  # 5 min

# Junk headline keywords to filter out
_JUNK_KEYWORDS = {
    "recipe", "horoscope", "crossword", "sudoku", "quiz",
    "beauty tips", "fashion", "viral video", "celebrity gossip",
    "travel tips", "how to cook", "best restaurants", "lifestyle",
    "book review", "movie review", "music review",
}

# Stopwords for keyword matching
_STOPWORDS = {
    "will", "the", "be", "in", "on", "at", "by", "to", "of", "a",
    "an", "is", "it", "or", "and", "for", "this", "that", "with",
    "has", "have", "had", "not", "but", "from", "are", "was", "were",
    "do", "does", "did", "can", "could", "would", "should", "may",
    "if", "than", "more", "most", "before", "after", "between",
}


def _fetch_rss_headlines() -> list:
    """Fetch headlines from all RSS feeds. Cached 5 min."""
    cached = _get_cached("rss_all", _RSS_TTL)
    if cached is not None:
        return cached

    articles = []

    def _fetch_one(name: str, url: str) -> list:
        result = []
        try:
            resp = requests.get(url, timeout=10,
                                headers={"User-Agent": "MultiSourceEstimator/1.0"})
            if not resp.ok:
                return []
            root = ET.fromstring(resp.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = root.findall(".//item") or root.findall(".//atom:entry", ns)
            for item in items[:10]:
                title = (
                    item.findtext("title") or
                    item.findtext("atom:title", namespaces=ns) or ""
                ).strip()
                if title:
                    result.append({"title": title, "source": name})
        except Exception:
            pass
        return result

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_fetch_one, n, u): n for n, u in RSS_FEEDS.items()}
        for fut in as_completed(futures, timeout=20):
            try:
                articles.extend(fut.result())
            except Exception:
                pass

    _set_cache("rss_all", articles)
    return articles


def _match_news(question: str, max_results: int = 5) -> list:
    """Find top N headlines relevant to the question via keyword overlap."""
    headlines = _fetch_rss_headlines()
    if not headlines:
        return []

    q_words = set(re.sub(r"[^a-z0-9\s]", "", question.lower()).split()) - _STOPWORDS

    scored = []
    for art in headlines:
        title_lower = art["title"].lower()
        if any(junk in title_lower for junk in _JUNK_KEYWORDS):
            continue
        t_words = set(re.sub(r"[^a-z0-9\s]", "", title_lower).split()) - _STOPWORDS
        overlap = q_words & t_words
        key_overlap = [w for w in overlap if len(w) >= 4]
        score = len(overlap) + len(key_overlap)  # entities count double
        if score >= 2:
            scored.append((score, art))

    scored.sort(key=lambda x: -x[0])
    seen, results = set(), []
    for _, art in scored:
        title_key = re.sub(r"[^a-z]", "", art["title"].lower())[:40]
        if title_key not in seen:
            seen.add(title_key)
            results.append(f"[{art['source']}] {art['title']}")
            if len(results) >= max_results:
                break
    return results


# --- Source 2: FRED (Federal Reserve Economic Data) ---
_FRED_TTL = 3600
_FRED_SERIES = {
    "FEDFUNDS": "Federal Funds Rate",
    "CPIAUCSL": "Consumer Price Index (CPI)",
    "GDP": "Real GDP",
    "UNRATE": "Unemployment Rate",
    "T10Y2Y": "10Y-2Y Treasury Spread",
    "VIXCLS": "VIX Volatility Index",
    "DCOILWTICO": "WTI Crude Oil Price",
    "GOLDAMGBD228NLBM": "Gold Price",
    "DEXUSEU": "USD/EUR Exchange Rate",
    "SP500": "S&P 500 Index",
}
_FRED_KEYWORD_MAP = {
    "fed": ["FEDFUNDS", "T10Y2Y"], "federal reserve": ["FEDFUNDS", "T10Y2Y"],
    "interest rate": ["FEDFUNDS", "T10Y2Y"], "rate cut": ["FEDFUNDS"],
    "rate hike": ["FEDFUNDS"], "inflation": ["CPIAUCSL"], "cpi": ["CPIAUCSL"],
    "gdp": ["GDP"], "recession": ["GDP", "UNRATE", "T10Y2Y"],
    "unemployment": ["UNRATE"], "jobs": ["UNRATE"], "oil": ["DCOILWTICO"],
    "crude": ["DCOILWTICO"], "gold": ["GOLDAMGBD228NLBM"], "vix": ["VIXCLS"],
    "volatility": ["VIXCLS"], "s&p": ["SP500"], "stock market": ["SP500", "VIXCLS"],
    "dollar": ["DEXUSEU"], "euro": ["DEXUSEU"], "yield curve": ["T10Y2Y"],
    "treasury": ["T10Y2Y"],
}


def _get_fred_context(question: str) -> list:
    """Fetch relevant FRED economic indicators."""
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key:
        return []

    q_lower = question.lower()
    relevant = set()
    for kw, series_list in _FRED_KEYWORD_MAP.items():
        if kw in q_lower:
            relevant.update(series_list)
    if not relevant:
        return []

    results = []
    for sid in list(relevant)[:4]:
        cache_key = f"fred_{sid}"
        cached = _get_cached(cache_key, _FRED_TTL)
        if cached is not None:
            results.append(cached)
            continue
        data = _safe_get(
            "https://api.stlouisfed.org/fred/series/observations",
            params={"series_id": sid, "api_key": api_key, "file_type": "json",
                    "sort_order": "desc", "limit": 5}
        )
        if not data or "observations" not in data:
            continue
        for o in data["observations"]:
            if o.get("value") and o["value"] != ".":
                val = float(o["value"])
                name = _FRED_SERIES.get(sid, sid)
                line = f"FRED {name}: {val:.2f} (as of {o['date']})"
                _set_cache(cache_key, line)
                results.append(line)
                break
    return results


# --- Source 3: GDELT (geopolitical sentiment) ---
_GDELT_TTL = 900
_GDELT_QUERIES = {
    "ukraine": "ukraine russia war conflict",
    "china": "china taiwan military tension",
    "iran": "iran nuclear sanctions",
    "israel": "israel gaza hamas conflict",
    "north korea": "north korea missile nuclear",
    "trade": "trade war tariff sanctions",
}


def _get_gdelt_context(question: str) -> list:
    """Fetch GDELT tone/sentiment for geopolitical topics."""
    q_lower = question.lower()
    results = []
    for topic, query in _GDELT_QUERIES.items():
        if topic not in q_lower:
            continue
        cache_key = f"gdelt_{hashlib.md5(query.encode()).hexdigest()[:8]}"
        cached = _get_cached(cache_key, _GDELT_TTL)
        if cached is not None:
            results.append(cached)
            continue
        data = _safe_get(
            "https://api.gdeltproject.org/api/v2/doc/doc",
            params={"query": query, "mode": "tonechart", "format": "json",
                    "timespan": "1d"}
        )
        if not data:
            continue
        tones = data if isinstance(data, list) else data.get("timeline", [])
        if not tones:
            continue
        avg_tone = sum(t.get("tone", 0) for t in tones[-10:]) / max(len(tones[-10:]), 1)
        tone_desc = ("very negative" if avg_tone < -5 else "negative" if avg_tone < -2
                     else "neutral" if avg_tone < 2 else "positive" if avg_tone < 5
                     else "very positive")
        line = (f"GDELT sentiment on '{topic}': {tone_desc} "
                f"(tone={avg_tone:.1f}, {len(tones)} articles/24h)")
        _set_cache(cache_key, line)
        results.append(line)
    return results


# --- Source 4: Odds API (sports bookmaker consensus) ---
_ODDS_TTL = 3600
_SPORT_KEYS = {
    "nba": "basketball_nba", "nfl": "americanfootball_nfl",
    "nhl": "icehockey_nhl", "mlb": "baseball_mlb",
    "ufc": "mma_mixed_martial_arts", "mma": "mma_mixed_martial_arts",
    "premier league": "soccer_epl", "champions league": "soccer_uefa_champions_league",
    "la liga": "soccer_spain_la_liga", "world cup": "soccer_fifa_world_cup",
    "bundesliga": "soccer_germany_bundesliga", "serie a": "soccer_italy_serie_a",
}


def _get_odds_context(question: str) -> list:
    """Fetch bookmaker odds for sports questions."""
    api_key = os.environ.get("ODDS_API_KEY", "")
    if not api_key:
        return []

    q_lower = question.lower()
    results = []
    for keyword, sport_key in _SPORT_KEYS.items():
        if keyword not in q_lower:
            continue
        cache_key = f"odds_{sport_key}"
        cached = _get_cached(cache_key, _ODDS_TTL)
        if cached is None:
            cached = _safe_get(
                f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds",
                params={"apiKey": api_key, "regions": "us,eu",
                        "markets": "h2h", "oddsFormat": "decimal"}
            )
            if cached:
                _set_cache(cache_key, cached)
        if not cached:
            continue

        q_words = _expand_team_names(question)
        for event in cached[:20]:
            home = event.get("home_team", "")
            away = event.get("away_team", "")
            teams_words = set(re.sub(r"[^a-z0-9\s]", "",
                                     f"{home} {away}".lower()).split())
            key_overlap = [w for w in (q_words & teams_words) if len(w) >= 3]
            if len(key_overlap) >= 1:
                for bm in event.get("bookmakers", [])[:3]:
                    for mkt in bm.get("markets", []):
                        if mkt.get("key") != "h2h":
                            continue
                        probs = {o["name"]: f"{1/o['price']:.0%}"
                                 for o in mkt.get("outcomes", []) if o["price"] > 1}
                        prob_str = ", ".join(f"{n}: {p}" for n, p in probs.items())
                        results.append(f"Bookmaker {bm['title']}: "
                                       f"{home} vs {away} - {prob_str}")
                    break
                break
        break
    return results[:3]


# --- Source 5: FiveThirtyEight polling ---
_538_TTL = 3600


def _get_538_context(question: str) -> list:
    """Fetch 538 presidential approval polling."""
    q_lower = question.lower()
    if not any(kw in q_lower for kw in ["approval", "election", "poll",
                                         "president", "biden", "trump"]):
        return []
    cached = _get_cached("538_approval", _538_TTL)
    if cached is not None:
        return cached
    text = _safe_get_text(
        "https://projects.fivethirtyeight.com/polls/data/approval_averages.csv")
    if not text:
        return []
    results = []
    for line in reversed(text.strip().split("\n")[-30:]):
        parts = line.split(",")
        if len(parts) >= 5 and "All polls" in line:
            try:
                approve, disapprove = float(parts[-2]), float(parts[-1])
                results.append(f"538 Approval: approve {approve:.1f}%, "
                               f"disapprove {disapprove:.1f}%")
                break
            except (ValueError, IndexError):
                pass
    _set_cache("538_approval", results)
    return results


# --- Source 6: Congress.gov (bill tracking) ---
_CONGRESS_TTL = 1800


def _get_congress_context(question: str) -> list:
    """Fetch legislation status from Congress.gov."""
    api_key = os.environ.get("CONGRESS_API_KEY", "")
    if not api_key:
        return []
    q_lower = question.lower()
    if not any(kw in q_lower for kw in ["bill", "law", "legislation", "act",
                                         "congress", "senate", "house", "pass"]):
        return []
    cached = _get_cached("congress_recent", _CONGRESS_TTL)
    if cached is None:
        data = _safe_get("https://api.congress.gov/v3/bill",
                         params={"api_key": api_key, "format": "json",
                                 "limit": 30, "sort": "updateDate+desc"})
        if data and "bills" in data:
            cached = data["bills"]
            _set_cache("congress_recent", cached)
        else:
            return []

    q_words = set(re.sub(r"[^a-z0-9\s]", "", q_lower).split())
    q_words -= {"will", "the", "be", "pass", "in", "congress", "bill", "act", "law"}
    results = []
    for bill in cached[:30]:
        title = bill.get("title", "")
        b_words = set(re.sub(r"[^a-z0-9\s]", "", title.lower()).split())
        key_overlap = [w for w in (q_words & b_words) if len(w) >= 4]
        if len(key_overlap) >= 2:
            status = bill.get("latestAction", {}).get("text", "unknown status")
            results.append(f"Congress: '{title[:80]}' - {status[:60]}")
            if len(results) >= 2:
                break
    return results


# --- Source 7: OpenFDA (drug approvals) ---
_FDA_TTL = 3600


def _get_fda_context(question: str) -> list:
    """Fetch FDA drug approval data."""
    q_lower = question.lower()
    if not any(kw in q_lower for kw in ["fda", "drug", "approv", "vaccine",
                                         "clinical trial", "pharma"]):
        return []
    cached = _get_cached("fda_recent", _FDA_TTL)
    if cached is None:
        today = datetime.utcnow().strftime("%Y%m%d")
        month_ago = (datetime.utcnow() - timedelta(days=60)).strftime("%Y%m%d")
        data = _safe_get("https://api.fda.gov/drug/drugsfda.json",
                         params={"search": f"submissions.submission_status_date:"
                                 f"[{month_ago}+TO+{today}]", "limit": 30})
        if data and "results" in data:
            cached = data["results"]
            _set_cache("fda_recent", cached)
        else:
            return []
    results = []
    for drug in cached:
        brand = drug.get("openfda", {}).get("brand_name", [""])[0]
        generic = drug.get("openfda", {}).get("generic_name", [""])[0]
        if brand.lower() in q_lower or generic.lower() in q_lower:
            subs = drug.get("submissions", [{}])[0]
            status = subs.get("submission_status", "unknown")
            results.append(f"FDA: {brand or generic} - status: {status}")
            if len(results) >= 2:
                break
    return results


# --- Source 8: Open-Meteo (weather forecasts) ---
_METEO_TTL = 1800
_CITIES = {
    "new york": (40.71, -74.01), "los angeles": (34.05, -118.24),
    "chicago": (41.88, -87.63), "london": (51.51, -0.13),
    "paris": (48.86, 2.35), "tokyo": (35.68, 139.69),
    "miami": (25.76, -80.19), "houston": (29.76, -95.37),
    "phoenix": (33.45, -112.07),
}


def _get_meteo_context(question: str) -> list:
    """Fetch weather forecast for a relevant city."""
    q_lower = question.lower()
    target = None
    for city, coords in _CITIES.items():
        if city in q_lower:
            target = (city, coords)
            break
    if not target:
        return []
    city_name, (lat, lon) = target
    cache_key = f"meteo_{city_name}"
    cached = _get_cached(cache_key, _METEO_TTL)
    if cached is not None:
        return cached
    data = _safe_get("https://api.open-meteo.com/v1/forecast",
                     params={"latitude": lat, "longitude": lon,
                             "daily": "temperature_2m_max,temperature_2m_min",
                             "forecast_days": 16, "temperature_unit": "fahrenheit"})
    if not data or "daily" not in data:
        return []
    daily = data["daily"]
    dates, maxes, mins = daily.get("time", []), daily.get("temperature_2m_max", []), \
        daily.get("temperature_2m_min", [])
    temps = [f"{dates[i]}: {mins[i]:.0f}-{maxes[i]:.0f}F"
             for i in range(min(7, len(dates)))]
    output = [f"Weather {city_name.title()}: " + ", ".join(temps)]
    _set_cache(cache_key, output)
    return output


# --- Source 9: USGS (earthquakes) ---
_USGS_TTL = 3600


def _get_usgs_context(question: str) -> list:
    """Fetch significant earthquake data."""
    q_lower = question.lower()
    if not any(kw in q_lower for kw in ["earthquake", "seismic", "quake",
                                         "magnitude", "richter"]):
        return []
    cached = _get_cached("usgs_quakes", _USGS_TTL)
    if cached is None:
        data = _safe_get(
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
            "significant_month.geojson")
        if data and "features" in data:
            cached = data["features"]
            _set_cache("usgs_quakes", cached)
        else:
            return []
    results = []
    for quake in cached[:5]:
        props = quake.get("properties", {})
        mag = props.get("mag", 0)
        place = props.get("place", "unknown")
        ts = props.get("time", 0)
        date = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d") if ts else "?"
        results.append(f"Earthquake M{mag} at {place} ({date})")
    return results[:3]


# --- Source 10: Finnhub (earnings/IPO calendar) ---
_FINNHUB_TTL = 3600


def _get_finnhub_context(question: str) -> list:
    """Fetch earnings calendar data."""
    api_key = os.environ.get("FINNHUB_API_KEY", "")
    if not api_key:
        return []
    q_lower = question.lower()
    if not any(kw in q_lower for kw in ["earnings", "revenue", "ipo", "stock",
                                         "quarterly", "profit", "market cap"]):
        return []
    today = datetime.utcnow().strftime("%Y-%m-%d")
    future = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
    cached = _get_cached("finnhub_earnings", _FINNHUB_TTL)
    if cached is None:
        data = _safe_get("https://finnhub.io/api/v1/calendar/earnings",
                         params={"from": today, "to": future, "token": api_key})
        if data and "earningsCalendar" in data:
            cached = data["earningsCalendar"]
            _set_cache("finnhub_earnings", cached)
        else:
            cached = []
    results = []
    for entry in cached[:50]:
        symbol = entry.get("symbol", "")
        if symbol.lower() in q_lower:
            date = entry.get("date", "?")
            est = entry.get("epsEstimate")
            results.append(f"Earnings: {symbol} on {date}"
                           + (f", EPS est: ${est}" if est else ""))
            if len(results) >= 2:
                break
    return results


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: Context orchestrator
# ═══════════════════════════════════════════════════════════════════════════

def fetch_context(question: str, category: str = "",
                  market_price: float = 0.5, max_chars: int = 2000) -> str:
    """
    Gather real-time context from all relevant sources in parallel.
    Returns a formatted string (max ~2000 chars) for injection into the LLM prompt.
    """
    categories = detect_categories(question)
    if category and category not in categories:
        categories.insert(0, category)

    parts = []

    # Always fetch news
    news = _match_news(question)
    if news:
        parts.append("RECENT NEWS:\n" + "\n".join(news))

    # Dispatch category-specific sources in parallel
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {}
        if any(c in categories for c in ["economics", "crypto"]):
            futures[pool.submit(_get_fred_context, question)] = "FRED"
        if "geopolitics" in categories:
            futures[pool.submit(_get_gdelt_context, question)] = "GDELT"
        if "sports" in categories:
            futures[pool.submit(_get_odds_context, question)] = "ODDS"
        if "politics" in categories:
            futures[pool.submit(_get_538_context, question)] = "538"
            futures[pool.submit(_get_congress_context, question)] = "CONGRESS"
        if "pharma" in categories:
            futures[pool.submit(_get_fda_context, question)] = "FDA"
        if "weather" in categories:
            futures[pool.submit(_get_meteo_context, question)] = "METEO"
        if any(kw in question.lower() for kw in ["earthquake", "quake", "seismic"]):
            futures[pool.submit(_get_usgs_context, question)] = "USGS"
        if any(kw in question.lower() for kw in ["earnings", "ipo", "revenue", "stock"]):
            futures[pool.submit(_get_finnhub_context, question)] = "FINNHUB"

        for fut in as_completed(futures, timeout=25):
            try:
                result = fut.result()
                if result:
                    source_name = futures[fut]
                    parts.append(f"{source_name} DATA:\n" + "\n".join(result))
            except Exception:
                pass

    if not parts:
        return ""

    full = "\n\n".join(parts)
    if len(full) > max_chars:
        full = full[:max_chars - 3] + "..."
    return full


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: Cross-platform price fetching
# ═══════════════════════════════════════════════════════════════════════════
_manifold_cache = None
_manifold_ts = 0.0
_kalshi_cache = None
_kalshi_ts = 0.0

MANIFOLD_URL = "https://api.manifold.markets/v0"
KALSHI_URL = "https://trading-api.kalshi.com/trade-api/v2"


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _word_overlap(a: str, b: str) -> float:
    """Jaccard word overlap score with entity boost and length penalty."""
    stops = {"will", "the", "be", "in", "on", "at", "by", "of", "or", "a",
             "and", "is", "to", "who", "win", "wins", "this", "that", "with"}
    wa = set(_normalize(a).split()) - stops
    wb = set(_normalize(b).split()) - stops
    if not wa or not wb:
        return 0.0
    overlap = wa & wb
    jaccard = len(overlap) / len(wa | wb) * 100
    key_overlap = [w for w in overlap if len(w) >= 4]
    if len(key_overlap) >= 2 and jaccard >= 35:
        jaccard = max(jaccard, min(jaccard * 1.3, 70))
    ratio = min(len(wa), len(wb)) / max(len(wa), len(wb))
    if ratio < 0.4:
        jaccard *= 0.6
    elif ratio < 0.6:
        jaccard *= 0.8
    return jaccard


def _fetch_manifold() -> list:
    """Fetch trending Manifold binary markets."""
    global _manifold_cache, _manifold_ts
    now = time.time()
    if _manifold_cache is not None and now - _manifold_ts < 600:
        return _manifold_cache
    results = []
    try:
        r = requests.get(f"{MANIFOLD_URL}/search-markets",
                         params={"sort": "liquidity", "filter": "open",
                                 "contractType": "BINARY", "limit": 200},
                         timeout=15)
        if r.ok:
            for m in r.json():
                prob = m.get("probability")
                if prob is not None:
                    results.append({"title": m.get("question", ""),
                                    "prob": float(prob), "source": "manifold"})
        _manifold_cache = results
        _manifold_ts = now
        log.info("Manifold: %d markets loaded", len(results))
    except Exception as e:
        log.debug("Manifold fetch error: %s", e)
    return _manifold_cache or []


def _fetch_kalshi() -> list:
    """Fetch active Kalshi markets."""
    global _kalshi_cache, _kalshi_ts
    now = time.time()
    if _kalshi_cache is not None and now - _kalshi_ts < 600:
        return _kalshi_cache
    results = []
    try:
        r = requests.get(f"{KALSHI_URL}/markets",
                         params={"status": "open", "limit": 200}, timeout=15)
        if r.ok:
            for m in r.json().get("markets", []):
                yes_price = m.get("yes_ask") or m.get("last_price")
                if yes_price is None:
                    continue
                prob = float(yes_price) / 100.0 if float(yes_price) > 1 else float(yes_price)
                results.append({"title": m.get("title", ""), "prob": prob,
                                "source": "kalshi"})
        _kalshi_cache = results
        _kalshi_ts = now
        log.info("Kalshi: %d markets loaded", len(results))
    except Exception as e:
        log.debug("Kalshi fetch error: %s", e)
        if _kalshi_cache is None:
            _kalshi_cache = []
            _kalshi_ts = now
    return _kalshi_cache or []


def _get_cross_platform_prices(question: str) -> dict:
    """Find matching prices on Manifold and Kalshi via fuzzy title match."""
    xplat = {}
    for name, fetcher in [("manifold", _fetch_manifold), ("kalshi", _fetch_kalshi)]:
        try:
            markets = fetcher()
            best_score = 0
            best = None
            for m in markets:
                score = _word_overlap(question, m["title"])
                if score > best_score and score >= 55:
                    best_score = score
                    best = m
            if best:
                xplat[name] = best["prob"]
        except Exception:
            pass
    return xplat


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: LLM probability estimation
# ═══════════════════════════════════════════════════════════════════════════
_llm_cache = {}
_LLM_CACHE_TTL = int(os.environ.get("LLM_CACHE_TTL", "1800"))  # 30 min
_llm_calls_this_cycle = 0
_LLM_MAX_CALLS = int(os.environ.get("LLM_MAX_CALLS", "50"))


def _estimate_with_llm(question: str, market_price: float,
                       category: str, xplat: dict) -> dict:
    """
    Ask the LLM to estimate true probability. Returns dict with
    estimated_prob, confidence, reasoning or None on failure.
    """
    global _llm_calls_this_cycle

    if _llm_calls_this_cycle >= _LLM_MAX_CALLS:
        log.warning("LLM call limit reached (%d), skipping", _LLM_MAX_CALLS)
        return None

    # Cache check
    cache_key = hashlib.md5(question.encode()).hexdigest()
    now = time.time()
    if cache_key in _llm_cache and now - _llm_cache[cache_key]["ts"] < _LLM_CACHE_TTL:
        cached = _llm_cache[cache_key]["result"]
        log.info("LLM cache hit: '%s...' -> %.0f%%",
                 question[:50], cached["estimated_prob"] * 100)
        return cached

    # LLM config
    api_url = os.environ.get("LLM_API_URL",
                             "https://openrouter.ai/api/v1/chat/completions")
    model = os.environ.get("LLM_MODEL", "xiaomi/mimo-v2-flash:free")
    api_key = os.environ.get("LLM_API_KEY", "")
    if not api_key:
        log.warning("No LLM_API_KEY set, skipping LLM estimate")
        return None

    # Build cross-platform context string
    xplat_str = ""
    if xplat:
        lines = [f"  {p.title()}: {prob:.0%}" for p, prob in xplat.items()]
        xplat_str = ("\n\nOther prediction market prices:\n" + "\n".join(lines)
                     + "\n(Real prices from other platforms - strong signal)")

    # Fetch real-time context
    context_str = ""
    try:
        raw = fetch_context(question, category, market_price)
        if raw:
            context_str = f"\n\nREAL-TIME CONTEXT:\n{raw}"
            log.info("Context enriched: %d chars", len(raw))
    except Exception as e:
        log.debug("Context enrichment failed: %s", e)

    prompt = f"""You are a calibrated prediction market analyst. Estimate the TRUE probability that the following event resolves YES.

Question: {question}
Current market price: {market_price:.2%}
Category: {category}{xplat_str}{context_str}

CALIBRATION RULES:
- 50% means genuinely 50/50, NOT "I don't know"
- Use the full range from 1% to 99%
- Consider base rates, current evidence, and time horizon
- Weight real-time context heavily - it has current news, economic data, odds
- Your estimate should be independent of market price
- If you truly have no info, stay close to the market price with low confidence

Respond with ONLY a JSON object (no markdown, no code blocks):
{{"probability": <float 0.01-0.99>, "confidence": "<low|medium|high>", "reasoning": "<1-2 sentences>"}}"""

    try:
        _llm_calls_this_cycle += 1
        resp = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json",
                     "HTTP-Referer": "https://simmer.markets"},
            json={"model": model, "max_tokens": 500,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=60,
        )
        if not resp.ok:
            log.error("LLM API error: %d %s", resp.status_code, resp.text[:200])
            return None

        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        text_clean = text.strip()
        if text_clean.startswith("```"):
            text_clean = re.sub(r"^```(?:json)?\s*", "", text_clean)
            text_clean = re.sub(r"\s*```$", "", text_clean)

        parsed = json.loads(text_clean)
        prob = max(0.01, min(0.99, float(parsed["probability"])))
        confidence = parsed.get("confidence", "medium")
        reasoning = parsed.get("reasoning", "")

        result = {
            "estimated_prob": round(prob, 4),
            "confidence": {"low": 0.3, "medium": 0.5, "high": 0.7}.get(confidence, 0.4),
            "reasoning": reasoning,
        }
        _llm_cache[cache_key] = {"result": result, "ts": now}
        log.info("LLM estimate: '%s...' -> %.0f%% (%s)",
                 question[:50], prob * 100, confidence)
        return result

    except json.JSONDecodeError as e:
        log.error("LLM response parse error: %s", e)
        return None
    except Exception as e:
        log.error("LLM call failed: %s", e)
        return None


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8: Main trading loop
# ═══════════════════════════════════════════════════════════════════════════

def run(live: bool = False, max_markets: int = 100):
    """
    Main execution loop:
    1. Fetch active markets from Simmer
    2. For each market, get LLM estimate enriched with real-time context
    3. Trade if the estimate diverges from market price beyond threshold
    """
    global _llm_calls_this_cycle
    _llm_calls_this_cycle = 0

    threshold = float(os.environ.get("ESTIMATOR_THRESHOLD", "0.15"))
    log.info("Starting %s | threshold=%.0f%% | max_markets=%d | live=%s",
             SKILL_SLUG, threshold * 100, max_markets, live)

    # Initialize client
    try:
        client = get_client()
    except Exception as e:
        log.error("Failed to create Simmer client: %s", e)
        return

    # Fetch active markets
    try:
        markets = client.get_markets(limit=max_markets, status="active")
    except Exception as e:
        log.error("Failed to fetch markets: %s", e)
        return

    if not markets:
        log.info("No active markets found")
        return

    log.info("Fetched %d active markets", len(markets))
    trades_placed = 0

    for market in markets:
        question = market.question or ""
        if not question:
            continue

        # Get current market price
        price = market.current_probability
        if price is None:
            continue
        price = float(price)
        if price <= 0.01 or price >= 0.99:
            continue  # Skip extreme markets

        # Detect category
        categories = detect_categories(question)
        category = categories[0] if categories else "other"

        # Get cross-platform prices
        xplat = _get_cross_platform_prices(question)

        # Get LLM estimate
        estimate = _estimate_with_llm(question, price, category, xplat)
        if not estimate:
            continue

        est_prob = estimate["estimated_prob"]
        divergence = est_prob - price

        # Check if divergence exceeds threshold
        if abs(divergence) < threshold:
            log.debug("Below threshold: '%s...' est=%.0f%% mkt=%.0f%% div=%.0f%%",
                      question[:40], est_prob * 100, price * 100, divergence * 100)
            continue

        # Determine trade direction
        side = "YES" if divergence > 0 else "NO"
        log.info("SIGNAL: '%s...' | est=%.0f%% mkt=%.0f%% | %s (div=%.0f%%)",
                 question[:50], est_prob * 100, price * 100, side,
                 abs(divergence) * 100)

        if not live:
            log.info("DRY-RUN: would trade %s on '%s...'", side, question[:50])
            continue

        # Context check before trading (flip-flop, slippage)
        market_id = market.id
        try:
            ctx = client.get_market_context(market_id, my_probability=est_prob)
            trading = ctx.get("trading", {})
            flip_flop = trading.get("flip_flop_warning")
            if flip_flop and "SEVERE" in flip_flop:
                log.warning("Skipping '%s...': %s", question[:50], flip_flop)
                continue
            slippage = ctx.get("slippage", {})
            if slippage.get("slippage_pct", 0) > 0.15:
                log.warning("Skipping '%s...': slippage too high", question[:50])
                continue
        except Exception as e:
            log.debug("Context check failed (non-blocking): %s", e)

        # Place trade
        try:
            amount = float(os.environ.get("TRADE_SIZE", "10.0"))
            result = client.trade(
                market_id=market_id,
                side=side.lower(),
                amount=amount,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=f"LLM estimate {est_prob:.0%} vs market {price:.0%} "
                          f"(divergence {abs(divergence):.0%}). {reasoning}",
            )
            trades_placed += 1
            log.info("TRADE PLACED: %s on '%s...' | result=%s",
                     side, question[:50], result)
        except Exception as e:
            log.error("Trade failed for '%s...': %s", question[:50], e)

    log.info("Run complete: %d markets scanned, %d trades placed, %d LLM calls",
             len(markets), trades_placed, _llm_calls_this_cycle)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 9: CLI entrypoint
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Source LLM Estimator for prediction markets")
    parser.add_argument("--live", action="store_true",
                        help="Enable live trading (default: dry-run)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress info logs (errors only)")
    parser.add_argument("--max-markets", type=int, default=100,
                        help="Maximum markets to scan (default: 100)")
    args = parser.parse_args()

    # Configure logging
    level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format=f"%(asctime)s [{SKILL_SLUG}] %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        run(live=args.live, max_markets=args.max_markets)
    except KeyboardInterrupt:
        log.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        log.error("Fatal error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

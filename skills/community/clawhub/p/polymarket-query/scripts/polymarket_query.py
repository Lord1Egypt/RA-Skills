#!/usr/bin/env python3
"""
Polymarket Real-time Query Tool
Query markets, events, odds, and live data from Polymarket's public APIs.

Usage:
  python polymarket_query.py <command> [options]

Commands:
  categories                          List all market categories
  trending [--limit N]                Show trending/active markets (default N=10)
  search <keyword> [--limit N]        Search markets by keyword
  event <event_id>                    Get event details with all sub-markets
  market <market_id>                  Get detailed market info including odds
  sports [--limit N]                  Show sports markets
  politics [--limit N]                Show politics markets
  crypto [--limit N]                  Show crypto markets
  category <slug> [--limit N]         Show markets in a specific category
  odds <market_id>                    Get current odds/prices for a market
  live                                Show currently live/in-play markets
  schedule [--sport X] [--date YYYY-MM-DD]  Show sports schedule by sport & date

Examples:
  python polymarket_query.py schedule --sport nba --date 2026-04-12
  python polymarket_query.py schedule --sport soccer --date 2026-04-11
  python polymarket_query.py search Bitcoin
  python polymarket_query.py market 540816
"""

import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
from datetime import datetime

# API Base URLs
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

# SSL context — secure, requires valid CA bundle
def _make_ssl_context():
    ctx = ssl.create_default_context()
    # Try certifi first (most reliable cross-platform CA bundle)
    try:
        import certifi
        ctx.load_verify_locations(certifi.where())
        return ctx
    except ImportError:
        pass
    # On Windows, try loading system cert store
    try:
        ctx.load_default_certs()
        return ctx
    except Exception:
        pass
    # Try creating a fresh context with default certs
    try:
        ctx2 = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx2.load_default_certs()
        return ctx2
    except Exception:
        pass
    # No CA bundle available — refuse to connect insecurely
    sys.exit(
        "ERROR: No SSL CA bundle found. Install certifi for secure connections:\n"
        "  pip install certifi"
    )

ctx = _make_ssl_context()

# Sport name to Polymarket slug prefix mapping
# Values can be a single prefix string or a list of prefixes to search.
# Game events use short prefixes (e.g. "lal", "epl"), while season/award
# events may use longer prefixes (e.g. "la-liga", "english-premier-league").
SPORT_MAP = {
    "nba": "nba", "basketball": "nba",
    "nfl": "nfl", "football": "nfl",
    "mlb": "mlb", "baseball": "mlb",
    "nhl": "nhl", "hockey": "nhl",
    "soccer": ["epl", "lal", "serie", "bundes", "ligue"], "epl": "epl", "premierleague": ["epl", "english-premier-league"],
    "laliga": ["lal", "la-liga"], "ligue1": ["ligue-1", "l1"], "seriea": ["serie", "serie-a"], "bundesliga": ["bundes", "bundesliga"],
    "ucl": "ucl", "championsleague": "ucl",
    "mls": "mls", "atp": "atp", "tennis": "atp", "wta": "wta",
    "ufc": "ufc", "mma": "ufc",
    "cs2": "cs2", "csgo": "cs2", "counterstrike": "cs2",
    "lol": "lol", "leagueoflegends": "lol",
    "f1": "f1", "racing": "f1",
    "pga": "pga", "golf": "pga",
    "boxing": "boxing", "cricket": "cricket",
}


def fetch(url, timeout=25):
    """Fetch JSON from a URL."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def format_price(price_str):
    """Convert price (0-1) to percentage odds."""
    try:
        p = float(price_str)
        return f"{p*100:.1f}%"
    except:
        return price_str


def format_volume(vol):
    """Format volume with appropriate units."""
    try:
        v = float(vol)
        if v >= 1_000_000:
            return f"${v/1_000_000:.2f}M"
        elif v >= 1_000:
            return f"${v/1_000:.1f}K"
        else:
            return f"${v:.2f}"
    except:
        return vol


def cmd_categories():
    """List all categories."""
    data = fetch(f"{GAMMA_API}/categories?limit=100")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    parents = {}
    children = {}
    for cat in data:
        pc = cat.get("parentCategory")
        if not pc:
            parents[cat["id"]] = cat
        else:
            if pc not in children:
                children[pc] = []
            children[pc].append(cat)

    print("=" * 60)
    print("POLYMARKET CATEGORIES")
    print("=" * 60)
    for pid, parent in sorted(parents.items(), key=lambda x: x[1].get("label", "")):
        print(f"\n  {parent['label']} (slug: {parent['slug']})")
        if pid in children:
            for child in sorted(children[pid], key=lambda x: x.get("label", "")):
                print(f"    -> {child['label']} (slug: {child['slug']})")


def cmd_trending(limit=10):
    """Show trending markets by 24h volume."""
    data = fetch(f"{GAMMA_API}/markets?limit={limit}&active=true&closed=false&order=volume24hr&ascending=false")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    print("=" * 80)
    print(f"TRENDING MARKETS (Top {limit} by 24h Volume)")
    print("=" * 80)
    for i, m in enumerate(data, 1):
        print(f"\n{i}. {m.get('question', 'N/A')}")
        print(f"   ID: {m.get('id', 'N/A')}")

        outcomes = json.loads(m.get("outcomes", "[]"))
        prices = json.loads(m.get("outcomePrices", "[]"))

        if outcomes and prices:
            for outcome, price in zip(outcomes, prices):
                print(f"   {outcome}: {format_price(price)}")

        vol24 = m.get("volume24hr", 0)
        vol_total = m.get("volumeNum", 0)
        liq = m.get("liquidityNum", 0)
        print(f"   Vol 24h: {format_volume(vol24)} | Total Vol: {format_volume(vol_total)} | Liquidity: {format_volume(liq)}")

        end = m.get("endDateIso", m.get("endDate", "N/A"))
        print(f"   End Date: {end}")
        print(f"   URL: https://polymarket.com/event/{m.get('slug', '')}")


def cmd_search(keyword, limit=10):
    """Search markets by keyword."""
    # Fetch active markets and filter
    data = fetch(f"{GAMMA_API}/markets?limit=100&active=true&closed=false&order=volume24hr&ascending=false")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    keyword_lower = keyword.lower()
    filtered = []
    for m in data:
        q = (m.get("question") or "").lower()
        d = (m.get("description") or "").lower()
        if keyword_lower in q or keyword_lower in d:
            filtered.append(m)
            if len(filtered) >= limit:
                break

    if not filtered:
        print(f"No markets found for '{keyword}'")
        return

    print("=" * 80)
    print(f"SEARCH RESULTS: '{keyword}' ({len(filtered)} results)")
    print("=" * 80)
    for i, m in enumerate(filtered, 1):
        print(f"\n{i}. {m.get('question', 'N/A')}")
        print(f"   ID: {m.get('id', 'N/A')}")

        outcomes = json.loads(m.get("outcomes", "[]"))
        prices = json.loads(m.get("outcomePrices", "[]"))

        if outcomes and prices:
            for outcome, price in zip(outcomes, prices):
                print(f"   {outcome}: {format_price(price)}")

        vol24 = m.get("volume24hr", 0)
        vol_total = m.get("volumeNum", 0)
        print(f"   Vol 24h: {format_volume(vol24)} | Total Vol: {format_volume(vol_total)}")
        end = m.get("endDateIso", m.get("endDate", "N/A"))
        print(f"   End Date: {end}")


def cmd_market(market_id):
    """Get detailed market info."""
    data = fetch(f"{GAMMA_API}/markets/{urllib.parse.quote(str(market_id), safe='')}")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    m = data
    print("=" * 80)
    print(f"MARKET DETAILS")
    print("=" * 80)
    print(f"Question: {m.get('question', 'N/A')}")
    print(f"ID: {m.get('id', 'N/A')}")
    print(f"Slug: {m.get('slug', 'N/A')}")

    print(f"\nDescription:")
    desc = m.get("description", "N/A")
    if len(desc) > 500:
        desc = desc[:500] + "..."
    print(f"  {desc}")

    print(f"\nODDS / PRICES:")
    outcomes = json.loads(m.get("outcomes", "[]"))
    prices = json.loads(m.get("outcomePrices", "[]"))

    if outcomes and prices:
        for outcome, price in zip(outcomes, prices):
            p = float(price)
            print(f"  {outcome}: {format_price(price)} (implied odds: {1/p:.1f}x)" if p > 0 else f"  {outcome}: {format_price(price)}")

    print(f"\nPRICE CHANGES:")
    print(f"  1 Day:  {m.get('oneDayPriceChange', 'N/A')}")
    print(f"  1 Week: {m.get('oneWeekPriceChange', 'N/A')}")
    print(f"  1 Month: {m.get('oneMonthPriceChange', 'N/A')}")

    print(f"\nVOLUME & LIQUIDITY:")
    print(f"  24h Volume: {format_volume(m.get('volume24hr', 0))}")
    print(f"  1wk Volume: {format_volume(m.get('volume1wk', 0))}")
    print(f"  Total Volume: {format_volume(m.get('volumeNum', 0))}")
    print(f"  Liquidity: {format_volume(m.get('liquidityNum', 0))}")
    print(f"  Open Interest: {format_volume(m.get('openInterest', 0))}")

    print(f"\nDATES:")
    print(f"  Start: {m.get('startDateIso', m.get('startDate', 'N/A'))}")
    print(f"  End: {m.get('endDateIso', m.get('endDate', 'N/A'))}")

    print(f"\nSTATUS:")
    print(f"  Active: {m.get('active', 'N/A')}")
    print(f"  Closed: {m.get('closed', 'N/A')}")
    print(f"  Accepting Orders: {m.get('acceptingOrders', 'N/A')}")

    if m.get("gameStartTime"):
        print(f"  Game Start: {m.get('gameStartTime')}")

    print(f"\nURL: https://polymarket.com/event/{m.get('slug', '')}")


def cmd_event(event_id):
    """Get event details with all sub-markets."""
    data = fetch(f"{GAMMA_API}/events/{urllib.parse.quote(str(event_id), safe='')}")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    e = data
    print("=" * 80)
    print(f"EVENT: {e.get('title', 'N/A')}")
    print("=" * 80)
    print(f"ID: {e.get('id', 'N/A')}")
    print(f"Slug: {e.get('slug', 'N/A')}")

    desc = e.get("description", "N/A")
    if len(desc) > 300:
        desc = desc[:300] + "..."
    print(f"Description: {desc}")

    print(f"\nVolume: {format_volume(e.get('volume', 0))}")
    print(f"Liquidity: {format_volume(e.get('liquidity', 0))}")
    print(f"Open Interest: {format_volume(e.get('openInterest', 0))}")
    print(f"24h Volume: {format_volume(e.get('volume24hr', 0))}")

    markets = e.get("markets", [])
    if markets:
        print(f"\nSUB-MARKETS ({len(markets)}):")
        print("-" * 80)
        for i, m in enumerate(markets, 1):
            print(f"\n  {i}. {m.get('question', 'N/A')}")
            print(f"     ID: {m.get('id', 'N/A')}")

            outcomes = json.loads(m.get("outcomes", "[]"))
            prices = json.loads(m.get("outcomePrices", "[]"))

            if outcomes and prices:
                for outcome, price in zip(outcomes, prices):
                    print(f"     {outcome}: {format_price(price)}")

            print(f"     Vol: {format_volume(m.get('volume', 0))} | Closed: {m.get('closed', 'N/A')}")

    print(f"\nURL: https://polymarket.com/event/{e.get('slug', '')}")


def cmd_category(slug, limit=15):
    """Show markets in a specific category."""
    data = fetch(f"{GAMMA_API}/markets?limit={limit}&active=true&closed=false&order=volume24hr&ascending=false&category={urllib.parse.quote(slug, safe='')}")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    if not data:
        print(f"No active markets found in category '{slug}'")
        return

    print("=" * 80)
    print(f"CATEGORY: {slug.upper()} ({len(data)} markets)")
    print("=" * 80)
    for i, m in enumerate(data, 1):
        print(f"\n{i}. {m.get('question', 'N/A')}")
        print(f"   ID: {m.get('id', 'N/A')}")

        outcomes = json.loads(m.get("outcomes", "[]"))
        prices = json.loads(m.get("outcomePrices", "[]"))

        if outcomes and prices:
            for outcome, price in zip(outcomes, prices):
                print(f"   {outcome}: {format_price(price)}")

        vol24 = m.get("volume24hr", 0)
        print(f"   Vol 24h: {format_volume(vol24)} | End: {m.get('endDateIso', 'N/A')}")


def cmd_sports(limit=15):
    cmd_category("sports", limit)


def cmd_politics(limit=15):
    cmd_category("politics", limit)


def cmd_crypto(limit=15):
    cmd_category("crypto", limit)


def cmd_odds(market_id):
    """Get current odds for a specific market."""
    data = fetch(f"{GAMMA_API}/markets/{urllib.parse.quote(str(market_id), safe='')}")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    m = data
    print("=" * 60)
    print(f"ODDS: {m.get('question', 'N/A')}")
    print("=" * 60)

    outcomes = json.loads(m.get("outcomes", "[]"))
    prices = json.loads(m.get("outcomePrices", "[]"))

    if outcomes and prices:
        print(f"\n{'Outcome':<20} {'Price':>10} {'Odds':>10}")
        print("-" * 45)
        for outcome, price in zip(outcomes, prices):
            p = float(price)
            implied = f"{1/p:.1f}x" if p > 0 else "N/A"
            print(f"{outcome:<20} {format_price(price):>10} {implied:>10}")

    if m.get("lastTradePrice") is not None:
        print(f"\nLast Trade Price: {format_price(str(m['lastTradePrice']))}")

    if m.get("bestBid") is not None:
        print(f"Best Bid: {format_price(str(m['bestBid']))}")
    if m.get("bestAsk") is not None:
        print(f"Best Ask: {format_price(str(m['bestAsk']))}")

    if m.get("spread") is not None:
        print(f"Spread: {float(m['spread'])*100:.2f}%")

    print(f"\nPrice Changes:")
    for key, label in [("oneDayPriceChange", "1D"), ("oneWeekPriceChange", "1W"), ("oneMonthPriceChange", "1M")]:
        val = m.get(key)
        if val is not None:
            vd = float(val)
            arrow = "+" if vd > 0 else "-" if vd < 0 else "="
            print(f"  {label}: [{arrow}] {vd*100:+.2f}%")


def cmd_live(limit=20):
    """Show currently live/in-play markets."""
    data = fetch(f"{GAMMA_API}/markets?limit={limit}&active=true&closed=false&order=volume24hr&ascending=false&category=sports")
    if isinstance(data, dict) and "error" in data:
        print(f"Error: {data['error']}")
        return

    now = datetime.utcnow()
    live_markets = []

    for m in data:
        game_start = m.get("gameStartTime")
        if game_start:
            try:
                gs = datetime.strptime(game_start.replace("+00", "").replace("+0000", ""), "%Y-%m-%d %H:%M:%S")
                diff = (now - gs).total_seconds()
                if -3600 < diff < 10800:
                    live_markets.append((m, gs, diff))
            except:
                pass

    if not live_markets:
        print("No live/in-play markets found at the moment.")
        print("Showing upcoming sports markets instead:")
        cmd_category("sports", limit)
        return

    print("=" * 80)
    print(f"LIVE / IN-PLAY MARKETS ({len(live_markets)} found)")
    print("=" * 80)
    for i, (m, gs, diff) in enumerate(live_markets, 1):
        status = "LIVE" if diff > 0 else "STARTING SOON"
        print(f"\n{i}. [{status}] {m.get('question', 'N/A')}")
        print(f"   ID: {m.get('id', 'N/A')}")
        print(f"   Game Start: {m.get('gameStartTime')}")

        outcomes = json.loads(m.get("outcomes", "[]"))
        prices = json.loads(m.get("outcomePrices", "[]"))

        if outcomes and prices:
            for outcome, price in zip(outcomes, prices):
                print(f"   {outcome}: {format_price(price)}")

        vol24 = m.get("volume24hr", 0)
        print(f"   Vol 24h: {format_volume(vol24)}")


def _fetch_events_by_slug_prefix(slug_prefix, date_filter=None, max_pages=10):
    """Fetch events filtered by slug prefix.
    
    The Polymarket Gamma API's tag/search/filter parameters are unreliable.
    The only reliable approach is to fetch events sorted by volume and filter
    by slug prefix client-side. Sport game events (nba-, nfl-, etc.) typically
    appear in the top 500 events by volume.
    """
    import time
    events = []
    seen_slugs = set()

    # Primary strategy: iterate /events by volume, filter by slug prefix
    # This is the only method that reliably finds sport game events
    offset = 0
    consecutive_empty_pages = 0
    while offset < max_pages * 100:
        url = f"{GAMMA_API}/events?limit=100&active=true&closed=false&order=volume24hr&ascending=false&offset={offset}"
        batch = fetch(url)
        if not batch or isinstance(batch, dict) or not isinstance(batch, list):
            # Rate limited or error — wait and retry once
            time.sleep(1)
            batch = fetch(url)
            if not batch or isinstance(batch, dict) or not isinstance(batch, list):
                break
        found_in_batch = 0
        for e in batch:
            slug = e.get("slug", "")
            if slug.startswith(f"{slug_prefix}-") and slug not in seen_slugs:
                seen_slugs.add(slug)
                events.append(e)
                found_in_batch += 1
        if len(batch) < 100:
            break
        # Optimization: if we found matches and next pages are unlikely to have more, stop early
        # Sport events cluster together by volume, so if we found some and then
        # a full page has no matches, we can stop
        if found_in_batch == 0:
            consecutive_empty_pages += 1
            if consecutive_empty_pages >= 3:
                break
        else:
            consecutive_empty_pages = 0
        offset += 100
        # Small delay between pages to avoid rate limiting
        if offset % 300 == 0:
            time.sleep(0.5)

    return events


def _fetch_events_by_slug_prefixes(slug_prefixes, max_pages=10):
    """Fetch events matching ANY of the given slug prefixes in a single API pass.
    
    Much faster than calling _fetch_events_by_slug_prefix per prefix when
    there are multiple prefixes (e.g. soccer → epl, lal, serie, bundes, ligue).
    """
    import time
    events = []
    seen_slugs = set()
    prefix_set = set(slug_prefixes)

    offset = 0
    consecutive_empty_pages = 0
    while offset < max_pages * 100:
        url = f"{GAMMA_API}/events?limit=100&active=true&closed=false&order=volume24hr&ascending=false&offset={offset}"
        batch = fetch(url)
        if not batch or isinstance(batch, dict) or not isinstance(batch, list):
            time.sleep(1)
            batch = fetch(url)
            if not batch or isinstance(batch, dict) or not isinstance(batch, list):
                break
        found_in_batch = 0
        for e in batch:
            slug = e.get("slug", "")
            # Check if slug starts with any of the prefixes (prefix must be followed by "-")
            matched = False
            for pfx in slug_prefixes:
                if slug.startswith(f"{pfx}-") and slug not in seen_slugs:
                    matched = True
                    break
            if matched:
                seen_slugs.add(slug)
                events.append(e)
                found_in_batch += 1
        if len(batch) < 100:
            break
        if found_in_batch == 0:
            consecutive_empty_pages += 1
            if consecutive_empty_pages >= 3:
                break
        else:
            consecutive_empty_pages = 0
        offset += 100
        if offset % 300 == 0:
            time.sleep(0.5)

    return events


def cmd_schedule(sport=None, date_str=None, limit=50):
    """Show sports schedule filtered by sport and/or date."""
    # Resolve sport name to slug prefix(es)
    slug_prefixes = []
    if sport:
        sp = sport.lower().strip()
        val = SPORT_MAP.get(sp, sp)
        if isinstance(val, list):
            slug_prefixes = val
        else:
            slug_prefixes = [val]

    # Normalize date
    date_filter = ""
    if date_str:
        date_filter = date_str.strip().replace("/", "-")

    header = "SPORTS SCHEDULE"
    if sport:
        header += f" - {sport.upper()}"
    if date_filter:
        header += f" - {date_filter}"

    print("=" * 80)
    print(header)
    print("=" * 80)

    # Fetch events
    filtered_events = []

    if slug_prefixes:
        # Fetch events matching ANY of the slug prefixes in a single pass
        raw_events = _fetch_events_by_slug_prefixes(slug_prefixes)

        # Filter by date and normalize event data
        for ev in raw_events:
            slug = ev.get("slug", "").lower()
            title = (ev.get("title") or "").lower()
            end_date = (ev.get("endDate") or ev.get("endDateIso") or "")[:10]
            start_date = (ev.get("startDate") or ev.get("startDateIso") or "")[:10]
            game_time = ev.get("gameStartTime", "")

            # Determine if this is a "game" event (slug contains date like 2026-04-12)
            # vs an "award" event (slug like nba-mvp-694 or la-liga-winner-114)
            # Try matching against any of the slug prefixes
            # Note: team abbreviations may contain digits (e.g. lol-ig1, ucl-liv1, ufc-cur1)
            is_game = False
            for pfx in slug_prefixes:
                if re.match(rf"^{pfx}-[a-z0-9]+-[a-z0-9]+-\d{{4}}-\d{{2}}-\d{{2}}", slug):
                    is_game = True
                    break
            # Special case: boxing/fighting events don't follow the team-date slug pattern;
            # their slugs look like "boxing-fighter1-vs-fighter2" (no date in slug)
            # Treat them as game events regardless of gameStartTime
            if not is_game:
                for pfx in slug_prefixes:
                    if slug.startswith(f"{pfx}-") and "-vs-" in slug:
                        is_game = True
                        break

            date_match = True
            if date_filter:
                if is_game:
                    # For game events: match date in slug, endDate, startDate, or gameStartTime
                    date_match = (date_filter in slug) or (end_date == date_filter) or (start_date == date_filter) or (date_filter in game_time)
                else:
                    # For award/season events: skip when date filter is specified
                    # (schedule command is for game schedules, not awards)
                    date_match = False

            if date_match:
                # Normalize event data
                event_data = {
                    "id": ev.get("id", ""),
                    "title": ev.get("title", ev.get("groupItemTitle", "")) or "N/A",
                    "slug": slug,
                    "gameStartTime": game_time,
                    "endDate": end_date,
                    "startDate": start_date,
                    "volume": float(ev.get("volume", 0) or 0),
                    "volume24hr": float(ev.get("volume24hr", 0) or 0),
                    "openInterest": float(ev.get("openInterest", 0) or 0),
                }

                # Build title from slug if needed
                if event_data["title"] == "N/A" or not event_data["title"]:
                    slug_parts = slug.split("-")
                    if len(slug_parts) >= 3:
                        event_data["title"] = f"{slug_parts[1].upper()} vs {slug_parts[2].upper()}"

                # Get markets/sub-markets for this event
                markets = []
                if ev.get("markets"):
                    # Full event with nested markets from /events
                    markets = ev["markets"]
                else:
                    # Fetch markets for this event
                    event_id = ev.get("id")
                    if event_id:
                        m_url = f"{GAMMA_API}/markets?limit=20&event_id={event_id}"
                        m_data = fetch(m_url)
                        if isinstance(m_data, list):
                            markets = m_data

                event_data["markets"] = markets
                filtered_events.append(event_data)
    else:
        # No sport specified - fetch all sports markets
        all_markets = []
        offset = 0
        while offset < 300:
            url = f"{GAMMA_API}/markets?limit=100&active=true&closed=false&order=volume24hr&ascending=false&tag=sports&offset={offset}"
            batch = fetch(url)
            if not batch or isinstance(batch, dict) or not isinstance(batch, list):
                break
            all_markets.extend(batch)
            if len(batch) < 100:
                break
            offset += 100

        # Group by slug prefix
        events_map = {}
        for m in all_markets:
            slug = m.get("slug", "")
            parts = slug.rsplit("-", 1)
            event_key = parts[0] if len(parts) > 1 else slug
            if event_key not in events_map:
                events_map[event_key] = {
                    "id": m.get("id"),
                    "title": m.get("groupItemTitle") or m.get("question", "N/A"),
                    "slug": event_key,
                    "markets": [],
                    "gameStartTime": m.get("gameStartTime", ""),
                    "endDate": "",
                    "startDate": "",
                    "volume": 0,
                    "volume24hr": 0,
                    "openInterest": 0,
                }
            events_map[event_key]["markets"].append(m)
            try:
                events_map[event_key]["volume"] += float(m.get("volume", 0) or 0)
                events_map[event_key]["volume24hr"] += float(m.get("volume24hr", 0) or 0)
                events_map[event_key]["openInterest"] += float(m.get("openInterest", 0) or 0)
            except:
                pass
            if m.get("gameStartTime"):
                if not events_map[event_key]["gameStartTime"] or m["gameStartTime"] < events_map[event_key]["gameStartTime"]:
                    events_map[event_key]["gameStartTime"] = m["gameStartTime"]
            end_raw = m.get("endDateIso", "") or m.get("endDate", "") or ""
            start_raw = m.get("startDateIso", "") or m.get("startDate", "") or ""
            if end_raw and not events_map[event_key]["endDate"]:
                events_map[event_key]["endDate"] = end_raw[:10]
            if start_raw and not events_map[event_key]["startDate"]:
                events_map[event_key]["startDate"] = start_raw[:10]

        # Filter by date
        for eid, ev in events_map.items():
            slug = (ev.get("slug") or "").lower()
            end_date = (ev.get("endDate") or "")[:10]
            start_date = (ev.get("startDate") or "")[:10]
            date_match = True
            if date_filter:
                date_match = (end_date == date_filter) or (start_date == date_filter) or (date_filter in slug) or (date_filter in (ev.get("gameStartTime") or ""))
            if date_match:
                filtered_events.append(ev)

    if not filtered_events:
        print(f"\nNo events found")
        if sport:
            print(f"  Sport: {sport}")
        if date_filter:
            print(f"  Date: {date_filter}")
        print(f"\nSupported sport keywords:")
        print(f"  nba, nfl, mlb, nhl, soccer/epl, atp/tennis, ufc/mma, cs2, lol, f1, pga/golf, boxing")
        if sport:
            print(f"\nTip: Try without date to see all upcoming {sport.upper()} events")
        return

    # Sort by game start time
    filtered_events.sort(key=lambda e: e.get("gameStartTime") or e.get("startDate") or "zzz")

    print(f"\nFound {len(filtered_events)} event(s):\n")

    for ev in filtered_events:
        print(f"  {ev.get('title', 'N/A')}")
        print(f"  Slug: {ev.get('slug', 'N/A')} | Event ID: {ev.get('id', 'N/A')}")

        if ev.get("gameStartTime"):
            print(f"  Game Time: {ev['gameStartTime']}")

        print(f"  Volume: {format_volume(ev.get('volume', 0))} | 24h Vol: {format_volume(ev.get('volume24hr', 0))} | OI: {format_volume(ev.get('openInterest', 0))}")

        # Show sub-markets with odds
        for m in ev.get("markets", []):
            print(f"\n    [{m.get('question', 'N/A')}]")
            try:
                outcomes = json.loads(m.get("outcomes", "[]"))
                prices = json.loads(m.get("outcomePrices", "[]"))
                for outcome, price in zip(outcomes, prices):
                    print(f"      {outcome}: {format_price(price)}")
            except:
                pass
            if m.get("spread"):
                try:
                    print(f"      Spread: {float(m['spread'])*100:.2f}%")
                except:
                    pass

        print(f"\n  URL: https://polymarket.com/event/{ev.get('slug', '')}")
        print(f"  {'-' * 70}")


def print_usage():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == "categories":
        cmd_categories()
    elif command == "trending":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        cmd_trending(limit)
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: polymarket_query.py search <keyword> [limit]")
            return
        keyword = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        cmd_search(keyword, limit)
    elif command == "event":
        if len(sys.argv) < 3:
            print("Usage: polymarket_query.py event <event_id>")
            return
        cmd_event(sys.argv[2])
    elif command == "market":
        if len(sys.argv) < 3:
            print("Usage: polymarket_query.py market <market_id>")
            return
        cmd_market(sys.argv[2])
    elif command == "odds":
        if len(sys.argv) < 3:
            print("Usage: polymarket_query.py odds <market_id>")
            return
        cmd_odds(sys.argv[2])
    elif command == "sports":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        cmd_sports(limit)
    elif command == "politics":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        cmd_politics(limit)
    elif command == "crypto":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        cmd_crypto(limit)
    elif command == "category":
        if len(sys.argv) < 3:
            print("Usage: polymarket_query.py category <slug> [limit]")
            return
        slug = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        cmd_category(slug, limit)
    elif command == "live":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        cmd_live(limit)
    elif command == "schedule":
        sport = None
        date_str = None
        # Parse --sport and --date args
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--sport" and i + 1 < len(args):
                sport = args[i + 1]
                i += 2
            elif args[i] == "--date" and i + 1 < len(args):
                date_str = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_schedule(sport, date_str)
    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()

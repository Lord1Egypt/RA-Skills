#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
Polymarket prediction market CLI.

Commands:
  trending   - Top markets by 24h volume
  featured   - Featured/curated markets
  search     - Fuzzy search with synonym expansion
  event      - Look up event by slug or URL
  market     - Drill into a specific outcome
  category   - Filter by topic
  watch      - Manage watchlist (add/remove/list)
  alerts     - Cron-friendly alert checker
  calendar   - Markets resolving soon
  movers     - Biggest price movers
  digest     - Category digest summary
  portfolio  - Paper trading portfolio
  buy        - Simulate buying a position
  sell       - Simulate selling a position
  reset      - Reset paper portfolio to default cash
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "https://gamma-api.polymarket.com"
DATA_DIR = Path.home() / ".polymarket"
DEFAULT_CASH = 10_000.0
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.25  # seconds between API calls in bulk operations

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("polymarket")


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename: str, default=None):
    """Load JSON from data dir. Returns `default` on missing file or parse error."""
    path = DATA_DIR / filename
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        log.error("Corrupted data file %s: %s — using default.", filename, exc)
        return default if default is not None else {}
    except OSError as exc:
        log.error("Cannot read %s: %s", filename, exc)
        return default if default is not None else {}


def save_json(filename: str, data) -> None:
    """Atomically save JSON to data dir."""
    ensure_data_dir()
    path = DATA_DIR / filename
    tmp = path.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        tmp.replace(path)
    except OSError as exc:
        log.error("Cannot save %s: %s", filename, exc)
        raise


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

_session = requests.Session()
_session.headers.update({"User-Agent": "polymarket-cli/2.0"})


def fetch(endpoint: str, params: dict | None = None) -> list | dict:
    """Fetch from Gamma API. Raises requests.HTTPError on bad status."""
    url = f"{BASE_URL}{endpoint}"
    resp = _session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_event(slug: str) -> dict | None:
    """Fetch a single event by slug. Returns None if not found."""
    data = fetch("/events", {"slug": slug})
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict) and data:
        return data
    return None


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_price(price) -> str:
    if price is None:
        return "N/A"
    try:
        return f"{float(price) * 100:.1f}%"
    except (ValueError, TypeError):
        return str(price)


def format_volume(volume) -> str:
    if volume is None:
        return "N/A"
    try:
        v = float(volume)
        if v >= 1_000_000:
            return f"${v / 1_000_000:.1f}M"
        if v >= 1_000:
            return f"${v / 1_000:.1f}K"
        return f"${v:.0f}"
    except (ValueError, TypeError):
        return str(volume)


def format_change(change) -> str:
    if change is None:
        return ""
    try:
        c = float(change) * 100
        if c > 0:
            return f"↑{c:.1f}%"
        if c < 0:
            return f"↓{abs(c):.1f}%"
        return "→0%"
    except (ValueError, TypeError):
        return ""


def format_time_remaining(end_date: str | None) -> str:
    if not end_date:
        return ""
    try:
        dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = dt - now
        if delta.days < 0:
            return "Ended"
        if delta.days == 0:
            hours = delta.seconds // 3600
            if hours == 0:
                return f"Ends in {delta.seconds // 60}m"
            return f"Ends in {hours}h"
        if delta.days == 1:
            return "Ends tomorrow"
        if delta.days < 7:
            return f"Ends in {delta.days}d"
        if delta.days < 30:
            return f"Ends in {delta.days // 7}w"
        return dt.strftime("%b %d, %Y")
    except (ValueError, AttributeError):
        return ""


def format_market(market: dict, verbose: bool = False) -> str:
    lines: list[str] = []

    question = market.get("question") or market.get("title", "Unknown")
    lines.append(f"  {question}")

    prices = _parse_prices(market)
    if prices and len(prices) >= 2:
        yes_price = format_price(prices[0])
        no_price = format_price(prices[1])
        day_change = format_change(market.get("oneDayPriceChange"))
        change_str = f" ({day_change})" if day_change else ""
        lines.append(f"    Yes: {yes_price}{change_str} | No: {no_price}")

    bid = market.get("bestBid")
    ask = market.get("bestAsk")
    if bid is not None and ask is not None:
        try:
            spread = float(ask) - float(bid)
            if spread > 0:
                lines.append(
                    f"    Spread: {spread * 100:.1f}% "
                    f"(Bid: {format_price(bid)} / Ask: {format_price(ask)})"
                )
        except (ValueError, TypeError):
            pass

    volume = market.get("volume") or market.get("volumeNum")
    if volume:
        vol_str = f"    Volume: {format_volume(volume)}"
        vol_24h = market.get("volume24hr")
        if vol_24h and float(vol_24h) > 0:
            vol_str += f" (24h: {format_volume(vol_24h)})"
        lines.append(vol_str)

    time_left = format_time_remaining(market.get("endDate") or market.get("endDateIso"))
    if time_left:
        lines.append(f"    ⏰ {time_left}")

    if verbose:
        week_change = format_change(market.get("oneWeekPriceChange"))
        month_change = format_change(market.get("oneMonthPriceChange"))
        if week_change or month_change:
            lines.append(f"    1w: {week_change or 'N/A'} | 1m: {month_change or 'N/A'}")
        liquidity = market.get("liquidityNum") or market.get("liquidity")
        if liquidity:
            lines.append(f"    Liquidity: {format_volume(liquidity)}")

    slug = market.get("slug") or market.get("market_slug")
    if slug:
        lines.append(f"    polymarket.com/event/{slug}")

    return "\n".join(lines)


def format_event(event: dict, show_all_markets: bool = False) -> str:
    lines: list[str] = []

    title = event.get("title", "Unknown Event")
    lines.append(f"[{title}]")

    volume = event.get("volume")
    if volume:
        vol_str = f"  Volume: {format_volume(volume)}"
        vol_24h = event.get("volume24hr")
        if vol_24h and float(vol_24h) > 0:
            vol_str += f" (24h: {format_volume(vol_24h)})"
        lines.append(vol_str)

    time_left = format_time_remaining(event.get("endDate"))
    if time_left:
        lines.append(f"  {time_left}")

    markets = event.get("markets", [])
    if markets:
        active = [
            (m, get_market_price(m))
            for m in markets
            if m.get("active", True) or float(m.get("volumeNum", 0) or 0) > 0
        ]
        active.sort(key=lambda x: x[1], reverse=True)

        display_count = len(active) if show_all_markets else min(10, len(active))
        lines.append(f"  Markets ({len(active)}):")

        for m, price in active[:display_count]:
            name = (m.get("groupItemTitle") or m.get("question", ""))[:50]
            vol = m.get("volumeNum", 0)
            day_change = format_change(m.get("oneDayPriceChange"))
            change_str = f" {day_change}" if day_change else ""
            price_str = format_price(price) if price > 0 else "—"
            lines.append(f"    • {name}: {price_str}{change_str} ({format_volume(vol)})")

        if len(active) > display_count:
            lines.append(f"    ... and {len(active) - display_count} more")

    slug = event.get("slug")
    if slug:
        lines.append(f"  polymarket.com/event/{slug}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_prices(market: dict) -> list[float]:
    """Return list of float prices from a market dict."""
    raw = market.get("outcomePrices")
    if raw is None:
        return []
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return []
    if isinstance(raw, list):
        try:
            return [float(p) for p in raw]
        except (ValueError, TypeError):
            return []
    return []


def get_market_price(market: dict) -> float:
    prices = _parse_prices(market)
    return prices[0] if prices else 0.0


def extract_slug_from_url(url_or_slug: str) -> str:
    if "polymarket.com" in url_or_slug:
        path = urlparse(url_or_slug).path.strip("/")
        return path.replace("event/", "", 1) if path.startswith("event/") else path
    return url_or_slug.strip("/")


def expand_query(query: str) -> list[str]:
    """Return a set of query variations for fuzzy search."""
    query = query.lower().strip()
    expansions: set[str] = {query}

    synonyms: dict[str, list[str]] = {
        "championship": ["champion", "winner", "tournament", "title", "finals"],
        "trade": ["traded", "next team", "destination", "move"],
        "win": ["winner", "won", "wins", "winning"],
        "election": ["president", "presidential", "vote"],
        "fed": ["federal reserve", "interest rate", "fomc"],
        "bitcoin": ["btc", "crypto"],
        "btc": ["bitcoin", "crypto"],
        "ethereum": ["eth", "crypto"],
        "eth": ["ethereum", "crypto"],
    }
    sport_leagues: dict[str, list[str]] = {
        "nba": ["basketball"],
        "nfl": ["football"],
        "mlb": ["baseball"],
        "nhl": ["hockey"],
        "ncaa": ["college", "tournament"],
    }

    for key, values in synonyms.items():
        if key in query:
            expansions.update(values)
            expansions.update(query.replace(key, v) for v in values)

    for league, sports in sport_leagues.items():
        if league in query:
            expansions.update(query.replace(league, s) for s in sports)

    # Only add individual words if they are meaningful (4+ chars) and the
    # query itself is multi-word — avoids noisy single-char fragments.
    words = query.split()
    if len(words) >= 2:
        expansions.update(w for w in words if len(w) >= 4)

    return list(expansions)


def _find_market_in_event(event: dict, outcome: str | None) -> tuple[dict | None, float]:
    """Return (market, price) for the best matching outcome, or first market."""
    markets = event.get("markets", [])
    if not markets:
        return None, 0.0

    if outcome:
        outcome_lower = outcome.lower()
        for m in markets:
            if outcome_lower in m.get("groupItemTitle", "").lower() or \
               outcome_lower in m.get("question", "").lower():
                return m, get_market_price(m)
        return None, 0.0

    # No outcome specified — return first market
    m = markets[0]
    return m, get_market_price(m)


def _find_position(portfolio: dict, slug: str, outcome: str | None) -> dict | None:
    """Find a portfolio position matching slug + outcome exactly."""
    for p in portfolio["positions"]:
        if p["slug"] == slug and p.get("outcome") == outcome:
            return p
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_trending(args):
    data = fetch("/events", {
        "order": "volume24hr",
        "ascending": "false",
        "closed": "false",
        "limit": args.limit,
    })
    print("Trending on Polymarket\n")
    for event in data:
        print(format_event(event))
        print()


def cmd_featured(args):
    data = fetch("/events", {"closed": "false", "featured": "true", "limit": args.limit})
    if not data:
        data = fetch("/events", {
            "order": "volume",
            "ascending": "false",
            "closed": "false",
            "limit": args.limit,
        })
        print("(No featured markets found — showing highest volume)\n")
    else:
        print("Featured Markets\n")
    for event in data:
        print(format_event(event))
        print()


def cmd_search(args):
    queries = expand_query(args.query)

    # Fast path: try exact slug match first
    slug_guess = args.query.lower().replace(" ", "-")
    event = fetch_event(slug_guess)
    if event:
        print(f"Search: '{args.query}'\n")
        print(format_event(event, show_all_markets=args.all))
        return

    # Full scan
    data = fetch("/events", {"closed": "false", "limit": 500})
    matches: list[dict] = []
    seen: set[str] = set()

    for event in data:
        eid = event.get("id") or event.get("slug", "")
        if eid in seen:
            continue

        slug = event.get("slug", "").lower()
        title = event.get("title", "").lower()
        desc = event.get("description", "").lower()

        searchable = f"{slug} {title} {desc}"
        hit = any(q in searchable for q in queries)

        if not hit:
            for m in event.get("markets", []):
                market_text = (
                    m.get("question", "").lower() + " " +
                    m.get("groupItemTitle", "").lower()
                )
                if any(q in market_text for q in queries):
                    hit = True
                    break

        if hit:
            matches.append(event)
            seen.add(eid)

    print(f"Search: '{args.query}' — {len(matches)} result(s)\n")
    if not matches:
        print("No markets found. Try a broader term.")
        return
    for event in matches[: args.limit]:
        print(format_event(event, show_all_markets=args.all))
        print()


def cmd_event(args):
    slug = extract_slug_from_url(args.slug)
    event = fetch_event(slug)

    if not event:
        # Fuzzy fallback
        all_events = fetch("/events", {"closed": "false", "limit": 200})
        slug_lower = slug.lower()
        matches = [e for e in all_events if slug_lower in e.get("slug", "").lower()]
        if not matches:
            print(f"Event not found: {slug}")
            sys.exit(1)
        event = matches[0]

    print(format_event(event, show_all_markets=True))


def cmd_market(args):
    slug = extract_slug_from_url(args.slug)
    event = fetch_event(slug)
    if not event:
        print(f"Event not found: {slug}")
        sys.exit(1)

    markets = event.get("markets", [])
    outcome = args.outcome

    if not outcome:
        print(f"[{event.get('title')}]\n")
        for m in markets:
            print(format_market(m, verbose=True))
            print()
        return

    market, _ = _find_market_in_event(event, outcome)
    if market:
        print(format_market(market, verbose=True))
    else:
        print(f"Outcome '{outcome}' not found.")
        print("\nAvailable outcomes:")
        for m in markets[:20]:
            name = m.get("groupItemTitle") or m.get("question", "")[:50]
            print(f"  • {name}")
        sys.exit(1)


def cmd_category(args):
    category_tags: dict[str, list[str]] = {
        "politics": ["politics", "election", "trump", "biden", "congress"],
        "crypto": ["crypto", "bitcoin", "ethereum", "btc", "eth"],
        "sports": ["sports", "nba", "nfl", "mlb", "soccer"],
        "tech": ["tech", "ai", "apple", "google", "microsoft"],
        "entertainment": ["entertainment", "movie", "oscar", "grammy"],
        "science": ["science", "space", "nasa", "climate"],
        "business": ["business", "fed", "interest", "stock", "market"],
    }
    tags = category_tags.get(args.category.lower(), [args.category.lower()])

    data = fetch("/events", {
        "closed": "false",
        "limit": 100,
        "order": "volume24hr",
        "ascending": "false",
    })

    matches = []
    for event in data:
        title = event.get("title", "").lower()
        event_tags = " ".join(t.get("label", "").lower() for t in event.get("tags", []))
        combined = f"{title} {event_tags}"
        if any(tag in combined for tag in tags):
            matches.append(event)

    print(f"Category: {args.category.title()}\n")
    if not matches:
        print(f"No markets found for '{args.category}'.")
        return
    for event in matches[: args.limit]:
        print(format_event(event))
        print()


# ---- Watchlist ----

def cmd_watch(args):
    watchlist = load_json("watchlist.json", {"markets": []})

    if args.action == "add":
        slug = extract_slug_from_url(args.slug)
        event = fetch_event(slug)
        if not event:
            print(f"Event not found: {slug}")
            sys.exit(1)

        market, price = _find_market_in_event(event, args.outcome)
        market_name = (
            (market.get("groupItemTitle") or market.get("question"))
            if market else event.get("title", slug)
        )

        # Remove any existing entry for this slug+outcome before adding
        watchlist["markets"] = [
            w for w in watchlist["markets"]
            if not (w["slug"] == slug and w.get("outcome") == args.outcome)
        ]

        entry = {
            "slug": slug,
            "outcome": args.outcome,
            "name": market_name,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "added_price": price,
            "alert_at": args.alert_at / 100 if args.alert_at is not None else None,
            "alert_change": args.alert_change / 100 if args.alert_change is not None else None,
        }
        watchlist["markets"].append(entry)
        save_json("watchlist.json", watchlist)

        alert_parts = []
        if args.alert_at is not None:
            alert_parts.append(f"alert at {args.alert_at}%")
        if args.alert_change is not None:
            alert_parts.append(f"alert on ±{args.alert_change}% change")
        alert_str = f" ({', '.join(alert_parts)})" if alert_parts else ""

        print(f"Now watching: {market_name}")
        print(f"  Current: {format_price(price)}{alert_str}")

    elif args.action == "remove":
        slug = extract_slug_from_url(args.slug)
        before = len(watchlist["markets"])
        watchlist["markets"] = [
            w for w in watchlist["markets"]
            if not (w["slug"] == slug and w.get("outcome") == args.outcome)
        ]
        save_json("watchlist.json", watchlist)
        removed = before - len(watchlist["markets"])
        if removed:
            print(f"Removed {removed} entry/entries for {slug}.")
        else:
            print(f"{slug} was not in the watchlist.")

    elif args.action == "list":
        markets = watchlist.get("markets", [])
        if not markets:
            print("Watchlist is empty.")
            print("Add with:  polymarket watch add <slug>")
            return

        print(f"Watchlist ({len(markets)} markets)\n")
        for w in markets:
            try:
                event = fetch_event(w["slug"])
                time.sleep(RATE_LIMIT_DELAY)
                if not event:
                    print(f"• {w['name']}  (event no longer available)")
                    print()
                    continue

                market, current_price = _find_market_in_event(event, w.get("outcome"))
                added_price = w.get("added_price", 0)
                change = current_price - added_price
                change_str = f" ({format_change(change)})" if change != 0 else ""

                print(f"• {w['name']}")
                print(f"  Current: {format_price(current_price)}{change_str}  (added at {format_price(added_price)})")
                if w.get("alert_at") is not None:
                    print(f"  Alert at: {w['alert_at'] * 100:.0f}%")
                if w.get("alert_change") is not None:
                    print(f"  Alert on: ±{w['alert_change'] * 100:.0f}% change")
                print()
            except requests.RequestException as exc:
                log.warning("Could not fetch %s: %s", w["slug"], exc)
                print(f"• {w['name']}  (fetch error)")
                print()


def cmd_alerts(args):
    watchlist = load_json("watchlist.json", {"markets": []})
    markets = watchlist.get("markets", [])

    if not markets:
        if not args.quiet:
            print("No markets in watchlist.")
        return

    triggered: list[dict] = []

    for w in markets:
        try:
            event = fetch_event(w["slug"])
            time.sleep(RATE_LIMIT_DELAY)
            if not event:
                continue

            _, current_price = _find_market_in_event(event, w.get("outcome"))
            added_price = w.get("added_price", 0.0)
            change = current_price - added_price
            reason = ""

            if w.get("alert_at") is not None and current_price >= w["alert_at"]:
                reason = f"reached {format_price(current_price)} (threshold: {w['alert_at'] * 100:.0f}%)"

            if not reason and w.get("alert_change") is not None and added_price > 0:
                pct_change = abs(change) / added_price
                if pct_change >= w["alert_change"]:
                    direction = "up" if change > 0 else "down"
                    reason = (
                        f"moved {direction} {format_change(change)} "
                        f"(threshold: ±{w['alert_change'] * 100:.0f}%)"
                    )

            if reason:
                triggered.append({"name": w["name"], "slug": w["slug"], "reason": reason})

        except requests.RequestException as exc:
            log.warning("Could not fetch %s: %s", w["slug"], exc)

    if triggered:
        print(f"Polymarket Alerts ({len(triggered)})\n")
        for a in triggered:
            print(f"• {a['name']}")
            print(f"  {a['reason']}")
            print(f"  polymarket.com/event/{a['slug']}")
            print()
    elif not args.quiet:
        print("No alerts triggered.")


# ---- Calendar ----

def cmd_calendar(args):
    data = fetch("/events", {
        "closed": "false",
        "limit": 200,
        "order": "endDate",
        "ascending": "true",
    })

    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=args.days)

    upcoming: list[tuple[datetime, dict]] = []
    for event in data:
        end_date = event.get("endDate")
        if not end_date:
            continue
        try:
            dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            if now <= dt <= cutoff:
                upcoming.append((dt, event))
        except ValueError:
            continue

    upcoming.sort(key=lambda x: x[0])

    print(f"Resolving in {args.days} day(s): {len(upcoming)} markets\n")
    if not upcoming:
        print("No markets resolving in this timeframe.")
        return

    current_date = None
    for dt, event in upcoming[: args.limit]:
        date_str = dt.strftime("%a %b %d")
        if date_str != current_date:
            current_date = date_str
            print(f"\n--- {date_str} ---")

        title = event.get("title", "Unknown")[:60]
        vol = format_volume(event.get("volume", 0))
        time_str = dt.strftime("%H:%M UTC")

        markets = event.get("markets", [])
        lead = ""
        if markets:
            top = max(markets, key=get_market_price)
            top_name = (top.get("groupItemTitle", "Yes") or "Yes")[:20]
            top_price = get_market_price(top)
            lead = f"  →  {top_name} {format_price(top_price)}"

        print(f"  {time_str}  {title}{lead}  ({vol})")


# ---- Movers ----

def cmd_movers(args):
    timeframe_key = {"24h": "oneDayPriceChange", "1w": "oneWeekPriceChange", "1m": "oneMonthPriceChange"}
    change_key = timeframe_key.get(args.timeframe, "oneDayPriceChange")
    min_volume = (args.min_volume or 10) * 1_000

    data = fetch("/events", {"closed": "false", "limit": 300})

    movers: list[dict] = []
    for event in data:
        if float(event.get("volume24hr") or 0) < min_volume:
            continue
        for m in event.get("markets", []):
            raw_change = m.get(change_key)
            if raw_change is None:
                continue
            try:
                change_val = float(raw_change)
            except (ValueError, TypeError):
                continue
            if abs(change_val) >= 0.01:
                movers.append({
                    "event": event.get("title", ""),
                    "market": m.get("groupItemTitle") or m.get("question", ""),
                    "change": change_val,
                    "price": get_market_price(m),
                    "volume": float(event.get("volume24hr") or 0),
                    "slug": event.get("slug", ""),
                })

    movers.sort(key=lambda x: abs(x["change"]), reverse=True)

    print(f"Biggest Movers ({args.timeframe})\n")
    if not movers:
        print("No significant movers found.")
        return

    for m in movers[: args.limit]:
        sign = "+" if m["change"] > 0 else ""
        name = (m["market"] or m["event"])[:55]
        print(f"  {'▲' if m['change'] > 0 else '▼'} {name}")
        print(f"    {sign}{m['change'] * 100:.1f}% → Now {format_price(m['price'])}  (24h vol: {format_volume(m['volume'])})")
        print()


# ---- Digest ----

def cmd_digest(args):
    category = args.category.lower()
    category_tags: dict[str, list[str]] = {
        "politics": ["politics", "election", "trump", "biden", "congress", "senate"],
        "crypto": ["crypto", "bitcoin", "ethereum", "btc", "eth", "solana"],
        "sports": ["sports", "nba", "nfl", "mlb", "soccer", "ufc", "ncaa"],
        "tech": ["tech", "ai", "apple", "google", "microsoft", "openai"],
        "business": ["business", "fed", "interest", "stock", "economy", "recession"],
    }
    tags = category_tags.get(category, [category])

    data = fetch("/events", {
        "closed": "false",
        "limit": 200,
        "order": "volume24hr",
        "ascending": "false",
    })

    matches = [
        e for e in data
        if any(tag in (e.get("title", "") + e.get("description", "")).lower() for tag in tags)
    ]

    if not matches:
        print(f"No markets found for '{category}'.")
        return

    total_volume = sum(float(e.get("volume") or 0) for e in matches)
    total_24h = sum(float(e.get("volume24hr") or 0) for e in matches)

    movers: list[dict] = []
    for event in matches:
        for m in event.get("markets", []):
            raw = m.get("oneDayPriceChange")
            if raw is not None:
                try:
                    movers.append({
                        "name": m.get("groupItemTitle") or event.get("title", ""),
                        "change": float(raw),
                        "price": get_market_price(m),
                    })
                except (ValueError, TypeError):
                    pass

    movers.sort(key=lambda x: abs(x["change"]), reverse=True)

    now = datetime.now(timezone.utc)
    week_out = now + timedelta(days=7)
    upcoming: list[tuple[datetime, dict]] = []
    for event in matches:
        end = event.get("endDate")
        if end:
            try:
                dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
                if now <= dt <= week_out:
                    upcoming.append((dt, event))
            except ValueError:
                pass
    upcoming.sort(key=lambda x: x[0])

    print(f"{category.title()} Digest")
    print(f"  {len(matches)} markets  |  Volume: {format_volume(total_volume)}  |  24h: {format_volume(total_24h)}\n")

    if movers:
        print("Biggest Movers (24h):")
        for m in movers[:5]:
            sign = "▲" if m["change"] > 0 else "▼"
            print(f"  {sign} {m['name'][:45]}: {m['change'] * 100:+.1f}%")
        print()

    if upcoming:
        print("Resolving This Week:")
        for dt, event in upcoming[:5]:
            print(f"  {dt.strftime('%a %b %d')}  {event.get('title', '')[:45]}")
        print()

    print("Top by Volume:")
    for event in matches[:5]:
        print(format_event(event))
        print()


# ---- Portfolio ----

def _load_portfolio() -> dict:
    return load_json("portfolio.json", {"positions": [], "history": [], "cash": DEFAULT_CASH})


def cmd_portfolio(args):
    portfolio = _load_portfolio()

    print("Paper Portfolio\n")
    print(f"  Cash: ${portfolio['cash']:,.2f}")

    if not portfolio["positions"]:
        print("\n  No open positions.")
        print("  Buy with:  polymarket buy <slug> <amount>")
        return

    total_value = portfolio["cash"]
    print()

    for pos in portfolio["positions"]:
        try:
            event = fetch_event(pos["slug"])
            time.sleep(RATE_LIMIT_DELAY)
            if not event:
                print(f"  • {pos['name']}  (event not found)")
                continue

            _, current_price = _find_market_in_event(event, pos.get("outcome"))
            shares = pos["shares"]
            cost_basis = pos["cost_basis"]
            current_value = shares * current_price
            pnl = current_value - cost_basis
            pnl_pct = (pnl / cost_basis * 100) if cost_basis > 0 else 0.0
            total_value += current_value

            sign = "+" if pnl >= 0 else ""
            arrow = "▲" if pnl >= 0 else "▼"
            print(f"  {arrow} {pos['name'][:45]}")
            print(
                f"    {shares:.1f} shares @ {format_price(pos['entry_price'])} → {format_price(current_price)}"
            )
            print(f"    Value: ${current_value:,.2f}  |  P&L: {sign}${pnl:,.2f} ({sign}{pnl_pct:.1f}%)")
            print()
        except requests.RequestException as exc:
            log.warning("Could not fetch %s: %s", pos["slug"], exc)
            print(f"  • {pos['name']}  (fetch error)")
            print()

    total_pnl = total_value - DEFAULT_CASH
    sign = "+" if total_pnl >= 0 else ""
    print(f"  Cash: ${portfolio['cash']:,.2f}")
    print(f"  Positions value: ${total_value - portfolio['cash']:,.2f}")
    print(f"  Total: ${total_value:,.2f}  (P&L: {sign}${total_pnl:,.2f})")


def cmd_buy(args):
    portfolio = _load_portfolio()
    slug = extract_slug_from_url(args.slug)
    amount = args.amount

    if amount <= 0:
        print("Amount must be greater than zero.")
        sys.exit(1)

    if amount > portfolio["cash"]:
        print(f"Insufficient cash. Have: ${portfolio['cash']:,.2f}, need: ${amount:,.2f}")
        sys.exit(1)

    event = fetch_event(slug)
    if not event:
        print(f"Event not found: {slug}")
        sys.exit(1)

    market, price = _find_market_in_event(event, args.outcome)

    if args.outcome and market is None:
        print(f"Outcome '{args.outcome}' not found in event.")
        print("Available outcomes:")
        for m in event.get("markets", [])[:20]:
            print(f"  • {m.get('groupItemTitle') or m.get('question', '')[:50]}")
        sys.exit(1)

    if price <= 0:
        print("Could not retrieve a valid price for this market.")
        sys.exit(1)

    market_name = (
        (market.get("groupItemTitle") or market.get("question"))
        if market else event.get("title", slug)
    )
    shares = amount / price

    # Upsert position (average in if existing)
    pos = _find_position(portfolio, slug, args.outcome)
    if pos:
        pos["shares"] += shares
        pos["cost_basis"] += amount
        pos["entry_price"] = pos["cost_basis"] / pos["shares"]
    else:
        portfolio["positions"].append({
            "slug": slug,
            "outcome": args.outcome,
            "name": market_name,
            "shares": shares,
            "entry_price": price,
            "cost_basis": amount,
            "bought_at": datetime.now(timezone.utc).isoformat(),
        })

    portfolio["cash"] -= amount
    portfolio["history"].append({
        "action": "buy",
        "slug": slug,
        "outcome": args.outcome,
        "shares": shares,
        "price": price,
        "amount": amount,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    save_json("portfolio.json", portfolio)

    print(f"Bought {shares:.2f} shares of '{market_name}'")
    print(f"  Price: {format_price(price)}  |  Cost: ${amount:,.2f}")
    print(f"  Cash remaining: ${portfolio['cash']:,.2f}")


def cmd_sell(args):
    portfolio = _load_portfolio()
    slug = extract_slug_from_url(args.slug)

    # Resolve which outcome to sell
    outcome = args.outcome
    pos = _find_position(portfolio, slug, outcome)

    if not pos:
        # List what we actually hold for this slug
        held = [p for p in portfolio["positions"] if p["slug"] == slug]
        if held:
            print(f"No position matching outcome '{outcome}' for {slug}.")
            print("Positions held:")
            for p in held:
                print(f"  • outcome={p.get('outcome')!r}  shares={p['shares']:.2f}")
        else:
            print(f"No positions held for {slug}.")
        sys.exit(1)

    event = fetch_event(slug)
    if not event:
        print(f"Event not found: {slug}")
        sys.exit(1)

    _, price = _find_market_in_event(event, pos.get("outcome"))
    if price <= 0:
        print("Could not retrieve a valid price for this market.")
        sys.exit(1)

    shares = pos["shares"]
    proceeds = shares * price
    pnl = proceeds - pos["cost_basis"]

    portfolio["cash"] += proceeds
    portfolio["positions"] = [
        p for p in portfolio["positions"]
        if not (p["slug"] == slug and p.get("outcome") == outcome)
    ]
    portfolio["history"].append({
        "action": "sell",
        "slug": slug,
        "outcome": outcome,
        "shares": shares,
        "price": price,
        "proceeds": proceeds,
        "pnl": pnl,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    save_json("portfolio.json", portfolio)

    sign = "+" if pnl >= 0 else ""
    arrow = "▲" if pnl >= 0 else "▼"
    print(f"{arrow} Sold {shares:.2f} shares of '{pos['name']}'")
    print(f"  Price: {format_price(price)}  |  Proceeds: ${proceeds:,.2f}")
    print(f"  P&L: {sign}${pnl:,.2f}")
    print(f"  Cash: ${portfolio['cash']:,.2f}")


def cmd_reset(args):
    confirm = input(f"Reset portfolio to ${DEFAULT_CASH:,.0f}? All positions will be lost. [y/N] ")
    if confirm.strip().lower() != "y":
        print("Cancelled.")
        return
    save_json("portfolio.json", {"positions": [], "history": [], "cash": DEFAULT_CASH})
    print(f"Portfolio reset. Starting cash: ${DEFAULT_CASH:,.0f}")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--limit", "-l", type=int, default=5, help="Number of results (default: 5)")
    shared.add_argument("--all", "-a", action="store_true", help="Show all markets in event")

    parser = argparse.ArgumentParser(
        description="Polymarket prediction market CLI",
        parents=[shared],
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("trending", parents=[shared], help="Trending markets by 24h volume")
    sub.add_parser("featured", parents=[shared], help="Featured/curated markets")

    p = sub.add_parser("search", parents=[shared], help="Search markets")
    p.add_argument("query", help="Search query")

    p = sub.add_parser("event", help="Get event by slug or URL")
    p.add_argument("slug", help="Event slug or polymarket.com URL")

    p = sub.add_parser("market", help="Get specific market outcome")
    p.add_argument("slug", help="Event slug or URL")
    p.add_argument("outcome", nargs="?", help="Outcome name (optional)")

    p = sub.add_parser("category", parents=[shared], help="Markets by category")
    p.add_argument("category", help="E.g. politics, crypto, sports, tech, business")

    p = sub.add_parser("watch", help="Manage watchlist")
    p.add_argument("action", choices=["add", "remove", "list"])
    p.add_argument("slug", nargs="?", help="Event slug (required for add/remove)")
    p.add_argument("--outcome", "-o", help="Specific outcome to watch")
    p.add_argument("--alert-at", type=float, metavar="PCT",
                   help="Alert when Yes price reaches PCT%%")
    p.add_argument("--alert-change", type=float, metavar="PCT",
                   help="Alert when price moves ±PCT%% from entry")

    p = sub.add_parser("alerts", help="Check watchlist for triggered alerts (cron-friendly)")
    p.add_argument("--quiet", "-q", action="store_true",
                   help="Suppress output when no alerts triggered")

    p = sub.add_parser("calendar", parents=[shared], help="Markets resolving soon")
    p.add_argument("--days", "-d", type=int, default=7, help="Look-ahead window in days (default: 7)")

    p = sub.add_parser("movers", parents=[shared], help="Biggest price movers")
    p.add_argument("--timeframe", "-t", default="24h", choices=["24h", "1w", "1m"])
    p.add_argument("--min-volume", type=float, default=10, metavar="K",
                   help="Minimum 24h volume in $K (default: 10)")

    p = sub.add_parser("digest", parents=[shared], help="Category digest summary")
    p.add_argument("category", help="E.g. politics, crypto, sports, tech, business")

    sub.add_parser("portfolio", help="Show paper trading portfolio")

    p = sub.add_parser("buy", help="Paper-buy a position")
    p.add_argument("slug", help="Event slug")
    p.add_argument("amount", type=float, help="Dollar amount to invest")
    p.add_argument("--outcome", "-o", help="Specific outcome (required for multi-outcome events)")

    p = sub.add_parser("sell", help="Paper-sell a position")
    p.add_argument("slug", help="Event slug")
    p.add_argument("--outcome", "-o", help="Specific outcome to sell")

    sub.add_parser("reset", help="Reset paper portfolio to starting cash")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "trending": cmd_trending,
        "featured": cmd_featured,
        "search": cmd_search,
        "event": cmd_event,
        "market": cmd_market,
        "category": cmd_category,
        "watch": cmd_watch,
        "alerts": cmd_alerts,
        "calendar": cmd_calendar,
        "movers": cmd_movers,
        "digest": cmd_digest,
        "portfolio": cmd_portfolio,
        "buy": cmd_buy,
        "sell": cmd_sell,
        "reset": cmd_reset,
    }

    try:
        dispatch[args.command](args)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)
    except requests.HTTPError as exc:
        log.error("API error: %s", exc)
        sys.exit(1)
    except requests.RequestException as exc:
        log.error("Network error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()

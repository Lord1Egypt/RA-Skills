#!/usr/bin/env python3
"""
Polymarket Council — CLI for querying and trading on Polymarket prediction markets.

APIs used:
  - Gamma API (https://gamma-api.polymarket.com) — markets, events, search
  - Data API (https://data-api.polymarket.com) — positions, trades, leaderboards
  - CLOB API (https://clob.polymarket.com) — order books, prices, trading
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError, URLError

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
WALLET_PATH = Path.home() / ".config" / "polymarket" / "wallet.json"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PolymarketCouncil/1.0)",
    "Accept": "application/json",
}


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _get(url, headers=None):
    """GET request, returns parsed JSON."""
    h = dict(DEFAULT_HEADERS)
    if headers:
        h.update(headers)
    req = Request(url, headers=h)
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _post(url, data, headers=None):
    """POST JSON request, returns parsed JSON."""
    h = dict(DEFAULT_HEADERS)
    h["Content-Type"] = "application/json"
    if headers:
        h.update(headers)
    payload = json.dumps(data).encode()
    req = Request(url, data=payload, headers=h, method="POST")
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)


# ── Formatting helpers ────────────────────────────────────────────────────────

def fmt_price(p):
    """Format price as percentage odds."""
    try:
        v = float(p)
        return f"{v*100:.1f}%"
    except (ValueError, TypeError):
        return str(p)


def fmt_volume(v):
    """Format volume with comma separators."""
    try:
        return f"${float(v):,.0f}"
    except (ValueError, TypeError):
        return str(v)


def fmt_ts(ts):
    """Format ISO timestamp to readable date."""
    if not ts:
        return "N/A"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return str(ts)


def print_market(m, verbose=False):
    """Print a single market/condition summary."""
    question = m.get("question") or m.get("title") or "Unknown"
    cid = m.get("conditionId") or m.get("condition_id") or ""

    # Extract outcomes and prices
    outcomes = m.get("outcomes", "")
    if isinstance(outcomes, str):
        try:
            outcomes = json.loads(outcomes)
        except Exception:
            outcomes = outcomes.split(",") if outcomes else []

    prices = m.get("outcomePrices") or m.get("outcome_prices") or ""
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except Exception:
            prices = []

    tokens = m.get("clobTokenIds") or m.get("tokens", [])
    if isinstance(tokens, str):
        try:
            tokens = json.loads(tokens)
        except Exception:
            tokens = []

    volume = m.get("volume") or m.get("volumeNum") or 0
    liquidity = m.get("liquidity") or 0
    end_date = m.get("endDate") or m.get("end_date_iso") or ""
    active = m.get("active", True)
    closed = m.get("closed", False)

    status = "CLOSED" if closed else ("ACTIVE" if active else "INACTIVE")

    print(f"\n{'─'*70}")
    print(f"  {question}")
    print(f"  Status: {status}  |  Volume: {fmt_volume(volume)}  |  Liquidity: {fmt_volume(liquidity)}")
    if end_date:
        print(f"  Ends: {fmt_ts(end_date)}")

    if outcomes and prices:
        print(f"  Odds:")
        for i, outcome in enumerate(outcomes):
            price = prices[i] if i < len(prices) else "?"
            token_id = ""
            if isinstance(tokens, list) and i < len(tokens):
                t = tokens[i]
                token_id = t.get("token_id", t) if isinstance(t, dict) else t
            odds = fmt_price(price)
            tid_str = f"  (token: {token_id[:16]}...)" if token_id and len(str(token_id)) > 16 else f"  (token: {token_id})" if token_id else ""
            print(f"    {outcome}: {odds}{tid_str}")
    elif outcomes:
        print(f"  Outcomes: {', '.join(str(o) for o in outcomes)}")

    if cid and verbose:
        print(f"  Condition ID: {cid}")

    slug = m.get("slug") or m.get("market_slug") or ""
    if slug:
        print(f"  URL: https://polymarket.com/event/{slug}")


def print_event(e):
    """Print an event with all its markets."""
    title = e.get("title") or "Unknown Event"
    slug = e.get("slug") or ""
    volume = e.get("volume") or 0
    liquidity = e.get("liquidity") or 0
    end_date = e.get("endDate") or ""

    print(f"\n{'═'*70}")
    print(f"  EVENT: {title}")
    print(f"  Volume: {fmt_volume(volume)}  |  Liquidity: {fmt_volume(liquidity)}")
    if end_date:
        print(f"  Ends: {fmt_ts(end_date)}")
    if slug:
        print(f"  URL: https://polymarket.com/event/{slug}")

    markets = e.get("markets", [])
    if markets:
        print(f"  Markets ({len(markets)}):")
        for m in markets:
            print_market(m, verbose=True)


# ── Market Discovery ─────────────────────────────────────────────────────────

def cmd_trending(args):
    """Show trending markets by volume."""
    limit = args.limit or 20
    params = urlencode({
        "limit": limit,
        "active": "true",
        "closed": "false",
        "order": "volume24hr",
        "ascending": "false",
    })
    data = _get(f"{GAMMA}/markets?{params}")
    markets = data if isinstance(data, list) else data.get("markets", data.get("data", []))
    print(f"📊 Trending Markets (top {limit} by 24h volume):")
    for m in markets[:limit]:
        print_market(m)
    print(f"\n{'─'*70}")
    print(f"Showing {len(markets[:limit])} markets")


def cmd_search(args):
    """Search markets by keyword."""
    query = args.query
    limit = args.limit or 10
    # Use markets endpoint with text_query filter (no auth needed)
    params = urlencode({
        "limit": limit,
        "active": "true",
        "closed": "false",
        "text_query": query,
    })
    data = _get(f"{GAMMA}/markets?{params}")
    results = data if isinstance(data, list) else data.get("markets", data.get("data", []))

    print(f'🔍 Search results for "{query}":')
    if not results:
        print("  No markets found.")
        return
    for m in results[:limit]:
        print_market(m)
    print(f"\n{'─'*70}")
    print(f"Found {len(results[:limit])} markets")


def cmd_category(args):
    """Browse markets by category tag."""
    tag = args.tag
    limit = args.limit or 20
    params = urlencode({
        "limit": limit,
        "active": "true",
        "closed": "false",
        "tag": tag,
        "order": "volume24hr",
        "ascending": "false",
    })
    data = _get(f"{GAMMA}/markets?{params}")
    markets = data if isinstance(data, list) else data.get("markets", data.get("data", []))
    print(f"📁 Markets tagged '{tag}':")
    for m in markets[:limit]:
        print_market(m)
    print(f"\n{'─'*70}")
    print(f"Showing {len(markets[:limit])} markets")


def cmd_events(args):
    """List active events."""
    limit = args.limit or 20
    params = {"limit": limit, "active": "true", "closed": "false", "order": "volume24hr", "ascending": "false"}
    if hasattr(args, "tag") and args.tag:
        params["tag"] = args.tag
    data = _get(f"{GAMMA}/events?{urlencode(params)}")
    events = data if isinstance(data, list) else data.get("events", data.get("data", []))
    print(f"📋 Active Events:")
    for e in events[:limit]:
        title = e.get("title", "Unknown")
        slug = e.get("slug", "")
        volume = e.get("volume", 0)
        n_markets = len(e.get("markets", []))
        print(f"\n  {title}")
        print(f"  Volume: {fmt_volume(volume)}  |  Markets: {n_markets}")
        if slug:
            print(f"  Slug: {slug}")


def cmd_event(args):
    """Get detailed event info by slug or ID."""
    identifier = args.identifier
    # Try by slug first, then by ID
    try:
        data = _get(f"{GAMMA}/events?slug={quote(identifier)}")
        events = data if isinstance(data, list) else data.get("events", data.get("data", []))
        if events:
            print_event(events[0])
            return
    except SystemExit:
        pass
    # Try by ID
    data = _get(f"{GAMMA}/events/{quote(identifier)}")
    if isinstance(data, dict):
        print_event(data)
    else:
        print(f"Event not found: {identifier}")


def cmd_market(args):
    """Get a single market's details by condition ID."""
    cid = args.condition_id
    params = urlencode({"conditionId": cid})
    data = _get(f"{GAMMA}/markets?{params}")
    markets = data if isinstance(data, list) else data.get("markets", data.get("data", []))
    if not markets:
        # Try direct lookup
        data = _get(f"{GAMMA}/markets/{quote(cid)}")
        if isinstance(data, dict):
            print_market(data, verbose=True)
            return
        print(f"Market not found: {cid}")
        return
    print_market(markets[0], verbose=True)


# ── Prices & Order Books ─────────────────────────────────────────────────────

def cmd_price(args):
    """Get midpoint price for a token."""
    token_id = args.token_id
    data = _get(f"{CLOB}/midpoint?token_id={quote(token_id)}")
    mid = data.get("mid", data.get("midpoint", data.get("price", "?")))
    print(f"💰 Midpoint price: {fmt_price(mid)}")
    print(f"   Token: {token_id}")


def cmd_prices(args):
    """Get midpoint prices for multiple tokens."""
    token_ids = args.token_ids
    # Use POST for batch
    data = _post(f"{CLOB}/midpoints", token_ids)
    if isinstance(data, list):
        print("💰 Midpoint prices:")
        for item in data:
            tid = item.get("token_id", "?")
            mid = item.get("mid", item.get("midpoint", "?"))
            print(f"   {tid[:20]}...: {fmt_price(mid)}")
    elif isinstance(data, dict):
        print("💰 Midpoint prices:")
        for tid, mid in data.items():
            print(f"   {tid[:20]}...: {fmt_price(mid)}")


def cmd_spread(args):
    """Get spread for a token."""
    token_id = args.token_id
    data = _get(f"{CLOB}/spread?token_id={quote(token_id)}")
    spread = data.get("spread", "?")
    print(f"📏 Spread: {spread}")
    print(f"   Token: {token_id}")


def cmd_book(args):
    """Get full order book for a token."""
    token_id = args.token_id
    data = _get(f"{CLOB}/book?token_id={quote(token_id)}")

    market = data.get("market", "")
    asset_id = data.get("asset_id", token_id)

    bids = data.get("bids", [])
    asks = data.get("asks", [])
    last = data.get("last_trade_price", "?")

    print(f"📖 Order Book")
    print(f"   Token: {asset_id}")
    if market:
        print(f"   Market: {market}")
    print(f"   Last trade: {fmt_price(last)}")

    print(f"\n   ASKS (sell orders) — {len(asks)} levels:")
    for a in asks[:10]:
        price = a.get("price", "?")
        size = a.get("size", "?")
        print(f"     {fmt_price(price)}  |  Size: {size}")

    print(f"\n   BIDS (buy orders) — {len(bids)} levels:")
    for b in bids[:10]:
        price = b.get("price", "?")
        size = b.get("size", "?")
        print(f"     {fmt_price(price)}  |  Size: {size}")


def cmd_history(args):
    """Get price history for a token."""
    token_id = args.token_id
    interval = args.interval or "1d"
    fidelity = args.fidelity or 60

    params = urlencode({
        "market": token_id,
        "interval": interval,
        "fidelity": fidelity,
    })
    data = _get(f"{CLOB}/prices-history?{params}")

    history = data.get("history", data) if isinstance(data, dict) else data
    if not history:
        print("No price history available.")
        return

    points = history if isinstance(history, list) else []
    print(f"📈 Price History (interval: {interval}, fidelity: {fidelity}min)")
    print(f"   Token: {token_id}")
    print(f"   Data points: {len(points)}")

    if points:
        print(f"\n   {'Time':<22} {'Price':>8}")
        print(f"   {'─'*32}")
        # Show last 20 points
        for p in points[-20:]:
            t = p.get("t", "")
            price = p.get("p", "?")
            ts = ""
            try:
                ts = datetime.fromtimestamp(int(t), tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            except Exception:
                ts = str(t)
            print(f"   {ts:<22} {fmt_price(price):>8}")

        if len(points) > 20:
            print(f"   ... ({len(points) - 20} earlier points omitted)")


def cmd_last_trade(args):
    """Get last trade price for a token."""
    token_id = args.token_id
    data = _get(f"{CLOB}/last-trade-price?token_id={quote(token_id)}")
    price = data.get("price", data.get("last_trade_price", "?"))
    side = data.get("side", "")
    print(f"💱 Last trade: {fmt_price(price)}")
    if side:
        print(f"   Side: {side}")
    print(f"   Token: {token_id}")


# ── Analytics ─────────────────────────────────────────────────────────────────

def cmd_open_interest(args):
    """Get open interest for a market."""
    cid = args.condition_id
    data = _get(f"{DATA}/open-interest?conditionId={quote(cid)}")
    oi = data if isinstance(data, list) else [data]
    print(f"📊 Open Interest")
    for item in oi:
        if isinstance(item, dict):
            for k, v in item.items():
                print(f"   {k}: {v}")
        else:
            print(f"   {item}")


def cmd_holders(args):
    """Get top holders of a token."""
    token_id = args.token_id
    limit = args.limit or 10
    params = urlencode({"limit": limit})
    data = _get(f"{DATA}/positions/top-holders?token_id={quote(token_id)}&{params}")
    holders = data if isinstance(data, list) else data.get("holders", data.get("data", []))
    print(f"👥 Top Holders (token: {token_id[:20]}...)")
    for i, h in enumerate(holders[:limit], 1):
        addr = h.get("address", h.get("user", "?"))
        size = h.get("size", h.get("amount", "?"))
        print(f"   {i}. {addr}  |  Size: {size}")


def cmd_volume(args):
    """Get live volume for an event."""
    event_id = args.event_id
    data = _get(f"{DATA}/volume?eventId={quote(event_id)}")
    print(f"📊 Live Volume for event {event_id}")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"   {k}: {v}")
    else:
        print(f"   {data}")


def cmd_leaderboard(args):
    """Get trader leaderboard."""
    limit = args.limit or 20
    data = _get(f"{DATA}/leaderboard?limit={limit}")
    leaders = data if isinstance(data, list) else data.get("leaderboard", data.get("data", []))
    print(f"🏆 Trader Leaderboard:")
    for i, l in enumerate(leaders[:limit], 1):
        name = l.get("displayName") or l.get("username") or l.get("address", "?")[:12]
        profit = l.get("profit", l.get("pnl", "?"))
        volume = l.get("volume", "?")
        print(f"   {i:>3}. {name:<20}  Profit: {fmt_volume(profit)}  Volume: {fmt_volume(volume)}")


def cmd_profile(args):
    """Get public profile of a trader."""
    address = args.address
    data = _get(f"{GAMMA}/profiles/{quote(address)}")
    if isinstance(data, dict):
        name = data.get("name") or data.get("username") or address
        bio = data.get("bio", "")
        print(f"👤 Profile: {name}")
        print(f"   Address: {address}")
        if bio:
            print(f"   Bio: {bio}")
        for k in ["volume", "positions", "marketsTraded", "profit"]:
            if k in data:
                print(f"   {k}: {data[k]}")


def cmd_activity(args):
    """Get a trader's activity history."""
    address = args.address
    limit = args.limit or 20
    params = urlencode({"limit": limit})
    data = _get(f"{DATA}/activity?address={quote(address)}&{params}")
    activities = data if isinstance(data, list) else data.get("activity", data.get("data", []))
    print(f"📜 Activity for {address}:")
    for a in activities[:limit]:
        action = a.get("type", a.get("action", "?"))
        title = a.get("title", a.get("question", "?"))
        ts = a.get("timestamp", a.get("createdAt", ""))
        amount = a.get("amount", a.get("size", ""))
        line = f"   [{action}] {title}"
        if amount:
            line += f"  |  {amount}"
        if ts:
            line += f"  |  {fmt_ts(ts)}"
        print(line)


# ── Trading ──────────────────────────────────────────────────────────────────

def _load_wallet():
    """Load wallet config."""
    if not WALLET_PATH.exists():
        print("No wallet configured. Run: python3 polymarket.py wallet-setup", file=sys.stderr)
        sys.exit(1)
    with open(WALLET_PATH) as f:
        return json.load(f)


def cmd_wallet_setup(args):
    """Interactive wallet setup."""
    print("🔐 Polymarket Wallet Setup")
    print(f"   Config path: {WALLET_PATH}")
    print()

    if WALLET_PATH.exists():
        print("   Wallet already configured!")
        print("   To reconfigure, delete the existing config first.")
        return

    pk = input("   Enter your Polygon private key (hex): ").strip()
    if not pk:
        print("   Aborted.")
        return

    # Remove 0x prefix if present
    if pk.startswith("0x"):
        pk = pk[2:]

    WALLET_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = {"private_key": pk}
    with open(WALLET_PATH, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(WALLET_PATH, 0o600)

    print(f"   ✅ Wallet saved to {WALLET_PATH}")
    print("   ⚠️  Keep this file secure. Never share your private key.")


def cmd_balance(args):
    """Check wallet balance (placeholder — needs web3)."""
    wallet = _load_wallet()
    print("💼 Wallet Balance")
    print("   Note: Full balance checking requires web3.py.")
    print("   Install it with: pip install web3")
    print(f"   Wallet configured at: {WALLET_PATH}")


def cmd_trade(args):
    """Place a trade order (requires CLOB auth)."""
    confirm = args.confirm
    side = args.side  # buy or sell
    token_id = args.token
    price = args.price
    size = args.size
    amount = getattr(args, "amount", None)
    market_order = getattr(args, "market_order", False)

    if not confirm:
        print("👀 PREVIEW MODE (add --confirm to execute)")
    else:
        print("⚡ LIVE MODE — order will be submitted")

    print(f"\n   Side: {side.upper()}")
    print(f"   Token: {token_id}")
    if market_order and amount:
        print(f"   Type: Market order")
        print(f"   Amount: ${amount}")
    else:
        print(f"   Type: Limit order")
        print(f"   Price: ${price}")
        print(f"   Size: {size}")

    if not confirm:
        print("\n   ℹ️  This is a preview. Add --confirm to execute.")
        return

    # For actual trading, we need CLOB API authentication
    # which requires py-clob-client or manual L1/L2 auth
    print("\n   ⚠️  Trading requires CLOB API authentication.")
    print("   Install py-clob-client: pip install py-clob-client")
    print("   See: https://docs.polymarket.com/api-reference/clob/post-a-new-order")


def cmd_orders(args):
    """View open orders."""
    address = getattr(args, "address", None)
    if not address:
        wallet = _load_wallet()
        print("   Using configured wallet address.")

    print("📋 Open Orders")
    print("   Note: Viewing orders requires CLOB API authentication.")
    print("   See: https://docs.polymarket.com/api-reference/clob/get-user-orders")


def cmd_cancel(args):
    """Cancel an order."""
    order_id = args.order_id
    confirm = args.confirm
    if not confirm:
        print(f"   Would cancel order: {order_id}")
        print("   Add --confirm to execute.")
        return
    print(f"   Cancelling order: {order_id}")
    print("   Note: Cancellation requires CLOB API authentication.")


def cmd_cancel_all(args):
    """Cancel all orders."""
    confirm = args.confirm
    if not confirm:
        print("   Would cancel ALL open orders.")
        print("   Add --confirm to execute.")
        return
    print("   Cancelling all orders...")
    print("   Note: Cancellation requires CLOB API authentication.")


def cmd_positions(args):
    """View positions."""
    address = getattr(args, "address", None)
    if address:
        data = _get(f"{DATA}/positions?address={quote(address)}")
    else:
        print("   Specify an address with --address, or configure a wallet.")
        print("   Example: python3 polymarket.py positions --address 0x...")
        return

    positions = data if isinstance(data, list) else data.get("positions", data.get("data", []))
    print(f"📊 Positions for {address}:")
    if not positions:
        print("   No positions found.")
        return
    for p in positions:
        title = p.get("title", p.get("question", "?"))
        outcome = p.get("outcome", "?")
        size = p.get("size", p.get("amount", "?"))
        value = p.get("currentValue", p.get("value", "?"))
        print(f"\n   {title}")
        print(f"   Outcome: {outcome}  |  Size: {size}  |  Value: {value}")


# ── CLI Parser ────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="polymarket",
        description="Polymarket Council — query and trade prediction markets",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # Market discovery
    p = sub.add_parser("trending", help="Trending markets by volume")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("search", help="Search markets")
    p.add_argument("query", help="Search query")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("category", help="Markets by category tag")
    p.add_argument("tag", help="Category tag (politics, crypto, sports, etc.)")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("events", help="List active events")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--tag", help="Filter by tag")

    p = sub.add_parser("event", help="Event details by slug or ID")
    p.add_argument("identifier", help="Event slug or ID")

    p = sub.add_parser("market", help="Market details by condition ID")
    p.add_argument("condition_id", help="Market condition ID")

    # Prices & books
    p = sub.add_parser("price", help="Midpoint price for a token")
    p.add_argument("token_id", help="CLOB token ID")

    p = sub.add_parser("prices", help="Batch midpoint prices")
    p.add_argument("token_ids", nargs="+", help="CLOB token IDs")

    p = sub.add_parser("spread", help="Spread for a token")
    p.add_argument("token_id", help="CLOB token ID")

    p = sub.add_parser("book", help="Full order book")
    p.add_argument("token_id", help="CLOB token ID")

    p = sub.add_parser("history", help="Price history")
    p.add_argument("token_id", help="CLOB token ID")
    p.add_argument("--interval", default="1d", help="1m, 5m, 1h, 1d, 1w")
    p.add_argument("--fidelity", type=int, default=60, help="Minutes between data points")

    p = sub.add_parser("last-trade", help="Last trade price")
    p.add_argument("token_id", help="CLOB token ID")

    # Analytics
    p = sub.add_parser("open-interest", help="Open interest for a market")
    p.add_argument("condition_id", help="Condition ID")

    p = sub.add_parser("holders", help="Top holders of a token")
    p.add_argument("token_id", help="Token ID")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("volume", help="Live volume for an event")
    p.add_argument("event_id", help="Event ID")

    p = sub.add_parser("leaderboard", help="Trader leaderboard")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("profile", help="Trader profile")
    p.add_argument("address", help="Wallet address")

    p = sub.add_parser("activity", help="Trader activity")
    p.add_argument("address", help="Wallet address")
    p.add_argument("--limit", type=int, default=20)

    # Trading
    sub.add_parser("wallet-setup", help="Configure wallet")

    sub.add_parser("balance", help="Check wallet balance")

    p = sub.add_parser("trade", help="Place a trade")
    p.add_argument("side", choices=["buy", "sell"])
    p.add_argument("--token", required=True, help="Token ID")
    p.add_argument("--price", type=float, help="Limit price")
    p.add_argument("--size", type=float, help="Number of shares")
    p.add_argument("--amount", type=float, help="Dollar amount (market orders)")
    p.add_argument("--market-order", action="store_true")
    p.add_argument("--confirm", action="store_true", help="Execute (not just preview)")

    p = sub.add_parser("orders", help="View open orders")
    p.add_argument("--address", help="Wallet address")

    p = sub.add_parser("cancel", help="Cancel an order")
    p.add_argument("order_id", help="Order ID")
    p.add_argument("--confirm", action="store_true")

    p = sub.add_parser("cancel-all", help="Cancel all orders")
    p.add_argument("--confirm", action="store_true")

    p = sub.add_parser("positions", help="View positions")
    p.add_argument("--address", help="Wallet address")

    return parser


# ── Main ──────────────────────────────────────────────────────────────────────

COMMANDS = {
    "trending": cmd_trending,
    "search": cmd_search,
    "category": cmd_category,
    "events": cmd_events,
    "event": cmd_event,
    "market": cmd_market,
    "price": cmd_price,
    "prices": cmd_prices,
    "spread": cmd_spread,
    "book": cmd_book,
    "history": cmd_history,
    "last-trade": cmd_last_trade,
    "open-interest": cmd_open_interest,
    "holders": cmd_holders,
    "volume": cmd_volume,
    "leaderboard": cmd_leaderboard,
    "profile": cmd_profile,
    "activity": cmd_activity,
    "wallet-setup": cmd_wallet_setup,
    "balance": cmd_balance,
    "trade": cmd_trade,
    "orders": cmd_orders,
    "cancel": cmd_cancel,
    "cancel-all": cmd_cancel_all,
    "positions": cmd_positions,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    fn = COMMANDS.get(args.command)
    if fn:
        fn(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

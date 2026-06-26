"""
polymarket-copy-early-mover-trader
Identifies which whale wallet consistently enters markets FIRST before other
whales follow.  When this early-mover whale opens a fresh position, the skill
copies it before the rest of the herd pushes the price away.

Core edge: The first whale into a market gets the best price.  Followers push
the price in the direction of the trade, creating slippage for latecomers.
By tracking *who* tends to move first -- and confirming that followers actually
pile in afterwards -- this skill isolates the single most predictive "lead
indicator" wallet and copies its freshest entries.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-copy-early-mover-trader"
SKILL_SLUG   = "polymarket-copy-early-mover-trader"

# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# ---------------------------------------------------------------------------
# Risk parameters -- declared as tunables in clawhub.json
# ---------------------------------------------------------------------------
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "40"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "3000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.10"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "5"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "8"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))

# ---------------------------------------------------------------------------
# Skill-specific parameters
# ---------------------------------------------------------------------------
EARLY_WINDOW_HOURS  = int(os.environ.get(  "SIMMER_EARLY_WINDOW_HOURS",  "6"))
MIN_FOLLOWERS       = int(os.environ.get(  "SIMMER_MIN_FOLLOWERS",       "1"))
FRESHNESS_HOURS     = int(os.environ.get(  "SIMMER_FRESHNESS_HOURS",     "48"))
LEADERBOARD_LIMIT   = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",  "15"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Flush-safe print for cron/daemon environments."""
    print(*args, **kwargs, flush=True)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global EARLY_WINDOW_HOURS, MIN_FOLLOWERS, FRESHNESS_HOURS, LEADERBOARD_LIMIT
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        if live:
            _client.live = True
        try:
            _client.apply_skill_config(SKILL_SLUG)
        except (AttributeError, Exception):
            pass  # apply_skill_config only available in Simmer runtime
        MAX_POSITION        = float(os.environ.get("SIMMER_MAX_POSITION",       str(MAX_POSITION)))
        MIN_VOLUME          = float(os.environ.get("SIMMER_MIN_VOLUME",         str(MIN_VOLUME)))
        MAX_SPREAD          = float(os.environ.get("SIMMER_MAX_SPREAD",         str(MAX_SPREAD)))
        MIN_DAYS            = int(os.environ.get(  "SIMMER_MIN_DAYS",           str(MIN_DAYS)))
        MAX_POSITIONS       = int(os.environ.get(  "SIMMER_MAX_POSITIONS",      str(MAX_POSITIONS)))
        YES_THRESHOLD       = float(os.environ.get("SIMMER_YES_THRESHOLD",      str(YES_THRESHOLD)))
        NO_THRESHOLD        = float(os.environ.get("SIMMER_NO_THRESHOLD",       str(NO_THRESHOLD)))
        MIN_TRADE           = float(os.environ.get("SIMMER_MIN_TRADE",          str(MIN_TRADE)))
        EARLY_WINDOW_HOURS  = int(os.environ.get(  "SIMMER_EARLY_WINDOW_HOURS", str(EARLY_WINDOW_HOURS)))
        MIN_FOLLOWERS       = int(os.environ.get(  "SIMMER_MIN_FOLLOWERS",      str(MIN_FOLLOWERS)))
        FRESHNESS_HOURS     = int(os.environ.get(  "SIMMER_FRESHNESS_HOURS",    str(FRESHNESS_HOURS)))
        LEADERBOARD_LIMIT   = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT", str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: int = 15) -> dict | list | None:
    """Simple stdlib JSON GET request."""
    try:
        req = Request(url, headers={"User-Agent": "simmer-early-mover/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as exc:
        safe_print(f"  [WARN] HTTP GET failed: {url} -> {exc}")
        return None


# ---------------------------------------------------------------------------
# Leaderboard fetching
# ---------------------------------------------------------------------------

def fetch_leaderboard(limit: int = 15) -> list[dict]:
    """Fetch top traders from predicting.top leaderboard API."""
    url = f"{LEADERBOARD_URL}?limit={limit}"
    data = _http_get_json(url)
    if data is None:
        safe_print("  [WARN] Leaderboard fetch returned None, using empty list")
        return []
    if isinstance(data, dict):
        traders = data.get("traders", data.get("data", data.get("results", [])))
    elif isinstance(data, list):
        traders = data
    else:
        traders = []
    safe_print(f"  Fetched {len(traders)} traders from leaderboard")
    return traders[:limit]


# ---------------------------------------------------------------------------
# Wallet activity fetching
# ---------------------------------------------------------------------------

def fetch_wallet_activity(wallet: str, limit: int = 100) -> list[dict]:
    """Fetch recent trades for a wallet from data-api.

    Returns list of trade dicts with keys: side, market, title, timestamp, size.
    """
    url = f"{DATA_API}/activity?user={wallet}&limit={limit}"
    data = _http_get_json(url, timeout=20)
    if not data:
        return []
    activities = data if isinstance(data, list) else data.get("history", data.get("data", []))
    if not activities:
        return []

    trades = []
    for act in activities:
        side = (act.get("side", act.get("type", ""))).lower()
        market = act.get("market", act.get("conditionId", act.get("id", "")))
        title = act.get("title", act.get("question", act.get("market_title", market)))
        ts_raw = act.get("timestamp", act.get("createdAt", act.get("time", "")))
        size = float(act.get("size", act.get("amount", act.get("usdcSize", 0))))

        # Parse timestamp
        ts = None
        if ts_raw:
            try:
                if isinstance(ts_raw, (int, float)):
                    ts = datetime.fromtimestamp(ts_raw, tz=timezone.utc)
                else:
                    ts = datetime.fromisoformat(str(ts_raw).replace("Z", "+00:00"))
            except Exception:
                pass

        trades.append({
            "wallet": wallet,
            "side": side,
            "market": str(market),
            "title": str(title),
            "timestamp": ts,
            "size": size,
        })
    return trades


# ---------------------------------------------------------------------------
# Entry timeline construction
# ---------------------------------------------------------------------------

def build_entry_timeline(all_wallet_activities: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Build a timeline of BUY entries grouped by market, sorted earliest-first.

    Args:
        all_wallet_activities: wallet_address -> list of trade dicts

    Returns:
        market_title -> list of {wallet, side, timestamp, size} ordered by time
    """
    market_entries: dict[str, list[dict]] = {}

    for wallet, activities in all_wallet_activities.items():
        for trade in activities:
            if trade["side"] not in ("buy", "long"):
                continue
            if trade["timestamp"] is None:
                continue

            title = trade["title"]
            entry = {
                "wallet": wallet,
                "side": trade["side"],
                "timestamp": trade["timestamp"],
                "size": trade["size"],
            }
            market_entries.setdefault(title, []).append(entry)

    # Sort each market's entries by timestamp (earliest first)
    for title in market_entries:
        market_entries[title].sort(key=lambda e: e["timestamp"])

    return market_entries


# ---------------------------------------------------------------------------
# Early mover detection
# ---------------------------------------------------------------------------

def find_early_mover_signals(
    entry_timeline: dict[str, list[dict]],
    early_window_hours: int,
    min_followers: int,
    freshness_hours: int,
) -> list[tuple[str, str, str, int, float]]:
    """Identify early-mover wallets and their confirmed signals.

    For each market in the timeline:
      - First entry = early mover candidate
      - Followers = wallets that entered same side within early_window_hours
      - Valid if followers >= min_followers AND first entry within freshness_hours

    Also tracks a per-wallet "lead score": how many markets each wallet led.

    Returns:
        list of (market_title, early_mover_wallet, early_mover_side,
                 follower_count, early_mover_lead_score)
    """
    now = datetime.now(timezone.utc)
    freshness_cutoff = now - timedelta(hours=freshness_hours)
    early_window = timedelta(hours=early_window_hours)

    # Track how many markets each wallet has led (for lead score)
    lead_counts: dict[str, int] = {}
    market_leads: dict[str, int] = {}  # wallet -> total markets where it was follower-confirmed first

    # First pass: count leads per wallet across ALL markets (not just fresh ones)
    for title, entries in entry_timeline.items():
        if len(entries) < 2:
            continue
        first = entries[0]
        first_wallet = first["wallet"]
        first_side = first["side"]
        first_ts = first["timestamp"]

        followers = 0
        for entry in entries[1:]:
            if entry["wallet"] == first_wallet:
                continue
            if entry["side"] != first_side:
                continue
            if (entry["timestamp"] - first_ts) <= early_window:
                followers += 1

        if followers >= min_followers:
            lead_counts[first_wallet] = lead_counts.get(first_wallet, 0) + 1

    # Second pass: build signals for fresh markets only
    signals = []
    for title, entries in entry_timeline.items():
        if len(entries) < 2:
            continue

        first = entries[0]
        first_wallet = first["wallet"]
        first_side = first["side"]
        first_ts = first["timestamp"]

        # Freshness check
        if first_ts < freshness_cutoff:
            continue

        followers = 0
        for entry in entries[1:]:
            if entry["wallet"] == first_wallet:
                continue
            if entry["side"] != first_side:
                continue
            if (entry["timestamp"] - first_ts) <= early_window:
                followers += 1

        if followers < min_followers:
            continue

        lead_score = lead_counts.get(first_wallet, 0)
        signals.append((title, first_wallet, first_side, followers, float(lead_score)))

    # Sort by lead score descending, then by follower count
    signals.sort(key=lambda s: (s[4], s[3]), reverse=True)
    return signals


# ---------------------------------------------------------------------------
# Fresh entries from early mover
# ---------------------------------------------------------------------------

def find_fresh_entries(
    early_mover_wallet: str,
    activities: list[dict],
    freshness_hours: int,
) -> list[tuple[str, str, float, float]]:
    """Find BUY positions by the early mover that are very recent.

    These are positions where the early mover just entered but followers
    may not have piled in yet -- the freshest alpha.

    Returns:
        list of (market_title, side, size, hours_ago)
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=freshness_hours)
    fresh = []

    for trade in activities:
        if trade["wallet"] != early_mover_wallet:
            continue
        if trade["side"] not in ("buy", "long"):
            continue
        if trade["timestamp"] is None:
            continue
        if trade["timestamp"] < cutoff:
            continue

        hours_ago = (now - trade["timestamp"]).total_seconds() / 3600
        fresh.append((trade["title"], trade["side"], trade["size"], round(hours_ago, 1)))

    # Most recent first
    fresh.sort(key=lambda x: x[3])
    return fresh


# ---------------------------------------------------------------------------
# Signal validation (per CLAUDE.md conviction-based sizing)
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """Standard conviction-based signal for market validation."""
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days} days to resolve"
        except Exception:
            pass

    if p <= YES_THRESHOLD:
        conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return "yes", size, f"YES {p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    if p >= NO_THRESHOLD:
        conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return "no", size, f"NO YES={p:.0%} edge={edge:.0%} size=${size} -- {q[:70]}"

    return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"


# ---------------------------------------------------------------------------
# Early-mover boosted signal
# ---------------------------------------------------------------------------

def compute_early_mover_signal(
    market,
    mover_side: str,
    lead_score: float,
    follower_count: int,
) -> tuple[str | None, float, str]:
    """Conviction-based signal boosted by early-mover lead score.

    Only trades if the mover's side aligns with compute_signal direction.
    Lead score multiplier: 1 + min(0.4, lead_score * 0.1)
    """
    base_side, base_size, base_reasoning = compute_signal(market)

    # No base signal -> skip
    if base_side is None:
        return None, 0, f"No base signal: {base_reasoning}"

    # Mover side must align with base signal direction
    mover_side_norm = "yes" if mover_side in ("buy", "long", "yes") else mover_side
    if base_side != mover_side_norm:
        return None, 0, (
            f"Mover side '{mover_side_norm}' conflicts with base signal '{base_side}'"
        )

    p = market.current_probability
    q = market.question

    # Recompute conviction with lead score boost
    if base_side == "yes":
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    else:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)

    lead_mult = 1 + min(0.4, lead_score * 0.1)
    conviction = min(1.0, base_conviction * lead_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    return base_side, size, (
        f"{base_side.upper()} {p:.0%} lead_score={lead_score:.0f} "
        f"followers={follower_count} mult={lead_mult:.2f} "
        f"size=${size} -- {q[:60]}"
    )


# ---------------------------------------------------------------------------
# Context check
# ---------------------------------------------------------------------------

def context_ok(client: SimmerClient) -> bool:
    """Check portfolio context to prevent excessive positions."""
    try:
        positions = client.get_positions()
        open_count = len([p for p in positions if float(getattr(p, "size", 0)) > 0])
        if open_count >= MAX_POSITIONS:
            safe_print(f"  [GATE] Already at {open_count}/{MAX_POSITIONS} positions, skipping")
            return False
    except Exception as exc:
        safe_print(f"  [WARN] Could not check positions: {exc}")
    return True


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False):
    mode = "LIVE" if live else "PAPER"
    safe_print(f"\n{'='*64}")
    safe_print(f"  Early Mover Copytrader [{mode}]")
    safe_print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    safe_print(f"{'='*64}")

    client = get_client(live)

    if not context_ok(client):
        safe_print("\nAborted: portfolio context check failed.")
        return

    # Step 1: Fetch leaderboard
    safe_print(f"\n[1/5] Fetching leaderboard (top {LEADERBOARD_LIMIT})...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    if not traders:
        safe_print("  No traders found on leaderboard. Exiting.")
        return

    # Step 2: Fetch activity for each wallet
    safe_print(f"\n[2/5] Fetching wallet activity...")
    all_activities: dict[str, list[dict]] = {}
    for i, t in enumerate(traders):
        wallet = (
            t.get("address")
            or t.get("wallet")
            or t.get("id", "unknown")
        )
        wallet = str(wallet)
        safe_print(f"  [{i+1}/{len(traders)}] {wallet[:12]}...")
        activities = fetch_wallet_activity(wallet, limit=100)
        if activities:
            all_activities[wallet] = activities
            safe_print(f"    -> {len(activities)} trades")
        else:
            safe_print(f"    -> no activity")

    if not all_activities:
        safe_print("  No wallet activity found. Exiting.")
        return

    # Step 3: Build entry timeline & find early movers
    safe_print(f"\n[3/5] Building entry timeline & detecting early movers...")
    timeline = build_entry_timeline(all_activities)
    safe_print(f"  Markets with multi-wallet entries: {len(timeline)}")

    signals = find_early_mover_signals(
        timeline,
        early_window_hours=EARLY_WINDOW_HOURS,
        min_followers=MIN_FOLLOWERS,
        freshness_hours=FRESHNESS_HOURS,
    )
    safe_print(f"  Early mover signals found: {len(signals)}")

    if not signals:
        safe_print("  No confirmed early-mover signals. Exiting.")
        return

    # Build per-wallet dashboard data
    wallet_stats: dict[str, dict] = {}
    for title, wallet, side, followers, lead_score in signals:
        if wallet not in wallet_stats:
            wallet_stats[wallet] = {
                "lead_score": lead_score,
                "markets_led": 0,
                "total_followers": 0,
            }
        wallet_stats[wallet]["markets_led"] += 1
        wallet_stats[wallet]["total_followers"] += followers

    # Print early mover dashboard
    safe_print(f"\n{'='*64}")
    safe_print(f"  EARLY MOVER DASHBOARD")
    safe_print(f"{'='*64}")
    safe_print(f"  {'Wallet':<14} | {'LeadScore':>9} | {'MktsLed':>7} | {'AvgFollowers':>12}")
    safe_print(f"  {'-'*14}-+-{'-'*9}-+-{'-'*7}-+-{'-'*12}")
    for wallet, stats in sorted(wallet_stats.items(), key=lambda x: x[1]["lead_score"], reverse=True):
        avg_f = stats["total_followers"] / max(1, stats["markets_led"])
        safe_print(
            f"  {wallet[:14]:<14} | {stats['lead_score']:>9.0f} | "
            f"{stats['markets_led']:>7} | {avg_f:>12.1f}"
        )

    # Step 4: Find fresh entries from top early mover(s)
    safe_print(f"\n[4/5] Finding fresh entries from top early movers...")

    # Collect top early mover wallets (by lead score)
    top_movers = sorted(wallet_stats.keys(), key=lambda w: wallet_stats[w]["lead_score"], reverse=True)

    fresh_targets: list[tuple[str, str, float, float, str, float]] = []
    # (market_title, side, size, hours_ago, mover_wallet, lead_score)
    for mover_wallet in top_movers[:3]:  # Check top 3 movers
        wallet_trades = all_activities.get(mover_wallet, [])
        fresh = find_fresh_entries(mover_wallet, wallet_trades, FRESHNESS_HOURS)
        for title, side, size, hours_ago in fresh:
            ls = wallet_stats[mover_wallet]["lead_score"]
            fresh_targets.append((title, side, size, hours_ago, mover_wallet, ls))
            safe_print(f"  FRESH: {title[:50]} | {side} | ${size:.0f} | {hours_ago:.1f}h ago | {mover_wallet[:10]}...")

    if not fresh_targets:
        safe_print("  No fresh entries from top early movers. Exiting.")
        return

    # Step 5: Match to Simmer markets & trade
    safe_print(f"\n[5/5] Matching to markets & executing signals...")
    executed = 0
    skipped = 0

    # Deduplicate by market title
    seen_markets: set[str] = set()
    for title, mover_side, mover_size, hours_ago, mover_wallet, lead_score in fresh_targets:
        if title in seen_markets:
            continue
        seen_markets.add(title)

        # Search for market in Simmer
        keywords = " ".join(title.split()[:5])
        try:
            markets = client.find_markets(keywords)
        except Exception as exc:
            safe_print(f"  [WARN] Market search failed for '{keywords}': {exc}")
            continue

        if not markets:
            safe_print(f"  [SKIP] No Simmer market found for: {title[:60]}")
            skipped += 1
            continue

        # Pick best match (first result)
        m = markets[0]

        # Volume gate
        vol = getattr(m, "volume", 0) or 0
        if vol < MIN_VOLUME:
            safe_print(f"  [SKIP] Low volume ${vol:.0f} < ${MIN_VOLUME:.0f}: {m.question[:60]}")
            skipped += 1
            continue

        # Get follower count for this market from signals
        follower_count = 0
        for s_title, s_wallet, s_side, s_followers, s_ls in signals:
            if s_title == title and s_wallet == mover_wallet:
                follower_count = s_followers
                break

        # Compute early-mover boosted signal
        side, size, reasoning = compute_early_mover_signal(
            m, mover_side, lead_score, follower_count
        )

        if side is None:
            safe_print(f"  [SKIP] {reasoning}")
            skipped += 1
            continue

        safe_print(f"  SIGNAL: {reasoning}")

        try:
            r = client.trade(
                market_id=m.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
            )
            safe_print(f"  TRADE: {side.upper()} ${size:.2f} on {m.question[:60]}")
            safe_print(f"    -> {r}")
            executed += 1
        except Exception as exc:
            safe_print(f"  [ERROR] Trade failed: {exc}")
            skipped += 1

    # Summary
    safe_print(f"\n{'='*64}")
    safe_print(f"  SUMMARY")
    safe_print(f"{'='*64}")
    safe_print(f"  Wallets scanned:    {len(all_activities)}")
    safe_print(f"  Markets in timeline:{len(timeline)}")
    safe_print(f"  Early mover signals:{len(signals)}")
    safe_print(f"  Fresh targets:      {len(fresh_targets)}")
    safe_print(f"  Trades executed:    {executed}")
    safe_print(f"  Trades skipped:     {skipped}")
    safe_print(f"{'='*64}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Early Mover Copytrader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: paper)")
    args = parser.parse_args()
    run(live=args.live)

"""
polymarket-whale-streak-trader
Tracks rolling win rate per whale wallet from the predicting.top leaderboard
and only follows wallets currently on a verified "hot streak". Computes a
rolling win rate over the most recent N trades per wallet, classifies each
wallet as HOT / WARM / COLD, and dynamically promotes or demotes wallets.
Only positions from HOT wallets are eligible for trading. A streak-boost
multiplier scales conviction when the whale's win rate exceeds the hot
threshold, rewarding consistently winning wallets with larger position sizes.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- live=True -> venue="polymarket" (real trades, only with --live flag).
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import argparse
import json
import statistics
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-whale-streak-trader"
SKILL_SLUG   = "polymarket-whale-streak-trader"

# Broad keywords for market discovery
KEYWORDS = [
    "crypto", "bitcoin", "ethereum", "trump", "biden", "election",
    "president", "fed", "inflation", "recession", "war", "nato",
    "ai", "openai", "sports", "nba", "nfl", "soccer", "ufc",
    "climate", "hurricane", "pandemic", "supreme court", "congress",
]

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "3000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.10"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "5"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "8"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Skill-specific tunables
HOT_WIN_RATE       = float(os.environ.get("SIMMER_HOT_WIN_RATE",       "0.65"))
COLD_WIN_RATE      = float(os.environ.get("SIMMER_COLD_WIN_RATE",      "0.45"))
STREAK_WINDOW      = int(os.environ.get(  "SIMMER_STREAK_WINDOW",      "30"))
LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",  "20"))

_client: SimmerClient | None = None

# Public APIs
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API = "https://data-api.polymarket.com"


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False -> venue="sim"  (paper trades -- safe default).
    live=True  -> venue="polymarket" (real trades, only with --live flag).
    """
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global HOT_WIN_RATE, COLD_WIN_RATE, STREAK_WINDOW, LEADERBOARD_LIMIT
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
        MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
        HOT_WIN_RATE       = float(os.environ.get("SIMMER_HOT_WIN_RATE",       str(HOT_WIN_RATE)))
        COLD_WIN_RATE      = float(os.environ.get("SIMMER_COLD_WIN_RATE",      str(COLD_WIN_RATE)))
        STREAK_WINDOW      = int(os.environ.get(  "SIMMER_STREAK_WINDOW",      str(STREAK_WINDOW)))
        LEADERBOARD_LIMIT  = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",  str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# Leaderboard and whale activity
# ---------------------------------------------------------------------------

def fetch_leaderboard(limit=20):
    """Fetch top traders from predicting.top"""
    req = Request(LEADERBOARD_URL, headers={"User-Agent": "SimmerSDK/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        traders = data if isinstance(data, list) else data.get("traders", data.get("data", []))
        return traders[:limit]
    except Exception as e:
        safe_print(f"[leaderboard] fetch error: {e}")
        return []


def fetch_wallet_activity(wallet, limit=50):
    """Fetch recent trades for a wallet from Polymarket data API (public, no auth)"""
    url = f"{DATA_API}/activity?user={wallet.lower()}&limit={limit}"
    req = Request(url, headers={"User-Agent": "SimmerSDK/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        safe_print(f"[activity] {wallet[:10]}...: {e}")
        return []


# ---------------------------------------------------------------------------
# Rolling win rate computation
# ---------------------------------------------------------------------------

def compute_rolling_win_rate(activities, window=30):
    """
    Compute rolling win rate from recent trade activity.

    Tracks positions per (market, outcome). For each sell/redeem event,
    calculates whether the position was profitable (exit price > avg entry).

    Returns (win_rate, total_closed_trades, pnl_estimate).
    """
    recent = activities[:window] if len(activities) > window else activities

    # Track open positions: key = (title, outcome) -> list of entry prices
    entries: dict[tuple[str, str], list[float]] = {}
    wins = 0
    losses = 0
    total_pnl = 0.0

    # Process in chronological order (reverse since API returns newest first)
    for a in reversed(recent):
        action = a.get("action", a.get("side", "")).lower()
        title = a.get("title", "")[:60]
        outcome = a.get("outcome", "").lower()
        price = float(a.get("price", a.get("avgPrice", 0.5)))
        size = float(a.get("usdcSize", a.get("size", 0)))

        if not title or not outcome:
            continue

        key = (title, outcome)

        if "buy" in action:
            # Record entry
            entries.setdefault(key, []).append(price)

        elif "sell" in action or "redeem" in action:
            # Check if we have an entry to compare against
            if key in entries and entries[key]:
                avg_entry = statistics.mean(entries[key])
                if "redeem" in action:
                    # Redemption at $1 means the outcome resolved YES
                    exit_price = 1.0
                else:
                    exit_price = price

                pnl = (exit_price - avg_entry) * size
                total_pnl += pnl

                if exit_price > avg_entry:
                    wins += 1
                else:
                    losses += 1

                # Clear the position
                entries[key] = []

    total_closed = wins + losses
    win_rate = wins / total_closed if total_closed > 0 else 0.0
    return win_rate, total_closed, total_pnl


def classify_streak(win_rate):
    """Classify wallet streak status based on win rate thresholds."""
    if win_rate >= HOT_WIN_RATE:
        return "HOT"
    elif win_rate <= COLD_WIN_RATE:
        return "COLD"
    else:
        return "WARM"


# ---------------------------------------------------------------------------
# Position extraction from hot wallets
# ---------------------------------------------------------------------------

def extract_hot_wallet_positions(activities):
    """
    Extract current open positions from recent activity.
    Only considers the last STREAK_WINDOW trades.
    Returns list of (market_title_fragment, side, net_size).
    """
    recent = activities[:STREAK_WINDOW] if len(activities) > STREAK_WINDOW else activities

    # Track net position per (title, outcome)
    positions: dict[str, dict[str, float]] = {}

    for a in recent:
        action = a.get("action", a.get("side", "")).lower()
        title = a.get("title", "")[:60]
        outcome = a.get("outcome", "").lower()
        size = float(a.get("usdcSize", a.get("size", 0)))

        if not title or outcome not in ("yes", "no"):
            continue

        if title not in positions:
            positions[title] = {"yes_size": 0.0, "no_size": 0.0}

        if "buy" in action:
            positions[title][f"{outcome}_size"] += size
        elif "sell" in action or "redeem" in action:
            positions[title][f"{outcome}_size"] -= size

    # Return net open positions with a clear directional lean
    result = []
    for title, sizes in positions.items():
        yes_net = max(0.0, sizes["yes_size"])
        no_net = max(0.0, sizes["no_size"])
        if yes_net > no_net and yes_net > 0:
            result.append((title, "yes", yes_net))
        elif no_net > yes_net and no_net > 0:
            result.append((title, "no", no_net))

    return sorted(result, key=lambda x: x[2], reverse=True)


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).
    Standard conviction-based sizing per CLAUDE.md.
    """
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


def compute_streak_boosted_signal(market, whale_side, win_rate) -> tuple[str | None, float, str]:
    """
    Only trade if whale_side matches compute_signal direction.
    Apply streak boost multiplier based on how far above HOT_WIN_RATE the whale is.

    streak_mult = 1 + min(0.5, (win_rate - HOT_WIN_RATE) / (1 - HOT_WIN_RATE))
    Final conviction = min(1.0, base_conviction * streak_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
    """
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

    # Compute base conviction from standard signal
    base_side = None
    base_conviction = 0.0
    edge = 0.0

    if p <= YES_THRESHOLD:
        base_side = "yes"
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        edge = YES_THRESHOLD - p
    elif p >= NO_THRESHOLD:
        base_side = "no"
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        edge = p - NO_THRESHOLD
    else:
        return None, 0, f"Neutral at {p:.1%} (outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands)"

    # Only trade if whale direction matches signal direction
    if base_side != whale_side:
        return None, 0, (
            f"Signal={base_side} but whale={whale_side} on {q[:50]} -- no alignment"
        )

    # Streak boost: reward higher win rates with larger positions
    streak_mult = 1 + min(0.5, (win_rate - HOT_WIN_RATE) / (1 - HOT_WIN_RATE))
    conviction = min(1.0, base_conviction * streak_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    return (
        base_side,
        size,
        f"{base_side.upper()} {p:.0%} edge={edge:.0%} streak_boost={streak_mult:.2f} "
        f"size=${size} wr={win_rate:.0%} -- {q[:60]}",
    )


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    """Check flip-flop and slippage safeguards."""
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            reason = ctx["discipline"].get("flip_flop_reason", "recent reversal")
            return False, f"Flip-flop: {reason}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def find_markets(client: SimmerClient) -> list:
    """
    Discover markets via keyword search with bulk fallback.
    Returns deduplicated list of all found markets.
    """
    seen: set[str] = set()
    unique: list = []

    for kw in KEYWORDS:
        try:
            for m in client.find_markets(kw):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] '{kw}': {e}")

    if len(unique) < 20:
        try:
            for m in client.get_markets(limit=200):
                market_id = getattr(m, "id", None)
                if market_id and market_id not in seen:
                    seen.add(market_id)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[bulk-fetch] {e}")

    return unique


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[whale-streak] mode={mode} max_pos=${MAX_POSITION} "
        f"hot_wr={HOT_WIN_RATE:.0%} cold_wr={COLD_WIN_RATE:.0%} window={STREAK_WINDOW}"
    )

    client = get_client(live=live)

    # Step 1: Fetch leaderboard
    safe_print(f"[whale-streak] fetching top {LEADERBOARD_LIMIT} traders from leaderboard...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    safe_print(f"[whale-streak] {len(traders)} traders fetched")

    if not traders:
        safe_print("[whale-streak] no traders from leaderboard. done.")
        return

    # Step 2: For each wallet, compute rolling win rate and classify streak
    safe_print("")
    safe_print("=" * 78)
    safe_print(f"{'WALLET':<16} {'WIN RATE':>10} {'STATUS':>8} {'CLOSED':>8} {'PNL':>10}")
    safe_print("-" * 78)

    hot_wallets = []   # (wallet, name, win_rate, activities)
    warm_count = 0
    cold_count = 0

    for t in traders:
        wallet = t.get("wallet", "") or ""
        name = t.get("name", "") or wallet[:12]
        if not wallet:
            continue

        activities = fetch_wallet_activity(wallet, limit=max(50, STREAK_WINDOW + 20))
        if not activities:
            safe_print(f"  {name[:14]:<16} {'N/A':>10} {'SKIP':>8} {'0':>8} {'$0':>10}")
            continue

        win_rate, closed_trades, pnl = compute_rolling_win_rate(activities, window=STREAK_WINDOW)
        status = classify_streak(win_rate)

        safe_print(
            f"  {name[:14]:<16} {win_rate:>9.0%} {status:>8} {closed_trades:>8} "
            f"{'${:,.0f}'.format(pnl):>10}"
        )

        if status == "HOT":
            hot_wallets.append((wallet, name, win_rate, activities))
        elif status == "WARM":
            warm_count += 1
        else:
            cold_count += 1

    safe_print("-" * 78)
    safe_print(
        f"  HOT: {len(hot_wallets)}  WARM: {warm_count}  COLD: {cold_count}"
    )
    safe_print("=" * 78)
    safe_print("")

    if not hot_wallets:
        safe_print("[whale-streak] no HOT wallets found. done.")
        return

    # Step 3: Collect positions from HOT wallets only
    all_hot_positions = []  # (title, side, net_size, wallet_name, win_rate)

    for wallet, name, win_rate, activities in hot_wallets:
        positions = extract_hot_wallet_positions(activities)
        safe_print(f"  [hot] {name}: {len(positions)} open positions (wr={win_rate:.0%})")
        for title, side, net_size in positions[:10]:
            all_hot_positions.append((title, side, net_size, name, win_rate))

    safe_print(f"[whale-streak] {len(all_hot_positions)} total hot-wallet positions to evaluate")

    if not all_hot_positions:
        safe_print("[whale-streak] no open positions from HOT wallets. done.")
        return

    # Step 4: Discover Simmer markets
    markets = find_markets(client)
    safe_print(f"[whale-streak] {len(markets)} Simmer markets discovered")

    # Build lookup: lowercase question -> market object
    market_lookup: dict[str, list] = {}
    for m in markets:
        q = getattr(m, "question", "")
        if q:
            market_lookup.setdefault(q.lower(), []).append(m)

    # Step 5: Match hot-wallet positions to Simmer markets and trade
    placed = 0

    # Sort by net size descending (strongest conviction first)
    all_hot_positions.sort(key=lambda x: x[2], reverse=True)

    for title, whale_side, net_size, whale_name, win_rate in all_hot_positions:
        if placed >= MAX_POSITIONS:
            break

        # Find matching Simmer market by substring matching
        matched_market = None
        title_lower = title.strip().lower()
        title_words = [w for w in title_lower.split() if len(w) > 3]

        if not title_words:
            continue

        for q_lower, mlist in market_lookup.items():
            matches = sum(1 for w in title_words if w in q_lower)
            if matches >= max(2, len(title_words) // 2):
                matched_market = mlist[0]
                break

        if not matched_market:
            safe_print(f"  [no-match] {title[:60]} -- no Simmer market found")
            continue

        # Volume gate
        vol = getattr(matched_market, "volume", 0) or 0
        if vol < MIN_VOLUME:
            safe_print(f"  [skip] volume ${vol:.0f} < ${MIN_VOLUME:.0f}: {title[:50]}")
            continue

        # Step 6: Compute streak-boosted signal
        side, size, reasoning = compute_streak_boosted_signal(
            matched_market, whale_side, win_rate
        )
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        # Step 7: Context check
        ok, why = context_ok(client, matched_market.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        # Step 8: Execute trade
        whale_reasoning = (
            f"STREAK-BOOSTED {reasoning} | whale={whale_name} wr={win_rate:.0%}"
        )

        try:
            r = client.trade(
                market_id=matched_market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=whale_reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {whale_reasoning[:120]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {matched_market.id}: {e}")

    safe_print(f"\n[whale-streak] done. {placed} orders placed.")
    safe_print(
        f"  HOT wallets tracked: {len(hot_wallets)} | "
        f"Positions evaluated: {len(all_hot_positions)} | "
        f"Trades placed: {placed}/{MAX_POSITIONS}"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Whale streak trader -- follows only hot-streak Polymarket whales."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)

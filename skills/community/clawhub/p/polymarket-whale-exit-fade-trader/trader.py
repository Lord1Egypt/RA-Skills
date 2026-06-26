"""
polymarket-whale-exit-fade-trader
Detects when multiple whale wallets exit (sell) positions simultaneously,
causing the market to overshoot downward. Fades the panic by buying the dip
after whale dumps -- the market often recovers because retail panic-sells
alongside whales, pushing prices below fair value. Once the panic subsides,
the market reverts.

Strategy:
1. Fetch top wallets from the predicting.top leaderboard.
2. Scan each wallet's recent activity for SELL actions.
3. Group sells by market -- when multiple whales sell the same market
   within the lookback window, flag it as a whale exit event.
4. Find the corresponding Simmer market and check if the price has
   overshot into the threshold band (e.g. dropped below YES_THRESHOLD).
5. Fade the exit: buy the dip with conviction-based sizing, boosted by
   exit intensity (more whales exiting = stronger signal).

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
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-whale-exit-fade-trader"
SKILL_SLUG   = "polymarket-whale-exit-fade-trader"

# Risk parameters -- declared as tunables in clawhub.json, adjustable from Simmer UI.
MAX_POSITION   = float(os.environ.get("SIMMER_MAX_POSITION",  "40"))
MIN_VOLUME     = float(os.environ.get("SIMMER_MIN_VOLUME",    "5000"))
MAX_SPREAD     = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.12"))
MIN_DAYS       = int(os.environ.get(  "SIMMER_MIN_DAYS",      "5"))
MAX_POSITIONS  = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "6"))
YES_THRESHOLD  = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD   = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE      = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

# Skill-specific tunables
EXIT_LOOKBACK_HOURS = int(os.environ.get(  "SIMMER_EXIT_LOOKBACK_HOURS", "24"))
MIN_EXIT_WHALES     = int(os.environ.get(  "SIMMER_MIN_EXIT_WHALES",     "2"))
MIN_EXIT_VOLUME     = float(os.environ.get("SIMMER_MIN_EXIT_VOLUME",     "500"))
LEADERBOARD_LIMIT   = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",   "20"))

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
    global EXIT_LOOKBACK_HOURS, MIN_EXIT_WHALES, MIN_EXIT_VOLUME, LEADERBOARD_LIMIT
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
        MAX_POSITION        = float(os.environ.get("SIMMER_MAX_POSITION",        str(MAX_POSITION)))
        MIN_VOLUME          = float(os.environ.get("SIMMER_MIN_VOLUME",          str(MIN_VOLUME)))
        MAX_SPREAD          = float(os.environ.get("SIMMER_MAX_SPREAD",          str(MAX_SPREAD)))
        MIN_DAYS            = int(os.environ.get(  "SIMMER_MIN_DAYS",            str(MIN_DAYS)))
        MAX_POSITIONS       = int(os.environ.get(  "SIMMER_MAX_POSITIONS",       str(MAX_POSITIONS)))
        YES_THRESHOLD       = float(os.environ.get("SIMMER_YES_THRESHOLD",       str(YES_THRESHOLD)))
        NO_THRESHOLD        = float(os.environ.get("SIMMER_NO_THRESHOLD",        str(NO_THRESHOLD)))
        MIN_TRADE           = float(os.environ.get("SIMMER_MIN_TRADE",           str(MIN_TRADE)))
        EXIT_LOOKBACK_HOURS = int(os.environ.get(  "SIMMER_EXIT_LOOKBACK_HOURS", str(EXIT_LOOKBACK_HOURS)))
        MIN_EXIT_WHALES     = int(os.environ.get(  "SIMMER_MIN_EXIT_WHALES",     str(MIN_EXIT_WHALES)))
        MIN_EXIT_VOLUME     = float(os.environ.get("SIMMER_MIN_EXIT_VOLUME",     str(MIN_EXIT_VOLUME)))
        LEADERBOARD_LIMIT   = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",   str(LEADERBOARD_LIMIT)))
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


def fetch_recent_activity(wallet, limit=100):
    """Fetch recent trades for a wallet from Polymarket data API (public, no auth)."""
    url = f"{DATA_API}/activity?user={wallet.lower()}&limit={limit}"
    req = Request(url, headers={"User-Agent": "SimmerSDK/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        safe_print(f"[activity] {wallet[:10]}...: {e}")
        return []


# ---------------------------------------------------------------------------
# Whale exit detection
# ---------------------------------------------------------------------------

def detect_whale_exits(all_activities, lookback_hours):
    """
    Analyze all whale activities to find markets where multiple whales are selling.

    Parameters:
        all_activities: dict of {wallet: [activity_records]}
        lookback_hours: only consider sells within this window

    Returns list of dicts:
        {
            "market_keyword": str,
            "exit_wallets": set of wallets selling this market,
            "exit_volume": float total USD volume of sells,
            "original_side_sold": str ("yes" or "no") -- what they were selling
        }
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

    # Group SELL actions by market title across all wallets
    # Key: (market_title_fragment, side_sold) -> {wallets, volume}
    sell_map: dict[tuple[str, str], dict] = {}

    for wallet, activities in all_activities.items():
        if not isinstance(activities, list):
            continue
        for a in activities:
            action = a.get("action", a.get("side", "")).lower()
            if "sell" not in action:
                continue

            # Check timestamp is within lookback window
            ts_str = a.get("timestamp", a.get("createdAt", ""))
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts < cutoff:
                        continue
                except Exception:
                    pass  # If we can't parse the timestamp, include it

            title = a.get("title", "").strip()
            if not title:
                continue

            outcome = a.get("outcome", "").lower()
            if outcome not in ("yes", "no"):
                continue

            size = float(a.get("usdcSize", a.get("size", 0)))
            key = (title[:80], outcome)

            if key not in sell_map:
                sell_map[key] = {"wallets": set(), "volume": 0.0}
            sell_map[key]["wallets"].add(wallet)
            sell_map[key]["volume"] += size

    # Convert to result list
    exits = []
    for (title_frag, side_sold), info in sell_map.items():
        exits.append({
            "market_keyword": title_frag,
            "exit_wallets": info["wallets"],
            "exit_volume": info["volume"],
            "original_side_sold": side_sold,
        })

    # Sort by number of exiting whales descending, then by volume
    exits.sort(key=lambda x: (len(x["exit_wallets"]), x["exit_volume"]), reverse=True)
    return exits


def find_fade_opportunities(client, exits, min_whales, min_volume):
    """
    Filter whale exits to actionable fade opportunities.

    For each qualified exit:
    - Find matching Simmer market
    - Check if market price has dropped into the fade zone

    Returns list of (market, fade_direction, whale_exit_count, exit_volume).
    """
    opportunities = []

    for exit_info in exits:
        whale_count = len(exit_info["exit_wallets"])
        volume = exit_info["exit_volume"]

        # Filter by minimum whale count and volume
        if whale_count < min_whales:
            continue
        if volume < min_volume:
            continue

        keyword = exit_info["market_keyword"]
        side_sold = exit_info["original_side_sold"]

        safe_print(
            f"  [exit] {whale_count} whales sold {side_sold.upper()} "
            f"${volume:.0f} on: {keyword[:60]}"
        )

        # Search for matching Simmer market using keyword fragments
        search_words = [w for w in keyword.split() if len(w) > 3][:5]
        search_query = " ".join(search_words) if search_words else keyword[:40]

        matched_market = None
        try:
            candidates = client.find_markets(search_query)
            for m in candidates:
                q = getattr(m, "question", "").lower()
                kw_lower = keyword.lower()
                # Match if enough keywords overlap
                kw_words = [w for w in kw_lower.split() if len(w) > 3]
                if not kw_words:
                    continue
                matches = sum(1 for w in kw_words if w in q)
                if matches >= max(2, len(kw_words) // 2):
                    matched_market = m
                    break
        except Exception as e:
            safe_print(f"  [search] error: {e}")
            continue

        if not matched_market:
            safe_print(f"  [no-match] {keyword[:50]} -- no Simmer market found")
            continue

        p = matched_market.current_probability

        # Determine fade direction:
        # If whales sold YES -> price likely dropped -> we buy YES (fade the dump)
        # If whales sold NO  -> price likely rose   -> we buy NO  (fade the pump)
        if side_sold == "yes" and p <= YES_THRESHOLD:
            fade_direction = "yes"
        elif side_sold == "no" and p >= NO_THRESHOLD:
            fade_direction = "no"
        else:
            safe_print(
                f"  [skip] {keyword[:50]} p={p:.1%} not in fade zone "
                f"(sold {side_sold}, need {'<=' + str(YES_THRESHOLD) if side_sold == 'yes' else '>=' + str(NO_THRESHOLD)})"
            )
            continue

        opportunities.append((matched_market, fade_direction, whale_count, volume))

    return opportunities


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


def compute_fade_signal(market, fade_direction, exit_whale_count, exit_volume):
    """
    Enhanced signal for whale-exit fade trades.

    Applies exit intensity boost on top of base conviction sizing:
    - More whales exiting = stronger fade signal
    - Higher exit volume = stronger fade signal
    - conviction capped at 1.0

    Returns (side, size, reasoning) or (None, 0, skip_reason).
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

    # Compute base conviction from threshold distance
    if fade_direction == "yes" and p <= YES_THRESHOLD:
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
        edge = YES_THRESHOLD - p
    elif fade_direction == "no" and p >= NO_THRESHOLD:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)
        edge = p - NO_THRESHOLD
    else:
        return None, 0, f"Price {p:.1%} not in {fade_direction} fade zone"

    # Exit intensity boost: more whales + higher volume = stronger signal
    exit_mult = 1 + min(0.5, (exit_whale_count - 1) * 0.15 + min(0.2, exit_volume / 5000))
    conviction = min(1.0, base_conviction * exit_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    reasoning = (
        f"FADE {fade_direction.upper()} {p:.0%} edge={edge:.0%} size=${size} "
        f"| {exit_whale_count} whales exited ${exit_volume:.0f} "
        f"conv={conviction:.0%} mult={exit_mult:.2f} -- {q[:60]}"
    )
    return fade_direction, size, reasoning


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


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(live: bool = False) -> None:
    mode = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[whale-exit-fade] mode={mode} max_pos=${MAX_POSITION} "
        f"lookback={EXIT_LOOKBACK_HOURS}h min_whales={MIN_EXIT_WHALES} "
        f"min_exit_vol=${MIN_EXIT_VOLUME}"
    )

    client = get_client(live=live)

    # Step 1: Fetch leaderboard
    safe_print(f"[whale-exit-fade] fetching top {LEADERBOARD_LIMIT} wallets from leaderboard...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    safe_print(f"[whale-exit-fade] {len(traders)} traders fetched")

    if not traders:
        safe_print("[whale-exit-fade] no traders from leaderboard. done.")
        return

    # Step 2: Fetch recent activity for each wallet
    all_activities: dict[str, list] = {}
    for t in traders:
        wallet = t.get("wallet", "")
        if not wallet:
            continue
        name = t.get("name", wallet[:12])
        activities = fetch_recent_activity(wallet, limit=100)
        if activities:
            all_activities[wallet] = activities
            safe_print(f"  [scan] {name}: {len(activities)} recent trades")
        else:
            safe_print(f"  [scan] {name}: no activity")

    if not all_activities:
        safe_print("[whale-exit-fade] no wallet activity found. done.")
        return

    # Step 3: Detect whale exits (multiple whales selling same market)
    safe_print(f"[whale-exit-fade] detecting exits in {EXIT_LOOKBACK_HOURS}h window...")
    exits = detect_whale_exits(all_activities, EXIT_LOOKBACK_HOURS)
    safe_print(f"[whale-exit-fade] {len(exits)} market exit events detected")

    if not exits:
        safe_print("[whale-exit-fade] no whale exit events found. done.")
        return

    # Step 4: Find fade opportunities (exits that meet thresholds + matching markets)
    safe_print("[whale-exit-fade] searching for fade opportunities...")
    opportunities = find_fade_opportunities(
        client, exits, MIN_EXIT_WHALES, MIN_EXIT_VOLUME
    )
    safe_print(f"[whale-exit-fade] {len(opportunities)} fade opportunities found")

    if not opportunities:
        safe_print("[whale-exit-fade] no actionable fade opportunities. done.")
        return

    # Step 5: Execute fade trades
    placed = 0
    for market, fade_direction, whale_count, exit_vol in opportunities:
        if placed >= MAX_POSITIONS:
            break

        # Use fade-enhanced signal
        side, size, reasoning = compute_fade_signal(
            market, fade_direction, whale_count, exit_vol
        )
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        # Context check
        ok, why = context_ok(client, market.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        # Execute trade
        try:
            r = client.trade(
                market_id=market.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:120]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {market.id}: {e}")

    safe_print(f"[whale-exit-fade] done. {placed} fade orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Whale exit fade trader -- fades panic selling after whale dumps."
    )
    ap.add_argument(
        "--live",
        action="store_true",
        help="Real trades on Polymarket. Default is paper (sim) mode.",
    )
    run(live=ap.parse_args().live)

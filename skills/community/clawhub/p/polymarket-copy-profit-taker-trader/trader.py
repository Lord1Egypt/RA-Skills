"""
polymarket-copy-profit-taker-trader
Mirrors whale take-profit behavior.  When a profitable whale starts REDUCING
exposure (selling parts of winning positions), it signals that smart money sees
the upside as limited.  This skill identifies those take-profit patterns and
avoids those markets, while finding NEW positions the whale is rotating INTO.

Core edge: Whales taking profit = upside exhausted.  Rotation targets = fresh
alpha.  By tracking sell-ratios across top wallets and detecting coordinated
rotations (exit market A, enter market B within a time window), the skill
follows the smart money flow from mature positions into fresh opportunities.

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

TRADE_SOURCE = "sdk:polymarket-copy-profit-taker-trader"
SKILL_SLUG   = "polymarket-copy-profit-taker-trader"

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
PROFIT_TAKE_THRESHOLD   = float(os.environ.get("SIMMER_PROFIT_TAKE_THRESHOLD",   "0.30"))
ROTATION_WINDOW_HOURS   = int(os.environ.get(  "SIMMER_ROTATION_WINDOW_HOURS",   "48"))
LEADERBOARD_LIMIT       = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",       "15"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Flush-safe print for cron/daemon environments."""
    print(*args, **kwargs, flush=True)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global PROFIT_TAKE_THRESHOLD, ROTATION_WINDOW_HOURS, LEADERBOARD_LIMIT
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
        MAX_POSITION            = float(os.environ.get("SIMMER_MAX_POSITION",           str(MAX_POSITION)))
        MIN_VOLUME              = float(os.environ.get("SIMMER_MIN_VOLUME",             str(MIN_VOLUME)))
        MAX_SPREAD              = float(os.environ.get("SIMMER_MAX_SPREAD",             str(MAX_SPREAD)))
        MIN_DAYS                = int(os.environ.get(  "SIMMER_MIN_DAYS",               str(MIN_DAYS)))
        MAX_POSITIONS           = int(os.environ.get(  "SIMMER_MAX_POSITIONS",          str(MAX_POSITIONS)))
        YES_THRESHOLD           = float(os.environ.get("SIMMER_YES_THRESHOLD",          str(YES_THRESHOLD)))
        NO_THRESHOLD            = float(os.environ.get("SIMMER_NO_THRESHOLD",           str(NO_THRESHOLD)))
        MIN_TRADE               = float(os.environ.get("SIMMER_MIN_TRADE",              str(MIN_TRADE)))
        PROFIT_TAKE_THRESHOLD   = float(os.environ.get("SIMMER_PROFIT_TAKE_THRESHOLD",  str(PROFIT_TAKE_THRESHOLD)))
        ROTATION_WINDOW_HOURS   = int(os.environ.get(  "SIMMER_ROTATION_WINDOW_HOURS",  str(ROTATION_WINDOW_HOURS)))
        LEADERBOARD_LIMIT       = int(os.environ.get(  "SIMMER_LEADERBOARD_LIMIT",      str(LEADERBOARD_LIMIT)))
    return _client


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: int = 15) -> dict | list | None:
    """Simple stdlib JSON GET request."""
    try:
        req = Request(url, headers={"User-Agent": "simmer-profit-taker/1.0"})
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

def fetch_wallet_activity(wallet: str, limit: int = 200) -> list[dict]:
    """Fetch recent trades for a wallet from data-api.

    Returns list of trade dicts with keys: wallet, side, market, title,
    timestamp, size, shares.
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
        shares = float(act.get("shares", act.get("outcomeTokens", size)))

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
            "shares": shares,
        })
    return trades


# ---------------------------------------------------------------------------
# Position change analysis
# ---------------------------------------------------------------------------

def analyze_position_changes(activities: list[dict]) -> list[tuple[str, str, float, float, float, str]]:
    """Track per (market, side): total bought shares, total sold shares, net.

    For positions where sold > 0:
      sell_ratio = sold / bought
      If sell_ratio >= PROFIT_TAKE_THRESHOLD -> whale is taking profit

    Returns:
        list of (market_title, side, buy_total, sell_total, sell_ratio, status)
        Status: "TAKING_PROFIT" | "ACCUMULATING" | "HOLDING"
    """
    now = datetime.now(timezone.utc)
    recent_cutoff = now - timedelta(hours=ROTATION_WINDOW_HOURS)

    # Group by (market_title, outcome_side)
    # outcome_side is the YES/NO side being traded, not buy/sell
    positions: dict[str, dict] = {}  # key = market_title

    for act in activities:
        title = act["title"]
        side = act["side"]
        shares = act.get("shares", act["size"])
        ts = act["timestamp"]

        if title not in positions:
            positions[title] = {
                "buy_total": 0.0,
                "sell_total": 0.0,
                "side": side,
                "recent_buys": 0,
                "last_buy_ts": None,
                "last_sell_ts": None,
            }

        pos = positions[title]

        if side in ("buy", "long", "yes"):
            pos["buy_total"] += shares
            if ts and ts > recent_cutoff:
                pos["recent_buys"] += 1
            if ts:
                if pos["last_buy_ts"] is None or ts > pos["last_buy_ts"]:
                    pos["last_buy_ts"] = ts
        elif side in ("sell", "short", "no"):
            pos["sell_total"] += shares
            if ts:
                if pos["last_sell_ts"] is None or ts > pos["last_sell_ts"]:
                    pos["last_sell_ts"] = ts

    results = []
    for title, pos in positions.items():
        buy_total = pos["buy_total"]
        sell_total = pos["sell_total"]

        if buy_total <= 0:
            continue

        sell_ratio = sell_total / buy_total

        if sell_ratio >= PROFIT_TAKE_THRESHOLD:
            status = "TAKING_PROFIT"
        elif sell_ratio < 0.1 and pos["recent_buys"] > 0:
            status = "ACCUMULATING"
        else:
            status = "HOLDING"

        results.append((title, pos["side"], buy_total, sell_total, sell_ratio, status))

    # Sort: TAKING_PROFIT first (highest sell_ratio), then ACCUMULATING
    status_order = {"TAKING_PROFIT": 0, "ACCUMULATING": 1, "HOLDING": 2}
    results.sort(key=lambda r: (status_order.get(r[5], 3), -r[4]))
    return results


# ---------------------------------------------------------------------------
# Rotation detection
# ---------------------------------------------------------------------------

def detect_rotations(
    all_wallet_positions: dict[str, list[tuple[str, str, float, float, float, str]]],
    rotation_window_hours: int,
) -> list[tuple[str, str, str, str, float]]:
    """Detect rotation patterns: whale exits market A AND enters market B.

    For each wallet: find markets where they're TAKING_PROFIT and markets
    where they're ACCUMULATING.  If same wallet does both within the
    rotation window -> rotation detected.

    Args:
        all_wallet_positions: wallet -> list of position change tuples
        rotation_window_hours: time window for rotation detection

    Returns:
        list of (wallet, exit_market, entry_market, entry_side, entry_conviction)
        entry_conviction = how much they're putting into the new position
                           relative to what they're taking out
    """
    rotations = []

    for wallet, positions in all_wallet_positions.items():
        exits = []
        entries = []

        for title, side, buy_total, sell_total, sell_ratio, status in positions:
            if status == "TAKING_PROFIT":
                exits.append((title, sell_total, sell_ratio))
            elif status == "ACCUMULATING":
                entries.append((title, side, buy_total))

        if not exits or not entries:
            continue

        # Each exit/entry pair is a potential rotation
        total_exit_value = sum(sell_total for _, sell_total, _ in exits)

        for exit_title, exit_sold, exit_ratio in exits:
            for entry_title, entry_side, entry_bought in entries:
                # entry_conviction: how much of the exit capital went to this entry
                if total_exit_value > 0:
                    entry_conviction = min(1.0, entry_bought / total_exit_value)
                else:
                    entry_conviction = 0.5

                rotations.append((
                    wallet,
                    exit_title,
                    entry_title,
                    entry_side,
                    round(entry_conviction, 3),
                ))

    # Sort by entry_conviction descending
    rotations.sort(key=lambda r: r[4], reverse=True)
    return rotations


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
# Rotation-boosted signal
# ---------------------------------------------------------------------------

def compute_rotation_signal(
    market,
    entry_side: str,
    rotation_conviction: float,
    num_rotating_whales: int,
) -> tuple[str | None, float, str]:
    """Conviction-based signal boosted by rotation pattern.

    Only trades if entry_side aligns with compute_signal direction.
    Rotation boost: rot_mult = 1 + min(0.4, rotation_conviction * 0.3
                                        + (num_rotating_whales - 1) * 0.1)
    """
    base_side, base_size, base_reasoning = compute_signal(market)

    # No base signal -> skip
    if base_side is None:
        return None, 0, f"No base signal: {base_reasoning}"

    # Normalize entry side
    entry_side_norm = "yes" if entry_side in ("buy", "long", "yes") else "no"
    if base_side != entry_side_norm:
        return None, 0, (
            f"Entry side '{entry_side_norm}' conflicts with base signal '{base_side}'"
        )

    p = market.current_probability
    q = market.question

    # Recompute conviction with rotation boost
    if base_side == "yes":
        base_conviction = (YES_THRESHOLD - p) / YES_THRESHOLD
    else:
        base_conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)

    rot_mult = 1 + min(0.4, rotation_conviction * 0.3 + (num_rotating_whales - 1) * 0.1)
    conviction = min(1.0, base_conviction * rot_mult)
    size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))

    return base_side, size, (
        f"{base_side.upper()} {p:.0%} rot_conv={rotation_conviction:.2f} "
        f"whales={num_rotating_whales} mult={rot_mult:.2f} "
        f"size=${size} -- Rotation target -- {q[:50]}"
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
    safe_print(f"\n{'='*68}")
    safe_print(f"  Profit-Taker Copytrader [{mode}]")
    safe_print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    safe_print(f"{'='*68}")

    client = get_client(live)

    # ---------------------------------------------------------------
    # Step 1: Fetch leaderboard
    # ---------------------------------------------------------------
    safe_print(f"\n[1/6] Fetching leaderboard (top {LEADERBOARD_LIMIT})...")
    traders = fetch_leaderboard(limit=LEADERBOARD_LIMIT)
    if not traders:
        safe_print("  No traders found on leaderboard. Exiting.")
        return

    # ---------------------------------------------------------------
    # Step 2: Fetch activity for each wallet
    # ---------------------------------------------------------------
    safe_print(f"\n[2/6] Fetching wallet activity...")
    all_activities: dict[str, list[dict]] = {}
    for i, t in enumerate(traders):
        wallet = (
            t.get("address")
            or t.get("wallet")
            or t.get("id", "unknown")
        )
        wallet = str(wallet)
        safe_print(f"  [{i+1}/{len(traders)}] {wallet[:12]}...")
        activities = fetch_wallet_activity(wallet, limit=200)
        if activities:
            all_activities[wallet] = activities
            safe_print(f"    -> {len(activities)} trades")
        else:
            safe_print(f"    -> no activity")

    if not all_activities:
        safe_print("  No wallet activity found. Exiting.")
        return

    # ---------------------------------------------------------------
    # Step 3: Analyze position changes per wallet
    # ---------------------------------------------------------------
    safe_print(f"\n[3/6] Analyzing position changes...")
    all_wallet_positions: dict[str, list[tuple[str, str, float, float, float, str]]] = {}
    for wallet, activities in all_activities.items():
        pos_changes = analyze_position_changes(activities)
        if pos_changes:
            all_wallet_positions[wallet] = pos_changes

    safe_print(f"  Wallets with position data: {len(all_wallet_positions)}")

    # ---------------------------------------------------------------
    # Step 4: Detect rotations across wallets
    # ---------------------------------------------------------------
    safe_print(f"\n[4/6] Detecting rotations (window={ROTATION_WINDOW_HOURS}h)...")
    rotations = detect_rotations(all_wallet_positions, ROTATION_WINDOW_HOURS)
    safe_print(f"  Rotations detected: {len(rotations)}")

    # ---------------------------------------------------------------
    # Dashboard A: Take-profit dashboard
    # ---------------------------------------------------------------
    safe_print(f"\n{'='*68}")
    safe_print(f"  TAKE-PROFIT DASHBOARD")
    safe_print(f"{'='*68}")
    safe_print(f"  {'Wallet':<14} | {'Market':<30} | {'SellRatio':>9} | {'Status':<15}")
    safe_print(f"  {'-'*14}-+-{'-'*30}-+-{'-'*9}-+-{'-'*15}")

    exit_markets: set[str] = set()
    for wallet, positions in all_wallet_positions.items():
        for title, side, buy_total, sell_total, sell_ratio, status in positions:
            if status == "TAKING_PROFIT":
                exit_markets.add(title)
                safe_print(
                    f"  {wallet[:14]:<14} | {title[:30]:<30} | "
                    f"{sell_ratio:>8.0%} | {status:<15}"
                )

    if not exit_markets:
        safe_print("  (no take-profit activity detected)")

    # ---------------------------------------------------------------
    # Dashboard B: Rotation dashboard
    # ---------------------------------------------------------------
    safe_print(f"\n{'='*68}")
    safe_print(f"  ROTATION DASHBOARD")
    safe_print(f"{'='*68}")
    safe_print(f"  {'Wallet':<14} | {'Exit Market':<22} | {'Entry Market':<22} | {'Side':<5}")
    safe_print(f"  {'-'*14}-+-{'-'*22}-+-{'-'*22}-+-{'-'*5}")

    for wallet, exit_mkt, entry_mkt, entry_side, entry_conv in rotations:
        safe_print(
            f"  {wallet[:14]:<14} | {exit_mkt[:22]:<22} | "
            f"{entry_mkt[:22]:<22} | {entry_side[:5]:<5}"
        )

    if not rotations:
        safe_print("  (no rotations detected)")

    # ---------------------------------------------------------------
    # Step 5: Trade rotation targets
    # ---------------------------------------------------------------
    safe_print(f"\n[5/6] Trading rotation targets...")

    if not context_ok(client):
        safe_print("\nAborted: portfolio context check failed.")
        return

    executed = 0
    skipped = 0
    seen_markets: set[str] = set()

    # Aggregate rotation data per entry market
    rotation_targets: dict[str, dict] = {}  # entry_market -> {entry_side, total_conv, num_whales, exit_markets}
    for wallet, exit_mkt, entry_mkt, entry_side, entry_conv in rotations:
        if entry_mkt not in rotation_targets:
            rotation_targets[entry_mkt] = {
                "entry_side": entry_side,
                "total_conviction": 0.0,
                "num_whales": 0,
                "exit_markets": set(),
            }
        rt = rotation_targets[entry_mkt]
        rt["total_conviction"] += entry_conv
        rt["num_whales"] += 1
        rt["exit_markets"].add(exit_mkt)

    for entry_title, rt in rotation_targets.items():
        if entry_title in seen_markets:
            continue
        seen_markets.add(entry_title)

        # Search for market in Simmer
        keywords = " ".join(entry_title.split()[:5])
        try:
            markets = client.find_markets(keywords)
        except Exception as exc:
            safe_print(f"  [WARN] Market search failed for '{keywords}': {exc}")
            continue

        if not markets:
            safe_print(f"  [SKIP] No Simmer market found for: {entry_title[:60]}")
            skipped += 1
            continue

        m = markets[0]

        # Volume gate
        vol = getattr(m, "volume", 0) or 0
        if vol < MIN_VOLUME:
            safe_print(f"  [SKIP] Low volume ${vol:.0f} < ${MIN_VOLUME:.0f}: {m.question[:60]}")
            skipped += 1
            continue

        avg_conviction = rt["total_conviction"] / max(1, rt["num_whales"])
        side, size, reasoning = compute_rotation_signal(
            m, rt["entry_side"], avg_conviction, rt["num_whales"]
        )

        if side is None:
            safe_print(f"  [SKIP] {reasoning}")
            skipped += 1
            continue

        exit_names = ", ".join(list(rt["exit_markets"])[:2])
        safe_print(f"  SIGNAL: {reasoning}")
        safe_print(f"    Rotation from: {exit_names[:60]}")

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

    # ---------------------------------------------------------------
    # Step 6: Standard signal fallback for non-exit markets
    # ---------------------------------------------------------------
    safe_print(f"\n[6/6] Checking standard signals (excluding exit markets)...")

    # Collect all accumulating markets across wallets that are NOT exit targets
    fallback_titles: set[str] = set()
    for wallet, positions in all_wallet_positions.items():
        for title, side, buy_total, sell_total, sell_ratio, status in positions:
            if status == "ACCUMULATING" and title not in exit_markets and title not in seen_markets:
                fallback_titles.add(title)

    for title in list(fallback_titles)[:10]:
        if title in seen_markets:
            continue
        seen_markets.add(title)

        keywords = " ".join(title.split()[:5])
        try:
            markets = client.find_markets(keywords)
        except Exception as exc:
            safe_print(f"  [WARN] Market search failed for '{keywords}': {exc}")
            continue

        if not markets:
            safe_print(f"  [SKIP] No Simmer market for: {title[:60]}")
            skipped += 1
            continue

        m = markets[0]
        vol = getattr(m, "volume", 0) or 0
        if vol < MIN_VOLUME:
            safe_print(f"  [SKIP] Low volume ${vol:.0f}: {m.question[:60]}")
            skipped += 1
            continue

        side, size, reasoning = compute_signal(m)
        if side is None:
            safe_print(f"  [SKIP] {reasoning}")
            skipped += 1
            continue

        if not context_ok(client):
            safe_print("  [GATE] Max positions reached, stopping fallback.")
            break

        safe_print(f"  SIGNAL (fallback): {reasoning}")
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

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    safe_print(f"\n{'='*68}")
    safe_print(f"  SUMMARY")
    safe_print(f"{'='*68}")
    safe_print(f"  Wallets scanned:      {len(all_activities)}")
    safe_print(f"  Take-profit markets:  {len(exit_markets)}")
    safe_print(f"  Rotations detected:   {len(rotations)}")
    safe_print(f"  Rotation targets:     {len(rotation_targets)}")
    safe_print(f"  Fallback candidates:  {len(fallback_titles)}")
    safe_print(f"  Trades executed:      {executed}")
    safe_print(f"  Trades skipped:       {skipped}")
    safe_print(f"{'='*68}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profit-Taker Copytrader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: paper)")
    args = parser.parse_args()
    run(live=args.live)

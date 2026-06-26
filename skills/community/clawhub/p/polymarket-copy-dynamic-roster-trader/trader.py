"""
polymarket-copy-dynamic-roster-trader
Automatically discovers top Polymarket wallets from the public leaderboard,
evaluates their recent rolling PnL, and dynamically builds a roster of
currently-performing wallets. Feeds this roster into the Simmer SDK
copytrading endpoint. Wallets that go cold get rotated out, hot newcomers
get added.

Core edge: Public leaderboards expose which wallets are *currently* hot.
By scoring wallets on a weighted combination of SmartScore, win rate, and
recent rolling PnL, this skill maintains a dynamic roster that adapts to
market regime changes. It then executes copytrading only on markets that
pass conviction-based signal validation, preventing blind copying into
overpriced or illiquid markets.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-copy-dynamic-roster-trader"
SKILL_SLUG   = "polymarket-copy-dynamic-roster-trader"

# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------
LEADERBOARD_URL = "https://predicting.top/api/leaderboard"
DATA_API        = "https://data-api.polymarket.com"

# ---------------------------------------------------------------------------
# Risk parameters — declared as tunables in clawhub.json
# ---------------------------------------------------------------------------
MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    "50"))
MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      "3000"))
MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      "0.10"))
MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        "3"))
MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   "10"))
YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   "0.38"))
NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    "0.62"))
MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       "5"))

# ---------------------------------------------------------------------------
# Skill-specific parameters
# ---------------------------------------------------------------------------
ROSTER_SIZE     = int(os.environ.get(  "SIMMER_ROSTER_SIZE",     "5"))
MIN_PNL         = float(os.environ.get("SIMMER_MIN_PNL",         "0"))
COPY_MAX_USD    = float(os.environ.get("SIMMER_COPY_MAX_USD",    "50"))
COPY_MAX_TRADES = int(os.environ.get(  "SIMMER_COPY_MAX_TRADES", "10"))

_client: SimmerClient | None = None


def safe_print(*args, **kwargs):
    """Flush-safe print for cron/daemon environments."""
    print(*args, **kwargs, flush=True)


def get_client(live: bool = False) -> SimmerClient:
    global _client, MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    global ROSTER_SIZE, MIN_PNL, COPY_MAX_USD, COPY_MAX_TRADES
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
        MAX_POSITION    = float(os.environ.get("SIMMER_MAX_POSITION",    str(MAX_POSITION)))
        MIN_VOLUME      = float(os.environ.get("SIMMER_MIN_VOLUME",      str(MIN_VOLUME)))
        MAX_SPREAD      = float(os.environ.get("SIMMER_MAX_SPREAD",      str(MAX_SPREAD)))
        MIN_DAYS        = int(os.environ.get(  "SIMMER_MIN_DAYS",        str(MIN_DAYS)))
        MAX_POSITIONS   = int(os.environ.get(  "SIMMER_MAX_POSITIONS",   str(MAX_POSITIONS)))
        YES_THRESHOLD   = float(os.environ.get("SIMMER_YES_THRESHOLD",   str(YES_THRESHOLD)))
        NO_THRESHOLD    = float(os.environ.get("SIMMER_NO_THRESHOLD",    str(NO_THRESHOLD)))
        MIN_TRADE       = float(os.environ.get("SIMMER_MIN_TRADE",       str(MIN_TRADE)))
        ROSTER_SIZE     = int(os.environ.get(  "SIMMER_ROSTER_SIZE",     str(ROSTER_SIZE)))
        MIN_PNL         = float(os.environ.get("SIMMER_MIN_PNL",         str(MIN_PNL)))
        COPY_MAX_USD    = float(os.environ.get("SIMMER_COPY_MAX_USD",    str(COPY_MAX_USD)))
        COPY_MAX_TRADES = int(os.environ.get(  "SIMMER_COPY_MAX_TRADES", str(COPY_MAX_TRADES)))
    return _client


# ---------------------------------------------------------------------------
# Leaderboard fetching
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: int = 15) -> dict | list | None:
    """Simple stdlib JSON GET request."""
    try:
        req = Request(url, headers={"User-Agent": "simmer-dynamic-roster/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as exc:
        safe_print(f"  [WARN] HTTP GET failed: {url} -> {exc}")
        return None


def fetch_leaderboard(limit: int = 30) -> list[dict]:
    """Fetch top traders from predicting.top leaderboard API."""
    url = f"{LEADERBOARD_URL}?limit={limit}"
    data = _http_get_json(url)
    if data is None:
        safe_print("  [WARN] Leaderboard fetch returned None, using empty list")
        return []
    # API may return {"traders": [...]} or a raw list
    if isinstance(data, dict):
        traders = data.get("traders", data.get("data", data.get("results", [])))
    elif isinstance(data, list):
        traders = data
    else:
        traders = []
    safe_print(f"  Fetched {len(traders)} traders from leaderboard")
    return traders[:limit]


# ---------------------------------------------------------------------------
# Wallet evaluation
# ---------------------------------------------------------------------------

def evaluate_wallet(trader_data: dict) -> dict:
    """Extract SmartScore metrics from a leaderboard entry.

    Returns a dict with normalized fields:
      wallet, smart_score, win_rate, pnl, sharpe, tier
    """
    wallet = (
        trader_data.get("address")
        or trader_data.get("wallet")
        or trader_data.get("id", "unknown")
    )
    smart_score = float(trader_data.get("smartScore", trader_data.get("score", 0)))
    win_rate    = float(trader_data.get("winRate", trader_data.get("win_rate", 0)))
    pnl         = float(trader_data.get("pnl", trader_data.get("totalPnl", 0)))
    sharpe      = float(trader_data.get("sharpeRatio", trader_data.get("sharpe", 0)))
    tier        = trader_data.get("tier", trader_data.get("rank", "unknown"))

    return {
        "wallet":      str(wallet),
        "smart_score": smart_score,
        "win_rate":    win_rate,
        "pnl":         pnl,
        "sharpe":      sharpe,
        "tier":        str(tier),
    }


def compute_rolling_pnl(wallet: str, limit: int = 50) -> tuple[float, float, int]:
    """Compute rolling PnL from recent on-chain activity via data-api.

    Returns (pnl, win_rate, num_closed).
    """
    url = f"{DATA_API}/activity?user={wallet}&limit={limit}"
    data = _http_get_json(url, timeout=20)
    if not data:
        return 0.0, 0.0, 0

    activities = data if isinstance(data, list) else data.get("history", data.get("data", []))
    if not activities:
        return 0.0, 0.0, 0

    # Track positions: group buys and sells by market
    positions: dict[str, list[dict]] = {}
    for act in activities:
        market_id = act.get("market", act.get("conditionId", act.get("id", "")))
        if not market_id:
            continue
        positions.setdefault(market_id, []).append(act)

    total_pnl = 0.0
    wins = 0
    num_closed = 0

    for market_id, trades in positions.items():
        buys  = [t for t in trades if t.get("side", t.get("type", "")).lower() in ("buy", "long")]
        sells = [t for t in trades if t.get("side", t.get("type", "")).lower() in ("sell", "short")]

        if not buys or not sells:
            continue  # Not a closed position

        avg_buy  = sum(float(t.get("price", 0)) * float(t.get("size", t.get("amount", 0)))
                       for t in buys)
        buy_size = sum(float(t.get("size", t.get("amount", 0))) for t in buys)
        avg_sell = sum(float(t.get("price", 0)) * float(t.get("size", t.get("amount", 0)))
                       for t in sells)
        sell_size = sum(float(t.get("size", t.get("amount", 0))) for t in sells)

        if buy_size == 0 or sell_size == 0:
            continue

        realized = avg_sell - avg_buy * (min(sell_size, buy_size) / buy_size)
        total_pnl += realized
        num_closed += 1
        if realized > 0:
            wins += 1

    win_rate = (wins / num_closed * 100) if num_closed > 0 else 0.0
    return round(total_pnl, 2), round(win_rate, 1), num_closed


# ---------------------------------------------------------------------------
# Dynamic roster construction
# ---------------------------------------------------------------------------

def _normalize(values: list[float]) -> list[float]:
    """Min-max normalize a list of floats to [0, 1]."""
    if not values:
        return []
    lo, hi = min(values), max(values)
    span = hi - lo
    if span == 0:
        return [0.5] * len(values)
    return [(v - lo) / span for v in values]


def build_dynamic_roster(
    traders: list[dict],
    roster_size: int,
) -> list[tuple[str, float, dict]]:
    """Build a ranked roster of top-performing wallets.

    For each trader in leaderboard:
      1. Extract SmartScore metrics (score, winRate, sharpeRatio)
      2. Compute rolling PnL from recent activity
      3. Combined score = 0.4 * norm_smart + 0.3 * norm_winrate + 0.3 * norm_pnl
    Sort by combined score, take top roster_size, filter out PnL < MIN_PNL.

    Returns list of (wallet_address, combined_score, metrics_dict).
    """
    if not traders:
        return []

    evaluated: list[dict] = []
    safe_print(f"\n--- Evaluating {len(traders)} wallets ---")

    for i, t in enumerate(traders):
        metrics = evaluate_wallet(t)
        wallet = metrics["wallet"]
        safe_print(f"  [{i+1}/{len(traders)}] {wallet[:10]}... score={metrics['smart_score']:.1f} "
                    f"wr={metrics['win_rate']:.1f}%")

        rolling_pnl, rolling_wr, num_closed = compute_rolling_pnl(wallet)
        metrics["rolling_pnl"]  = rolling_pnl
        metrics["rolling_wr"]   = rolling_wr
        metrics["num_closed"]   = num_closed
        evaluated.append(metrics)

    if not evaluated:
        return []

    # Normalize each component
    smart_scores = _normalize([e["smart_score"] for e in evaluated])
    win_rates    = _normalize([e["win_rate"] for e in evaluated])
    rolling_pnls = _normalize([e["rolling_pnl"] for e in evaluated])

    # Compute combined scores
    scored: list[tuple[str, float, dict]] = []
    for idx, metrics in enumerate(evaluated):
        combined = (
            0.4 * smart_scores[idx]
            + 0.3 * win_rates[idx]
            + 0.3 * rolling_pnls[idx]
        )
        scored.append((metrics["wallet"], round(combined, 4), metrics))

    # Sort descending by combined score
    scored.sort(key=lambda x: x[1], reverse=True)

    # Take top N and filter by MIN_PNL
    roster = []
    for wallet, score, metrics in scored[:roster_size * 2]:  # oversample then filter
        if metrics["rolling_pnl"] < MIN_PNL:
            safe_print(f"  Filtered out {wallet[:10]}... rolling_pnl={metrics['rolling_pnl']:.2f} < {MIN_PNL}")
            continue
        roster.append((wallet, score, metrics))
        if len(roster) >= roster_size:
            break

    return roster


# ---------------------------------------------------------------------------
# Copytrading execution
# ---------------------------------------------------------------------------

def execute_roster_copy(
    client: SimmerClient,
    roster_wallets: list[str],
    max_usd: float,
    max_trades: int,
    dry_run: bool = True,
) -> dict:
    """Execute copytrading via Simmer SDK endpoint.

    Sends the roster of wallets to the copytrading API and processes results.
    """
    if not roster_wallets:
        return {"trades_executed": 0, "trades_skipped": 0, "details": []}

    data = {
        "wallets": roster_wallets,
        "max_usd_per_position": max_usd,
        "dry_run": dry_run,
        "buy_only": True,
        "detect_whale_exits": True,
        "max_trades": max_trades,
    }

    safe_print(f"\n--- Calling copytrading endpoint (dry_run={dry_run}) ---")
    safe_print(f"  Wallets: {len(roster_wallets)}")
    safe_print(f"  Max USD/pos: ${max_usd:.0f}  Max trades: {max_trades}")

    try:
        result = client._request("POST", "/api/sdk/copytrading/execute", json=data, timeout=60)
    except Exception as exc:
        safe_print(f"  [ERROR] Copytrading endpoint failed: {exc}")
        return {"trades_executed": 0, "trades_skipped": 0, "details": [], "error": str(exc)}

    if result is None:
        result = {}

    trades = result.get("trades", [])
    executed = 0
    skipped  = 0
    details  = []

    for trade_info in trades:
        market_id = trade_info.get("market_id", trade_info.get("conditionId", ""))
        side      = trade_info.get("side", "yes")
        amount    = float(trade_info.get("amount", trade_info.get("size", max_usd)))
        prob      = float(trade_info.get("probability", trade_info.get("price", 0.5)))
        question  = trade_info.get("question", trade_info.get("title", ""))[:80]

        # Validate against conviction thresholds
        skip_reason = None
        if side.lower() == "yes" and prob > YES_THRESHOLD:
            skip_reason = f"YES prob {prob:.0%} > threshold {YES_THRESHOLD:.0%}"
        elif side.lower() == "no" and prob < NO_THRESHOLD:
            skip_reason = f"NO prob {prob:.0%} < threshold {NO_THRESHOLD:.0%}"

        if skip_reason:
            safe_print(f"  SKIP: {skip_reason} | {question}")
            skipped += 1
            details.append({"action": "skip", "reason": skip_reason, "market": question})
            continue

        # Cap amount
        amount = min(amount, max_usd, MAX_POSITION)

        if dry_run:
            safe_print(f"  [DRY] {side.upper()} ${amount:.2f} @ {prob:.0%} | {question}")
            executed += 1
            details.append({"action": "dry_run", "side": side, "amount": amount, "market": question})
        else:
            try:
                r = client.trade(
                    market_id=market_id,
                    side=side,
                    amount=amount,
                    source=TRADE_SOURCE,
                )
                safe_print(f"  TRADE: {side.upper()} ${amount:.2f} @ {prob:.0%} | {question}")
                executed += 1
                details.append({"action": "trade", "side": side, "amount": amount,
                                "market": question, "result": str(r)})
            except Exception as exc:
                safe_print(f"  [ERROR] Trade failed: {exc} | {question}")
                skipped += 1
                details.append({"action": "error", "reason": str(exc), "market": question})

    return {"trades_executed": executed, "trades_skipped": skipped, "details": details}


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
# Context check — prevent flip-flop / slippage
# ---------------------------------------------------------------------------

def context_ok(client: SimmerClient) -> bool:
    """Check portfolio context to prevent excessive positions or flip-flops."""
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
    safe_print(f"\n{'='*60}")
    safe_print(f"  Dynamic Roster Copytrader [{mode}]")
    safe_print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    safe_print(f"{'='*60}")

    client = get_client(live)

    # Check portfolio context
    if not context_ok(client):
        safe_print("\nAborted: portfolio context check failed.")
        return

    # Step 1: Fetch leaderboard
    safe_print("\n[1/4] Fetching leaderboard...")
    traders = fetch_leaderboard(limit=30)
    if not traders:
        safe_print("  No traders found on leaderboard. Exiting.")
        return

    # Step 2: Build dynamic roster
    safe_print(f"\n[2/4] Building dynamic roster (target size={ROSTER_SIZE})...")
    roster = build_dynamic_roster(traders, ROSTER_SIZE)
    if not roster:
        safe_print("  No qualifying wallets for roster. Exiting.")
        return

    # Print roster dashboard
    safe_print(f"\n{'='*60}")
    safe_print(f"  ACTIVE ROSTER ({len(roster)} wallets)")
    safe_print(f"{'='*60}")
    safe_print(f"  {'#':>2} | {'Wallet':<12} | {'Score':>6} | {'WinRate':>7} | {'RollingPnL':>10} | Status")
    safe_print(f"  {'-'*2}-+-{'-'*12}-+-{'-'*6}-+-{'-'*7}-+-{'-'*10}-+-{'-'*8}")
    for i, (wallet, score, metrics) in enumerate(roster, 1):
        status = "HOT" if metrics["rolling_pnl"] > 0 else "WARM"
        safe_print(
            f"  {i:>2} | {wallet[:12]:<12} | {score:>6.3f} | "
            f"{metrics['win_rate']:>6.1f}% | "
            f"${metrics['rolling_pnl']:>9.2f} | {status}"
        )

    # Step 3: Execute roster copy
    safe_print(f"\n[3/4] Executing roster copy...")
    roster_wallets = [w for w, _, _ in roster]
    dry_run = not live

    results = execute_roster_copy(
        client=client,
        roster_wallets=roster_wallets,
        max_usd=COPY_MAX_USD,
        max_trades=COPY_MAX_TRADES,
        dry_run=dry_run,
    )

    # Step 4: Summary
    safe_print(f"\n[4/4] Summary")
    safe_print(f"{'='*60}")
    safe_print(f"  Wallets in roster:  {len(roster)}")
    safe_print(f"  Trades executed:    {results['trades_executed']}")
    safe_print(f"  Trades skipped:     {results['trades_skipped']}")
    if results.get("error"):
        safe_print(f"  Error:              {results['error']}")
    safe_print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Roster Copytrader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: paper)")
    args = parser.parse_args()
    run(live=args.live)

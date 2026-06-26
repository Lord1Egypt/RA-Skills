#!/usr/bin/env python3
"""
Kalshi F1 Elimination Trader

Trades F1 Drivers Championship markets on Kalshi by identifying
mathematically eliminated drivers. When a driver cannot catch the
championship leader even with maximum points in all remaining races,
their championship probability is effectively zero -- yet markets
often still price them above 0.

This skill sells NO on eliminated drivers still priced > 0,
capturing guaranteed edge from structural market inefficiency.

Usage:
    python trader.py              # Dry run (show opportunities, no trades)
    python trader.py --live       # Execute real trades via DFlow/Solana
    python trader.py --positions  # Show current positions only
    python trader.py --config     # Show current configuration

Requires:
    SIMMER_API_KEY environment variable (get from simmer.markets/dashboard)
    SOLANA_PRIVATE_KEY environment variable (base58-encoded, for live trading)
"""

import os
import sys
import json
import math
import argparse
from datetime import datetime, timezone

# Force line-buffered stdout for non-TTY environments (cron, Docker, automaton)
sys.stdout.reconfigure(line_buffering=True)

# Optional: Trade Journal integration
try:
    from tradejournal import log_trade
    JOURNAL_AVAILABLE = True
except ImportError:
    try:
        from skills.tradejournal import log_trade
        JOURNAL_AVAILABLE = True
    except ImportError:
        JOURNAL_AVAILABLE = False
        def log_trade(*args, **kwargs):
            pass

# =============================================================================
# Configuration
# =============================================================================

from simmer_sdk.skill import load_config, update_config, get_config_path

CONFIG_SCHEMA = {
    "entry_edge":        {"env": "SIMMER_F1_ELIM_ENTRY_EDGE",        "default": 0.03,  "type": float},
    "exit_threshold":    {"env": "SIMMER_F1_ELIM_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_F1_ELIM_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_F1_ELIM_MAX_TRADES_PER_RUN","default": 5,     "type": int},
    "slippage_max":      {"env": "SIMMER_F1_ELIM_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_F1_ELIM_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-f1-elimination-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-f1-elim"
SKILL_SLUG = "kalshi-f1-elimination-trader"
_automaton_reported = False

# Kalshi constraints
MIN_SHARES_PER_ORDER = 1.0

# Strategy parameters from config
ENTRY_EDGE = _config["entry_edge"]
EXIT_THRESHOLD = _config["exit_threshold"]
MAX_POSITION_USD = _config["max_position_usd"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max:
    MAX_POSITION_USD = min(MAX_POSITION_USD, float(_automaton_max))

MAX_TRADES_PER_RUN = _config["max_trades_per_run"]
SLIPPAGE_MAX_PCT = _config["slippage_max"]
MIN_LIQUIDITY_USD = _config["min_liquidity"]
TIME_TO_RESOLUTION_MIN_HOURS = 2

# =============================================================================
# F1 Elimination Model
# =============================================================================

# Maximum points a driver can score per race weekend
# 25 (win) + 1 (fastest lap) = 26
MAX_POINTS_PER_RACE = 26

# Total number of races in the 2025 F1 season
TOTAL_RACES_2025 = 24

# Current championship standings (update periodically)
# Format: driver -> {"points": int, "races_completed": int}
CHAMPIONSHIP_STANDINGS = {
    "verstappen": {"points": 136, "position": 1},
    "norris":     {"points": 120, "position": 2},
    "leclerc":    {"points": 97,  "position": 3},
    "piastri":    {"points": 86,  "position": 4},
    "hamilton":   {"points": 64,  "position": 5},
    "russell":    {"points": 54,  "position": 6},
    "alonso":     {"points": 32,  "position": 7},
    "lawson":     {"points": 18,  "position": 8},
    "antonelli":  {"points": 12,  "position": 9},
    "stroll":     {"points": 8,   "position": 10},
    "tsunoda":    {"points": 6,   "position": 11},
    "gasly":      {"points": 4,   "position": 12},
    "hulkenberg": {"points": 3,   "position": 13},
    "ocon":       {"points": 2,   "position": 14},
    "bearman":    {"points": 1,   "position": 15},
    "colapinto":  {"points": 0,   "position": 16},
    "doohan":     {"points": 0,   "position": 17},
    "hadjar":     {"points": 0,   "position": 18},
    "bortoleto":  {"points": 0,   "position": 19},
    "drugovich":  {"points": 0,   "position": 20},
}

# Number of races completed so far
RACES_COMPLETED = 5

# Driver name aliases for market question parsing
DRIVER_ALIASES = {
    "max verstappen": "verstappen",
    "lando norris": "norris",
    "charles leclerc": "leclerc",
    "lewis hamilton": "hamilton",
    "george russell": "russell",
    "oscar piastri": "piastri",
    "fernando alonso": "alonso",
    "lance stroll": "stroll",
    "liam lawson": "lawson",
    "kimi antonelli": "antonelli",
    "andrea kimi antonelli": "antonelli",
    "yuki tsunoda": "tsunoda",
    "pierre gasly": "gasly",
    "nico hulkenberg": "hulkenberg",
    "esteban ocon": "ocon",
    "oliver bearman": "bearman",
    "franco colapinto": "colapinto",
    "jack doohan": "doohan",
    "isack hadjar": "hadjar",
    "gabriel bortoleto": "bortoleto",
    "felipe drugovich": "drugovich",
}


def compute_elimination_status() -> dict:
    """Determine which drivers are mathematically eliminated.

    A driver is eliminated if their maximum possible points
    (current points + MAX_POINTS_PER_RACE * remaining races)
    is less than the current leader's points.

    Returns dict: driver -> {"eliminated": bool, "max_possible": int,
                              "leader_gap": int, "deficit": int}
    """
    remaining_races = TOTAL_RACES_2025 - RACES_COMPLETED

    # Find leader points
    leader_points = max(s["points"] for s in CHAMPIONSHIP_STANDINGS.values())

    results = {}
    for driver, standing in CHAMPIONSHIP_STANDINGS.items():
        current = standing["points"]
        max_possible = current + (MAX_POINTS_PER_RACE * remaining_races)
        gap = leader_points - current
        deficit = leader_points - max_possible  # positive = eliminated

        results[driver] = {
            "eliminated": max_possible < leader_points,
            "current_points": current,
            "max_possible": max_possible,
            "leader_gap": gap,
            "deficit": max(0, deficit),
            "remaining_races": remaining_races,
        }
    return results


# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def extract_driver(question: str) -> str | None:
    """Extract driver name from a market question string."""
    q = question.lower()
    for alias, driver in sorted(DRIVER_ALIASES.items(), key=lambda x: -len(x[0])):
        if alias in q:
            return driver
    for driver in CHAMPIONSHIP_STANDINGS:
        if driver in q:
            return driver
    return None


def is_f1_championship_market(question: str) -> bool:
    """Check if a market question is about F1 drivers championship."""
    q = question.lower()
    f1_terms = ["f1", "formula 1", "formula one", "drivers championship",
                "driver championship", "world drivers"]
    return any(term in q for term in f1_terms)


# =============================================================================
# Simmer Client
# =============================================================================

def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "kalshi")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover F1 championship markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["F1", "drivers championship", "Formula 1 champion"]:
        try:
            results = client.list_importable_markets(
                q=term, venue="kalshi", limit=20, min_volume=0
            )
        except Exception as e:
            if "429" in str(e):
                log("  Rate limit reached -- stopping discovery")
                return imported
            log(f"  Discovery failed for '{term}': {e}")
            continue

        for m in results:
            url = m.get("url", "")
            question = (m.get("question") or "").lower()
            if not url or url in seen:
                continue
            seen.add(url)
            if not is_f1_championship_market(question):
                continue
            try:
                result = client.import_kalshi_market(url)
                status = result.get("status", "") if result else ""
                if status == "imported":
                    imported += 1
                    log(f"  Imported: {m.get('question', url)[:70]}")
            except Exception as e:
                if "rate limit" in str(e).lower() or "429" in str(e):
                    log("  Rate limit reached -- stopping discovery")
                    return imported

    return imported


def fetch_f1_markets():
    """Fetch active F1 championship markets from Simmer API."""
    try:
        all_markets = []
        for query in ["F1", "drivers championship"]:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": query, "limit": 50}
            )
            markets = result.get("markets", [])
            all_markets.extend(markets)

        seen_ids = set()
        unique = []
        for m in all_markets:
            mid = m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                if is_f1_championship_market(m.get("question", "")):
                    unique.append(m)
        return unique
    except Exception as e:
        safe_print(f"  Failed to fetch markets: {e}")
        return []


# =============================================================================
# Context & Safeguards
# =============================================================================

def get_market_context(market_id: str, my_probability: float = None) -> dict:
    """Get market context with safeguards and edge analysis."""
    try:
        if my_probability is not None:
            return get_client()._request(
                "GET", f"/api/sdk/context/{market_id}",
                params={"my_probability": my_probability}
            )
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def check_safeguards(context: dict) -> tuple[bool, list[str]]:
    """Check context for safeguards. Returns (should_trade, reasons)."""
    if not context:
        return True, []

    reasons = []
    market = context.get("market", {})
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})
    slippage = context.get("slippage", {})

    for w in warnings:
        if "MARKET RESOLVED" in str(w).upper():
            return False, ["Market already resolved"]

    level = discipline.get("warning_level", "none")
    if level == "severe":
        return False, [f"Severe flip-flop: {discipline.get('flip_flop_warning', '')}"]
    elif level == "mild":
        reasons.append("Mild flip-flop warning")

    time_str = market.get("time_to_resolution", "")
    if time_str:
        try:
            hours = 0
            if "d" in time_str:
                hours += int(time_str.split("d")[0].strip()) * 24
            if "h" in time_str:
                h_part = time_str.split("h")[0]
                if "d" in h_part:
                    h_part = h_part.split("d")[-1].strip()
                hours += int(h_part)
            if hours < TIME_TO_RESOLUTION_MIN_HOURS:
                return False, [f"Resolves in {hours}h -- too soon"]
        except (ValueError, IndexError):
            pass

    if MIN_LIQUIDITY_USD > 0:
        liquidity = market.get("liquidity", 0) or 0
        if liquidity < MIN_LIQUIDITY_USD:
            return False, [f"Low liquidity: ${liquidity:.0f}"]

    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slip = estimates[0].get("slippage_pct", 0)
        if slip > SLIPPAGE_MAX_PCT:
            return False, [f"Slippage {slip:.1%} > max {SLIPPAGE_MAX_PCT:.0%}"]

    return True, reasons


# =============================================================================
# Trade Execution
# =============================================================================

def execute_trade(market_id: str, side: str, amount: float,
                  reasoning: str = "", signal_data: dict = None) -> dict:
    """Execute a trade via Simmer SDK with source tagging."""
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
            reasoning=reasoning, signal_data=signal_data,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}


def get_positions():
    """Get current open positions."""
    try:
        result = get_client()._request("GET", "/api/sdk/positions")
        return result.get("positions", []) if isinstance(result, dict) else result
    except Exception:
        return []


def check_exits(dry_run: bool, log=print) -> tuple[int, int]:
    """Check open F1 elimination positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    f1_positions = [p for p in positions
                    if TRADE_SOURCE in p.get("sources", [])
                    or is_f1_championship_market(p.get("question", ""))]

    if not f1_positions:
        return 0, 0

    log(f"\n  Checking {len(f1_positions)} F1 elimination positions for exit...")
    found, executed = 0, 0

    for pos in f1_positions:
        market_id = pos.get("market_id")
        price = pos.get("current_price") or pos.get("price_yes") or 0
        shares = pos.get("shares_yes") or pos.get("shares") or 0
        question = pos.get("question", "")[:50]

        if shares < MIN_SHARES_PER_ORDER:
            continue

        if price >= EXIT_THRESHOLD:
            found += 1
            log(f"  EXIT: {question}  price={price:.2f} >= {EXIT_THRESHOLD:.2f}")

            ctx = get_market_context(market_id)
            ok, reasons = check_safeguards(ctx)
            if not ok:
                log(f"    Skipped: {'; '.join(reasons)}")
                continue

            if not dry_run:
                result = execute_trade(
                    market_id, "sell", shares,
                    reasoning=f"Exit: price {price:.2f} >= threshold {EXIT_THRESHOLD:.2f}",
                )
                if result.get("success"):
                    executed += 1
                    tag = "[PAPER] " if result.get("simulated") else ""
                    log(f"    {tag}Sold {shares:.1f} @ {price:.2f}")
                    if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                        log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                                  skill_slug=SKILL_SLUG, thesis="Exit on threshold", action="sell")
                else:
                    log(f"    Sell failed: {result.get('error')}")
            else:
                log(f"    [DRY RUN] Would sell {shares:.1f} shares")

    return found, executed


# =============================================================================
# Main Strategy
# =============================================================================

def run_strategy(dry_run: bool = True, positions_only: bool = False,
                 show_config: bool = False, quiet: bool = False):
    """Run the F1 elimination trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("F1 Elimination Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Max points/race: {MAX_POINTS_PER_RACE}  Races completed: {RACES_COMPLETED}/{TOTAL_RACES_2025}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        f1 = [p for p in positions if is_f1_championship_market(p.get("question", ""))]
        if not f1:
            log("  No F1 championship positions")
        for p in f1:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Elimination Analysis ---
    remaining_races = TOTAL_RACES_2025 - RACES_COMPLETED
    elim_status = compute_elimination_status()

    log("Championship Standings & Elimination Status:")
    leader_points = max(s["points"] for s in CHAMPIONSHIP_STANDINGS.values())
    for driver, status in sorted(elim_status.items(),
                                  key=lambda x: -x[1]["current_points"]):
        pts = status["current_points"]
        max_p = status["max_possible"]
        tag = " ** ELIMINATED **" if status["eliminated"] else ""
        log(f"  {driver:>15}: {pts:4d}pts  max_possible={max_p:4d}  "
            f"gap={status['leader_gap']:+4d}{tag}")

    eliminated = {d for d, s in elim_status.items() if s["eliminated"]}
    log(f"\n  Eliminated drivers: {len(eliminated)}")
    log(f"  Remaining races: {remaining_races}")
    log("")

    # --- Discovery ---
    log("Discovering F1 championship markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_f1_markets()
    log(f"  Found {len(markets)} active F1 championship markets")

    if not markets:
        log("  No F1 championship markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        driver = extract_driver(question)
        if not driver:
            log(f"  ? Unknown driver: {question[:60]}")
            continue

        status = elim_status.get(driver)
        if not status:
            log(f"  ? No standings data for: {driver}")
            continue

        if not status["eliminated"]:
            log(f"  {driver:>15}: NOT eliminated (pts={status['current_points']}, "
                f"max={status['max_possible']}, leader={leader_points})")
            continue

        # Driver is eliminated -- their fair value is 0
        # If market prices them > ENTRY_EDGE, sell NO (buy NO = bet they won't win)
        if price > ENTRY_EDGE:
            edge = price  # edge = market_price - 0 (fair value)
            signals += 1

            # Conviction-based sizing: higher price = more conviction
            raw_conv = min(edge / ENTRY_EDGE, 2.0) / 2.0
            size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

            log(f"  {driver:>15}: ELIMINATED but market={price:.1%}  "
                f"edge={edge:.1%}  size=${size:.2f}")
            log(f"    -> BUY NO: driver mathematically eliminated, "
                f"deficit={status['deficit']}pts")

            if trades_executed >= MAX_TRADES_PER_RUN:
                log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
                skip_reasons.append("max_trades")
                continue

            # Safeguards
            ctx = get_market_context(market_id, my_probability=0.0)
            ok, reasons = check_safeguards(ctx)
            if not ok:
                log(f"    Skipped: {'; '.join(reasons)}")
                skip_reasons.extend(reasons)
                continue
            if reasons:
                log(f"    Warnings: {'; '.join(reasons)}")

            if not dry_run:
                result = execute_trade(
                    market_id, "no", size,
                    reasoning=(f"Elimination: {driver} eliminated "
                               f"(deficit={status['deficit']}pts, "
                               f"{remaining_races} races left) "
                               f"but market={price:.1%}"),
                    signal_data={"driver": driver, "eliminated": True,
                                 "current_points": status["current_points"],
                                 "max_possible": status["max_possible"],
                                 "deficit": status["deficit"],
                                 "market_price": round(price, 4)},
                )
                if result.get("success"):
                    trades_executed += 1
                    total_usd += size
                    tag = "[PAPER] " if result.get("simulated") else ""
                    log(f"    {tag}Bought NO ${size:.2f}", force=True)
                    if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                        log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                                  skill_slug=SKILL_SLUG,
                                  thesis=f"Eliminated driver: {driver}", action="buy")
                else:
                    log(f"    Trade failed: {result.get('error')}", force=True)
            else:
                log(f"    [DRY RUN] Would buy NO ${size:.2f}")
                trades_executed += 1
                total_usd += size
        else:
            log(f"  {driver:>15}: eliminated, market={price:.1%} (below edge threshold)")

    # --- Exits ---
    exits_found, exits_exec = check_exits(dry_run, log=log)

    # --- Summary ---
    log(f"\n  Signals: {signals}  Trades: {trades_executed}  USD: ${total_usd:.2f}")
    if exits_found:
        log(f"  Exits: {exits_found} found, {exits_exec} executed")

    # --- Automaton report ---
    if os.environ.get("AUTOMATON_MANAGED"):
        _automaton_reported = True
        report = {
            "signals": signals + exits_found,
            "trades_attempted": signals + exits_found,
            "trades_executed": trades_executed + exits_exec,
            "amount_usd": round(total_usd, 2),
        }
        if signals > 0 and trades_executed == 0 and skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        print(json.dumps({"automaton": report}))


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kalshi F1 Elimination Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set entry_edge=0.05)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Only output on trades/errors")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, val = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    updates[key] = CONFIG_SCHEMA[key]["type"](val)
        if updates:
            update_config(updates, __file__)
            safe_print(f"Updated config: {updates}")

    dry_run = not args.live
    run_strategy(dry_run, args.positions, args.config, args.quiet)

    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                        "skip_reason": "no_signal"}}))

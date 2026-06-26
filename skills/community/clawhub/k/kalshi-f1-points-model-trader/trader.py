#!/usr/bin/env python3
"""
Kalshi F1 Points Model Trader

Trades F1 Drivers Championship winner markets on Kalshi using current points
standings to Monte Carlo simulate remaining races. Computes championship win
probability per driver and trades when market diverges from simulation.

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
import random
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
    "entry_edge":        {"env": "SIMMER_F1_PTS_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_F1_PTS_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_F1_PTS_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_F1_PTS_MAX_TRADES_PER_RUN","default": 5,     "type": int},
    "slippage_max":      {"env": "SIMMER_F1_PTS_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_F1_PTS_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-f1-points-model-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-f1-points"
SKILL_SLUG = "kalshi-f1-points-model-trader"
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
# F1 Points Standings — update periodically from official F1 results
# =============================================================================

# 2025 F1 Drivers Championship standings (update after each race)
CURRENT_STANDINGS = {
    "verstappen":   51,
    "norris":       42,
    "leclerc":      39,
    "piastri":      30,
    "hamilton":     26,
    "russell":      22,
    "antonelli":    12,
    "lawson":        6,
    "alonso":        4,
    "gasly":         2,
    "tsunoda":       1,
    "hulkenberg":    0,
    "stroll":        0,
    "colapinto":     0,
    "bearman":       0,
    "ocon":          0,
    "bottas":        0,
    "zhou":          0,
    "doohan":        0,
    "hadjar":        0,
}

# Number of races remaining in the season
REMAINING_RACES = 19

# Points awarded per race (win + sprint possibilities)
POINTS_PER_POSITION = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
FASTEST_LAP_BONUS = 1

# Number of Monte Carlo simulations
NUM_SIMULATIONS = 10000

# Driver skill tiers (affects simulation finishing position distribution)
# Higher rating = more likely to finish in top positions
DRIVER_RATINGS = {
    "verstappen": 0.95,  "norris": 0.88,  "leclerc": 0.87,
    "piastri": 0.84,     "hamilton": 0.85, "russell": 0.83,
    "antonelli": 0.75,   "lawson": 0.70,   "alonso": 0.78,
    "gasly": 0.72,       "tsunoda": 0.70,  "hulkenberg": 0.68,
    "stroll": 0.65,      "colapinto": 0.60,"bearman": 0.62,
    "ocon": 0.70,        "bottas": 0.65,   "zhou": 0.58,
    "doohan": 0.55,      "hadjar": 0.60,
}

# Known Kalshi driver names for market question parsing
DRIVER_ALIASES = {
    "max verstappen": "verstappen",
    "lando norris": "norris",
    "charles leclerc": "leclerc",
    "oscar piastri": "piastri",
    "lewis hamilton": "hamilton",
    "george russell": "russell",
    "andrea kimi antonelli": "antonelli",
    "kimi antonelli": "antonelli",
    "liam lawson": "lawson",
    "fernando alonso": "alonso",
    "pierre gasly": "gasly",
    "yuki tsunoda": "tsunoda",
    "nico hulkenberg": "hulkenberg",
    "lance stroll": "stroll",
    "franco colapinto": "colapinto",
    "oliver bearman": "bearman",
    "esteban ocon": "ocon",
    "valtteri bottas": "bottas",
    "guanyu zhou": "zhou",
    "jack doohan": "doohan",
    "isack hadjar": "hadjar",
}

# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def monte_carlo_championship(standings: dict, ratings: dict,
                              remaining: int, n_sims: int) -> dict:
    """Run Monte Carlo simulation of remaining F1 season.

    For each simulation, randomly assigns finishing positions weighted by
    driver rating, accumulates points, and tracks championship wins.

    Returns dict of driver -> win probability.
    """
    drivers = list(standings.keys())
    wins = {d: 0 for d in drivers}

    for _ in range(n_sims):
        sim_points = dict(standings)

        for _race in range(remaining):
            # Weight finishing positions by driver rating
            weights = [ratings.get(d, 0.5) for d in drivers]
            total_w = sum(weights)
            probs = [w / total_w for w in weights]

            # Sample finishing order (weighted shuffle)
            remaining_drivers = list(drivers)
            remaining_probs = list(probs)
            finish_order = []

            for _pos in range(min(len(remaining_drivers), len(POINTS_PER_POSITION))):
                if not remaining_drivers:
                    break
                total_p = sum(remaining_probs)
                if total_p <= 0:
                    break
                norm_probs = [p / total_p for p in remaining_probs]

                r = random.random()
                cumulative = 0.0
                chosen_idx = len(remaining_drivers) - 1
                for idx, p in enumerate(norm_probs):
                    cumulative += p
                    if r <= cumulative:
                        chosen_idx = idx
                        break

                finish_order.append(remaining_drivers[chosen_idx])
                remaining_drivers.pop(chosen_idx)
                remaining_probs.pop(chosen_idx)

            # Award points
            for pos, driver in enumerate(finish_order):
                if pos < len(POINTS_PER_POSITION):
                    pts = POINTS_PER_POSITION[pos]
                    # Random fastest lap bonus for top 10
                    if pos < 10 and random.random() < 0.1:
                        pts += FASTEST_LAP_BONUS
                    sim_points[driver] = sim_points.get(driver, 0) + pts

        # Determine winner
        winner = max(sim_points, key=sim_points.get)
        wins[winner] += 1

    return {d: wins[d] / n_sims for d in drivers}


def extract_driver(question: str) -> str | None:
    """Extract driver name from a market question string."""
    q = question.lower()
    # Try full name aliases first (longest match first)
    for alias in sorted(DRIVER_ALIASES.keys(), key=len, reverse=True):
        if alias in q:
            return DRIVER_ALIASES[alias]
    # Try last name direct match
    for driver in CURRENT_STANDINGS:
        if driver in q:
            return driver
    return None


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

    for term in ["F1 drivers championship", "formula 1 championship", "F1 champion"]:
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
            if not any(kw in question for kw in ["f1", "formula 1", "drivers championship"]):
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
    """Fetch active F1 drivers championship markets from Simmer API."""
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "F1 drivers championship", "limit": 50}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if any(kw in (m.get("question") or "").lower()
                       for kw in ["f1", "formula 1", "drivers championship"])]
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
    """Check open F1 positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    f1_pos = [p for p in positions
              if TRADE_SOURCE in p.get("sources", [])
              or any(kw in (p.get("question") or "").lower()
                     for kw in ["f1", "formula 1", "drivers championship"])]

    if not f1_pos:
        return 0, 0

    log(f"\n  Checking {len(f1_pos)} F1 positions for exit...")
    found, executed = 0, 0

    for pos in f1_pos:
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
    """Run the F1 Points Model trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("F1 Points Model Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Simulations: {NUM_SIMULATIONS}  Remaining races: {REMAINING_RACES}")
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
        f1_pos = [p for p in positions
                  if any(kw in (p.get("question") or "").lower()
                         for kw in ["f1", "formula 1", "drivers championship"])]
        if not f1_pos:
            log("  No F1 positions")
        for p in f1_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Monte Carlo Model ---
    log(f"Running {NUM_SIMULATIONS} Monte Carlo simulations...")
    model_probs = monte_carlo_championship(
        CURRENT_STANDINGS, DRIVER_RATINGS, REMAINING_RACES, NUM_SIMULATIONS
    )

    log("Model Championship Win Probabilities (top 10):")
    for driver, prob in sorted(model_probs.items(), key=lambda x: -x[1])[:10]:
        pts = CURRENT_STANDINGS.get(driver, 0)
        rating = DRIVER_RATINGS.get(driver, 0.5)
        log(f"  {driver:>15}: {prob:6.1%}  (pts={pts} rating={rating:.2f})")
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

        model_p = model_probs.get(driver)
        if model_p is None:
            log(f"  ? No model data for: {driver}")
            continue

        edge = model_p - price
        log(f"  {driver:>15}: market={price:.1%}  model={model_p:.1%}  edge={edge:+.1%}")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1

        # Conviction-based sizing: edge / entry_edge normalized to 0-1
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=model_p if side == "yes" else 1 - model_p)
        ok, reasons = check_safeguards(ctx)
        if not ok:
            log(f"    Skipped: {'; '.join(reasons)}")
            skip_reasons.extend(reasons)
            continue
        if reasons:
            log(f"    Warnings: {'; '.join(reasons)}")

        if not dry_run:
            result = execute_trade(
                market_id, side, size,
                reasoning=f"MC model: {driver} market={price:.1%} model={model_p:.1%} edge={edge:+.1%}",
                signal_data={"model_prob": round(model_p, 4),
                             "current_points": CURRENT_STANDINGS.get(driver, 0),
                             "edge": round(edge, 4), "driver": driver},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis=f"MC points edge on {driver}", action="buy")
            else:
                log(f"    Trade failed: {result.get('error')}", force=True)
        else:
            log(f"    [DRY RUN] Would buy {side.upper()} ${size:.2f}")
            trades_executed += 1
            total_usd += size

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
    parser = argparse.ArgumentParser(description="Kalshi F1 Points Model Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set entry_edge=0.15)")
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

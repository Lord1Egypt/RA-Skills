#!/usr/bin/env python3
"""
Kalshi F1 Race Momentum Trader

Trades F1 Drivers Championship markets on Kalshi using recent race results
to compute momentum-adjusted probabilities. Drivers on hot streaks (podiums,
wins in last 3 races) get a momentum boost, while cold streaks reduce
championship probability. Markets are slow to price in form changes.

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
    "entry_edge":        {"env": "SIMMER_F1_RACEMOM_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_F1_RACEMOM_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_F1_RACEMOM_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_F1_RACEMOM_MAX_TRADES_PER_RUN","default": 5,     "type": int},
    "slippage_max":      {"env": "SIMMER_F1_RACEMOM_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_F1_RACEMOM_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-f1-race-momentum-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-f1-racemod"
SKILL_SLUG = "kalshi-f1-race-momentum-trader"
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
# Momentum Model
# =============================================================================

# Recent race results (last 3 races) for each driver
# Position finished: 1=win, 2=second, ..., 20=last, DNF=21
# Weights: most recent race = 3x, second = 2x, third = 1x
RECENT_RESULTS = {
    "verstappen": [1, 2, 1],    # Win, P2, Win -- strong momentum
    "norris":     [2, 1, 3],    # P2, Win, P3 -- solid
    "leclerc":    [3, 3, 2],    # P3, P3, P2 -- consistent podiums
    "piastri":    [4, 4, 4],    # P4, P4, P4 -- consistent but off podium
    "hamilton":   [5, 5, 6],    # P5, P5, P6 -- midfield for him
    "russell":    [6, 7, 5],    # P6, P7, P5 -- inconsistent
    "alonso":     [8, 8, 7],    # P8, P8, P7 -- best of the rest
    "lawson":     [7, 10, 8],   # P7, P10, P8 -- adjusting to Red Bull
    "antonelli":  [10, 9, 11],  # P10, P9, P11 -- rookie growing
    "stroll":     [12, 11, 10], # P12, P11, P10 -- improving slightly
    "tsunoda":    [9, 12, 9],   # P9, P12, P9 -- inconsistent
    "gasly":      [11, 6, 13],  # P11, P6, P13 -- feast or famine
    "hulkenberg": [13, 13, 12], # P13, P13, P12 -- consistent midfield
    "ocon":       [14, 14, 14], # P14, P14, P14 -- stuck
    "bearman":    [15, 15, 15], # P15, P15, P15 -- backmarker
    "colapinto":  [16, 16, 16], # P16, P16, P16 -- backmarker
    "doohan":     [17, 17, 17], # P17, P17, P17 -- backmarker
    "hadjar":     [18, 18, 18], # P18, P18, P18 -- backmarker
    "bortoleto":  [19, 19, 19], # P19, P19, P19 -- backmarker
    "drugovich":  [20, 20, 20], # P20, P20, P20 -- backmarker
}

# Base championship probabilities (from standings/bookmakers)
BASE_PROBABILITIES = {
    "verstappen": 0.35,
    "norris":     0.28,
    "leclerc":    0.15,
    "piastri":    0.08,
    "hamilton":   0.05,
    "russell":    0.04,
    "alonso":     0.02,
    "lawson":     0.01,
    "antonelli":  0.005,
    "stroll":     0.003,
    "tsunoda":    0.002,
    "gasly":      0.002,
    "hulkenberg": 0.001,
    "ocon":       0.001,
    "bearman":    0.001,
    "colapinto":  0.001,
    "doohan":     0.001,
    "hadjar":     0.001,
    "bortoleto":  0.001,
    "drugovich":  0.001,
}

# Momentum weights: [most recent, second, third]
MOMENTUM_WEIGHTS = [3, 2, 1]

# Momentum scaling factor: how much momentum adjusts base probability
# 0.1 = momentum can shift probability by up to +/- 10% of base
MOMENTUM_SCALE = 0.15

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


def compute_momentum_score(results: list[int]) -> float:
    """Compute weighted momentum score from recent race results.

    Returns a score from -1.0 (cold streak) to +1.0 (hot streak).
    Positions are inverted (P1 = best) and weighted by recency.
    """
    if not results:
        return 0.0

    # Convert positions to performance scores: P1=1.0, P20=0.0
    max_pos = 21  # DNF value
    scores = [(max_pos - pos) / (max_pos - 1) for pos in results]

    # Apply recency weights
    total_weight = sum(MOMENTUM_WEIGHTS[:len(scores)])
    weighted = sum(s * w for s, w in zip(scores, MOMENTUM_WEIGHTS[:len(scores)]))
    avg_score = weighted / total_weight

    # Normalize to [-1, +1] range (0.5 = neutral)
    return (avg_score - 0.5) * 2


def compute_momentum_probabilities() -> dict:
    """Compute momentum-adjusted championship probabilities.

    Applies momentum boost/penalty to base probabilities.
    Hot streaks increase probability, cold streaks decrease it.
    """
    adjusted = {}
    for driver, base_p in BASE_PROBABILITIES.items():
        results = RECENT_RESULTS.get(driver, [])
        momentum = compute_momentum_score(results)
        # Apply momentum: positive momentum boosts probability
        adjustment = momentum * MOMENTUM_SCALE * base_p
        adjusted_p = max(0.001, base_p + adjustment)
        adjusted[driver] = adjusted_p

    # Normalize to sum to 1.0
    total = sum(adjusted.values())
    return {d: p / total for d, p in adjusted.items()}


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
    for driver in BASE_PROBABILITIES:
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
    """Check open F1 momentum positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    f1_positions = [p for p in positions
                    if TRADE_SOURCE in p.get("sources", [])
                    or is_f1_championship_market(p.get("question", ""))]

    if not f1_positions:
        return 0, 0

    log(f"\n  Checking {len(f1_positions)} F1 momentum positions for exit...")
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
    """Run the F1 momentum-based trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("F1 Race Momentum Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Momentum scale: {MOMENTUM_SCALE:.0%}  Weights: {MOMENTUM_WEIGHTS}")
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

    # --- Momentum Model ---
    model_probs = compute_momentum_probabilities()

    log("Momentum Model (last 3 races weighted):")
    for driver, prob in sorted(model_probs.items(), key=lambda x: -x[1])[:12]:
        results = RECENT_RESULTS.get(driver, [])
        momentum = compute_momentum_score(results)
        base = BASE_PROBABILITIES.get(driver, 0)
        positions_str = ",".join(f"P{r}" for r in results)
        trend = "HOT" if momentum > 0.3 else "COLD" if momentum < -0.3 else "FLAT"
        log(f"  {driver:>15}: {prob:6.1%}  (base={base:.1%}  momentum={momentum:+.2f} "
            f"[{positions_str}] {trend})")
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

        momentum = compute_momentum_score(RECENT_RESULTS.get(driver, []))
        edge = model_p - price
        trend = "HOT" if momentum > 0.3 else "COLD" if momentum < -0.3 else "FLAT"

        log(f"  {driver:>15}: market={price:.1%}  model={model_p:.1%}  "
            f"edge={edge:+.1%}  momentum={momentum:+.2f} ({trend})")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1

        # Conviction-based sizing
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id,
                                 my_probability=model_p if side == "yes" else 1 - model_p)
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
                reasoning=(f"Momentum model: {driver} market={price:.1%} "
                           f"model={model_p:.1%} edge={edge:+.1%} "
                           f"momentum={momentum:+.2f} ({trend})"),
                signal_data={"driver": driver, "model_prob": round(model_p, 4),
                             "momentum": round(momentum, 4),
                             "recent_results": RECENT_RESULTS.get(driver, []),
                             "edge": round(edge, 4), "trend": trend},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"Momentum edge on {driver} ({trend})", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi F1 Race Momentum Trader")
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

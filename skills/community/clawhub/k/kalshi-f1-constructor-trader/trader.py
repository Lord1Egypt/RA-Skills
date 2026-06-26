#!/usr/bin/env python3
"""
Kalshi F1 Constructor Trader

Trades F1 Drivers Championship markets on Kalshi using constructor (team)
car performance ratings. Drivers in faster cars have structurally higher
championship probabilities -- this is the single strongest predictor of
F1 outcomes and markets often underprice constructor advantage.

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
    "entry_edge":        {"env": "SIMMER_F1_CONSTR_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_F1_CONSTR_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_F1_CONSTR_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_F1_CONSTR_MAX_TRADES_PER_RUN","default": 4,     "type": int},
    "slippage_max":      {"env": "SIMMER_F1_CONSTR_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_F1_CONSTR_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-f1-constructor-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-f1-constr"
SKILL_SLUG = "kalshi-f1-constructor-trader"
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
# Constructor Performance Model
# =============================================================================

# Constructor (team) car performance ratings (0-100 scale)
# Based on 2025 season pace data: qualifying gaps, race pace, development rate
# These ratings represent relative car speed advantage
CONSTRUCTOR_RATINGS = {
    "Red Bull":      95,
    "McLaren":       92,
    "Ferrari":       90,
    "Mercedes":      88,
    "Aston Martin":  82,
}

# Driver-to-constructor mapping (2025 season)
DRIVER_CONSTRUCTORS = {
    "verstappen":  "Red Bull",
    "lawson":      "Red Bull",
    "norris":      "McLaren",
    "piastri":     "McLaren",
    "leclerc":     "Ferrari",
    "hamilton":    "Ferrari",
    "russell":     "Mercedes",
    "antonelli":   "Mercedes",
    "alonso":      "Aston Martin",
    "stroll":      "Aston Martin",
}

# Individual driver skill modifiers (relative to teammate baseline)
# Positive = outperforms teammate, Negative = underperforms
DRIVER_SKILL_MODIFIER = {
    "verstappen":  +8,   # Generational talent, consistently outperforms car
    "norris":      +4,   # Elite qualifier, strong racer
    "leclerc":     +3,   # Top qualifier, improving race craft
    "hamilton":    +3,   # GOAT-tier consistency
    "russell":     +2,   # Strong all-rounder
    "piastri":     +1,   # Rising star, solid results
    "alonso":      +2,   # Experience and racecraft
    "lawson":       0,   # New to top team, baseline
    "antonelli":   -1,   # Rookie season
    "stroll":      -2,   # Consistent underperformer vs teammate
}

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
}


def compute_model_probabilities() -> dict:
    """Compute championship win probabilities from constructor + driver ratings.

    Uses a power-law model: P(win) proportional to (rating)^3
    The cubic exponent amplifies the advantage of faster cars,
    reflecting the compounding nature of F1 points over a season.
    """
    driver_ratings = {}
    for driver, constructor in DRIVER_CONSTRUCTORS.items():
        base = CONSTRUCTOR_RATINGS.get(constructor, 75)
        modifier = DRIVER_SKILL_MODIFIER.get(driver, 0)
        driver_ratings[driver] = base + modifier

    # Power-law conversion to probabilities
    raw = {d: r ** 3 for d, r in driver_ratings.items()}
    total = sum(raw.values())
    return {d: v / total for d, v in raw.items()}


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
    # Try full name aliases first (longer matches first)
    for alias, driver in sorted(DRIVER_ALIASES.items(), key=lambda x: -len(x[0])):
        if alias in q:
            return driver
    # Try last name only
    for driver in DRIVER_CONSTRUCTORS:
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
    """Check open F1 positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    f1_positions = [p for p in positions
                    if TRADE_SOURCE in p.get("sources", [])
                    or is_f1_championship_market(p.get("question", ""))]

    if not f1_positions:
        return 0, 0

    log(f"\n  Checking {len(f1_positions)} F1 positions for exit...")
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
    """Run the F1 constructor-based trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("F1 Constructor Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("")
        log("Constructor ratings:")
        for team, rating in sorted(CONSTRUCTOR_RATINGS.items(), key=lambda x: -x[1]):
            log(f"  {team:>15}: {rating}")
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

    # --- Model ---
    model_probs = compute_model_probabilities()
    log("Constructor Model Probabilities:")
    for driver, prob in sorted(model_probs.items(), key=lambda x: -x[1]):
        constructor = DRIVER_CONSTRUCTORS[driver]
        rating = CONSTRUCTOR_RATINGS[constructor] + DRIVER_SKILL_MODIFIER.get(driver, 0)
        log(f"  {driver:>15}: {prob:6.1%}  (team={constructor}, rating={rating})")
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

        constructor = DRIVER_CONSTRUCTORS[driver]
        edge = model_p - price
        log(f"  {driver:>15} ({constructor:>12}): market={price:.1%}  "
            f"model={model_p:.1%}  edge={edge:+.1%}")

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
                reasoning=(f"Constructor model: {driver} ({constructor}) "
                           f"market={price:.1%} model={model_p:.1%} edge={edge:+.1%}"),
                signal_data={"driver": driver, "constructor": constructor,
                             "model_prob": round(model_p, 4),
                             "constructor_rating": CONSTRUCTOR_RATINGS[constructor],
                             "edge": round(edge, 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"Constructor edge on {driver}", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi F1 Constructor Trader")
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

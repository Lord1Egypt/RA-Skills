#!/usr/bin/env python3
"""
Kalshi CPI Seasonal Trader

Trades CPI/inflation markets on Kalshi using documented seasonal patterns
in CPI data. Energy costs spike in summer, housing adjustments hit January,
and other well-known seasonal effects create predictable biases in CPI bins.

The skill adjusts CPI bin probabilities based on the current month's
seasonal adjustment factor, then compares to market prices for edge.

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
    "entry_edge":        {"env": "SIMMER_ECON_SEAS_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ECON_SEAS_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ECON_SEAS_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ECON_SEAS_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_ECON_SEAS_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ECON_SEAS_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-econ-seasonal-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-econ-seasonal"
SKILL_SLUG = "kalshi-econ-seasonal-trader"
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
# Seasonal Adjustment Model
# =============================================================================

# Monthly CPI seasonal adjustments (percentage points)
# Positive = CPI tends to run hotter than consensus
# Negative = CPI tends to run cooler than consensus
#
# Based on historical BLS CPI data patterns:
# - January: +0.10 (housing OER annual reset, January effect)
# - February: -0.05 (post-holiday normalization)
# - March: 0.00 (neutral transition month)
# - April: +0.05 (spring demand uptick, gasoline blend switch)
# - May: +0.05 (summer driving season begins, energy demand)
# - June: +0.10 (peak summer energy costs, travel season)
# - July: +0.05 (continued summer energy, but moderating)
# - August: 0.00 (back-to-school offsets energy)
# - September: -0.05 (summer demand fade, energy pullback)
# - October: -0.05 (autumn deflation in food/energy)
# - November: 0.00 (pre-holiday neutral)
# - December: +0.05 (holiday demand, year-end pricing)
SEASONAL_ADJUSTMENTS = {
    1: +0.10,
    2: -0.05,
    3:  0.00,
    4: +0.05,
    5: +0.05,
    6: +0.10,
    7: +0.05,
    8:  0.00,
    9: -0.05,
    10: -0.05,
    11:  0.00,
    12: +0.05,
}

# CPI bin labels and their base probabilities (uniform prior)
# These represent typical Kalshi CPI bins for monthly/annual readings
CPI_BIN_KEYWORDS = {
    "below 2": "low",
    "under 2": "low",
    "less than 2": "low",
    "2.0% or lower": "low",
    "2% or less": "low",
    "below 2.5": "low_mid",
    "2.0% to 2.4": "low_mid",
    "2.0%-2.4": "low_mid",
    "2.5% to 2.9": "mid",
    "2.5%-2.9": "mid",
    "3.0% to 3.4": "high_mid",
    "3.0%-3.4": "high_mid",
    "3.0% or higher": "high",
    "above 3": "high",
    "3.5% or higher": "high",
    "above 3.5": "high",
    "over 3": "high",
}

# How seasonal adjustments shift bin probabilities
# Positive seasonal adj -> shift probability mass toward higher bins
# Negative seasonal adj -> shift probability mass toward lower bins
BIN_SHIFT_WEIGHTS = {
    "low":     -1.0,  # Benefits from negative seasonal adj
    "low_mid": -0.5,
    "mid":      0.0,  # Neutral
    "high_mid": +0.5,
    "high":    +1.0,  # Benefits from positive seasonal adj
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


def get_current_seasonal_adj() -> float:
    """Get the seasonal adjustment for the current month."""
    month = datetime.now(timezone.utc).month
    return SEASONAL_ADJUSTMENTS.get(month, 0.0)


def classify_cpi_bin(question: str) -> str | None:
    """Classify a market question into a CPI bin category."""
    q = question.lower()
    for keyword, bin_cat in CPI_BIN_KEYWORDS.items():
        if keyword.lower() in q:
            return bin_cat
    return None


def compute_seasonal_fair_value(market_price: float, bin_category: str,
                                 seasonal_adj: float) -> float:
    """Compute seasonally-adjusted fair value for a CPI bin.

    The seasonal adjustment shifts probability mass between bins.
    A positive seasonal adj (hot CPI month) increases fair value
    for high bins and decreases it for low bins.
    """
    shift_weight = BIN_SHIFT_WEIGHTS.get(bin_category, 0.0)
    # Fair value = market price adjusted by seasonal factor
    # The shift is proportional to both the seasonal adj and the bin's position
    adjustment = seasonal_adj * shift_weight
    fair_value = market_price + adjustment
    # Clamp to valid probability range
    return max(0.01, min(0.99, fair_value))


def is_cpi_market(question: str) -> bool:
    """Check if a market question is about CPI/inflation."""
    q = question.lower()
    cpi_terms = ["cpi", "inflation", "consumer price index",
                 "price index", "core cpi", "headline cpi"]
    return any(term in q for term in cpi_terms)


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
    """Discover CPI/inflation markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["CPI", "inflation", "consumer price index", "core CPI"]:
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
            if not is_cpi_market(question):
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


def fetch_cpi_markets():
    """Fetch active CPI/inflation markets from Simmer API."""
    try:
        all_markets = []
        for query in ["CPI", "inflation"]:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": query, "limit": 50}
            )
            markets = result.get("markets", [])
            all_markets.extend(markets)

        # Deduplicate by market ID
        seen_ids = set()
        unique = []
        for m in all_markets:
            mid = m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                if is_cpi_market(m.get("question", "")):
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
    """Check open CPI positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    cpi_positions = [p for p in positions
                     if TRADE_SOURCE in p.get("sources", [])
                     or is_cpi_market(p.get("question", ""))]

    if not cpi_positions:
        return 0, 0

    log(f"\n  Checking {len(cpi_positions)} CPI positions for exit...")
    found, executed = 0, 0

    for pos in cpi_positions:
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
    """Run the CPI seasonal trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    current_month = datetime.now(timezone.utc).month
    seasonal_adj = get_current_seasonal_adj()
    month_name = datetime.now(timezone.utc).strftime("%B")

    log("CPI Seasonal Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Month: {month_name} (#{current_month})  Seasonal adj: {seasonal_adj:+.2f}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("")
        log("Seasonal adjustments by month:")
        for m in range(1, 13):
            adj = SEASONAL_ADJUSTMENTS[m]
            marker = " <-- current" if m == current_month else ""
            log(f"  {m:2d}: {adj:+.2f}{marker}")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        cpi = [p for p in positions if is_cpi_market(p.get("question", ""))]
        if not cpi:
            log("  No CPI/inflation positions")
        for p in cpi:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Seasonal Model Summary ---
    log(f"Seasonal Model for {month_name}:")
    log(f"  Adjustment: {seasonal_adj:+.2f}")
    if seasonal_adj > 0:
        log("  Bias: CPI tends to run HOT this month -> favor higher bins")
    elif seasonal_adj < 0:
        log("  Bias: CPI tends to run COOL this month -> favor lower bins")
    else:
        log("  Bias: Neutral month -- no seasonal tilt")
    log("")

    # --- Discovery ---
    log("Discovering CPI/inflation markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_cpi_markets()
    log(f"  Found {len(markets)} active CPI/inflation markets")

    if not markets:
        log("  No CPI markets available")
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

        bin_cat = classify_cpi_bin(question)
        if not bin_cat:
            log(f"  ? Unclassified bin: {question[:60]}")
            continue

        # Compute seasonally-adjusted fair value
        fair_value = compute_seasonal_fair_value(price, bin_cat, seasonal_adj)
        edge = fair_value - price

        log(f"  {bin_cat:>10}: market={price:.1%}  fair={fair_value:.1%}  "
            f"edge={edge:+.1%}  ({question[:50]})")

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
                                 my_probability=fair_value if side == "yes" else 1 - fair_value)
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
                reasoning=(f"Seasonal model: {bin_cat} month={month_name} "
                           f"adj={seasonal_adj:+.2f} market={price:.1%} "
                           f"fair={fair_value:.1%} edge={edge:+.1%}"),
                signal_data={"bin_category": bin_cat, "month": current_month,
                             "seasonal_adj": seasonal_adj, "fair_value": round(fair_value, 4),
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
                              thesis=f"Seasonal edge on {bin_cat} bin", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi CPI Seasonal Trader")
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

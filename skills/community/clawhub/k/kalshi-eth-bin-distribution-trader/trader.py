#!/usr/bin/env python3
"""
Kalshi ETH Bin Distribution Trader

ETH price bins on Kalshi must sum to 100%. When they deviate beyond a
tolerance, this skill identifies mispriced bins and trades toward
the expected rebalance.

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
    "entry_edge":        {"env": "SIMMER_ETH_BINDIST_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ETH_BINDIST_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ETH_BINDIST_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ETH_BINDIST_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_ETH_BINDIST_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ETH_BINDIST_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
    "sum_tolerance":     {"env": "SIMMER_ETH_BINDIST_SUM_TOLERANCE",     "default": 0.05,  "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-eth-bin-distribution-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-eth-bindist"
SKILL_SLUG = "kalshi-eth-bin-distribution-trader"
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
SUM_TOLERANCE = _config["sum_tolerance"]
TIME_TO_RESOLUTION_MIN_HOURS = 2

# Conviction-based sizing (CLAUDE.md compliant)
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", "0.62"))
MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", "5"))

# =============================================================================
# Bin Distribution Model
# =============================================================================

# Known ETH price bin structures on Kalshi
# These are mutually exclusive and exhaustive bins that must sum to ~100%
ETH_BIN_GROUPS = {
    "weekly_close": [
        "below $1500", "$1500-$2000", "$2000-$2500", "$2500-$3000",
        "$3000-$3500", "$3500-$4000", "$4000-$4500", "$4500-$5000",
        "above $5000",
    ],
    "monthly_close": [
        "below $1000", "$1000-$2000", "$2000-$3000", "$3000-$4000",
        "$4000-$5000", "$5000-$6000", "above $6000",
    ],
}

# Price range keywords for matching markets to bins
PRICE_KEYWORDS = [
    "above", "below", "between", "over", "under", "higher", "lower",
    "close", "end", "settle", "price",
]


def classify_bin_group(markets: list) -> dict:
    """Group markets into bin sets that should sum to 100%.

    Returns dict of group_key -> list of (market, price) tuples.
    Markets are grouped by shared resolution date and event type.
    """
    groups = {}
    for m in markets:
        question = (m.get("question") or "").lower()
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        resolve_date = m.get("resolves_at", "")[:10]  # YYYY-MM-DD

        # Build group key from resolution date and base question
        # Strip specific price numbers to group related bins
        base_q = question
        for char in "0123456789$,.":
            base_q = base_q.replace(char, "")
        base_q = " ".join(base_q.split()[:6])  # First 6 words as group key

        group_key = f"{resolve_date}|{base_q}"

        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append({"market": m, "price": price, "question": question})

    # Filter to groups with 3+ bins (likely a complete bin set)
    return {k: v for k, v in groups.items() if len(v) >= 3}


def compute_bin_adjustments(bin_group: list) -> list:
    """Compute fair prices for a bin group that sums to 100%.

    If the sum > 1.0 + tolerance, all bins are overpriced proportionally.
    If the sum < 1.0 - tolerance, all bins are underpriced proportionally.
    Returns list of (market, current_price, fair_price, adjustment) dicts.
    """
    total = sum(b["price"] for b in bin_group)
    if total <= 0:
        return []

    adjustments = []
    for b in bin_group:
        current = b["price"]
        fair = current / total  # Normalize so sum = 1.0
        adjustment = fair - current

        adjustments.append({
            "market": b["market"],
            "question": b["question"],
            "current_price": current,
            "fair_price": fair,
            "adjustment": adjustment,
        })

    return adjustments


def find_best_trades(adjustments: list, entry_edge: float) -> list:
    """Find the best trades from bin adjustments.

    Returns list of (market, side, fair_price, edge) sorted by |edge| desc.
    """
    trades = []
    for adj in adjustments:
        edge = abs(adj["adjustment"])
        if edge < entry_edge:
            continue

        if adj["adjustment"] > 0:
            side = "yes"  # Underpriced, buy YES
        else:
            side = "no"   # Overpriced, buy NO

        trades.append({
            "market": adj["market"],
            "side": side,
            "fair_price": adj["fair_price"],
            "current_price": adj["current_price"],
            "edge": edge,
            "question": adj["question"],
        })

    trades.sort(key=lambda t: t["edge"], reverse=True)
    return trades


# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


# =============================================================================
# Simmer Client
# =============================================================================

def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client, YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
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

        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD = float(os.environ.get("SIMMER_NO_THRESHOLD", str(NO_THRESHOLD)))
        MIN_TRADE = float(os.environ.get("SIMMER_MIN_TRADE", str(MIN_TRADE)))
    return _client


# =============================================================================
# Signal: conviction-based (CLAUDE.md compliant)
# =============================================================================

def compute_signal(market: dict, fair_price: float) -> tuple:
    """Compute trade signal with conviction-based sizing.

    Returns (side, size, reasoning) -- never (side, reasoning).
    """
    p = market.get("external_price_yes") or market.get("price_yes") or 0
    q = (market.get("question") or "")

    edge = fair_price - p

    if abs(edge) < ENTRY_EDGE:
        return None, 0, f"Neutral: bin={p:.1%} fair={fair_price:.1%} edge={edge:+.1%}"

    if edge > 0:
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(MIN_TRADE, round(conviction * MAX_POSITION_USD, 2))
        return "yes", size, f"YES bin={p:.0%} fair={fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"
    else:
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(MIN_TRADE, round(conviction * MAX_POSITION_USD, 2))
        return "no", size, f"NO bin={p:.0%} fair={fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover ETH price bin markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["ETH price", "ethereum", "ether price", "ETH above", "ETH below",
                  "ETH between", "ethereum close"]:
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
            if "eth" not in question and "ethereum" not in question:
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


def fetch_eth_markets():
    """Fetch active ETH price markets from Simmer API."""
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "ETH", "limit": 100}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if "eth" in (m.get("question") or "").lower()
                or "ethereum" in (m.get("question") or "").lower()]
    except Exception as e:
        safe_print(f"  Failed to fetch ETH markets: {e}")
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


def check_safeguards(context: dict) -> tuple:
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


def check_exits(dry_run: bool, log=print) -> tuple:
    """Check open ETH bin positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    eth_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or "eth" in (p.get("question") or "").lower()]

    if not eth_pos:
        return 0, 0

    log(f"\n  Checking {len(eth_pos)} ETH bin positions for exit...")
    found, executed = 0, 0

    for pos in eth_pos:
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
    """Run the ETH bin distribution rebalance trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("ETH Bin Distribution Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Sum tolerance: {SUM_TOLERANCE:.0%}")
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
        eth_pos = [p for p in positions
                   if "eth" in (p.get("question") or "").lower()]
        if not eth_pos:
            log("  No ETH bin positions")
        for p in eth_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering ETH price bin markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new ETH markets")

    # --- Fetch ---
    markets = fetch_eth_markets()
    log(f"  Found {len(markets)} active ETH markets")

    if not markets:
        log("  No ETH markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Group into bins ---
    bin_groups = classify_bin_group(markets)
    log(f"  Identified {len(bin_groups)} bin groups")

    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for group_key, bins in bin_groups.items():
        total_prob = sum(b["price"] for b in bins)
        deviation = abs(total_prob - 1.0)

        log(f"\n  Group: {group_key[:50]}")
        log(f"    Bins: {len(bins)}  Sum: {total_prob:.1%}  Deviation: {deviation:.1%}")

        if deviation < SUM_TOLERANCE:
            log(f"    Sum within tolerance ({SUM_TOLERANCE:.0%}) -- skip")
            continue

        # Compute fair prices and find trades
        adjustments = compute_bin_adjustments(bins)
        best_trades = find_best_trades(adjustments, ENTRY_EDGE)

        if not best_trades:
            log(f"    No bins with sufficient edge")
            continue

        for trade in best_trades:
            m = trade["market"]
            market_id = m.get("id")

            side, size, reasoning = compute_signal(m, trade["fair_price"])

            if side is None:
                continue

            signals += 1
            log(f"    {trade['question'][:50]}  mkt={trade['current_price']:.1%}  "
                f"fair={trade['fair_price']:.1%}  edge={trade['edge']:.1%}")

            if trades_executed >= MAX_TRADES_PER_RUN:
                log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
                skip_reasons.append("max_trades")
                continue

            # Safeguards
            ctx = get_market_context(market_id, my_probability=trade["fair_price"])
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
                    reasoning=reasoning,
                    signal_data={"fair_price": round(trade["fair_price"], 4),
                                 "bin_sum": round(total_prob, 4),
                                 "edge": round(trade["edge"], 4)},
                )
                if result.get("success"):
                    trades_executed += 1
                    total_usd += size
                    tag = "[PAPER] " if result.get("simulated") else ""
                    log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                    if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                        log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                                  skill_slug=SKILL_SLUG, thesis="Bin distribution rebalance", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi ETH Bin Distribution Trader")
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

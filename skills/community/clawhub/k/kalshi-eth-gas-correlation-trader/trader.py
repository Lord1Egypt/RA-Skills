#!/usr/bin/env python3
"""
Kalshi ETH Gas Correlation Trader

High on-chain gas usage signals strong demand for ETH block space, which
is a bullish signal for ETH price. This skill monitors gas price levels
and trades ETH price markets when gas indicates a directional move.

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
    "entry_edge":        {"env": "SIMMER_ETH_GAS_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ETH_GAS_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ETH_GAS_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ETH_GAS_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_ETH_GAS_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ETH_GAS_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
    "gas_high_gwei":     {"env": "SIMMER_ETH_GAS_HIGH_GWEI",         "default": 50.0,  "type": float},
    "gas_low_gwei":      {"env": "SIMMER_ETH_GAS_LOW_GWEI",          "default": 10.0,  "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-eth-gas-correlation-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-eth-gas"
SKILL_SLUG = "kalshi-eth-gas-correlation-trader"
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
GAS_HIGH_GWEI = _config["gas_high_gwei"]
GAS_LOW_GWEI = _config["gas_low_gwei"]
TIME_TO_RESOLUTION_MIN_HOURS = 2


# =============================================================================
# Gas Correlation Model
# =============================================================================

# Historical gas-price regimes and their ETH price implications
GAS_REGIMES = {
    "extreme":  {"min_gwei": 100, "bias": 0.15, "label": "Extreme demand"},
    "high":     {"min_gwei": 50,  "bias": 0.08, "label": "High demand"},
    "normal":   {"min_gwei": 20,  "bias": 0.00, "label": "Normal activity"},
    "low":      {"min_gwei": 10,  "bias": -0.05, "label": "Low activity"},
    "dead":     {"min_gwei": 0,   "bias": -0.10, "label": "Minimal activity"},
}


def classify_gas_regime(gas_gwei: float) -> dict:
    """Classify current gas price into a regime.

    Returns the regime dict with bias information.
    """
    for name, regime in GAS_REGIMES.items():
        if gas_gwei >= regime["min_gwei"]:
            return {"name": name, **regime}
    return {"name": "dead", **GAS_REGIMES["dead"]}


def estimate_gas_from_market_data(markets: list) -> float:
    """Estimate current gas regime from market question keywords.

    Since we may not have direct gas data, we look for gas-related
    keywords in market questions to infer the regime.
    Returns estimated gas price in gwei.
    """
    gas_mentions = 0
    high_activity_mentions = 0

    for m in markets:
        q = (m.get("question") or "").lower()
        if "gas" in q or "fee" in q or "transaction" in q:
            gas_mentions += 1
        if "congestion" in q or "high" in q or "surge" in q:
            high_activity_mentions += 1

    # Default to normal gas if no signals
    if gas_mentions == 0:
        return 25.0  # Normal gas

    if high_activity_mentions > gas_mentions / 2:
        return 60.0  # High gas
    return 25.0


def compute_gas_adjusted_fair(market_price: float, gas_bias: float,
                               is_bullish_market: bool) -> float:
    """Compute gas-adjusted fair probability.

    High gas = bullish for "ETH above X" markets.
    Low gas = bearish for "ETH above X" markets.
    """
    if is_bullish_market:
        # "Will ETH be above $X?" -- high gas is bullish
        fair = market_price + gas_bias
    else:
        # "Will ETH be below $X?" -- high gas is bearish (less likely below)
        fair = market_price - gas_bias

    return max(0.01, min(0.99, fair))


def is_bullish_question(question: str) -> bool:
    """Determine if a market question is bullish-direction.

    "ETH above $X" = bullish, "ETH below $X" = bearish.
    """
    q = question.lower()
    bullish_keywords = ["above", "over", "higher", "reach", "exceed", "top"]
    bearish_keywords = ["below", "under", "lower", "drop", "fall"]

    bullish_count = sum(1 for kw in bullish_keywords if kw in q)
    bearish_count = sum(1 for kw in bearish_keywords if kw in q)

    return bullish_count >= bearish_count


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
        return None, 0, f"Neutral: mkt={p:.1%} fair={fair_price:.1%} edge={edge:+.1%}"

    if edge > 0:
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(conviction * MAX_POSITION_USD, 2))
        return "yes", size, f"YES mkt={p:.0%} fair={fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"
    else:
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(conviction * MAX_POSITION_USD, 2))
        return "no", size, f"NO mkt={p:.0%} fair={fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover ETH price markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["ETH price", "ethereum", "ether price", "ETH above", "ETH below",
                  "ethereum gas", "ETH gas"]:
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
                    "q": "ETH", "limit": 50}
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
    """Check open ETH gas positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    eth_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or "eth" in (p.get("question") or "").lower()]

    if not eth_pos:
        return 0, 0

    log(f"\n  Checking {len(eth_pos)} ETH gas positions for exit...")
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
    """Run the ETH gas correlation trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("ETH Gas Correlation Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Gas thresholds: high={GAS_HIGH_GWEI:.0f} gwei, low={GAS_LOW_GWEI:.0f} gwei")
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
            log("  No ETH gas positions")
        for p in eth_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering ETH price markets on Kalshi...")
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

    # --- Estimate gas regime ---
    estimated_gas = estimate_gas_from_market_data(markets)
    gas_regime = classify_gas_regime(estimated_gas)
    log(f"  Gas regime: {gas_regime['name']} ({gas_regime['label']}) "
        f"bias={gas_regime['bias']:+.0%}")

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        bullish = is_bullish_question(question)
        fair = compute_gas_adjusted_fair(price, gas_regime["bias"], bullish)

        side, size, reasoning = compute_signal(m, fair)

        log(f"  {question[:50]}  mkt={price:.1%}  fair={fair:.1%}  "
            f"{'bull' if bullish else 'bear'}  -> {side or 'hold'}")

        if side is None:
            continue

        signals += 1

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=fair if side == "yes" else 1 - fair)
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
                signal_data={"fair": round(fair, 4), "gas_regime": gas_regime["name"],
                             "gas_bias": gas_regime["bias"]},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis="ETH gas correlation", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi ETH Gas Correlation Trader")
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

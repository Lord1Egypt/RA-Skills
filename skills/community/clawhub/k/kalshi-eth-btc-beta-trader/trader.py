#!/usr/bin/env python3
"""
Kalshi ETH-BTC Beta Trader

ETH historically moves ~1.3x BTC. When BTC-linked Kalshi odds shift,
ETH markets lag behind. This skill detects that lag and trades the
expected ETH catch-up.

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
    "entry_edge":        {"env": "SIMMER_ETH_BTCBETA_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ETH_BTCBETA_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ETH_BTCBETA_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ETH_BTCBETA_MAX_TRADES_PER_RUN","default": 4,     "type": int},
    "slippage_max":      {"env": "SIMMER_ETH_BTCBETA_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ETH_BTCBETA_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
    "beta_factor":       {"env": "SIMMER_ETH_BTCBETA_BETA",              "default": 1.3,   "type": float},
    "lag_window_hours":  {"env": "SIMMER_ETH_BTCBETA_LAG_HOURS",         "default": 6.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-eth-btc-beta-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-eth-btcbeta"
SKILL_SLUG = "kalshi-eth-btc-beta-trader"
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
BETA_FACTOR = _config["beta_factor"]
LAG_WINDOW_HOURS = _config["lag_window_hours"]
TIME_TO_RESOLUTION_MIN_HOURS = 2


# =============================================================================
# ETH-BTC Beta Model
# =============================================================================

# Historical BTC price bin boundaries for Kalshi markets (approximate)
BTC_PRICE_BINS = [
    (50000, 55000), (55000, 60000), (60000, 65000), (65000, 70000),
    (70000, 75000), (75000, 80000), (80000, 90000), (90000, 100000),
    (100000, 120000), (120000, 150000),
]

# ETH/BTC correlation mapping: BTC bin midpoint -> expected ETH multiplier
# ETH moves beta * BTC_move, so if BTC goes up 10%, ETH expected up 13%
ETH_BTC_RATIO_BASELINE = 0.04  # ETH/BTC ratio baseline (~0.04)

def estimate_eth_fair_price(btc_market_price: float, eth_market_price: float,
                            btc_move_pct: float) -> float:
    """Estimate fair ETH probability given BTC move.

    If BTC odds shifted by btc_move_pct, ETH should shift by beta * btc_move_pct.
    Returns the fair ETH probability after applying the beta adjustment.
    """
    eth_expected_move = btc_move_pct * BETA_FACTOR
    fair_eth = eth_market_price + eth_expected_move
    return max(0.01, min(0.99, fair_eth))


def detect_btc_shift(btc_markets: list) -> dict:
    """Detect recent BTC probability shifts from market data.

    Returns dict mapping price-bin keywords to shift magnitude.
    """
    shifts = {}
    for m in btc_markets:
        question = (m.get("question") or "").lower()
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        prev_price = m.get("previous_price_yes") or m.get("price_24h_ago") or price

        if prev_price > 0 and price > 0:
            shift = price - prev_price
            if abs(shift) > 0.02:  # Only care about 2%+ shifts
                shifts[question[:80]] = {
                    "current": price,
                    "previous": prev_price,
                    "shift": shift,
                    "market_id": m.get("id"),
                }
    return shifts


def match_eth_to_btc(eth_question: str, btc_shifts: dict) -> float | None:
    """Match an ETH market to corresponding BTC shift.

    Looks for overlapping price range keywords between ETH and BTC markets.
    Returns the expected BTC shift that should propagate to ETH, or None.
    """
    eq = eth_question.lower()

    # Extract price keywords from ETH question
    price_keywords = []
    for word in eq.split():
        word = word.replace(",", "").replace("$", "").replace("k", "000")
        try:
            val = float(word)
            if val > 100:
                price_keywords.append(val)
        except ValueError:
            continue

    if not price_keywords:
        return None

    # Find BTC shifts in correlated price ranges
    total_shift = 0.0
    matched = 0
    for bq, data in btc_shifts.items():
        total_shift += data["shift"]
        matched += 1

    if matched == 0:
        return None

    avg_shift = total_shift / matched
    return avg_shift


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

        # Re-read thresholds after SDK may have applied skill config
    return _client


# =============================================================================
# Signal: conviction-based (CLAUDE.md compliant)
# =============================================================================

def compute_signal(market: dict, model_fair_price: float) -> tuple:
    """Compute trade signal with conviction-based sizing.

    Returns (side, size, reasoning) -- never (side, reasoning).
    """
    p = market.get("external_price_yes") or market.get("price_yes") or 0
    q = (market.get("question") or "")

    edge = model_fair_price - p

    if abs(edge) < ENTRY_EDGE:
        return None, 0, f"Neutral: ETH market={p:.1%} model={model_fair_price:.1%} edge={edge:+.1%}"

    if edge > 0:
        # Model says underpriced -> buy YES
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(conviction * MAX_POSITION_USD, 2))
        return "yes", size, f"YES ETH={p:.0%} fair={model_fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"
    else:
        # Model says overpriced -> buy NO
        conviction = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(conviction * MAX_POSITION_USD, 2))
        return "no", size, f"NO ETH={p:.0%} fair={model_fair_price:.0%} edge={edge:+.0%} size=${size} -- {q[:70]}"


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover ETH price markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["ETH price", "ethereum", "ether price", "ETH above", "ETH below"]:
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


def discover_btc_markets(log=print):
    """Discover BTC price markets for beta correlation."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["BTC price", "bitcoin", "BTC above", "BTC below"]:
        try:
            results = client.list_importable_markets(
                q=term, venue="kalshi", limit=20, min_volume=0
            )
        except Exception as e:
            if "429" in str(e):
                return imported
            continue

        for m in results:
            url = m.get("url", "")
            question = (m.get("question") or "").lower()
            if not url or url in seen:
                continue
            seen.add(url)
            if "btc" not in question and "bitcoin" not in question:
                continue
            try:
                result = client.import_kalshi_market(url)
                status = result.get("status", "") if result else ""
                if status == "imported":
                    imported += 1
            except Exception as e:
                if "rate limit" in str(e).lower() or "429" in str(e):
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


def fetch_btc_markets():
    """Fetch active BTC price markets for beta reference."""
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "BTC", "limit": 50}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if "btc" in (m.get("question") or "").lower()
                or "bitcoin" in (m.get("question") or "").lower()]
    except Exception as e:
        safe_print(f"  Failed to fetch BTC markets: {e}")
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
    """Check open ETH positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    eth_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or "eth" in (p.get("question") or "").lower()
               or "ethereum" in (p.get("question") or "").lower()]

    if not eth_pos:
        return 0, 0

    log(f"\n  Checking {len(eth_pos)} ETH positions for exit...")
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
    """Run the ETH-BTC beta lag trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("ETH-BTC Beta Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Beta factor: {BETA_FACTOR:.2f}  Lag window: {LAG_WINDOW_HOURS:.1f}h")
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
                   if "eth" in (p.get("question") or "").lower()
                   or "ethereum" in (p.get("question") or "").lower()]
        if not eth_pos:
            log("  No ETH positions")
        for p in eth_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering ETH price markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new ETH markets")

    log("Discovering BTC markets for beta reference...")
    btc_newly = discover_btc_markets(log=log)
    if btc_newly:
        log(f"  Imported {btc_newly} new BTC markets")

    # --- Fetch ---
    eth_markets = fetch_eth_markets()
    btc_markets = fetch_btc_markets()
    log(f"  Found {len(eth_markets)} active ETH markets, {len(btc_markets)} BTC markets")

    if not eth_markets:
        log("  No ETH markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Detect BTC shifts ---
    btc_shifts = detect_btc_shift(btc_markets)
    if btc_shifts:
        log(f"\n  BTC shifts detected: {len(btc_shifts)}")
        for bq, data in list(btc_shifts.items())[:5]:
            log(f"    {bq[:50]}: {data['shift']:+.1%}")
    else:
        log("  No significant BTC shifts detected -- using direct edge analysis")

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in eth_markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        # Compute fair price: if BTC shifted, apply beta adjustment
        if btc_shifts:
            btc_shift = match_eth_to_btc(question, btc_shifts)
            if btc_shift is not None:
                model_fair = estimate_eth_fair_price(0, price, btc_shift)
            else:
                model_fair = price  # No matching BTC shift
        else:
            model_fair = price  # No BTC data, rely on direct edge

        side, size, reasoning = compute_signal(m, model_fair)

        log(f"  {question[:60]}  mkt={price:.1%}  fair={model_fair:.1%}  -> {reasoning[:80]}")

        if side is None:
            continue

        signals += 1

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=model_fair if side == "yes" else 1 - model_fair)
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
                signal_data={"model_fair": round(model_fair, 4), "beta": BETA_FACTOR,
                             "edge": round(model_fair - price, 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis=f"ETH-BTC beta lag", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi ETH-BTC Beta Trader")
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

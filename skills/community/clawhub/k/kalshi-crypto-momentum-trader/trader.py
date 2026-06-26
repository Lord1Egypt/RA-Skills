#!/usr/bin/env python3
"""
Kalshi Crypto Momentum Trader

Uses 7-day and 30-day price trend extrapolation to trade crypto year-end
price target markets on Kalshi.

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
import re
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
    "entry_edge":        {"env": "SIMMER_CRYPTO_MOM_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_CRYPTO_MOM_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_CRYPTO_MOM_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_CRYPTO_MOM_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_CRYPTO_MOM_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_CRYPTO_MOM_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-crypto-momentum-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-crypto-mom"
SKILL_SLUG = "kalshi-crypto-momentum-trader"
_automaton_reported = False

MIN_SHARES_PER_ORDER = 1.0

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

SEARCH_TERMS = ["bitcoin", "BTC price", "ETH price", "ethereum", "crypto"]
FILTER_KWS = ["bitcoin", "btc", "ethereum", "eth"]
FILTER_KWS2 = ["above", "over", "exceed", "reach", "price", "year-end"]

# =============================================================================
# Momentum Model
# =============================================================================

MOMENTUM_PARAMS = {
    "BTC": {"avg_daily_return": 0.0012, "daily_vol": 0.035, "trend_7d": 0.05, "trend_30d": 0.12},
    "ETH": {"avg_daily_return": 0.0015, "daily_vol": 0.045, "trend_7d": 0.04, "trend_30d": 0.10},
}

CURRENT_PRICES = {"BTC": 95000.0, "ETH": 3500.0}

ASSET_PATTERN = re.compile(r"\b(bitcoin|btc|ethereum|eth|ether)\b", re.IGNORECASE)
PRICE_PATTERN = re.compile(
    r"(?:above|over|exceed|reach|hit|at least)\s*\$?([\d,]+(?:\.\d+)?)", re.IGNORECASE,
)


def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def extract_asset(question):
    m = ASSET_PATTERN.search(question)
    if not m:
        return None
    token = m.group(1).lower()
    if token in ("bitcoin", "btc"):
        return "BTC"
    if token in ("ethereum", "eth", "ether"):
        return "ETH"
    return None


def extract_price_level(question):
    m = PRICE_PATTERN.search(question)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def momentum_fair_prob(asset, target_level, days_to_expiry=270):
    params = MOMENTUM_PARAMS.get(asset, MOMENTUM_PARAMS["BTC"])
    current_price = CURRENT_PRICES.get(asset, 95000.0)
    trend = params["trend_30d"]
    daily_vol = params["daily_vol"]
    projected_price = current_price * (1 + trend) ** (days_to_expiry / 30)
    vol_to_expiry = daily_vol * math.sqrt(days_to_expiry)
    if vol_to_expiry <= 0:
        return 1.0 if projected_price >= target_level else 0.0
    z = math.log(projected_price / target_level) / vol_to_expiry
    return normal_cdf(z)


def is_relevant_market(question):
    q = question.lower()
    return any(kw in q for kw in FILTER_KWS) and any(kw in q for kw in FILTER_KWS2)


# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


# =============================================================================
# Simmer Client
# =============================================================================

def get_client(live=True):
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
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "kalshi")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    client = get_client()
    imported = 0
    seen = set()

    for term in SEARCH_TERMS:
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
            if not is_relevant_market(question):
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


def fetch_markets():
    all_markets = []
    for term in SEARCH_TERMS:
        try:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": term, "limit": 50}
            )
            markets = result.get("markets", [])
            for m in markets:
                if is_relevant_market(m.get("question", "")):
                    all_markets.append(m)
        except Exception as e:
            safe_print(f"  Failed to fetch markets for '{term}': {e}")

    seen = set()
    unique = []
    for m in all_markets:
        mid = m.get("id")
        if mid and mid not in seen:
            seen.add(mid)
            unique.append(m)
    return unique


# =============================================================================
# Context & Safeguards
# =============================================================================

def get_market_context(market_id, my_probability=None):
    try:
        if my_probability is not None:
            return get_client()._request(
                "GET", f"/api/sdk/context/{market_id}",
                params={"my_probability": my_probability}
            )
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def check_safeguards(context):
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

def execute_trade(market_id, side, amount, reasoning="", signal_data=None):
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
            reasoning=reasoning, signal_data=signal_data,
        )
        return {
            "success": result.success, "trade_id": result.trade_id,
            "shares_bought": result.shares_bought, "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}


def get_positions():
    try:
        result = get_client()._request("GET", "/api/sdk/positions")
        return result.get("positions", []) if isinstance(result, dict) else result
    except Exception:
        return []


def check_exits(dry_run, log=print):
    positions = get_positions()
    if not positions:
        return 0, 0
    my_pos = [p for p in positions
              if TRADE_SOURCE in p.get("sources", [])
              or is_relevant_market(p.get("question", ""))]
    if not my_pos:
        return 0, 0
    log(f"\n  Checking {len(my_pos)} positions for exit...")
    found, executed = 0, 0
    for pos in my_pos:
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
                result = execute_trade(market_id, "sell", shares,
                    reasoning=f"Exit: price {price:.2f} >= threshold {EXIT_THRESHOLD:.2f}")
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

def run_strategy(dry_run=True, positions_only=False, show_config=False, quiet=False):
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Crypto Momentum Trader (7d/30d Trend Extrapolation)")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        return

    get_client(live=not dry_run)

    if positions_only:
        positions = get_positions()
        my_pos = [p for p in positions if is_relevant_market(p.get("question", ""))]
        if not my_pos:
            log("  No positions")
        for p in my_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    log("Discovering crypto markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    markets = fetch_markets()
    log(f"  Found {len(markets)} active crypto markets")

    if not markets:
        log("  No crypto markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # Display momentum parameters
    log("\nMomentum Parameters:")
    for asset, params in MOMENTUM_PARAMS.items():
        log(f"  {asset}: 7d={params['trend_7d']:+.0%}  30d={params['trend_30d']:+.0%}  vol={params['daily_vol']:.1%}/day")

    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        asset = extract_asset(question)
        level = extract_price_level(question)
        if not asset or level is None:
            continue

        model_p = momentum_fair_prob(asset, level)
        edge = model_p - price

        log(f"  {asset}>${level:,.0f}: market={price:.1%}  momentum={model_p:.1%}  edge={edge:+.1%}")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

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
                reasoning=f"Momentum: {asset}>${level:,.0f} market={price:.1%} model={model_p:.1%} edge={edge:+.1%}",
                signal_data={"model_prob": round(model_p, 4), "asset": asset,
                             "target_level": level, "edge": round(edge, 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis=f"Momentum edge on {asset}", action="buy")
            else:
                log(f"    Trade failed: {result.get('error')}", force=True)
        else:
            log(f"    [DRY RUN] Would buy {side.upper()} ${size:.2f}")
            trades_executed += 1
            total_usd += size

    exits_found, exits_exec = check_exits(dry_run, log=log)

    log(f"\n  Signals: {signals}  Trades: {trades_executed}  USD: ${total_usd:.2f}")
    if exits_found:
        log(f"  Exits: {exits_found} found, {exits_exec} executed")

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
    parser = argparse.ArgumentParser(description="Kalshi Crypto Momentum Trader")
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

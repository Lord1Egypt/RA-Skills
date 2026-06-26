#!/usr/bin/env python3
"""
SOL 5m MTF Momentum — Multi-Timeframe CEX Momentum for Polymarket Fast Markets

Reads 1m/3m/5m Binance SOL/USDT returns, votes on direction,
and trades Polymarket 5-minute fast markets when conviction is high.

Usage:
    python mtf_momentum.py              # Dry run
    python mtf_momentum.py --live       # Real trades
    python mtf_momentum.py --positions  # Show positions
    python mtf_momentum.py --config     # Show config

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import math
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Force line-buffered stdout (required for cron/Docker/OpenClaw visibility)
sys.stdout.reconfigure(line_buffering=True)

from simmer_sdk.skill import load_config, update_config, get_config_path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SKILL_SLUG = "polymarket-sol-5m-mtf-momentum-dyll"
TRADE_SOURCE = "sdk:sol-mtf-momentum"
ASSET = "SOL"
BINANCE_SYMBOL = "SOLUSDT"

CONFIG_SCHEMA = {
    "conf_min": {"env": "SIMMER_MTF_CONF_MIN", "default": 0.50, "type": float},
    "conf_scale": {"env": "SIMMER_MTF_CONF_SCALE", "default": 3.0, "type": float},
    "eval_min_age": {"env": "SIMMER_MTF_EVAL_MIN_AGE", "default": 90, "type": int},
    "eval_max_age": {"env": "SIMMER_MTF_EVAL_MAX_AGE", "default": 180, "type": int},
    "trade_size": {"env": "SIMMER_MTF_TRADE_SIZE", "default": 10, "type": float},
    "max_trades_per_run": {"env": "SIMMER_MTF_MAX_TRADES", "default": 1, "type": int},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONF_MIN = _config["conf_min"]
CONF_SCALE = _config["conf_scale"]
EVAL_MIN_AGE = _config["eval_min_age"]
EVAL_MAX_AGE = _config["eval_max_age"]
TRADE_SIZE = _config["trade_size"]
MAX_TRADES_PER_RUN = _config["max_trades_per_run"]

MIN_SHARES_PER_ORDER = 5.0
MIN_TICK_SIZE = 0.01
SLIPPAGE_MAX_PCT = 0.15

SIMMER_API_URL = os.environ.get("SIMMER_API_URL", "https://api.simmer.markets")
BINANCE_KLINE_URL = "https://api.binance.com/api/v3/klines"

# ---------------------------------------------------------------------------
# SimmerClient singleton
# ---------------------------------------------------------------------------

_client = None


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
        venue = os.environ.get("TRADING_VENUE", "sim")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# ---------------------------------------------------------------------------
# SDK wrappers
# ---------------------------------------------------------------------------

def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception as e:
        print(f"  Portfolio fetch failed: {e}")
        return None


def get_positions():
    try:
        positions = get_client().get_positions()
        from dataclasses import asdict
        return [asdict(p) for p in positions]
    except Exception as e:
        print(f"  Error fetching positions: {e}")
        return []


def get_market_context(market_id):
    try:
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def check_context_safeguards(context):
    """Check context for deal-breakers. Returns (should_trade, reasons)."""
    if not context:
        return True, []

    reasons = []
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})
    slippage = context.get("slippage", {})

    for warning in warnings:
        if "MARKET RESOLVED" in str(warning).upper():
            return False, ["Market already resolved"]

    warning_level = discipline.get("warning_level", "none")
    if warning_level == "severe":
        return False, [f"Severe flip-flop warning: {discipline.get('flip_flop_warning', '')}"]
    elif warning_level == "mild":
        reasons.append("Mild flip-flop warning (proceed with caution)")

    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slippage_pct = estimates[0].get("slippage_pct", 0)
        if slippage_pct > SLIPPAGE_MAX_PCT:
            return False, [f"Slippage too high: {slippage_pct:.1%}"]

    return True, reasons


def execute_trade(market_id, side, amount, reasoning=""):
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, reasoning=reasoning,
            skill_slug=SKILL_SLUG,
        )
        return {
            "success": result.success, "trade_id": result.trade_id,
            "shares_bought": result.shares_bought, "shares": result.shares_bought,
            "error": result.error, "simulated": result.simulated,
            "skip_reason": getattr(result, "skip_reason", None),
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Binance klines
# ---------------------------------------------------------------------------

def fetch_binance_klines(symbol, interval="1m", limit=15):
    """Fetch recent klines from Binance. Returns list of [open_time, o, h, l, c, ...]."""
    url = f"{BINANCE_KLINE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        req = Request(url, headers={"User-Agent": "SimmerMTFMomentum/1.0"})
        data = json.loads(urlopen(req, timeout=10).read())
        return data
    except Exception as e:
        print(f"  Binance kline fetch failed: {e}")
        return []


def compute_mtf_signal(klines):
    """
    Compute multi-timeframe momentum signal from 1m klines.

    Returns (direction, confidence, details_dict) or (None, 0, details_dict).
    """
    if len(klines) < 10:
        return None, 0.0, {"error": "insufficient klines"}

    # Extract close prices
    closes = [float(k[4]) for k in klines]

    # Returns
    r1 = (closes[-1] - closes[-2]) / closes[-2]  # 1m return
    r3 = (closes[-1] - closes[-4]) / closes[-4]  # 3m return
    r5 = (closes[-1] - closes[-6]) / closes[-6]  # 5m return

    # Majority vote on direction; r5 is tiebreaker
    votes = [
        1 if r1 > 0 else (-1 if r1 < 0 else 0),
        1 if r3 > 0 else (-1 if r3 < 0 else 0),
        1 if r5 > 0 else (-1 if r5 < 0 else 0),
    ]
    vote_sum = sum(votes)

    if vote_sum > 0:
        direction = "up"
    elif vote_sum < 0:
        direction = "down"
    else:
        # Tie — use r5 as tiebreaker
        if r5 > 0:
            direction = "up"
        elif r5 < 0:
            direction = "down"
        else:
            return None, 0.0, {"r1": r1, "r3": r3, "r5": r5, "reason": "flat"}

    # Volatility: stdev of last 10 1m returns
    recent_returns = []
    for i in range(-10, 0):
        ret = (closes[i] - closes[i - 1]) / closes[i - 1]
        recent_returns.append(ret)

    mean_ret = sum(recent_returns) / len(recent_returns)
    variance = sum((r - mean_ret) ** 2 for r in recent_returns) / len(recent_returns)
    vol = math.sqrt(variance) if variance > 0 else 1e-9

    # Confidence
    confidence = min(1.0, (abs(r3) + abs(r5)) / 2.0 / (vol * CONF_SCALE))

    aligned = sum(1 for v in votes if (v > 0 if direction == "up" else v < 0))

    details = {
        "r1": r1, "r3": r3, "r5": r5,
        "vol": vol, "confidence": confidence,
        "direction": direction, "aligned": aligned,
        "votes": votes,
    }
    return direction, confidence, details


# ---------------------------------------------------------------------------
# Fast market discovery
# ---------------------------------------------------------------------------

def fetch_fast_markets():
    """Fetch active fast markets for the configured asset from Simmer API."""
    try:
        api_key = os.environ.get("SIMMER_API_KEY", "")
        req = Request(
            f"{SIMMER_API_URL}/api/sdk/fast-markets?asset={ASSET}&window=5m&limit=10",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        data = json.loads(urlopen(req, timeout=10).read())
        return data.get("markets", [])
    except Exception as e:
        print(f"  Failed to fetch fast markets: {e}")
        return []


def get_market_age(market):
    """Get market age in seconds. Returns None if can't determine."""
    resolves_at = market.get("resolves_at", "")
    if not resolves_at:
        return None
    try:
        res_dt = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        remaining = (res_dt - now).total_seconds()
        # 5m market = 300s total
        age = 300 - remaining
        return age
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Main strategy
# ---------------------------------------------------------------------------

def run_strategy(dry_run=True, positions_only=False, show_config=False,
                 use_safeguards=True, quiet=False):
    """Run the MTF momentum strategy."""
    print(f"⚡ {ASSET} 5m MTF Momentum")
    print("=" * 50)

    get_client(live=not dry_run)

    if dry_run and not quiet:
        print("\n  [PAPER MODE] Use --live for real trades.")

    if not quiet:
        print(f"\n  Config: conf_min={CONF_MIN} conf_scale={CONF_SCALE} "
              f"eval_window={EVAL_MIN_AGE}-{EVAL_MAX_AGE}s size=${TRADE_SIZE}")

    if show_config:
        print("\n  Configuration:")
        for key, schema in CONFIG_SCHEMA.items():
            print(f"    {key} = {_config[key]} (env: {schema['env']}, default: {schema['default']})")
        return

    if positions_only:
        positions = get_positions()
        source_positions = [p for p in positions if TRADE_SOURCE in (p.get("sources") or [])]
        if not source_positions:
            print("\n  No active positions from this skill.")
        else:
            print(f"\n  Active positions ({len(source_positions)}):")
            for p in source_positions:
                q = (p.get("question") or "")[:50]
                pnl = p.get("pnl", 0)
                print(f"    {q}... PnL: ${pnl:+.2f}")
        return

    # --- Fetch CEX signal ---
    if not quiet:
        print(f"\n  Fetching {BINANCE_SYMBOL} 1m klines...")

    klines = fetch_binance_klines(BINANCE_SYMBOL, interval="1m", limit=15)
    if not klines:
        print("  ❌ Failed to fetch klines. Aborting.")
        return

    direction, confidence, details = compute_mtf_signal(klines)

    if not quiet:
        r1 = details.get("r1", 0)
        r3 = details.get("r3", 0)
        r5 = details.get("r5", 0)
        aligned = details.get("aligned", 0)
        print(f"  r1={r1:+.4%} r3={r3:+.4%} r5={r5:+.4%}")

    if direction is None:
        if not quiet:
            print("  ⏸ No directional signal (flat). Skipping.")
        return

    if not quiet:
        arrow = "↑" if direction == "up" else "↓"
        print(f"  Direction: {direction.upper()} {arrow} ({details['aligned']}/3 aligned) "
              f"conf={confidence:.2f}")

    if confidence < CONF_MIN:
        if not quiet:
            print(f"  ⏸ Confidence {confidence:.2f} < {CONF_MIN}. Skipping.")
        return

    # --- Find fast markets ---
    if not quiet:
        print(f"\n  Fetching {ASSET} 5m fast markets...")

    markets = fetch_fast_markets()
    if not markets:
        if not quiet:
            print(f"  No active {ASSET} 5m fast markets found.")
        return

    if not quiet:
        print(f"  Found {len(markets)} active market(s)")

    # --- Evaluate and trade ---
    signals_found = 0
    trades_attempted = 0
    trades_executed = 0
    skip_reasons = []
    execution_errors = []

    for market in markets:
        market_id = market.get("id")
        question = market.get("question", "")

        # Check market age
        age = get_market_age(market)
        if age is None:
            if not quiet:
                print(f"\n  📊 {question[:60]}")
                print("     Could not determine market age. Skipping.")
            continue

        if age < EVAL_MIN_AGE or age > EVAL_MAX_AGE:
            if not quiet:
                print(f"\n  📊 {question[:60]}")
                print(f"     Market age: {age:.0f}s (outside {EVAL_MIN_AGE}-{EVAL_MAX_AGE}s window). Skipping.")
            continue

        if not quiet:
            print(f"\n  📊 {question[:60]}")
            print(f"     Market age: {age:.0f}s (in eval window)")
            print(f"     r1={details['r1']:+.4%} r3={details['r3']:+.4%} "
                  f"r5={details['r5']:+.4%} → {direction.upper()} "
                  f"({details['aligned']}/3 aligned)")
            print(f"     vol={details['vol']:.6f} conf={confidence:.2f} ✅ TRADE")

        signals_found += 1

        # Determine side
        side = "yes" if direction == "up" else "no"

        # Safeguards
        if use_safeguards:
            context = get_market_context(market_id)
            should_trade, reasons = check_context_safeguards(context)
            if not should_trade:
                if not quiet:
                    print(f"     ⛔ Safeguard blocked: {'; '.join(reasons)}")
                skip_reasons.append("; ".join(reasons))
                continue

        # Rate limit
        if trades_executed >= MAX_TRADES_PER_RUN:
            if not quiet:
                print("     ⏸ Max trades per run reached.")
            skip_reasons.append("max_trades_reached")
            continue

        # Execute
        reasoning = (f"MTF momentum aligned {direction.upper()} "
                     f"(conf={confidence:.2f}, {details['aligned']}/3 timeframes, "
                     f"r5={details['r5']:+.4%})")

        trades_attempted += 1
        result = execute_trade(market_id, side, TRADE_SIZE, reasoning=reasoning)

        if result.get("success"):
            trades_executed += 1
            shares = result.get("shares_bought") or result.get("shares", 0)
            sim_tag = "Paper trade" if result.get("simulated") else "LIVE trade"
            if not quiet:
                print(f"     → BUY {side.upper()} ${TRADE_SIZE:.2f} | {reasoning}")
                print(f"     ✅ {sim_tag} executed ({shares:.1f} shares)")
        elif result.get("skip_reason"):
            skip_reasons.append(result["skip_reason"])
            if not quiet:
                print(f"     ⏸ Skipped: {result['skip_reason']}")
        elif result.get("error"):
            execution_errors.append(result["error"])
            if not quiet:
                print(f"     ❌ Error: {result['error']}")

    # Summary
    if not quiet:
        print(f"\n  Summary: {signals_found} signal(s), {trades_executed} trade(s)")

    # Automaton report
    if os.environ.get("AUTOMATON_MANAGED"):
        report = {
            "signals": signals_found,
            "trades_attempted": trades_attempted,
            "trades_executed": trades_executed,
        }
        if skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        if execution_errors:
            report["execution_errors"] = execution_errors
        print(json.dumps({"automaton": report}))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{ASSET} 5m MTF Momentum")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--dry-run", action="store_true", help="(Default) Dry run")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value")
    parser.add_argument("--no-safeguards", action="store_true",
                        help="Disable safeguards")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Only output on trades/errors")
    args = parser.parse_args()

    # Handle --set
    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    type_fn = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        value = type_fn(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            updated = update_config(updates, __file__)
            print(f"Config updated: {updates}")
            print(f"Saved to: {get_config_path(__file__)}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

    dry_run = not args.live

    run_strategy(
        dry_run=dry_run,
        positions_only=args.positions,
        show_config=args.config,
        use_safeguards=not args.no_safeguards,
        quiet=args.quiet,
    )

    # Fallback report for automaton if the strategy returned early (no signal)
    if os.environ.get("AUTOMATON_MANAGED"):
        print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0,
                                        "trades_executed": 0, "skip_reason": "no_signal"}}))

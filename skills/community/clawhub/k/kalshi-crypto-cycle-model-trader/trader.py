#!/usr/bin/env python3
"""
Kalshi Crypto Cycle Model Trader

Trades Bitcoin year-end price markets on Kalshi using Bitcoin's 4-year halving
cycle pattern to compute fair price probabilities. Post-halving ROI history:
cycle1=100x, cycle2=30x, cycle3=8x, cycle4=~3x (current). April 2024 halving
means we are in year 2 of cycle 4.

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
    "entry_edge":        {"env": "SIMMER_CRYPTO_CYCLE_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_CRYPTO_CYCLE_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_CRYPTO_CYCLE_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_CRYPTO_CYCLE_MAX_TRADES_PER_RUN","default": 5,     "type": int},
    "slippage_max":      {"env": "SIMMER_CRYPTO_CYCLE_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_CRYPTO_CYCLE_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-crypto-cycle-model-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-crypto-cycle"
SKILL_SLUG = "kalshi-crypto-cycle-model-trader"
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
# Bitcoin Halving Cycle Model
# =============================================================================

# Historical halving data
# Halving 1: Nov 2012 — pre-halving price ~$12,   peak ~$1,200  (100x)
# Halving 2: Jul 2016 — pre-halving price ~$650,  peak ~$20,000 (30x)
# Halving 3: May 2020 — pre-halving price ~$8,500, peak ~$69,000 (8x)
# Halving 4: Apr 2024 — pre-halving price ~$64,000, projected peak ~$180k-200k (3x)

HALVING_DATE = datetime(2024, 4, 20, tzinfo=timezone.utc)
HALVING_PRICE_USD = 64000.0

# Cycle 4 projected ROI multiplier (conservative based on diminishing returns)
CYCLE_4_PEAK_MULTIPLIER = 3.0
CYCLE_4_PEAK_PRICE = HALVING_PRICE_USD * CYCLE_4_PEAK_MULTIPLIER  # ~$192,000

# Year-in-cycle expected return profile (fraction of peak reached)
# Based on historical pattern: year 1 = accumulation, year 2 = breakout, year 3 = peak, year 4 = bear
CYCLE_YEAR_PROFILE = {
    1: 0.40,   # Year 1 post-halving: 40% of peak move realized
    2: 0.75,   # Year 2 post-halving: 75% of peak move realized (we are here)
    3: 1.00,   # Year 3 post-halving: peak (historically Q4)
    4: 0.35,   # Year 4 post-halving: bear market retracement
}

# Expected year-end 2026 price range parameters
# We are in year 2 (Apr 2024 + ~2 years = Apr 2026)
# By end of 2026, entering year 3 territory
CURRENT_CYCLE_YEAR = 2
YEAR_END_FRACTION = 0.85  # Between year 2 (0.75) and year 3 (1.00) by Dec 2026

# Model price distribution parameters
MODEL_EXPECTED_PRICE = HALVING_PRICE_USD + (CYCLE_4_PEAK_PRICE - HALVING_PRICE_USD) * YEAR_END_FRACTION
MODEL_VOLATILITY = 0.45  # Annualized vol for BTC (reduced in cycle maturity)


def lognormal_cdf(x, mu, sigma):
    """CDF of lognormal distribution."""
    if x <= 0:
        return 0.0
    z = (math.log(x) - mu) / sigma
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def compute_bin_probability(lower, upper):
    """Compute probability that BTC year-end price falls in [lower, upper].

    Uses lognormal model calibrated from halving cycle analysis.
    """
    mu = math.log(MODEL_EXPECTED_PRICE) - 0.5 * MODEL_VOLATILITY ** 2
    sigma = MODEL_VOLATILITY

    p_upper = lognormal_cdf(upper, mu, sigma) if upper < float('inf') else 1.0
    p_lower = lognormal_cdf(lower, mu, sigma) if lower > 0 else 0.0

    return p_upper - p_lower


def parse_price_bin(question: str) -> tuple:
    """Extract price bin boundaries from market question.

    Handles patterns like:
    - "Bitcoin above $100,000 on December 31?"
    - "Bitcoin between $100,000 and $150,000?"
    - "Bitcoin below $50,000?"
    - "BTC price $100k-$150k?"
    """
    q = question.lower().replace(",", "").replace("$", "").replace("k", "000")

    # Try "above X" / "at least X" / "over X"
    for pat in ["above ", "at least ", "over ", "higher than ", "> "]:
        if pat in q:
            try:
                idx = q.index(pat) + len(pat)
                num_str = ""
                for c in q[idx:]:
                    if c.isdigit() or c == ".":
                        num_str += c
                    elif num_str:
                        break
                if num_str:
                    return (float(num_str), float('inf'))
            except (ValueError, IndexError):
                pass

    # Try "below X" / "under X" / "less than X"
    for pat in ["below ", "under ", "less than ", "< "]:
        if pat in q:
            try:
                idx = q.index(pat) + len(pat)
                num_str = ""
                for c in q[idx:]:
                    if c.isdigit() or c == ".":
                        num_str += c
                    elif num_str:
                        break
                if num_str:
                    return (0, float(num_str))
            except (ValueError, IndexError):
                pass

    # Try "between X and Y"
    if "between" in q:
        try:
            parts = q.split("between")[1].split("and")
            if len(parts) == 2:
                lo = float("".join(c for c in parts[0] if c.isdigit() or c == "."))
                hi = float("".join(c for c in parts[1] if c.isdigit() or c == "."))
                return (lo, hi)
        except (ValueError, IndexError):
            pass

    # Try extracting two numbers separated by dash or "to"
    import re
    nums = re.findall(r'[\d.]+', q)
    if len(nums) >= 2:
        # Heuristic: look for price-like numbers (>1000 for BTC)
        prices = [float(n) for n in nums if float(n) > 1000]
        if len(prices) >= 2:
            return (min(prices), max(prices))

    return None


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
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover Bitcoin price markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["bitcoin", "BTC price"]:
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
            # Filter for BTC price markets
            if not any(kw in question for kw in ["bitcoin", "btc"]):
                continue
            if not any(kw in question for kw in ["price", "above", "below", "between", "end of"]):
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


def fetch_btc_markets():
    """Fetch active BTC price markets from Simmer API."""
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "bitcoin", "limit": 50}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if any(kw in (m.get("question") or "").lower() for kw in ["bitcoin", "btc"])
                and any(kw in (m.get("question") or "").lower() for kw in ["price", "above", "below", "between"])]
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
    """Check open BTC cycle positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    btc_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or any(kw in (p.get("question") or "").lower() for kw in ["bitcoin", "btc"])]

    if not btc_pos:
        return 0, 0

    log(f"\n  Checking {len(btc_pos)} BTC cycle positions for exit...")
    found, executed = 0, 0

    for pos in btc_pos:
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
    """Run the Bitcoin halving cycle model trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Bitcoin Halving Cycle Model Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Cycle 4 expected price (EOY 2026): ${MODEL_EXPECTED_PRICE:,.0f}")
    log(f"  Model volatility: {MODEL_VOLATILITY:.0%}")
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
        btc = [p for p in positions
               if any(kw in (p.get("question") or "").lower() for kw in ["bitcoin", "btc"])]
        if not btc:
            log("  No BTC cycle positions")
        for p in btc:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Model info ---
    log("Halving Cycle Model:")
    log(f"  Halving date: {HALVING_DATE.date()}")
    log(f"  Halving price: ${HALVING_PRICE_USD:,.0f}")
    log(f"  Cycle 4 peak multiplier: {CYCLE_4_PEAK_MULTIPLIER}x -> ${CYCLE_4_PEAK_PRICE:,.0f}")
    log(f"  Current cycle year: {CURRENT_CYCLE_YEAR}")
    log(f"  Year-end fraction: {YEAR_END_FRACTION:.0%} of peak move")
    log(f"  Model expected EOY price: ${MODEL_EXPECTED_PRICE:,.0f}")
    log("")

    # Sample bin probabilities for display
    test_bins = [
        (0, 50000), (50000, 75000), (75000, 100000), (100000, 125000),
        (125000, 150000), (150000, 200000), (200000, 300000), (300000, float('inf'))
    ]
    log("Model bin probabilities:")
    for lo, hi in test_bins:
        p = compute_bin_probability(lo, hi)
        hi_str = f"${hi:,.0f}" if hi < float('inf') else "inf"
        log(f"  ${lo:>9,.0f} - {hi_str:>10}: {p:6.1%}")
    log("")

    # --- Discovery ---
    log("Discovering BTC price markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_btc_markets()
    log(f"  Found {len(markets)} active BTC price markets")

    if not markets:
        log("  No BTC price markets available")
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

        bin_range = parse_price_bin(question)
        if not bin_range:
            log(f"  ? Cannot parse bin: {question[:60]}")
            continue

        lo, hi = bin_range
        model_p = compute_bin_probability(lo, hi)
        edge = model_p - price

        hi_str = f"${hi:,.0f}" if hi < float('inf') else "inf"
        log(f"  ${lo:,.0f}-{hi_str}: market={price:.1%}  model={model_p:.1%}  edge={edge:+.1%}")

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
                reasoning=f"Cycle model: bin=${lo:,.0f}-{hi_str} market={price:.1%} model={model_p:.1%} edge={edge:+.1%}",
                signal_data={"model_prob": round(model_p, 4), "bin_lower": lo,
                             "bin_upper": hi if hi < float('inf') else 999999,
                             "edge": round(edge, 4), "cycle_year": CURRENT_CYCLE_YEAR},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis=f"Cycle model edge on BTC bin", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi Crypto Cycle Model Trader")
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

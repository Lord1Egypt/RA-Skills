#!/usr/bin/env python3
"""
Kalshi ETH Merge Momentum Trader

Post-merge Ethereum burns ~0.5% of supply annually via EIP-1559, making ETH
structurally deflationary. This skill computes a deflation-adjusted fair value
for ETH price markets and trades when markets underprice the supply reduction.

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
    "entry_edge":        {"env": "SIMMER_ETH_MERGE_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ETH_MERGE_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ETH_MERGE_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ETH_MERGE_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_ETH_MERGE_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ETH_MERGE_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
    "annual_burn_pct":   {"env": "SIMMER_ETH_MERGE_BURN_PCT",          "default": 0.5,   "type": float},
    "base_eth_price":    {"env": "SIMMER_ETH_MERGE_BASE_PRICE",        "default": 3500.0,"type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-eth-merge-momentum-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-eth-merge"
SKILL_SLUG = "kalshi-eth-merge-momentum-trader"
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
ANNUAL_BURN_PCT = _config["annual_burn_pct"]
BASE_ETH_PRICE = _config["base_eth_price"]
TIME_TO_RESOLUTION_MIN_HOURS = 2


# =============================================================================
# Merge Deflation Model
# =============================================================================

# ETH supply dynamics post-merge
TOTAL_ETH_SUPPLY = 120_000_000  # Approximate current supply
ANNUAL_ISSUANCE_PCT = 0.5       # ~0.5% new issuance to stakers
# Net supply change = issuance - burn
# If burn > issuance, ETH is deflationary

# Merge momentum factors
MERGE_MOMENTUM_FACTORS = {
    "deflation_active": {
        "description": "Net supply decreasing (burn > issuance)",
        "price_bias_pct": 3.0,
    },
    "neutral": {
        "description": "Net supply roughly flat",
        "price_bias_pct": 0.0,
    },
    "inflationary": {
        "description": "Net supply increasing (low gas = low burn)",
        "price_bias_pct": -2.0,
    },
}


def compute_deflation_adjusted_price(base_price: float, annual_burn_pct: float,
                                      days_to_resolution: int) -> float:
    """Compute deflation-adjusted fair ETH price.

    If ETH burns 0.5% annually with 0.5% issuance, net change depends on
    gas levels. During active burn periods, price should be higher.

    Simple model: fair_price = base * (1 + net_deflation_rate * days/365)
    """
    net_deflation_rate = (annual_burn_pct - ANNUAL_ISSUANCE_PCT) / 100.0
    day_fraction = days_to_resolution / 365.0

    # If net deflationary, price should appreciate
    # Conservative: apply half the theoretical impact
    adjustment = 1.0 + (net_deflation_rate * day_fraction * 0.5)
    return base_price * max(0.9, adjustment)


def extract_price_target(question: str) -> float | None:
    """Extract price target from market question."""
    q = question.lower().replace(",", "")
    words = q.split()

    for i, word in enumerate(words):
        if word.startswith("$"):
            try:
                val = float(word.replace("$", "").replace("k", "000"))
                if val > 100:
                    return val
            except ValueError:
                continue

    for keyword in ["above", "below", "over", "under", "higher", "lower"]:
        if keyword in q:
            idx = q.index(keyword) + len(keyword)
            remaining = q[idx:].strip().split()
            for word in remaining[:3]:
                word = word.replace("$", "").replace("k", "000").replace(",", "")
                try:
                    val = float(word)
                    if val > 100:
                        return val
                except ValueError:
                    continue

    return None


def compute_merge_fair_probability(price_target: float, adjusted_price: float) -> float:
    """Compute fair probability that ETH exceeds target given deflation model.

    Uses a simple logistic model centered on the adjusted price.
    """
    if price_target <= 0 or adjusted_price <= 0:
        return 0.5

    ratio = price_target / adjusted_price

    # Logistic curve: P(above target) = 1 / (1 + exp(k * (ratio - 1)))
    k = 5.0  # Steepness parameter
    try:
        prob = 1.0 / (1.0 + math.exp(k * (ratio - 1.0)))
    except OverflowError:
        prob = 0.01 if ratio > 1 else 0.99

    return max(0.01, min(0.99, prob))


def estimate_days_to_resolution(resolves_at: str) -> int:
    """Estimate days until market resolution."""
    if not resolves_at:
        return 30
    try:
        resolves = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
        days = (resolves - datetime.now(timezone.utc)).days
        return max(1, days)
    except Exception:
        return 30


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
    """Check open ETH merge positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    eth_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or "eth" in (p.get("question") or "").lower()]

    if not eth_pos:
        return 0, 0

    log(f"\n  Checking {len(eth_pos)} ETH merge positions for exit...")
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
    """Run the ETH merge momentum deflation trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("ETH Merge Momentum Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Annual burn: {ANNUAL_BURN_PCT:.1f}%  Base ETH price: ${BASE_ETH_PRICE:.0f}")
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
            log("  No ETH merge positions")
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

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        # Extract price target
        price_target = extract_price_target(question)
        if price_target is None:
            log(f"  ? No price target: {question[:60]}")
            continue

        # Compute deflation-adjusted fair price
        days = estimate_days_to_resolution(m.get("resolves_at", ""))
        adj_price = compute_deflation_adjusted_price(BASE_ETH_PRICE, ANNUAL_BURN_PCT, days)
        fair_prob = compute_merge_fair_probability(price_target, adj_price)

        log(f"  {question[:50]}  target=${price_target:.0f}  adj=${adj_price:.0f}  "
            f"fair={fair_prob:.1%}  mkt={price:.1%}")

        side, size, reasoning = compute_signal(m, fair_prob)

        if side is None:
            continue

        signals += 1

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=fair_prob if side == "yes" else 1 - fair_prob)
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
                signal_data={"fair_prob": round(fair_prob, 4), "adj_price": round(adj_price, 2),
                             "price_target": price_target, "burn_pct": ANNUAL_BURN_PCT},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis="ETH merge deflation", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi ETH Merge Momentum Trader")
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

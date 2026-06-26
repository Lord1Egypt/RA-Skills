#!/usr/bin/env python3
"""
Kalshi Crypto Monotonicity Trader

Enforces the monotonicity constraint on crypto price-level markets:
P(BTC > $110k) >= P(BTC > $120k) ALWAYS. When this is violated, buy the
cheaper higher-probability contract and sell the overpriced lower one.

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
    "violation_threshold": {"env": "SIMMER_CRYPTO_MONO_VIOLATION_THRESHOLD", "default": 0.03, "type": float},
    "exit_threshold":      {"env": "SIMMER_CRYPTO_MONO_EXIT_THRESHOLD",      "default": 0.45, "type": float},
    "max_position_usd":    {"env": "SIMMER_CRYPTO_MONO_MAX_POSITION_USD",    "default": 5.00, "type": float},
    "max_trades_per_run":  {"env": "SIMMER_CRYPTO_MONO_MAX_TRADES_PER_RUN",  "default": 3,    "type": int},
    "slippage_max":        {"env": "SIMMER_CRYPTO_MONO_SLIPPAGE_MAX",        "default": 0.15, "type": float},
    "min_liquidity":       {"env": "SIMMER_CRYPTO_MONO_MIN_LIQUIDITY",       "default": 0.0,  "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-crypto-monotonicity-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-crypto-mono"
SKILL_SLUG = "kalshi-crypto-monotonicity-trader"
_automaton_reported = False

# Kalshi constraints
MIN_SHARES_PER_ORDER = 1.0

# Strategy parameters from config
VIOLATION_THRESHOLD = _config["violation_threshold"]
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
# Monotonicity Logic
# =============================================================================

# Search terms for market discovery
SEARCH_TERMS = ["bitcoin", "BTC price", "ETH price", "ethereum", "crypto"]

# Pattern to extract price levels from market questions
# e.g. "Will Bitcoin be above $110,000?" -> 110000
PRICE_PATTERN = re.compile(
    r"(?:above|over|exceed|reach|hit|at least)\s*\$?([\d,]+(?:\.\d+)?)",
    re.IGNORECASE,
)

ASSET_PATTERN = re.compile(
    r"\b(bitcoin|btc|ethereum|eth|ether)\b", re.IGNORECASE
)


def extract_asset(question: str) -> str | None:
    """Extract which crypto asset a market question refers to."""
    m = ASSET_PATTERN.search(question)
    if not m:
        return None
    token = m.group(1).lower()
    if token in ("bitcoin", "btc"):
        return "BTC"
    if token in ("ethereum", "eth", "ether"):
        return "ETH"
    return None


def extract_price_level(question: str) -> float | None:
    """Extract the dollar price level from a market question."""
    m = PRICE_PATTERN.search(question)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def find_monotonicity_violations(markets: list[dict]) -> list[dict]:
    """Find pairs of markets that violate P(X > A) >= P(X > B) when A < B.

    Returns a list of violation dicts with the cheaper/overpriced market info.
    """
    # Group markets by asset
    by_asset: dict[str, list[dict]] = {}
    for m in markets:
        q = m.get("question", "")
        asset = extract_asset(q)
        level = extract_price_level(q)
        if asset and level is not None:
            price = m.get("external_price_yes") or m.get("price_yes") or 0
            if price > 0:
                entry = {**m, "_asset": asset, "_level": level, "_price": price}
                by_asset.setdefault(asset, []).append(entry)

    violations = []
    for asset, entries in by_asset.items():
        # Sort by price level ascending
        entries.sort(key=lambda e: e["_level"])

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                lower = entries[i]  # lower price level  -> should have HIGHER probability
                higher = entries[j]  # higher price level -> should have LOWER probability

                p_lower = lower["_price"]
                p_higher = higher["_price"]

                # Violation: P(asset > lower_level) < P(asset > higher_level)
                # Also trade when the gap is too small (within violation_threshold)
                if p_lower < p_higher - VIOLATION_THRESHOLD:
                    violation_size = p_higher - p_lower
                    violations.append({
                        "asset": asset,
                        "underpriced": lower,   # should be higher probability
                        "overpriced": higher,    # should be lower probability
                        "violation": violation_size,
                        "lower_level": lower["_level"],
                        "higher_level": higher["_level"],
                        "p_lower": p_lower,
                        "p_higher": p_higher,
                    })

    # Sort by violation size descending (biggest opportunities first)
    violations.sort(key=lambda v: -v["violation"])
    return violations


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
    """Discover crypto price-level markets on Kalshi and auto-import to Simmer."""
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
            # Must be a crypto price-level market
            if not any(kw in question for kw in ("bitcoin", "btc", "ethereum", "eth")):
                continue
            if not any(kw in question for kw in ("above", "over", "exceed", "reach", "price")):
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


def fetch_crypto_markets():
    """Fetch active crypto price-level markets from Simmer API."""
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
                q = (m.get("question") or "").lower()
                if any(kw in q for kw in ("bitcoin", "btc", "ethereum", "eth")):
                    if any(kw in q for kw in ("above", "over", "exceed", "reach", "price")):
                        all_markets.append(m)
        except Exception as e:
            safe_print(f"  Failed to fetch markets for '{term}': {e}")

    # Deduplicate by market ID
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
    """Check open crypto positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    crypto_pos = [p for p in positions
                  if TRADE_SOURCE in p.get("sources", [])
                  or any(kw in (p.get("question") or "").lower()
                         for kw in ("bitcoin", "btc", "ethereum", "eth"))]

    if not crypto_pos:
        return 0, 0

    log(f"\n  Checking {len(crypto_pos)} crypto positions for exit...")
    found, executed = 0, 0

    for pos in crypto_pos:
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
    """Run the crypto monotonicity trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Crypto Monotonicity Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Violation threshold: {VIOLATION_THRESHOLD:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
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
        crypto_pos = [p for p in positions
                      if any(kw in (p.get("question") or "").lower()
                             for kw in ("bitcoin", "btc", "ethereum", "eth"))]
        if not crypto_pos:
            log("  No crypto positions")
        for p in crypto_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering crypto price-level markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_crypto_markets()
    log(f"  Found {len(markets)} active crypto price-level markets")

    if not markets:
        log("  No crypto price-level markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Parse and display market data ---
    log("\nCrypto Price-Level Markets:")
    parsed = []
    for m in markets:
        q = m.get("question", "")
        asset = extract_asset(q)
        level = extract_price_level(q)
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        if asset and level is not None and price > 0:
            parsed.append({**m, "_asset": asset, "_level": level, "_price": price})
            log(f"  {asset} > ${level:,.0f}:  P={price:.1%}  ({q[:50]})")

    if len(parsed) < 2:
        log("  Need at least 2 price-level markets to check monotonicity")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "insufficient_markets"}}))
        return

    # --- Find Violations ---
    violations = find_monotonicity_violations(parsed)
    log(f"\n  Found {len(violations)} monotonicity violations")

    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for v in violations:
        asset = v["asset"]
        underpriced = v["underpriced"]
        overpriced = v["overpriced"]
        violation = v["violation"]

        log(f"\n  VIOLATION ({asset}): P(>{v['lower_level']:,.0f})={v['p_lower']:.1%} "
            f"< P(>{v['higher_level']:,.0f})={v['p_higher']:.1%}  gap={violation:.1%}")

        signals += 1

        # Conviction-based sizing: violation size relative to threshold
        raw_conv = min(violation / VIOLATION_THRESHOLD, 3.0) / 3.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        # Trade 1: Buy YES on the underpriced (lower price level) market
        log(f"    -> BUY YES on {asset}>${v['lower_level']:,.0f} (underpriced at {v['p_lower']:.1%})"
            f"  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards for underpriced market
        under_id = underpriced.get("id")
        ctx = get_market_context(under_id, my_probability=v["p_higher"])
        ok, reasons = check_safeguards(ctx)
        if not ok:
            log(f"    Skipped underpriced: {'; '.join(reasons)}")
            skip_reasons.extend(reasons)
            continue
        if reasons:
            log(f"    Warnings: {'; '.join(reasons)}")

        if not dry_run:
            result = execute_trade(
                under_id, "yes", size,
                reasoning=(f"Monotonicity: {asset}>${v['lower_level']:,.0f} at {v['p_lower']:.1%} "
                           f"< {asset}>${v['higher_level']:,.0f} at {v['p_higher']:.1%} "
                           f"(violation={violation:.1%})"),
                signal_data={"asset": asset, "lower_level": v["lower_level"],
                             "higher_level": v["higher_level"], "violation": round(violation, 4),
                             "p_lower": round(v["p_lower"], 4), "p_higher": round(v["p_higher"], 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought YES ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis=f"Monotonicity violation {asset}", action="buy")
            else:
                log(f"    Trade failed: {result.get('error')}", force=True)
        else:
            log(f"    [DRY RUN] Would buy YES ${size:.2f}")
            trades_executed += 1
            total_usd += size

        # Trade 2: Buy NO on the overpriced (higher price level) market
        if trades_executed < MAX_TRADES_PER_RUN:
            over_id = overpriced.get("id")
            log(f"    -> BUY NO on {asset}>${v['higher_level']:,.0f} (overpriced at {v['p_higher']:.1%})"
                f"  size=${size:.2f}")

            ctx2 = get_market_context(over_id, my_probability=1 - v["p_higher"])
            ok2, reasons2 = check_safeguards(ctx2)
            if not ok2:
                log(f"    Skipped overpriced: {'; '.join(reasons2)}")
                skip_reasons.extend(reasons2)
                continue
            if reasons2:
                log(f"    Warnings: {'; '.join(reasons2)}")

            if not dry_run:
                result2 = execute_trade(
                    over_id, "no", size,
                    reasoning=(f"Monotonicity: {asset}>${v['higher_level']:,.0f} overpriced at "
                               f"{v['p_higher']:.1%} vs {asset}>${v['lower_level']:,.0f} at "
                               f"{v['p_lower']:.1%}"),
                    signal_data={"asset": asset, "lower_level": v["lower_level"],
                                 "higher_level": v["higher_level"], "violation": round(violation, 4),
                                 "side": "no_overpriced"},
                )
                if result2.get("success"):
                    trades_executed += 1
                    total_usd += size
                    tag = "[PAPER] " if result2.get("simulated") else ""
                    log(f"    {tag}Bought NO ${size:.2f}", force=True)
                    if result2.get("trade_id") and JOURNAL_AVAILABLE and not result2.get("simulated"):
                        log_trade(trade_id=result2["trade_id"], source=TRADE_SOURCE,
                                  skill_slug=SKILL_SLUG, thesis=f"Monotonicity NO {asset}", action="buy")
                else:
                    log(f"    Trade failed: {result2.get('error')}", force=True)
            else:
                log(f"    [DRY RUN] Would buy NO ${size:.2f}")
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
    parser = argparse.ArgumentParser(description="Kalshi Crypto Monotonicity Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set violation_threshold=0.05)")
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

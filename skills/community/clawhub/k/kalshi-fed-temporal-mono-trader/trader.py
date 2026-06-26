#!/usr/bin/env python3
"""
Kalshi Fed Temporal Monotonicity Trader

Exploits temporal monotonicity violations in Fed rate markets on Kalshi.
P(rate cut by June) >= P(rate cut by April) ALWAYS — if April cut is priced
higher than June cut, that's a violation we can trade.

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
    "violation_threshold": {"env": "SIMMER_FED_TEMP_VIOLATION_THRESHOLD", "default": 0.03,  "type": float},
    "exit_threshold":      {"env": "SIMMER_FED_TEMP_EXIT_THRESHOLD",      "default": 0.45,  "type": float},
    "max_position_usd":    {"env": "SIMMER_FED_TEMP_MAX_POSITION_USD",    "default": 5.00,  "type": float},
    "max_trades_per_run":  {"env": "SIMMER_FED_TEMP_MAX_TRADES_PER_RUN",  "default": 3,     "type": int},
    "slippage_max":        {"env": "SIMMER_FED_TEMP_SLIPPAGE_MAX",        "default": 0.15,  "type": float},
    "min_liquidity":       {"env": "SIMMER_FED_TEMP_MIN_LIQUIDITY",       "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-fed-temporal-mono-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-fed-temporal"
SKILL_SLUG = "kalshi-fed-temporal-mono-trader"
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
# Temporal ordering of FOMC meeting dates for 2025-2026
# =============================================================================

# These represent the chronological ordering of FOMC meetings.
# P(rate cut by later_date) >= P(rate cut by earlier_date) ALWAYS.
FOMC_MEETING_ORDER = [
    "january",
    "march",
    "april",      # sometimes labeled "may" in markets
    "june",
    "july",
    "september",
    "october",    # sometimes labeled "november" in markets
    "december",
]

# Month aliases found in market questions
MONTH_ALIASES = {
    "jan": "january", "feb": "march", "mar": "march",
    "apr": "april", "may": "april",
    "jun": "june", "jul": "july",
    "aug": "september", "sep": "september",
    "oct": "october", "nov": "october",
    "dec": "december",
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


def extract_meeting_date(question: str) -> str | None:
    """Extract the FOMC meeting month from a market question string.

    Looks for patterns like "by June", "June meeting", "June 2025", etc.
    Returns canonical month name or None.
    """
    q = question.lower()
    # Try full month names first
    for month in FOMC_MEETING_ORDER:
        if month in q:
            return month
    # Try abbreviations
    for abbr, canonical in MONTH_ALIASES.items():
        pattern = r'\b' + abbr + r'\b'
        if re.search(pattern, q):
            return canonical
    return None


def extract_year(question: str) -> int | None:
    """Extract year from market question (e.g., 2025, 2026)."""
    m = re.search(r'20(2[4-9])', question)
    if m:
        return int("20" + m.group(1))
    return None


def meeting_index(month: str) -> int:
    """Return the chronological index of a meeting month."""
    try:
        return FOMC_MEETING_ORDER.index(month)
    except ValueError:
        return -1


def is_rate_cut_market(question: str) -> bool:
    """Check if this market is about a Fed rate cut."""
    q = question.lower()
    return ("rate" in q and ("cut" in q or "lower" in q or "reduce" in q)) or \
           ("federal" in q and "reserve" in q and "cut" in q)


def is_rate_hike_market(question: str) -> bool:
    """Check if this market is about a Fed rate hike."""
    q = question.lower()
    return ("rate" in q and ("hike" in q or "raise" in q or "increase" in q)) or \
           ("federal" in q and "reserve" in q and ("hike" in q or "raise" in q))


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
    """Discover Fed rate markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["fed", "federal reserve", "rate cut", "rate hike"]:
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
            if not (is_rate_cut_market(question) or is_rate_hike_market(question)):
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


def fetch_fed_markets():
    """Fetch active Fed rate markets from Simmer API."""
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "rate", "limit": 50}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if is_rate_cut_market(m.get("question", ""))
                or is_rate_hike_market(m.get("question", ""))]
    except Exception as e:
        safe_print(f"  Failed to fetch markets: {e}")
        return []


# =============================================================================
# Temporal Monotonicity Analysis
# =============================================================================

def group_by_year_and_type(markets: list) -> dict:
    """Group markets by (year, type) where type is 'cut' or 'hike'.

    Returns dict of {(year, type): [(month, market_dict, price), ...]} sorted
    chronologically.
    """
    groups = {}
    for m in markets:
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        month = extract_meeting_date(question)
        year = extract_year(question) or datetime.now().year

        if month is None:
            continue

        mtype = None
        if is_rate_cut_market(question):
            mtype = "cut"
        elif is_rate_hike_market(question):
            mtype = "hike"
        if mtype is None:
            continue

        key = (year, mtype)
        if key not in groups:
            groups[key] = []
        groups[key].append((month, m, price))

    # Sort each group chronologically
    for key in groups:
        groups[key].sort(key=lambda x: meeting_index(x[0]))

    return groups


def find_violations(groups: dict, threshold: float) -> list:
    """Find temporal monotonicity violations.

    For rate cuts: P(cut by June) >= P(cut by April) always.
    A violation occurs when an earlier meeting has HIGHER cut probability
    than a later meeting by more than threshold.

    For rate hikes: Same logic — P(hike by June) >= P(hike by April).

    Returns list of violation dicts with trade recommendations.
    """
    violations = []

    for (year, mtype), entries in groups.items():
        # Compare all pairs (i < j means i is earlier)
        for i in range(len(entries)):
            month_early, market_early, price_early = entries[i]
            for j in range(i + 1, len(entries)):
                month_late, market_late, price_late = entries[j]

                # Violation: earlier meeting priced HIGHER than later meeting
                diff = price_early - price_late
                if diff > threshold:
                    violations.append({
                        "year": year,
                        "type": mtype,
                        "early_month": month_early,
                        "late_month": month_late,
                        "early_price": price_early,
                        "late_price": price_late,
                        "violation_size": diff,
                        "early_market": market_early,
                        "late_market": market_late,
                        # Trade: sell the overpriced early, buy the underpriced late
                        "sell_market": market_early,
                        "sell_side": "no",  # sell YES = buy NO on early
                        "buy_market": market_late,
                        "buy_side": "yes",  # buy YES on later
                    })

    # Sort by violation size descending
    violations.sort(key=lambda v: -v["violation_size"])
    return violations


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
    """Check open Fed temporal positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    fed_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or ("rate" in (p.get("question") or "").lower()
                   and ("cut" in (p.get("question") or "").lower()
                        or "hike" in (p.get("question") or "").lower()))]

    if not fed_pos:
        return 0, 0

    log(f"\n  Checking {len(fed_pos)} Fed temporal positions for exit...")
    found, executed = 0, 0

    for pos in fed_pos:
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
    """Run the Fed Temporal Monotonicity trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Fed Temporal Monotonicity Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Violation threshold: {VIOLATION_THRESHOLD:.0%}  Exit: {EXIT_THRESHOLD:.0%}")
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
        fed_pos = [p for p in positions
                   if "rate" in (p.get("question") or "").lower()]
        if not fed_pos:
            log("  No Fed rate positions")
        for p in fed_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering Fed rate markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_fed_markets()
    log(f"  Found {len(markets)} active Fed rate markets")

    if not markets:
        log("  No Fed rate markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Group by year/type and find violations ---
    groups = group_by_year_and_type(markets)
    log(f"\n  Grouped into {len(groups)} year/type buckets:")
    for (year, mtype), entries in groups.items():
        months = [e[0] for e in entries]
        log(f"    {year} {mtype}: {', '.join(months)}")

    violations = find_violations(groups, VIOLATION_THRESHOLD)
    log(f"\n  Found {len(violations)} temporal monotonicity violations")

    # --- Trade violations ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for v in violations:
        signals += 1
        violation_size = v["violation_size"]
        early_q = v["early_market"].get("question", "")[:50]
        late_q = v["late_market"].get("question", "")[:50]

        log(f"\n  VIOLATION: {v['early_month']} ({v['early_price']:.1%}) > "
            f"{v['late_month']} ({v['late_price']:.1%})  "
            f"diff={violation_size:.1%}")
        log(f"    Early: {early_q}")
        log(f"    Late:  {late_q}")

        # Conviction-based sizing: violation_size / violation_threshold normalized
        raw_conv = min(violation_size / VIOLATION_THRESHOLD, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> Trade size: ${size:.2f} (conviction={raw_conv:.1%})")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Trade the later (underpriced) market — buy YES
        buy_market = v["buy_market"]
        buy_id = buy_market.get("id")

        ctx = get_market_context(buy_id, my_probability=v["late_price"] + violation_size / 2)
        ok, reasons = check_safeguards(ctx)
        if not ok:
            log(f"    Skipped buy: {'; '.join(reasons)}")
            skip_reasons.extend(reasons)
            continue
        if reasons:
            log(f"    Warnings: {'; '.join(reasons)}")

        if not dry_run:
            result = execute_trade(
                buy_id, "yes", size,
                reasoning=(f"Temporal violation: {v['early_month']}={v['early_price']:.1%} > "
                           f"{v['late_month']}={v['late_price']:.1%} diff={violation_size:.1%}"),
                signal_data={
                    "violation_size": round(violation_size, 4),
                    "early_month": v["early_month"],
                    "late_month": v["late_month"],
                    "early_price": round(v["early_price"], 4),
                    "late_price": round(v["late_price"], 4),
                },
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought YES on {v['late_month']} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"Temporal violation {v['early_month']}>{v['late_month']}",
                              action="buy")
            else:
                log(f"    Trade failed: {result.get('error')}", force=True)
        else:
            log(f"    [DRY RUN] Would buy YES on {v['late_month']} ${size:.2f}")
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
    parser = argparse.ArgumentParser(description="Kalshi Fed Temporal Monotonicity Trader")
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

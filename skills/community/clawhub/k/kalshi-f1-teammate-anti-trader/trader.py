#!/usr/bin/env python3
"""
Kalshi F1 Teammate Anti-Correlation Trader

Trades F1 Drivers Championship markets on Kalshi using teammate
anti-correlation. Teammates share the same car, so their championship
probabilities are structurally anti-correlated: if one rises, the other
should fall. Markets are slow to adjust teammate prices symmetrically,
creating exploitable mispricings.

The skill monitors teammate pairs and trades when one driver's probability
rises without a corresponding drop in their teammate's price.

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
    "entry_edge":        {"env": "SIMMER_F1_TEAM_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_F1_TEAM_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_F1_TEAM_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_F1_TEAM_MAX_TRADES_PER_RUN","default": 4,     "type": int},
    "slippage_max":      {"env": "SIMMER_F1_TEAM_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_F1_TEAM_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-f1-teammate-anti-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-f1-teammate"
SKILL_SLUG = "kalshi-f1-teammate-anti-trader"
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
# Teammate Anti-Correlation Model
# =============================================================================

# Teammate pairs: (driver_a, driver_b) — share the same constructor car
TEAMMATE_PAIRS = [
    ("verstappen", "lawson"),      # Red Bull
    ("leclerc",    "hamilton"),     # Ferrari
    ("russell",    "antonelli"),   # Mercedes
    ("piastri",    "norris"),      # McLaren
]

# Historical teammate dominance ratios
# When one teammate is stronger, the team's total probability
# should split roughly according to this ratio.
# 0.7 means driver_a typically captures ~70% of the team's total.
TEAMMATE_DOMINANCE = {
    ("verstappen", "lawson"):    0.85,  # VER clearly dominant
    ("leclerc",    "hamilton"):  0.50,  # Evenly matched
    ("russell",    "antonelli"): 0.70,  # RUS has experience edge
    ("piastri",    "norris"):   0.40,  # NOR slightly stronger
}

# Expected team probability share (sum of both drivers)
# This represents the constructor's fair share of the championship
TEAM_TOTAL_SHARE = {
    ("verstappen", "lawson"):    0.36,  # Red Bull ~36% total
    ("leclerc",    "hamilton"):  0.20,  # Ferrari ~20% total
    ("russell",    "antonelli"): 0.08,  # Mercedes ~8% total
    ("piastri",    "norris"):   0.36,  # McLaren ~36% total
}

# All known drivers for market matching
ALL_DRIVERS = set()
for a, b in TEAMMATE_PAIRS:
    ALL_DRIVERS.add(a)
    ALL_DRIVERS.add(b)

# Driver name aliases for market question parsing
DRIVER_ALIASES = {
    "max verstappen": "verstappen",
    "lando norris": "norris",
    "charles leclerc": "leclerc",
    "lewis hamilton": "hamilton",
    "george russell": "russell",
    "oscar piastri": "piastri",
    "liam lawson": "lawson",
    "kimi antonelli": "antonelli",
    "andrea kimi antonelli": "antonelli",
}


def get_teammate(driver: str) -> str | None:
    """Get the teammate of a given driver."""
    for a, b in TEAMMATE_PAIRS:
        if driver == a:
            return b
        if driver == b:
            return a
    return None


def get_pair_key(driver: str) -> tuple | None:
    """Get the canonical pair tuple for a driver."""
    for pair in TEAMMATE_PAIRS:
        if driver in pair:
            return pair
    return None


def compute_fair_split(driver: str, team_market_total: float) -> float:
    """Compute a driver's fair share of the team total.

    Based on the dominance ratio for their teammate pair.
    """
    pair = get_pair_key(driver)
    if not pair:
        return team_market_total * 0.5

    dominance = TEAMMATE_DOMINANCE.get(pair, 0.5)
    if driver == pair[0]:
        return team_market_total * dominance
    else:
        return team_market_total * (1 - dominance)


def analyze_pair_mispricing(driver_a: str, price_a: float,
                             driver_b: str, price_b: float) -> list[dict]:
    """Analyze a teammate pair for anti-correlation mispricings.

    Returns a list of trade signals when the pair prices don't
    reflect the expected dominance ratio.
    """
    pair = get_pair_key(driver_a)
    if not pair:
        return []

    team_total = price_a + price_b
    expected_total = TEAM_TOTAL_SHARE.get(pair, 0.20)

    # Compute fair prices based on dominance ratio
    fair_a = compute_fair_split(driver_a, team_total)
    fair_b = compute_fair_split(driver_b, team_total)

    signals = []

    # Check driver A mispricing
    edge_a = fair_a - price_a
    if abs(edge_a) >= ENTRY_EDGE:
        signals.append({
            "driver": driver_a,
            "teammate": driver_b,
            "market_price": price_a,
            "fair_price": fair_a,
            "edge": edge_a,
            "side": "yes" if edge_a > 0 else "no",
            "reason": (f"Team total={team_total:.1%}, "
                       f"fair split for {driver_a}={fair_a:.1%} vs market={price_a:.1%}"),
        })

    # Check driver B mispricing
    edge_b = fair_b - price_b
    if abs(edge_b) >= ENTRY_EDGE:
        signals.append({
            "driver": driver_b,
            "teammate": driver_a,
            "market_price": price_b,
            "fair_price": fair_b,
            "edge": edge_b,
            "side": "yes" if edge_b > 0 else "no",
            "reason": (f"Team total={team_total:.1%}, "
                       f"fair split for {driver_b}={fair_b:.1%} vs market={price_b:.1%}"),
        })

    return signals


# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def extract_driver(question: str) -> str | None:
    """Extract driver name from a market question string."""
    q = question.lower()
    for alias, driver in sorted(DRIVER_ALIASES.items(), key=lambda x: -len(x[0])):
        if alias in q:
            return driver
    for driver in ALL_DRIVERS:
        if driver in q:
            return driver
    return None


def is_f1_championship_market(question: str) -> bool:
    """Check if a market question is about F1 drivers championship."""
    q = question.lower()
    f1_terms = ["f1", "formula 1", "formula one", "drivers championship",
                "driver championship", "world drivers"]
    return any(term in q for term in f1_terms)


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
    """Discover F1 championship markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["F1", "drivers championship", "Formula 1 champion"]:
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
            if not is_f1_championship_market(question):
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


def fetch_f1_markets():
    """Fetch active F1 championship markets from Simmer API."""
    try:
        all_markets = []
        for query in ["F1", "drivers championship"]:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": query, "limit": 50}
            )
            markets = result.get("markets", [])
            all_markets.extend(markets)

        seen_ids = set()
        unique = []
        for m in all_markets:
            mid = m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                if is_f1_championship_market(m.get("question", "")):
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
    """Check open F1 teammate positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    f1_positions = [p for p in positions
                    if TRADE_SOURCE in p.get("sources", [])
                    or is_f1_championship_market(p.get("question", ""))]

    if not f1_positions:
        return 0, 0

    log(f"\n  Checking {len(f1_positions)} F1 teammate positions for exit...")
    found, executed = 0, 0

    for pos in f1_positions:
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
    """Run the F1 teammate anti-correlation trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("F1 Teammate Anti-Correlation Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("")
        log("Teammate pairs and dominance ratios:")
        for pair in TEAMMATE_PAIRS:
            dom = TEAMMATE_DOMINANCE.get(pair, 0.5)
            total = TEAM_TOTAL_SHARE.get(pair, 0.20)
            log(f"  {pair[0]:>15} vs {pair[1]:<15}  "
                f"dominance={dom:.0%}/{1-dom:.0%}  team_total={total:.0%}")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        f1 = [p for p in positions if is_f1_championship_market(p.get("question", ""))]
        if not f1:
            log("  No F1 championship positions")
        for p in f1:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering F1 championship markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_f1_markets()
    log(f"  Found {len(markets)} active F1 championship markets")

    if not markets:
        log("  No F1 championship markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Build driver price map ---
    driver_prices = {}  # driver -> (market_id, price)
    for m in markets:
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        driver = extract_driver(question)
        if driver and driver in ALL_DRIVERS:
            driver_prices[driver] = {
                "market_id": m.get("id"),
                "price": price,
                "question": question,
            }

    log(f"\n  Matched {len(driver_prices)} drivers to markets:")
    for d, info in sorted(driver_prices.items()):
        teammate = get_teammate(d)
        log(f"    {d:>15}: {info['price']:.1%}  (teammate: {teammate})")
    log("")

    # --- Analyze Teammate Pairs ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []
    trade_signals = []

    for driver_a, driver_b in TEAMMATE_PAIRS:
        info_a = driver_prices.get(driver_a)
        info_b = driver_prices.get(driver_b)

        if not info_a or not info_b:
            missing = driver_a if not info_a else driver_b
            log(f"  Pair {driver_a}/{driver_b}: missing market for {missing}")
            continue

        price_a = info_a["price"]
        price_b = info_b["price"]
        team_total = price_a + price_b
        pair_key = get_pair_key(driver_a)
        expected_total = TEAM_TOTAL_SHARE.get(pair_key, 0.20)
        dominance = TEAMMATE_DOMINANCE.get(pair_key, 0.5)

        log(f"  Pair: {driver_a}={price_a:.1%} + {driver_b}={price_b:.1%} "
            f"= {team_total:.1%}  (expected={expected_total:.1%}, "
            f"dominance={dominance:.0%}/{1-dominance:.0%})")

        pair_signals = analyze_pair_mispricing(driver_a, price_a, driver_b, price_b)
        for sig in pair_signals:
            driver = sig["driver"]
            info = driver_prices[driver]
            log(f"    -> {sig['side'].upper()} {driver}: "
                f"market={sig['market_price']:.1%} fair={sig['fair_price']:.1%} "
                f"edge={sig['edge']:+.1%}")
            trade_signals.append({**sig, "market_id": info["market_id"]})

    # --- Execute Trades ---
    for sig in trade_signals:
        signals += 1
        edge = abs(sig["edge"])

        # Conviction-based sizing
        raw_conv = min(edge / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped {sig['driver']}: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        fair_p = sig["fair_price"]
        ctx = get_market_context(sig["market_id"],
                                 my_probability=fair_p if sig["side"] == "yes" else 1 - fair_p)
        ok, reasons = check_safeguards(ctx)
        if not ok:
            log(f"    Skipped {sig['driver']}: {'; '.join(reasons)}")
            skip_reasons.extend(reasons)
            continue
        if reasons:
            log(f"    Warnings for {sig['driver']}: {'; '.join(reasons)}")

        if not dry_run:
            result = execute_trade(
                sig["market_id"], sig["side"], size,
                reasoning=(f"Teammate anti-corr: {sig['driver']} vs {sig['teammate']} "
                           f"market={sig['market_price']:.1%} fair={sig['fair_price']:.1%} "
                           f"edge={sig['edge']:+.1%}"),
                signal_data={"driver": sig["driver"], "teammate": sig["teammate"],
                             "market_price": round(sig["market_price"], 4),
                             "fair_price": round(sig["fair_price"], 4),
                             "edge": round(sig["edge"], 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {sig['side'].upper()} {sig['driver']} ${size:.2f}",
                    force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"Teammate edge: {sig['driver']} vs {sig['teammate']}",
                              action="buy")
            else:
                log(f"    Trade failed for {sig['driver']}: {result.get('error')}",
                    force=True)
        else:
            log(f"    [DRY RUN] Would buy {sig['side'].upper()} {sig['driver']} ${size:.2f}")
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
    parser = argparse.ArgumentParser(description="Kalshi F1 Teammate Anti-Correlation Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set entry_edge=0.10)")
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

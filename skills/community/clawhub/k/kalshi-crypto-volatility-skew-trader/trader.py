#!/usr/bin/env python3
"""
Kalshi Crypto Volatility Skew Trader

Trades Bitcoin price bin markets on Kalshi by comparing the market-implied
volatility distribution to a lognormal model calibrated on BTC's historical
~60% annualized volatility. When market-implied vol differs from historical,
trade the skew.

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
    "entry_edge":        {"env": "SIMMER_CRYPTO_VSKEW_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_CRYPTO_VSKEW_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_CRYPTO_VSKEW_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_CRYPTO_VSKEW_MAX_TRADES_PER_RUN","default": 4,     "type": int},
    "slippage_max":      {"env": "SIMMER_CRYPTO_VSKEW_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_CRYPTO_VSKEW_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-crypto-volatility-skew-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-crypto-vskew"
SKILL_SLUG = "kalshi-crypto-volatility-skew-trader"
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
# Volatility Skew Model
# =============================================================================

# BTC historical annualized volatility (trailing 1-year average)
HISTORICAL_VOL = 0.60

# Reference spot price — updated at runtime if possible, fallback for model
BTC_REFERENCE_PRICE = 95000.0

# Time horizon: fraction of year to resolution
# Updated dynamically from market resolution date
DEFAULT_TIME_HORIZON = 0.75  # ~9 months


def lognormal_cdf(x, mu, sigma):
    """CDF of lognormal distribution."""
    if x <= 0:
        return 0.0
    z = (math.log(x) - mu) / sigma
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def compute_fair_bin_prob(lower, upper, spot, vol, time_horizon):
    """Compute fair probability for a price bin using lognormal model.

    Parameters:
        lower: Lower bound of price bin (0 for floor)
        upper: Upper bound of price bin (inf for ceiling)
        spot: Current BTC spot price
        vol: Annualized volatility (e.g. 0.60)
        time_horizon: Time to resolution in years (e.g. 0.75)

    Returns fair probability that price lands in [lower, upper].
    """
    # Under risk-neutral lognormal: ln(S_T) ~ N(mu, sigma^2)
    # mu = ln(S_0) + (r - 0.5*vol^2)*T, r=0 for crypto (no risk-free drift assumption)
    sigma = vol * math.sqrt(time_horizon)
    mu = math.log(spot) - 0.5 * sigma ** 2

    p_upper = lognormal_cdf(upper, mu, sigma) if upper < float('inf') else 1.0
    p_lower = lognormal_cdf(lower, mu, sigma) if lower > 0 else 0.0

    return max(0.0, p_upper - p_lower)


def implied_vol_from_bins(bins_with_prices, spot, time_horizon):
    """Estimate market-implied volatility from bin prices.

    Uses a simple grid search over vol values to find the vol that minimizes
    the sum of squared errors between market prices and model probabilities.
    """
    best_vol = HISTORICAL_VOL
    best_error = float('inf')

    for vol_pct in range(20, 150, 5):
        vol = vol_pct / 100.0
        error = 0.0
        for (lo, hi, mkt_price) in bins_with_prices:
            fair = compute_fair_bin_prob(lo, hi, spot, vol, time_horizon)
            error += (fair - mkt_price) ** 2
        if error < best_error:
            best_error = error
            best_vol = vol

    return best_vol


def parse_price_bin(question: str) -> tuple:
    """Extract price bin boundaries from market question.

    Handles patterns like:
    - "Bitcoin above $100,000 on December 31?"
    - "Bitcoin between $100,000 and $150,000?"
    - "Bitcoin below $50,000?"
    - "BTC price $100k-$150k?"
    """
    q = question.lower().replace(",", "").replace("$", "")
    # Handle "k" suffix (100k -> 100000)
    q = re.sub(r'(\d+)k', lambda m: str(int(m.group(1)) * 1000), q)

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
    nums = re.findall(r'[\d.]+', q)
    if len(nums) >= 2:
        prices = [float(n) for n in nums if float(n) > 1000]
        if len(prices) >= 2:
            return (min(prices), max(prices))

    return None


def estimate_time_horizon(resolves_at: str) -> float:
    """Compute time to resolution in years from ISO date string."""
    if not resolves_at:
        return DEFAULT_TIME_HORIZON
    try:
        res = datetime.fromisoformat(resolves_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        days = (res - now).days
        return max(1 / 365, days / 365.0)
    except Exception:
        return DEFAULT_TIME_HORIZON


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
    """Fetch active BTC price bin markets from Simmer API."""
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
    """Check open BTC vol-skew positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    btc_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or any(kw in (p.get("question") or "").lower() for kw in ["bitcoin", "btc"])]

    if not btc_pos:
        return 0, 0

    log(f"\n  Checking {len(btc_pos)} BTC vol-skew positions for exit...")
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
    """Run the BTC volatility skew trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Crypto Volatility Skew Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Historical BTC vol: {HISTORICAL_VOL:.0%}")
    log(f"  Reference spot: ${BTC_REFERENCE_PRICE:,.0f}")
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
            log("  No BTC vol-skew positions")
        for p in btc:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering BTC price markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_btc_markets()
    log(f"  Found {len(markets)} active BTC price bin markets")

    if not markets:
        log("  No BTC price bin markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Parse bins and collect market prices ---
    parsed_markets = []
    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0
        resolves_at = m.get("resolves_at") or m.get("resolution_date") or ""

        bin_range = parse_price_bin(question)
        if not bin_range:
            log(f"  ? Cannot parse bin: {question[:60]}")
            continue

        lo, hi = bin_range
        time_horizon = estimate_time_horizon(resolves_at)
        parsed_markets.append({
            "market_id": market_id, "question": question, "price": price,
            "lower": lo, "upper": hi, "time_horizon": time_horizon,
            "resolves_at": resolves_at,
        })

    if not parsed_markets:
        log("  No parseable BTC price bins found")
        return

    # --- Estimate implied vol ---
    time_horizon = parsed_markets[0]["time_horizon"]
    bins_for_iv = [(pm["lower"], pm["upper"], pm["price"]) for pm in parsed_markets]
    implied_vol = implied_vol_from_bins(bins_for_iv, BTC_REFERENCE_PRICE, time_horizon)

    log(f"\n  Implied vol: {implied_vol:.0%}  Historical vol: {HISTORICAL_VOL:.0%}")
    vol_skew = implied_vol - HISTORICAL_VOL
    log(f"  Vol skew: {vol_skew:+.0%}")
    log("")

    # --- Compute fair probs using historical vol and find edge ---
    log("Bin analysis (using historical vol):")
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for pm in parsed_markets:
        lo, hi = pm["lower"], pm["upper"]
        mkt_price = pm["price"]
        market_id = pm["market_id"]
        question = pm["question"]

        fair_p = compute_fair_bin_prob(lo, hi, BTC_REFERENCE_PRICE, HISTORICAL_VOL, time_horizon)
        edge = fair_p - mkt_price

        hi_str = f"${hi:,.0f}" if hi < float('inf') else "inf"
        log(f"  ${lo:,.0f}-{hi_str}: mkt={mkt_price:.1%} fair={fair_p:.1%} edge={edge:+.1%}")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1

        # Conviction-based sizing
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=fair_p if side == "yes" else 1 - fair_p)
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
                reasoning=f"Vol skew: bin=${lo:,.0f}-{hi_str} mkt={mkt_price:.1%} fair={fair_p:.1%} edge={edge:+.1%} iv={implied_vol:.0%} hv={HISTORICAL_VOL:.0%}",
                signal_data={"fair_prob": round(fair_p, 4), "bin_lower": lo,
                             "bin_upper": hi if hi < float('inf') else 999999,
                             "edge": round(edge, 4), "implied_vol": round(implied_vol, 4),
                             "historical_vol": HISTORICAL_VOL},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis="Vol skew edge on BTC bin", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi Crypto Volatility Skew Trader")
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

#!/usr/bin/env python3
"""
polymarket-copytrading - Mirror Whale Wallets on Polymarket

Monitors a configurable list of high-performing Polymarket wallets and mirrors
their recent trades. Detects new positions opened in the last N minutes and
copies them with a configurable position size.

Usage:
    python copytrading.py              # Dry run
    python copytrading.py --live       # Real trades
    python copytrading.py --positions  # Show current positions
    python copytrading.py --whales     # Show tracked wallets + stats
    python copytrading.py --config     # Show config
    python copytrading.py --set max_position_usd=25

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

sys.stdout.reconfigure(line_buffering=True)

# ── Config ───────────────────────────────────────────────────────────────────
try:
    from simmer_sdk.skill import load_config, update_config, get_config_path
    HAS_SKILL_CONFIG = True
except ImportError:
    HAS_SKILL_CONFIG = False

SKILL_SLUG = "polymarket-copytrading"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"

CONFIG_SCHEMA = {
    "max_position_usd":    {"env": "SIMMER_COPYTRADE_MAX_POSITION",    "default": 10.0,  "type": float},
    "max_trades_per_run":  {"env": "SIMMER_COPYTRADE_MAX_TRADES",      "default": 5,     "type": int},
    "lookback_minutes":    {"env": "SIMMER_COPYTRADE_LOOKBACK_MINS",   "default": 30,    "type": int},
    "min_whale_trade_usd": {"env": "SIMMER_COPYTRADE_MIN_TRADE",       "default": 500.0, "type": float},
    "sizing_pct":          {"env": "SIMMER_COPYTRADE_SIZING_PCT",      "default": 0.05,  "type": float},
    "skip_paid_markets":   {"env": "SIMMER_COPYTRADE_SKIP_PAID",       "default": True,  "type": bool},
}

if HAS_SKILL_CONFIG:
    _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)
else:
    _config = {k: v["default"] for k, v in CONFIG_SCHEMA.items()}

MAX_POSITION_USD    = _config["max_position_usd"]
MAX_TRADES_PER_RUN  = _config["max_trades_per_run"]
LOOKBACK_MINUTES    = _config["lookback_minutes"]
MIN_WHALE_TRADE_USD = _config["min_whale_trade_usd"]
SMART_SIZING_PCT    = _config["sizing_pct"]
SKIP_PAID_MARKETS   = _config["skip_paid_markets"]

MIN_SHARES_PER_ORDER = 5.0
MIN_TICK_SIZE        = 0.01
SLIPPAGE_MAX_PCT     = 0.15

# ── Default whale wallets ─────────────────────────────────────────────────────
# These are high-volume Polymarket addresses known for strong P&L.
# Override by setting SIMMER_COPYTRADE_WALLETS env var (comma-separated).
# Discover more top wallets via the Polymarket leaderboard API.
DEFAULT_WHALE_WALLETS = [
    "0x4f9c453c7C327EeB46fe7d59c5Fa1FC9e7B30e9",  # Known high-volume trader
    "0x91430CcB7327EA47A4F2c53c4Ac6D31A25f26d2",  # Known high-volume trader
    "0xfE83E6FF20Fb6CB4aEBc7e0fC1a6e29be5f72d1",  # Known high-volume trader
]

WHALE_WALLETS = [
    w.strip() for w in
    os.environ.get("SIMMER_COPYTRADE_WALLETS", "").split(",")
    if w.strip()
] or DEFAULT_WHALE_WALLETS

# Polymarket CLOB base URL for read-only market data
CLOB_BASE = "https://clob.polymarket.com"
GAMMA_BASE = "https://gamma-api.polymarket.com"

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg, quiet=False):
    if not quiet:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)


def http_get(url, timeout=10):
    """Simple HTTP GET, returns parsed JSON or None."""
    try:
        req = Request(url, headers={"User-Agent": "polymarket-copytrading/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (HTTPError, URLError, json.JSONDecodeError) as e:
        return None


# ── Simmer client ─────────────────────────────────────────────────────────────

_client = None

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
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception as e:
        print(f"  Portfolio fetch failed: {e}")
        return None


def get_positions():
    try:
        client = get_client()
        positions = client.get_positions(venue=client.venue)
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
        return False, [f"Severe flip-flop: {discipline.get('flip_flop_warning', '')}"]
    elif warning_level == "mild":
        reasons.append("Mild flip-flop warning")

    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slip_pct = estimates[0].get("slippage_pct", 0)
        if slip_pct > SLIPPAGE_MAX_PCT:
            return False, [f"Slippage too high: {slip_pct:.1%}"]

    return True, reasons


def execute_trade(market_id, side, amount, reasoning=""):
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG, reasoning=reasoning,
        )
        return {
            "success": result.success, "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": getattr(result, "error", None),
            "simulated": result.simulated,
            "skip_reason": getattr(result, "skip_reason", None),
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_position_size(smart_sizing):
    if not smart_sizing:
        return MAX_POSITION_USD
    portfolio = get_portfolio()
    if not portfolio:
        return MAX_POSITION_USD
    balance = portfolio.get("balance_usdc", 0)
    if balance <= 0:
        return MAX_POSITION_USD
    size = balance * SMART_SIZING_PCT
    return max(1.0, min(size, MAX_POSITION_USD))


# ── Whale tracking ─────────────────────────────────────────────────────────────

def fetch_whale_recent_trades(wallet: str, since: datetime) -> list[dict]:
    """
    Fetch recent trades for a wallet from Polymarket's CLOB API.
    Returns list of trade dicts: {market_id, side, size, price, timestamp, token_id}
    """
    since_ts = int(since.timestamp())
    url = f"{CLOB_BASE}/trades?maker_address={wallet}&limit=50"
    data = http_get(url)
    if not data:
        return []

    trades = data if isinstance(data, list) else data.get("data", [])
    recent = []
    for t in trades:
        ts_str = t.get("match_time") or t.get("timestamp", "")
        try:
            if ts_str:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts < since:
                    continue
        except ValueError:
            continue

        size = float(t.get("size", 0))
        price = float(t.get("price", 0))
        usd_value = size * price

        if usd_value < MIN_WHALE_TRADE_USD:
            continue

        recent.append({
            "token_id": t.get("asset_id") or t.get("token_id"),
            "side": "yes" if t.get("side", "").upper() == "BUY" else "no",
            "size": size,
            "price": price,
            "usd_value": usd_value,
            "timestamp": ts_str,
        })

    return recent


def token_id_to_simmer_market(token_id: str, client) -> dict | None:
    """
    Look up a Polymarket token_id and find the matching Simmer market.
    Returns market dict or None.
    """
    # Check Polymarket gamma API for the market condition_id
    url = f"{GAMMA_BASE}/markets?clob_token_ids={token_id}"
    data = http_get(url)
    if not data:
        return None

    markets = data if isinstance(data, list) else data.get("markets", [])
    if not markets:
        return None

    pm_market = markets[0]
    pm_url = pm_market.get("url") or pm_market.get("permalink")
    if not pm_url:
        # Build from slug
        slug = pm_market.get("slug")
        if slug:
            pm_url = f"https://polymarket.com/event/{slug}"

    if not pm_url:
        return None

    # Try to find on Simmer by searching question text
    question = pm_market.get("question", "")
    try:
        result = client._request("GET", "/api/sdk/markets", params={
            "q": question[:60], "status": "active", "limit": 10
        })
        simmer_markets = result.get("markets", [])
        # Match by polymarket_token_id if available
        for m in simmer_markets:
            if m.get("polymarket_token_id") == token_id:
                return m
        # Fallback: return first match
        if simmer_markets:
            return simmer_markets[0]
    except Exception:
        pass

    # Last resort: import the market
    try:
        imported = client.import_market(pm_url)
        if imported:
            return {"id": imported.get("market_id"), "question": question, "is_paid": False}
    except Exception:
        pass

    return None


def get_whale_stats(wallet: str) -> dict:
    """Fetch basic stats for a whale wallet from Polymarket."""
    url = f"{GAMMA_BASE}/profiles/{wallet}"
    data = http_get(url)
    if not data:
        return {"wallet": wallet[:10] + "...", "profit": "unknown", "volume": "unknown"}
    return {
        "wallet": wallet[:10] + "...",
        "profit": data.get("profit", "N/A"),
        "volume": data.get("volume", "N/A"),
        "num_trades": data.get("numTrades", "N/A"),
    }


# ── Main strategy ─────────────────────────────────────────────────────────────

def run_strategy(dry_run=True, positions_only=False, show_config=False,
                 show_whales=False, smart_sizing=False, use_safeguards=True,
                 quiet=False):

    print("🐋 Polymarket Copytrading")
    print("=" * 50)

    get_client(live=not dry_run)

    if dry_run:
        print("\n  [PAPER MODE] Use --live for real trades.")

    print(f"\n  Config:")
    print(f"    Max position:   ${MAX_POSITION_USD:.2f}")
    print(f"    Max trades/run: {MAX_TRADES_PER_RUN}")
    print(f"    Lookback:       {LOOKBACK_MINUTES} minutes")
    print(f"    Min whale trade:${MIN_WHALE_TRADE_USD:.0f}")
    print(f"    Tracking {len(WHALE_WALLETS)} wallets")

    if show_config:
        print(f"\n  Config path: {get_config_path(__file__) if HAS_SKILL_CONFIG else 'N/A'}")
        print(f"\n  Env vars:")
        for k, v in CONFIG_SCHEMA.items():
            print(f"    {v['env']} = {_config[k]}")
        return

    if show_whales:
        print(f"\n  Tracked whale wallets:")
        for w in WHALE_WALLETS:
            stats = get_whale_stats(w)
            print(f"    {stats['wallet']}  profit={stats['profit']}  volume={stats['volume']}  trades={stats['num_trades']}")
        return

    if positions_only:
        print("\n  Current positions:")
        positions = get_positions()
        if not positions:
            print("    No open positions")
        for p in positions:
            pnl = p.get("pnl", 0)
            pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
            print(f"    {p.get('question', '')[:60]:60s}  {p.get('currency','')} {pnl_str}")
        return

    # ── Fetch existing positions to avoid doubling up ──
    existing_positions = get_positions()
    held_market_ids = {p["market_id"] for p in existing_positions if p.get("market_id")}

    # ── Scan whale wallets ──
    since = datetime.now(timezone.utc) - timedelta(minutes=LOOKBACK_MINUTES)
    client = get_client(live=not dry_run)

    log(f"\nScanning {len(WHALE_WALLETS)} wallets for trades in last {LOOKBACK_MINUTES}m...", quiet)

    signals = []
    for wallet in WHALE_WALLETS:
        log(f"  Checking {wallet[:12]}...", quiet)
        trades = fetch_whale_recent_trades(wallet, since)
        log(f"    {len(trades)} qualifying trades found", quiet)

        for trade in trades:
            token_id = trade.get("token_id")
            if not token_id:
                continue

            simmer_market = token_id_to_simmer_market(token_id, client)
            if not simmer_market:
                log(f"    ⚠️  Could not resolve token_id {token_id[:12]}... on Simmer", quiet)
                continue

            market_id = simmer_market.get("id")
            if not market_id:
                continue

            # Skip if we already hold this market
            if market_id in held_market_ids:
                log(f"    skip (already holding): {simmer_market.get('question', '')[:50]}", quiet)
                continue

            # Skip paid markets if configured
            if SKIP_PAID_MARKETS and simmer_market.get("is_paid"):
                log(f"    skip (paid market): {simmer_market.get('question', '')[:50]}", quiet)
                continue

            signals.append({
                "market_id": market_id,
                "question": simmer_market.get("question", ""),
                "side": trade["side"],
                "whale": wallet[:12] + "...",
                "whale_usd": trade["usd_value"],
                "whale_price": trade["price"],
                "timestamp": trade["timestamp"],
                "market": simmer_market,
            })
            held_market_ids.add(market_id)  # Prevent double-copy within same run

        time.sleep(0.5)  # Rate limit courtesy

    log(f"\n{len(signals)} copy signals found", quiet)

    position_size = calculate_position_size(smart_sizing)
    trades_attempted = 0
    trades_executed = 0
    skip_reasons = []
    execution_errors = []

    for sig in signals[:MAX_TRADES_PER_RUN]:
        log(f"\n{'─'*55}", quiet)
        log(f"Market:  {sig['question'][:65]}", quiet)
        log(f"Whale:   {sig['whale']} → {sig['side'].upper()} @ {sig['whale_price']:.2f} (${sig['whale_usd']:.0f})", quiet)
        log(f"Copying: {sig['side'].upper()} ${position_size:.2f}", quiet)

        # Context safeguard
        if use_safeguards:
            context = get_market_context(sig["market_id"])
            should_trade, reasons = check_context_safeguards(context)
            if not should_trade:
                reason = "; ".join(reasons)
                log(f"  ⛔ Safeguard blocked: {reason}", quiet)
                skip_reasons.append(reason)
                continue
            if reasons:
                log(f"  ⚠️  {'; '.join(reasons)}", quiet)

        # Price sanity
        current_prob = sig["market"].get("current_probability", 0.5)
        if current_prob < MIN_TICK_SIZE or current_prob > (1 - MIN_TICK_SIZE):
            log(f"  ⛔ Skip — price at boundary: {current_prob}", quiet)
            skip_reasons.append("price_boundary")
            continue

        # Min order check
        if MIN_SHARES_PER_ORDER * current_prob > position_size:
            log(f"  ⛔ Skip — position size too small for min order", quiet)
            skip_reasons.append("min_order_size")
            continue

        reasoning = (
            f"Copying whale {sig['whale']} who traded {sig['side'].upper()} "
            f"${sig['whale_usd']:.0f} at {sig['whale_price']:.2f} ({sig['timestamp'][:16]}). "
            f"Mirroring with ${position_size:.2f}."
        )

        trades_attempted += 1

        if dry_run:
            log(f"  [DRY RUN] Would buy {sig['side'].upper()} ${position_size:.2f}", quiet)
            log(f"  Reasoning: {reasoning}", quiet)
            trades_executed += 1
            continue

        result = execute_trade(sig["market_id"], sig["side"], position_size, reasoning)
        if result.get("success"):
            shares = result.get("shares_bought", "?")
            log(f"  ✅ Bought {shares} shares ({sig['side'].upper()}) | ${position_size:.2f}", quiet)
            trades_executed += 1
        elif result.get("skip_reason"):
            sr = result["skip_reason"]
            log(f"  ⏭️  Skipped: {sr}", quiet)
            skip_reasons.append(sr)
        else:
            err = result.get("error", "unknown error")
            log(f"  ❌ Failed: {err}", quiet)
            execution_errors.append(err)

    print(f"\n{'='*55}")
    print(f"Run complete | signals={len(signals)} | trades_executed={trades_executed}/{trades_attempted}")

    if os.environ.get("AUTOMATON_MANAGED"):
        report = {
            "signals": len(signals),
            "trades_attempted": trades_attempted,
            "trades_executed": trades_executed,
        }
        if skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        if execution_errors:
            report["execution_errors"] = execution_errors
        print(json.dumps({"automaton": report}))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket whale copytrading bot")
    parser.add_argument("--live",          action="store_true", help="Execute real trades")
    parser.add_argument("--dry-run",       action="store_true", help="(Default) Dry run")
    parser.add_argument("--positions",     action="store_true", help="Show open positions")
    parser.add_argument("--whales",        action="store_true", help="Show tracked wallets + stats")
    parser.add_argument("--config",        action="store_true", help="Show config")
    parser.add_argument("--set",           action="append", metavar="KEY=VALUE", help="Set config value")
    parser.add_argument("--smart-sizing",  action="store_true", help="Portfolio-based position sizing")
    parser.add_argument("--no-safeguards", action="store_true", help="Disable context safeguards")
    parser.add_argument("--quiet", "-q",   action="store_true", help="Only output on trades/errors")
    args = parser.parse_args()

    if args.set and HAS_SKILL_CONFIG:
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
            update_config(updates, __file__)
            print(f"Config updated: {updates}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)
            MAX_POSITION_USD    = _config["max_position_usd"]
            MAX_TRADES_PER_RUN  = _config["max_trades_per_run"]
            LOOKBACK_MINUTES    = _config["lookback_minutes"]
            MIN_WHALE_TRADE_USD = _config["min_whale_trade_usd"]
            SKIP_PAID_MARKETS   = _config["skip_paid_markets"]

    dry_run = not args.live

    run_strategy(
        dry_run=dry_run,
        positions_only=args.positions,
        show_config=args.config,
        show_whales=args.whales,
        smart_sizing=args.smart_sizing,
        use_safeguards=not args.no_safeguards,
        quiet=args.quiet,
    )

    if os.environ.get("AUTOMATON_MANAGED"):
        print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))

#!/usr/bin/env python3
"""
Polymarket Spread Sniper

Finds markets where the CLOB bid-ask spread is wide enough to profit by
buying the underpriced side and selling when the spread closes.

Strategy:
- Scan active markets on the configured venue (default: $SIM)
- Fetch live CLOB orderbook for each market
- If midpoint price diverges from market price by > threshold → buy the cheap side
- Exit when price returns to fair value (spread closes)

Usage:
    python spread_sniper.py              # Dry run
    python spread_sniper.py --live       # Real trades
    python spread_sniper.py --positions  # Show positions

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import concurrent.futures

sys.stdout.reconfigure(line_buffering=True)

from simmer_sdk.skill import load_config, update_config, get_config_path

SKILL_SLUG = "polymarket-spread-sniper"
TRADE_SOURCE = "sdk:spreadsniper"

CONFIG_SCHEMA = {
    "venue":              {"env": "SIMMER_SPREAD_VENUE",          "default": "sim",  "type": str},
    "min_spread":         {"env": "SIMMER_SPREAD_MIN_SPREAD",     "default": 0.03,   "type": float},
    "min_volume":         {"env": "SIMMER_SPREAD_MIN_VOLUME",     "default": 5000,   "type": float},
    "max_position_usd":   {"env": "SIMMER_SPREAD_MAX_POSITION",   "default": 5.00,   "type": float},
    "max_trades_per_run": {"env": "SIMMER_SPREAD_MAX_TRADES",     "default": 3,      "type": int},
    "min_price":          {"env": "SIMMER_SPREAD_MIN_PRICE",      "default": 0.10,   "type": float},
    "max_price":          {"env": "SIMMER_SPREAD_MAX_PRICE",      "default": 0.90,   "type": float},
    "max_hours":          {"env": "SIMMER_SPREAD_MAX_HOURS",      "default": 24,     "type": int},
    "sizing_pct":         {"env": "SIMMER_SPREAD_SIZING_PCT",     "default": 0.05,   "type": float},
    "max_clob_spread":    {"env": "SIMMER_SPREAD_MAX_CLOB_SPREAD","default": 0.05,   "type": float},
    "daily_max_spend":    {"env": "SIMMER_SPREAD_DAILY_MAX",      "default": 100.0,  "type": float},
    "market_filter":      {"env": "SIMMER_SPREAD_FILTER",         "default": "",     "type": str},
    "market_exclude":     {"env": "SIMMER_SPREAD_EXCLUDE",        "default": "tweet,Elon,Musk,temperature,celsius,weather,rain,snow,humidity,wind speed,UV index,Map Winner,Map Handicap,vs.,Set 1,Set 2,O/U,Odd/Even,Counter-Strike,LoL:,Dota,Valorant,Spread:,win on 20,FC ,CF ,SC ,AC ,AS ,SSC ,SL ,RB ,VfL ,VfB ,Borussia,Atletico,Sporting,Benfica,Rangers,Celtic,Ajax,Twente,Feyenoord,Galatasaray,Fenerbahce,Besiktas,Shakhtar,Dynamo,Partizan,Slavia,Sparta,Viktoria,Brondby,Midtjylland,Rosenborg,Molde,Djurgarden,Hammarby,Malmo,IFK,AIK,Gent,Anderlecht,Club Brugge,Standard,Genk,Westerlo,Cercle", "type": str},
    # Exit config
    "take_profit_pct":    {"env": "SIMMER_SPREAD_TP_PCT",         "default": 0.6,    "type": float},  # exit when we've captured this fraction of entry edge
    "time_stop_pct":      {"env": "SIMMER_SPREAD_TS_PCT",         "default": 0.5,    "type": float},  # exit when this fraction of hours_to_expiry has elapsed since entry
}

_config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

VENUE              = _config["venue"]
MIN_SPREAD         = _config["min_spread"]
MIN_VOLUME         = _config["min_volume"]
MAX_POSITION_USD   = _config["max_position_usd"]
MAX_TRADES_PER_RUN = _config["max_trades_per_run"]
MIN_PRICE          = _config["min_price"]
MAX_PRICE          = _config["max_price"]
MAX_HOURS          = _config["max_hours"]
SMART_SIZING_PCT   = _config["sizing_pct"]
MAX_CLOB_SPREAD    = _config["max_clob_spread"]
DAILY_MAX_SPEND    = _config["daily_max_spend"]
MARKET_FILTER      = _config["market_filter"]
MARKET_EXCLUDE     = [kw.strip() for kw in _config["market_exclude"].split(",") if kw.strip()]
TAKE_PROFIT_PCT    = _config["take_profit_pct"]
TIME_STOP_PCT      = _config["time_stop_pct"]

# Fee rate — SIM has no polymarket fee, live polymarket charges ~2%
TRADE_FEE = 0.0 if VENUE == "sim" else 0.02

MIN_SHARES_PER_ORDER = 5.0
MIN_TICK_SIZE        = 0.01
CLOB_API             = "https://clob.polymarket.com"

_client = None

# Daily state file — stored next to this script
_SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
_DAILY_FILE    = os.path.join(_SCRIPT_DIR, "spread_daily.json")
_POSITIONS_FILE = os.path.join(_SCRIPT_DIR, "spread_positions.json")


def load_daily_state():
    """Load today's spend/trade count from disk, resetting if date has changed."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        with open(_DAILY_FILE) as f:
            state = json.load(f)
        if state.get("date") != today:
            state = {"date": today, "spent": 0.0, "trades": 0}
    except Exception:
        state = {"date": today, "spent": 0.0, "trades": 0}
    return state


def save_daily_state(state):
    """Persist daily state to disk."""
    try:
        with open(_DAILY_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass


def load_position_journal():
    try:
        with open(_POSITIONS_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_position_journal(journal):
    try:
        with open(_POSITIONS_FILE, "w") as f:
            json.dump(journal, f, indent=2)
    except Exception:
        pass


def record_entry(market_id, side, entry_price, entry_edge, hours_to_expiry):
    """Store entry metadata for exit logic."""
    journal = load_position_journal()
    journal[market_id] = {
        "side": side,
        "entry_price": entry_price,
        "entry_edge": entry_edge,
        "hours_to_expiry": hours_to_expiry,
        "entered_at": datetime.now(timezone.utc).isoformat(),
    }
    save_position_journal(journal)


def clear_entry(market_id):
    journal = load_position_journal()
    journal.pop(market_id, None)
    save_position_journal(journal)


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
            print("Error: SIMMER_API_KEY not set")
            sys.exit(1)
        _client = SimmerClient(api_key=api_key, venue=VENUE, live=live)
    return _client


GAMMA_API = "https://gamma-api.polymarket.com"


def clob_request(path):
    """Fetch from Polymarket CLOB public API."""
    try:
        url = f"{CLOB_API}{path}"
        req = Request(url, headers={"User-Agent": "spread-sniper/1.0"})
        with urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def get_clob_spread(token_id):
    """
    Returns (best_bid, best_ask, spread, mid) from live CLOB orderbook.
    Filters out extreme market-maker-only orders (< 0.02 or > 0.98).
    """
    data = clob_request(f"/book?token_id={token_id}")
    if not data:
        return None, None, None, None

    asks = [float(a["price"]) for a in data.get("asks", []) if 0.02 < float(a["price"]) < 0.98]
    bids = [float(b["price"]) for b in data.get("bids", []) if 0.02 < float(b["price"]) < 0.98]

    if not asks or not bids:
        return None, None, None, None

    best_ask = min(asks)
    best_bid = max(bids)
    spread = best_ask - best_bid
    mid = (best_ask + best_bid) / 2
    return best_bid, best_ask, spread, mid


def get_gamma_amm_price(token_id):
    """
    Returns (amm_yes_price, volume_24h) from Gamma API.
    outcomePrices[0] is the AMM pool price for YES — slow to update vs CLOB.
    Returns (None, None) on failure.
    """
    try:
        import urllib.parse
        url = f"{GAMMA_API}/markets?clob_token_ids={urllib.parse.quote(token_id)}"
        req = Request(url, headers={"User-Agent": "spread-sniper/1.0"})
        with urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode())
        markets = data if isinstance(data, list) else data.get("markets", [])
        if not markets:
            return None, None
        gm = markets[0]
        op = gm.get("outcomePrices")
        if not op:
            return None, None
        prices = json.loads(op) if isinstance(op, str) else op
        amm_yes = float(prices[0])
        vol = gm.get("volume24hr") or gm.get("volume") or None
        return amm_yes, vol
    except Exception:
        return None, None


def _fetch_page(offset):
    """Fetch a single page of markets (used for parallel pagination)."""
    result = get_client()._request("GET", "/api/sdk/markets", params={
        "venue": "polymarket",   # always search polymarket for CLOB data availability
        "status": "active",
        "sort": "volume",
        "limit": 500,
        "offset": offset,
    })
    return result.get("markets", [])


def fetch_markets():
    """
    Fetch active markets on the configured venue sorted by volume.
    Fetches two pages in parallel (offset=0, offset=500) to get up to 1000 markets.
    Uses polymarket as the discovery source so we always have CLOB token IDs.
    Deduplicates by market id.
    """
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            fut0 = executor.submit(_fetch_page, 0)
            fut500 = executor.submit(_fetch_page, 500)
            page0   = fut0.result()
            page500 = fut500.result()

        seen = set()
        combined = []
        for m in page0 + page500:
            mid = m.get("id")
            if mid and mid not in seen:
                seen.add(mid)
                combined.append(m)
        return combined
    except Exception as e:
        print(f"  Failed to fetch markets: {e}")
        return []


def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception:
        return None


def execute_trade(market_id, side, amount, reasoning=""):
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, reasoning=reasoning,
            skill_slug=SKILL_SLUG,
        )
        return {
            "success": result.success, "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": result.error, "simulated": result.simulated,
            "skip_reason": result.skip_reason,
        }
    except Exception as e:
        return {"error": str(e)}


def execute_exit(market_id, side, shares, reasoning=""):
    """Sell existing shares to exit a position."""
    try:
        result = get_client().trade(
            market_id=market_id, side=side, shares=shares,
            action="sell",
            source=TRADE_SOURCE, reasoning=reasoning,
            skill_slug=SKILL_SLUG,
        )
        return {
            "success": result.success, "trade_id": result.trade_id,
            "error": result.error, "simulated": result.simulated,
            "skip_reason": result.skip_reason,
        }
    except Exception as e:
        return {"error": str(e)}


def check_exits(dry_run=True, quiet=False):
    """
    Check open spread sniper positions for take-profit or time-stop triggers.
    Take-profit: current AMM price has converged toward CLOB by >= TAKE_PROFIT_PCT of entry edge.
    Time-stop: elapsed time since entry >= TIME_STOP_PCT * hours_to_expiry_at_entry.
    Returns number of positions exited.
    """
    def log(msg):
        if not quiet:
            print(msg)

    import requests as _req

    api_key = os.environ.get("SIMMER_API_KEY", "")
    if not api_key:
        return 0

    try:
        resp = _req.get(
            "https://api.simmer.markets/api/sdk/positions",
            params={"status": "active", "venue": VENUE, "source": TRADE_SOURCE},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        resp.raise_for_status()
        positions = resp.json().get("positions", [])
    except Exception as e:
        log(f"  [exit-check] Failed to fetch positions: {e}")
        return 0

    now = datetime.now(timezone.utc)
    exited = 0
    journal = load_position_journal()

    for p in positions:
        market_id   = p.get("market_id", "")
        question    = p.get("question", "")[:55]
        shares_yes  = p.get("shares_yes", 0) or 0
        shares_no   = p.get("shares_no", 0) or 0
        cur_price   = p.get("current_probability") or 0
        resolves    = p.get("resolves_at", "")

        if shares_no > shares_yes:
            side = "no"
            shares = shares_no
            current_p = 1.0 - cur_price
        else:
            side = "yes"
            shares = shares_yes
            current_p = cur_price

        if shares < 0.01:
            continue

        # Use journaled entry data; fall back to avg_cost approximation for pre-journal positions
        jdata = journal.get(market_id, {})
        entry_p    = jdata.get("entry_price") or (p.get("avg_cost") or 0)
        entry_edge = jdata.get("entry_edge") or MIN_SPREAD
        entered_at = jdata.get("entered_at") or p.get("created_at", "")
        orig_hours = jdata.get("hours_to_expiry")

        if entry_p == 0:
            continue

        # Take-profit: AMM price converged toward fair value by >= TAKE_PROFIT_PCT of entry edge
        price_move = current_p - entry_p
        tp_threshold = entry_edge * TAKE_PROFIT_PCT
        take_profit_hit = price_move >= tp_threshold

        # Time-stop: elapsed >= TIME_STOP_PCT * original hours_to_expiry window
        time_stop_hit = False
        elapsed_hours = 0.0
        try:
            resolves_dt = datetime.fromisoformat(resolves.replace("Z", "+00:00"))
            hours_remaining = (resolves_dt - now).total_seconds() / 3600
            if entered_at:
                entered_dt = datetime.fromisoformat(entered_at.replace("Z", "+00:00"))
                elapsed_hours = (now - entered_dt).total_seconds() / 3600
                window = orig_hours if orig_hours else elapsed_hours + max(hours_remaining, 0)
                if window > 0:
                    time_stop_hit = elapsed_hours >= (window * TIME_STOP_PCT)
            elif orig_hours:
                # Have original window but no entered_at: fire time-stop when less than
                # (1 - TIME_STOP_PCT) of original window remains
                time_stop_hit = hours_remaining <= (orig_hours * (1.0 - TIME_STOP_PCT))
            else:
                # No entry data: fire time-stop when < 2h to expiry (last-resort exit)
                time_stop_hit = 0 < hours_remaining < 2.0
        except Exception:
            pass

        reason = None
        if take_profit_hit:
            reason = f"take-profit: move={price_move:+.3f} >= threshold={tp_threshold:.3f}"
        elif time_stop_hit:
            reason = f"time-stop: elapsed={elapsed_hours:.1f}h >= {TIME_STOP_PCT:.0%} of entry window"

        if reason:
            log(f"\n  [EXIT] {question}")
            log(f"     side={side} shares={shares:.2f} entry={entry_p:.3f} now={current_p:.3f}")
            log(f"     Reason: {reason}")
            if not dry_run:
                result = execute_exit(market_id, side, shares, reasoning=f"Spread sniper exit: {reason}")
                if result.get("success"):
                    log(f"     ✅ Exited {shares:.2f} shares")
                    clear_entry(market_id)
                    exited += 1
                else:
                    log(f"     ❌ Exit failed: {result.get('error') or result.get('skip_reason')}")
            else:
                log(f"     [PAPER] would exit {shares:.2f} shares")
                exited += 1

    # Clear journal entries for positions no longer returned by Simmer (already resolved)
    api_market_ids = {p.get("market_id") for p in positions}
    stale = [mid for mid in list(journal.keys()) if mid not in api_market_ids]
    if stale:
        for mid in stale:
            journal.pop(mid, None)
            log(f"  [exit-check] Cleared stale journal entry: {mid}")
        save_position_journal(journal)

    return exited


def calculate_position_size(smart_sizing):
    if not smart_sizing:
        return MAX_POSITION_USD
    portfolio = get_portfolio()
    if not portfolio:
        return MAX_POSITION_USD
    balance = portfolio.get("balance_usdc", 0)
    smart = min(max(balance * SMART_SIZING_PCT, 1.0), MAX_POSITION_USD)
    return smart


def run_strategy(dry_run=True, positions_only=False, show_config=False,
                 smart_sizing=False, use_safeguards=True, quiet=False):

    def log(msg, force=False):
        if not quiet or force:
            print(msg)

    log("📊 Polymarket Spread Sniper")
    log("=" * 50)

    get_client(live=not dry_run)

    if dry_run:
        log("\n  [PAPER MODE] Use --live for real trades.")

    log(f"\n  Venue:      {VENUE}")
    log(f"  Min edge:   {MIN_SPREAD:.1%}")
    log(f"  Trade fee:  {TRADE_FEE:.1%}")
    log(f"  Min volume: ${MIN_VOLUME:,.0f}")
    log(f"  Max pos:    ${MAX_POSITION_USD:.2f}")
    log(f"  Price range:{MIN_PRICE:.0%} – {MAX_PRICE:.0%}")
    log(f"  Max hours:  {MAX_HOURS}h")
    log(f"  Max CLOB spread: {MAX_CLOB_SPREAD:.2f}")
    log(f"  Daily max spend: ${DAILY_MAX_SPEND:.2f}")
    log(f"  Take-profit: {TAKE_PROFIT_PCT:.0%} of edge | Time-stop: {TIME_STOP_PCT:.0%} of window")
    log(f"  Filter:     '{MARKET_FILTER}' | Exclude: {len(MARKET_EXCLUDE)} keywords")

    if show_config:
        return 0

    if positions_only:
        from dataclasses import asdict
        positions = get_client().get_positions(venue=VENUE)
        tagged = [asdict(p) for p in positions if TRADE_SOURCE in str(getattr(p, "sources", ""))]
        log(f"\n📋 Open positions ({len(tagged)}):")
        for p in tagged:
            log(f"  {p.get('question','')[:55]} | pnl={p.get('pnl',0):+.2f}")
        return 0

    # Run exits check + market fetch concurrently (independent)
    log("\n🚪 Checking exits + scanning markets...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as _pre_ex:
        _exits_fut = _pre_ex.submit(check_exits, dry_run, quiet)
        _markets_fut = _pre_ex.submit(fetch_markets)

    exits = _exits_fut.result()
    if exits:
        log(f"  Exited {exits} position(s)")

    # Load daily loss limit state
    daily_state = load_daily_state()
    if daily_state["spent"] >= DAILY_MAX_SPEND:
        log(f"\n  Daily spend limit reached (${daily_state['spent']:.2f} / ${DAILY_MAX_SPEND:.2f}). Stopping.")
        if os.environ.get("AUTOMATON_MANAGED"):
            print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "daily_limit_reached"}}))
        return 0

    log("\n🔍 Scanning markets...")
    markets = _markets_fut.result()
    log(f"  {len(markets)} markets loaded")

    position_size = calculate_position_size(smart_sizing)
    trades_executed = 0
    trades_attempted = 0
    signals_found = 0
    skip_reasons = []
    execution_errors = []

    # --- Pass 1: pre-filter without CLOB (cheap), then batch-fetch CLOB in parallel ---
    now_utc = datetime.now(timezone.utc)
    candidates = []
    for market in markets:
        try:
            market_id = market.get("id")
            vol       = market.get("volume_24h")  # None = API doesn't have it, not zero
            market_p  = market.get("current_probability", 0.5) or 0.5
            token_id  = market.get("polymarket_token_id", "")
            resolves  = market.get("resolves_at", "")
            full_q    = market.get("question", "")

            # Skip only if volume is known and below threshold; null = pass through
            if (vol is not None and vol < MIN_VOLUME) or not token_id:
                continue
            if not (MIN_PRICE <= market_p <= MAX_PRICE):
                continue
            if MARKET_FILTER and MARKET_FILTER.lower() not in full_q.lower():
                continue
            if any(kw.lower() in full_q.lower() for kw in MARKET_EXCLUDE):
                continue
            try:
                dt = datetime.fromisoformat(resolves.replace("Z", "+00:00"))
                hours = (dt - now_utc).total_seconds() / 3600
                if hours < 0 or hours > MAX_HOURS:
                    continue
            except Exception:
                continue
            candidates.append({**market, "_hours": hours})
        except Exception:
            continue

    # Parallel CLOB fetch for all candidates
    from concurrent.futures import ThreadPoolExecutor as _TPE, as_completed as _ac

    def _fetch_clob(m):
        return m, get_clob_spread(m.get("polymarket_token_id", ""))

    signals = []
    clob_results = {}
    if not candidates:
        return signals
    candidates = candidates[:150]
    with _TPE(max_workers=max(1, min(len(candidates), 50))) as ex:
        futs = {ex.submit(_fetch_clob, m): m for m in candidates}
        for fut in _ac(futs, timeout=30):
            try:
                m, (best_bid, best_ask, spread, mid) = fut.result()
                clob_results[m.get("id")] = (best_bid, best_ask, spread, mid)
            except Exception:
                pass

    for market in candidates:
        try:
            market_id = market.get("id")
            question  = market.get("question", "")[:60]
            vol       = market.get("volume_24h")
            market_p  = market.get("current_probability", 0.5) or 0.5
            hours     = market["_hours"]

            clob = clob_results.get(market_id)
            if not clob or clob[2] is None:
                continue
            best_bid, best_ask, clob_spread, clob_mid = clob
            if clob_spread > MAX_CLOB_SPREAD:
                continue

            # Edge = divergence between Simmer price (last-trade/oracle) and live CLOB mid.
            # When Simmer lags the CLOB, we buy the cheap side and capture the gap as it closes.
            if market_p < clob_mid:
                side = "yes"
                entry_price = market_p
                edge = (clob_mid - market_p) - (entry_price * TRADE_FEE)
            else:
                side = "no"
                entry_price = 1.0 - market_p
                edge = (market_p - clob_mid) - (entry_price * TRADE_FEE)

            if edge < MIN_SPREAD:
                continue

            signals.append({
                "market_id":   market_id,
                "question":    question,
                "vol":         vol,
                "amm_yes":     market_p,
                "clob_mid":    clob_mid,
                "clob_spread": clob_spread,
                "edge":        edge,
                "side":        side,
                "entry_price": entry_price,
                "hours":       hours,
            })
        except Exception:
            continue

    # Sort by edge descending — execute strongest signals first
    signals.sort(key=lambda s: s["edge"], reverse=True)
    signals_found = len(signals)

    # --- Pass 2: execute up to MAX_TRADES_PER_RUN best signals ---
    for sig in signals:
        if trades_executed >= MAX_TRADES_PER_RUN:
            break

        # Re-check daily limit before each trade
        if daily_state["spent"] >= DAILY_MAX_SPEND:
            log(f"\n  Daily spend limit reached (${daily_state['spent']:.2f} / ${DAILY_MAX_SPEND:.2f}). Stopping.")
            break

        market_id   = sig["market_id"]
        question    = sig["question"]
        vol         = sig["vol"]
        amm_yes     = sig["amm_yes"]
        clob_mid    = sig["clob_mid"]
        clob_spread = sig["clob_spread"]
        edge        = sig["edge"]
        side        = sig["side"]
        entry_price = sig["entry_price"]
        hours       = sig["hours"]

        log(f"\n  {question}")
        log(f"     AMM_yes={amm_yes:.3f} CLOB_mid={clob_mid:.3f} clob_spread={clob_spread:.3f} edge={edge:.3f} {hours:.0f}h")
        vol_str = f"${vol:.0f}" if vol is not None else "n/a"
        log(f"     → BUY {side.upper()} via {VENUE} @ ~{entry_price:.3f} | vol={vol_str}")

        trades_attempted += 1
        result = execute_trade(
            market_id, side, position_size,
            reasoning=f"Spread snipe ({VENUE}): mid={mid:.3f} vs price={market_p:.3f}, edge={edge:.3f}, {hours:.0f}h to resolve"
        )

        if result.get("success"):
            trades_executed += 1
            shares = result.get("shares_bought", 0)
            sim = result.get("simulated", False)
            log(f"     {'[PAPER] ' if sim else ''}✅ Bought {shares:.1f} shares @ ${position_size:.2f}")
            record_entry(market_id, side, entry_price, edge, hours)
            # Update daily state
            daily_state["spent"] += position_size
            daily_state["trades"] += 1
            save_daily_state(daily_state)
        elif result.get("skip_reason"):
            skip_reasons.append(result["skip_reason"])
            log(f"     ⏭️  Skipped: {result['skip_reason']}")
        else:
            err = result.get("error", "unknown")
            execution_errors.append(err)
            log(f"     ❌ Failed: {err}")

    log(f"\n{'=' * 50}")
    log(f"  Signals: {signals_found} | Executed: {trades_executed}/{trades_attempted}")
    log(f"  Daily spend: ${daily_state['spent']:.2f} / ${DAILY_MAX_SPEND:.2f}")

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
        if signals_found == 0:
            report["skip_reason"] = "no_signal"
        print(json.dumps({"automaton": report}))

    return signals_found


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket Spread Sniper")
    parser.add_argument("--live",          action="store_true")
    parser.add_argument("--dry-run",       action="store_true")
    parser.add_argument("--positions",     action="store_true")
    parser.add_argument("--config",        action="store_true")
    parser.add_argument("--set",           action="append", metavar="KEY=VALUE")
    parser.add_argument("--smart-sizing",  action="store_true")
    parser.add_argument("--no-safeguards", action="store_true")
    parser.add_argument("--quiet", "-q",   action="store_true")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                k, v = item.split("=", 1)
                if k in CONFIG_SCHEMA:
                    try:
                        v = CONFIG_SCHEMA[k]["type"](v)
                    except Exception:
                        pass
                updates[k] = v
        if updates:
            update_config(updates, __file__)
            print(f"Config updated: {updates}")
            _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)
            globals().update({
                "VENUE":             _config["venue"],
                "MIN_SPREAD":        _config["min_spread"],
                "MIN_VOLUME":        _config["min_volume"],
                "MAX_POSITION_USD":  _config["max_position_usd"],
                "MAX_TRADES_PER_RUN":_config["max_trades_per_run"],
                "MIN_PRICE":         _config["min_price"],
                "MAX_PRICE":         _config["max_price"],
                "MAX_HOURS":         _config["max_hours"],
                "MAX_CLOB_SPREAD":   _config["max_clob_spread"],
                "DAILY_MAX_SPEND":   _config["daily_max_spend"],
                "TAKE_PROFIT_PCT":   _config["take_profit_pct"],
                "TIME_STOP_PCT":     _config["time_stop_pct"],
            })

    run_strategy(
        dry_run=not args.live,
        positions_only=args.positions,
        show_config=args.config,
        smart_sizing=args.smart_sizing,
        use_safeguards=not args.no_safeguards,
        quiet=args.quiet,
    )

#!/usr/bin/env python3
"""
Simmer FastLoop Improved (V8.10 "Industrial Sniper")

This version is based on the official Simmer SDK trading examples but has been heavily 
optimized for continuous, high-conviction sniper execution. The core logic relies on 
NOFX data, Binance L2 orderbook analysis, and Pin Bar morphological filtering.

[V8.10 Engine Upgrade]: Replaced raw Simmer SDK calls with a hybrid "Pre-Caching ID Strategy". 
Uses persistent local JSON storage to prevent Polymarket's 5m "in-progress" API blindspot.

Authors: Antigravity & USER
"""

import os
import sys
import json
import math
import time
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote

# Force line-buffered stdout
sys.stdout.reconfigure(line_buffering=True)

# =============================================================================
# Configuration (Official SCHEMA + Sniper Extensions)
# =============================================================================

CONFIG_SCHEMA = {
    # Official Simmer Params
    "entry_threshold": {"default": 0.05, "env": "SIMMER_SPRINT_ENTRY", "type": float,
                        "help": "Min price divergence from 50¢ to trigger"},
    "min_momentum_pct": {"default": 0.01, "env": "SIMMER_SPRINT_MOMENTUM", "type": float,
                         "help": "Min BTC % move in lookback window"},
    "max_position": {"default": 5.0, "env": "SIMMER_SPRINT_MAX_POSITION", "type": float,
                     "help": "Max $ per trade"},
    "signal_source": {"default": "binance", "env": "SIMMER_SPRINT_SIGNAL", "type": str,
                      "help": "Price feed source"},
    "lookback_minutes": {"default": 5, "env": "SIMMER_SPRINT_LOOKBACK", "type": int,
                         "help": "Momentum lookback minutes"},
    "min_time_remaining": {"default": 0, "env": "SIMMER_SPRINT_MIN_TIME", "type": int,
                           "help": "Skip if < X secs (0=auto)"},
    "asset": {"default": "BTC", "env": "SIMMER_SPRINT_ASSET", "type": str,
              "help": "Asset (BTC, ETH, SOL)"},
    "window": {"default": "5m", "env": "SIMMER_SPRINT_WINDOW", "type": str,
               "help": "Duration (5m or 15m)"},
    "volume_confidence": {"default": True, "env": "SIMMER_SPRINT_VOL_CONF", "type": bool,
                          "help": "Weight signal by volume"},
    "daily_budget": {"default": 10.0, "env": "SIMMER_SPRINT_DAILY_BUDGET", "type": float,
                     "help": "Max spend per UTC day"},
    
    # Sniper Specific Extensions
    "require_orderbook": {"default": True, "env": "SIMMER_REQ_OB", "type": bool,
                          "help": "Verify with Binance L2 book depth"},
    "require_funding": {"default": False, "env": "SIMMER_REQ_FUNDING", "type": bool,
                        "help": "Skip if funding is crowded"},
    "fee_buffer": {"default": 0.02, "env": "SIMMER_FEE_BUFFER", "type": float,
                   "help": "Extra EV margin to cover fees"},
    "max_pin_bar_tail_pct": {"default": 0.3, "env": "SIMMER_PIN_BAR_MAX", "type": float,
                             "help": "Max top/bottom tail ratio allowed to filter Pin Bar noise"},
    "oi_neutral_zone": {"default": 2.0, "env": "SIMMER_OI_NEUTRAL", "type": float,
                        "help": "OI % change buffer (e.g. 2.0 means +/-2% doesn't block signal)"},
    "min_wall_usd": {"default": 500000.0, "env": "SIMMER_MIN_WALL_USD", "type": float,
                     "help": "Minimum USD volume required at a price level to be considered a Wall"},
    "wall_scan_depth": {"default": 50, "env": "SIMMER_WALL_SCAN_DEPTH", "type": int,
                        "help": "Number of orderbook levels to scan for walls (up to 100)"},
}

TRADE_SOURCE = "sdk:polymarket-simmer-fastloop-sync-pulse"
SKILL_SLUG = "polymarket-simmer-fastloop-sync-pulse"
ASSET_SYMBOLS = {"BTC": "BTCUSDT", "ETH": "ETHUSDT", "SOL": "SOLUSDT"}
ASSET_PATTERNS = {"BTC": ["bitcoin up or down"], "ETH": ["ethereum up or down"], "SOL": ["solana up or down"]}
POLY_FEE_RATE, POLY_FEE_EXPONENT = 0.25, 2
_automaton_reported = False

# =============================================================================
# Infrastructure (100% Official V6.1 Naming & Flow)
# =============================================================================

from simmer_sdk.skill import load_config, update_config
cfg = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)

ENTRY_THRESHOLD = cfg["entry_threshold"]
MIN_MOMENTUM_PCT = cfg["min_momentum_pct"]
MAX_POSITION_USD = cfg["max_position"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max: MAX_POSITION_USD = min(MAX_POSITION_USD, float(_automaton_max))
SIGNAL_SOURCE = cfg["signal_source"]
LOOKBACK_MINUTES = cfg["lookback_minutes"]
ASSET, WINDOW, DAILY_BUDGET = cfg["asset"].upper(), cfg["window"], cfg["daily_budget"]

# Debug Config (V9.2 Cleaner)


TARGET_TIME_MIN, TARGET_TIME_MAX = 0, 999999 # Hardcode to infinity since V9.0 bypasses this
REQUIRE_ORDERBOOK, REQUIRE_FUNDING = cfg["require_orderbook"], cfg["require_funding"]
FEE_BUFFER = cfg["fee_buffer"]
MAX_PIN_BAR_TAIL_PCT = cfg.get("max_pin_bar_tail_pct", 0.3)
OI_NEUTRAL = cfg.get("oi_neutral_zone", 2.0)
MIN_WALL_USD = cfg.get("min_wall_usd", 1000000.0)
WALL_SCAN_DEPTH = cfg.get("wall_scan_depth", 50)

_window_seconds = {"5m": 300, "15m": 900, "1h": 3600}
_configured_min_time = cfg["min_time_remaining"]
MIN_TIME_REMAINING = _configured_min_time if _configured_min_time > 0 else max(30, _window_seconds.get(WINDOW, 300) // 10)
VOLUME_CONFIDENCE = cfg["volume_confidence"]

def log(msg, force=False, quiet=False):
    if not quiet or force: print(msg)

def _get_spend_path(skill_file):
    from pathlib import Path
    return Path(skill_file).parent / "daily_spend.json"

def _load_daily_spend(skill_file):
    path = _get_spend_path(skill_file)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
            if data.get("date") == today: return data
        except Exception: pass
    return {"date": today, "spent": 0.0, "trades": 0}

def _save_daily_spend(skill_file, data):
    with open(_get_spend_path(skill_file), "w") as f: json.dump(data, f, indent=2)

def _get_ledger_path(skill_file):
    from pathlib import Path
    return Path(skill_file).parent / "fastloop_ledger.json"

def _log_trade_to_ledger(skill_file, **kwargs):
    path = _get_ledger_path(skill_file)
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), **kwargs}
    ledger = []
    if path.exists():
        try:
            with open(path) as f: ledger = json.load(f)
        except Exception: pass
    ledger.append(entry)
    with open(path, "w") as f: json.dump(ledger, f, indent=2)

_client = None
_discovery_client = None
CLOB_API = "https://clob.polymarket.com"

def get_client(live=True, discovery=False):
    global _client, _discovery_client
    
    # New V8.9.3: Discovery Client always uses real-market venue to avoid scanning "empty" sim servers
    if discovery:
        if _discovery_client is None:
            from simmer_sdk import SimmerClient
            api_key = os.environ.get("SIMMER_API_KEY")
            if not api_key: print("Error: SIMMER_API_KEY for discovery not set"); sys.exit(1)
            # Discovery doesn't need a wallet or live-signing
            _discovery_client = SimmerClient(api_key=api_key, venue="polymarket", live=True)
        return _discovery_client

    if _client is None:
        from simmer_sdk import SimmerClient
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key: print("Error: SIMMER_API_KEY not set"); sys.exit(1)
        
        priv_key = os.environ.get("WALLET_PRIVATE_KEY")
        venue = "polymarket" if priv_key else "sim"
        
        if priv_key:
            print(f"🔐 Wallet Private Key detected. Mode: {venue.upper()} (LIVE: {live})")
        else:
            print(f"🍦 No Wallet Private Key. Mode: SIMULATION (Dry Run: {live})")

        _client = SimmerClient(api_key=api_key, venue=venue, live=live, private_key=priv_key)
    return _client

def _api_request(url, method="GET", data=None, headers=None, timeout=15):
    try:
        req_headers = headers or {}
        if "User-Agent" not in req_headers: req_headers["User-Agent"] = "simmer-sdk/6.1"
        body = json.dumps(data).encode("utf-8") if data else None
        if data: req_headers["Content-Type"] = "application/json"
        req = Request(url, data=body, headers=req_headers, method=method)
        with urlopen(req, timeout=timeout) as resp: return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        try:
            error_body = json.loads(e.read().decode("utf-8"))
            return {"error": error_body.get("detail", str(e)), "status_code": e.code}
        except Exception: return {"error": str(e), "status_code": e.code}
    except URLError as e: return {"error": f"Connection error: {e.reason}"}
    except Exception as e: return {"error": str(e)}

def fetch_live_midpoint(token_id):
    res = _api_request(f"{CLOB_API}/midpoint?token_id={quote(str(token_id))}", timeout=5)
    if not res or not isinstance(res, dict) or res.get("error"): return None
    try: return float(res["mid"])
    except Exception: return None

def fetch_live_prices(clob_token_ids):
    if not clob_token_ids: return None
    return fetch_live_midpoint(clob_token_ids[0])

def _lookup_fee_rate(token_id):
    res = _api_request(f"{CLOB_API}/fee-rate?token_id={quote(str(token_id))}")
    try: return int(float(res.get("base_fee") or 0))
    except Exception: return 0

# =============================================================================
# Discovery & Local Cache (V8.10 Pre-Caching ID Strategy)
# =============================================================================

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'fast_markets_cache.json')

def _update_market_cache(new_markets):
    """Save future markets to local cache to survive API disappearing act."""
    now = datetime.now(timezone.utc)
    cache = []
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                saved = json.load(f)
                cache = [m for m in saved if _parse_resolves_at(m.get('end_time')) and _parse_resolves_at(m.get('end_time')) > now]
        except Exception: pass
    
    cache_dict = {m.get('market_id'): m for m in cache if m.get('market_id')}
    for m in new_markets:
        if m.get('market_id') and m.get('end_time') and m['end_time'] > now:
            m_copy = m.copy()
            m_copy['end_time'] = m['end_time'].isoformat()
            cache_dict[m['market_id']] = m_copy
            
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(list(cache_dict.values()), f)
        if len(new_markets) > 0:
            print(f"  [Ignition] Successfully cached {len(new_markets)} future market IDs.")
    except Exception: pass

def _get_cached_markets():
    """Load cached active markets."""
    now = datetime.now(timezone.utc)
    if not os.path.exists(CACHE_FILE): return []
    try:
        with open(CACHE_FILE, 'r') as f:
            saved = json.load(f)
            parsed = []
            for m in saved:
                dt = _parse_resolves_at(m.get('end_time'))
                if dt and dt > now:
                    m['end_time'] = dt
                    m['source'] = 'cache'
                    # Force is_live_now to None so `find_best_fast_market` uses strict time-based radar to engage
                    m['is_live_now'] = None
                    parsed.append(m)
            return parsed
    except Exception: return []

def discover_fast_market_markets(asset="BTC", window="5m", include_gamma=True):
    simmer_markets = []
    try:
        # V8.9.5: Always fetch both to ensure we see the "imminent" market even if SDK list is long
        sdk_m = get_client(discovery=True).get_fast_markets(asset=asset, window=window, limit=100)
        for m in (sdk_m or []):
            raw_res = getattr(m, 'resolves_at', None)
            end_time = _parse_resolves_at(raw_res)
            if not end_time:
                end_time = _parse_fast_market_end_time(m.question)
            simmer_markets.append({
                "question": m.question, "market_id": m.id, "end_time": end_time,
                "clob_token_ids": [m.polymarket_token_id, m.polymarket_no_token_id],
                "is_live_now": m.is_live_now, "source": "simmer", "slug": getattr(m, 'slug', None)
            })
    except Exception as e: log(f"  [Discovery] Simmer API skip: {e}")
    
    # V8.10 Cache Injection: Save upcoming markets, resurrect hidden/active ones
    _update_market_cache(simmer_markets)
    cached_markets = _get_cached_markets()
    
    # Always scan Gamma for supplemental radar visibility
    gamma_markets = _discover_via_gamma(asset, window)
    
    # Merge by question name to avoid duplicates
    seen, merged = set(), []
    for m in simmer_markets + cached_markets + gamma_markets:
        if m["question"] not in seen:
            seen.add(m["question"])
            merged.append(m)
    
    # Sort by absolute proximity to current time to find the most relevant one
    now = datetime.now(timezone.utc)
    merged.sort(key=lambda x: abs((x['end_time'] - now).total_seconds()) if x.get('end_time') else 999999)
    return merged

def _discover_via_gamma(asset, window):
    patterns = ASSET_PATTERNS.get(asset, ["bitcoin up or down"])
    url = "https://gamma-api.polymarket.com/markets?limit=100&closed=false&tag=crypto&order=endDate&ascending=true"
    res = _api_request(url)
    if not res or (isinstance(res, dict) and res.get("error")): return []
    markets = []
    for m in res:
        q, slug = (m.get("question") or "").lower(), m.get("slug", "")
        if f"-{window}-" in slug and any(p in q for p in patterns):
            markets.append({
                "question": m.get("question", ""), "slug": slug, "market_id": m.get("id"),
                "end_time": _parse_fast_market_end_time(m.get("question", "")),
                "clob_token_ids": json.loads(m.get("clobTokenIds", "[]")) if isinstance(m.get("clobTokenIds"), str) else (m.get("clobTokenIds") or []),
                "fee_rate_bps": int(m.get("fee_rate_bps") or 0), "source": "gamma",
            })
    return markets

def _parse_resolves_at(s):
    if not s: return None
    # V8.9.3: Robust check if s is already a datetime (some SDK versions might auto-parse)
    if isinstance(s, datetime): return s.astimezone(timezone.utc)
    try:
        # Standard Simmer format: "2024-03-07 20:00:00Z"
        clean = s.replace("Z", "+00:00").replace(" ", "T")
        return datetime.fromisoformat(clean)
    except Exception as e:
        log(f"    [Warning] Failed to parse SDK resolves_at string '{s}': {e}")
        return None

def _parse_fast_market_end_time(q):
    import re
    match = re.search(r'(\w+ \d+),.*?-\s*(\d{1,2}(?::\d{2})?(?:AM|PM))\s*ET', q)
    if not match: return None
    t_str = match.group(2)
    if ":" not in t_str: t_str = t_str.replace("AM", ":00AM").replace("PM", ":00PM")
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.strptime(f"{match.group(1)} {datetime.now().year} {t_str}", "%B %d %Y %I:%M%p")
        return dt.replace(tzinfo=ZoneInfo("America/New_York")).astimezone(timezone.utc)
    except Exception: return None

def find_best_fast_market(markets):
    now = datetime.now(timezone.utc)
    max_rem = _window_seconds.get(WINDOW, 300) * 2
    candidates = []
    for m in markets:
        rem = (m['end_time'] - now).total_seconds() if m.get('end_time') else 0
        is_physically_live = (rem <= 300)
        
        if m.get("is_live_now") is not None:
            is_live = m["is_live_now"] or is_physically_live
            if is_live and rem > MIN_TIME_REMAINING: candidates.append((rem, m))
        elif rem > MIN_TIME_REMAINING and rem < max_rem: candidates.append((rem, m))
    if not candidates: return None
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

# =============================================================================
# Sniper Brain (NOFX, L2 Walls, Binance Momentum)
# =============================================================================

def fetch_nofx_oi(asset="BTC", duration="5m"):
    sym = ASSET_SYMBOLS.get(asset, "BTCUSDT")
    # Rule: Check both Top (Increase) and Low (Decrease) rankings
    for rank_type in ["top-ranking", "low-ranking"]:
        url = f"https://nofxos.ai/api/oi/{rank_type}?auth=cm_568c67eae410d912c54c&duration={duration}"
        res = _api_request(url)
        if res and "data" in res and "positions" in res["data"]:
            for i in res['data']['positions']:
                if i['symbol'] == sym: return float(i.get('oi_delta_percent', 0.0)) * 100
    return 0.0

def fetch_nofx_netflow(asset="BTC", duration="5m"):
    sym = ASSET_SYMBOLS.get(asset, "BTCUSDT")
    # Rule: Check both Top (Inflow) and Low (Outflow) rankings
    # Institution type is mandatory per user blueprint
    for rank_type in ["top-ranking", "low-ranking"]:
        url = f"https://nofxos.ai/api/netflow/{rank_type}?auth=cm_568c67eae410d912c54c&type=institution&duration={duration}"
        res = _api_request(url)
        if res and "data" in res and "netflows" in res["data"]:
            for i in res['data']['netflows']:
                if i['symbol'] == sym:
                    amt = float(i.get('amount', 0.0))
                    # low-ranking (outflow) should be returned as negative for logic consistency
                    return amt if rank_type == "top-ranking" else -abs(amt)
    return 0.0


def fetch_binance_orderbook(asset="BTC", limit=100):
    url = f"https://api.binance.com/api/v3/depth?symbol={ASSET_SYMBOLS.get(asset, 'BTCUSDT')}&limit={limit}"
    res = _api_request(url)
    if not res or "bids" not in res: return None
    bids, asks = [[float(i[0]), float(i[1])] for i in res["bids"]], [[float(i[0]), float(i[1])] for i in res["asks"]]
    mid = (bids[0][0] + asks[0][0]) / 2
    b_depth, a_depth = sum(p*v for p,v in bids if p > mid * 0.999), sum(p*v for p,v in asks if p < mid * 1.001)
    
    scan_limit = min(limit, WALL_SCAN_DEPTH)
    return {
        "imbalance": (b_depth - a_depth) / (b_depth + a_depth) if (b_depth + a_depth) > 0 else 0,
        "has_ask_wall": any(p*v > MIN_WALL_USD for p,v in asks[:scan_limit]),
        "has_bid_wall": any(p*v > MIN_WALL_USD for p,v in bids[:scan_limit]),
    }

def fetch_binance_orderbook_verified(asset="BTC", limit=100, delay=1.5):
    res1 = fetch_binance_orderbook(asset, limit)
    if not res1: return None
    if res1['has_ask_wall'] or res1['has_bid_wall']:
        log(f"  [L2] Wall detected. Waiting {delay}s for spoofing double-check...", quiet=False)
        time.sleep(delay)
        res2 = fetch_binance_orderbook(asset, limit)
        if not res2: return res1
        res1['has_ask_wall'] = res1['has_ask_wall'] and res2['has_ask_wall']
        res1['has_bid_wall'] = res1['has_bid_wall'] and res2['has_bid_wall']
        if not (res1['has_ask_wall'] or res1['has_bid_wall']):
            log(f"  [L2] Spoofing detected! The wall disappeared.", quiet=False)
        else:
            log(f"  [L2] Wall remains solid.", quiet=False)
    return res1

def get_binance_momentum(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=12"
    res = _api_request(url)
    if not res or isinstance(res, dict) or len(res) < 2: return None
    try:
        # Use the PREVIOUS COMPLETED 5m candle for stable momentum analysis
        # res[-2] is the candle that just closed
        p_close, p_open = float(res[-2][4]), float(res[-2][1])
        p_high, p_low = float(res[-2][2]), float(res[-2][3])
        p_1h_start = float(res[0][1])
        v_avg = sum(float(i[5]) for i in res[:-1]) / (len(res)-1)
        v_last_5m = float(res[-2][5]) # Volume of the completed candle
        
        kline_range = p_high - p_low
        top_tail = p_high - max(p_open, p_close)
        bottom_tail = min(p_open, p_close) - p_low

        return {
            "momentum_pct": ((p_close - p_open) / p_open) * 100,
            "direction_5m": "up" if p_close > p_open else "down",
            "top_tail_ratio": top_tail / kline_range if kline_range > 0 else 0,
            "bottom_tail_ratio": bottom_tail / kline_range if kline_range > 0 else 0,
            "volume_ratio": v_last_5m / v_avg if v_avg > 0 else 1.0,
            "price_now": float(res[-1][4])
        }
    except Exception: return None

# =============================================================================
# Execution & Reporting (100% Official V6.1 Parity)
# =============================================================================

def get_positions():
    try:
        from dataclasses import asdict
        return [asdict(p) for p in get_client().get_positions()]
    except Exception: return []

def calculate_position_size(momentum_data):
    return MAX_POSITION_USD

def _emit_skip_report(signals=1, attempted=0, executed=0, skips=None, error=None, amount=0):
    global _automaton_reported
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        report = {"signals": signals, "trades_attempted": attempted, "trades_executed": executed, "amount_usd": round(amount, 2)}
        if skips: report["skip_reason"] = ", ".join(dict.fromkeys(skips))
        if error: report["execution_errors"] = [error]
        print(json.dumps({"automaton": report}))
        _automaton_reported = True

def run_fast_market_strategy(dry_run=True, positions_only=False, quiet=False):
    log("⚡ Simmer V6.1: Industrial Sniper", force=True, quiet=quiet)
    log("="*50, quiet=quiet)

    # 1. Official Flow: Budget
    daily_spend = _load_daily_spend(__file__)
    log(f"⚙️ Config: {ASSET} {WINDOW} | Budget: ${daily_spend['spent']:.2f}/${DAILY_BUDGET:.2f}", quiet=quiet)

    # Sniper Value-Add: Auto-Sync Delay
    # V9.2: Removed artificial sync delay as natural pipeline latency (~5.5s) is sufficient.
    if not positions_only:
        pass

    client = get_client(live=not dry_run)

    if positions_only:
        for p in get_positions():
            if "up or down" in p.get("question", "").lower():
                log(f"  • {p['question'][:60]} | PnL: ${p.get('pnl', 0):.2f}", force=True)
        return

    # 2. Discovery & Fee pre-fetch
    log(f"\n🔍 Discovering {ASSET} markets...", quiet=quiet)
    
    best, rem = None, 0
    # Retry Loop (up to 10 times, 1.5s each = 15s max)
    for attempt in range(10):
        # V8.9.5: Always fetch merged list for radar visibility
        markets = discover_fast_market_markets(ASSET, WINDOW)
        if markets:
            best_candidate = find_best_fast_market(markets)
            if best_candidate:
                now_utc = datetime.now(timezone.utc)
                candidate_rem = (best_candidate['end_time'] - now_utc).total_seconds()
                # Sniper Check (V9.0: Bypassed for Pre-Cached IDs)
                # if TARGET_TIME_MIN <= candidate_rem <= TARGET_TIME_MAX:
                #     best = best_candidate
                #     rem = candidate_rem
                #     break
                # else:
                #     log(f"  [Wait] Market found but {candidate_rem:.0f}s is outside Sniper Window [{TARGET_TIME_MIN}, {TARGET_TIME_MAX}].", quiet=quiet)
                best = best_candidate
                rem = candidate_rem
                break
            else:
                log(f"  [API Delay] No active markets in Discovery. Waiting 1.5s...", quiet=quiet)
        else:
            log(f"  [API Delay] Failed to fetch Simmer list. Waiting 1.5s...", quiet=quiet)
            
        time.sleep(1.5)

    if not best:
        log("  No tradeable markets found (outside window or not live).", quiet=quiet)
        _emit_skip_report(0, 0, 0, skips=["no_markets"])
        return

    log(f"🎯 Selected: {best['question']} ({rem:.0f}s left)", quiet=quiet)

    skip_reasons = []
    # Sniper Timing (V9.0: Bypassed)
    # if not (TARGET_TIME_MIN <= rem <= TARGET_TIME_MAX): skip_reasons.append("outside_window")
    # Official Dedup
    if any((p.get("market_id") == best["market_id"] or p.get("question") == best["question"]) and (p.get("shares_yes",0)+p.get("shares_no",0))>0 for p in get_positions()):
        skip_reasons.append("already_holding")

    if skip_reasons:
        log(f"  ⏸️ Skipping: {', '.join(skip_reasons)}", quiet=quiet)
        _emit_skip_report(1, 0, 0, skips=skip_reasons); return

    # 3. Decision Phase
    # V8.9.1: Optimized for cost (Simmer-First)
    # On-demand import is a paid feature, so we only use the market_id from Simmer
    target_market_id = best['market_id']
    if best.get('source') == 'gamma':
        # Skip trade if from gamma to avoid import fees (unless it was already imported)
        log("  [V8.9.1] Market sourced from Gamma. Skipping to avoid import fees.")
        return

    price_yes = fetch_live_prices(best["clob_token_ids"])
    if price_yes is None: print("  ❌ Error: Live CLOB price unavailable."); return
    log(f"  Current YES: ${price_yes:.3f} (Live CLOB)", quiet=quiet)

    log(f"\n📈 Analyzing signal...", quiet=quiet)
    mom = get_binance_momentum(ASSET_SYMBOLS[ASSET])
    book = fetch_binance_orderbook_verified(ASSET) if REQUIRE_ORDERBOOK else None
    oi_chg, nf_chg = fetch_nofx_oi(ASSET), fetch_nofx_netflow(ASSET)

    if not mom: print("  ❌ Failed to fetch signal data."); return
    log(f"  Mom: {mom['momentum_pct']:+.3f}% (Tail Top:{mom['top_tail_ratio']:.0%} Bottom:{mom['bottom_tail_ratio']:.0%}) | NOFX: OI {oi_chg:+.3f}% | NF ${nf_chg/1e6:.1f}M", quiet=quiet)

    # Sniper Logic CHOICE (Refined V7.3 - 0.01% Pass-through)
    m_pct = abs(mom['momentum_pct'])
    v_rat = mom.get('volume_ratio', 1.0)
    top_r, bot_r = mom.get('top_tail_ratio', 0.0), mom.get('bottom_tail_ratio', 0.0)
    
    # Pin Bar Filter
    is_up_clean = mom['direction_5m'] == "up" and top_r <= MAX_PIN_BAR_TAIL_PCT
    is_down_clean = mom['direction_5m'] == "down" and bot_r <= MAX_PIN_BAR_TAIL_PCT
    clean_kline = is_up_clean or is_down_clean

    if not clean_kline:
         log(f"  [Filter] Pin Bar detected (Shadow too long). Skipping noise.", quiet=False)

    # Effectively pass-through using configured MIN_MOMENTUM_PCT to let Sniper Brain (NOFX/L2) lead
    # V10.0: Added OI_NEUTRAL buffer to avoid noise-driven skips
    is_trend = (clean_kline and m_pct > MIN_MOMENTUM_PCT and v_rat > 1.0 and oi_chg > -OI_NEUTRAL and nf_chg * (1 if mom['direction_5m']=="up" else -1) > 0 and (not book or (mom['direction_5m']=="up" and not book['has_ask_wall']) or (mom['direction_5m']=="down" and not book['has_bid_wall'])))
    is_reversion = (clean_kline and m_pct > MIN_MOMENTUM_PCT and v_rat > 1.0 and oi_chg < OI_NEUTRAL and book and ((mom['direction_5m']=="up" and book['has_ask_wall']) or (mom['direction_5m']=="down" and book['has_bid_wall'])))
    
    side, reason = None, ""
    if is_trend: side, reason = ("yes" if mom['direction_5m']=="up" else "no"), "Trend: Flow follow + No wall"
    elif is_reversion: side, reason = ("no" if mom['direction_5m']=="up" else "yes"), "Reversion: Squeeze + Wall fade"

    if not side:
        log("  ⏸️ No high-conviction signal. Skip.", force=True)
        _emit_skip_report(1, 0, 0, skips=["no_signal"]); return

    # 4. EV & Fee Formula
    log(f"  Signal: {side.upper()} ({reason})", force=True, quiet=quiet)
    buy_p = price_yes if side=="yes" else (1 - price_yes)
    eff_fee_rate = POLY_FEE_RATE * (buy_p * (1 - buy_p)) ** POLY_FEE_EXPONENT
    min_div = buy_p * eff_fee_rate * 2 + FEE_BUFFER
    div = (0.5 + ENTRY_THRESHOLD - price_yes) if side=="yes" else (price_yes - (0.5 - ENTRY_THRESHOLD))

    if div < min_div:
        log(f"  ⏸️ Low EV: Divergence {div:.3f} < Min {min_div:.3f}.", force=True)
        _emit_skip_report(1, 0, 0, skips=["low_ev"]); return

    # 5. Sizing & Execution
    p_size = min(calculate_position_size(mom), DAILY_BUDGET - daily_spend["spent"])
    if p_size < 1.0:
        log("  ⏸️ Budget low. Skip.", force=True)
        _emit_skip_report(1, 1, 0, skips=["budget_low"]); return

    log(f"  ✅ Executing ${p_size:.2f} on {side.upper()}...", force=True)
    try:
        result = client.trade(
            market_id=target_market_id,
            side=side,
            amount=p_size,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reason
        )
        if result.success:
            log(f"  💰 Success! Bought {result.shares_bought:.1f} shares.", force=True)
            if not result.simulated:
                daily_spend["spent"] += p_size; daily_spend["trades"] += 1
                _save_daily_spend(__file__, daily_spend)
                _log_trade_to_ledger(__file__, market=best["question"], side=side, amount=p_size, result="executed")
            _emit_skip_report(1, 1, 1, amount=p_size)
        else:
            log(f"  ❌ Failed: {res.error}", force=True)
            _emit_skip_report(1, 1, 0, error=res.error)
    except Exception as e:
        log(f"  ❌ execution error: {e}", force=True)
        _emit_skip_report(1, 1, 0, error=str(e))

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--positions", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--set", action="append")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for s in args.set:
            k, v = s.split("=")
            updates[k] = float(v) if k in ["entry_threshold", "max_position", "daily_budget"] else v
        update_config(updates, __file__)
        sys.exit(0)

    if args.stats:
        ledger = []
        path = _get_ledger_path(__file__)
        if path.exists():
            with open(path) as f: ledger = json.load(f)
        print(f"📊 Stats: {len(ledger)} trades | Total Spent: ${sum(t['amount'] for t in ledger):.2f}")
        sys.exit(0)

    run_fast_market_strategy(dry_run=not args.live, positions_only=args.positions, quiet=args.quiet)

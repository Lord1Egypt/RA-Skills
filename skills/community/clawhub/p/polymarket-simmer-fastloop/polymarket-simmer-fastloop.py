#!/usr/bin/env python3
"""
Polymarket Simmer FastLoop Trader

Trades Polymarket BTC/ETH/SOL 5-minute and 15-minute fast markets using multi-signal CEX momentum.
Adds order book imbalance, time-of-day filtering, volatility-adjusted sizing,
win-rate calibration, and fee-accurate EV math.

Usage:
    python polymarket-simmer-fastloop.py              # Dry run (paper mode)
    python polymarket-simmer-fastloop.py --live       # Execute real trades
    python polymarket-simmer-fastloop.py --stats      # Show calibration stats
    python polymarket-simmer-fastloop.py --resolve    # Resolve expired positions
    python polymarket-simmer-fastloop.py --quiet      # Only output on trades/errors

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import math
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from pathlib import Path

# Force line-buffered stdout
sys.stdout.reconfigure(line_buffering=True)

# Optional: Trade Journal integration
JOURNAL_AVAILABLE = False
try:
    from tradejournal import log_trade
    JOURNAL_AVAILABLE = True
except ImportError:
    try:
        from skills.tradejournal import log_trade
        JOURNAL_AVAILABLE = True
    except ImportError:
        def log_trade(*args, **kwargs):
            pass

# =============================================================================
# Configuration
# =============================================================================

CONFIG_SCHEMA = {
    "entry_threshold": {"default": 0.05, "env": "SIMMER_ENTRY", "type": float,
                        "help": "Min divergence from 50c to trigger trade"},
    "min_momentum_pct": {"default": 1.0, "env": "SIMMER_MOMENTUM", "type": float,
                         "help": "Min % move (raised from 0.5 to 1.0)"},
    "max_position": {"default": 5.0, "env": "SIMMER_MAX_POSITION", "type": float,
                     "help": "Max $ per trade"},
    "signal_source": {"default": "binance", "env": "SIMMER_SIGNAL", "type": str,
                      "help": "Price feed source"},
    "lookback_minutes": {"default": 5, "env": "SIMMER_LOOKBACK", "type": int,
                         "help": "Minutes of price history"},
    "min_time_remaining": {"default": 60, "env": "SIMMER_MIN_TIME", "type": int,
                           "help": "Skip if < N seconds left"},
    "target_time_min": {"default": 90, "env": "SIMMER_TARGET_MIN", "type": int,
                        "help": "Prefer markets with >= N seconds left"},
    "target_time_max": {"default": 210, "env": "SIMMER_TARGET_MAX", "type": int,
                        "help": "Prefer markets with <= N seconds left"},
    "asset": {"default": "BTC", "env": "SIMMER_ASSET", "type": str,
              "help": "Asset to trade (BTC, ETH, SOL)"},
    "window": {"default": "5m", "env": "SIMMER_WINDOW", "type": str,
               "help": "Market window (5m or 15m)"},
    "volume_confidence": {"default": True, "env": "SIMMER_VOL_CONF", "type": bool,
                          "help": "Weight signal by volume"},
    "require_orderbook": {"default": False, "env": "SIMMER_ORDERBOOK", "type": bool,
                          "help": "Require order book imbalance confirmation"},
    "time_filter": {"default": True, "env": "SIMMER_TIME_FILTER", "type": bool,
                    "help": "Skip low-liquidity hours (02:00-06:00 UTC)"},
    "vol_sizing": {"default": True, "env": "SIMMER_VOL_SIZING", "type": bool,
                   "help": "Adjust size by volatility"},
    "fee_buffer": {"default": 0.05, "env": "SIMMER_FEE_BUFFER", "type": float,
                   "help": "Extra edge required above fee breakeven"},
    "daily_budget": {"default": 10.0, "env": "SIMMER_DAILY_BUDGET", "type": float,
                     "help": "Max spend per UTC day"},
    "starting_balance": {"default": 1000.0, "env": "SIMMER_STARTING_BALANCE", "type": float,
                         "help": "Paper portfolio starting balance"},
}

TRADE_SOURCE = "sdk:polymarket-simmer-fastloop"
SKILL_SLUG = "polymarket-simmer-fastloop"
_automaton_reported = False

# Asset mappings
ASSET_SYMBOLS = {"BTC": "BTCUSDT", "ETH": "ETHUSDT", "SOL": "SOLUSDT"}
ASSET_PATTERNS = {"BTC": ["bitcoin up or down"], "ETH": ["ethereum up or down"], "SOL": ["solana up or down"]}
BINANCE_FUTURES_SYMBOLS = {"BTC": "BTCUSDT", "ETH": "ETHUSDT", "SOL": "SOLUSDT"}

_window_seconds = {"5m": 300, "15m": 900}
MAX_SPREAD_PCT = 0.10
MIN_SHARES_PER_ORDER = 5
SMART_SIZING_PCT = 0.05

from simmer_sdk.skill import load_config, update_config, get_config_path

cfg = load_config(CONFIG_SCHEMA, __file__, slug="polymarket-simmer-fastloop")

# Config values
ENTRY_THRESHOLD = cfg["entry_threshold"]
MIN_MOMENTUM_PCT = cfg["min_momentum_pct"]
MAX_POSITION_USD = cfg["max_position"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max:
    MAX_POSITION_USD = min(MAX_POSITION_USD, float(_automaton_max))
SIGNAL_SOURCE = cfg["signal_source"]
LOOKBACK_MINUTES = cfg["lookback_minutes"]
ASSET = cfg["asset"].upper()
WINDOW = cfg["window"]
MIN_TIME_REMAINING = cfg["min_time_remaining"]
TARGET_TIME_MIN = cfg["target_time_min"]
TARGET_TIME_MAX = cfg["target_time_max"]
VOLUME_CONFIDENCE = cfg["volume_confidence"]
REQUIRE_ORDERBOOK = cfg["require_orderbook"]
TIME_FILTER = cfg["time_filter"]
VOL_SIZING = cfg["vol_sizing"]
FEE_BUFFER = cfg["fee_buffer"]
DAILY_BUDGET = cfg["daily_budget"]
STARTING_BALANCE = cfg["starting_balance"]

# Ledger file for win rate tracking
LEDGER_FILE = Path(__file__).parent / "fastloop_ledger.json"

# =============================================================================
# Daily Budget & Ledger Tracking
# =============================================================================

def _get_spend_path():
    return Path(__file__).parent / "daily_spend.json"

def _load_daily_spend():
    spend_path = _get_spend_path()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if spend_path.exists():
        try:
            with open(spend_path) as f:
                data = json.load(f)
            if data.get("date") == today:
                return data
        except (json.JSONDecodeError, IOError):
            pass
    return {"date": today, "spent": 0.0, "trades": 0}

def _save_daily_spend(spend_data):
    with open(_get_spend_path(), "w") as f:
        json.dump(spend_data, f, indent=2)

def _load_ledger():
    if LEDGER_FILE.exists():
        try:
            with open(LEDGER_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"trades": [], "stats": {"total": 0, "wins": 0, "losses": 0, "pnl": 0.0}}

def _save_ledger(ledger):
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

def _log_trade_to_ledger(trade_id, market_id, side, entry_price, amount, reason, momentum_pct, resolved=False, outcome=None, pnl=None):
    ledger = _load_ledger()
    trade = {
        "trade_id": trade_id,
        "market_id": market_id,
        "side": side,
        "entry_price": entry_price,
        "amount": amount,
        "reason": reason,
        "momentum_pct": momentum_pct,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": resolved,
        "outcome": outcome,
        "pnl": pnl,
    }
    ledger["trades"].append(trade)
    if resolved and pnl is not None:
        ledger["stats"]["total"] += 1
        ledger["stats"]["pnl"] += pnl
        if pnl > 0:
            ledger["stats"]["wins"] += 1
        else:
            ledger["stats"]["losses"] += 1
    _save_ledger(ledger)

# =============================================================================
# API Helpers
# =============================================================================

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
        venue = os.environ.get("TRADING_VENUE", "simmer")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client

def _api_request(url, method="GET", data=None, headers=None, timeout=15):
    try:
        req_headers = headers or {}
        if "User-Agent" not in req_headers:
            req_headers["User-Agent"] = "polymarket-simmer-fastloop/1.0"
        body = json.dumps(data).encode("utf-8") if data else None
        if body:
            req_headers["Content-Type"] = "application/json"
        req = Request(url, data=body, headers=req_headers, method=method)
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        try:
            error_body = json.loads(e.read().decode("utf-8"))
            return {"error": error_body.get("detail", str(e)), "status_code": e.code}
        except Exception:
            return {"error": str(e), "status_code": e.code}
    except URLError as e:
        return {"error": f"Connection error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

CLOB_API = "https://clob.polymarket.com"

def fetch_live_midpoint(token_id):
    result = _api_request(f"{CLOB_API}/midpoint?token_id={quote(str(token_id))}", timeout=5)
    if not result or not isinstance(result, dict) or result.get("error"):
        return None
    try:
        return float(result["mid"])
    except (KeyError, ValueError, TypeError):
        return None

def fetch_live_prices(clob_token_ids):
    if not clob_token_ids or len(clob_token_ids) < 1:
        return None
    return fetch_live_midpoint(clob_token_ids[0])

def fetch_orderbook_summary(clob_token_ids):
    if not clob_token_ids or len(clob_token_ids) < 1:
        return None
    yes_token = clob_token_ids[0]
    result = _api_request(f"{CLOB_API}/book?token_id={quote(str(yes_token))}", timeout=5)
    if not result or not isinstance(result, dict):
        return None
    bids = result.get("bids", [])
    asks = result.get("asks", [])
    if not bids or not asks:
        return None
    try:
        best_bid = float(bids[0]["price"])
        best_ask = float(asks[0]["price"])
        spread = best_ask - best_bid
        mid = (best_ask + best_bid) / 2
        spread_pct = spread / mid if mid > 0 else 0
        bid_depth = sum(float(b.get("size", 0)) * float(b.get("price", 0)) for b in bids[:5])
        ask_depth = sum(float(a.get("size", 0)) * float(a.get("price", 0)) for a in asks[:5])
        # Order book imbalance
        total_depth = bid_depth + ask_depth
        imbalance = (bid_depth - ask_depth) / total_depth if total_depth > 0 else 0
        return {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread_pct": spread_pct,
            "bid_depth_usd": bid_depth,
            "ask_depth_usd": ask_depth,
            "imbalance": imbalance,
        }
    except (KeyError, ValueError, IndexError, TypeError):
        return None

def fetch_binance_orderbook(asset="BTC", limit=20):
    """Fetch Binance spot order book and calculate imbalance.
    
    Args:
        asset: Asset symbol (BTC, ETH, SOL)
        limit: Number of levels to fetch (default 20)
    
    Returns:
        dict with bid_depth, ask_depth, imbalance, or None on error
    """
    symbol = ASSET_SYMBOLS.get(asset, "BTCUSDT")
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
    result = _api_request(url, timeout=5)
    if not result or isinstance(result, dict) and result.get("error"):
        return None
    try:
        # Binance depth format: {"bids": [[price, qty], ...], "asks": [[price, qty], ...]}
        bids = result.get("bids", [])
        asks = result.get("asks", [])
        if not bids or not asks:
            return None
        
        # Calculate depth in quote currency (USDT)
        bid_depth = sum(float(b[0]) * float(b[1]) for b in bids)  # price * qty
        ask_depth = sum(float(a[0]) * float(a[1]) for a in asks)
        
        total_depth = bid_depth + ask_depth
        imbalance = (bid_depth - ask_depth) / total_depth if total_depth > 0 else 0
        
        return {
            "bid_depth": bid_depth,
            "ask_depth": ask_depth,
            "imbalance": imbalance,
            "levels": limit,
        }
    except (KeyError, ValueError, IndexError, TypeError) as e:
        return None

# =============================================================================
# Market Discovery (V8.10 Pre-Caching Engine)
# =============================================================================

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'fast_markets_cache.json')

def _parse_cache_dt(dt_str):
    """Parse ISO datetime string, returning UTC-aware datetime or None."""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(str(dt_str).replace('Z', '+00:00'))
    except Exception:
        return None

def _update_market_cache(new_markets):
    """[V8.10] Save future markets to local JSON cache to survive API blackout at market open."""
    now = datetime.now(timezone.utc)
    cache = []
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                saved = json.load(f)
                cache = [m for m in saved if _parse_cache_dt(m.get('end_time')) and _parse_cache_dt(m.get('end_time')) > now]
        except Exception:
            pass

    cache_dict = {m.get('id') or m.get('market_id'): m for m in cache if m.get('id') or m.get('market_id')}
    for m in new_markets:
        key = m.get('market_id') or m.get('id')
        end_time = m.get('end_time')
        if key and end_time and end_time > now:
            m_copy = m.copy()
            m_copy['end_time'] = end_time.isoformat() if hasattr(end_time, 'isoformat') else str(end_time)
            m_copy['market_id'] = key
            cache_dict[key] = m_copy

    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(list(cache_dict.values()), f)
        if new_markets:
            print(f"  [Ignition] Successfully cached {len(new_markets)} future market IDs.")
    except Exception:
        pass

def _get_cached_markets():
    """[V8.10] Load alive cached markets. Used to rescue hidden markets after API goes dark."""
    now = datetime.now(timezone.utc)
    if not os.path.exists(CACHE_FILE):
        return []
    try:
        with open(CACHE_FILE, 'r') as f:
            saved = json.load(f)
        parsed = []
        for m in saved:
            dt = _parse_cache_dt(m.get('end_time'))
            if dt and dt > now:
                m['end_time'] = dt
                m['id'] = m.get('market_id') or m.get('id')
                m['source'] = 'cache'
                m.setdefault('is_live_now', None)
                parsed.append(m)
        return parsed
    except Exception:
        return []

def discover_fast_markets(asset="BTC", window="5m"):
    """Find active fast markets. Uses Simmer SDK first, then Pre-Cache, then Gamma fallback."""
    simmer_markets = []
    try:
        client = get_client()
        sdk_markets = client.get_fast_markets(asset=asset, window=window, limit=50)
        if sdk_markets:
            for m in sdk_markets:
                end_time = None
                if m.resolves_at:
                    try:
                        iso_str = m.resolves_at.replace(" ", "T").replace("Z", "+00:00")
                        end_time = datetime.fromisoformat(iso_str)
                    except ValueError:
                        pass

                clob_tokens = [m.polymarket_token_id] if m.polymarket_token_id else []
                if m.polymarket_no_token_id:
                    clob_tokens.append(m.polymarket_no_token_id)
                simmer_markets.append({
                    "id": m.id,
                    "question": m.question,
                    "slug": "",
                    "condition_id": "",
                    "end_time": end_time,
                    "outcome_prices": f'[{m.current_probability or 0.5}, {1 - (m.current_probability or 0.5)}]',
                    "clob_token_ids": clob_tokens,
                    "is_live_now": m.is_live_now,
                    "spread_cents": m.spread_cents,
                    "liquidity_tier": m.liquidity_tier,
                    "external_price_yes": m.external_price_yes,
                    "fee_rate_bps": 0,
                    "source": "simmer",
                    "market_id": m.id,
                })
    except Exception as e:
        print(f"  [WARNING] Simmer fast-markets API failed ({e}), falling back to cache/Gamma")

    # [V8.10] Always update the cache with whatever Simmer found, then load cached ones
    _update_market_cache(simmer_markets)
    cached_markets = _get_cached_markets()

    # Fallback to Gamma if both Simmer and cache are empty
    gamma_markets = []
    if not simmer_markets and not cached_markets:
        gamma_markets = _discover_via_gamma(asset, window)

    # Merge, deduplicate by question title
    seen, merged = set(), []
    for m in simmer_markets + cached_markets + gamma_markets:
        q = m.get('question', '')
        if q and q not in seen:
            seen.add(q)
            merged.append(m)

    return merged

def _discover_via_gamma(asset="BTC", window="5m"):
    """Fallback: Find active fast markets on Polymarket via Gamma API."""
    asset_patterns = {
        "BTC": ["Bitcoin", "BTC"],
        "ETH": ["Ethereum", "ETH"],
        "SOL": ["Solana", "SOL"],
    }
    patterns = asset_patterns.get(asset, [asset])
    url = (
        "https://gamma-api.polymarket.com/markets"
        "?limit=100&closed=false&tag=crypto&order=endDate&ascending=true"
    )
    result = _api_request(url)
    if not result or isinstance(result, dict) and result.get("error"):
        return []

    markets = []
    for m in result:
        q = (m.get("question") or "").lower()
        slug = m.get("slug", "")
        matches_window = f"-{window}-" in slug
        if any(p.lower() in q for p in patterns) and matches_window:
            condition_id = m.get("conditionId", "")
            closed = m.get("closed", False)
            if not closed and slug:
                end_time = _parse_end_time(m.get("question", ""))
                clob_tokens_raw = m.get("clobTokenIds", "[]")
                if isinstance(clob_tokens_raw, str):
                    try:
                        import json
                        clob_tokens = json.loads(clob_tokens_raw)
                    except (json.JSONDecodeError, ValueError):
                        clob_tokens = []
                else:
                    clob_tokens = clob_tokens_raw or []
                markets.append({
                    "id": m.get("id", slug),
                    "question": m.get("question", ""),
                    "slug": slug,
                    "condition_id": condition_id,
                    "end_time": end_time,
                    "outcomes": m.get("outcomes", []),
                    "outcome_prices": str(m.get("outcomePrices", "[]")),
                    "clob_token_ids": clob_tokens,
                    "fee_rate_bps": int(m.get("fee_rate_bps") or m.get("feeRateBps") or 0),
                    "source": "gamma",
                })
    return markets

def _parse_end_time(question):
    import re
    pattern = r'(\w+ \d+),.*?-\s*(\d{1,2}:\d{2}(?:AM|PM))\s*ET'
    match = re.search(pattern, question)
    if not match:
        return None
    try:
        from zoneinfo import ZoneInfo
        date_str = match.group(1)
        time_str = match.group(2)
        year = datetime.now(timezone.utc).year
        dt_str = f"{date_str} {year} {time_str}"
        dt = datetime.strptime(dt_str, "%B %d %Y %I:%M%p")
        et = ZoneInfo("America/New_York")
        dt = dt.replace(tzinfo=et).astimezone(timezone.utc)
        return dt
    except Exception:
        return None

def find_best_market(markets):
    now = datetime.now(timezone.utc)
    candidates = []
    for m in markets:
        end_time = m.get("end_time")
        if not end_time:
            continue
        remaining = (end_time - now).total_seconds()
        # Filter by time window
        if remaining < MIN_TIME_REMAINING:
            continue
        if remaining < TARGET_TIME_MIN or remaining > TARGET_TIME_MAX:
            continue
        candidates.append((remaining, m))
    if not candidates:
        # Fallback: just check min_time, but strictly cap at 900s (15m) to avoid ghost markets
        for m in markets:
            end_time = m.get("end_time")
            if not end_time:
                continue
            remaining = (end_time - now).total_seconds()
            if MIN_TIME_REMAINING <= remaining <= 900:
                candidates.append((remaining, m))
    if not candidates:
        return None
    # Prefer markets in the sweet spot, then soonest expiring
    candidates.sort(key=lambda x: abs(x[0] - (TARGET_TIME_MIN + TARGET_TIME_MAX) / 2))
    return candidates[0][1]

# =============================================================================
# CEX Signals
# =============================================================================

def get_binance_momentum(symbol="BTCUSDT", lookback_minutes=5):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={lookback_minutes}"
    result = _api_request(url)
    if not result or isinstance(result, dict):
        return None
    try:
        candles = result
        if len(candles) < 2:
            return None
        price_then = float(candles[0][1])
        price_now = float(candles[-1][4])
        momentum_pct = ((price_now - price_then) / price_then) * 100
        direction = "up" if momentum_pct > 0 else "down"
        import time
        volumes = [float(c[5]) for c in candles]
        # historical average from fully closed candles
        avg_volume = sum(volumes[:-1]) / len(volumes[:-1]) if len(volumes) > 1 else volumes[0]
        latest_volume = volumes[-1]
        # time-proportional scaling for the current unclosed candle
        open_time_ms = int(candles[-1][0])
        elapsed_seconds = (time.time() * 1000 - open_time_ms) / 1000.0
        elapsed_seconds = max(1.0, min(elapsed_seconds, 60.0))  # Clamp 1s-60s
        projected_volume = latest_volume * (60.0 / elapsed_seconds)
        volume_ratio = projected_volume / avg_volume if avg_volume > 0 else 1.0
        # Calculate 24h volatility (using available candles as proxy)
        returns = []
        for i in range(1, len(candles)):
            ret = (float(candles[i][4]) - float(candles[i-1][4])) / float(candles[i-1][4])
            returns.append(ret)
        if len(returns) >= 2:
            mean_ret = sum(returns) / len(returns)
            variance = sum((r - mean_ret) ** 2 for r in returns) / len(returns)
            volatility_24h = math.sqrt(variance) * math.sqrt(24 * 60 / len(returns))
        else:
            volatility_24h = 0.02  # Default 2%
        return {
            "momentum_pct": momentum_pct,
            "direction": direction,
            "price_now": price_now,
            "price_then": price_then,
            "avg_volume": avg_volume,
            "latest_volume": latest_volume,
            "volume_ratio": volume_ratio,
            "candles": len(candles),
            "volatility_24h": volatility_24h,
        }
    except (IndexError, ValueError, KeyError):
        return None

def get_momentum(asset="BTC", source="binance", lookback=5):
    if source == "binance":
        symbol = ASSET_SYMBOLS.get(asset, "BTCUSDT")
        return get_binance_momentum(symbol, lookback)
    else:
        return None

# =============================================================================
# Import & Trade
# =============================================================================

def import_market(slug):
    url = f"https://polymarket.com/event/{slug}"
    try:
        result = get_client().import_market(url)
    except Exception as e:
        return None, str(e)
    if not result:
        return None, "No response"
    if result.get("error"):
        return None, result.get("error", "Unknown error")
    status = result.get("status")
    market_id = result.get("market_id")
    if status == "resolved":
        alternatives = result.get("active_alternatives", [])
        if alternatives:
            return None, f"Market resolved. Try: {alternatives[0].get('id')}"
        return None, "Market resolved"
    if status in ("imported", "already_exists"):
        return market_id, None
    return None, f"Unexpected status: {status}"

def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception as e:
        return {"error": str(e)}

def get_positions():
    try:
        positions = get_client().get_positions()
        from dataclasses import asdict
        return [asdict(p) for p in positions]
    except Exception:
        return []

def execute_trade(market_id, side, amount, reasoning=""):
    try:
        result = get_client().trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "shares": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_position_size(max_size, volatility_24h=None):
    if not VOL_SIZING or not volatility_24h:
        return max_size
    # Volatility-adjusted sizing: reduce size when volatility is high
    # Target: size = max_size * (0.02 / volatility_24h), capped at max_size
    adjusted = max_size * min(1.0, 0.02 / max(volatility_24h, 0.001))
    return max(adjusted, 0.5)  # Minimum $0.50

# =============================================================================
# Stats & Resolve
# =============================================================================

def show_stats():
    ledger = _load_ledger()
    stats = ledger["stats"]
    print("\nChart Polymarket Simmer FastLoop -- Calibration Stats")
    print("=" * 50)
    print(f"Total trades: {stats['total']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    if stats['total'] > 0:
        win_rate = stats['wins'] / stats['total'] * 100
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Total PnL: ${stats['pnl']:.2f}")
        avg_pnl = stats['pnl'] / stats['total']
        print(f"Avg PnL per trade: ${avg_pnl:.2f}")
        # Breakeven analysis
        breakeven_rate = 50 + (10 / 2)  # With 10% fee, need ~55% to breakeven
        print(f"\nBreakeven win rate (10% fee): ~55%")
        if win_rate >= 63:
            print(f"[OK] Your win rate ({win_rate:.1f}%) is profitable!")
        elif win_rate >= 55:
            print(f"[WARNING]  Your win rate ({win_rate:.1f}%) is near breakeven")
        else:
            print(f"[FAIL] Your win rate ({win_rate:.1f}%) needs improvement")
    else:
        print("No resolved trades yet. Run with --live, then --resolve after markets expire.")
    print()

def get_settled_positions():
    """Fetch settled positions from Simmer API with real outcomes."""
    try:
        client = get_client()
        # Call internal API to get settled positions
        data = client._request("GET", "/api/sdk/positions", params={"status": "settled"})
        settled = []
        for p in data.get("positions", []):
            settled.append({
                "market_id": p.get("market_id"),
                "question": p.get("question", ""),
                "status": p.get("status", "settled"),
                "outcome": p.get("outcome"),  # "yes" or "no"
                "pnl": p.get("pnl", 0),
                "cost_basis": p.get("cost_basis", 0),
                "sources": p.get("sources", []),
            })
        return settled
    except Exception as e:
        print(f"  [WARNING]  Failed to fetch settled positions: {e}")
        return []

def resolve_positions():
    """Resolve expired paper trades against real outcomes from Simmer API."""
    print("\nSEARCH Resolving expired positions...")
    ledger = _load_ledger()
    settled = get_settled_positions()
    resolved_count = 0
    
    for trade in ledger["trades"]:
        if trade.get("resolved"):
            continue
        
        trade_id = trade.get("trade_id")
        market_id = trade.get("market_id")
        our_side = trade.get("side")  # "yes" or "no"
        
        # Find matching settled position by market_id
        matched = None
        for pos in settled:
            if pos.get("market_id") == market_id:
                matched = pos
                break
        
        if matched:
            # Got real outcome from API
            outcome = matched.get("outcome")  # "yes" or "no"
            actual_pnl = matched.get("pnl", 0)
            
            trade["resolved"] = True
            trade["outcome"] = outcome
            trade["pnl"] = actual_pnl
            
            # Determine win/loss
            won = (our_side == outcome)
            if won:
                print(f"  [OK] Won: {trade_id[:16]}... | {our_side.upper()} | PnL: ${actual_pnl:+.2f}")
            else:
                print(f"  [FAIL] Lost: {trade_id[:16]}... | {our_side.upper()} vs outcome {outcome.upper()} | PnL: ${actual_pnl:+.2f}")
            resolved_count += 1
        else:
            # Fallback: if no settled data, assume loss (old behavior)
            trade["resolved"] = True
            trade["outcome"] = "unknown"
            trade["pnl"] = -trade.get("amount", 0)
            print(f"  [WARNING]  No API data for {trade_id[:16]}... (assumed loss)")
            resolved_count += 1
    
    if resolved_count > 0:
        # Update stats
        stats = ledger["stats"]
        for trade in ledger["trades"]:
            if trade.get("resolved") and trade.get("pnl") is not None:
                stats["total"] = stats.get("total", 0) + 1
                if trade.get("pnl", 0) > 0:
                    stats["wins"] = stats.get("wins", 0) + 1
                else:
                    stats["losses"] = stats.get("losses", 0) + 1
                stats["pnl"] = stats.get("pnl", 0) + trade.get("pnl", 0)
        
        _save_ledger(ledger)
        print(f"\n[OK] Resolved {resolved_count} trades")
        print(f"   Stats: {stats['total']} total, {stats['wins']} wins, {stats['losses']} losses")
        print(f"   Total PnL: ${stats['pnl']:+.2f}")
    else:
        print("  No positions to resolve")
    print()

# =============================================================================
# Main Strategy
# =============================================================================

def run_strategy(dry_run=True, positions_only=False, show_config=False, quiet=False):
    def log(msg, force=False):
        if not quiet or force:
            print(msg)

    log("Fast Polymarket Simmer FastLoop Trader")
    log("=" * 50)

    if dry_run:
        log("\n[PAPER MODE] Use --live for real trades")

    log(f"\nSETTINGS  Configuration:")
    log(f"  Asset:             {ASSET}")
    log(f"  Window:            {WINDOW}")
    log(f"  Entry threshold:   {ENTRY_THRESHOLD}")
    log(f"  Min momentum:      {MIN_MOMENTUM_PCT}%")
    log(f"  Max position:      ${MAX_POSITION_USD:.2f}")
    log(f"  Signal source:     {SIGNAL_SOURCE}")
    log(f"  Time filter:       {'ON' if TIME_FILTER else 'OFF'} (skip 02:00-06:00 UTC)")
    log(f"  Require orderbook: {'ON' if REQUIRE_ORDERBOOK else 'OFF'}")
    log(f"  Vol sizing:        {'ON' if VOL_SIZING else 'OFF'}")
    log(f"  Fee buffer:        {FEE_BUFFER:.0%}")

    daily_spend = _load_daily_spend()
    log(f"  Daily budget:      ${DAILY_BUDGET:.2f} (${daily_spend['spent']:.2f} spent)")

    if show_config:
        config_path = get_config_path(__file__)
        log(f"\n  Config: {config_path}")
        return

    get_client(live=not dry_run)

    if positions_only:
        log("\nChart Positions:")
        positions = get_positions()
        fast_positions = [p for p in positions if "up or down" in (p.get("question", "") or "").lower()]
        if not fast_positions:
            log("  No open fast market positions")
        else:
            for pos in fast_positions:
                log(f"  * {pos.get('question', 'Unknown')[:60]}")
                log(f"    YES: {pos.get('shares_yes', 0):.1f} | NO: {pos.get('shares_no', 0):.1f} | P&L: ${pos.get('pnl', 0):.2f}")
        return

    # Time filter check
    if TIME_FILTER:
        now_utc = datetime.now(timezone.utc)
        hour_utc = now_utc.hour
        if 2 <= hour_utc < 6:
            log(f"\nPause\ufe0f  Time filter: low liquidity window (02:00-06:00 UTC)")
            if not quiet:
                print(f"Chart Summary: No trade (time filter)")
            return

    # Discover markets
    log(f"\nSEARCH Discovering {ASSET} fast markets...")
    markets = discover_fast_markets(ASSET, WINDOW)
    log(f"  Found {len(markets)} active markets")

    if not markets:
        log("  No active markets found")
        if not quiet:
            print("Chart Summary: No markets available")
        return

    # Find best market
    best = find_best_market(markets)
    if not best:
        now = datetime.now(timezone.utc)
        for m in markets:
            end_time = m.get("end_time")
            if end_time:
                secs_left = (end_time - now).total_seconds()
                log(f"  Skipped: {m['question'][:50]}... ({secs_left:.0f}s left)")
        log(f"  No tradeable markets in time window ({TARGET_TIME_MIN}-{TARGET_TIME_MAX}s)")
        if not quiet:
            print(f"Chart Summary: No tradeable markets")
        return

    end_time = best.get("end_time")
    remaining = (end_time - datetime.now(timezone.utc)).total_seconds() if end_time else 0
    log(f"\nTARGET Selected: {best['question']}")
    log(f"  Expires in: {remaining:.0f}s")

    # Fetch live price
    clob_tokens = best.get("clob_token_ids", [])
    live_price = fetch_live_prices(clob_tokens) if clob_tokens else None
    if live_price is not None:
        market_yes_price = live_price
        log(f"  Current YES price: ${market_yes_price:.3f} (live CLOB)")
    else:
        try:
            prices = json.loads(best.get("outcome_prices", "[]"))
            market_yes_price = float(prices[0]) if prices else 0.5
        except (json.JSONDecodeError, IndexError, ValueError):
            market_yes_price = 0.5
        log(f"  Current YES price: ${market_yes_price:.3f} (Gamma WARNING)")

    # Fee info
    fee_rate_bps = best.get("fee_rate_bps", 0)
    fee_rate = fee_rate_bps / 10000
    if fee_rate > 0:
        log(f"  Fee rate: {fee_rate:.0%}")

    # Order book check (Binance, not CLOB)
    binance_book = fetch_binance_orderbook(ASSET, limit=20) if REQUIRE_ORDERBOOK else None
    skip_reasons = []

    if binance_book:
        log(f"  Binance OB Imbalance: {binance_book['imbalance']:+.3f} (bid: ${binance_book['bid_depth']:.0f} / ask: ${binance_book['ask_depth']:.0f})")
        # Order book confirmation
        if REQUIRE_ORDERBOOK:
            if binance_book["imbalance"] > 0.1:
                log(f"  OK Order book confirms bullish (bid dominance)")
            elif binance_book["imbalance"] < -0.1:
                log(f"  OK Order book confirms bearish (ask dominance)")
            else:
                log(f"  Pause Order book neutral (imbalance {binance_book['imbalance']:+.3f}) — skip")
                skip_reasons.append("orderbook neutral")
                if not quiet:
                    print(f"Chart Summary: No trade (orderbook neutral)")
                _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
                return

    # Get momentum
    log(f"\nFetching {ASSET} signal...")
    momentum = get_momentum(ASSET, SIGNAL_SOURCE, LOOKBACK_MINUTES)
    if not momentum:
        log("  [FAIL] Failed to fetch price data", force=True)
        return

    log(f"  Price: ${momentum['price_now']:,.2f}")
    log(f"  Momentum: {momentum['momentum_pct']:+.3f}%")
    log(f"  Direction: {momentum['direction']}")
    if VOLUME_CONFIDENCE:
        log(f"  Volume ratio: {momentum['volume_ratio']:.2f}x")
    if VOL_SIZING:
        log(f"  24h volatility: {momentum.get('volatility_24h', 0):.1%}")

    # Check minimum momentum
    momentum_pct = abs(momentum["momentum_pct"])
    if momentum_pct < MIN_MOMENTUM_PCT:
        log(f"  Pause Momentum {momentum_pct:.3f}% < {MIN_MOMENTUM_PCT}%")
        if not quiet:
            print(f"Chart Summary: No trade (weak momentum)")
        skip_reasons.append("weak momentum")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return

    # Volume confidence
    if VOLUME_CONFIDENCE and momentum["volume_ratio"] < 1.0:
        log(f"  Pause Low volume ({momentum['volume_ratio']:.2f}x < 1.0x)")
        skip_reasons.append("low volume")
        if not quiet:
            print(f"Chart Summary: No trade (low volume)")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return

    # Decision logic (mean reversion)
    direction = momentum["direction"]
    if direction == "up":
        side = "no"
        trade_rationale = f"{ASSET} up {momentum['momentum_pct']:+.3f}% (Mean Reversion -> DOWN)"
    else:
        side = "yes"
        trade_rationale = f"{ASSET} down {momentum['momentum_pct']:+.3f}% (Mean Reversion -> UP)"

    # NOFX Macro Check
    try:
        nofx_url = "https://nofxos.ai/api/netflow/top-ranking?auth=cm_568c67eae410d912c54c&type=institution&duration=1h"
        nofx_24_url = "https://nofxos.ai/api/netflow/top-ranking?auth=cm_568c67eae410d912c54c&type=institution&duration=24h"
        res1 = _api_request(nofx_url, timeout=5)
        res24 = _api_request(nofx_24_url, timeout=5)
        if res1 and res24:
            flow_1h = next((i['amount'] for i in res1.get('data',{}).get('netflows',[]) if i['symbol']=='BTCUSDT'), 0)
            flow_24h = next((i['amount'] for i in res24.get('data',{}).get('netflows',[]) if i['symbol']=='BTCUSDT'), 0)
            avg_1h = flow_24h / 24.0
            ratio = flow_1h / abs(avg_1h) if avg_1h != 0 else 0
            log(f"  NOFX 1h Netflow: ${flow_1h:,.0f} (Ratio: {ratio:+.1f}x)")
            if ratio > 2.0 and side == "no":
                log(f"  Pause NOFX Bull Elephant ({ratio:+.1f}x) — Block DOWN")
                return
            elif ratio < -2.0 and side == "yes":
                log(f"  Pause NOFX Bear Elephant ({ratio:+.1f}x) — Block UP")
                return
    except Exception as e:
        log(f"  WARNING NOFX Error: {e}")

    # Calculate divergence
    if side == "yes":
        divergence = 0.50 + ENTRY_THRESHOLD - market_yes_price
    else:
        divergence = market_yes_price - (0.50 - ENTRY_THRESHOLD)

    if divergence <= 0:
        log(f"  Pause Market priced in (divergence {divergence:.3f})")
        skip_reasons.append("market priced in")
        if not quiet:
            print(f"Chart Summary: No trade (market priced in)")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return

    # Fee-aware EV check
    if fee_rate > 0:
        buy_price = market_yes_price if side == "yes" else (1 - market_yes_price)
        fee_cost = (1 - buy_price) * fee_rate
        min_divergence = fee_cost + FEE_BUFFER
        log(f"  Fee cost: ${fee_cost:.3f} (min div: {min_divergence:.3f})")
        if divergence < min_divergence:
            log(f"  Pause Divergence {divergence:.3f} < {min_divergence:.3f}")
            skip_reasons.append("fees eat edge")
            if not quiet:
                print(f"Chart Summary: No trade (fees)")
            _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
            return

    # Position sizing
    position_size = calculate_position_size(MAX_POSITION_USD, momentum.get("volatility_24h"))
    price = market_yes_price if side == "yes" else (1 - market_yes_price)

    # Budget check
    remaining_budget = DAILY_BUDGET - daily_spend["spent"]
    if remaining_budget <= 0:
        log(f"  Pause Budget exhausted")
        skip_reasons.append("budget exhausted")
        if not quiet:
            print(f"Chart Summary: No trade (budget)")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return
    if position_size > remaining_budget:
        position_size = remaining_budget
        log(f"  Budget cap: ${position_size:.2f}")
    if position_size < 0.50:
        log(f"  Pause Position too small")
        skip_reasons.append("position too small")
        if not quiet:
            print(f"Chart Summary: No trade (size)")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return

    # Minimum order check
    min_cost = MIN_SHARES_PER_ORDER * price
    if min_cost > position_size:
        log(f"  WARNING Position ${position_size:.2f} < min {MIN_SHARES_PER_ORDER} shares")
        skip_reasons.append("below min order")
        if not quiet:
            print(f"Chart Summary: No trade (min order)")
        _emit_automaton(0, 0, 0, ", ".join(skip_reasons))
        return

    # Signal confirmed!
    log(f"\n  [OK] Signal: {side.upper()} — {trade_rationale}", force=True)
    log(f"  Divergence: {divergence:.3f}", force=True)
    log(f"  Position: ${position_size:.2f}", force=True)

    # Simmer market ID is already available from API
    market_id = best.get("id")
    if not market_id:
        log(f"  [FAIL] No Simmer market ID found", force=True)
        return
    log(f"\n[OK] Market ID: {market_id[:16]}...", force=True)

    tag = "SIMULATED" if dry_run else "LIVE"
    log(f"  Executing {side.upper()} ${position_size:.2f} ({tag})...", force=True)
    result = execute_trade(market_id, side, position_size, reasoning=trade_rationale)

    execution_error = None
    if result and result.get("success"):
        shares = result.get("shares_bought") or result.get("shares") or 0
        trade_id = result.get("trade_id")
        simulated = result.get("simulated")
        log(f"  {'[OK] [PAPER] ' if simulated else '[OK] '}Bought {shares:.1f} {side.upper()} @ ${price:.3f}", force=True)

        if not simulated:
            daily_spend["spent"] += position_size
            daily_spend["trades"] += 1
            _save_daily_spend(daily_spend)
            # Log to ledger
            _log_trade_to_ledger(
                trade_id=trade_id,
                market_id=market_id,
                side=side,
                entry_price=price,
                amount=position_size,
                reason=trade_rationale,
                momentum_pct=momentum["momentum_pct"],
            )

        if JOURNAL_AVAILABLE and trade_id and not simulated:
            confidence = min(0.9, 0.5 + divergence + (momentum_pct / 100))
            log_trade(
                trade_id=trade_id,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                thesis=trade_rationale,
                confidence=round(confidence, 2),
                asset=ASSET,
                momentum_pct=round(momentum["momentum_pct"], 3),
                volume_ratio=round(momentum["volume_ratio"], 2),
                signal_source=SIGNAL_SOURCE,
            )
    else:
        error = result.get("error", "Unknown") if result else "No response"
        log(f"  [FAIL] Trade failed: {error}", force=True)
        execution_error = error[:120]

    # Summary
    total_trades = 1 if result and result.get("success") else 0
    if not quiet or total_trades > 0:
        print(f"\nChart Summary:")
        print(f"  Market: {best['question'][:50]}")
        print(f"  Signal: {direction} {momentum_pct:.3f}%")
        print(f"  Action: {'PAPER' if dry_run else ('TRADED' if total_trades else 'FAILED')}")

    _emit_automaton(1, 1, total_trades, None, execution_error, position_size if total_trades else 0)

def _emit_automaton(signals, attempted, executed, skip_reason=None, error=None, amount=0):
    global _automaton_reported
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        report = {
            "signals": signals,
            "trades_attempted": attempted,
            "trades_executed": executed,
            "amount_usd": round(amount, 2),
        }
        if skip_reason:
            report["skip_reason"] = skip_reason
        if error:
            report["execution_errors"] = [error]
        print(json.dumps({"automaton": report}))
        _automaton_reported = True

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket Simmer FastLoop Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--dry-run", action="store_true", help="Paper mode (default)")
    parser.add_argument("--positions", action="store_true", help="Show positions")
    parser.add_argument("--stats", action="store_true", help="Show calibration stats")
    parser.add_argument("--resolve", action="store_true", help="Resolve expired trades")
    parser.add_argument("--config", action="store_true", help="Show config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE", help="Update config")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" not in item:
                print(f"Invalid --set format: {item}")
                sys.exit(1)
            key, val = item.split("=", 1)
            if key in CONFIG_SCHEMA:
                type_fn = CONFIG_SCHEMA[key].get("type", str)
                try:
                    if type_fn == bool:
                        updates[key] = val.lower() in ("true", "1", "yes")
                    else:
                        updates[key] = type_fn(val)
                except ValueError:
                    print(f"Invalid value for {key}: {val}")
                    sys.exit(1)
            else:
                print(f"Unknown key: {key}")
                sys.exit(1)
        result = update_config(updates, __file__)
        print(f"[OK] Config updated: {json.dumps(updates)}")
        sys.exit(0)

    if args.stats:
        show_stats()
        sys.exit(0)

    if args.resolve:
        resolve_positions()
        sys.exit(0)

    dry_run = not args.live
    run_strategy(dry_run=dry_run, positions_only=args.positions, show_config=args.config, quiet=args.quiet)

    # Fallback automaton report
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))

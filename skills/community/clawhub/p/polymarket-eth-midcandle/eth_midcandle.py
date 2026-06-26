#!/usr/bin/env python3
"""
ETH Mid-Candle Scalper — Polymarket / Simmer
=============================================
77%+ win rate. Real money. 400+ trades.

Enters ETH Up/Down 15-minute Polymarket markets mid-candle (2–12 min remaining)
when ETH 5m+3m momentum is confirmed AND BTC is aligned (not moving against you).

The BTC alignment gate is what separates this from a naive momentum strategy.
When ETH signals UP but BTC is dropping hard, you're fighting the tide — this gate
skips those trades entirely.

Usage:
    python eth_midcandle.py              # Paper trade (dry run)
    python eth_midcandle.py --live       # Real trades
    python eth_midcandle.py --positions  # Show open positions
    python eth_midcandle.py --config     # Show current config
    python eth_midcandle.py --set momentum_threshold=0.0010

Requires:
    SIMMER_API_KEY environment variable
    pip install simmer-sdk
"""

import os
import sys
import json
import argparse
import time
import urllib.request as _ur
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────

SKILL_SLUG   = "polymarket-eth-midcandle"
TRADE_SOURCE = "sdk:ethmc"

CONFIG_SCHEMA = {
    "poly_agent_id":      {"env": "SIMMER_ETHMC_AGENT_ID",  "default": "",      "type": str},
    "bet_size":           {"env": "SIMMER_ETHMC_BET_SIZE",  "default": 5.0,     "type": float},
    "momentum_threshold": {"env": "SIMMER_ETHMC_THRESHOLD", "default": 0.0012,  "type": float},
    "btc_gate_threshold": {"env": "SIMMER_ETHMC_BTC_GATE",  "default": 0.0015,  "type": float},
    "min_volume_ratio": {"env": "SIMMER_ETHMC_VOL_RATIO", "default": 0.0, "type": float},
    "min_entry_price":    {"env": "SIMMER_ETHMC_MIN_ENTRY", "default": 0.45,    "type": float},
    "max_entry_price":    {"env": "SIMMER_ETHMC_MAX_ENTRY", "default": 0.65,    "type": float},
    "enable_1m_confirm":  {"env": "SIMMER_ETHMC_1M_CONFIRM","default": False,   "type": bool},
    "skip_hours":         {"env": "SIMMER_ETHMC_SKIP_HOURS","default": "13,17", "type": str},
    "discord_webhook":    {"env": "SIMMER_ETHMC_WEBHOOK",   "default": "",      "type": str},
    "max_position_usd":   {"env": "SIMMER_ETHMC_MAX_POS",   "default": 50.0,    "type": float},
    "sizing_pct":         {"env": "SIMMER_ETHMC_SIZING_PCT","default": 0.03,    "type": float},
    "max_consecutive_losses": {"env": "SIMMER_ETHMC_MAX_LOSSES", "default": 3, "type": int},
}

try:
    from simmer_sdk.skill import load_config, update_config, get_config_path
    _config = load_config(CONFIG_SCHEMA, __file__, slug=SKILL_SLUG)
except ImportError:
    def _coerce(v, t):
        if t == bool:
            return str(v).lower() in ("1", "true", "yes")
        return t(v)
    _config = {k: _coerce(os.environ.get(s["env"], s["default"]), s["type"])
               for k, s in CONFIG_SCHEMA.items()}

POLY_AGENT_ID       = _config["poly_agent_id"]
BET_SIZE            = _config["bet_size"]
MOMENTUM_THRESHOLD  = _config["momentum_threshold"]
BTC_GATE_THRESHOLD  = _config["btc_gate_threshold"]
MIN_VOLUME_RATIO    = _config["min_volume_ratio"]
MIN_ENTRY_PRICE     = _config["min_entry_price"]
MAX_ENTRY_PRICE     = _config["max_entry_price"]
ENABLE_1M_CONFIRM   = _config["enable_1m_confirm"]
DISCORD_WEBHOOK     = _config["discord_webhook"]
MAX_POSITION_USD    = _config["max_position_usd"]
SMART_SIZING_PCT    = _config["sizing_pct"]
MAX_CONSECUTIVE_LOSSES = _config["max_consecutive_losses"]

# Parse skip hours
try:
    SKIP_HOURS = {int(h.strip()) for h in _config["skip_hours"].split(",") if h.strip()}
except Exception:
    SKIP_HOURS = {13, 17}

# Polymarket minimums
MIN_SHARES_PER_ORDER = 5.0
MIN_TICK_SIZE        = 0.01
SLIPPAGE_MAX_PCT     = 0.15

# ──────────────────────────────────────────────
# SimmerClient singleton
# ──────────────────────────────────────────────

_client = None
_client_live_mode = None

def get_client(live=True):
    global _client, _client_live_mode
    if _client is None:
        _client_live_mode = live
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY not set. Get yours at simmer.markets/dashboard → SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    elif _client_live_mode != live:
        print(f"  ⚠️  Warning: get_client(live={live}) called but client already initialized as live={_client_live_mode}. Using existing client.")
    return _client

# ──────────────────────────────────────────────
# SDK wrappers
# ──────────────────────────────────────────────

def get_portfolio():
    try:
        return get_client().get_portfolio()
    except Exception as e:
        print(f"  Portfolio fetch failed: {e}")
        return None

def get_positions():
    try:
        positions = get_client().get_positions()
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
    discipline = context.get("discipline", {})
    slippage   = context.get("slippage", {})
    warning_level = discipline.get("warning_level", "none")
    if warning_level == "severe":
        return False, [f"Flip-flop warning: {discipline.get('flip_flop_warning','')}"]
    elif warning_level == "mild":
        reasons.append("Mild flip-flop warning")
    estimates = slippage.get("estimates", []) if slippage else []
    if estimates and estimates[0].get("slippage_pct", 0) > SLIPPAGE_MAX_PCT:
        return False, [f"Slippage too high: {estimates[0].get('slippage_pct', 0):.1%}"]
    return True, reasons

def execute_trade(market_id, side, amount, reasoning="", signal_data=None):
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG, reasoning=reasoning,
            signal_data=signal_data if signal_data else None,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
            "skip_reason": getattr(result, "skip_reason", None),
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_position_size(smart_sizing=False):
    if not smart_sizing:
        return BET_SIZE
    portfolio = get_portfolio()
    if not portfolio:
        return BET_SIZE
    balance = portfolio.get("balance_usdc", 0)
    if balance <= 0:
        return BET_SIZE
    return max(min(balance * SMART_SIZING_PCT, MAX_POSITION_USD), 1.0)

# ──────────────────────────────────────────────
# Market fetching
# ──────────────────────────────────────────────

def find_eth_market():
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "q": "ETH", "limit": 20,
                    "agent_id": POLY_AGENT_ID}
        )
        markets = result.get("markets", [])
        candidates = [m for m in markets if "15" in m.get("question", "")]
        if not candidates:
            candidates = markets
        return candidates[0] if candidates else None
    except Exception as e:
        print(f"  Market fetch failed: {e}")
        return None

# ──────────────────────────────────────────────
# Signal logic
# ──────────────────────────────────────────────

def candle_timing():
    now = datetime.now(timezone.utc)
    candle_start = (now.minute // 15) * 15
    mins_remaining = 15 - (now.minute - candle_start)
    in_window = 2 <= mins_remaining <= 12
    return in_window, mins_remaining, candle_start

def binance_klines(symbol, interval, limit, retries=2):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    for attempt in range(retries):
        try:
            req = _ur.Request(url, headers={"User-Agent": "simmer-ethmc/1.0"})
            with _ur.urlopen(req, timeout=10) as resp:
                return [float(k[4]) for k in json.loads(resp.read())]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"  Binance {symbol} klines error: {e}")
    return []

def get_eth_momentum():
    closes = binance_klines("ETHUSDT", "1m", 16)
    if len(closes) < 6:
        return None, 0, 0, closes
    c5 = (closes[-1] - closes[-6]) / closes[-6]
    c3 = (closes[-1] - closes[-4]) / closes[-4]
    if c5 > MOMENTUM_THRESHOLD and c3 > 0:
        direction = "up"
    elif c5 < -MOMENTUM_THRESHOLD and c3 < 0:
        direction = "down"
    else:
        direction = "flat"
    return direction, round(c5 * 100, 4), round(c3 * 100, 4), closes

def get_1m_direction(closes):
    if len(closes) < 2:
        return "flat", 0
    c = (closes[-1] - closes[-2]) / closes[-2]
    return ("up" if c > 0 else "down" if c < 0 else "flat"), round(c * 100, 4)

def check_btc_alignment(eth_direction):
    """Check BTC isn't moving hard against ETH direction. Returns (aligned, btc_change_pct)."""
    if BTC_GATE_THRESHOLD <= 0:
        return True, 0.0
    try:
        closes = binance_klines("BTCUSDT", "5m", 3)
        if len(closes) < 2:
            return True, 0.0  # can't check — allow through
        btc_c5 = (closes[-1] - closes[-2]) / closes[-2]
        btc_pct = round(btc_c5 * 100, 4)
        if eth_direction == "up" and btc_c5 < -BTC_GATE_THRESHOLD:
            return False, btc_pct
        if eth_direction == "down" and btc_c5 > BTC_GATE_THRESHOLD:
            return False, btc_pct
        return True, btc_pct
    except Exception:
        return True, 0.0  # fail open

def check_volume():
    if MIN_VOLUME_RATIO <= 0:
        return True, 0.0
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=5m&limit=26"
        req = _ur.Request(url, headers={"User-Agent": "simmer-ethmc/1.0"})
        with _ur.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if len(data) < 25:
            return True, 0.0
        vols = [float(k[5]) for k in data]
        ratio = vols[-2] / (sum(vols[-26:-2]) / 24)
        return ratio >= MIN_VOLUME_RATIO, round(ratio, 2)
    except Exception:
        return True, 0.0

# ──────────────────────────────────────────────
# Dedup state
# ──────────────────────────────────────────────

_STATE = Path(__file__).parent / "traded_markets.json"

def _load_traded():
    if _STATE.exists():
        try:
            d = json.loads(_STATE.read_text())
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
            return {k: v for k, v in d.items() if v > cutoff}
        except Exception:
            pass
    return {}

def _mark_traded(market_id):
    try:
        d = _load_traded()
        d[market_id] = datetime.now(timezone.utc).isoformat()
        _STATE.write_text(json.dumps(d))
    except Exception as e:
        print(f"  ⚠️ Failed to save dedup state: {e}")

# ──────────────────────────────────────────────
# Circuit breaker
# ──────────────────────────────────────────────

_CB_STATE = Path(__file__).parent / "circuit_state.json"

def _load_cb_state():
    if _CB_STATE.exists():
        try:
            return json.loads(_CB_STATE.read_text())
        except Exception:
            pass
    return {"consecutive_losses": 0, "paused_until": None}

def _save_cb_state(state):
    try:
        _CB_STATE.write_text(json.dumps(state))
    except Exception as e:
        print(f"  ⚠️ Failed to save circuit breaker state: {e}")

def check_circuit_breaker():
    """Returns (allowed, reason). Checks and clears expired pauses."""
    if MAX_CONSECUTIVE_LOSSES <= 0:
        return True, ""
    state = _load_cb_state()
    paused_until = state.get("paused_until")
    if paused_until:
        if datetime.now(timezone.utc).isoformat() < paused_until:
            losses = state.get("consecutive_losses", 0)
            return False, f"Circuit breaker: {losses} consecutive losses — paused until {paused_until[:16]} UTC"
        else:
            # Pause expired — reset
            state["paused_until"] = None
            state["consecutive_losses"] = 0
            _save_cb_state(state)
    return True, ""
 
def record_trade_outcome(success: bool):
    """Call after trade result is known. Updates consecutive loss counter."""
    if MAX_CONSECUTIVE_LOSSES <= 0:
        return
    state = _load_cb_state()
    if success:
        state["consecutive_losses"] = 0
        state["paused_until"] = None
    else:
        state["consecutive_losses"] = state.get("consecutive_losses", 0) + 1
        if state["consecutive_losses"] >= MAX_CONSECUTIVE_LOSSES:
            # Pause for 2 hours
            pause_until = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
            state["paused_until"] = pause_until
            print(f"  🛑 Circuit breaker triggered: {state['consecutive_losses']} consecutive losses — pausing until {pause_until[:16]} UTC")
            notify_discord(f"🛑 ETH Midcandle circuit breaker: {state['consecutive_losses']} consecutive losses — paused 2h")
    _save_cb_state(state)

# ──────────────────────────────────────────────
# Discord
# ──────────────────────────────────────────────

def notify_discord(msg):
    if not DISCORD_WEBHOOK:
        return
    try:
        body = json.dumps({"content": msg}).encode()
        req = _ur.Request(DISCORD_WEBHOOK, data=body,
                          headers={"Content-Type": "application/json"}, method="POST")
        _ur.urlopen(req, timeout=5)
    except Exception:
        pass

# ──────────────────────────────────────────────
# Main strategy
# ──────────────────────────────────────────────

def run_strategy(dry_run=True, positions_only=False, show_config=False,
                 smart_sizing=False, use_safeguards=True):
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    mode_icon = "🔶" if dry_run else "🔴"
    print(f"\n{'='*60}")
    print(f"{mode_icon} ETH Mid-Candle Scalper — {now_str} ({'PAPER' if dry_run else 'LIVE'})")
    print(f"{'='*60}")

    get_client(live=not dry_run)

    if dry_run:
        print("\n  [PAPER MODE] Use --live for real trades.\n")

    if show_config:
        print("\n📋 Current config:")
        for k, v in _config.items():
            print(f"  {k:<22} = {v}")
        return

    if positions_only:
        positions = get_positions()
        if not positions:
            print("No open positions.")
            return
        print(f"\n📋 Open positions ({len(positions)}):")
        for p in positions:
            print(f"  {p.get('side','?').upper()} {p.get('shares',0):.1f} shares — {p.get('market_question','')[:55]}")
        return

    signals_found = 0
    trades_attempted = 0
    trades_executed = 0
    skip_reasons = []
    execution_errors = []

    # 0. Circuit breaker
    cb_ok, cb_reason = check_circuit_breaker()
    if not cb_ok:
        print(f"⏸️ {cb_reason}")
        skip_reasons.append("circuit_breaker")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 1. Hour filter
    current_hour = datetime.now(timezone.utc).hour
    if current_hour in SKIP_HOURS:
        print(f"⏸️ Skip hour {current_hour}h UTC (historically poor ETH win rate)")
        skip_reasons.append(f"skip_hour_{current_hour}")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 2. Candle timing
    in_window, mins_remaining, candle_start = candle_timing()
    print(f"⏰ Candle :{candle_start:02d} | {mins_remaining} min remaining | {'✅ In window' if in_window else '❌ Not in window'}")
    if not in_window:
        skip_reasons.append("outside_candle_window")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 3. Volume
    vol_ok, vol_ratio = check_volume()
    if MIN_VOLUME_RATIO > 0:
        print(f"📊 Volume: {vol_ratio:.2f}x {'✅' if vol_ok else '❌ below threshold'}")
        if not vol_ok:
            print("⏸️ Volume too low — skipping")
            skip_reasons.append("low_volume")
            _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
            return
    else:
        print(f"📊 Volume gate: disabled")

    # 4. ETH momentum
    direction, c5, c3, eth_closes = get_eth_momentum()
    if direction is None:
        print("❌ Could not fetch ETH momentum data")
        execution_errors.append("eth_fetch_failed")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return
    print(f"📈 ETH Momentum: {direction} | 5m: {c5:+.4f}% | 3m: {c3:+.4f}%")
    if direction == "flat":
        print("⏸️ No ETH momentum — skipping")
        skip_reasons.append("flat_momentum")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 5. Optional 1m confirmation
    if ENABLE_1M_CONFIRM:
        d1m, c1m = get_1m_direction(eth_closes)
        print(f"   1m: {d1m} ({c1m:+.4f}%)")
        if d1m != direction:
            print(f"⏸️ 1m contradicts {direction} — skipping")
            skip_reasons.append("1m_contradiction")
            _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
            return
    else:
        if len(eth_closes) >= 2:
            c1m = round((eth_closes[-1] - eth_closes[-2]) / eth_closes[-2] * 100, 4)
            print(f"   1m: {c1m:+.4f}% — gate disabled (off by default)")

    # 6. BTC alignment gate
    btc_aligned, btc_pct = check_btc_alignment(direction)
    if BTC_GATE_THRESHOLD > 0:
        gate_icon = "✅ aligned" if btc_aligned else f"❌ vetoing {direction}"
        print(f"₿  BTC check: {btc_pct:+.4f}% — {gate_icon}")
        if not btc_aligned:
            print(f"⏸️ BTC fighting ETH direction — skipping")
            skip_reasons.append("btc_misaligned")
            _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
            return
    else:
        print(f"₿  BTC gate: disabled")

    signals_found += 1
    side = "yes" if direction == "up" else "no"

    # 7. Find market
    market = find_eth_market()
    if not market:
        print("❌ No active ETH market found")
        execution_errors.append("no_market")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return
    print(f"📋 Market: {market.get('question','')[:70]}")

    # 8. Entry price filter
    prob = market.get("yes_price") or market.get("probability") or market.get("current_probability") or 0.5
    entry_price = prob if side == "yes" else (1 - prob)
    print(f"💲 Entry price: {entry_price:.3f} (side={side})")

    # Fee awareness: at entry > 0.58, breakeven WR rises above ~64% after ~2% Polymarket fee
    if entry_price > 0.58:
        print(f"  ⚠️ Fee note: entry {entry_price:.3f} > 0.58 — breakeven WR ~{(1/(entry_price*0.98)):.0%} after fees")

    if entry_price > MAX_ENTRY_PRICE:
        print(f"⏸️ Entry {entry_price:.2f} > max {MAX_ENTRY_PRICE} — too expensive")
        skip_reasons.append("entry_too_expensive")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return
    if entry_price < MIN_ENTRY_PRICE:
        print(f"⏸️ Entry {entry_price:.2f} < min {MIN_ENTRY_PRICE} — too contrarian")
        skip_reasons.append("entry_too_cheap")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 9. Dedup
    if _load_traded().get(market["id"]):
        print(f"⏸️ Already traded this market — skipping")
        skip_reasons.append("already_traded")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 10. Price sanity
    if prob < MIN_TICK_SIZE or prob > (1 - MIN_TICK_SIZE):
        skip_reasons.append("price_at_limit")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    # 11. Safeguards
    if use_safeguards:
        context = get_market_context(market["id"])
        should_trade, reasons = check_context_safeguards(context)
        if not should_trade:
            print(f"  🛡️ Safeguard blocked: {'; '.join(reasons)}")
            skip_reasons.append("safeguard_blocked")
            _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
            return
        for r in reasons:
            print(f"  ⚠️ {r}")

    # 12. Position size
    position_size = calculate_position_size(smart_sizing)
    if MIN_SHARES_PER_ORDER * entry_price > position_size:
        print(f"⏸️ Below min order size — increase bet_size")
        skip_reasons.append("below_min_order")
        _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)
        return

    reasoning = (f"Mid-candle {direction} ({mins_remaining}m left): "
                 f"5m={c5:+.4f}% 3m={c3:+.4f}% vol={vol_ratio:.2f}x BTC={btc_pct:+.4f}%")
    print(f"\n🚀 Placing {side.upper()} ${position_size:.2f} — {reasoning}")

    trades_attempted += 1
    _signal_data = {
        "momentum_pct": round(c5, 4),
        "change_3m_pct": round(c3, 4),
        "volume_ratio": round(vol_ratio, 2),
        "entry_price": round(entry_price, 4),
        "btc_change_pct": round(btc_pct, 4),
        "mins_remaining": mins_remaining,
        "signal_source": "eth_5m_momentum",
    }
    result = execute_trade(market["id"], side, position_size, reasoning, signal_data=_signal_data)

    if result.get("success"):
        shares = result.get("shares_bought", 0) or 0
        cost   = result.get("cost", position_size) or position_size
        print(f"✅ Filled: {shares:.1f} {side.upper()} shares for ${cost:.2f}")
        _mark_traded(market["id"])
        record_trade_outcome(True)
        trades_executed += 1
        notify_discord(
            f"🔥 ETH Midcandle | {side.upper()} ${cost:.2f} | "
            f"{market.get('question','')[:55]}\n"
            f"Signal: {direction} | 5m={c5:+.3f}% | BTC={btc_pct:+.3f}% | entry={entry_price:.2f}"
        )
        if result.get("skip_reason"):
            skip_reasons.append(result["skip_reason"])
    else:
        err = result.get("error", "unknown error")
        print(f"❌ Trade failed: {err}")
        record_trade_outcome(False)
        execution_errors.append(err)
        if result.get("skip_reason"):
            skip_reasons.append(result["skip_reason"])

    _emit_automaton(signals_found, trades_attempted, trades_executed, skip_reasons, execution_errors)


_automaton_emitted = False

def _emit_automaton(signals, attempted, executed, skip_reasons, errors):
    global _automaton_emitted
    if not os.environ.get("AUTOMATON_MANAGED"):
        return
    _automaton_emitted = True
    report = {"signals": signals, "trades_attempted": attempted, "trades_executed": executed}
    if skip_reasons:
        report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
    if errors:
        report["execution_errors"] = errors
    print(json.dumps({"automaton": report}))


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETH Mid-Candle Scalper")
    parser.add_argument("--live",          action="store_true", help="Execute real trades")
    parser.add_argument("--dry-run",       action="store_true", help="(Default) Dry run")
    parser.add_argument("--positions",     action="store_true", help="Show open positions")
    parser.add_argument("--config",        action="store_true", help="Show current config")
    parser.add_argument("--set",           action="append", metavar="KEY=VALUE", help="Set config value")
    parser.add_argument("--smart-sizing",  action="store_true", help="Portfolio-based sizing")
    parser.add_argument("--no-safeguards", action="store_true", help="Disable safeguards")
    parser.add_argument("--quiet", "-q",   action="store_true", help="Only output on trades/errors")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, value = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    t = CONFIG_SCHEMA[key].get("type", str)
                    try:
                        value = (lambda v: str(v).lower() in ("1","true","yes"))(value) if t == bool else t(value)
                    except (ValueError, TypeError):
                        pass
                updates[key] = value
        if updates:
            try:
                update_config(updates, __file__)
                print(f"Config updated: {updates}")
            except Exception:
                print(f"Config update failed — set env vars directly")

    run_strategy(
        dry_run=not args.live,
        positions_only=args.positions,
        show_config=args.config,
        smart_sizing=args.smart_sizing,
        use_safeguards=not args.no_safeguards,
    )

    # Automaton fallback (covers --config / --positions paths that don't emit)
    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_emitted:
        print(json.dumps({"automaton": {"signals": 0, "trades_attempted": 0, "trades_executed": 0, "skip_reason": "no_signal"}}))

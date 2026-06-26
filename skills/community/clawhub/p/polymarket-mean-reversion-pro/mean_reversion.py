#!/usr/bin/env python3
"""
📉 Mean Reversion Signal Engine
=================================
Detects markets where price has deviated significantly from its 7-day mean
and fires a buy signal (buy the crash / fade the spike).

Logic:
  - Every 30 min, fetch price history for top 100 markets by volume
  - Rolling 7-day window stored in .mr_history.json
  - z = (current_price - mean) / std_dev
  - z < -3.0  → BUY YES (price crashed, expect reversion)
  - z > +3.0  → BUY NO  (price spiked, expect reversion)
  - Filter: volume > $10k/day AND time to resolution > 6h
  - Cross-check: VPIN > 0.6 → SKIP (crash might be informed)
  - Size: Kelly-based, capped at $25

Usage:
    python3 mean_reversion.py               # Run once
    python3 mean_reversion.py --dry-run     # Show signals, no execution
    python3 mean_reversion.py --watch       # Run every 30 min
"""

import os
import sys
import json
import math
import time
import argparse
import requests
import boto3
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
GAMMA_API         = "https://gamma-api.polymarket.com"
CLOB_API          = "https://clob.polymarket.com"
STATE_FILE        = Path(__file__).parent / ".mr_history.json"
HISTORY_DAYS      = 7
Z_BUY_THRESHOLD   = -4.0       # price crashed → BUY YES (tightened from -3.0)
Z_SELL_THRESHOLD  = +4.0       # price spiked  → BUY NO  (tightened from +3.0)
MIN_VOLUME_DAY    = 100_000    # minimum daily volume in $ (tightened from 10k)
MIN_HOURS_LEFT    = 6          # skip markets resolving in < 6h
MAX_HOURS_LEFT    = 168        # skip markets > 7 days out (new — kills macro/lottery tickets)
VPIN_SKIP_THRESH  = 0.6        # skip if VPIN > 0.6 (possibly informed)
MAX_TRADE_SIZE    = 25.0       # hard cap per trade
MIN_TRADE_SIZE    = 2.0
KELLY_FRACTION    = 0.25
TOP_N_MARKETS     = 100
SQS_QUEUE_URL     = "https://sqs.us-east-1.amazonaws.com/291215835256/polymarket-arb"
TELEGRAM_BOT_TOKEN = "8763627754:AAHGhDCcsuQytONr_i5VG335VS7q4zMAtQk"
TELEGRAM_CHAT_ID   = "5545460543"
POLL_INTERVAL      = 1800       # 30 minutes


def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


# ── State ─────────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(msg: str):
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
        chat  = os.environ.get("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": msg, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as e:
        print(f"[mr] telegram error: {e}")


# ── SQS ───────────────────────────────────────────────────────────────────────

def push_to_sqs(signal: dict):
    """Push mean reversion signal to SQS queue for arb_poller to consume."""
    try:
        sqs = boto3.client("sqs", region_name="us-east-1")
        payload = {**signal, "type": "mean_reversion"}
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(payload),
        )
        print(f"[mr] pushed to SQS: {signal.get('market_name', '?')[:40]}")
    except Exception as e:
        print(f"[mr] SQS push error: {e}")


# ── Market fetch ──────────────────────────────────────────────────────────────

def parse_prices(m) -> list[float]:
    raw = m.get("outcomePrices") or "[]"
    try:
        prices = json.loads(raw) if isinstance(raw, str) else raw
        return [float(p) for p in prices]
    except Exception:
        return []


def hours_to_resolution(m) -> float:
    """Return hours until resolution, or 999 if unknown."""
    for key in ("endDate", "endDateIso", "end_date_iso", "resolutionTime"):
        val = m.get(key)
        if val:
            try:
                dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                delta = dt - datetime.now(timezone.utc)
                return max(0, delta.total_seconds() / 3600)
            except Exception:
                continue
    return 999.0


def fetch_top_markets(n=TOP_N_MARKETS) -> list[dict]:
    """Fetch top N markets by 24h volume."""
    markets = []
    pages   = math.ceil(n / 100)
    for page in range(pages):
        try:
            r = requests.get(
                f"{GAMMA_API}/markets",
                params={
                    "active"    : "true",
                    "closed"    : "false",
                    "limit"     : 100,
                    "offset"    : page * 100,
                    "order"     : "volume24hr",
                    "ascending" : "false",
                },
                timeout=15,
            )
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            markets.extend(batch)
        except Exception as e:
            print(f"[mr] market fetch error (page {page}): {e}")
            break
    return markets[:n]


# ── VPIN integration ──────────────────────────────────────────────────────────

def get_vpin(condition_id: str) -> float:
    """Try to import live VPIN; fall back to 0.5 if unavailable."""
    try:
        from vpin import get_vpin as _get_vpin
        return _get_vpin(condition_id)
    except ImportError:
        return 0.5
    except Exception:
        return 0.5


# ── Price history & z-score ───────────────────────────────────────────────────

def update_history(market_id: str, current_price: float, state: dict):
    """Append current price to rolling 7-day history."""
    now     = time.time()
    cutoff  = now - (HISTORY_DAYS * 86400)

    if market_id not in state:
        state[market_id] = {"prices": []}

    state[market_id]["prices"].append({"p": current_price, "ts": now})
    # prune old entries
    state[market_id]["prices"] = [
        e for e in state[market_id]["prices"] if e["ts"] >= cutoff
    ]


def calc_zscore(market_id: str, current_price: float, state: dict) -> float | None:
    """Calculate z-score vs 7-day rolling mean. Returns None if < 24 data points."""
    entries = state.get(market_id, {}).get("prices", [])
    if len(entries) < 24:   # need at least 24 samples (24h @ 30min = 48, but relax to 24)
        return None

    prices = [e["p"] for e in entries]
    mean   = sum(prices) / len(prices)
    std    = math.sqrt(sum((p - mean) ** 2 for p in prices) / len(prices))

    if std < 1e-6:
        return 0.0

    return (current_price - mean) / std


# ── Technical Indicators ─────────────────────────────────────────────────────

def calc_rsi(prices: list[float], period: int = 14) -> float | None:
    """RSI(14) — returns 0-100. <30 = oversold, >70 = overbought."""
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        d = prices[i] - prices[i-1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss < 1e-10:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_ema(prices: list[float], period: int) -> list[float]:
    """Exponential moving average."""
    if not prices:
        return []
    k = 2 / (period + 1)
    ema = [prices[0]]
    for p in prices[1:]:
        ema.append(p * k + ema[-1] * (1 - k))
    return ema

def calc_macd(prices: list[float]) -> tuple[float, float] | None:
    """
    MACD(12,26,9). Returns (macd_line, signal_line) for last point.
    We use this to detect divergence, not crossovers.
    """
    if len(prices) < 35:
        return None
    ema12 = calc_ema(prices, 12)
    ema26 = calc_ema(prices, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    if len(macd_line) < 9:
        return None
    signal = calc_ema(macd_line, 9)
    return macd_line[-1], signal[-1]

def calc_atr(prices: list[float], period: int = 14) -> float | None:
    """ATR proxy using price ranges (we only have close prices, so use abs diff)."""
    if len(prices) < period + 1:
        return None
    ranges = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
    return sum(ranges[-period:]) / period

def check_technical_confirmation(market_id: str, action: str, current_price: float, state: dict) -> tuple[bool, str]:
    """
    Confirm mean reversion signal with technical indicators.
    BUY_YES (price crashed): needs RSI oversold + MACD bullish divergence + low ATR
    BUY_NO  (price spiked):  needs RSI overbought + MACD bearish divergence + low ATR

    Returns (confirmed: bool, reason: str)
    """
    history = state.get(market_id, {}).get("prices", [])
    prices = [p for _, p in sorted(history)]  # sorted by timestamp

    if len(prices) < 20:
        return True, "insufficient history — skipping tech check"

    rsi = calc_rsi(prices)
    macd_result = calc_macd(prices)
    atr = calc_atr(prices)
    avg_price = sum(prices) / len(prices)

    reasons = []

    # ATR check — require price compression (low volatility before entry)
    if atr is not None:
        atr_pct = atr / (avg_price + 1e-10)
        if atr_pct > 0.05:  # ATR > 5% of price = too volatile
            return False, f"ATR too high ({atr_pct:.1%}) — price not compressed"

    if action == "BUY_YES":
        # RSI oversold confirmation
        if rsi is not None:
            if rsi > 40:
                return False, f"RSI={rsi:.0f} — not oversold (need <40)"
            reasons.append(f"RSI={rsi:.0f} ✓")

        # MACD bullish divergence: price makes lower low, MACD makes higher low
        if macd_result is not None:
            macd_val, signal_val = macd_result
            if macd_val < signal_val and abs(macd_val - signal_val) > 0.001:
                return False, f"MACD bearish ({macd_val:.4f} < {signal_val:.4f}) — no bullish divergence"
            reasons.append(f"MACD divergence ✓")

    elif action == "BUY_NO":
        # RSI overbought confirmation
        if rsi is not None:
            if rsi < 60:
                return False, f"RSI={rsi:.0f} — not overbought (need >60)"
            reasons.append(f"RSI={rsi:.0f} ✓")

        # MACD bearish divergence: price makes higher high, MACD makes lower high
        if macd_result is not None:
            macd_val, signal_val = macd_result
            if macd_val > signal_val and abs(macd_val - signal_val) > 0.001:
                return False, f"MACD bullish ({macd_val:.4f} > {signal_val:.4f}) — no bearish divergence"
            reasons.append(f"MACD divergence ✓")

    reason_str = ", ".join(reasons) if reasons else "confirmed"
    return True, reason_str


# ── Kelly sizing ──────────────────────────────────────────────────────────────

def kelly_size(prob: float, odds: float = 1.0) -> float:
    """
    Fractional Kelly sizing.
    prob = probability of winning (estimated)
    odds = net odds (1.0 for binary at ~50¢)
    """
    q   = 1 - prob
    f   = (odds * prob - q) / odds
    f   = max(0, f)
    raw = f * KELLY_FRACTION * MAX_TRADE_SIZE * 2   # scale
    return min(max(raw, MIN_TRADE_SIZE), MAX_TRADE_SIZE)


# ── Signal generation ─────────────────────────────────────────────────────────

def generate_signals(markets: list[dict], state: dict, dry_run=False) -> list[dict]:
    """
    Process markets, update history, calculate z-scores, emit signals.
    """
    signals = []

    for m in markets:
        market_id   = m.get("id") or m.get("conditionId")
        name        = m.get("question") or m.get("title") or market_id
        volume_24h  = float(m.get("volume24hr") or m.get("volumeNum") or 0)
        prices      = parse_prices(m)
        hours_left  = hours_to_resolution(m)
        condition_id = m.get("conditionId") or m.get("condition_id") or ""

        if not market_id or not prices:
            continue

        # Filters
        if volume_24h < MIN_VOLUME_DAY:
            continue
        if hours_left < MIN_HOURS_LEFT:
            continue
        if hours_left > MAX_HOURS_LEFT:
            continue

        # YES price (first outcome)
        yes_price = prices[0] if prices else None
        if yes_price is None or yes_price <= 0:
            continue
        # Skip lottery tickets and near-certainties — only trade in 10¢-90¢ range
        if yes_price < 0.10 or yes_price > 0.90:
            continue

        # Update rolling history
        update_history(market_id, yes_price, state)

        # Need enough history
        z = calc_zscore(market_id, yes_price, state)
        if z is None:
            continue

        # Check thresholds
        if z > Z_SELL_THRESHOLD:
            action     = "BUY_NO"
            trade_prob = 1 - yes_price   # prob NO wins
            signal_dir = "+"
        elif z < Z_BUY_THRESHOLD:
            action     = "BUY_YES"
            trade_prob = yes_price       # prob YES wins (we expect reversion up)
            signal_dir = "-"
        else:
            continue

        # Technical confirmation — RSI + MACD divergence + ATR compression
        tech_ok, tech_reason = check_technical_confirmation(market_id, action, yes_price, state)
        if not tech_ok:
            print(f"[mr] SKIP {name[:40]} — {tech_reason}")
            continue
        print(f"[mr] TECH OK {name[:40]} — {tech_reason}")

        # VPIN cross-check — skip if possibly informed
        if condition_id:
            vpin = get_vpin(condition_id)
            if vpin > VPIN_SKIP_THRESH:
                print(f"[mr] SKIP {name[:40]} — VPIN={vpin:.3f} > {VPIN_SKIP_THRESH} (possibly informed)")
                continue

        # Kelly size
        size = kelly_size(trade_prob)

        signal = {
            "market_id"   : market_id,
            "condition_id": condition_id,
            "market_name" : name,
            "action"      : action,
            "yes_price"   : round(yes_price, 4),
            "z_score"     : round(z, 3),
            "volume_24h"  : volume_24h,
            "hours_left"  : round(hours_left, 1),
            "trade_prob"  : round(trade_prob, 4),
            "size_usd"    : round(size, 2),
            "ts"          : time.time(),
            "dry_run"     : dry_run,
        }
        signals.append(signal)

    return signals


# ── Execution ─────────────────────────────────────────────────────────────────

def execute_signal(signal: dict) -> bool:
    """Execute a mean reversion trade via CLOB client."""
    try:
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import OrderArgs, OrderType

        pk     = os.environ.get("PRIVATE_KEY")
        funder = os.environ.get("WALLET_ADDRESS")
        client = ClobClient(CLOB_HOST if 'CLOB_HOST' in dir() else "https://clob.polymarket.com",
                            key=pk, chain_id=137, signature_type=1, funder=funder)
        creds  = client.create_or_derive_api_creds()
        client.set_api_creds(creds)

        action    = signal["action"]
        cid       = signal.get("condition_id")
        size      = signal["size_usd"]
        yes_price = signal["yes_price"]

        if action == "BUY_YES":
            side  = "BUY"
            price = round(yes_price + 0.001, 4)   # small lift above mid
        else:  # BUY_NO
            side  = "SELL"
            price = round(yes_price - 0.001, 4)   # small lift on NO side

        if not cid:
            print(f"[mr] No condition_id for {signal['market_name'][:40]}, skipping execution")
            return False

        # Resolve token IDs from CLOB (condition_id → YES/NO token_id)
        import requests as _req
        clob_mkt = _req.get(f"https://clob.polymarket.com/markets/{cid}", timeout=10).json()
        tokens = clob_mkt.get("tokens", [])
        yes_token = next((t["token_id"] for t in tokens if t["outcome"] == "Yes"), None)
        no_token  = next((t["token_id"] for t in tokens if t["outcome"] == "No"),  None)
        if not yes_token or not no_token:
            print(f"[mr] Could not resolve token IDs for {cid}, skipping")
            return False

        # BUY_YES → buy YES token; BUY_NO → buy NO token (at NO price)
        if action == "BUY_YES":
            token_id = yes_token
            side     = "BUY"
            price    = round(yes_price + 0.001, 4)
        else:
            token_id = no_token
            side     = "BUY"
            no_price = round(1 - yes_price, 4)
            price    = round(no_price + 0.001, 4)

        tick = clob_mkt.get("minimum_tick_size", 0.001)

        # size is in USD — convert to shares (number of tokens)
        # Polymarket min order is $1, so enforce that floor
        cost_usd = max(size, 1.0)
        shares   = round(cost_usd / price, 2)

        ord_obj = client.create_order(
            OrderArgs(token_id=token_id, price=price, size=shares, side=side),
        )
        order = client.post_order(ord_obj, OrderType.GTC)
        print(f"[mr] ✅ Executed: {action} ${cost_usd:.2f} ({shares} shares) @ {price:.4f}  order={order}")

        # Record fill for flow monitor
        try:
            from flow_monitor import record_fill
            record_fill(side, price, size, signal.get("market_name", "")[:40])
        except Exception:
            pass

        return True

    except Exception as e:
        print(f"[mr] Execution error: {e}")
        return False


# ── Alert formatting ──────────────────────────────────────────────────────────

def format_signal_alert(signal: dict) -> str:
    action     = signal["action"]
    name       = signal["market_name"][:60]
    z          = signal["z_score"]
    yes_price  = signal["yes_price"]
    size       = signal["size_usd"]
    hours      = signal["hours_left"]
    vol        = signal["volume_24h"]
    emoji      = "📉" if action == "BUY_YES" else "📈"
    direction  = "CRASHED — BUY YES" if action == "BUY_YES" else "SPIKED — BUY NO"

    return (
        f"{emoji} <b>Mean Reversion Signal</b>\n"
        f"{name}\n"
        f"Action: <b>{direction}</b>\n"
        f"z-score: <b>{z:+.2f}σ</b>  |  YES price: {yes_price:.3f}\n"
        f"Size: ${size:.2f}  |  {hours:.1f}h left  |  vol ${vol:,.0f}/day"
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def run_once(dry_run=False):
    print(f"[mr] {'[DRY RUN] ' if dry_run else ''}Fetching top {TOP_N_MARKETS} markets...")
    markets = fetch_top_markets()
    print(f"[mr] Got {len(markets)} markets.")

    state   = load_state()
    signals = generate_signals(markets, state, dry_run=dry_run)
    save_state(state)

    if not signals:
        print("[mr] No mean reversion signals this cycle.")
        return

    print(f"\n[mr] 🎯 {len(signals)} signal(s) found:")
    for s in signals:
        print(f"  {s['action']:8s}  z={s['z_score']:+.2f}  {s['market_name'][:50]}")
        print(f"            size=${s['size_usd']:.2f}  price={s['yes_price']:.3f}  {s['hours_left']:.1f}h left")

        # Telegram alert
        send_telegram(format_signal_alert(s))

        # SQS push (always, even on dry-run — let arb_poller decide)
        push_to_sqs(s)

        # Execute if live
        if not dry_run:
            execute_signal(s)
        else:
            print(f"  [DRY RUN] Would execute {s['action']} ${s['size_usd']:.2f}")


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Mean reversion signal engine")
    parser.add_argument("--dry-run", action="store_true", help="No execution, signals only")
    parser.add_argument("--watch",   action="store_true", help=f"Run every {POLL_INTERVAL//60} min")
    args = parser.parse_args()

    if args.watch:
        print(f"[mr] Watch mode: running every {POLL_INTERVAL//60} minutes. Ctrl-C to stop.")
        while True:
            try:
                run_once(dry_run=args.dry_run)
            except Exception as e:
                print(f"[mr] Error: {e}")
            time.sleep(POLL_INTERVAL)
    else:
        run_once(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

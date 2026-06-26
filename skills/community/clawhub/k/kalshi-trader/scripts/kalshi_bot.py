#!/usr/bin/env python3
"""
Kalshi Trading Bot - part of the kalshi-trader OpenClaw skill
Usage:
  python3 kalshi_bot.py          # scan for opportunities
  python3 kalshi_bot.py summary  # print P&L summary
  python3 kalshi_bot.py test     # verify API connection
"""
import requests
import time
import base64
import json
import os
import sys
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# ── Config ────────────────────────────────────────────────────────────────────
KEY_PATH     = os.path.expanduser("~/.kalshi/private_key.pem")
KEY_ID_PATH  = os.path.expanduser("~/.kalshi/key_id.txt")
LOG_PATH     = os.path.expanduser("~/kalshi_trades.json")
BASE         = "https://api.elections.kalshi.com"
MAX_PER_TRADE = 7.00    # max $ per single trade
MIN_YES      = 0.65     # min YES price to consider
MAX_YES      = 0.90     # max YES price to consider
MIN_VOL      = 200      # min volume
MAX_SPREAD   = 0.10     # max bid/ask spread
CASH_BUFFER  = 0.05     # keep 5% cash

# ── Auth ──────────────────────────────────────────────────────────────────────
with open(KEY_PATH, "rb") as f:
    _private_key = serialization.load_pem_private_key(f.read(), password=None)

with open(KEY_ID_PATH) as f:
    _key_id = f.read().strip()

def signed_request(method, path, body=None):
    timestamp = str(int(time.time() * 1000))
    msg = (timestamp + method + path.split("?")[0]).encode()
    sig = _private_key.sign(
        msg,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256()
    )
    headers = {
        "KALSHI-ACCESS-KEY": _key_id,
        "KALSHI-ACCESS-TIMESTAMP": timestamp,
        "KALSHI-ACCESS-SIGNATURE": base64.b64encode(sig).decode(),
        "Content-Type": "application/json"
    }
    if body:
        return requests.request(method, BASE + path, headers=headers, json=body)
    return requests.request(method, BASE + path, headers=headers)

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_balance():
    r = signed_request("GET", "/trade-api/v2/portfolio/balance")
    return r.json().get("balance", 0) / 100

def get_positions():
    r = signed_request("GET", "/trade-api/v2/portfolio/positions?count_filter=position&limit=50")
    return r.json().get("market_positions", [])

def load_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return json.load(f)
    return {"trades": []}

def save_log(data):
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def place_trade(ticker, side, price_dollars, count, reason):
    price_key = "yes_price_dollars" if side == "yes" else "no_price_dollars"
    order = {
        "ticker": ticker,
        "action": "buy",
        "side": side,
        "type": "limit",
        "count": count,
        price_key: str(round(price_dollars, 4)),
        "client_order_id": f"bot-{int(time.time())}"
    }
    r = signed_request("POST", "/trade-api/v2/portfolio/orders", order)
    result = r.json().get("order", {})
    entry = {
        "ticker": ticker, "side": side, "price": price_dollars,
        "count": count, "status": result.get("status"),
        "filled": result.get("fill_count_fp"),
        "cost": result.get("taker_fill_cost_dollars"),
        "fees": result.get("taker_fees_dollars"),
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "order_id": result.get("order_id")
    }
    log = load_log()
    log["trades"].append(entry)
    save_log(log)
    return entry

# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_test():
    balance = get_balance()
    print(f"✅ Connected! Balance: ${balance:.2f}")

def cmd_scan():
    balance = get_balance()
    deployable = balance * (1 - CASH_BUFFER)
    positions = get_positions()
    owned = {p.get("ticker") for p in positions}

    close_ts = int(time.time()) + (7 * 24 * 3600)
    r = signed_request("GET", f"/trade-api/v2/markets?limit=200&status=open&max_close_ts={close_ts}")
    markets = r.json().get("markets", [])

    candidates = []
    for m in markets:
        t = m.get("ticker", "")
        if t in owned:
            continue
        ya = float(m.get("yes_ask_dollars", "0") or "0")
        yb = float(m.get("yes_bid_dollars", "0") or "0")
        vol = float(m.get("volume_fp", "0") or "0")
        if MIN_YES <= ya <= MAX_YES and yb > 0 and vol >= MIN_VOL and (ya - yb) <= MAX_SPREAD:
            candidates.append((ya, vol, m))

    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    print(f"Balance: ${balance:.2f} | Deployable: ${deployable:.2f}")
    print(f"Top candidates ({len(candidates)} total):")
    for ya, vol, m in candidates[:10]:
        print(f"  YES:{ya:.0%} Vol:{int(vol)} Closes:{m.get('close_time','')[:10]} | {m.get('title','')[:55]}")
        print(f"  Ticker: {m.get('ticker')}")
    return candidates, balance, deployable

def cmd_summary():
    balance = get_balance()
    positions = get_positions()
    log = load_log()
    recent = [t for t in log.get("trades", []) if t.get("status") == "executed"][-5:]

    print(f"🌿 Kalshi Trading Summary — {datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M UTC')}")
    print(f"💰 Balance: ${balance:.2f}")
    print(f"\n📊 Open Positions ({len(positions)}):")
    for p in positions:
        print(f"  • {p.get('ticker','')[:40]}")
    if recent:
        print(f"\n🔄 Recent Trades:")
        for t in recent:
            print(f"  • {t['ticker'][:35]} | {t['side'].upper()} {t['filled']} @ ${t['price']} | cost:${t['cost']}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if cmd == "test":
        cmd_test()
    elif cmd == "summary":
        cmd_summary()
    else:
        cmd_scan()

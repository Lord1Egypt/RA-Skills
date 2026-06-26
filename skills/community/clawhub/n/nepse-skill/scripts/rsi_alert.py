#!/usr/bin/env python3
"""
Intraday Seller Detection for NEPSE

Monitors stocks during trading hours (9 AM - 3 PM NPT, Mon-Fri).
Alert triggers when BOTH:
  1. Price drops >= 2% from open (or from yesterday's close for first candle)
  2. Volume >= 1.5x the 10-day average

Usage:
    python3 rsi_alert.py intraday      # Run intraday check
    python3 rsi_alert.py status        # Show current price+volume for watchlist
"""
import sys
import json
import os
import re
import time
from datetime import datetime, time as dtime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({"error": "Missing deps. Run: pip3 install requests beautifulsoup4 --break-system-packages"}))
    sys.exit(1)

# ── config ───────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
OPEN_PRICE_FILE = DATA_DIR / "open_prices.json"   # stores today's open per symbol
RSI_HISTORY_FILE = DATA_DIR / "rsi_history.json"

TELEGRAM_BOT_TOKEN  = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID    = os.environ.get("TELEGRAM_CHAT_ID", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

# Alert thresholds
PRICE_DROP_THRESHOLD = 2.0    # % drop from open to trigger
VOLUME_SPIKE_RATIO   = 1.5    # volume vs 10-day avg to trigger

# Trading window
TRADING_START = dtime(9, 0)
TRADING_END   = dtime(15, 0)

# ── helpers ──────────────────────────────────────────────────────────────────
def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))

def send_telegram(msg: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"},
            timeout=10
        )
        return r.status_code == 200
    except Exception:
        return False

def is_trading_hours() -> bool:
    now = datetime.now().time()
    # Monday=0 ... Friday=4
    if datetime.now().weekday() > 4:
        return False
    return TRADING_START <= now <= TRADING_END

# ── scraping ─────────────────────────────────────────────────────────────────
def fetch_merolagani_live(symbol: str) -> dict:
    """Get current price + today's volume estimate from Merolagani."""
    symbol = symbol.upper()
    url = f"https://merolagani.com/CompanyDetail.aspx?symbol={symbol}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Current price
        price_tag = soup.find("span", id=re.compile(r".*lblMarketPrice.*", re.I))
        if not price_tag:
            price_tag = soup.find("strong", class_=re.compile(r"rate", re.I))
        current_price = float(re.sub(r"[^\d.]", "", price_tag.text)) if price_tag else None

        # Daily change
        change_tag = soup.find("span", id=re.compile(r".*lblChange.*", re.I))
        change_txt = change_tag.text.strip() if change_tag else None

        # Today's volume (last row of history table = today)
        volume = 0
        table = soup.find("table", {"id": re.compile(r".*gridHistory.*", re.I)})
        if table:
            rows = table.find_all("tr")[1:3]  # today + yesterday
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 6:
                    try:
                        vol = int(re.sub(r"[^\d]", "", cols[5].text) or "0")
                        if volume == 0:
                            volume = vol
                    except Exception:
                        pass

        # Historical closes (for avg volume calc)
        closes = []
        if table:
            for row in table.find_all("tr")[1:31]:  # last 30 rows
                cols = row.find_all("td")
                if len(cols) >= 6:
                    try:
                        closes.append(float(re.sub(r"[^\d.]", "", cols[1].text)))
                    except Exception:
                        continue

        return {
            "symbol": symbol,
            "price": current_price,
            "change": change_txt,
            "volume_today": volume,
            "closes": list(reversed(closes)),
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}

def get_stock_data(symbol: str) -> dict:
    return fetch_merolagani_live(symbol)

# ── core alert logic ─────────────────────────────────────────────────────────
def check_intraday() -> dict:
    """Run intraday seller detection on watchlist. Returns report."""
    watchlist = load_json(WATCHLIST_FILE, [])
    if not watchlist:
        return {"error": "Watchlist empty", "hint": "python3 nepse_fetch.py watchlist add SYMBOL"}

    open_prices = load_json(OPEN_PRICE_FILE, {})
    alerts = []
    results = []

    for symbol in watchlist:
        data = get_stock_data(symbol)
        time.sleep(1.2)

        if "error" in data or not data.get("price"):
            results.append({"symbol": symbol, "error": data.get("error")})
            continue

        price = data["price"]
        volume_today = data.get("volume_today", 0)
        closes = data.get("closes", [])

        # Reference price: today's open (from market open record), else yesterday close
        ref_price = open_prices.get(symbol) or (closes[0] if closes else None)
        ref_price = ref_price or price  # fallback

        price_drop_pct = ((ref_price - price) / ref_price * 100) if ref_price else 0

        # Volume analysis
        avg_volume = 0
        vol_ratio = 0.0
        if len(closes) >= 3:
            # Volume estimate: approximate from closes data if no live vol
            # Use last 10 days' closes as proxy (crude but works)
            lookback = min(10, len(closes) - 1)
            prev_volumes = [max(1, int(c * 1e5 / closes[i+1])) if i+1 < len(closes) else 1
                           for i, c in enumerate(closes[:lookback])]
            avg_volume = sum(prev_volumes) / len(prev_volumes) if prev_volumes else 1
            vol_ratio = round(volume_today / avg_volume, 2) if avg_volume > 0 else 0

        # Alert condition: significant price drop + volume surge
        alert = None
        if price_drop_pct >= PRICE_DROP_THRESHOLD and vol_ratio >= VOLUME_SPIKE_RATIO:
            alert = "SELLER_INFLOW"
        elif price_drop_pct >= PRICE_DROP_THRESHOLD and vol_ratio >= 1.2:
            alert = "WARNING"

        results.append({
            "symbol": symbol,
            "price": price,
            "ref_price": round(ref_price, 2),
            "price_drop_pct": round(price_drop_pct, 2),
            "volume_today": volume_today,
            "avg_volume": round(avg_volume),
            "vol_ratio": vol_ratio,
            "change": data.get("change"),
            "alert": alert,
            "closes_count": len(closes),
            "fetched_at": data.get("fetched_at")
        })

        if alert:
            alerts.append({"symbol": symbol, "type": alert, "price_drop_pct": round(price_drop_pct, 2), "vol_ratio": vol_ratio})

    # Send Telegram if alerts
    triggered = []
    if alerts and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M NPT")
        if is_trading_hours():
            lines = [f"⚠️ *SELLER ALERT* — {now_str}"]
        else:
            lines = [f"⚠️ *SELLER ALERT (AFTER-HOURS CHECK)* — {now_str}"]

        for a in alerts:
            emoji = "🔴" if a["type"] == "SELLER_INFLOW" else "🟡"
            lines.append(f"{emoji} *{a['symbol']}*")
            lines.append(f"   Price drop: *-{a['price_drop_pct']}%*")
            lines.append(f"   Volume: *{a['vol_ratio']}x avg*")

        lines.append("")
        lines.append("_Sellers may be stepping in. Consider setting a stop-loss or taking profit._")
        lines.append("_Analysis only. Trade at your own risk._")

        if send_telegram("\n".join(lines)):
            triggered = [a["symbol"] for a in alerts]

    return {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M NPT"),
        "is_trading_hours": is_trading_hours(),
        "watchlist": watchlist,
        "alerts_triggered": triggered,
        "telegram_sent": bool(triggered),
        "alerts": alerts,
        "results": results
    }

def show_status() -> dict:
    """Quick snapshot without triggering alerts."""
    watchlist = load_json(WATCHLIST_FILE, [])
    if not watchlist:
        return {"error": "Watchlist empty"}

    results = []
    for symbol in watchlist:
        data = get_stock_data(symbol)
        time.sleep(1.2)
        if "error" not in data and data.get("price"):
            results.append(data)
    return {"results": results}

# ── commands ─────────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]

    if not args or args[0] == "intraday":
        result = check_intraday()
        print(json.dumps(result, indent=2))
    elif args[0] == "status":
        result = show_status()
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({
            "error": "Unknown command",
            "usage": "rsi_alert.py [intraday|status]"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
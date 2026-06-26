#!/usr/bin/env python3
"""
Alpha Vantage Stock Scanner — Catalyst Edge
Pulls live RSI, price, and momentum for JB's watchlist.
Free tier: 25 API calls/day, 5/min.
API key: AYP4CXXCHLRXNH8L
"""
import urllib.request, json, os, sys
from datetime import datetime

KEY = "AYP4CXXCHLRXNH8L"
BASE_URL = "https://www.alphavantage.co/query"
SCAN_DIR = "/workspace/skills/catalyst-edge/stock_scanner"
WATCHLIST_FILE = f"{SCAN_DIR}/watchlist.json"
LAST_SCAN_FILE = f"{SCAN_DIR}/last_scan.json"
LOG_FILE = f"{SCAN_DIR}/scan_log.md"

# ──────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────
DEFAULT_WATCHLIST = [
    "VT",    # Vanguard Total World Stock ETF
    "VTI",   # Vanguard Total Stock Market ETF
    "QYLD",  # Global X NASDAQ 100 Covered Call ETF
    "JEPI",  # JPMorgan Equity Premium Income ETF
    "SCHD",  # Schwab US Dividend Equity ETF
    "VYM",   # Vanguard High Dividend Yield ETF
    "AMD",   # Advanced Micro Devices
    "IBM",   # Test ticker
]

# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def get_quote(symbol):
    """Get GLOBAL_QUOTE — price, volume, change."""
    url = f"{BASE_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={KEY}"
    d = fetch(url)
    q = d.get("Global Quote", {})
    if not q:
        note = d.get("Note", d.get("Information", ""))
        return None, f"Rate limit or error: {note}"
    return {
        "price": float(q.get("05. price", 0)),
        "volume": int(q.get("06. volume", 0)),
        "change": float(q.get("09. change", 0)),
        "change_pct": float(q.get("10. change percent", "0").replace("%","")),
    }, None

def get_rsi(symbol, period=14):
    """Calculate RSI(14) from TIME_SERIES_DAILY compact (100 days)."""
    url = f"{BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={KEY}&outputsize=compact"
    d = fetch(url)
    ts = d.get("Time Series (Daily)", {})
    if not ts:
        note = d.get("Note", d.get("Information", ""))
        return None, f"Rate limit or error: {note}"

    # Get last 'period+1' closes
    closes = [float(v["4. close"]) for v in list(ts.values())[:period+1]]
    closes.reverse()  # oldest first

    # Calculate RSI
    gains = []
    losses = []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i-1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(delta))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100, None
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 1), None

def get_sma(symbol, days=20):
    """Get SMA(d) as trend confirmation."""
    url = f"{BASE_URL}?function=SMA&symbol={symbol}&interval=daily&time_period={days}&series_type=close&apikey={KEY}"
    d = fetch(url)
    sma_data = d.get("Technical Analysis: SMA", {})
    if not sma_data:
        return None
    latest = list(sma_data.keys())[0]
    return float(sma_data[latest]["SMA"])

def score_stock(rsi, change_pct):
    """
    Score 0-100 based on RSI + momentum.
    RSI > 70 = overbought (lower score)
    RSI < 30 = oversold (higher score)
    Strong up day = momentum bonus
    """
    # RSI score component (40% of score)
    if rsi >= 80:
        rsi_score = 10
    elif rsi >= 70:
        rsi_score = 30
    elif rsi >= 60:
        rsi_score = 50
    elif rsi >= 50:
        rsi_score = 60
    elif rsi >= 40:
        rsi_score = 70
    elif rsi >= 30:
        rsi_score = 85
    else:
        rsi_score = 95

    # Momentum component (60%)
    if change_pct >= 5:
        mom_score = 100
    elif change_pct >= 3:
        mom_score = 85
    elif change_pct >= 1:
        mom_score = 70
    elif change_pct >= 0:
        mom_score = 55
    elif change_pct >= -2:
        mom_score = 45
    else:
        mom_score = 30

    score = int(rsi_score * 0.4 + mom_score * 0.6)

    # Signal
    if score >= 75:
        signal = "STRONG BUY"
    elif score >= 60:
        signal = "BUY"
    elif score >= 45:
        signal = "HOLD"
    elif score >= 30:
        signal = "WEAK"
    else:
        signal = "AVOID"

    return score, signal

# ──────────────────────────────────────────────────────────────
# Main scan
# ──────────────────────────────────────────────────────────────
def scan(watchlist=None):
    results = []
    errors = []

    if watchlist is None:
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE) as f:
                watchlist = json.load(f).get("tickers", DEFAULT_WATCHLIST)
        else:
            watchlist = DEFAULT_WATCHLIST

    print(f"Scanning {len(watchlist)} tickers: {', '.join(watchlist)}")

    for ticker in watchlist:
        print(f"  Scanning {ticker}...", end=" ", flush=True)

        # Get quote
        quote, err = get_quote(ticker)
        if err:
            print(f"ERROR ({err[:50]})")
            errors.append({"ticker": ticker, "error": err})
            continue

        # Get RSI
        rsi, err = get_rsi(ticker)
        if err:
            print(f"RSI ERROR ({err[:50]})")
            # Still record quote without RSI
            results.append({
                "ticker": ticker,
                "price": quote["price"],
                "volume": quote["volume"],
                "change_pct": quote["change_pct"],
                "rsi": None,
                "score": None,
                "signal": "DATA ERROR"
            })
            continue

        # Score
        score, signal = score_stock(rsi, quote["change_pct"])

        results.append({
            "ticker": ticker,
            "price": quote["price"],
            "volume": quote["volume"],
            "change_pct": quote["change_pct"],
            "rsi": rsi,
            "score": score,
            "signal": signal,
            "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M CDT")
        })
        print(f"RSI={rsi} | Score={score} | {signal}")

    # Sort by score (highest first)
    scored = [r for r in results if r["score"] is not None]
    unscored = [r for r in results if r["score"] is None]
    scored.sort(key=lambda x: x["score"], reverse=True)

    output = {
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M CDT"),
        "api_key_used": KEY[:8] + "...",
        "tickers_scanned": len(results),
        "errors": errors,
        "results": scored + unscored
    }

    # Save
    with open(LAST_SCAN_FILE, "w") as f:
        json.dump(output, f, indent=2)

    # Log
    log_entry = f"\n## Scan {datetime.now().strftime('%Y-%m-%d %H:%M CDT')} — {len(scored)} results\n"
    for r in scored:
        log_entry += f"- **{r['ticker']}**: RSI={r['rsi']} | Score={r['score']} | {r['signal']} | \${r['price']} ({r['change_pct']:+.2f}%)\n"
    log_entry += f"- Errors: {len(errors)}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    print(f"\nScan complete. {len(scored)} scored, {len(errors)} errors.")
    return output

# ──────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tickers = sys.argv[1:] if len(sys.argv) > 1 else None
    result = scan(tickers)
    print(json.dumps(result, indent=2))

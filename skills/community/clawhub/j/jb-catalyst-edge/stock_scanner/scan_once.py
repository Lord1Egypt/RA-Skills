#!/usr/bin/env python3
"""
Catalyst Edge Scanner — Yahoo Finance Primary (unlimited, no auth)
Alpha Vantage kept burning its 25-call daily quota in a single run — replaced.
Yahoo Finance chart API: no key, no rate limit, full OHLCV + RSI.
Saves results to last_scan.json.
"""
import urllib.request, json, os, time
from datetime import datetime

SCAN_DIR = "/workspace/skills/catalyst-edge/stock_scanner"
LAST_SCAN_FILE = f"{SCAN_DIR}/last_scan.json"
LOG_FILE = f"{SCAN_DIR}/scan_log.md"

TICKERS = ["VT", "VTI", "QYLD", "JEPI", "SCHD", "VYM", "AMD"]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def get_rsi_from_closes(closes, period=14):
    """Wilder's RSI via Yahoo Finance daily closes."""
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    return round(100 - (100 / (1 + avg_gain / avg_loss)), 1)

def get_quote_rsi(symbol):
    """Fetch price + RSI from Yahoo Finance chart API (no auth)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=3mo"
    d = fetch(url)
    result = d["chart"]["result"][0]
    meta = result["meta"]
    q = result["indicators"]["quote"][0]
    closes = [c for c in q["close"] if c is not None]
    if not closes:
        return None, None, "No close data"
    price = meta["regularMarketPrice"]
    prev = meta.get("chartPreviousClose", closes[-1])
    change_pct = round(((price - prev) / prev) * 100, 2)
    rsi = get_rsi_from_closes(closes)
    return price, change_pct, rsi

def score_rsi(rsi, change_pct):
    if rsi is None:
        return None, "UNKNOWN"
    # RSI component (40%)
    if rsi >= 80: rsi_s = 10
    elif rsi >= 70: rsi_s = 30
    elif rsi >= 60: rsi_s = 50
    elif rsi >= 50: rsi_s = 60
    elif rsi >= 40: rsi_s = 70
    elif rsi >= 30: rsi_s = 85
    else: rsi_s = 95
    # Momentum component (60%)
    if change_pct >= 5: m_s = 100
    elif change_pct >= 3: m_s = 85
    elif change_pct >= 1: m_s = 70
    elif change_pct >= 0: m_s = 55
    elif change_pct >= -2: m_s = 45
    else: m_s = 30
    score = int(rsi_s * 0.4 + m_s * 0.6)
    signal = "STRONG BUY" if score >= 75 else "BUY" if score >= 60 else "HOLD" if score >= 45 else "WEAK" if score >= 30 else "AVOID"
    return score, signal

def run_scan():
    results, errors = [], []

    for i, ticker in enumerate(TICKERS):
        print(f"[{i+1}/{len(TICKERS)}] {ticker}...", end=" ", flush=True)
        price, change_pct, rsi_or_err = get_quote_rsi(ticker)
        if price is None:
            print(f"ERROR: {rsi_or_err}")
            errors.append({"ticker": ticker, "step": "fetch", "error": rsi_or_err})
            continue
        score, signal = score_rsi(rsi_or_err, change_pct)
        print(f"${price:.2f} ({change_pct:+.2f}%) | RSI={rsi_or_err} | Score={score} | {signal}")
        results.append({
            "ticker": ticker,
            "price": round(price, 2),
            "change_pct": change_pct,
            "rsi": rsi_or_err,
            "score": score,
            "signal": signal,
            "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M CDT")
        })
        time.sleep(0.5)  # polite delay, no rate limit

    scored = sorted(results, key=lambda x: x["score"], reverse=True)

    output = {
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M CDT"),
        "data_source": "Yahoo Finance (primary, no auth)",
        "tickers_scanned": len(results),
        "errors": errors,
        "results": scored
    }

    with open(LAST_SCAN_FILE, "w") as f:
        json.dump(output, f, indent=2)

    with open(LOG_FILE, "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M CDT")
        f.write(f"\n## {ts} | Yahoo Finance | {len(scored)} scanned | {len(errors)} errors\n")
        for r in scored:
            f.write(f"- **{r['ticker']}**: RSI={r['rsi']} | Score={r['score']} | {r['signal']} | ${r['price']} ({r['change_pct']:+.2f}%)\n")
        for e in errors:
            f.write(f"  ERROR {e['ticker']}: {e['error']}\n")

    print(f"\nDone. {len(scored)} scanned, {len(errors)} errors.")
    return output

if __name__ == "__main__":
    run_scan()

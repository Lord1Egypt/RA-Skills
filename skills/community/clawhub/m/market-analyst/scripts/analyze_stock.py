#!/usr/bin/env python3
"""
Single stock deep analysis — full technical
Usage: python3 analyze_stock.py FPT [HOSE]
       python3 analyze_stock.py VCB HOSE
       python3 analyze_stock.py HPG
"""
import urllib.request, json, sys

def analyze(ticker, exchange="HOSE"):
    payload = {
        "symbols": {"tickers": [f"{exchange}:{ticker}"]},
        "columns": ["name","close","change","change_abs","volume","high","low","open",
                   "RSI","EMA20","EMA50","EMA200","MACD.macd","MACD.signal",
                   "BB.upper","BB.lower","ATR","Stoch.K","Stoch.D",
                   "price_52_week_high","price_52_week_low"]
    }

    req = urllib.request.Request(
        "https://scanner.tradingview.com/vietnam/scan",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())

    if not data.get("data"):
        print(f"❌ Not found {exchange}:{ticker}")
        print("   Check the stock ticker and exchange (HOSE/HNX/UPCOM)")
        return None

    d = data["data"][0]["d"]
    name, close, chg, chg_abs, vol, high, low, open_, rsi, ema20, ema50, ema200, macd, macd_sig, bb_up, bb_low, atr, stoch_k, stoch_d, h52, l52 = d

    # --- Signal computation ---
    rsi_sig   = "🟢 Oversold"   if rsi < 35  else ("🔴 Overbought" if rsi > 65  else "🟡 Neutral")
    stoch_sig = "🟢 Oversold"   if stoch_k < 20 else ("🔴 Overbought" if stoch_k > 80 else "🟡 Neutral")
    macd_label = "🟢 Bullish" if macd > macd_sig else "🔴 Bearish"

    def arrow(price, ref):
        return "▲" if (price and ref and price > ref) else "▼"

    t20  = arrow(close, ema20)
    t50  = arrow(close, ema50)
    t200 = arrow(close, ema200)

    # Trend summary
    if close > ema20 and close > ema50 and close > ema200:
        trend_summary = "Strong uptrend ▲▲▲"
    elif close > ema200:
        trend_summary = "Long-term uptrend, short-term correction"
    elif close < ema20 and close < ema50 and close < ema200:
        trend_summary = "Strong downtrend ▼▼▼"
    else:
        trend_summary = "Mixed — sideways"

    # Bollinger position
    bb_mid = (bb_up + bb_low) / 2
    if close <= bb_low * 1.01:
        bb_label = "🟢 At BB Lower (oversold zone)"
    elif close >= bb_up * 0.99:
        bb_label = "🔴 At BB Upper (overbought zone)"
    elif close < bb_mid:
        bb_label = "Below midband"
    else:
        bb_label = "Above midband"

    # 52W position
    pos52 = (close - l52) / (h52 - l52) * 100 if (h52 and l52 and h52 != l52) else 0

    # Buy zone check
    buy_score = 0
    buy_reasons = []
    if rsi < 40:
        buy_score += 1
        buy_reasons.append(f"RSI={rsi:.1f} (<40)")
    if close > ema200:
        buy_score += 1
        buy_reasons.append("Above EMA200")
    if close <= bb_low * 1.03:
        buy_score += 1
        buy_reasons.append("Near BB Lower")

    if buy_score >= 2:
        verdict = "🟢 GOOD BUY ZONE"
    elif buy_score == 1:
        verdict = "🟡 WATCH"
    else:
        verdict = "⏳ WAIT"

    # --- Output ---
    print(f"\n{'='*56}")
    print(f"  📊 {ticker} ({exchange})")
    print(f"{'='*56}")
    print(f"  Giá:      {close:>10,.0f} VND  ({chg:+.2f}%  {chg_abs:+,.0f})")
    print(f"  O/H/L:    {open_:,.0f} / {high:,.0f} / {low:,.0f}")
    print(f"  Volume:   {vol/1e6:.2f}M shares")
    print(f"\n  ─── Technical Indicators ────────────────────────")
    print(f"  RSI(14):   {rsi:>6.1f}  {rsi_sig}")
    print(f"  EMA20:     {ema20:>10,.0f}  {t20}")
    print(f"  EMA50:     {ema50:>10,.0f}  {t50}")
    print(f"  EMA200:    {ema200:>10,.0f}  {t200}")
    print(f"  Trend:     {trend_summary}")
    print(f"  MACD:      {macd:>8.1f} / Signal: {macd_sig:.1f}  {macd_label}")
    print(f"  Stoch K/D: {stoch_k:>5.1f} / {stoch_d:.1f}  {stoch_sig}")
    print(f"  BB Upper:  {bb_up:>10,.0f}")
    print(f"  BB Lower:  {bb_low:>10,.0f}  {bb_label}")
    print(f"  ATR(14):   {atr:>10,.0f}")
    print(f"\n  ─── 52 Weeks ──────────────────────────────────")
    print(f"  High:      {h52:>10,.0f}")
    print(f"  Low:       {l52:>10,.0f}")
    print(f"  Position:    {pos52:.1f}% from 52W low")
    print(f"\n  ─── Conclusion ─────────────────────────────────")
    print(f"  {verdict}")
    if buy_reasons:
        print(f"  Reason: {', '.join(buy_reasons)}")
    print(f"{'='*56}")

    return {
        "ticker": ticker, "exchange": exchange,
        "close": close, "change": chg, "volume": vol,
        "rsi": rsi, "ema20": ema20, "ema50": ema50, "ema200": ema200,
        "macd": macd, "macd_signal": macd_sig,
        "bb_upper": bb_up, "bb_lower": bb_low, "atr": atr,
        "stoch_k": stoch_k, "stoch_d": stoch_d,
        "high52": h52, "low52": l52, "pos52w": pos52,
        "buy_score": buy_score, "verdict": verdict
    }

if __name__ == "__main__":
    ticker   = sys.argv[1].upper() if len(sys.argv) > 1 else "FPT"
    exchange = sys.argv[2].upper() if len(sys.argv) > 2 else "HOSE"
    analyze(ticker, exchange)

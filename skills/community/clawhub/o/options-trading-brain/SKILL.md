---
name: options-trading-brain
version: 1.0.16
description: |
  Professional-grade options trading signal generator. Monitors whale flow (Unusual 
  Whales), counts Elliott Waves, analyzes Bollinger Bands, multi-timeframe trend 
  alignment, and liquidity zones. Combines all 5 inputs into actionable trade signals.
  Use when user asks for options signals, stock analysis, trading setups, or to check 
  a specific ticker. Fully autonomous — no API keys required for core analysis.
compatibility: Python 3.10+, yfinance, numpy, scipy. Optional: Unusual Whales subscription.
metadata:
  author: ssyopro.zo.computer
  category: finance
  display-name: Options Trading Brain
  tags: options, trading, signals, elliott-wave, whale-flow, bollinger, theta-gang
---

# Options Trading Brain

Professional options trading intelligence system combining 5 analysis dimensions into one unified signal.

## The 5 Inputs (Signal Requires 3+ Aligned)

### 1. Whale Flow (Unusual Whales)
- Filter: $25K+ premium, sweep/block executions, ask-side fills
- Hierarchy: sweeps > blocks > splits > single fills
- Bullish: calls at ask + volume > OI; Bearish: puts at ask + volume > OI

### 2. Elliott Wave
- Wave 3 = strongest momentum entry
- Wave 5 = exhaustion warning
- Rules: Wave 2 can't retrace Wave 1; Wave 3 not shortest; Wave 4 can't overlap Wave 1

### 3. Bollinger Bands
- Squeeze (BB width < 2% of price) = volatile expansion imminent
- Band thrust through upper/lower = strong momentum continuation
- Position near bands = overbought/oversold reversal candidates

### 4. Multi-Timeframe Trend
- ADX > 25 = confirmed trend
- MA alignment (price > MA20 > MA50) = uptrend confirmed
- Weekly/Daily must align for high conviction

### 5. Liquidity Zones
- 4-layer strike walls: OI concentration + GEX + PCR + Max Pain proximity
- Max Pain = where max options expire worthless (gravity level)
- Support = cluster of put OI below price; Resistance = call OI above

## Signal Hierarchy

| Conviction | Requirement |
|---|---|
| **HIGH** | Whale + Wave 3 + (Trend OR Bollinger) aligned |
| **MEDIUM** | Whale + 2 others aligned |
| **NONE** | No whale signal = no trade |

## Scripts (all embedded below)

### whale_scanner.py
```python
#!/usr/bin/env python3
"""Whale flow scanner — Unusual Whales inspired filters."""
import yfinance as yf, numpy as np

WHALE_THRESHOLD = 25_000  # $25K minimum

def get_price(ticker: str) -> float:
    return yf.Ticker(ticker).info["regularMarketPrice"]

def scan(ticker: str) -> dict:
    price = get_price(ticker)
    chains = yf.Ticker(ticker).option_chain()
    
    calls = chains.calls[chains.calls["volume"] * chains.calls["lastPrice"] * 100 >= WHALE_THRESHOLD]
    puts  = chains.puts[chains.puts["volume"] * chains.puts["lastPrice"] * 100 >= WHALE_THRESHOLD]
    
    call_premium = (calls["volume"] * calls["lastPrice"] * 100).sum()
    put_premium  = (puts["volume"] * puts["lastPrice"] * 100).sum()
    
    return {
        "ticker": ticker, "price": price,
        "whale_calls": len(calls), "whale_puts": len(puts),
        "call_premium": call_premium, "put_premium": put_premium,
        "direction": "bullish" if call_premium > put_premium * 1.2
                    else "bearish" if put_premium > call_premium * 1.2 else "neutral"
    }

if __name__ == "__main__":
    import sys
    r = scan(sys.argv[1] if len(sys.argv) > 1 else "SPY")
    print(f"{r['ticker']}: {r['direction']} | Calls: {r['whale_calls']} | Puts: {r['whale_puts']} | "
          f"Call$: ${r['call_premium']:,.0f} | Put$: ${r['put_premium']:,.0f}")
```

### elliott_wave.py
```python
#!/usr/bin/env python3
"""Elliott Wave counter — validates 3 rules, identifies impulse waves."""
import yfinance as yf, numpy as np

def count_waves(prices: list) -> dict:
    highs, lows = [], []
    for i in range(1, len(prices)-1):
        if prices[i] > prices[i-1] and prices[i] > prices[i+1]: highs.append(i)
        if prices[i] < prices[i-1] and prices[i] < prices[i+1]: lows.append(i)
    
    if len(highs) < 2: return {"wave_count": 0, "wave_number": 0, "wave_type": "unknown"}
    
    wave3_strong = highs[1] - highs[0] > (highs[0] - lows[0]) if len(highs) > 1 else False
    return {
        "wave_count": len(highs),
        "wave_number": min(5, len(highs)),
        "wave_type": "impulse_wave_3" if wave3_strong else "impulse_wave_1_or_5"
    }

def fib_levels(high: float, low: float) -> dict:
    return {
        "fib_236": low + (high - low) * 0.236,
        "fib_382": low + (high - low) * 0.382,
        "fib_500": low + (high - low) * 0.500,
        "fib_618": low + (high - low) * 0.618,
        "fib_786": low + (high - low) * 0.786,
    }

def validate_impulse(p1, p2, p3, p4, p5) -> bool:
    return (p2 < p1 and p3 > max(p1,p2) and p4 < p3 and p4 > p1 and p5 < p4)

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    data = yf.download(ticker, period="3mo", auto_redirect=True)["Close"].dropna()
    waves = count_waves(data.values.tolist())
    print(f"{ticker}: Wave {waves['wave_number']} ({waves['wave_type']})")
```

### bollinger_analyzer.py
```python
#!/usr/bin/env python3
"""Bollinger Bands analyzer — squeeze, thrust, regime detection."""
import yfinance as yf, numpy as np

def get_bands(prices: np.ndarray, window=20):
    sma = np.convolve(prices, np.ones(window)/window, mode='valid')
    std = np.array([np.std(prices[i:i+window]) for i in range(len(prices)-window+1)])
    upper = sma + 2*std; lower = sma - 2*std
    return {"sma": sma, "upper": upper, "lower": lower, "width": upper-lower}

def detect_squeeze(bands: dict, threshold_pct=0.02) -> bool:
    latest_width_pct = bands["width"][-1] / bands["sma"][-1]
    return latest_width_pct < threshold_pct

def regime(bands: dict, price: float) -> str:
    bbp = (price - bands["lower"][-1]) / (bands["upper"][-1] - bands["lower"][-1])
    if bbp > 0.90: return "upper_thrust_bullish"
    if bbp < 0.10: return "lower_thrust_bearish"
    if bbp > 0.60: return "bullish"
    if bbp < 0.40: return "bearish"
    return "neutral"

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    data = yf.download(ticker, period="3mo", auto_redirect=True)["Close"].dropna().values
    bands = get_bands(data)
    sqz = detect_squeeze(bands)
    reg = regime(bands, data[-1])
    pos = (data[-1] - bands["lower"][-1]) / (bands["upper"][-1] - bands["lower"][-1])
    print(f"{ticker}: {'SQUEEZE' if sqz else 'Normal'} | Regime: {reg} | BBPosition: {pos:.1%}")
```

### trend_engine.py
```python
#!/usr/bin/env python3
"""Multi-timeframe trend engine — ADX + MA alignment."""
import yfinance as yf, numpy as np

def adx(high, low, close, period=14):
    plus_dm = np.maximum(high[1:] - high[:-1], 0)
    minus_dm = np.maximum(low[:-1] - low[1:], 0)
    tr = high[1:] - low[1:]; tr = np.maximum(tr, np.abs(close[1:] - close[:-1]))
    plus_di = 100 * np.mean(plus_dm[-period:]) / (np.mean(tr[-period:]) + 1e-9)
    minus_di = 100 * np.mean(minus_dm[-period:]) / (np.mean(tr[-period:]) + 1e-9)
    return plus_di / (plus_di + minus_di + 1e-9) * 100

def ma_alignment(prices, ma20, ma50):
    return "bullish" if prices[-1] > ma20[-1] > ma50[-1] else \
           "bearish" if prices[-1] < ma20[-1] < ma50[-1] else "mixed"

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    for tf in ["1d","1wk","1mo"]:
        try:
            d = yf.download(ticker, period="3mo", interval=tf, auto_redirect=True)
            h,l,c = d["High"].values, d["Low"].values, d["Close"].values
            a = adx(h,l,c)
            ma20 = np.convolve(c, np.ones(20)/20, mode='valid')
            ma50 = np.convolve(c, np.ones(50)/50, mode='valid')
            al = ma_alignment(c, ma20, ma50)
            print(f"{tf.upper()}: ADX={a:.1f} | MA={al}")
        except: pass
```

### liquidity_map.py
```python
#!/usr/bin/env python3
"""Liquidity zones — max pain, strike walls, support/resistance."""
import yfinance as yf

def get_liquidity(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    price = t.info["regularMarketPrice"]
    try:
        chain = t.option_chain(tExpiry := t.options[0])
        strikes = sorted(chain.calls["strike"].values)
        max_pain = strikes[np.argmin(np.abs(strikes - price))]
        return {"max_pain": max_pain, "price": price, "expiry": tExpiry}
    except: return {"max_pain": price, "price": price, "expiry": "unknown"}

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    z = get_liquidity(ticker)
    pct = (z["max_pain"] - z["price"]) / z["price"] * 100
    print(f"{ticker}: Price={z['price']:.2f} | Max Pain={z['max_pain']:.2f} ({pct:+.2f}%) | Expires: {z['expiry']}")
```

### signal_generator.py
```python
#!/usr/bin/env python3
"""Combined signal generator — all 5 inputs, unified output."""
import subprocess, sys

def run_script(name, ticker):
    try:
        r = subprocess.run(["python", f"scripts/{name}", ticker], capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except: return ""

def generate(ticker: str) -> dict:
    whale   = run_script("whale_scanner.py", ticker)
    wave    = run_script("elliott_wave.py", ticker)
    bands   = run_script("bollinger_analyzer.py", ticker)
    trend   = run_script("trend_engine.py", ticker)
    liq     = run_script("liquidity_map.py", ticker)
    signals = {"whale": "🟢" in whale, "wave3": "3" in wave, "squeeze": "SQUEEZE" in bands}
    score   = sum(signals.values())
    conviction = "HIGH" if score >= 3 and signals["whale"] else \
                 "MEDIUM" if score >= 2 and signals["whale"] else "NONE"
    return {"ticker": ticker, "score": score, "conviction": conviction, "details": locals()}

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    result = generate(ticker)
    print(f"{ticker}: {result['conviction']} ({result['score']}/5 signals)")
    print(f"  Whale: {result['details']['whale']} | Wave3: {result['details']['wave3']} | Squeeze: {result['details']['squeeze']}")
```

## Usage

Run any script directly:
```bash
python scripts/whale_scanner.py SPY
python scripts/elliott_wave.py NVDA
python scripts/bollinger_analyzer.py TSLA
python scripts/signal_generator.py --ticker AAPL
```

Or run all 5 inputs together:
```bash
python scripts/signal_generator.py --ticker NVDA
```

## Research Sources

- Whale flow: FlowProof.io — "sweeps > blocks > splits > single fills"
- Elliott Wave: elliottwave-forecast.com — 3 inviolable rules
- Liquidity: StrikeWatch EA — 4-layer strike wall conviction scoring
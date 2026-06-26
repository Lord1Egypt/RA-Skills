#!/usr/bin/env python3
"""
NEPSE Analyst Script for OpenClaw
Fetches data from Merolagani, calculates technical indicators, manages watchlist/alerts.
Usage: python3 nepse_fetch.py <command> [args]
"""

import sys
import json
import os
import re
import time
import math
from datetime import datetime
from pathlib import Path

# ── optional deps with friendly error ──────────────────────────────────────
try:
    import requests
    from bs4 import BeautifulSoup
    import numpy as np
except ImportError as e:
    print(json.dumps({"error": f"Missing dependency: {e}. Run: pip3 install requests beautifulsoup4 numpy --break-system-packages"}))
    sys.exit(1)

# ── config ──────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

WATCHLIST_FILE = DATA_DIR / "watchlist.json"
ALERTS_FILE    = DATA_DIR / "alerts.json"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

# ── helpers ─────────────────────────────────────────────────────────────────

def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2))

def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

# ── indicators ──────────────────────────────────────────────────────────────
# Adaptive indicators that work with whatever data is available

def adaptive_ema(prices: list, period: int) -> list:
    """
    Adaptive EMA - uses min(period, len(prices)-1) to compute with available data.
    Returns EMA values or None if insufficient data.
    """
    n = len(prices)
    if n < 2:
        return [None] * n

    # Use whatever period is possible
    effective_period = min(period, n - 1)
    if effective_period < 1:
        return [None] * n

    k = 2.0 / (effective_period + 1)
    result = [None] * (effective_period - 1) if effective_period > 1 else []

    # First EMA is SMA of available period
    sma_period = min(effective_period, n)
    result.append(sum(prices[:sma_period]) / sma_period)

    for p in prices[sma_period:]:
        result.append(p * k + result[-1] * (1 - k))

    # Pad with None if we couldn't compute for early positions
    while len(result) < n:
        result.insert(0, None)

    return result

def ema(prices: list, period: int) -> list:
    """Legacy EMA - kept for backwards compatibility. Use adaptive_ema for new code."""
    return adaptive_ema(prices, period)

def adaptive_rsi(prices: list, period: int = 14) -> float | None:
    """
    Adaptive RSI - uses min(period, len(prices)-1) to compute with available data.
    For very short data (e.g., 5 days), computes a shorter-period RSI.
    """
    n = len(prices)
    if n < 3:  # Need at least 3 points for any meaningful RSI
        return None

    # Use whatever period is possible (minimum 2)
    effective_period = min(period, n - 1)
    effective_period = max(effective_period, 2)

    deltas = [prices[i+1] - prices[i] for i in range(n-1)]
    gains = [max(d, 0) for d in deltas[-effective_period:]]
    losses = [abs(min(d, 0)) for d in deltas[-effective_period:]]

    avg_gain = sum(gains) / effective_period
    avg_loss = sum(losses) / effective_period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def rsi(prices: list, period: int = 14) -> float | None:
    """Legacy RSI - kept for backwards compatibility. Use adaptive_rsi for new code."""
    return adaptive_rsi(prices, period)

def stoch_rsi(prices: list, rsi_period: int = 14, stoch_period: int = 14) -> float | None:
    """
    Adaptive Stochastic RSI - adjusts periods based on available data.
    """
    n = len(prices)
    if n < 6:  # Need minimum data for meaningful StochRSI
        return None

    # Adapt periods to available data
    effective_rsi_period = min(rsi_period, max(2, n // 3))
    effective_stoch_period = min(stoch_period, max(2, n // 3))

    rsi_values = []
    for i in range(effective_stoch_period, n):
        start_idx = max(0, i - effective_rsi_period - effective_stoch_period)
        r = adaptive_rsi(prices[start_idx:i+1], effective_rsi_period)
        if r is not None:
            rsi_values.append(r)

    if len(rsi_values) < effective_stoch_period:
        return None

    window = rsi_values[-effective_stoch_period:]
    low_rsi = min(window)
    high_rsi = max(window)

    if high_rsi == low_rsi:
        return 50.0

    return round((window[-1] - low_rsi) / (high_rsi - low_rsi) * 100, 2)

def adaptive_adx(highs: list, lows: list, closes: list, period: int = 14) -> float | None:
    """
    Adaptive ADX - uses min(period, len(closes)//2) to compute with available data.
    Requires at least 6 data points for meaningful calculation.
    """
    n = len(closes)
    if n < 6 or not highs or not lows:
        return None

    # Adapt period to available data (minimum 3, maximum available/2)
    effective_period = min(period, max(3, n // 2))

    tr_list, plus_dm, minus_dm = [], [], []
    for i in range(1, n):
        h, l, pc = highs[i], lows[i], closes[i-1]
        tr_list.append(max(h - l, abs(h - pc), abs(l - pc)))
        up_move = highs[i] - highs[i-1]
        down_move = lows[i-1] - lows[i]
        plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0)
        minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0)

    def smooth(lst, p):
        s = [sum(lst[:p])]
        for v in lst[p:]:
            s.append(s[-1] - s[-1]/p + v)
        return s

    atr = smooth(tr_list, effective_period)
    pdi_raw = smooth(plus_dm, effective_period)
    mdi_raw = smooth(minus_dm, effective_period)

    dx_list = []
    for i in range(len(atr)):
        if atr[i] == 0:
            continue
        pdi = 100 * pdi_raw[i] / atr[i]
        mdi = 100 * mdi_raw[i] / atr[i]
        if pdi + mdi == 0:
            continue
        dx_list.append(100 * abs(pdi - mdi) / (pdi + mdi))

    if len(dx_list) < effective_period:
        return None

    return round(sum(dx_list[-effective_period:]) / effective_period, 2)

def adx(highs: list, lows: list, closes: list, period: int = 14) -> float | None:
    """Legacy ADX - kept for backwards compatibility. Use adaptive_adx for new code."""
    return adaptive_adx(highs, lows, closes, period)

def obv(closes: list, volumes: list) -> dict:
    """
    On-Balance Volume - works with any data length >= 2.
    """
    if len(closes) < 2 or not volumes:
        return {"trend": "unknown", "value": 0, "note": "insufficient data"}

    obv_val = 0
    obv_series = []

    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]:
            obv_val += volumes[i] if i < len(volumes) else 0
        elif closes[i] < closes[i-1]:
            obv_val -= volumes[i] if i < len(volumes) else 0
        obv_series.append(obv_val)

    # Adapt lookback to available data
    lookback = min(5, len(obv_series)) if obv_series else 0

    if lookback < 2:
        return {"trend": "unknown", "value": obv_val, "note": "insufficient data for trend"}

    recent = obv_series[-lookback:]
    trend = "rising" if recent[-1] > recent[0] else "falling"
    return {"trend": trend, "value": obv_val}

def adaptive_support_resistance(closes: list, window: int = 20) -> dict:
    """
    Adaptive Support/Resistance - uses min(window, len(closes)) for available data.
    """
    n = len(closes)
    if n < 3:
        return {"support": None, "resistance": None, "note": "insufficient data"}

    # Adapt window to available data (minimum 3)
    effective_window = min(window, max(3, n))
    recent = closes[-effective_window:]

    return {
        "support": round(min(recent), 2),
        "resistance": round(max(recent), 2),
        "window_used": effective_window
    }

def support_resistance(closes: list, window: int = 20) -> dict:
    """Legacy support/resistance - kept for backwards compatibility."""
    return adaptive_support_resistance(closes, window)

def adaptive_volume_signal(volumes: list) -> dict:
    """
    Adaptive Volume Signal - uses min(10, len(volumes)-1) for average calculation.
    Works with as few as 2 volume data points.
    """
    n = len(volumes)
    if n < 2:
        return {"avg": 0, "current": 0, "ratio": 0, "signal": "insufficient data", "note": "need at least 2 data points"}

    current = volumes[-1]

    # Adapt average period to available data
    avg_period = min(10, n - 1)
    avg_period = max(avg_period, 1)

    # Calculate average of previous period (excluding current day)
    start_idx = max(0, n - 1 - avg_period)
    avg_volume = sum(volumes[start_idx:n-1]) / (n - 1 - start_idx) if (n - 1 - start_idx) > 0 else current

    ratio = round(current / avg_volume, 2) if avg_volume > 0 else 1.0

    # Adjust thresholds for shorter data windows
    if n < 10:
        # More lenient thresholds for new stocks
        signal = "high volume" if ratio >= 1.3 else "low volume" if ratio < 0.8 else "average volume"
        note = f"based on {n-1}-day average (new stock)"
    else:
        signal = "high volume" if ratio >= 1.5 else "low volume" if ratio < 0.7 else "average volume"
        note = None

    return {
        "avg": round(avg_volume),
        "current": current,
        "ratio": ratio,
        "signal": signal,
        "note": note
    }

def volume_signal(volumes: list) -> dict:
    """Legacy volume signal - kept for backwards compatibility. Use adaptive_volume_signal."""
    return adaptive_volume_signal(volumes)

# ── scraper ─────────────────────────────────────────────────────────────────

def parse_nepali_number(text: str) -> float | None:
    """
    Parse Nepali number formats (e.g., '1.23 Cr.', '456.78 Lakhs', '1,234.56').
    Returns float value or None if parsing fails.
    """
    if not text:
        return None

    text = text.strip().upper()

    # Remove common suffixes and get multiplier
    multiplier = 1.0
    if "CR" in text or "CRORE" in text:
        multiplier = 10000000  # 1 Crore = 10 million
        text = re.sub(r"CR(ORe)?\.?", "", text, flags=re.I)
    elif "LAKH" in text or "LAC" in text:
        multiplier = 100000  # 1 Lakh = 100 thousand
        text = re.sub(r"LAKH(S)?|LAC(S)?", "", text, flags=re.I)

    # Remove commas and other non-numeric chars except decimal/minus
    text = re.sub(r"[^\d.\-]", "", text)

    try:
        return float(text) * multiplier
    except Exception:
        return None

def fetch_merolagani(symbol: str) -> dict:
    """
    Scrape stock data from Merolagani.
    Enhanced to pull: Market Cap, Book Value, Dividend Yield, Sector, Paid-up Capital.
    """
    symbol = symbol.upper()
    url = f"https://merolagani.com/CompanyDetail.aspx?symbol={symbol}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # current price
        price_tag = soup.find("span", {"id": re.compile(r".*lblMarketPrice.*", re.I)})
        if not price_tag:
            price_tag = soup.find("strong", class_=re.compile(r"rate", re.I))
        current_price = float(re.sub(r"[^\d.]", "", price_tag.text)) if price_tag else None

        # change
        change_tag = soup.find("span", {"id": re.compile(r".*lblChange.*", re.I)})
        change = change_tag.text.strip() if change_tag else "N/A"

        # 52W high/low
        high52_tag = soup.find("span", {"id": re.compile(r".*lbl52WeekHigh.*", re.I)})
        low52_tag  = soup.find("span", {"id": re.compile(r".*lbl52WeekLow.*", re.I)})
        high52 = float(re.sub(r"[^\d.]", "", high52_tag.text)) if high52_tag else None
        low52  = float(re.sub(r"[^\d.]", "", low52_tag.text))  if low52_tag  else None

        # EPS / PE / book value
        eps_tag = soup.find("td", string=re.compile(r"EPS", re.I))
        eps = None
        if eps_tag and eps_tag.find_next_sibling("td"):
            try:
                eps = float(re.sub(r"[^\d.\-]", "", eps_tag.find_next_sibling("td").text))
            except Exception:
                pass

        pe_tag = soup.find("td", string=re.compile(r"P/E", re.I))
        pe = None
        if pe_tag and pe_tag.find_next_sibling("td"):
            try:
                pe = float(re.sub(r"[^\d.\-]", "", pe_tag.find_next_sibling("td").text))
            except Exception:
                pass

        # Enhanced fundamental data extraction
        # Look for fundamental data in various possible locations
        fundamentals = {}

        # Market Cap - search for label containing "Market Cap" or "Capitalization"
        mcap_label = soup.find("td", string=re.compile(r"Market\s*Cap", re.I))
        if not mcap_label:
            mcap_label = soup.find("td", string=re.compile(r"Capitalization", re.I))
        if mcap_label and mcap_label.find_next_sibling("td"):
            fundamentals["market_cap"] = parse_nepali_number(mcap_label.find_next_sibling("td").text)

        # Book Value per share
        bv_tag = soup.find("td", string=re.compile(r"Book\s*Value", re.I))
        if bv_tag and bv_tag.find_next_sibling("td"):
            try:
                fundamentals["book_value"] = float(re.sub(r"[^\d.\-]", "", bv_tag.find_next_sibling("td").text))
            except Exception:
                pass

        # Dividend Yield
        div_yield_tag = soup.find("td", string=re.compile(r"Dividend\s*Yield", re.I))
        if div_yield_tag and div_yield_tag.find_next_sibling("td"):
            try:
                fundamentals["dividend_yield"] = float(re.sub(r"[^\d.\-]", "", div_yield_tag.find_next_sibling("td").text))
            except Exception:
                pass

        # Sector
        sector_tag = soup.find("td", string=re.compile(r"Sector", re.I))
        if sector_tag and sector_tag.find_next_sibling("td"):
            fundamentals["sector"] = sector_tag.find_next_sibling("td").text.strip()

        # Paid-up Capital
        paidup_tag = soup.find("td", string=re.compile(r"Paid[-\s]Up\s*Capital", re.I))
        if not paidup_tag:
            paidup_tag = soup.find("td", string=re.compile(r"Paid\s*Up", re.I))
        if paidup_tag and paidup_tag.find_next_sibling("td"):
            fundamentals["paid_up_capital"] = parse_nepali_number(paidup_tag.find_next_sibling("td").text)

        # Additional fundamentals if available
        # Face Value
        face_tag = soup.find("td", string=re.compile(r"Face\s*Value", re.I))
        if face_tag and face_tag.find_next_sibling("td"):
            try:
                fundamentals["face_value"] = float(re.sub(r"[^\d.\-]", "", face_tag.find_next_sibling("td").text))
            except Exception:
                pass

        # P/E Ratio (already have, but also add to fundamentals)
        if pe is not None:
            fundamentals["pe_ratio"] = pe

        # EPS (already have, but also add to fundamentals)
        if eps is not None:
            fundamentals["eps"] = eps

        # historical price table — scrape closes, highs, lows, volumes
        closes, highs, lows, volumes = [], [], [], []
        table = soup.find("table", {"id": re.compile(r".*gridHistory.*", re.I)})
        if table:
            for row in table.find_all("tr")[1:51]:  # last 50 rows
                cols = row.find_all("td")
                if len(cols) >= 6:
                    try:
                        closes.append(float(re.sub(r"[^\d.]", "", cols[1].text)))
                        highs.append(float(re.sub(r"[^\d.]", "", cols[2].text)))
                        lows.append(float(re.sub(r"[^\d.]", "", cols[3].text)))
                        volumes.append(int(re.sub(r"[^\d]", "", cols[5].text) or "0"))
                    except Exception:
                        continue

        # prepend current price to series
        if current_price:
            closes.insert(0, current_price)
            if highs:
                highs.insert(0, highs[0])
                lows.insert(0, lows[0])
            if volumes:
                volumes.insert(0, volumes[0])

        return {
            "symbol": symbol,
            "price": current_price,
            "change": change,
            "high_52w": high52,
            "low_52w": low52,
            "eps": eps,
            "pe": pe,
            "fundamentals": fundamentals,  # Enhanced fundamental data
            "closes": list(reversed(closes)),
            "highs": list(reversed(highs)),
            "lows": list(reversed(lows)),
            "volumes": list(reversed(volumes)),
            "source": "merolagani",
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}

def fetch_sharesansar_fallback(symbol: str) -> dict:
    """Fallback: fetch basic price from Sharesansar."""
    symbol = symbol.upper()
    url = f"https://www.sharesansar.com/company/{symbol.lower()}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        price_tag = soup.find("strong", class_=re.compile(r"ltp|price", re.I))
        price = float(re.sub(r"[^\d.]", "", price_tag.text)) if price_tag else None
        return {
            "symbol": symbol,
            "price": price,
            "change": "N/A",
            "source": "sharesansar",
            "closes": [price] if price else [],
            "highs": [], "lows": [], "volumes": [],
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}

def get_stock_data(symbol: str) -> dict:
    data = fetch_merolagani(symbol)
    if "error" in data or not data.get("price"):
        data = fetch_sharesansar_fallback(symbol)
    return data

# ── commands ─────────────────────────────────────────────────────────────────

def cmd_price(symbol: str):
    data = get_stock_data(symbol)
    if "error" in data:
        print(json.dumps({"error": data["error"], "symbol": symbol}))
        return
    print(json.dumps({
        "symbol": data["symbol"],
        "price": data["price"],
        "change": data["change"],
        "high_52w": data.get("high_52w"),
        "low_52w": data.get("low_52w"),
        "source": data.get("source"),
        "fetched_at": data.get("fetched_at")
    }))

def cmd_analyze(symbol: str):
    data = get_stock_data(symbol)
    if "error" in data:
        print(json.dumps({"error": data["error"], "symbol": symbol}))
        return

    closes  = data.get("closes", [])
    highs   = data.get("highs", [])
    lows    = data.get("lows", [])
    volumes = data.get("volumes", [])

    n = len(closes)

    # Handle extremely limited data
    if n < 3:
        print(json.dumps({
            "symbol": data["symbol"],
            "price": data.get("price"),
            "change": data.get("change"),
            "high_52w": data.get("high_52w"),
            "low_52w": data.get("low_52w"),
            "fundamentals": data.get("fundamentals", {}),
            "error": "too_little_data",
            "data_points": n,
            "note": "Need at least 3 data points for technical analysis. Only price data available.",
            "source": data.get("source"),
            "fetched_at": data.get("fetched_at"),
            "disclaimer": "Analysis only. NEPSE is volatile — manage your risk."
        }))
        return

    # Use adaptive indicators that work with available data
    ema20  = adaptive_ema(closes, 20)
    ema50  = adaptive_ema(closes, 50)
    ema200 = adaptive_ema(closes, 200)
    rsi14  = adaptive_rsi(closes, 14)
    srsi   = stoch_rsi(closes)
    adx14  = adaptive_adx(highs, lows, closes, 14) if highs and lows else None
    obv_r  = obv(closes, volumes) if volumes else {"trend": "no data"}
    sr     = adaptive_support_resistance(closes)
    vol_s  = adaptive_volume_signal(volumes) if volumes else {"signal": "no volume data"}

    # EMA alignment
    curr_ema20  = next((v for v in reversed(ema20)  if v), None)
    curr_ema50  = next((v for v in reversed(ema50)  if v), None)
    curr_ema200 = next((v for v in reversed(ema200) if v), None)
    price = data["price"]

    # Data quality notes for limited data scenarios
    data_notes = []
    if n < 20:
        data_notes.append(f"New stock: only {n} days of data available")
    if n < 50:
        data_notes.append("EMA50 may be unreliable with limited data")
    if n < 200:
        data_notes.append("EMA200 computed on available data (full 200 days not available)")

    ema_signal = "neutral"
    if price and curr_ema20 and curr_ema50 and curr_ema200:
        if price > curr_ema20 > curr_ema50 > curr_ema200:
            ema_signal = "strong_bullish"
        elif price > curr_ema20 > curr_ema50:
            ema_signal = "bullish"
        elif price < curr_ema20 < curr_ema50 < curr_ema200:
            ema_signal = "strong_bearish"
        elif price < curr_ema20 < curr_ema50:
            ema_signal = "bearish"
    elif price and curr_ema20 and curr_ema50:
        # Partial alignment (no EMA200 yet)
        if price > curr_ema20 > curr_ema50:
            ema_signal = "bullish (short-term)"
            data_notes.append("EMA200 not available yet - using short-term EMAs only")
        elif price < curr_ema20 < curr_ema50:
            ema_signal = "bearish (short-term)"
            data_notes.append("EMA200 not available yet - using short-term EMAs only")

    # ADX interpretation
    trend_strength = "no data"
    if adx14 is not None:
        if adx14 >= 25:
            trend_strength = "strong trend"
        elif adx14 >= 20:
            trend_strength = "developing trend"
        else:
            trend_strength = "choppy/sideways — avoid trading on technicals alone"
    elif n < 10:
        trend_strength = "insufficient data for ADX (need 10+ days)"
        data_notes.append("ADX not available - insufficient data")

    # RSI signal (NEPSE adjusted: 60/40)
    rsi_signal = "neutral"
    if rsi14 is not None:
        if rsi14 >= 60:
            rsi_signal = "overbought (NEPSE)"
        elif rsi14 <= 40:
            rsi_signal = "oversold (NEPSE)"
    elif n < 5:
        rsi_signal = "insufficient data"
        data_notes.append("RSI computed on limited data - interpret with caution")

    # confluence score
    bull_signals, bear_signals = 0, 0
    if ema_signal in ("bullish", "strong_bullish", "bullish (short-term)"):
        bull_signals += 1
    elif ema_signal in ("bearish", "strong_bearish", "bearish (short-term)"):
        bear_signals += 1
    if rsi_signal == "oversold (NEPSE)":
        bull_signals += 1
    elif rsi_signal == "overbought (NEPSE)":
        bear_signals += 1
    if obv_r.get("trend") == "rising":
        bull_signals += 1
    elif obv_r.get("trend") == "falling":
        bear_signals += 1
    if vol_s.get("ratio", 0) >= 1.3:  # Lowered threshold for new stocks
        bull_signals += 1  # high volume confirms move

    if bull_signals >= 3:
        confluence = "BULLISH CONFLUENCE"
    elif bear_signals >= 3:
        confluence = "BEARISH CONFLUENCE"
    elif bull_signals > bear_signals:
        confluence = "Mild Bullish"
    elif bear_signals > bull_signals:
        confluence = "Mild Bearish"
    else:
        confluence = "Neutral / Mixed"

    print(json.dumps({
        "symbol": data["symbol"],
        "price": price,
        "change": data.get("change"),
        "high_52w": data.get("high_52w"),
        "low_52w": data.get("low_52w"),
        "fundamentals": data.get("fundamentals", {}),
        "indicators": {
            "ema20": round(curr_ema20, 2) if curr_ema20 else None,
            "ema50": round(curr_ema50, 2) if curr_ema50 else None,
            "ema200": round(curr_ema200, 2) if curr_ema200 else None,
            "ema_signal": ema_signal,
            "rsi14": rsi14,
            "rsi_signal": rsi_signal,
            "stoch_rsi": srsi,
            "adx": adx14,
            "trend_strength": trend_strength,
            "obv": obv_r,
            "volume": vol_s,
            "support": sr.get("support"),
            "resistance": sr.get("resistance")
        },
        "confluence": confluence,
        "bull_signals": bull_signals,
        "bear_signals": bear_signals,
        "data_points": n,
        "data_notes": data_notes if data_notes else None,
        "source": data.get("source"),
        "fetched_at": data.get("fetched_at"),
        "disclaimer": "Analysis only. NEPSE is volatile — manage your risk."
    }))

def cmd_watchlist(action: str, symbol: str = None):
    wl = load_json(WATCHLIST_FILE, [])
    if action == "show":
        print(json.dumps({"watchlist": wl}))
    elif action == "add" and symbol:
        symbol = symbol.upper()
        if symbol not in wl:
            wl.append(symbol)
            save_json(WATCHLIST_FILE, wl)
            print(json.dumps({"status": "added", "symbol": symbol, "watchlist": wl}))
        else:
            print(json.dumps({"status": "already_exists", "symbol": symbol, "watchlist": wl}))
    elif action == "remove" and symbol:
        symbol = symbol.upper()
        if symbol in wl:
            wl.remove(symbol)
            save_json(WATCHLIST_FILE, wl)
            print(json.dumps({"status": "removed", "symbol": symbol, "watchlist": wl}))
        else:
            print(json.dumps({"status": "not_found", "symbol": symbol}))
    else:
        print(json.dumps({"error": "Unknown watchlist action"}))

def cmd_alert(action: str, symbol: str = None, price: float = None, direction: str = None):
    alerts = load_json(ALERTS_FILE, {})
    if action == "set" and symbol and price and direction:
        symbol = symbol.upper()
        direction = direction.lower()
        if direction not in ("above", "below"):
            print(json.dumps({"error": "direction must be 'above' or 'below'"}))
            return
        alerts[symbol] = {"price": price, "direction": direction, "created": datetime.now().isoformat()}
        save_json(ALERTS_FILE, alerts)
        print(json.dumps({
            "status": "alert_set",
            "symbol": symbol,
            "trigger": f"Alert when {symbol} goes {direction} Rs. {price}"
        }))
    elif action == "list":
        print(json.dumps({"alerts": alerts}))
    elif action == "clear" and symbol:
        symbol = symbol.upper()
        if symbol in alerts:
            del alerts[symbol]
            save_json(ALERTS_FILE, alerts)
            print(json.dumps({"status": "cleared", "symbol": symbol}))
        else:
            print(json.dumps({"status": "not_found", "symbol": symbol}))
    else:
        print(json.dumps({"error": "Usage: alert set SYMBOL PRICE above|below  OR  alert list  OR  alert clear SYMBOL"}))

def cmd_market():
    """Fetch top gainers/losers from Merolagani market summary."""
    url = "https://merolagani.com/MarketSummary.aspx"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        gainers, losers = [], []

        gainer_table = soup.find("table", {"id": re.compile(r".*gainer.*", re.I)})
        if gainer_table:
            for row in gainer_table.find_all("tr")[1:6]:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    gainers.append({"symbol": cols[0].text.strip(), "price": cols[1].text.strip(), "change": cols[2].text.strip()})

        loser_table = soup.find("table", {"id": re.compile(r".*loser.*", re.I)})
        if loser_table:
            for row in loser_table.find_all("tr")[1:6]:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    losers.append({"symbol": cols[0].text.strip(), "price": cols[1].text.strip(), "change": cols[2].text.strip()})

        print(json.dumps({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "top_gainers": gainers,
            "top_losers": losers,
            "source": "merolagani"
        }))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_cron_check():
    """Check all alerts and watchlist — called by cron job. Sends Telegram alerts."""
    alerts = load_json(ALERTS_FILE, {})
    watchlist = load_json(WATCHLIST_FILE, [])
    triggered = []
    summary_lines = [f"📊 *NEPSE Daily Check* — {datetime.now().strftime('%Y-%m-%d %H:%M')}"]

    # check watchlist prices
    if watchlist:
        summary_lines.append("\n*📋 Watchlist:*")
        for symbol in watchlist:
            data = get_stock_data(symbol)
            if data.get("price"):
                change = data.get("change", "")
                summary_lines.append(f"• {symbol}: Rs. {data['price']} {change}")
            time.sleep(1)  # polite delay between requests

    # check alerts
    for symbol, alert in list(alerts.items()):
        data = get_stock_data(symbol)
        current = data.get("price")
        if not current:
            continue
        threshold = alert["price"]
        direction = alert["direction"]
        hit = (direction == "above" and current >= threshold) or \
              (direction == "below" and current <= threshold)
        if hit:
            triggered.append(symbol)
            msg = f"🚨 *ALERT TRIGGERED*\n{symbol} is now Rs. {current} ({direction} Rs. {threshold})"
            send_telegram(msg)
            summary_lines.append(f"\n🚨 ALERT: {symbol} = Rs. {current} (trigger: {direction} Rs. {threshold})")
        time.sleep(1)

    # send daily summary
    full_summary = "\n".join(summary_lines)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram(full_summary)

    print(json.dumps({
        "status": "cron_done",
        "watchlist_checked": watchlist,
        "alerts_triggered": triggered,
        "telegram_sent": bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
        "time": datetime.now().isoformat()
    }))

# ── main ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "No command given. Use: price|analyze|watchlist|alert|market|cron-check"}))
        sys.exit(1)

    cmd = args[0].lower()

    if cmd == "price":
        if len(args) < 2:
            print(json.dumps({"error": "Usage: price SYMBOL"}))
        else:
            cmd_price(args[1].upper())

    elif cmd == "analyze":
        if len(args) < 2:
            print(json.dumps({"error": "Usage: analyze SYMBOL"}))
        else:
            cmd_analyze(args[1].upper())

    elif cmd == "watchlist":
        action = args[1] if len(args) > 1 else "show"
        symbol = args[2].upper() if len(args) > 2 else None
        cmd_watchlist(action, symbol)

    elif cmd == "alert":
        action = args[1] if len(args) > 1 else "list"
        symbol = args[2].upper() if len(args) > 2 else None
        price  = float(args[3]) if len(args) > 3 else None
        direction = args[4].lower() if len(args) > 4 else None
        cmd_alert(action, symbol, price, direction)

    elif cmd == "market":
        cmd_market()

    elif cmd == "cron-check":
        cmd_cron_check()

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}. Use: price|analyze|watchlist|alert|market|cron-check"}))
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Advanced Technical Analysis Module
Multi-timeframe analysis, indicators, and signal generation
"""

import os
import json
import time
import hmac
import hashlib
import requests
from typing import Dict, List, Optional, Tuple

# Load env
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k] = v

API_KEY = os.environ.get('BINANCE_API_KEY', '')
SECRET = os.environ.get('BINANCE_SECRET', '')

def get_sig(params):
    return hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

def retry_api_call(func, max_retries=3, delay=1):
    """Retry API call with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))
                continue
            return {'error': str(e)}
    return {'error': 'Max retries exceeded'}

def get_klines(symbol: str, interval: str = '1h', limit: int = 100) -> List:
    """Fetch klines/candlestick data with retry"""
    def _fetch():
        ts = int(time.time() * 1000)
        url = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}'
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
    
    result = retry_api_call(_fetch)
    if 'error' in result:
        return []
    return result

def get_24h_ticker(symbol: str) -> Dict:
    """Get 24h ticker with retry"""
    def _fetch():
        ts = int(time.time() * 1000)
        params = f'symbol={symbol}&timestamp={ts}'
        sig = get_sig(params)
        url = f'https://fapi.binance.com/fapi/v2/positionRisk?{params}&signature={sig}'
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.json()
    
    return retry_api_call(_fetch)

def calculate_sma(prices: List[float], period: int) -> Optional[float]:
    """Simple Moving Average"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def calculate_ema(prices: List[float], period: int) -> Optional[float]:
    """Exponential Moving Average"""
    if len(prices) < period:
        return None
    mul = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for p in prices[period:]:
        ema = (p - ema) * mul + ema
    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    """RSI - Relative Strength Index"""
    if len(prices) < period + 1:
        return None
    
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [c if c > 0 else 0 for c in changes[-period:]]
    losses = [-c if c < 0 else 0 for c in changes[-period:]]
    
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """MACD - returns (macd_line, signal_line, histogram)"""
    if len(prices) < slow + signal:
        return None, None, None
    
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    if ema_fast is None or ema_slow is None:
        return None, None, None
    
    macd_line = ema_fast - ema_slow
    
    # Calculate signal line (EMA of MACD)
    # Simplified - just return macd for now
    signal_line = macd_line * 0.9  # approximation
    
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Bollinger Bands - returns (upper, middle, lower)"""
    if len(prices) < period:
        return None, None, None
    
    sma = calculate_sma(prices, period)
    if sma is None:
        return None, None, None
    
    variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
    std = variance ** 0.5
    
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    
    return upper, sma, lower

def calculate_vwap(klines: List) -> Optional[float]:
    """VWAP - Volume Weighted Average Price"""
    if len(klines) < 2:
        return None
    
    total_pv = 0
    total_vol = 0
    
    for candle in klines[-20:]:  # Use last 20 candles
        high = float(candle[2])
        low = float(candle[3])
        close = float(candle[4])
        volume = float(candle[5])
        
        typical_price = (high + low + close) / 3
        total_pv += typical_price * volume
        total_vol += volume
    
    if total_vol == 0:
        return None
    
    return total_pv / total_vol

def calculate_atr(klines: List, period: int = 14) -> Optional[float]:
    """ATR - Average True Range"""
    if len(klines) < period + 1:
        return None
    
    trs = []
    for i in range(1, min(period + 1, len(klines))):
        high = float(klines[-i][2])
        low = float(klines[-i][3])
        prev_close = float(klines[-i-1][4])
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    
    return sum(trs) / len(trs) if trs else None

def detect_rsi_divergence(prices: List[float], period: int = 14) -> Optional[str]:
    """Detect RSI divergence (bullish/bearish)"""
    if len(prices) < period * 3:
        return None
    
    rsi_values = []
    for i in range(len(prices) - period):
        rsi = calculate_rsi(prices[i:i+period+1], period)
        if rsi:
            rsi_values.append(rsi)
    
    if len(rsi_values) < 5:
        return None
    
    # Check last 5 RSI values
    recent_rsi = rsi_values[-5:]
    recent_prices = prices[-6:]
    
    # Bullish: price making lower lows, RSI making higher lows
    if recent_prices[-1] < recent_prices[0] and recent_rsi[-1] > recent_rsi[0]:
        return 'bullish'
    
    # Bearish: price making higher highs, RSI making lower highs
    if recent_prices[-1] > recent_prices[0] and recent_rsi[-1] < recent_rsi[0]:
        return 'bearish'
    
    return None

def detect_bollinger_breakout(prices: List[float], current_price: float) -> Optional[str]:
    """Detect Bollinger Band breakout"""
    upper, middle, lower = calculate_bollinger_bands(prices)
    
    if upper is None:
        return None
    
    # Price above upper band = bullish breakout
    if current_price > upper:
        return 'bullish'
    
    # Price below lower band = bearish breakout
    if current_price < lower:
        return 'bearish'
    
    return None

def detect_volume_spike(klines: List, threshold: float = 2.0) -> bool:
    """Detect unusual volume spike"""
    if len(klines) < 20:
        return False
    
    volumes = [float(c[5]) for c in klines[-20:]]
    avg_volume = sum(volumes) / len(volumes)
    current_volume = volumes[-1]
    
    return current_volume > (avg_volume * threshold)

def detect_support_resistance(prices: List[float], window: int = 20) -> Tuple[float, float]:
    """Detect support and resistance levels"""
    if len(prices) < window:
        return min(prices), max(prices)
    
    recent = prices[-window:]
    return min(recent), max(recent)

def calculate_market_regime(prices: List[float], lookback: int = 50) -> str:
    """Detect market regime (bull/bear/sideways)"""
    if len(prices) < lookback:
        return 'unknown'
    
    recent = prices[-lookback:]
    
    # Calculate trend angle
    start_price = recent[0]
    end_price = recent[-1]
    change_pct = ((end_price - start_price) / start_price) * 100
    
    # Calculate volatility
    variance = sum((p - sum(recent)/len(recent))**2 for p in recent) / len(recent)
    volatility = (variance ** 0.5) / sum(recent) * len(recent)
    
    if change_pct > 5 and volatility < 3:
        return 'bull'
    elif change_pct < -5 and volatility < 3:
        return 'bear'
    elif volatility < 2:
        return 'sideways'
    
    return 'volatile'

def analyze_signal(symbol: str) -> Dict:
    """Comprehensive signal analysis"""
    klines_1h = get_klines(symbol, '1h', 100)
    klines_4h = get_klines(symbol, '4h', 100)
    klines_1d = get_klines(symbol, '1d', 50)
    
    if not klines_1h:
        return {'error': 'Failed to fetch data'}
    
    # Extract prices
    prices_1h = [float(c[4]) for c in klines_1h]  # close
    prices_4h = [float(c[4]) for c in klines_4h]
    prices_1d = [float(c[4]) for c in klines_1d]
    
    current_price = prices_1h[-1]
    
    # Calculate indicators
    rsi_1h = calculate_rsi(prices_1h)
    rsi_4h = calculate_rsi(prices_4h)
    rsi_1d = calculate_rsi(prices_1d)
    
    ema_21_1h = calculate_ema(prices_1h, 21)
    ema_50_1h = calculate_ema(prices_1h, 50)
    ema_200_1h = calculate_ema(prices_1h, 200)
    
    macd, signal, hist = calculate_macd(prices_1h)
    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(prices_1h)
    vwap = calculate_vwap(klines_1h)
    atr = calculate_atr(klines_1h)
    
    # Detect patterns
    rsi_div = detect_rsi_divergence(prices_1h)
    bb_breakout = detect_bollinger_breakout(prices_1h, current_price)
    volume_spike = detect_volume_spike(klines_1h)
    
    support, resistance = detect_support_resistance(prices_1h)
    regime = calculate_market_regime(prices_1h)
    
    # Calculate scores
    score = 0
    signals = []
    
    # RSI analysis
    if rsi_1h:
        if rsi_1h < 30:
            score += 2
            signals.append('RSI oversold')
        elif rsi_1h > 70:
            score -= 2
            signals.append('RSI overbought')
        elif 40 < rsi_1h < 60:
            score += 1
            signals.append('RSI neutral')
    
    # MACD analysis
    if macd and signal:
        if macd > signal:
            score += 2
            signals.append('MACD bullish')
        else:
            score -= 2
            signals.append('MACD bearish')
    
    if hist and hist > 0:
        score += 1
        signals.append('MACD histogram positive')
    
    # EMA alignment
    if ema_21_1h and ema_50_1h and ema_200_1h:
        if ema_21_1h > ema_50_1h > ema_200_1h:
            score += 3
            signals.append('Strong uptrend (EMA bullish alignment)')
        elif ema_21_1h < ema_50_1h < ema_200_1h:
            score -= 3
            signals.append('Strong downtrend (EMA bearish alignment)')
    
    # VWAP
    if vwap:
        if current_price > vwap:
            score += 2
            signals.append('Above VWAP (bullish)')
        else:
            score -= 2
            signals.append('Below VWAP (bearish)')
    
    # Bollinger breakout
    if bb_breakout == 'bullish':
        score += 2
        signals.append('Bollinger bullish breakout')
    elif bb_breakout == 'bearish':
        score -= 2
        signals.append('Bollinger bearish breakout')
    
    # RSI divergence
    if rsi_div == 'bullish':
        score += 3
        signals.append('RSI bullish divergence')
    elif rsi_div == 'bearish':
        score -= 3
        signals.append('RSI bearish divergence')
    
    # Volume
    if volume_spike:
        score += 2
        signals.append('Volume spike')
    
    # Trend following
    if ema_21_1h and current_price > ema_21_1h:
        score += 1
        signals.append('Above EMA 21')
    elif ema_21_1h and current_price < ema_21_1h:
        score -= 1
        signals.append('Below EMA 21')
    
    # Normalize score to 0-10
    normalized_score = max(0, min(10, (score + 10) * 0.5))
    
    return {
        'symbol': symbol,
        'price': current_price,
        'score': round(normalized_score, 1),
        'signals': signals,
        'indicators': {
            'rsi_1h': round(rsi_1h, 1) if rsi_1h else None,
            'rsi_4h': round(rsi_4h, 1) if rsi_4h else None,
            'rsi_1d': round(rsi_1d, 1) if rsi_1d else None,
            'ema_21': round(ema_21_1h, 6) if ema_21_1h else None,
            'ema_50': round(ema_50_1h, 6) if ema_50_1h else None,
            'macd': round(macd, 6) if macd else None,
            'vwap': round(vwap, 6) if vwap else None,
            'atr': round(atr, 6) if atr else None,
            'bb_upper': round(bb_upper, 6) if bb_upper else None,
            'bb_lower': round(bb_lower, 6) if bb_lower else None,
        },
        'patterns': {
            'rsi_divergence': rsi_div,
            'bb_breakout': bb_breakout,
            'volume_spike': volume_spike,
        },
        'levels': {
            'support': round(support, 6),
            'resistance': round(resistance, 6),
        },
        'regime': regime,
    }

if __name__ == '__main__':
    # Test
    result = analyze_signal('BTCUSDT')
    print(json.dumps(result, indent=2))

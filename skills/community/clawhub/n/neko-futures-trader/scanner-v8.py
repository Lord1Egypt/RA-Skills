#!/usr/bin/env python3
"""
import math
Simplified Scanner v8 - Aggressive momentum trading
"""

import os
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime
from signal_filter import filter_signal

# === LOAD FROM ENV FILE ===

# Import advanced modules
try:
    import advanced_analysis as aa
    import error_handling as eh
    ADVANCED_ANALYSIS_AVAILABLE = True
except ImportError as e:
    ADVANCED_ANALYSIS_AVAILABLE = False
    print(f"Warning: Advanced modules not available: {e}")

# Only load from the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

if env_file and os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# === LOAD CONFIG FROM config.py ===
try:
    from config import *
except ImportError:
    pass

# Load delisting blocklist
try:
    from delisting_monitor import is_token_blocked, get_blocklist, check_binance_delist_announcements
    DELISTING_CHECK = True
except ImportError:
    DELISTING_CHECK = False

# Default ATR multipliers if not loaded from config
try:
    ATR_MULTIPLIER_SL_HIGH
except NameError:
    ATR_MULTIPLIER_SL_HIGH = 2.0
try:
    ATR_MULTIPLIER_TP_HIGH
except NameError:
    ATR_MULTIPLIER_TP_HIGH = 4.0
try:
    ATR_MULTIPLIER_SL_NORMAL
except NameError:
    ATR_MULTIPLIER_SL_NORMAL = 1.5
try:
    ATR_MULTIPLIER_TP_NORMAL
except NameError:
    ATR_MULTIPLIER_TP_NORMAL = 3.0
try:
    ATR_MULTIPLIER_SL_LOW
except NameError:
    ATR_MULTIPLIER_SL_LOW = 1.0
try:
    ATR_MULTIPLIER_TP_LOW
except NameError:
    ATR_MULTIPLIER_TP_LOW = 2.5

# === CONFIG ===
API_KEY = os.environ.get('BINANCE_API_KEY', '')
SECRET = os.environ.get('BINANCE_SECRET', '')

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL = os.environ.get('TELEGRAM_CHANNEL', '')
BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', '')

LEVERAGE = 10

# === API HELPERS ===
def get_signature(params):
    return hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

def binance_get(url, params=None):
    if params:
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = get_signature('&'.join(f'{k}={v}' for k, v in params.items()))
    headers = {'X-MBX-APIKEY': API_KEY}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json()

def binance_post(url, params):
    params['timestamp'] = int(time.time() * 1000)
    params['signature'] = get_signature('&'.join(f'{k}={v}' for k, v in params.items()))
    headers = {'X-MBX-APIKEY': API_KEY}
    r = requests.post(url, data=params, headers=headers, timeout=15)
    return r.json()

# === GET DATA ===
def get_balance():
    """Return totalMarginBalance (includes unrealized PnL)"""
    ts = int(time.time() * 1000)
    params = "timestamp={}".format(ts)
    sig = get_signature(params)
    r = requests.get("https://fapi.binance.com/fapi/v3/account?{}&signature={}".format(params, sig),
                     headers={"X-MBX-APIKEY": API_KEY}, timeout=15)
    if r:
        try:
            return float(r.json().get('totalMarginBalance', 0))
        except:
            return 0

def get_positions():
    ts = int(time.time() * 1000)
    params = "timestamp={}".format(ts)
    sig = get_signature(params)
    r = requests.get("https://fapi.binance.com/fapi/v3/account?{}&signature={}".format(params, sig),
                     headers={"X-MBX-APIKEY": API_KEY}, timeout=15)
    if r:
        return [p for p in r.json().get('positions', []) if float(p.get('positionAmt', 0)) != 0]
    return []

def cleanup_cache():
    """Clean up old cache entries"""
    import time
    now = time.time()
    cutoff = 86400  # 24 hours
    
    # Clean .recently_closed
    try:
        with open('.recently_closed', 'r') as f:
            lines = f.readlines()
        valid = []
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                sym, ts = parts[0], int(parts[1])
                if now - ts < cutoff:
                    valid.append(line.strip())
        with open('.recently_closed', 'w') as f:
            for line in valid:
                f.write(line + '\n')
    except:
        pass
    
    # Clear .posted_signals to allow re-posts
    try:
        open('.posted_signals', 'w').close()
    except:
        pass

# Cleanup on startup
cleanup_cache()

def get_24h_tickers():
    return binance_get('https://fapi.binance.com/fapi/v1/ticker/24hr')

def get_open_interest(symbol):
    """Get current Open Interest for a symbol"""
    try:
        url = f'https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}'
        r = requests.get(url, timeout=10)
        data = r.json()
        return float(data.get('openInterest', 0))
    except:
        return 0

def get_oi_change(symbol, limit=5):
    """Get OI change over recent candles - returns percentage change"""
    try:
        url = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1h&limit={limit+1}'
        r = requests.get(url, timeout=10)
        candles = r.json()
        
        # Get OI for each hour
        oi_values = []
        for i in range(1, len(candles)):
            # Use volume as proxy for OI (not exact but related)
            vol = float(candles[i][5])  # volume
            oi_values.append(vol)
        
        if len(oi_values) < 2:
            return 0
        
        # Calculate change
        current = oi_values[-1]
        previous = sum(oi_values[:-1]) / len(oi_values[:-1])
        
        if previous == 0:
            return 0
        
        return ((current - previous) / previous) * 100
    except:
        return 0

def get_oi_history(symbol, period='1h', limit=24):
    """Get OI history - more accurate than volume proxy"""
    try:
        url = f'https://futures.binance.com/futures/data/openInterestHist?symbol={symbol.replace("USDT","")}&period={period}&limit={limit}'
        r = requests.get(url, timeout=10)
        data = r.json()
        if data and len(data) > 1:
            # Calculate OI change trend
            oi_values = [float(d['openInterest']) for d in data]
            current = oi_values[-1]
            previous = sum(oi_values[:-1]) / len(oi_values[:-1])
            if previous > 0:
                return {
                    'current': current,
                    'change_pct': ((current - previous) / previous) * 100,
                    'trend': 'up' if current > previous else 'down'
                }
        return {'current': 0, 'change_pct': 0, 'trend': 'neutral'}
    except:
        return {'current': 0, 'change_pct': 0, 'trend': 'neutral'}

def get_mark_price(symbol):
    """Get mark price for more accurate SL/TP"""
    try:
        url = f'https://fapi.binance.com/fapi/v1/markPrice?symbol={symbol}'
        r = requests.get(url, timeout=10)
        data = r.json()
        return float(data.get('markPrice', 0))
    except:
        return 0

def get_price_v2(symbol):
    """Get price using v2 endpoint - lower latency"""
    try:
        url = f'https://fapi.binance.com/fapi/v2/ticker/price?symbol={symbol}'
        r = requests.get(url, timeout=10)
        data = r.json()
        return float(data.get('price', 0))
    except:
        return 0

def get_klines(symbol, interval='1h', limit=100):
    url = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}'
    r = requests.get(url, timeout=15)
    return r.json()

def place_order_with_sl_tp(symbol, side, quantity, sl_price, tp_price):
    """Place market order FIRST, only add SL/TP if market order succeeds"""
    ts = int(time.time() * 1000)
    
    # First place the market order
    params = "symbol={}&side={}&type=MARKET&quantity={}&timestamp={}".format(symbol, side, quantity, ts)
    sig = get_signature(params)
    url = "https://fapi.binance.com/fapi/v1/order?{}&signature={}".format(params, sig)
    headers = {'X-MBX-APIKEY': API_KEY}
    r = requests.post(url, headers=headers, timeout=15)
    result = r.json()
    
    # Only place SL/TP if market order succeeded
    order_id = result.get('orderId')
    if not order_id or str(order_id) == 'N/A':
        return result  # Return early - market order failed, no SL/TP
    
    # OCO Orders - place both SL and TP simultaneously
    if sl_price and tp_price:
        # Get current price
        r = requests.get(f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}', timeout=10)
        current_price = float(r.json()['price'])
        
        # Calculate working prices (trigger prices)
        if side == "BUY":  # LONG
            # SL triggers when price falls
            sl_trigger = sl_price
            sl_working = sl_price * 0.99
            # TP triggers when price rises  
            tp_trigger = tp_price
            tp_working = tp_price * 1.01
        else:  # SHORT
            sl_trigger = sl_price
            sl_working = sl_price * 1.01
            tp_trigger = tp_price
            tp_working = tp_price * 0.99
        
        # Place STOP Loss order
        sl_side = "SELL" if side == "BUY" else "BUY"
        sl_params = "symbol={}&side={}&type=STOP_MARKET&stopPrice={}&workingType=CONTRACT_PRICE&closePosition=true&timestamp={}".format(
            symbol, sl_side, round(sl_trigger, 6), int(time.time() * 1000))
        sl_sig = get_signature(sl_params)
        sl_url = "https://fapi.binance.com/fapi/v1/order?{}&signature={}".format(sl_params, sl_sig)
        sl_r = requests.post(sl_url, headers=headers, timeout=10)
        if sl_r.status_code != 200:
            print(f"  ⚠️ SL order failed: {sl_r.text[:100]}")
        
        # Place TAKE PROFIT order
        tp_side = "SELL" if side == "BUY" else "BUY"
        tp_params = "symbol={}&side={}&type=TAKE_PROFIT_MARKET&stopPrice={}&workingType=CONTRACT_PRICE&closePosition=true&timestamp={}".format(
            symbol, tp_side, round(tp_trigger, 6), int(time.time() * 1000))
        tp_sig = get_signature(tp_params)
        tp_url = "https://fapi.binance.com/fapi/v1/order?{}&signature={}".format(tp_params, tp_sig)
        tp_r = requests.post(tp_url, headers=headers, timeout=10)
        if tp_r.status_code != 200:
            print(f"  ⚠️ TP order failed: {tp_r.text[:100]}")
    
    return result

def check_margin_risk():
    """Check margin and position risk - don't overtrade"""
    ts = int(time.time() * 1000)
    sig = get_signature(f'timestamp={ts}')
    # Use v2/positionRisk for accurate entry prices
    r = requests.get(f'https://fapi.binance.com/fapi/v2/positionRisk?timestamp={ts}&signature={sig}',
                     headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
    v2_data = r.json()
    if isinstance(v2_data, dict) and v2_data.get('code'):
        v2_positions = []
    else:
        v2_positions = v2_data

    balance = float(get_balance())
    positions = get_positions()
    
    # Build entry price map from v2
    entry_map = {p['symbol']: float(p.get('entryPrice', 0)) for p in v2_positions}
    
    notional = 0
    for p in positions:
        amt = float(p.get('positionAmt', 0))
        entry = entry_map.get(p['symbol'], 0)
        if entry == 0:
            entry = float(p.get('entryPrice', 0)) or 0
        notional += abs(amt * entry)
    
    margin_used = notional / LEVERAGE if LEVERAGE > 0 else notional
    margin_pct = (margin_used / balance * 100) if balance > 0 else 0
    
    return {
        'balance': balance,
        'positions': len(positions),
        'notional': notional,
        'margin_used': margin_used,
        'margin_pct': margin_pct,
        'safe_to_trade': margin_pct < MAX_MARGIN_PERCENT and len(positions) < MAX_POSITIONS
    }

def should_add_trailing_tp(entry, current, tp, side, trailing_percent=1.5):
    """Check if trailing TP should be activated
    Activates when price moves 1.5% in profit direction
    """
    if side == "LONG":
        profit_pct = ((current - entry) / entry) * 100
        if profit_pct >= trailing_percent:
            # Move TP up by 0.5%
            new_tp = current * 1.005
            return new_tp if new_tp > tp else tp
    else:  # SHORT
        profit_pct = ((entry - current) / entry) * 100
        if profit_pct >= trailing_percent:
            new_tp = current * 0.995
            return new_tp if new_tp < tp else tp
    return None

def place_order(symbol, side, quantity):
    ts = int(time.time() * 1000)
    params = "symbol={}&side={}&type=MARKET&quantity={}&timestamp={}".format(symbol, side, quantity, ts)
    sig = get_signature(params)
    url = "https://fapi.binance.com/fapi/v1/order?{}&signature={}".format(params, sig)
    headers = {'X-MBX-APIKEY': API_KEY}
    r = requests.post(url, headers=headers, timeout=15)
    return r.json()

def set_leverage(symbol, lev=LEVERAGE):
    ts = int(time.time() * 1000)
    params = "symbol={}&leverage={}&timestamp={}".format(symbol, lev, ts)
    sig = get_signature(params)
    url = "https://fapi.binance.com/fapi/v1/leverage?{}&signature={}".format(params, sig)
    headers = {'X-MBX-APIKEY': API_KEY}
    r = requests.post(url, headers=headers, timeout=15)
    return r.json()

def notify_trade(notification_type, data):
    """Send notification based on config settings"""
    # Check if posting is enabled
    post_enabled = True
    try:
        post_enabled = POST_SIGNALS_TO_TELEGRAM
    except:
        pass
    
    if not post_enabled:
        return False
    
    # Check specific notification types
    if notification_type == 'open' and not data.get('NOTIFY_ON_OPEN', True):
        try:
            if not NOTIFY_ON_OPEN:
                return False
        except:
            pass
    elif notification_type == 'close' and not data.get('NOTIFY_ON_CLOSE', True):
        try:
            if not NOTIFY_ON_CLOSE:
                return False
        except:
            pass
    
    msg = ""
    
    if notification_type == 'open':
        msg = f"""🚨 *NEW POSITION OPENED*

🔖 Symbol: {data['symbol']}
📊 Direction: {data['direction']}
💵 Entry: ${data['entry']:.6f}
🛡 SL: ${data['sl']:.6f}
📈 TP: ${data['tp']:.6f}
💰 Size: {data['size']}
📋 Order ID: {data.get('order_id', 'N/A')}"""
    
    elif notification_type == 'close':
        msg = f"""🔴 *POSITION CLOSED*

🔖 Symbol: {data['symbol']}
📊 Type: {data['close_type']}  # SL or TP
💵 Entry: ${data['entry']:.6f}
💵 Exit: ${data['exit']:.6f}
💰 PnL: ${data['pnl']:.2f}
📋 Order ID: {data.get('order_id', 'N/A')}"""
    
    elif notification_type == 'breakeven':
        msg = f"""🛡 *STOP LOSS MOVED TO BREAKEVEN*

🔖 Symbol: {data['symbol']}
💵 Entry: ${data['entry']:.6f}
🛡 New SL: ${data['sl']:.6f}
💰 Current Profit: {data['profit_pct']:.2f}%"""
    
    elif notification_type == 'trailing_tp':
        msg = f"""📈 *TRAILING TP ACTIVATED*

🔖 Symbol: {data['symbol']}
📈 Old TP: ${data['old_tp']:.6f}
📈 New TP: ${data['new_tp']:.6f}
💰 Current Profit: {data['profit_pct']:.2f}%"""
    
    elif notification_type == 'error':
        msg = f"""❌ *TRADING ERROR*

🔖 Symbol: {data['symbol']}
📝 Error: {data['error']}"""
    
    if msg:
        return send_telegram(msg)
    return False

def send_telegram(msg):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHANNEL, 'text': msg, 'parse_mode': 'Markdown'}
    r = requests.post(url, data=data, timeout=15)
    return r.status_code == 200

# === ANALYSIS ===
def calc_ema(prices, period):
    if len(prices) < period:
        return None
    mul = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for p in prices[period:]:
        ema = (p - ema) * mul + ema
    return ema

def calc_atr(candles, period=14):
    if len(candles) < period + 1:
        return None
    trs = []
    for i in range(1, min(period + 1, len(candles))):
        high = float(candles[-i][1])
        low = float(candles[-i][2])
        prev = float(candles[-i-1][3])
        tr = max(high - low, abs(high - prev), abs(low - prev))
        trs.append(tr)
    return sum(trs) / len(trs) if trs else None

def analyze_symbol(symbol, stats):
    """Runner-focused analysis - look for momentum explosions"""
    stat = stats.get(symbol, {})
    price_change = float(stat.get('priceChangePercent', 0))
    
    # Get candles first to check volume/momentum
    candles = get_klines(symbol, '1h', 50)
    if not candles or len(candles) < 20:
        return None
    
    closes = [float(c[4]) for c in candles]  # index 4 = close
    opens = [float(c[1]) for c in candles]     # index 1 = open
    highs = [float(c[2]) for c in candles]    # index 2 = high
    lows = [float(c[3]) for c in candles]     # index 3 = low
    volumes = [float(c[5]) for c in candles] # index 5 = volume
    current = closes[-1]
    
    # === RUNNER CRITERIA ===
    # 1. Volume Spike (5x+ average)
    avg_vol = sum(volumes[-24:]) / 24 if len(volumes) >= 24 else sum(volumes) / len(volumes)
    recent_vol = volumes[-1]
    vol_ratio = recent_vol / avg_vol if avg_vol > 0 else 1
    
    # Get weekly data
    r_weekly = requests.get(f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1w&limit=5', timeout=10)
    weekly_candles = r_weekly.json()
    weekly_change = 0
    if len(weekly_candles) >= 2:
        weekly_open = float(weekly_candles[-1][1])
        weekly_close = float(weekly_candles[-1][4])
        weekly_change = ((weekly_close - weekly_open) / weekly_open) * 100
    
    # 2. 1H Momentum (continuation)
    change_1h = ((closes[-1] - closes[-6]) / closes[-6]) * 100 if len(closes) >= 6 else 0
    
    # 3. Breakout/Breakdown (breaking recent high/low)
    recent_high = max(highs[-10:])
    prev_high = max(highs[-20:-10]) if len(highs) >= 20 else max(highs[:-10])
    recent_low = min(lows[-10:])
    prev_low = min(lows[-20:-10]) if len(lows) >= 20 else min(lows[:-10])
    breakout = recent_high > prev_high * 1.02  # 2% above for LONG
    breakdown = recent_low < prev_low * 0.98  # 2% below for SHORT
    
    # 4. Pocket Pivot Detection (price > 50SMA, green candle, vol spike)
    sma_50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else closes[-1]
    is_green_candle = closes[-1] > opens[-1] if len(opens) > 0 else True
    past_10_vol_max = max(volumes[-10:])
    pocket_pivot = (current > sma_50) and is_green_candle and (recent_vol > past_10_vol_max)
    
    # 5. DCR% (Daily Closing Range %)
    dcr = ((current - lows[-1]) / (highs[-1] - lows[-1])) * 100 if (highs[-1] - lows[-1]) > 0 else 0
    
    # 6. VCS - Volatility Contraction Score (based on ATR compression)
    # Low ATR relative to recent = contraction
    atr_current = calc_atr(candles, 14) or (current * 0.02)
    atr_avg = sum(calc_atr(candles[i:i+5], 14) or (closes[i] * 0.02) for i in range(min(10, len(candles)-5))) / min(10, len(candles)-5) if len(candles) > 5 else atr_current
    vcs_score = 100 - (atr_current / atr_avg * 100) if atr_avg > 0 else 50  # Higher = more contracted
    vcs = vcs_score > 30  # Contraction detected
    
    # 7. Trend Base (price > 50SMA AND 10WMA > 30WMA)
    wma_10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else closes[-1]
    wma_30 = sum(closes[-30:]) / 30 if len(closes) >= 30 else closes[-1]
    trend_base = (current > sma_50) and (wma_10 > wma_30)
    
    # 8. PP Count - count pocket pivots in last 30 days
    pp_count = 0
    for i in range(20, len(closes)-1):
        if i >= 50:  # Need 50 EMA
            vol_high = max(volumes[i-10:i])
            if volumes[i] > vol_high and closes[i] > sum(closes[i-50:i-40])/10:
                pp_count += 1
    
    # 9. 21EMA position in ATR range
    ema_21_val = calc_ema(closes, 21) or current
    ema_position = ((current - (ema_21_val - atr_current)) / (atr_current * 2)) * 100 if atr_current > 0 else 50
    
    # Open Interest - use enhanced OI history
    oi_data = get_oi_history(symbol)
    oi = oi_data.get('current', 0)
    oi_change = oi_data.get('change_pct', 0)
    oi_trend = oi_data.get('trend', 'neutral')
    
    # === NEW INDICATORS v1.0.29 ===
    
    # 10. RSI (14) - Oversold/Oversold
    def calc_rsi(closes, period=14):
        if len(closes) < period + 1:
            return 50
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d if d > 0 else 0 for d in deltas[-period:]]
        losses = [-d if d < 0 else 0 for d in deltas[-period:]]
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    rsi_14 = calc_rsi(closes, 14)
    rsi_signal = (rsi_14 < 30 or rsi_14 > 70)  # Oversold or Overbought
    
    # 11. MACD Histogram Cross
    ema_12 = calc_ema(closes[-26:], 12) if len(closes) >= 26 else calc_ema(closes, 12)
    ema_26 = calc_ema(closes[-26:], 26) if len(closes) >= 26 else calc_ema(closes, 26)
    
    macd_line = ema_12 - ema_26 if ema_12 and ema_26 else 0
    
    # Signal line = EMA of MACD
    macd_hist_current = 0
    macd_hist_prev = 0
    if len(closes) >= 35:
        # Calculate MACD for previous candle
        ema_12_prev = calc_ema(closes[-27:-1], 12)
        ema_26_prev = calc_ema(closes[-27:-1], 26)
        macd_prev = ema_12_prev - ema_26_prev if ema_12_prev and ema_26_prev else 0
        # Signal prev = EMA of MACD prev
        signal_prev = calc_ema([macd_prev] * 9, 9) if macd_prev else 0
        macd_hist_prev = macd_prev - signal_prev if signal_prev else 0
        # Signal current
        signal_current = calc_ema([macd_prev, macd_line], 9) if macd_prev else macd_line
        macd_hist_current = macd_line - signal_current if signal_current else 0
    
    macd_cross = (macd_hist_current > 0 and macd_hist_prev < 0) or (macd_hist_current < 0 and macd_hist_prev > 0)
    
    # 12. Bollinger Bands Touch
    sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else sum(closes) / len(closes)
    std_20 = (sum((c - sma_20) ** 2 for c in closes[-20:]) / 20) ** 0.5 if len(closes) >= 20 else sma_20 * 0.02
    bb_upper = sma_20 + (2 * std_20)
    bb_lower = sma_20 - (2 * std_20)
    bb_touch = (current >= bb_upper * 0.99) or (current <= bb_lower * 1.01)  # Near bands
    
    # 13. VWAP Cross (price crossing VWAP)
    if len(candles) >= 24:
        typical_prices = [(float(c[2]) + float(c[3]) + float(c[4])) / 3 for c in candles[-24:]]
        volumes_24 = [float(c[5]) for c in candles[-24:]]
        vwap = sum(tp * v for tp, v in zip(typical_prices, volumes_24)) / sum(volumes_24) if sum(volumes_24) > 0 else current
    else:
        vwap = current
    vwap_cross = (closes[-1] > vwap > closes[-2]) or (closes[-1] < vwap < closes[-2])
    
    # 14. Extra Volume Score (5x+ avg - extra bonus)
    extra_vol_score = 2 if vol_ratio > 5 else 0
    
    # Runner score - updated with new setups
    runner_score = 0
    
    # Volume
    if vol_ratio > 3: runner_score += 2
    elif vol_ratio > 2: runner_score += 1
    
    # Price changes
    if price_change > 10: runner_score += 2
    elif price_change > 5: runner_score += 1
    if abs(change_1h) > 3: runner_score += 1
    
    # Breakout/Breakdown
    if breakout: runner_score += 2
    if breakdown: runner_score += 2
    
    # OI
    if oi_change > 20: runner_score += 2
    elif oi_change > 10: runner_score += 1
    
    # New setups scoring
    if weekly_change > 20: runner_score += 3  # Weekly 20%+
    elif weekly_change > 10: runner_score += 2
    elif weekly_change > 5: runner_score += 1
    
    if pocket_pivot: runner_score += 2
    if trend_base: runner_score += 1
    if 0 <= ema_position <= 100 and ema_position < 50: runner_score += 1  # Price near 21EMA
    
    # NEW INDICATORS v1.0.29
    if rsi_signal: runner_score += 1  # RSI <30 or >70
    if extra_vol_score > 0: runner_score += extra_vol_score  # Volume 5x+ (extra +2)
    
    # Must have at least score 3 for signal
    if runner_score < MIN_SCORE:
        return None
    
    # Must have significant change for signal (either direction)
    if abs(price_change) < 3:
        return None
    
    # EMAs
    ema_21 = calc_ema(closes, 21)
    ema_50 = calc_ema(closes, 50)
    if not ema_21 or not ema_50:
        return None
    
    # ATR for SL/TP
    atr = calc_atr(candles, 14) or (current * 0.02)
    atr_pct = (atr / current * 100) if current > 0 else 0
    
    # Direction - Detect LONG or SHORT based on momentum
    if price_change > 0:
        direction = "LONG"
    else:
        direction = "SHORT"
    
    # Use ATR-based if ATR% is in safe range, otherwise fallback to PRICE
    if atr_pct >= PRICE_FALLBACK_MIN_ATR and atr_pct <= PRICE_FALLBACK_MAX_ATR:
        # ATR-based SL/TP (anti-fakeout: wider multipliers)
        if atr_pct > ATR_HIGH_VOLATILITY:
            atr_mult_sl = ATR_MULTIPLIER_SL_HIGH
            atr_mult_tp = ATR_MULTIPLIER_TP_HIGH
        else:
            atr_mult_sl = ATR_MULTIPLIER_SL_NORMAL
            atr_mult_tp = ATR_MULTIPLIER_TP_NORMAL
        
        if direction == "LONG":
            sl = current - (atr * atr_mult_sl)
            tp1 = current + (atr * atr_mult_tp)
        else:
            sl = current + (atr * atr_mult_sl)
            tp1 = current - (atr * atr_mult_tp)
        tp2 = None
        sl_method = "ATR"
    else:
        # Fallback to PRICE_TP/PRICE_SL (too tight or too wide)
        if direction == "LONG":
            sl = current * (1 - PRICE_SL / 100)
            tp1 = current * (1 + PRICE_TP / 100)
        else:
            sl = current * (1 + PRICE_SL / 100)
            tp1 = current * (1 - PRICE_TP / 100)
        tp2 = None
        sl_method = "PRICE"
    
    # Trend
    trend = "BULLISH" if current > ema_50 else "BEARISH"
    
    # Structure
    if breakout and direction == "LONG":
        structure = "BREAKOUT"
    elif breakout and direction == "SHORT":
        structure = "BREAKDOWN"
    elif price_change > 10:
        structure = "STRONG_MOMENTUM"
    elif price_change < -10:
        structure = "STRONG_DOWNSIDE"
    else:
        structure = "MOMENTUM"
    
    # Support/Resistance
    resistance = max(highs[-50:]) if len(highs) >= 50 else max(highs)
    support = min(lows[-50:]) if len(lows) >= 50 else min(lows)
    
    # RSI
    rsi = 50
    try:
        gains, losses = 0, 0
        for i in range(1, 15):
            if i >= len(closes): break
            diff = closes[-i] - closes[-i-1]
            if diff > 0: gains += diff
            else: losses -= diff
        avg_gain = gains / 14 if gains else 0
        avg_loss = losses / 14 if losses else 0
        rsi = 100 - (100 / (1 + (avg_gain / avg_loss))) if avg_loss > 0 else 50
    except:
        rsi = 50
    
    # Get Open Interest data
    return {
        'symbol': symbol,
        'direction': direction,
        'current': current,
        'price_change': price_change,
        'change_1h': change_1h,
        'sl': sl,
        'tp1': tp1,
        'tp2': tp2,
        'atr': atr,
        'atr_pct': atr_pct,
        'sl_method': sl_method,
        'rsi': rsi,
        'ema_21': ema_21,
        'ema_50': ema_50,
        'trend': trend,
        'structure': structure,
        'support': support,
        'resistance': resistance,
        'vol_spike': vol_ratio > 2,
        'vol_ratio': vol_ratio,
        'breakout': breakout,
        'runner_score': runner_score,
        'oi': oi,
        'oi_change': oi_change,
        'oi_trend': oi_trend,
        # New setups
        'weekly_change': weekly_change,
        'pocket_pivot': pocket_pivot,
        'dcr': dcr,
        'vcs': vcs,
        'vcs_score': vcs_score,
        'trend_base': trend_base,
        'pp_count': pp_count,
        'ema_position': ema_position
    }

def fetch_brave_news(query, count=2):
    """Fetch news using Brave Search API"""
    try:
        import requests
        brave_key = os.environ.get('BRAVE_API_KEY', '')
        url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count={count}"
        headers = {"Accept": "application/json", "X-Subscription-Token": brave_key}
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            results = data.get('web', {}).get('results', [])
            news = []
            for item in results[:count]:
                title = item.get('title', '')[:50]
                if title:
                    news.append(title)
            return news if news else None
    except:
        pass
    return None

def get_token_news(symbol, stats):
    """Get latest info for a token - price action + market context + real news"""
    sym = symbol.replace('USDT', '')
    
    # Token name mapping for search
    token_names = {
        'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'BNB': 'Binance', 'SOL': 'Solana',
        'XRP': 'XRP Ripple', 'ADA': 'Cardano', 'DOGE': 'Dogecoin', 'AVAX': 'Avalanche',
        'DOT': 'Polkadot', 'MATIC': 'Polygon', 'LINK': 'Chainlink', 'UNI': 'Uniswap',
        'ATOM': 'Cosmos', 'LTC': 'Litecoin', 'FIL': 'Filecoin', 'AAVE': 'Aave',
        'PEPE': 'Pepe crypto', 'SHIB': 'Shiba Inu', 'WIF': 'dogwifhat', 'BONK': 'Bonk',
        'INJ': 'Injective', 'OP': 'Optimism', 'ARB': 'Arbitrum', 'TIA': 'Celestia',
        'SUI': 'Sui blockchain', 'SEI': 'Sei blockchain', 'NEAR': 'NEAR Protocol',
        'APT': 'Aptos', 'RUNE': 'THORChain', 'GRT': 'The Graph', 'ENS': 'Ethereum Name Service',
        'IMX': 'Immutable X', 'STX': 'Stacks', 'RNDR': 'Render Token',
        'XAN': 'XANA metaverse', 'AXS': 'Axie Infinity', 'FTM': 'Fantom',
        'GALA': 'Gala', 'SAND': 'The Sandbox', 'MANA': 'Decentraland',
        'ALGO': 'Algorand', 'VET': 'VeChain', 'THETA': 'Theta'
    }
    
    # Get real news first
    token_name = token_names.get(sym, sym)
    real_news = None
    try:
        import requests
        # Use web search for news
        brave_url = "https://api.search.brave.com/res/v1/web/search"
        headers = {"Accept": "application/json"}
        params = {"q": f"{token_name} crypto news 2026", "count": 2}
        r = requests.get(brave_url, params=params, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            results = data.get('web', {}).get('results', [])
            if results:
                news_titles = [r.get('title', '')[:45] for r in results[:2] if r.get('title')]
                if news_titles:
                    real_news = " | ".join(news_titles)
    except:
        pass
    
    # Get stats
    stat = stats.get(symbol, {})
    change_24h = float(stat.get('priceChangePercent', 0))
    volume = float(stat.get('volume', 0))
    high_24h = float(stat.get('highPrice', 0))
    low_24h = float(stat.get('lowPrice', 0))
    
    # Format volume
    if volume > 1e9:
        vol_str = f"${volume/1e9:.1f}B"
    elif volume > 1e6:
        vol_str = f"${volume/1e6:.1f}M"
    else:
        vol_str = f"${volume/1e3:.1f}K"
    
    # Market context
    if change_24h > 10:
        context = "🔥 Hot momentum"
    elif change_24h > 5:
        context = "📈 Strong gain"
    elif change_24h > 0:
        context = "📊 Positive"
    elif change_24h < -10:
        context = "💥 Heavy selloff"
    elif change_24h < -5:
        context = "📉 Sharp drop"
    else:
        context = "➡️ Sideways"
    
    # If we have real news, use it
    if real_news:
        return f"📰 {real_news}"
    
    return f"{context} | 24h: {change_24h:+.2f}% | Vol: {vol_str}"

def format_signal(analysis, stats):
    s = analysis
    sym = s['symbol'].replace('USDT', '')
    emoji = "🟢" if s['direction'] == "LONG" else "🔴"
    
    # Get token context
    news = get_token_news(s['symbol'], stats)
    
    # Format OI
    oi = s.get('oi', 0)
    oi_change = s.get('oi_change', 0)
    oi_trend = s.get('oi_trend', 'neutral')
    oi_str = f"{oi:,.0f}" if oi else "N/A"
    oi_emoji = "📈" if oi_change > 10 else "📉" if oi_change < -10 else "➡️"
    trend_emoji = "⬆️" if oi_trend == 'up' else "⬇️" if oi_trend == 'down' else "➡️"
    
    msg = f"""{emoji} {s['direction']} SIGNAL {emoji}

📈 {sym}USDT TECHNICAL ANALYSIS 📊
📊 Chart: https://www.tradingview.com/chart/?symbol=BINANCE:{sym}USDT

📐 MULTI-TF CONFIRMATION:
• Trend 1H: {s['trend']}
• Structure: {s['structure']}
📊 24h Change: {s['price_change']:.2f}%

📐 INDICATORS:
• RSI (14): {s['rsi']:.1f}
• EMA 21: {s['ema_21']:.6f}
• EMA 50: {s['ema_50']:.6f}
• ATR: {s['atr']:.6f}

📊 OPEN INTEREST:
• OI: {oi_str}
• OI Change: {oi_emoji} {oi_change:+.1f}%
• OI Trend: {trend_emoji} {oi_trend.upper()}

🔊 VOLUME: {'Volume Spike' if s['vol_spike'] else 'Normal'}

📊 MOMENTUM SETUPS (v1.0.30):
• Weekly: {s.get('weekly_change', 0):+.1f}%
• Pocket Pivot: {'✅ Yes' if s.get('pocket_pivot') else '❌ No'}
• OI Change: {s.get('oi_change', 0):+.1f}%
• Volume Spike: {s.get('vol_ratio', 0):.1f}x

🎯 KEY INDICATORS:
• RSI Signal: {'🔥 OB' if s.get('rsi', 50) > 70 else '❄️ OS' if s.get('rsi', 50) < 30 else '➡️ Neutral'}
• Volume 5x+: {'🔥 Yes' if s.get('vol_ratio', 0) > 5 else '❌ No'}
• Breakout: {'✅ Yes' if s.get('breakout') else '❌ No'}
• Filter: {'✅ PASSED' if filter_signal(s.get('symbol',''), s)[0] else '❌ REJECTED'}
• Score: {s.get('runner_score', 0)}/10

⏱️ COOLDOWN: 2h after SL
• Support: {s['support']:.6f}
• Resistance: {s['resistance']:.6f}

🎯 RUNNER METRICS:
• 1H Momentum: {s.get('change_1h', 0):+.1f}%
• Volume Spike: {s.get('vol_ratio', 1):.1f}x
• Breakout: {'✅ Yes' if s.get('breakout') else '❌ No'}
• Score: {s.get('runner_score', 0)}/10 🚀

💡 INSIGHT: {s['direction']} | {s['structure']} | RSI: {s['rsi']:.1f}
🎯 Entry: ${s['current']:.6f}
🛡 SL: ${s['sl']:.6f} ({s.get('sl_method','ATR')}-based)
📈 TP: ${s['tp1']:.6f}
📊 ATR%: {s.get('atr_pct', 0):.2f}% | Volatility: {'HIGH' if s.get('atr_pct',0)>3 else 'NORMAL' if s.get('atr_pct',0)>1 else 'LOW'}
⏰ Timeframe: 1H

📰 {news}
"""
    return msg

# === MAIN ===
def main():
    print(f"🔍 Scanner v8 Starting...")
    
    balance = get_balance()
    positions = get_positions()
    open_count = len(positions)
    
    # Detect manually closed positions
    try:
        positions_file = os.path.join(script_dir, '.positions_sl_tp.json')
        if os.path.exists(positions_file):
            with open(positions_file, 'r') as f:
                saved_positions = json.load(f)
            
            current_symbols = {p.get('symbol') for p in positions}
            
            for sym in list(saved_positions.keys()):
                if sym not in current_symbols:
                    # Position was closed (manually or auto)
                    print(f"  📝 Detected closed: {sym}")
                    # Add to recently closed
                    with open('.recently_closed', 'a') as f:
                        f.write(f"{sym},{int(time.time())}\n")
                    # Remove from saved
                    del saved_positions[sym]
            
            # Update saved positions
            with open(positions_file, 'w') as f:
                json.dump(saved_positions, f)
    except Exception as e:
        print(f"  Warning: Could not check closed positions: {e}")
    
    print(f"  Balance: ${balance:.2f}")
    print(f"  Open: {open_count}/{MAX_POSITIONS}")
    
    # Check margin risk before trading
    risk = check_margin_risk()
    print(f"  📊 Risk: {risk['margin_pct']:.1f}% margin used")
    
    if not risk['safe_to_trade']:
        print(f"⚠️ HIGH RISK - Not trading!")
        print(f"   Margin: {risk['margin_pct']:.1f}% (max 40%)")
        print(f"   Positions: {risk['positions']}/{MAX_POSITIONS}")
        return
    
    if open_count >= MAX_POSITIONS:
        print("⚠️ Max positions reached")
        return
    
    # Get all tickers
    tickers = get_24h_tickers()
    stats = {t['symbol']: t for t in tickers if t['symbol'].endswith('USDT')}
    
    # Sort by price change
    movers = [(s, float(t['priceChangePercent'])) for s, t in stats.items()]
    movers.sort(key=lambda x: x[1], reverse=True)
    
    print(f"  Found {len(movers)} symbols")
    
    # Load posted signals (to avoid duplicates)
    try:
        with open('.posted_signals', 'r') as f:
            posted = set(f.read().strip().split(','))
    except:
        posted = set()
    
    # Load recently closed positions (skip re-entry for 24h)
    recently_closed = set()
    try:
        with open('.recently_closed', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        symbol, timestamp = parts[0], int(parts[1])
                        # Skip if closed in last 24 hours
                        if time.time() - timestamp < 86400:  # 24 hours
                            recently_closed.add(symbol)
    except:
        pass
    
    # Only check safe coins
    movers_filtered = [(s, p) for s, p in movers if s in SAFE_COINS]
    
    # Check safe coins with momentum
    for symbol, change in movers_filtered[:50]:
        if open_count >= MAX_POSITIONS:
            break
        
        # Skip if already has position
        if any(p.get('symbol') == symbol for p in positions):
            continue
        
        # Skip if token is on delisting blocklist
        if DELISTING_CHECK and is_token_blocked(symbol):
            print(f"  ⚠️ Skipping {symbol} - on delisting blocklist")
            continue
        
        # Skip if recently closed (avoid re-entry)
        if symbol in recently_closed:
            print(f"  Skipping {symbol} - recently closed")
            continue
        
        print(f"  Checking {symbol} ({change:.1f}%)...", end=" ")
        
        try:
            analysis = analyze_symbol(symbol, stats)
            if analysis:
                print(f"✅ SIGNAL! {analysis['direction']}")
                
                # Calculate quantity with proper floor (not int truncation)
                trade_amount = (balance * ENTRY_PERCENT / 100) * LEVERAGE
                
                # Get step size for proper quantity formatting
                try:
                    info_r = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo', timeout=10)
                    step_size = 0.001
                    min_qty = 0.001
                    min_notional = 5.0
                    for s in info_r.json().get('symbols', []):
                        if s['symbol'] == symbol:
                            for f in s.get('filters', []):
                                if f.get('filterType') == 'LOT_SIZE':
                                    step_size = float(f.get('stepSize', 0.001))
                                    min_qty = float(f.get('minQty', 0.001))
                                elif f.get('filterType') == 'MIN_NOTIONAL':
                                    min_notional = float(f.get('notional', 5))
                            break
                except:
                    step_size = 0.001
                    min_notional = 5.0
                
                qty_raw = trade_amount / analysis['current']
                
                # Floor to step size to pass Binance LOT_SIZE filter
                quantity = math.floor(qty_raw / step_size) * step_size
                
                # Ensure minimum notional ($5 Binance minimum)
                if quantity * analysis['current'] < min_notional:
                    quantity = math.floor(min_notional / analysis["current"] / step_size) * step_size
                
                # Ensure quantity >= minimum
                if quantity < min_qty:
                    quantity = min_qty
                
                set_leverage(symbol, LEVERAGE)
                
                side = "BUY" if analysis['direction'] == "LONG" else "SELL"
                
                # Get SL/TP from analysis
                sl_price = analysis.get('sl')
                tp_price = analysis.get('tp1')
                
                # Place order with SL/TP
                result = place_order_with_sl_tp(symbol, side, quantity, sl_price, tp_price)
                
                order_id = result.get('orderId', 'N/A')
                status = result.get('status', 'UNKNOWN')
                
                # Only post if order succeeded (has valid orderId)
                if order_id and order_id != 'N/A':
                    if symbol in posted:
                        print(f"  (already posted)")
                    else:
                        msg = format_signal(analysis, stats)
                        msg += f"\n✅ ORDER EXECUTED: {analysis['direction']}\n"
                        msg += f"🛡 SL: ${analysis['sl']:.6f}\n"
                        msg += f"📈 TP: ${analysis['tp1']:.6f}\n"
                        msg += f"📋 Order ID: {order_id} | Status: {status}"
                        
                        send_telegram(msg)
                        print(f"  Order: {order_id} | Posted to Telegram")
                        
                        # Save SL/TP for price monitor
                        try:
                            positions_file = os.path.join(script_dir, '.positions_sl_tp.json')
                            positions_data = {}
                            if os.path.exists(positions_file):
                                with open(positions_file, 'r') as f:
                                    positions_data = json.load(f)
                            positions_data[symbol] = {
                                'entry': analysis['current'],
                                'sl': analysis['sl'],
                                'tp1': analysis['tp1'],
                                'side': side,
                                'opened_at': datetime.now().isoformat()
                            }
                            with open(positions_file, 'w') as f:
                                json.dump(positions_data, f)
                            print(f"  Saved SL/TP: SL={sl_price}, TP={tp_price}")
                        except Exception as e:
                            print(f"  Warning: Could not save SL/TP: {e}")
                        
                        posted.add(symbol)
                        with open('.posted_signals', 'w') as f:
                            f.write(','.join(posted))
                        
                        open_count += 1
                else:
                    print(f"  Order failed: {status}")
            else:
                print("no signal")
        except Exception as e:
            print(f"error: {e}")
    
    print(f"\n✅ Scan complete!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Price Monitor - Auto close positions when SL/TP hit
Uses SL/TP saved by scanner-v8.py
"""

import os
import time
import hmac
import hashlib
import requests
import json

from datetime import datetime

# === LOAD CONFIG ===
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from config import *
except ImportError:
    pass  # Use defaults

# === LOAD FROM ENV FILE ===
script_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(script_dir, '.env')

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k] = v

# === LOAD CONFIG ===
sys.path.insert(0, script_dir)
try:
    from config import *
except ImportError:
    pass

env_file = os.path.join(script_dir, '.env')

if env_file and os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

API_KEY = os.environ.get('BINANCE_API_KEY', '')
SECRET = os.environ.get('BINANCE_SECRET', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL = os.environ.get('TELEGRAM_CHANNEL', '')

POSITIONS_FILE = os.path.join(script_dir, '.positions_sl_tp.json')

# === LOAD CONFIG FROM config.py ===
try:
    from config import *
except ImportError:
    pass
CHECK_INTERVAL = 60  # seconds

def get_sig(params):
    return hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

def should_move_sl_to_breakeven(entry, current, sl, side, profit_threshold=1.0):
    """Move SL to breakeven when profit > threshold%"""
    if side == 'LONG':
        profit_pct = ((current - entry) / entry) * 100
        if profit_pct >= profit_threshold and sl < entry:
            return entry
    else:
        profit_pct = ((entry - current) / entry) * 100
        if profit_pct >= profit_threshold and sl > entry:
            return entry
    return None

def should_activate_trailing_tp(entry, current, tp, side, trail_percent=1.5):
    """Activate trailing TP when profit > trail_percent%"""
    if side == 'LONG':
        profit_pct = ((current - entry) / entry) * 100
        if profit_pct >= trail_percent:
            new_tp = current * 1.005
            return new_tp if new_tp > tp else tp
    else:
        profit_pct = ((entry - current) / entry) * 100
        if profit_pct >= trail_percent:
            new_tp = current * 0.995
            return new_tp if new_tp < tp else tp
    return None

def update_sl_to_breakeven(symbol, side, new_sl):
    """Update stop loss to breakeven via Binance API"""
    ts = int(time.time() * 1000)
    headers = {'X-MBX-APIKEY': API_KEY}
    try:
        params = f'symbol={symbol}&timestamp={ts}'
        sig = get_sig(params)
        requests.delete(f'https://fapi.binance.com/fapi/v1/allOpenOrders?{params}&signature={sig}', 
                       headers=headers, timeout=15)
    except:
        pass
    
    ts = int(time.time() * 1000)
    close_side = 'SELL' if side == 'LONG' else 'BUY'
    params = f'symbol={symbol}&side={close_side}&type=STOP_MARKET&stopPrice={new_sl}&workingType=CONTRACT_PRICE&closePosition=true&timestamp={ts}'
    sig = get_sig(params)
    try:
        r = requests.post(f'https://fapi.binance.com/fapi/v1/order?{params}&signature={sig}', 
                        headers=headers, timeout=15)
        return r.json()
    except:
        return None

def update_tp_trailing(symbol, side, new_tp):
    """Update TP to trailing level via Binance API"""
    ts = int(time.time() * 1000)
    headers = {'X-MBX-APIKEY': API_KEY}
    close_side = 'SELL' if side == 'LONG' else 'BUY'
    params = f'symbol={symbol}&side={close_side}&type=TAKE_PROFIT_MARKET&stopPrice={new_tp}&workingType=CONTRACT_PRICE&closePosition=true&timestamp={ts}'
    sig = get_sig(params)
    try:
        r = requests.post(f'https://fapi.binance.com/fapi/v1/order?{params}&signature={sig}', 
                        headers=headers, timeout=15)
        return r.json()
    except:
        return None

def get_positions():
    ts = int(time.time() * 1000)
    params = f'timestamp={ts}'
    r = requests.get(f'https://fapi.binance.com/fapi/v2/positionRisk?{params}&signature={get_sig(params)}', 
                   headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
    return [p for p in r.json() if float(p.get('positionAmt', 0)) != 0]

def get_price(symbol):
    ts = int(time.time() * 1000)
    params = f'timestamp={ts}'
    r = requests.get(f'https://fapi.binance.com/fapi/v2/positionRisk?symbol={symbol}&{params}&signature={get_sig(params)}', 
                   headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        return float(data[0].get('markPrice', 0))
    return 0

def load_positions_sl_tp():
    try:
        if os.path.exists(POSITIONS_FILE):
            with open(POSITIONS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def get_atr(symbol, period=14):
    """Get ATR for SL/TP calculation - Template: 1h period"""
    try:
        r = requests.get(f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1h&limit={period+1}', timeout=10)
        candles = r.json()
        
        if len(candles) < period + 1:
            return None
        
        trs = []
        for i in range(1, len(candles)):
            high = float(candles[i][2])  # High
            low = float(candles[i][3])    # Low
            prev_close = float(candles[i-1][4])  # Previous close
            
            # True Range = max(High - Low, |High - PrevClose|, |Low - PrevClose|)
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            trs.append(tr)
        
        return sum(trs) / len(trs) if trs else None
    except:
        return None

def save_positions_sl_tp(data):
    try:
        with open(POSITIONS_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def close_position(symbol, side, quantity):
    ts = int(time.time() * 1000)
    params = f'symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={ts}'
    r = requests.post(f'https://fapi.binance.com/fapi/v1/order?{params}&signature={get_sig(params)}',
                     headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
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
    try:
        if notification_type == 'close' and not NOTIFY_ON_CLOSE:
            return False
        elif notification_type == 'breakeven' and not NOTIFY_ON_BREAKEVEN:
            return False
        elif notification_type == 'trailing_tp' and not NOTIFY_ON_TRAILING_TP:
            return False
    except:
        pass
    
    msg = ""
    
    if notification_type == 'close':
        msg = f"""🔴 *POSITION CLOSED*

🔖 Symbol: {data['symbol']}
📊 Type: {data['close_type']}
💵 Entry: ${data['entry']:.6f}
💵 Exit: ${data['exit']:.6f}
💰 PnL: ${data['pnl']:.2f}"""
    
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

def add_to_recently_closed(symbol):
    """Add symbol to recently closed list"""
    try:
        with open('.recently_closed', 'a') as f:
            f.write(f'{symbol},{int(time.time())}\n')
    except:
        pass

def send_telegram(msg):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
                    data={'chat_id': TELEGRAM_CHANNEL, 'text': msg, 'parse_mode': 'Markdown'})

def check_multi_tp(symbol, side, entry, current, position_amt, original_amt):
    """Check for multi-TP levels and close partial positions"""
    if side == 'LONG':
        profit_pct = ((current - entry) / entry) * 100
    else:
        profit_pct = ((entry - current) / entry) * 100
    
    # Load config
    try:
        tp1 = TP1_PERCENT
        tp2 = TP2_PERCENT
        tp3 = TP3_PERCENT
    except:
        tp1, tp2, tp3 = 2.0, 4.0, 6.0
    
    remaining_pct = (abs(position_amt) / original_amt) * 100 if original_amt > 0 else 0
    
    # TP3: Close remaining at +6% (check first - highest level)
    if profit_pct >= tp3 and remaining_pct > 0:
        close_amt = abs(position_amt)
        close_side = 'SELL' if side == 'LONG' else 'BUY'
        result = close_position(symbol, close_side, close_amt)
        if result and 'orderId' in result:
            notify_trade('partial_tp', {
                'symbol': symbol, 'tp_level': 'TP3', 'profit_pct': profit_pct,
                'closed_amount': close_amt, 'remaining_pct': 0
            })
            print(f"    📈 TP3 HIT! Closed all at +{profit_pct:.2f}%")
            return True
    
    # TP2: Close 33% at +4% (if >33% remaining)
    elif profit_pct >= tp2 and remaining_pct > 33:
        close_amt = abs(original_amt * 0.33)
        close_side = 'SELL' if side == 'LONG' else 'BUY'
        result = close_position(symbol, close_side, close_amt)
        if result and 'orderId' in result:
            notify_trade('partial_tp', {
                'symbol': symbol, 'tp_level': 'TP2', 'profit_pct': profit_pct,
                'closed_amount': close_amt, 'remaining_pct': remaining_pct - 33
            })
            print(f"    📈 TP2 HIT! Closed 33% at +{profit_pct:.2f}%")
            return True
    
    # TP1: Close 33% at +2% (if >66% remaining)
    elif profit_pct >= tp1 and remaining_pct > 66:
        close_amt = abs(original_amt * 0.33)
        close_side = 'SELL' if side == 'LONG' else 'BUY'
        result = close_position(symbol, close_side, close_amt)
        if result and 'orderId' in result:
            notify_trade('partial_tp', {
                'symbol': symbol, 'tp_level': 'TP1', 'profit_pct': profit_pct,
                'closed_amount': close_amt, 'remaining_pct': remaining_pct - 33
            })
            print(f"    📈 TP1 HIT! Closed 33% at +{profit_pct:.2f}%")
            return True
    
    return False

def main():
    if not API_KEY or not SECRET:
        print("❌ ERROR: API keys not set")
        return
    
    print(f"🔔 Price Monitor Starting...")
    print(f"   Check interval: {CHECK_INTERVAL}s")
    
    while True:
        try:
            # Get current open positions from Binance
            positions = get_positions()
            open_symbols = {p.get('symbol') for p in positions}
            
            # Load saved SL/TP data
            saved_data = load_positions_sl_tp()
            
            # Clean stale entries
            stale = [s for s in saved_data if s not in open_symbols]
            if stale:
                for s in stale:
                    del saved_data[s]
                save_positions_sl_tp(saved_data)
                print(f"  🗑 Cleaned {len(stale)} stale positions")
            
            if not positions:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No positions")
                time.sleep(CHECK_INTERVAL)
                continue
            
            for p in positions:
                symbol = p.get('symbol')
                amt = float(p.get('positionAmt', 0))
                entry = float(p.get('entryPrice', 0) or 0)
                current = float(p.get('markPrice', 0) or 0)
                
                if not entry or entry == 0:
                    entry = get_price(symbol)
                if not current or current == 0:
                    current = get_price(symbol)
                
                side = 'LONG' if amt > 0 else 'SHORT'
                
                # Get SL/TP from saved data, or calculate from ATR
                pos_data = saved_data.get(symbol, {})
                
                if pos_data and 'sl' in pos_data and 'tp1' in pos_data:
                    # Use saved SL/TP from scanner
                    sl_price = float(pos_data['sl'])
                    tp_price = float(pos_data['tp1'])
                    print(f"  {symbol}: [SAVED] Entry={entry:.6f} Current={current:.6f} SL={sl_price:.6f} TP={tp_price:.6f}")
                
                # Check for Multi-TP levels (partial closes)
                original_amt = abs(amt)  # Store original amount for Multi-TP calculation
                check_multi_tp(symbol, side, entry, current, amt, original_amt)
                
                # Check for trailing TP - activate when profit > configured %
                try:
                    trail_thresh = MIN_PROFIT_TRAILING_TP if 'MIN_PROFIT_TRAILING_TP' in dir() else 3.0
                except:
                    trail_thresh = 3.0
                new_trailing_tp = should_activate_trailing_tp(entry, current, tp_price, side, trail_percent=trail_thresh)
                if new_trailing_tp and new_trailing_tp != tp_price:
                    print(f"    📈 Trailing TP: {tp_price:.6f} -> {new_trailing_tp:.6f}")
                    update_tp_trailing(symbol, side, new_trailing_tp)
                    tp_price = new_trailing_tp
                
                # === AGGRESSIVE AUTO-CLOSE ===
                # Check if SL should trigger (price crosses SL level)
                if side == 'LONG' and current <= sl_price:
                    print(f"    🚨 LONG SL HIT! {current:.6f} <= {sl_price:.6f}")
                    result = close_position(symbol, 'SELL', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'SL',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                elif side == 'SHORT' and current >= sl_price:
                    print(f"    🚨 SHORT SL HIT! {current:.6f} >= {sl_price:.6f}")
                    result = close_position(symbol, 'BUY', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'SL',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                # Check if TP should trigger
                if side == 'LONG' and current >= tp_price:
                    print(f"    🎯 LONG TP HIT! {current:.6f} >= {tp_price:.6f}")
                    result = close_position(symbol, 'SELL', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'TP',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                elif side == 'SHORT' and current <= tp_price:
                    print(f"    🎯 SHORT TP HIT! {current:.6f} <= {tp_price:.6f}")
                    result = close_position(symbol, 'BUY', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'TP',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                # Aggressive breakeven - move SL to entry when in profit
                try:
                    be_thresh = MIN_PROFIT_BREAKEVEN if 'MIN_PROFIT_BREAKEVEN' in dir() else 5.0
                except:
                    be_thresh = 5.0
                new_breakeven_sl = should_move_sl_to_breakeven(entry, current, sl_price, side, profit_threshold=be_thresh)
                if new_breakeven_sl and new_breakeven_sl != sl_price:
                    print(f"    🛡 Breakeven: {sl_price:.6f} -> {new_breakeven_sl:.6f}")
                    update_sl_to_breakeven(symbol, side, new_breakeven_sl)
                    sl_price = new_breakeven_sl
                else:
                    # Calculate SL/TP from ATR (template formula)
                    atr = get_atr(symbol)
                    if not atr:
                        atr = entry * 0.02  # Default 2%
                    
                    if side == 'LONG':
                        sl_price = entry - (atr * 1.5)  # Template: Entry - 1.5×ATR
                        tp_price = entry + (atr * 3.0)   # Template: Entry + 3×ATR
                    else:  # SHORT
                        sl_price = entry + (atr * 1.5)
                        tp_price = entry - (atr * 3.0)
                    
                    print(f"  {symbol}: [CALC] Entry={entry:.6f} Current={current:.6f} SL={sl_price:.6f} TP={tp_price:.6f} (ATR={atr:.6f})")
                
                # Check for Multi-TP levels (partial closes)
                original_amt = abs(amt)  # Store original amount for Multi-TP calculation
                check_multi_tp(symbol, side, entry, current, amt, original_amt)
                
                # Check for trailing TP - activate when profit > configured %
                try:
                    trail_thresh = MIN_PROFIT_TRAILING_TP if 'MIN_PROFIT_TRAILING_TP' in dir() else 3.0
                except:
                    trail_thresh = 3.0
                new_trailing_tp = should_activate_trailing_tp(entry, current, tp_price, side, trail_percent=trail_thresh)
                if new_trailing_tp and new_trailing_tp != tp_price:
                    print(f"    📈 Trailing TP: {tp_price:.6f} -> {new_trailing_tp:.6f}")
                    update_tp_trailing(symbol, side, new_trailing_tp)
                    tp_price = new_trailing_tp
                
                # === AGGRESSIVE AUTO-CLOSE ===
                # Check if SL should trigger (price crosses SL level)
                if side == 'LONG' and current <= sl_price:
                    print(f"    🚨 LONG SL HIT! {current:.6f} <= {sl_price:.6f}")
                    result = close_position(symbol, 'SELL', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'SL',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                elif side == 'SHORT' and current >= sl_price:
                    print(f"    🚨 SHORT SL HIT! {current:.6f} >= {sl_price:.6f}")
                    result = close_position(symbol, 'BUY', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'SL',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                # Check if TP should trigger
                if side == 'LONG' and current >= tp_price:
                    print(f"    🎯 LONG TP HIT! {current:.6f} >= {tp_price:.6f}")
                    result = close_position(symbol, 'SELL', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'TP',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                elif side == 'SHORT' and current <= tp_price:
                    print(f"    🎯 SHORT TP HIT! {current:.6f} <= {tp_price:.6f}")
                    result = close_position(symbol, 'BUY', abs(amt))
                    if result and 'orderId' in result:
                        # Calculate PnL from entry and exit
                        if side == 'LONG':
                            pnl = (current - entry) * abs(amt)
                        else:
                            pnl = (entry - current) * abs(amt)
                        notify_trade('close', {
                            'symbol': symbol, 'close_type': 'TP',
                            'entry': entry, 'exit': current, 'pnl': pnl
                        })
                        add_to_recently_closed(symbol)
                    continue
                
                # Aggressive breakeven - move SL to entry when in profit
                try:
                    be_thresh = MIN_PROFIT_BREAKEVEN if 'MIN_PROFIT_BREAKEVEN' in dir() else 5.0
                except:
                    be_thresh = 5.0
                new_breakeven_sl = should_move_sl_to_breakeven(entry, current, sl_price, side, profit_threshold=be_thresh)
                if new_breakeven_sl and new_breakeven_sl != sl_price:
                    print(f"    🛡 Breakeven: {sl_price:.6f} -> {new_breakeven_sl:.6f}")
                    update_sl_to_breakeven(symbol, side, new_breakeven_sl)
                    sl_price = new_breakeven_sl
                
                # Check if SL/TP hit
                hit = None
                if side == 'LONG':
                    if current <= sl_price:
                        hit = 'SL'
                    elif current >= tp_price:
                        hit = 'TP'
                else:  # SHORT
                    if current >= sl_price:
                        hit = 'SL'
                    elif current <= tp_price:
                        hit = 'TP'
                
                if hit:
                    print(f"    ⚠️ {hit} triggered! Waiting 60s to confirm...")
                    time.sleep(60)
                    
                    # Verify still hit
                    current_check = get_price(symbol)
                    still_hit = False
                    
                    if side == 'LONG':
                        if hit == 'SL' and current_check <= sl_price:
                            still_hit = True
                        elif hit == 'TP' and current_check >= tp_price:
                            still_hit = True
                    else:
                        if hit == 'SL' and current_check >= sl_price:
                            still_hit = True
                        elif hit == 'TP' and current_check <= tp_price:
                            still_hit = True
                    
                    if not still_hit:
                        print(f"    ⚠️ False alarm - price recovered")
                        continue
                    
                    print(f"    ✅ Confirmed! Closing...")
                    
                    # Close position
                    close_side = 'SELL' if side == 'LONG' else 'BUY'
                    result = close_position(symbol, close_side, abs(amt))
                    
                    order_status = result.get('status', '')
                    order_id = result.get('orderId')
                    
                    if order_status not in ['NEW', 'FILLED', 'PARTIALLY_FILLED']:
                        print(f"    ❌ Close failed: {result}")
                        continue
                    
                    # Wait for order to fill and get actual exit price
                    exit_price = 0
                    max_retries = 10
                    for i in range(max_retries):
                        time.sleep(1)
                        check_params = f'orderId={order_id}&symbol={symbol}&timestamp={int(time.time() * 1000)}'
                        check_r = requests.get(f'https://fapi.binance.com/fapi/v1/order?{check_params}&signature={get_sig(check_params)}', 
                                              headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
                        order_data = check_r.json()
                        status = order_data.get('status', '')
                        avg_price = float(order_data.get('avgPrice', 0))
                        
                        if status == 'FILLED' and avg_price > 0:
                            exit_price = avg_price
                            print(f"    📝 Order filled at {exit_price:.6f}")
                            break
                        elif status == 'FILLED':
                            # Use current price as fallback
                            exit_price = current_check
                            break
                    
                    # Fallback if still no exit price
                    if exit_price == 0:
                        exit_price = current_check
                        print(f"    ⚠️ Using current price: {exit_price:.6f}")
                    
                    # Calculate PnL
                    if side == 'LONG':
                        pnl = (exit_price - entry) * abs(amt)
                        pnl_pct = ((exit_price - entry) / entry) * 100
                    else:
                        pnl = (entry - exit_price) * abs(amt)
                        pnl_pct = ((entry - exit_price) / entry) * 100
                    
                    emoji = "🟢" if pnl > 0 else "🔴"
                    
                    # Send Telegram
                    if hit == 'TP':
                        msg = f"🎉💰 PROFIT TAKEN! 💰🎉\n\n"
                    else:
                        msg = f"❌ STOP HIT\n\n"
                    
                    msg += f"{emoji} {symbol} {side}\n"
                    msg += f"📈 {pnl_pct:+.2f}% (${pnl:+.2f})\n"
                    msg += f"Entry: ${entry:.6f} → Exit: ${exit_price:.6f}\n"
                    msg += f"\n"
                    msg += f"🛡 SL: ${sl_price:.6f}\n"
                    msg += f"📈 TP: ${tp_price:.6f}\n"
                    msg += f"🎯 Hit: {hit}\n"
                    
                    if hit == 'SL':
                        msg += f"\n#StopLoss #Trading #Crypto"
                    else:
                        msg += f"\n#TakeProfit #Winning #Crypto"
                    
                    send_telegram(msg)
                    
                    # Save to recently_closed (to avoid re-entry for 24h)
                    try:
                        with open('.recently_closed', 'a') as f:
                            f.write(f"{symbol},{int(time.time())}\n")
                    except:
                        pass
                    
                    # Remove from saved
                    if symbol in saved_data:
                        del saved_data[symbol]
                        save_positions_sl_tp(saved_data)
                    
                    print(f"    ✅ Closed! {hit} | PnL: ${pnl:.2f}")
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checked {len(positions)} positions")
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

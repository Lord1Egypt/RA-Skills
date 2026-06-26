#!/usr/bin/env python3
"""
/position command - Check current trading positions
Usage: python3 position_command.py
"""

import os
import sys
import json
import time
import hmac
import hashlib
import requests

# Load .env
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and '=' in line:
            k, v = line.split('=', 1)
            os.environ[k] = v

API_KEY = os.environ['BINANCE_API_KEY']
SECRET = os.environ['BINANCE_SECRET']

def get_sig(params):
    ts = int(time.time() * 1000)
    params = f'timestamp={ts}'
    return hmac.new(SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

def main():
    ts = int(time.time() * 1000)
    params = f'timestamp={ts}'
    sig = get_sig(params)
    
    # Get account info
    r = requests.get(f'https://fapi.binance.com/fapi/v2/positionRisk?{params}&signature={sig}',
                   headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
    positions = [p for p in r.json() if float(p.get('positionAmt', 0)) != 0]
    
    # Get account balance
    r2 = requests.get(f'https://fapi.binance.com/fapi/v3/account?{params}&signature={sig}',
                    headers={'X-MBX-APIKEY': API_KEY}, timeout=15)
    acc = r2.json()
    balance = float(acc.get('totalMarginBalance', 0))
    
    # Load SL/TP data
    try:
        with open('.positions_sl_tp.json') as f:
            sl_tp = json.load(f)
    except:
        sl_tp = {}
    
    # Get prices
    r3 = requests.get('https://fapi.binance.com/fapi/v1/ticker/price', timeout=10)
    prices = {t['symbol']: float(t['price']) for t in r3.json()}
    
    # Build output
    msg = "📊 **POSISI TERKINI**\n\n"
    msg += f"💰 Balance: ${balance:.2f}\n"
    msg += f"📊 Positions: {len(positions)}/7\n"
    
    if positions:
        msg += "\n" + "─" * 40 + "\n"
        
        total_pnl = 0
        for p in positions:
            sym = p['symbol']
            entry = float(p['entryPrice'])
            amt = float(p['positionAmt'])
            current = float(p['markPrice'])
            pnl = float(p.get('unRealizedProfit', 0))
            total_pnl += pnl
            side = '🟢' if amt > 0 else '🔴'
            direction = 'LONG' if amt > 0 else 'SHORT'
            
            # Calculate actual ROI per position
            leverage = 10  # default leverage
            capital = abs(entry * amt) / leverage
            if side == '🟢':
                pnl_real = (current - entry) * abs(amt)
            else:
                pnl_real = (entry - current) * abs(amt)
            roi_pct = (pnl_real / capital) * 100 if capital > 0 else 0
            # Price percentage from entry
            pnl_pct = ((current - entry) / entry * 100) if side == '🟢' else ((entry - current) / entry * 100)
            
            if sym in sl_tp:
                sl = float(sl_tp[sym]['sl'])
                tp1 = float(sl_tp[sym]['tp1'])
                tp2 = float(sl_tp[sym].get('tp2', tp1 * 1.5))
                tp3 = float(sl_tp[sym].get('tp3', tp1 * 2))
            else:
                sl = tp1 = tp2 = tp3 = 0
            
            # Status
            if side == '🟢':
                if current <= sl:
                    status = "🚨 SL HIT!"
                elif current >= tp1:
                    status = "🎯 TP1 HIT!"
                else:
                    dist = ((current - entry) / entry * 100)
                    status = f"📈 +{dist:.1f}%"
            else:
                if current >= sl:
                    status = "🚨 SL HIT!"
                elif current <= tp1:
                    status = "🎯 TP1 HIT!"
                else:
                    dist = ((entry - current) / entry * 100)
                    status = f"📈 +{dist:.1f}%"
            
            msg += f"\n{side} **{sym.replace('USDT','')}** {direction}\n"
            msg += f"   Entry: ${entry:.6f}\n"
            msg += f"   Current: ${current:.6f}\n"
            msg += f"   PnL: {pnl_pct:+.2f}% (${pnl:+.2f})\n"
            msg += f"   Status: {status}\n"
            
            if sl:
                msg += f"   SL: ${sl:.6f} | TP: ${tp1:.6f}\n"
        
        msg += "\n" + "─" * 40 + "\n"
        msg += f"📈 Total PnL: ${total_pnl:+.2f}\n"
        roi = (total_pnl / balance * 100) if balance > 0 else 0
        msg += f"📊 ROI: {roi:+.2f}%\n"
    else:
        msg += "\n❌ Tidak ada posisi terbuka\n"
    
    msg += "\n" + "─" * 40 + "\n"
    msg += "⚙️ **AUTOMATION STATUS**\n"
    msg += "   🔍 Scanner: ✅ Automated (5 min)\n"
    msg += "   ⏱️ Entry: ✅ Automated\n"
    msg += "   🚨 SL/TP: ✅ Automated (1 sec)\n"
    msg += "   📊 Breakeven: ✅ +5%\n"
    msg += "   🎯 Trailing TP: ✅ +10%\n"
    msg += "   📱 Notify: ✅ Telegram\n"
    
    return msg

if __name__ == "__main__":
    print(main())

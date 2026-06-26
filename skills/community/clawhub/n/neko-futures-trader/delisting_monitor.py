#!/usr/bin/env python3
"""
Binance Delisting Monitor
Automatically monitors and blocks delisted tokens from trading
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Set, List, Dict

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
BLOCKLIST_FILE = os.path.join(script_dir, '.delist_blocklist.json')

# Keywords that indicate delisting
DELIST_KEYWORDS = [
    'delist', 'removal', 'will be removed', 'will no longer',
    '停止交易', '下架', 'delisted', 'termination',
    'terminate', '停止合约', '合约到期'
]

def load_blocklist() -> Set[str]:
    """Load blocked tokens from file"""
    try:
        with open(BLOCKLIST_FILE, 'r') as f:
            data = json.load(f)
            return set(data.get('tokens', []))
    except:
        return set()

def save_blocklist(tokens: Set[str]):
    """Save blocked tokens to file"""
    data = {
        'tokens': list(tokens),
        'updated': datetime.now().isoformat()
    }
    with open(BLOCKLIST_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_binance_announcements() -> List[Dict]:
    """Fetch latest Binance announcements"""
    try:
        url = "https://api.binance.com/api/v3/exchangeLogo"
        # Actually let's use the proper announcements API
        url = "https://api.binance.com/cms/announcements/getArticles"
        params = {
            'type': 1,
            'page': 1,
            'rows': 50,
            "locale": "en"
        }
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return data.get('articles', []).get('articles', [])
    except Exception as e:
        print(f"Error fetching announcements: {e}")
    return []

def check_delisting_keywords(text: str) -> bool:
    """Check if text contains delisting keywords"""
    text_lower = text.lower()
    for keyword in DELIST_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    return False

def extract_symbols_from_text(text: str) -> List[str]:
    """Extract potential token symbols from text"""
    import re
    # Match common patterns like BTCUSDT, ETHUSDT, etc.
    symbols = re.findall(r'([A-Z]{2,20})(?:USDT|USDC|PERPETUAL|FUTURES)', text)
    return list(set(symbols))

def check_binance_delist_announcements() -> Set[str]:
    """Check Binance announcements for delisting"""
    new_delisted = set()
    blocklist = load_blocklist()
    
    announcements = get_binance_announcements()
    
    for ann in announcements:
        title = ann.get('title', '')
        content = ann.get('content', '')
        article_id = ann.get('id', '')
        
        full_text = f"{title} {content}".lower()
        
        if check_delisting_keywords(full_text):
            symbols = extract_symbols_from_text(title + ' ' + content)
            for sym in symbols:
                sym_usdt = f"{sym}USDT"
                if sym_usdt not in blocklist:
                    new_delisted.add(sym_usdt)
                    print(f"⚠️ DELISTING DETECTED: {sym_usdt}")
                    print(f"   Title: {title}")
    
    if new_delisted:
        all_blocked = blocklist | new_delisted
        save_blocklist(all_blocked)
        notify_telegram_delisting(new_delisted, list(announcements)[:1])
    
    return new_delisted

def notify_telegram_delisting(delisted: Set[str], announcements: List):
    """Send Telegram notification for delisted tokens"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    channel = os.environ.get('TELEGRAM_CHANNEL', '')
    
    if not token or not channel:
        return
    
    msg = "🚨 *DELISTING ALERT*\n\n"
    msg += "Tokens blocked from trading:\n"
    for sym in sorted(delisted):
        msg += f"• {sym}\n"
    msg += "\n_Automatically added to blocklist_"
    
    try:
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
                    data={'chat_id': channel, 'text': msg, 'parse_mode': 'Markdown'},
                    timeout=10)
    except:
        pass

def get_futures_delisted_symbols() -> Set[str]:
    """Check Binance API for futures delisted symbols"""
    try:
        # Check for perpetual contracts that are no longer trading
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            current_symbols = {s['symbol'] for s in data.get('symbols', []) 
                             if s.get('contractType') == 'PERPETUAL'}
            return current_symbols
    except Exception as e:
        print(f"Error checking futures info: {e}")
    return set()

def update_blocklist_from_api():
    """Update blocklist from Binance futures API"""
    blocklist = load_blocklist()
    changed = False
    
    # Check if any current positions are on delist watchlist
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            active_symbols = {s['symbol'] for s in data.get('symbols', [])}
            
            # If a symbol in our blocklist is no longer active, keep it blocked
            for sym in blocklist:
                if sym not in active_symbols and 'DELISTED' not in sym:
                    # Add DELISTED tag
                    new_sym = sym.replace('USDT', '_DELISTED_USDT')
                    blocklist.remove(sym)
                    blocklist.add(new_sym)
                    changed = True
    except Exception as e:
        print(f"Error updating from API: {e}")
    
    if changed:
        save_blocklist(blocklist)

def is_token_blocked(symbol: str) -> bool:
    """Check if a symbol is blocked"""
    blocklist = load_blocklist()
    return symbol in blocklist or f"{symbol}_DELISTED" in blocklist

def get_blocklist() -> Set[str]:
    """Get current blocklist"""
    return load_blocklist()

def manual_add(symbol: str):
    """Manually add a symbol to blocklist"""
    blocklist = load_blocklist()
    if not symbol.endswith('USDT'):
        symbol = f"{symbol}USDT"
    blocklist.add(symbol)
    save_blocklist(blocklist)
    print(f"Added {symbol} to blocklist")

def manual_remove(symbol: str):
    """Manually remove a symbol from blocklist"""
    blocklist = load_blocklist()
    if not symbol.endswith('USDT'):
        symbol = f"{symbol}USDT"
    if symbol in blocklist:
        blocklist.remove(symbol)
        save_blocklist(blocklist)
        print(f"Removed {symbol} from blocklist")

if __name__ == '__main__':
    print("🔍 Checking Binance for delisting announcements...")
    
    blocklist = load_blocklist()
    print(f"Current blocklist: {len(blocklist)} tokens")
    
    new_delisted = check_binance_delist_announcements()
    
    if new_delisted:
        print(f"\n🚨 NEW DELISTED TOKENS:")
        for sym in sorted(new_delisted):
            print(f"  • {sym}")
    else:
        print("✅ No new delisting detected")
    
    print(f"\nTotal blocked: {len(load_blocklist())} tokens")

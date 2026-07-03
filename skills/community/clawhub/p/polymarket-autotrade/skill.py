#!/usr/bin/env python3
"""
Polymarket Skill - PolyMarket Prediction Market Integration

Features:
- Browse trending markets and events
- Check prices and order book
- Execute trades (requires py-clob-client)
"""

import json
import os
import sys
import requests

# Config
USDC_CONTRACT = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
POLYGON_RPC = "https://polygon-rpc.com"
CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137

CREDS_FILE = os.path.join(os.environ.get('OPENCLAW_HOME', os.path.expanduser('~/.openclaw')), 'credentials', 'polymarket.json')
API_CREDS_FILE = os.path.join(os.environ.get('OPENCLAW_HOME', os.path.expanduser('~/.openclaw')), 'credentials', 'polymarket_api.json')

# Trading client cache
_trade_client = None

def load_creds():
    """Load wallet credentials. Priority: env vars > config file."""
    private_key = os.environ.get('POLYMARKET_PRIVATE_KEY')
    proxy_address = os.environ.get('POLYMARKET_PROXY_ADDRESS')
    
    if private_key:
        return {
            'private_key': private_key,
            'proxy_address': proxy_address or ''
        }
    
    # Fallback to config file
    try:
        with open(CREDS_FILE) as f:
            return json.load(f)
    except:
        return None

def load_api_creds():
    """Load API credentials as ApiCreds object"""
    try:
        from py_clob_client.clob_types import ApiCreds
        
        with open(API_CREDS_FILE) as f:
            creds_dict = json.load(f)
            return ApiCreds(
                api_key=creds_dict.get('api_key', ''),
                api_secret=creds_dict.get('api_secret', ''),
                api_passphrase=creds_dict.get('api_passphrase', '')
            )
    except:
        return None

def save_api_creds(api_creds):
    """Save API credentials"""
    creds_dict = {
        'api_key': getattr(api_creds, 'api_key', ''),
        'api_secret': getattr(api_creds, 'api_secret', ''),
        'api_passphrase': getattr(api_creds, 'api_passphrase', ''),
    }
    
    os.makedirs(os.path.dirname(API_CREDS_FILE), exist_ok=True)
    with open(API_CREDS_FILE, 'w') as f:
        json.dump(creds_dict, f, indent=2)

def get_default_wallet():
    """Get default wallet from credentials"""
    creds = load_creds()
    return creds.get('proxy_address') if creds else None

# ==================== Commands ====================
def main():
    args = sys.argv[1:]
    
    if not args:
        print("Polymarket CLI - Browse & Trade Prediction Markets")
        print()
        print("Usage: polymarket <command> [options]")
        print()
        print("Browse:")
        print("  polymarket trending [category]     Trending markets")
        print("  polymarket detail <slug>        Event details (full)")
        print("  polymarket event <slug>         Event details (simple)")
        print()
        print("Trade:")
        print("  polymarket price <token_id>      Check price & order book")
        print("  polymarket buy <token_id> <amt>  Buy (USDC)")
        print("  polymarket sell <token_id> <amt> Sell (USDC)")
        print()
        print("Portfolio:")
        print("  polymarket position             Your positions (from config)")
        print("  polymarket position <wallet>   Positions for wallet")
        print("  polymarket balance            USDC balance (from config)")
        print("  polymarket balance <wallet>   Balance for wallet")
        print()
        print("Categories: geopolitics, crypto, sports, politics, business, entertainment, tech")
        print()
        print("Config: credentials/polymarket.json")
        print("  Required: private_key, proxy_address")
        sys.exit(1)
    
    command = args[0]
    
    # Handle commands with optional wallet
    wallet = get_default_wallet()
    
    if command == "position" or command == "positions":
        w = args[1] if len(args) > 1 else wallet
        if w:
            query_positions(w)
        else:
            print("❌ Wallet not configured")
            print("   Set proxy_address in credentials/polymarket.json")
            print("   Or: polymarket position <wallet_address>")
    elif command == "bal" or command == "balance":
        w = args[1] if len(args) > 1 else wallet
        if w:
            query_balance(w)
        else:
            print("❌ Wallet not configured")
            print("   Set proxy_address in credentials/polymarket.json")
            print("   Or: polymarket balance <wallet_address>")
    
    elif command == "trending":
        get_trending(args[1] if len(args) > 1 else None)
    elif command == "detail" and len(args) > 1:
        get_event_detail(args[1])
    elif command == "event" and len(args) > 1:
        get_event_details(args[1])
    elif command == "price" and len(args) > 1:
        check_price(args[1])
    elif command == "buy" and len(args) > 2:
        trade(args[1], float(args[2]), "BUY")
    elif command == "sell" and len(args) > 2:
        trade(args[1], float(args[2]), "SELL")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

# ==================== Helpers ====================

def get_chinese_desc(title, slug):
    """Get Chinese description for a market"""
    title_lower = title.lower()
    slug_lower = slug.lower()
    
    # Sports
    if any(k in slug_lower for k in ['nfl', 'nba', 'mlb', 'nhl', 'super-bowl', 'game', 'vs']):
        if 'super-bowl' in slug_lower:
            return "🏈 NFL超级碗"
        elif 'nba' in slug_lower:
            return "🏀 NBA篮球"
        elif 'nfl' in slug_lower:
            return "🏈 NFL橄榄球"
        elif 'mlb' in slug_lower:
            return "⚾ MLB棒球"
        else:
            return "🏆 体育赛事"
    
    # Crypto
    if any(k in slug_lower for k in ['bitcoin', 'btc', 'eth', 'ethereum', 'crypto', 'solana']):
        return "₿ 加密货币"
    
    # Fed/Finance
    if any(k in slug_lower for k in ['fed', 'interest', 'rate', 'inflation', 'gdp', 'recession', 'spx', 's&p', 'gold']):
        return "📈 美联储/金融"
    
    # Politics
    if any(k in slug_lower for k in ['trump', 'biden', 'harris', 'vance', 'president', 'election', 'congress', 'senate']):
        return "🗳️ 美国政治"
    
    # Geopolitics
    if any(k in slug_lower for k in ['iran', 'china', 'russia', 'ukraine', 'war', 'military', 'strike']):
        return "🌍 地缘政治"
    
    # AI/Tech
    if any(k in slug_lower for k in ['ai', 'claude', 'gpt', 'openai', 'google', 'apple', 'meta', 'nvidia', 'gpu']):
        return "🤖 AI/科技"
    
    # Entertainment
    if any(k in slug_lower for k in ['oscar', 'grammy', 'emmy', 'movie', 'music', 'celebrity']):
        return "🎬 娱乐八卦"
    
    # Business
    if any(k in slug_lower for k in ['stock', 'company', 'ipo', 'market', 'business', 'store', 'ceo']):
        return "💼 商业经济"
    
    # Default
    return ""

# ==================== Browse ====================
def get_trending(category=None):
    """Get trending markets"""
    name = category.upper() if category else "ALL"
    print(f"🚀 Polymarket {name} Trending Top 10\n")
    
    tag_slugs = {
        'crypto': 'crypto', 'sports': 'sports', 'geopolitics': 'geopolitics',
        'politics': 'politics', 'business': 'business', 'entertainment': 'pop-culture',
        'tech': 'tech', 'technology': 'tech',
    }
    
    url = "https://gamma-api.polymarket.com/events/pagination"
    params = {
        "order": "featuredOrder", "featured_order": "true", "ascending": "true",
        "active": "true", "archived": "false", "closed": "false", "limit": 10,
    }
    
    if category and category.lower() in tag_slugs:
        params = {
            "tag_slug": tag_slugs[category.lower()], "order": "volume24hr", 
            "ascending": "false", "active": "true", "archived": "false", 
            "closed": "false", "limit": 10,
        }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"❌ Request failed: {resp.status_code}")
            return
        
        events = resp.json().get('data', [])
        
        for i, e in enumerate(events[:10]):
            title = e.get('title', '')
            slug = e.get('slug', '')
            vol = float(e.get('volume24hr', 0) or 0)
            vol_str = f"${vol/1e6:.1f}M" if vol >= 1e6 else f"${vol/1e3:.0f}K"
            
            desc = get_chinese_desc(title, slug)
            tag = f" {desc}" if desc else ""
            
            print(f"【{i+1}】{title}{tag}")
            print(f"   📊 {vol_str} | https://polymarket.com/event/{slug}")
            
            # Get odds
            try:
                d = requests.get(f"https://gamma-api.polymarket.com/events/slug/{slug}", timeout=5).json()
                markets = d.get('markets', [])
                opts = []
                for m in markets[:3]:
                    outcomes = json.loads(m.get('outcomes', '[]'))
                    prices = json.loads(m.get('outcomePrices', '[]'))
                    for j, o in enumerate(outcomes[:2]):
                        if j < len(prices):
                            try:
                                opts.append(f"{o}: {float(prices[j])*100:.0f}%")
                            except:
                                pass
                if opts:
                    print(f"   🎯 {' | '.join(opts)}")
            except:
                pass
            print()
        
        print(f"Total: {len(events)} events")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def get_event_detail(slug):
    """Get full event details"""
    slug = slug.replace('event/', '').replace('https://polymarket.com/event/', '')
    
    try:
        resp = requests.get(f"https://gamma-api.polymarket.com/events/slug/{slug}", timeout=10)
        if resp.status_code != 200:
            print(f"❌ Not found: {resp.status_code}")
            return
        
        e = resp.json()
        print("=" * 60)
        print(f"📌 {e.get('title')}")
        print(f"   📊 24h: ${float(e.get('volume24hr', 0)):,.0f} | 💰 Total: ${float(e.get('volume', 0)):,.0f}")
        print(f"   🔗 https://polymarket.com/event/{slug}")
        print("=" * 60)
        
        markets = e.get('markets', [])
        if not markets:
            print("\n⚠️ No options")
            return
        
        print(f"\n📊 Markets ({len(markets)}):\n")
        
        for i, m in enumerate(markets):
            q = m.get('question', '')
            vol = float(m.get('volume', 0) or 0)
            token_id = m.get('tokenId', '')
            outcomes = json.loads(m.get('outcomes', '[]'))
            prices = json.loads(m.get('outcomePrices', '[]'))
            
            print(f"{i+1}. {q}")
            print(f"   💰 ${vol:,.0f}")
            if token_id:
                print(f"   🪙 Token: {token_id[:30]}...")
            
            if outcomes and prices:
                print("   🎯 Odds:")
                for j, o in enumerate(outcomes):
                    if j < len(prices):
                        try:
                            print(f"      • {o}: {float(prices[j])*100:.1f}%")
                        except:
                            print(f"      • {o}: {prices[j]}")
            print()
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def get_event_details(slug):
    """Get simple event details"""
    slug = slug.replace('event/', '').replace('https://polymarket.com/event/', '')
    
    try:
        resp = requests.get(f"https://gamma-api.polymarket.com/events/slug/{slug}", timeout=10)
        if resp.status_code != 200:
            print(f"❌ Not found: {resp.status_code}")
            return
        
        e = resp.json()
        print(f"📌 {e.get('title')}")
        print(f"   📊 24h: ${float(e.get('volume24hr', 0)):,.0f} | 💰 Total: ${float(e.get('volume', 0)):,.0f}")
        print(f"   🏷️ {len(e.get('markets', []))} options")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== Trade ====================
def _init_trade_client():
    """Initialize trading client"""
    global _trade_client
    
    if _trade_client is not None:
        return _trade_client
    
    try:
        from py_clob_client_v2 import ClobClient
        from py_clob_client_v2.clob_types import MarketOrderArgsV2, OrderType, PartialCreateOrderOptions
        from py_clob_client.order_builder.constants import BUY, SELL
    except ImportError:
        print("❌ py-clob-client not installed")
        print("   Install: pip install py-clob-client")
        return None
    
    creds = load_creds()
    if not creds or not creds.get('private_key'):
        print("❌ Configure wallet first")
        print("   Add private_key to credentials/polymarket.json")
        return None
    
    client = ClobClient(
        host=CLOB_HOST, key=creds['private_key'], chain_id=CHAIN_ID,
        signature_type=2, funder=creds.get('proxy_address', '')
    )
    
    api_creds = load_api_creds()
    if api_creds:
        client.set_api_creds(api_creds)
    else:
        api_creds = client.create_or_derive_api_creds()
        save_api_creds(api_creds)
        client.set_api_creds(api_creds)
        print("✅ API credentials generated")
    
    _trade_client = client
    return client

def check_price(token_id):
    """Check price and order book"""
    print(f"\n📊 Price: {token_id[:30]}...\n")
    
    client = _init_trade_client()
    if not client:
        return
    
    try:
        from py_clob_client_v2 import ClobClient
        
        buy = client.get_price(token_id=token_id, side="BUY")
        sell = client.get_price(token_id=token_id, side="SELL")
        
        print(f"   💚 Buy:  ${float(buy.get('price', 0)):.4f}")
        print(f"   💔 Sell: ${float(sell.get('price', 0)):.4f}")
        
        book = client.get_order_book(token_id=token_id)
        print(f"\n📘 Order Book: {len(book.bids)} bids | {len(book.asks)} asks")
        
        if book.bids[:3]:
            print("\n🟢 Top Bids:")
            for i, b in enumerate(book.bids[:3]):
                print(f"   {i+1}. ${float(b.price):.4f} × {float(b.size):.2f}")
        
        if book.asks[:3]:
            print("\n🔴 Top Asks:")
            for i, a in enumerate(book.asks[:3]):
                print(f"   {i+1}. ${float(a.price):.4f} × {float(a.size):.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def trade(token_id, amount, side):
    """Execute trade"""
    from py_clob_client_v2.clob_types import MarketOrderArgsV2, OrderType, PartialCreateOrderOptions
    from py_clob_client.order_builder.constants import BUY, SELL
    
    print(f"\n🛒 {'BUY' if side == 'BUY' else 'SELL'}")
    print(f"   Token: {token_id[:30]}...")
    print(f"   Amount: ${amount:.2f}")
    
    client = _init_trade_client()
    if not client:
        return
    
    try:
        mo_args = MarketOrderArgsV2(
            token_id=token_id, 
            amount=amount, 
            side=BUY if side == "BUY" else SELL
        )
        signed = client.create_market_order(mo_args)
        response = client.post_order(signed, OrderType.FOK)
        
        if response:
            print("\n✅ Order placed:")
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Order ID: {response.get('orderID', 'unknown')[:20]}...")
            h = response.get('transactionsHashes', [])
            if h:
                print(f"   Hash: {h[0]}")
        else:
            print("❌ Order failed")
            
    except Exception as e:
        print(f"❌ Trade failed: {e}")

def query_positions(wallet):
    """Query positions"""
    try:
        resp = requests.get("https://data-api.polymarket.com/positions",
                          params={"user": wallet.lower(), "sizeThreshold": 0.01, "limit": 100}, timeout=10)
        data = resp.json()
        
        if not data:
            print("No positions")
            return
        
        print(f"\n=== Positions ({len(data)} items) ===")
        
        total = 0
        for p in data:
            o = p.get('outcome', 'Unknown')
            s = float(p.get('size', 0))
            v = float(p.get('currentValue', 0))
            cur_price = float(p.get('curPrice', 0))
            title = p.get('title', '')
            init_val = float(p.get('initialValue', 0))
            pnl = float(p.get('cashPnl', 0))
            
            print(f"\n  📌 {title}")
            print(f"     选项: {o} | {s:,.4f} shares")
            print(f"     当前价: {cur_price:.4f} | 市值: ${v:,.2f} | 投入: ${init_val:.2f} | PnL: ${pnl:+,.2f}")
            total += v
        
        print(f"\n💰 总市值: ${total:,.2f}")
        
    except Exception as e:
        print(f"Error: {e}")

def query_balance(wallet):
    """Query wallet balances (USDC, USDC.e, POL, pUSD via clob)"""
    def _balance_of(contract, decimals):
        data = f"0x70a08231000000000000000000000000{wallet[2:]}"
        try:
            resp = requests.post(POLYGON_RPC, json={"jsonrpc":"2.0","method":"eth_call","params":[{"to":contract,"data":data},"latest"],"id":1}, timeout=10)
            return int(resp.json().get("result", "0x0"), 16) / 10**decimals
        except:
            return None
    
    try:
        # POL (native MATIC)
        resp = requests.post(POLYGON_RPC, json={"jsonrpc":"2.0","method":"eth_getBalance","params":[wallet,"latest"],"id":1}, timeout=10)
        pol = int(resp.json().get("result", "0x0"), 16) / 10**18
        
        # USDC (native)
        usdc_contract = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        usdc_bal = _balance_of(usdc_contract, 6)
        
        # USDC.e (Bridged)
        usdc_e_contract = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
        usdce_bal = _balance_of(usdc_e_contract, 6)
        
        # pUSD via CLOB API (Polymarket platform balance)
        pusd_bal = None
        try:
            creds = load_creds()
            if creds and creds.get('private_key'):
                from py_clob_client_v2 import ClobClient
                from py_clob_client_v2.clob_types import ApiCreds, BalanceAllowanceParams, AssetType
                
                client = ClobClient(CLOB_HOST, key=creds['private_key'], chain_id=CHAIN_ID, signature_type=2, funder=creds.get('proxy_address',''))
                api_creds = load_api_creds()
                if api_creds:
                    client.set_api_creds(api_creds)
                else:
                    api_creds = client.create_or_derive_api_creds()
                    client.set_api_creds(api_creds)
                    save_api_creds(api_creds)
                
                params = BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
                ba = client.get_balance_allowance(params)
                pusd_bal = int(ba.get('balance', '0')) / 10**6
        except Exception:
            pass
        
        print(f"\n💵 Balance for {wallet}")
        print(f"   POL: {pol:,.6f}")
        if usdc_bal is not None:
            print(f"   USDC (on-chain): {usdc_bal:,.6f}")
        if usdce_bal is not None:
            print(f"   USDC.e: {usdce_bal:,.6f}")
        if pusd_bal is not None:
            print(f"   pUSD (Polymarket): {pusd_bal:,.6f}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Meme Scanner v2 - 基于 GMGN 官方 API 的扫链工具
完全使用 GMGN API，通过浏览器 CDP 绕过 Cloudflare
"""

import json, asyncio, sys, os, time, websockets, urllib.request
from datetime import datetime

CHROME_WS_BASE = "ws://localhost:9222"
SCANNED_FILE = "/root/.openclaw/workspace/scanned_tokens.json"

# GMGN API 配置
GMGN_BASE = "https://gmgn.ai"
DEVICE_ID = "bf3bd459-9cc5-46f0-95bf-8297b8a58c72"
FP_DID = "c44ca81f8d7dabb1d0dc62c33c0ee26d"
CLIENT_ID = "gmgn_web_20260304-11376-fc51c8a"
FROM_APP = "gmgn"
APP_VER = "20260304-11376-fc51c8a"
TZ_NAME = "Asia/Shanghai"
TZ_OFFSET = "28800"
APP_LANG = "zh-CN"
OS = "web"
WORKER = "0"

# 筛选条件（测试用，非常宽松）
MIN_MCAP = 5000         # $5K
MAX_MCAP = 10000000     # $10M
MIN_LIQUIDITY = 1000    # $1K
MIN_HOLDERS = 10        # 10人
MIN_CHANGE_24H = 0      # 0%
MIN_VOL_MCAP_RATIO = 0.1  # 10%
MAX_BUNDLER_RATE = 0.9  # 90%
MIN_EARLY_SCORE = 4     # 4分

def get_common_params():
    return f"device_id={DEVICE_ID}&fp_did={FP_DID}&client_id={CLIENT_ID}&from_app={FROM_APP}&app_ver={APP_VER}&tz_name={TZ_NAME}&tz_offset={TZ_OFFSET}&app_lang={APP_LANG}&os={OS}&worker={WORKER}"

def fmt_num(n):
    if n is None: return "N/A"
    n = float(n)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.2f}"

def fmt_price(p):
    if p is None: return "N/A"
    p = float(p)
    if p >= 1: return f"${p:.4f}"
    if p >= 0.001: return f"${p:.8f}".rstrip('0')
    return f"${p:.12f}".rstrip('0')

def load_scanned():
    if os.path.exists(SCANNED_FILE):
        try:
            with open(SCANNED_FILE, 'r') as f:
                data = json.load(f)
                now = time.time()
                cleaned = {k: v for k, v in data.items() if now - v < 86400}
                return cleaned
        except:
            return {}
    return {}

def save_scanned(scanned):
    with open(SCANNED_FILE, 'w') as f:
        json.dump(scanned, f)

async def get_page_id():
    try:
        resp = urllib.request.urlopen("http://localhost:9222/json/list")
        tabs = json.loads(resp.read())
        for t in tabs:
            if t.get('type') == 'page' and 'gmgn.ai' in t.get('url', ''):
                return t['id']
        for t in tabs:
            if t.get('type') == 'page':
                return t['id']
    except Exception as e:
        print(f"Error getting page ID: {e}", file=sys.stderr)
    return None

async def chrome_fetch(ws, url):
    js = f"fetch('{url}').then(r=>r.json())"
    await ws.send(json.dumps({'id':1,'method':'Runtime.evaluate','params':{'expression':js,'awaitPromise':True}}))
    resp = await ws.recv()
    result = json.loads(resp).get('result',{}).get('result',{})
    if result.get('type') == 'object':
        obj_id = result.get('objectId')
        if obj_id:
            await ws.send(json.dumps({'id':2,'method':'Runtime.callFunctionOn','params':{'objectId':obj_id,'functionDeclaration':'function(){return JSON.stringify(this)}'}}))
            resp2 = await ws.recv()
            json_str = json.loads(resp2).get('result',{}).get('result',{}).get('value','{}')
            return json.loads(json_str)
    return {}

async def scan_gmgn_rank(ws, chain):
    """使用 GMGN rank API 扫描热门代币"""
    params = get_common_params()
    tokens = []
    
    # 1. 扫描 1小时交易最活跃
    url = f"{GMGN_BASE}/defi/quotation/v1/rank/{chain}/swaps/1h?{params}&limit=50&orderby=swaps&direction=desc"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        rank_list = data.get('data', {}).get('rank', [])
        for item in rank_list:
            # rank API 返回的数据已经包含大部分信息
            token = {
                'address': item.get('address'),
                'chain': chain,
                'symbol': item.get('symbol'),
                'price': float(item.get('price', 0)),
                'market_cap': float(item.get('market_cap', 0)),
                'liquidity': float(item.get('liquidity', 0)),
                'volume_24h': float(item.get('volume', 0)),
                'holder_count': item.get('holder_count', 0),
                'is_honeypot': item.get('is_honeypot', 0) == 1,
                'buy_tax': float(item.get('buy_tax', 0) or 0),
                'sell_tax': float(item.get('sell_tax', 0) or 0),
                'top_10_holder_rate': float(item.get('top_10_holder_rate', 0)),
                'twitter': item.get('twitter_username'),
                'website': item.get('website'),
                'creation_timestamp': item.get('creation_timestamp'),
                # 计算涨跌幅
                'change_1h': item.get('price_change_percent1h', 0) * 100 if item.get('price_change_percent1h') else 0,
            }
            tokens.append(token)
    
    # 2. 扫描 24小时涨幅榜
    url = f"{GMGN_BASE}/defi/quotation/v1/rank/{chain}/gainers/24h?{params}&limit=50&orderby=price_change_percent&direction=desc"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        rank_list = data.get('data', {}).get('rank', [])
        for item in rank_list:
            token = {
                'address': item.get('address'),
                'chain': chain,
                'symbol': item.get('symbol'),
                'price': float(item.get('price', 0)),
                'market_cap': float(item.get('market_cap', 0)),
                'liquidity': float(item.get('liquidity', 0)),
                'volume_24h': float(item.get('volume', 0)),
                'holder_count': item.get('holder_count', 0),
                'is_honeypot': item.get('is_honeypot', 0) == 1,
                'buy_tax': float(item.get('buy_tax', 0) or 0),
                'sell_tax': float(item.get('sell_tax', 0) or 0),
                'top_10_holder_rate': float(item.get('top_10_holder_rate', 0)),
                'twitter': item.get('twitter_username'),
                'website': item.get('website'),
                'creation_timestamp': item.get('creation_timestamp'),
                'change_24h': item.get('price_change_percent', 0) * 100 if item.get('price_change_percent') else 0,
            }
            tokens.append(token)
    
    return tokens

async def fetch_token_details(ws, chain, address):
    """获取代币详细信息"""
    params = get_common_params()
    token = {}
    
    # 1. 基础信息
    url = f"{GMGN_BASE}/vas/api/v1/search_v3?{params}&chain={chain}&q={address}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        coins = data.get('data', {}).get('coins', [])
        if coins:
            coin = coins[0]
            token['address'] = address
            token['chain'] = chain
            token['name'] = coin.get('name')
            token['symbol'] = coin.get('symbol')
            token['price'] = float(coin.get('price', 0))
            token['market_cap'] = float(coin.get('mcp', 0))
            token['liquidity'] = float(coin.get('liquidity', 0))
            token['volume_24h'] = float(coin.get('volume_24h', 0))
            token['holder_count'] = coin.get('holder_count', 0)
            
            # 计算24小时涨跌幅
            price_24h = coin.get('price_24h')
            if price_24h and float(price_24h) > 0:
                current_price = float(coin.get('price', 0))
                price_24h_float = float(price_24h)
                token['change_24h'] = ((current_price - price_24h_float) / price_24h_float) * 100
    
    # 2. 安全检测
    url = f"{GMGN_BASE}/api/v1/mutil_window_token_security_launchpad/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        security = data.get('data', {}).get('security', {})
        token['is_honeypot'] = security.get('is_honeypot', False)
        token['buy_tax'] = float(security.get('buy_tax', 0) or 0)
        token['sell_tax'] = float(security.get('sell_tax', 0) or 0)
    
    # 3. 持有者统计
    url = f"{GMGN_BASE}/api/v1/token_stat/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        stat = data.get('data', {})
        token['top_10_holder_rate'] = float(stat.get('top_10_holder_rate', 0))
        token['bundler_rate'] = float(stat.get('top_bundler_trader_percentage', 0))
    
    # 4. 社交链接
    url = f"{GMGN_BASE}/api/v1/mutil_window_token_link_rug_vote/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        link = data.get('data', {}).get('link', {})
        token['twitter'] = link.get('twitter_username')
        token['website'] = link.get('website')
    
    return token

def calculate_early_score(token):
    """计算早期得分"""
    score = 5
    mc = token.get('market_cap', 0) or 0
    liq = token.get('liquidity', 0) or 0
    holders = token.get('holder_count', 0) or 0
    vol = token.get('volume_24h', 0) or 0
    change_24h = token.get('change_24h', 0) or 0
    bundler = token.get('bundler_rate', 0) or 0
    
    # 流动性评分
    if liq > 100000: score += 2
    elif liq > 50000: score += 1
    elif liq < 10000: score -= 1
    
    # 市值评分
    if 100000 < mc < 2000000: score += 2
    elif mc < 50000: score += 1
    
    # 持有者评分
    if holders > 1000: score += 1
    elif holders < 100: score -= 1
    
    # 交易量评分
    if mc > 0:
        vol_ratio = vol / mc
        if vol_ratio > 1: score += 2
        elif vol_ratio > 0.5: score += 1
    
    # 涨幅评分
    if change_24h > 500: score += 2
    elif change_24h > 200: score += 1
    
    # Bundler 惩罚
    if bundler > 0.5: score -= 2
    elif bundler > 0.3: score -= 1
    
    return max(1, min(10, score))

def filter_token(token):
    """筛选代币"""
    mc = token.get('market_cap', 0) or 0
    liq = token.get('liquidity', 0) or 0
    holders = token.get('holder_count', 0) or 0
    change_24h = token.get('change_24h', 0) or 0
    bundler = token.get('bundler_rate', 0) or 0
    vol = token.get('volume_24h', 0) or 0
    
    # 基础筛选
    if token.get('is_honeypot'): return False
    if not (MIN_MCAP <= mc <= MAX_MCAP): return False
    if liq < MIN_LIQUIDITY: return False
    if holders < MIN_HOLDERS: return False
    if change_24h < MIN_CHANGE_24H: return False
    if bundler > MAX_BUNDLER_RATE: return False
    
    # 交易量/市值比
    if mc > 0:
        vol_ratio = vol / mc
        if vol_ratio < MIN_VOL_MCAP_RATIO: return False
    
    # 早期得分
    score = calculate_early_score(token)
    if score < MIN_EARLY_SCORE: return False
    
    return True

def format_message(token):
    """格式化消息"""
    chain = token['chain'].upper()
    address = token['address']
    score = calculate_early_score(token)
    
    # 风险等级
    if score >= 8:
        risk_level = "🟢 Low"
        action = "☢️ 重点关注"
    elif score >= 6:
        risk_level = "🟡 Medium"
        action = "👀 可以关注"
    else:
        risk_level = "🔴 High"
        action = "⚠️ 谨慎观望"
    
    # 计算创建时间
    age_str = "未知"
    creation_timestamp = token.get('creation_timestamp')
    if creation_timestamp:
        age_seconds = int(time.time() - creation_timestamp)
        if age_seconds < 3600:
            age_str = f"{age_seconds // 60} 分钟前"
        elif age_seconds < 86400:
            age_str = f"{age_seconds // 3600} 小时前"
        else:
            age_str = f"{age_seconds // 86400} 天前"
    
    msg = f"🔔 发现潜力 Meme 代币！📊 gmgn热门\n"
    msg += f"🔍 {token.get('name', 'Unknown')} (${token.get('symbol', 'N/A')}) | {chain} (创建 {age_str})\n"
    msg += f"CA: {address}\n\n"
    msg += f"| 指标 | 数值 |\n"
    msg += f"| ---------- | -------------------- |\n"
    msg += f"| 💰 价格 | {fmt_price(token.get('price'))} |\n"
    msg += f"| 📊 市值 | {fmt_num(token.get('market_cap'))} |\n"
    msg += f"| 💧 流动性 | {fmt_num(token.get('liquidity'))} |\n"
    
    # 涨跌幅
    change_24h = token.get('change_24h')
    if change_24h:
        msg += f"| 📈 24h | {'+' if change_24h >= 0 else ''}{change_24h:.2f}% |\n"
    
    msg += f"| 👥 Holders | {token.get('holder_count', 'N/A')} |\n"
    
    vol_mc_ratio = 0
    if token.get('volume_24h') and token.get('market_cap'):
        vol_mc_ratio = (token['volume_24h'] / token['market_cap']) * 100
    msg += f"| 📦 24h Vol | {fmt_num(token.get('volume_24h'))} ({vol_mc_ratio:.0f}% of MC) |\n"
    
    change_1h = token.get('change_1h')
    if change_1h:
        msg += f"| ⏱️ 1h | {'+' if change_1h >= 0 else ''}{change_1h:.2f}% |\n"
    
    msg += f"\n• Early Score: {score}/10\n"
    msg += f"• Risk: {risk_level}\n"
    msg += f"• Action: {action}\n"
    
    # 链接
    links = []
    if token.get('twitter'):
        twitter = token['twitter']
        if not twitter.startswith('http'):
            twitter = f"https://x.com/{twitter}"
        links.append(f"🐦 Twitter: {twitter}")
    if token.get('website'):
        links.append(f"🌐 Website: {token['website']}")
    
    if links:
        msg += "\n".join(links) + "\n"
    
    # GMGN 链接
    msg += f"🔗 [GMGN](https://gmgn.ai/{token['chain']}/token/{address})\n"
    
    # Why Alpha 分析
    why_alpha = generate_why_alpha(token, score, change_24h, change_1h)
    msg += f"💡 Why Alpha: {why_alpha}\n"
    
    # Narrative Vibe
    narrative = generate_narrative(token, chain)
    msg += f"• Narrative Vibe: {narrative}\n"
    
    # 风险提示
    risks = []
    if token.get('bundler_rate', 0) > 0.3:
        risks.append(f"Bundler比例{token['bundler_rate']*100:.0f}%")
    if token.get('top_10_holder_rate', 0) > 0.5:
        risks.append(f"Top10集中度{token['top_10_holder_rate']*100:.0f}%")
    
    liq = token.get('liquidity', 0) or 0
    if liq < 10000:
        risks.append("流动性偏低")
    
    buy_tax = token.get('buy_tax', 0) or 0
    sell_tax = token.get('sell_tax', 0) or 0
    if buy_tax > 5 or sell_tax > 5:
        risks.append(f"税率偏高(买{buy_tax:.0f}%/卖{sell_tax:.0f}%)")
    
    if risks:
        msg += f"• ⚠️ 风险提示: {', '.join(risks)}\n"
    else:
        msg += f"• ⚠️ 风险提示: 暂无明显风险\n"
    
    return msg

def generate_why_alpha(token, score, change_24h, change_1h):
    """生成 Why Alpha 分析"""
    name = token.get('name', '该代币')
    symbol = token.get('symbol', 'N/A')
    mc = token.get('market_cap', 0) or 0
    vol = token.get('volume_24h', 0) or 0
    
    analysis = f"{name}(${symbol}) 得分{score}/10，"
    
    if score >= 8:
        analysis += "潜力强劲。"
    elif score >= 6:
        analysis += "潜力中等。"
    else:
        analysis += "潜力较弱。"
    
    if change_24h and change_24h > 50:
        analysis += f" 24h暴涨{change_24h:.0f}%，短期爆发力强。"
    elif change_24h and change_24h > 0:
        analysis += f" 24h上涨{change_24h:.0f}%，表现稳健。"
    
    if mc > 0 and vol > 0:
        vol_ratio = vol / mc
        if vol_ratio > 10:
            analysis += f" 交易量是市值{vol_ratio:.0f}倍，市场关注度极高。"
        elif vol_ratio > 1:
            analysis += f" 交易量是市值{vol_ratio:.0f}倍，交易活跃。"
    
    analysis += " 综合看"
    if score >= 8:
        analysis += "潜力强，值得重点关注。"
    elif score >= 6:
        analysis += "有一定潜力，可以关注。"
    else:
        analysis += "风险较高，需谨慎。"
    
    return analysis

def generate_narrative(token, chain):
    """生成 Narrative Vibe"""
    narratives = [f"{chain.upper()} 生态"]
    
    name = token.get('name', '').lower()
    symbol = token.get('symbol', '').lower()
    
    # 根据名称判断叙事
    if any(x in name or x in symbol for x in ['trump', 'biden', 'musk', 'cz', 'elon']):
        narratives.append("政治名人币")
    elif any(x in name or x in symbol for x in ['dog', 'cat', 'pepe', 'frog', '狗', '猫', '青蛙']):
        narratives.append("动物币")
    elif any(x in name or x in symbol for x in ['ai', 'gpt', 'bot', 'agent']):
        narratives.append("AI概念")
    elif any(x in name or x in symbol for x in ['game', 'play', '游戏']):
        narratives.append("游戏")
    else:
        narratives.append("MEME币")
    
    return ", ".join(narratives)

async def main():
    scanned = load_scanned()
    page_id = await get_page_id()
    
    if not page_id:
        print("❌ 无法连接到 Chrome DevTools", file=sys.stderr)
        return
    
    ws_url = f"{CHROME_WS_BASE}/devtools/page/{page_id}"
    
    async with websockets.connect(ws_url) as ws:
        results = []
        
        # 扫描 SOL 和 BSC
        for chain in ['sol', 'bsc']:
            tokens = await scan_gmgn_rank(ws, chain)
            
            for token in tokens:
                address = token.get('address')
                if not address: continue
                
                # 跳过已扫描的
                if address in scanned: continue
                
                # 获取 name（rank API 没有返回）
                if not token.get('name'):
                    params = get_common_params()
                    url = f"{GMGN_BASE}/vas/api/v1/search_v3?{params}&chain={chain}&q={address}"
                    data = await chrome_fetch(ws, url)
                    if data.get('code') == 0:
                        coins = data.get('data', {}).get('coins', [])
                        if coins:
                            token['name'] = coins[0].get('name')
                
                # 获取 bundler 数据
                if 'bundler_rate' not in token:
                    params = get_common_params()
                    url = f"{GMGN_BASE}/api/v1/token_stat/{chain}/{address}?{params}"
                    data = await chrome_fetch(ws, url)
                    if data.get('code') == 0:
                        stat = data.get('data', {})
                        token['bundler_rate'] = float(stat.get('top_bundler_trader_percentage', 0))
                
                # 筛选
                if not filter_token(token): continue
                
                # 格式化消息
                message = format_message(token)
                results.append(message)
                
                # 标记为已扫描
                scanned[address] = time.time()
        
        # 保存已扫描记录
        save_scanned(scanned)
        
        # 输出结果
        if results:
            print(json.dumps(results, ensure_ascii=False))
        else:
            print("[]")

if __name__ == "__main__":
    asyncio.run(main())

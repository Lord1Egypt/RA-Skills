#!/usr/bin/env python3
"""
获取股票实时行情 - 多数据源并行验证版本
支持：东方财富、新浪财经、腾讯财经、百度股市通、谷歌财经、雅虎财经等
"""

import requests
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 数据源配置
SOURCES = {
    'eastmoney': '东方财富',
    'sina': '新浪财经',
    'tencent': '腾讯财经',
    'baidu': '百度股市通',
    '163': '网易财经',
    'cnfol': '中金在线',
    'p5w': '全景网',
}

def get_price_eastmoney(symbol):
    """东方财富数据源"""
    try:
        if symbol.startswith('6'):
            market = '1'
        else:
            market = '0'
        
        url = "http://push2.eastmoney.com/api/qt/stock/get"
        params = {
            'secid': f'{market}.{symbol}',
            'fields': 'f43,f44,f45,f46,f57,f58,f169,f170,f152,f2,f3,f4,f5,f6,f60,f168'
        }
        
        response = requests.get(url, params=params, timeout=3)
        data = response.json()
        
        if data.get('data'):
            d = data['data']
            return {
                'source': '东方财富',
                'source_id': 'eastmoney',
                'name': d.get('f58', ''),
                'price': d.get('f2', 0),
                'change_pct': d.get('f3', 0),
                'change_amt': d.get('f4', 0),
                'open': d.get('f46', 0),
                'high': d.get('f44', 0),
                'low': d.get('f45', 0),
                'prev_close': d.get('f60', 0),
                'volume': d.get('f6', 0),
                'amount': d.get('f43', 0),
                'limit_up': d.get('f169', 0),
                'limit_down': d.get('f170', 0),
                'timestamp': datetime.now()
            }
    except Exception as e:
        pass
    return None

def get_price_sina(symbol):
    """新浪财经数据源"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://hq.sinajs.cn/list={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('=')[1].strip('"').split(',')
            if len(parts) >= 32:
                price = float(parts[3])
                prev_close = float(parts[2])
                return {
                    'source': '新浪财经',
                    'source_id': 'sina',
                    'name': parts[0],
                    'price': price,
                    'change_pct': float(parts[26]) * 100,
                    'change_amt': price - prev_close,
                    'open': float(parts[1]),
                    'high': float(parts[4]),
                    'low': float(parts[5]),
                    'prev_close': prev_close,
                    'volume': float(parts[8]),
                    'amount': float(parts[9]),
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_price_tencent(symbol):
    """腾讯财经数据源"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://qt.gtimg.cn/q={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('"')[1].split('~')
            if len(parts) >= 50:
                price = float(parts[3])
                return {
                    'source': '腾讯财经',
                    'source_id': 'tencent',
                    'name': parts[1],
                    'price': price,
                    'change_pct': float(parts[32]),
                    'change_amt': float(parts[4]),
                    'open': float(parts[5]),
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                    'prev_close': float(parts[4]),
                    'volume': float(parts[6]),
                    'amount': float(parts[37]),
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_price_163(symbol):
    """网易财经数据源"""
    try:
        market = '0' if symbol.startswith('6') else '1'
        url = f"http://api.money.126.net/data/feed/{market}{symbol},money.api"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200:
            text = response.text.replace('_ntes_quote_callback(', '').rstrip(')')
            data = json.loads(text)
            if data.get('data'):
                d = data['data'][f'{market}{symbol}']
                price = d.get('price', 0)
                prev_close = d.get('yestclose', 0)
                return {
                    'source': '网易财经',
                    'source_id': '163',
                    'name': d.get('name', ''),
                    'price': price,
                    'change_pct': d.get('percent', 0) * 100,
                    'change_amt': price - prev_close,
                    'open': d.get('open', 0),
                    'high': d.get('high', 0),
                    'low': d.get('low', 0),
                    'prev_close': prev_close,
                    'volume': d.get('volume', 0),
                    'amount': d.get('turnover', 0),
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_price_cnfol(symbol):
    """中金在线数据源"""
    try:
        market = '600' if symbol.startswith('6') else '000'
        url = f"http://quote.cnfol.com/{market}{symbol}.xml"
        response = requests.get(url, timeout=3)
        response.encoding = 'utf-8'
        
        if response.status_code == 200 and '<quote>' in response.text:
            text = response.text
            # 简单解析 XML
            def extract(tag):
                start = text.find(f'<{tag}>') + len(tag) + 2
                end = text.find(f'</{tag}>')
                return text[start:end] if start > len(tag)+1 and end > start else None
            
            price = float(extract('now') or 0)
            prev_close = float(extract('lastclose') or 0)
            return {
                'source': '中金在线',
                'source_id': 'cnfol',
                'name': extract('name') or '',
                'price': price,
                'change_pct': float(extract('increaserate') or 0) * 100,
                'change_amt': price - prev_close,
                'open': float(extract('open') or 0),
                'high': float(extract('high') or 0),
                'low': float(extract('low') or 0),
                'prev_close': prev_close,
                'timestamp': datetime.now()
            }
    except Exception as e:
        pass
    return None

def get_price_p5w(symbol):
    """全景网数据源"""
    try:
        market = 'SH' if symbol.startswith('6') else 'SZ'
        url = f"http://quote.p5w.net/json/quote/quoteData.jsp?symbol={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                d = data['data']
                price = float(d.get('newPrice', 0))
                prev_close = float(d.get('preClose', 0))
                return {
                    'source': '全景网',
                    'source_id': 'p5w',
                    'name': d.get('name', ''),
                    'price': price,
                    'change_pct': ((price - prev_close) / prev_close * 100) if prev_close else 0,
                    'change_amt': price - prev_close,
                    'open': float(d.get('openPrice', 0)),
                    'high': float(d.get('highPrice', 0)),
                    'low': float(d.get('lowPrice', 0)),
                    'prev_close': prev_close,
                    'volume': float(d.get('volume', 0)),
                    'amount': float(d.get('turnover', 0)),
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_price_baidu(symbol):
    """百度股市通数据源"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"https://finance.pae.baidu.com/api/getstockinfo"
        params = {
            'symbol': f'{market}{symbol}',
            'type': 'stock'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://gushitong.baidu.com/'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=3)
        data = response.json()
        
        if data.get('Result'):
            d = data['Result']
            price = float(d.get('price', 0))
            return {
                'source': '百度股市通',
                'source_id': 'baidu',
                'name': d.get('name', ''),
                'price': price,
                'change_pct': float(d.get('changePercent', 0)),
                'change_amt': float(d.get('change', 0)),
                'open': float(d.get('open', 0)),
                'high': float(d.get('high', 0)),
                'low': float(d.get('low', 0)),
                'prev_close': float(d.get('prevClose', 0)),
                'volume': float(d.get('volume', 0)),
                'amount': float(d.get('amount', 0)),
                'timestamp': datetime.now()
            }
    except Exception as e:
        pass
    return None

def get_price_xueqiu(symbol):
    """雪球财经数据源"""
    try:
        market = 'SH' if symbol.startswith('6') else 'SZ'
        url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={market}{symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://xueqiu.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        
        if data.get('data') and data['data'].get('quote'):
            d = data['data']['quote']
            price = float(d.get('current', 0))
            return {
                'source': '雪球财经',
                'source_id': 'xueqiu',
                'name': d.get('name', ''),
                'price': price,
                'change_pct': float(d.get('percent', 0)),
                'change_amt': float(d.get('chg', 0)),
                'open': float(d.get('open', 0)),
                'high': float(d.get('high', 0)),
                'low': float(d.get('low', 0)),
                'prev_close': float(d.get('last_close', 0)),
                'volume': float(d.get('volume', 0)),
                'amount': float(d.get('amount', 0)),
                'timestamp': datetime.now()
            }
    except Exception as e:
        pass
    return None

def get_price_hexin(symbol):
    """同花顺数据源"""
    try:
        market = '1' if symbol.startswith('6') else '0'
        url = f"http://d.10jqka.com.cn/v6/line/hs_{market}{symbol}/11/last.js"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://quote.10jqka.com.cn/'
        }
        
        response = requests.get(url, headers=headers, timeout=3)
        response.encoding = 'utf-8'
        
        if response.status_code == 200 and '=' in response.text:
            text = response.text.replace(f'var hq_{market}{symbol}="', '').rstrip('";')
            parts = text.split(',')
            if len(parts) >= 10:
                price = float(parts[7])
                prev_close = float(parts[2])
                return {
                    'source': '同花顺',
                    'source_id': 'hexin',
                    'name': parts[0],
                    'price': price,
                    'change_pct': float(parts[8]) if len(parts) > 8 else 0,
                    'change_amt': price - prev_close,
                    'open': float(parts[3]),
                    'high': float(parts[4]),
                    'low': float(parts[5]),
                    'prev_close': prev_close,
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_price_dazhihui(symbol):
    """大智慧数据源"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://hq.gw.com.cn/mkt/{market}{symbol}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        
        response = requests.get(url, headers=headers, timeout=3)
        response.encoding = 'utf-8'
        
        if response.status_code == 200 and '=' in response.text:
            text = response.text.split('=')[1].strip('"[]').replace('"', '')
            parts = text.split(',')
            if len(parts) >= 10:
                price = float(parts[3])
                prev_close = float(parts[2])
                return {
                    'source': '大智慧',
                    'source_id': 'dazhihui',
                    'name': parts[0],
                    'price': price,
                    'change_pct': ((price - prev_close) / prev_close * 100) if prev_close else 0,
                    'change_amt': price - prev_close,
                    'open': float(parts[1]),
                    'high': float(parts[4]),
                    'low': float(parts[5]),
                    'prev_close': prev_close,
                    'timestamp': datetime.now()
                }
    except Exception as e:
        pass
    return None

def get_all_prices(symbol, timeout=20, retries=2):
    """并行获取所有数据源价格（带重试）"""
    
    source_funcs = [
        get_price_eastmoney,
        get_price_sina,
        get_price_tencent,
        get_price_163,
        get_price_cnfol,
        get_price_p5w,
        get_price_baidu,
        get_price_xueqiu,
        get_price_hexin,
        get_price_dazhihui,
    ]
    
    results = []
    
    for attempt in range(retries + 1):
        if attempt > 0:
            time.sleep(1 * attempt)  # 递增延迟
        
        with ThreadPoolExecutor(max_workers=7) as executor:
            future_to_source = {
                executor.submit(func, symbol): func.__name__ 
                for func in source_funcs
            }
            
            for future in as_completed(future_to_source, timeout=timeout):
                try:
                    result = future.result()
                    if result and result['price'] > 0:
                        # 避免重复添加同一数据源
                        if not any(r['source_id'] == result['source_id'] for r in results):
                            results.append(result)
                except Exception:
                    pass
        
        # 如果已经有 5 个以上数据源，认为足够
        if len(results) >= 5:
            break
    
    # 按价格排序，找出异常值
    if results:
        results.sort(key=lambda x: x['price'])
    
    return results

def validate_prices(results):
    """验证数据源一致性"""
    if len(results) < 2:
        return {
            'valid': len(results) >= 1,
            'consensus': results[0]['price'] if results else None,
            'outliers': [],
            'avg_price': results[0]['price'] if results else None,
            'std_dev': 0,
            'reliability': 'low' if len(results) < 3 else 'medium' if len(results) < 5 else 'high'
        }
    
    prices = [r['price'] for r in results]
    avg_price = sum(prices) / len(prices)
    
    # 计算标准差
    variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
    std_dev = variance ** 0.5
    
    # 找出异常值（超过 2 个标准差）
    outliers = []
    valid_results = []
    for r in results:
        if abs(r['price'] - avg_price) > 2 * std_dev:
            outliers.append(r['source'])
        else:
            valid_results.append(r)
    
    # 使用有效数据重新计算
    if valid_results:
        valid_prices = [r['price'] for r in valid_results]
        consensus = sum(valid_prices) / len(valid_prices)
    else:
        consensus = avg_price
    
    return {
        'valid': True,
        'consensus': consensus,
        'outliers': outliers,
        'avg_price': avg_price,
        'std_dev': std_dev,
        'reliability': 'low' if len(valid_results) < 3 else 'medium' if len(valid_results) < 5 else 'high',
        'valid_sources': len(valid_results),
        'total_sources': len(results)
    }

def calculate_profit(current_price, cost_price, shares):
    """计算持仓盈亏"""
    profit = (current_price - cost_price) * shares
    profit_pct = (current_price - cost_price) / cost_price * 100
    return profit, profit_pct

def main():
    symbol = '600769'
    cost_price = 14.87
    shares = 100
    target_profit = 17.50
    stop_loss = 13.65
    
    print(f"{'='*60}")
    print(f"  祥龙电业 ({symbol}) 多数据源行情验证")
    print(f"{'='*60}\n")
    print(f"数据时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 获取所有数据源
    print("📡 正在获取数据源...")
    results = get_all_prices(symbol, timeout=10)
    
    if not results:
        print("❌ 所有数据源均失败，请稍后重试")
        return
    
    print(f"✅ 成功获取 {len(results)} 个数据源\n")
    
    # 显示各数据源价格
    print("📊 各数据源报价：")
    print(f"{'数据源':<12} {'价格':>10} {'涨跌幅':>10} {'状态':>8}")
    print("-" * 45)
    
    for r in results:
        status = "✅" if r['price'] > 0 else "❌"
        print(f"{r['source']:<12} ¥{r['price']:>8.2f} {r['change_pct']:>+9.2f}% {status:>8}")
    
    # 数据验证
    print("\n" + "="*60 + "\n")
    print("🔍 数据验证结果：")
    
    validation = validate_prices(results)
    
    print(f"  有效数据源：{validation.get('valid_sources', len(results))}/{len(results)}")
    print(f"  一致价格：¥{validation['consensus']:.2f}")
    print(f"  平均价格：¥{validation['avg_price']:.2f}")
    print(f"  标准差：¥{validation['std_dev']:.4f}")
    print(f"  可靠性：{validation['reliability'].upper()}")
    
    if validation['outliers']:
        print(f"  ⚠️ 异常数据源：{', '.join(validation['outliers'])}")
    
    # 使用共识价格
    current_price = validation['consensus']
    
    print("\n" + "="*60 + "\n")
    
    # 持仓盈亏
    profit, profit_pct = calculate_profit(current_price, cost_price, shares)
    
    print("💼 持仓盈亏：")
    print(f"  持仓数量：{shares} 股")
    print(f"  成本价：¥{cost_price:.2f}")
    print(f"  当前价：¥{current_price:.2f} (多数据源验证)")
    print(f"  持仓盈亏：¥{profit:.2f} ({profit_pct:+.2f}%)")
    
    print("\n🎯 条件单状态：")
    dist_to_profit = ((target_profit - current_price) / current_price * 100) if current_price < target_profit else -((current_price - target_profit) / current_price * 100)
    dist_to_loss = ((current_price - stop_loss) / current_price * 100) if current_price > stop_loss else -((stop_loss - current_price) / current_price * 100)
    
    print(f"  止盈价：¥{target_profit:.2f} (还需涨 {dist_to_profit:+.1f}%)")
    print(f"  止损价：¥{stop_loss:.2f} (还需跌 {dist_to_loss:+.1f}%)")
    
    if stop_loss < current_price < target_profit:
        print(f"  状态：✅ 正常监控中")
    elif current_price >= target_profit:
        print(f"  状态：🎉 已触发止盈！")
    else:
        print(f"  状态：🛑 已触发止损！")
    
    print("\n" + "="*60)
    print(f"✨ 数据获取成功！可靠性：{validation['reliability'].upper()}")

if __name__ == '__main__':
    main()

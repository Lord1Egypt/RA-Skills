#!/usr/bin/env python3
"""
获取股票实时行情 - 生产版本
数据源优先级：腾讯财经 > 东方财富 > 新浪财经
"""

import requests
import json
import time
from datetime import datetime

def get_price_tencent(symbol):
    """腾讯财经（最稳定）"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://qt.gtimg.cn/q={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('"')[1].split('~')
            if len(parts) >= 50:
                price = float(parts[3])
                if price > 0:
                    return {
                        'source': '腾讯财经',
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
        print(f"腾讯财经失败：{e}")
    return None

def get_price_eastmoney_v2(symbol):
    """东方财富（备用）"""
    try:
        market = '1' if symbol.startswith('6') else '0'
        url = "http://push2.eastmoney.com/api/qt/stock/get"
        params = {
            'secid': f'{market}.{symbol}',
            'fields': 'f57,f58,f2,f3,f4,f46,f44,f45,f60,f6,f43,f169,f170'
        }
        response = requests.get(url, params=params, timeout=3)
        data = response.json()
        
        if data.get('data'):
            d = data['data']
            price = d.get('f2', 0)
            if price and price > 0:
                return {
                    'source': '东方财富',
                    'name': d.get('f58', ''),
                    'price': price,
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
        print(f"东方财富失败：{e}")
    return None

def get_price_sina_v2(symbol):
    """新浪财经（备用，可能需要特殊处理）"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://hq.sinajs.cn/list={market}{symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://finance.sina.com.cn/'
        }
        response = requests.get(url, headers=headers, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('=')[1].strip('"').split(',')
            if len(parts) >= 32:
                price = float(parts[3])
                if price > 0:
                    prev_close = float(parts[2])
                    return {
                        'source': '新浪财经',
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
        print(f"新浪财经失败：{e}")
    return None

def get_stock_price(symbol, retry=3):
    """获取股票价格（多数据源自动切换）"""
    
    sources = [
        get_price_tencent,      # 优先腾讯
        get_price_eastmoney_v2, # 备用东方财富
        get_price_sina_v2,      # 备用新浪
    ]
    
    for i in range(retry):
        for source_func in sources:
            result = source_func(symbol)
            if result and result['price'] > 0:
                return result
            time.sleep(0.3)
        time.sleep(1)
    
    return None

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
    print(f"  祥龙电业 ({symbol}) 实时行情")
    print(f"{'='*60}\n")
    print(f"数据时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 获取行情
    data = get_stock_price(symbol)
    
    if not data:
        print("❌ 所有数据源均失败，请稍后重试")
        return
    
    print(f"📊 数据来源：{data['source']} ✅")
    print(f"💰 当前价格：¥{data['price']:.2f}")
    print(f"📈 涨跌幅：{data['change_pct']:+.2f}%")
    print(f"💵 涨跌额：¥{data['change_amt']:+.2f}")
    print(f"📉 今开：¥{data['open']:.2f}")
    print(f"📈 最高：¥{data['high']:.2f}")
    print(f"📉 最低：¥{data['low']:.2f}")
    print(f"📊 昨收：¥{data['prev_close']:.2f}")
    
    if 'limit_up' in data:
        print(f"📈 涨停价：¥{data['limit_up']:.2f}")
        print(f"📉 跌停价：¥{data['limit_down']:.2f}")
    
    print("\n" + "="*60 + "\n")
    
    # 持仓盈亏
    profit, profit_pct = calculate_profit(data['price'], cost_price, shares)
    
    print("💼 持仓盈亏：")
    print(f"  持仓数量：{shares} 股")
    print(f"  成本价：¥{cost_price:.2f}")
    print(f"  当前价：¥{data['price']:.2f}")
    print(f"  持仓盈亏：¥{profit:.2f} ({profit_pct:+.2f}%)")
    
    print("\n🎯 条件单状态：")
    dist_to_profit = ((target_profit - data['price']) / data['price'] * 100) if data['price'] < target_profit else -((data['price'] - target_profit) / data['price'] * 100)
    dist_to_loss = ((data['price'] - stop_loss) / data['price'] * 100) if data['price'] > stop_loss else -((stop_loss - data['price']) / data['price'] * 100)
    
    print(f"  止盈价：¥{target_profit:.2f} (还需涨 {dist_to_profit:+.1f}%)")
    print(f"  止损价：¥{stop_loss:.2f} (还需跌 {dist_to_loss:+.1f}%)")
    
    if stop_loss < data['price'] < target_profit:
        print(f"  状态：✅ 正常监控中")
    elif data['price'] >= target_profit:
        print(f"  状态：🎉 已触发止盈！")
    else:
        print(f"  状态：🛑 已触发止损！")
    
    print("\n" + "="*60)
    print(f"✨ 数据获取成功！")

if __name__ == '__main__':
    main()

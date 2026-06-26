#!/usr/bin/env python3
"""
每日股市复盘 - 自动获取行情和新闻
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def get_market_summary():
    """获取大盘指数"""
    indices = {
        '上证指数': '1.000001',
        '深证成指': '0.399001',
        '创业板指': '0.399006',
        '沪深300': '1.000300',
    }
    
    results = {}
    for name, secid in indices.items():
        try:
            url = "http://push2.eastmoney.com/api/qt/stock/get"
            params = {'secid': secid, 'fields': 'f2,f3,f4,f5,f6'}
            response = requests.get(url, params=params, timeout=3)
            data = response.json()
            if data.get('data'):
                d = data['data']
                results[name] = {
                    'price': d.get('f2', 0),
                    'change_pct': d.get('f3', 0),
                    'change_amt': d.get('f4', 0),
                    'high': d.get('f5', 0),
                    'low': d.get('f6', 0),
                }
        except:
            pass
    
    return results

def get_hot_stocks():
    """获取涨停股和热门股票"""
    try:
        # 涨停股
        url = "http://push2.eastmoney.com/api/qt/clist/get"
        params = {
            'pn': '1',
            'pz': '50',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:0 t:81 s:2048',
            'fields': 'f12,f14,f2,f3,f4,f5,f6'
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if data.get('data') and data['data'].get('diff'):
            stocks = data['data']['diff'][:20]  # 前 20 只
            return stocks
    except Exception as e:
        print(f"获取涨停股失败：{e}")
    
    return []

def get_finance_news():
    """获取财经新闻"""
    news_list = []
    
    try:
        # 新浪财经 RSS
        url = "http://finance.sina.com.cn/rss/finance.xml"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('item')[:10]
            for item in items:
                news_list.append({
                    'title': item.title.text if item.title else '',
                    'link': item.link.text if item.link else '',
                    'time': item.pubDate.text if item.pubDate else '',
                    'source': '新浪财经'
                })
    except Exception as e:
        print(f"获取新浪新闻失败：{e}")
    
    try:
        # 东方财富新闻
        url = "http://api.eastmoney.com/v1/news/list"
        params = {'type': 'cj', 'page': 1, 'page_size': 10}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if data.get('Data'):
            for item in data['Data'][:10]:
                news_list.append({
                    'title': item.get('Title', ''),
                    'link': f"https://www.eastmoney.com/a/{item.get('ID', '')}.html",
                    'time': item.get('UpdateTime', ''),
                    'source': '东方财富'
                })
    except Exception as e:
        print(f"获取东方财富新闻失败：{e}")
    
    return news_list[:15]  # 最多 15 条

def get_stock_price(symbol):
    """获取个股价格"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://qt.gtimg.cn/q={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('"')[1].split('~')
            if len(parts) >= 50:
                return {
                    'name': parts[1],
                    'price': float(parts[3]),
                    'change_pct': float(parts[32]),
                    'volume': float(parts[6]),
                }
    except:
        pass
    return None

def main():
    print("="*70)
    print("  📊 每日股市复盘报告")
    print("="*70)
    print(f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. 大盘指数
    print("="*70)
    print("📈 一、大盘指数")
    print("="*70)
    
    indices = get_market_summary()
    print(f"{'指数名称':<12} {'当前点位':>12} {'涨跌幅':>10} {'涨跌额':>10}")
    print("-"*50)
    
    for name, data in indices.items():
        print(f"{name:<12} {data['price']:>12.2f} {data['change_pct']:>+10.2f}% {data['change_amt']:>+10.2f}")
    
    print("\n")
    
    # 2. 涨停股
    print("="*70)
    print("🔥 二、涨停股 TOP20")
    print("="*70)
    
    stocks = get_hot_stocks()
    if stocks:
        print(f"{'代码':<10} {'名称':<12} {'价格':>10} {'涨幅':>10} {'成交量':>12}")
        print("-"*60)
        for s in stocks[:20]:
            code = s.get('f12', '')
            name = s.get('f14', '')
            price = s.get('f2', 0)
            change = s.get('f3', 0)
            volume = s.get('f6', 0)
            print(f"{code:<10} {name:<12} {price:>10.2f} {change:>10.2f}% {volume:>10.0f}")
    else:
        print("暂无数据")
    
    print("\n")
    
    # 3. 财经新闻
    print("="*70)
    print("📰 三、重要财经新闻")
    print("="*70)
    
    news = get_finance_news()
    if news:
        for i, n in enumerate(news[:10], 1):
            print(f"{i:2d}. [{n['source']}] {n['title']}")
            print(f"    {n['link']}")
            print()
    else:
        print("暂无新闻数据")
    
    print("\n")
    
    # 4. 持仓股跟踪
    print("="*70)
    print("💼 四、持仓股跟踪")
    print("="*70)
    
    holdings = [
        {'symbol': '600769', 'name': '祥龙电业', 'cost': 14.87, 'shares': 100},
    ]
    
    print(f"{'股票':<12} {'成本价':>10} {'现价':>10} {'盈亏':>10} {'盈亏率':>10}")
    print("-"*60)
    
    for h in holdings:
        data = get_stock_price(h['symbol'])
        if data:
            current_price = data['price']
            profit = (current_price - h['cost']) * h['shares']
            profit_pct = (current_price - h['cost']) / h['cost'] * 100
            
            status = "📈" if profit > 0 else "📉" if profit < 0 else "➖"
            print(f"{h['name']:<12} {h['cost']:>10.2f} {current_price:>10.2f} "
                  f"{profit:>10.2f} {profit_pct:>9.2f}% {status}")
        else:
            print(f"{h['name']:<12} {h['cost']:>10.2f} {'获取失败':>10} {'-':>10} {'-':>10}")
    
    print("\n" + "="*70)
    print("✨ 复盘完成！")
    print("="*70)

if __name__ == '__main__':
    main()

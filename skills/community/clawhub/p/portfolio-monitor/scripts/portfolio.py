#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资组合监控脚本
"""

import yfinance as yf
import json
import sys
from datetime import datetime


def load_portfolio():
    """加载持仓配置"""
    try:
        with open('/Users/apple/.openclaw/workspace/memory/portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果没有配置，返回默认示例
        return {
            "settings": {"currency": "USD", "alert_threshold": 0.05},
            "holdings": [
                {"symbol": "0700.HK", "name": "腾讯控股", "shares": 100, "cost": 500.00, "currency": "HKD"},
                {"symbol": "AAPL", "name": "苹果", "shares": 10, "cost": 180.00, "currency": "USD"},
                {"symbol": "BTC-USD", "name": "比特币", "shares": 0.5, "cost": 45000.00, "currency": "USD"},
                {"symbol": "ETH-USD", "name": "以太坊", "shares": 2.0, "cost": 2500.00, "currency": "USD"},
            ]
        }


def get_price(symbol):
    """获取实时价格"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='1d')
        if hist is not None and len(hist) > 0:
            return hist['Close'].iloc[-1]
    except:
        pass
    return None


def format_currency(amount, currency='$'):
    """格式化货币"""
    if currency in ['HKD', 'HK$']:
        return f'HK${amount:.2f}'
    return f'${amount:.2f}'


def analyze_portfolio():
    """分析投资组合"""
    portfolio = load_portfolio()
    holdings = portfolio.get('holdings', [])
    settings = portfolio.get('settings', {})
    
    print(f"\n{'='*60}")
    print(f"📊 投资组合监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print('='*60)
    
    total_value = 0
    total_cost = 0
    results = []
    
    for holding in holdings:
        symbol = holding['symbol']
        name = holding['name']
        shares = holding['shares']
        cost = holding['cost']
        currency = holding.get('currency', 'USD')
        
        # 获取实时价格
        price = get_price(symbol)
        
        if price is None:
            print(f"⚠️ {name}({symbol}): 无法获取价格")
            continue
        
        # 计算
        value = price * shares
        cost_total = cost * shares
        profit = value - cost_total
        profit_pct = (profit / cost_total * 100) if cost_total > 0 else 0
        
        total_value += value
        total_cost += cost_total
        
        results.append({
            'name': name,
            'symbol': symbol,
            'shares': shares,
            'price': price,
            'value': value,
            'cost': cost,
            'cost_total': cost_total,
            'profit': profit,
            'profit_pct': profit_pct,
            'currency': currency
        })
        
        # 打印每只股票
        trend = "📈" if profit >= 0 else "📉"
        print(f"\n{trend} {name}({symbol})")
        print(f"   数量: {shares}股 | 成本: {format_currency(cost, currency)}")
        print(f"   现价: {format_currency(price, currency)} | 市值: {format_currency(value, currency)}")
        print(f"   盈亏: {format_currency(profit, currency)} ({profit_pct:+.2f}%)")
        
        # 提醒
        threshold = settings.get('alert_threshold', 0.05)
        if abs(profit_pct) > threshold * 100:
            if profit_pct > 0:
                print(f"   🔔 提醒: 涨幅超过{int(threshold*100)}%")
            else:
                print(f"   🔔 提醒: 跌幅超过{int(threshold*100)}%")
    
    # 总计
    total_profit = total_value - total_cost
    total_profit_pct = (total_profit / total_cost * 100) if total_cost > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"💰 总资产: {format_currency(total_value)}")
    print(f"💵 总成本: {format_currency(total_cost)}")
    
    trend = "📈" if total_profit >= 0 else "📉"
    print(f"{trend} 总盈亏: {format_currency(total_profit)} ({total_profit_pct:+.2f}%)")
    print('='*60)
    
    # 保存状态
    state = {
        'last_update': datetime.now().isoformat(),
        'total_value': total_value,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'total_profit_pct': total_profit_pct,
        'holdings': [{'symbol': r['symbol'], 'price': r['price'], 'profit_pct': r['profit_pct']} for r in results]
    }
    
    with open('/Users/apple/.openclaw/workspace/memory/portfolio_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    return state


def main():
    # 可以传入参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--add':
            # 添加持仓
            print("添加持仓功能待开发")
        elif sys.argv[1] == '--report':
            # 生成报告
            print("报告功能待开发")
        else:
            print("未知参数")
    else:
        # 默认运行监控
        analyze_portfolio()


if __name__ == "__main__":
    main()

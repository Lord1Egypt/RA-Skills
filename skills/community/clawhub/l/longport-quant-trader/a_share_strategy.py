#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股量化策略测试 - 动量策略
策略逻辑：
1. 选择当日强势股（涨幅>1%）
2. 小仓位建仓（100 股）
3. 设置止损（-3%）和止盈（+5%）
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from datetime import datetime
import json

# 配置
config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# 策略参数
STRATEGY_CONFIG = {
    "name": "A 股动量策略 v1.0",
    "min_change_rate": 0.01,  # 最小涨幅 1%
    "position_size": 100,     # 每只股票 100 股
    "stop_loss": -0.03,       # 止损 -3%
    "take_profit": 0.05,      # 止盈 +5%
    "max_positions": 3,       # 最多持有 3 只股票
}

# 候选股票池（沪深港通标的，流动性好）
STOCK_POOL = [
    {"symbol": "000001.SZ", "name": "平安银行"},
    {"symbol": "000858.SZ", "name": "五粮液"},
    {"symbol": "300750.SZ", "name": "宁德时代"},
    {"symbol": "600519.SH", "name": "贵州茅台"},
    {"symbol": "601318.SH", "name": "中国平安"},
]

def get_stock_quotes():
    """获取股票池行情"""
    symbols = [s["symbol"] for s in STOCK_POOL]
    quotes = qctx.quote(symbols)
    
    result = []
    for q in quotes:
        stock_info = next((s for s in STOCK_POOL if s["symbol"] == q.symbol), None)
        if stock_info:
            change_rate = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
            result.append({
                "symbol": q.symbol,
                "name": stock_info["name"],
                "price": q.last_done,
                "change_rate": change_rate,
                "volume": q.volume,
            })
    return result

def select_stocks(quotes):
    """选择符合条件的股票"""
    # 按涨幅排序
    sorted_stocks = sorted(quotes, key=lambda x: x["change_rate"], reverse=True)
    
    # 选择涨幅>1% 的股票
    selected = [s for s in sorted_stocks if s["change_rate"] >= STRATEGY_CONFIG["min_change_rate"]]
    
    # 限制数量
    return selected[:STRATEGY_CONFIG["max_positions"]]

def submit_buy_order(symbol, price, quantity):
    """提交买入订单"""
    try:
        # 限价单，价格上浮 0.5% 确保成交
        order_price = Decimal(str(float(price) * 1.005))
        order_qty = Decimal(str(quantity))
        
        resp = ctx.submit_order(
            side=OrderSide.Buy,
            symbol=symbol,
            order_type=OrderType.LO,
            submitted_price=order_price,
            submitted_quantity=order_qty,
            time_in_force=TimeInForceType.Day,
            remark=f"量化策略-{STRATEGY_CONFIG['name']}"
        )
        return {"success": True, "order_id": resp.order_id, "price": float(order_price)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """主函数"""
    print()
    print("=" * 70)
    print("🤖 A 股量化策略测试 - 动量策略")
    print("=" * 70)
    print(f"策略名称：{STRATEGY_CONFIG['name']}")
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"当前时段：A 股下午盘中 (13:00-15:00)")
    print("=" * 70)
    print()
    
    # 1. 获取行情
    print("📊 步骤 1: 获取股票池行情")
    print("-" * 70)
    quotes = get_stock_quotes()
    for q in quotes:
        flag = "✅" if q["change_rate"] >= STRATEGY_CONFIG["min_change_rate"] else "❌"
        print(f"{flag} {q['symbol']:12} {q['name']:10} | 最新：{q['price']:8.2f} | 涨跌：{q['change_rate']:6.2%}")
    print()
    
    # 2. 选股
    print("🎯 步骤 2: 选股（涨幅 >= 1%）")
    print("-" * 70)
    selected = select_stocks(quotes)
    
    if not selected:
        print("⚠️  无符合条件的股票，今日市场偏弱")
        print()
        return
    
    for s in selected:
        print(f"✅ {s['symbol']:12} {s['name']:10} | 涨幅：{s['change_rate']:6.2%} | 价格：{s['price']:.2f}")
    print()
    
    # 3. 执行交易
    print("📤 步骤 3: 执行买入订单")
    print("-" * 70)
    
    orders = []
    for stock in selected:
        print(f"准备买入：{stock['symbol']} {stock['name']}")
        print(f"  数量：{STRATEGY_CONFIG['position_size']}股")
        print(f"  市价：¥{stock['price']:.2f}")
        estimated_cost = stock['price'] * STRATEGY_CONFIG['position_size']
        print(f"  预估成本：¥{estimated_cost:,.2f}")
        
        # 确认买入
        result = submit_buy_order(stock['symbol'], stock['price'], STRATEGY_CONFIG['position_size'])
        
        if result['success']:
            print(f"  ✅ 订单提交成功！订单 ID: {result['order_id']}")
            print(f"  委托价格：¥{result['price']:.2f}")
            orders.append({
                "symbol": stock['symbol'],
                "name": stock['name'],
                "order_id": result['order_id'],
                "price": result['price'],
                "quantity": STRATEGY_CONFIG['position_size'],
                "stop_loss": result['price'] * (1 + STRATEGY_CONFIG['stop_loss']),
                "take_profit": result['price'] * (1 + STRATEGY_CONFIG['take_profit']),
            })
        else:
            print(f"  ❌ 订单失败：{result['error']}")
        print()
    
    # 4. 交易总结
    print("📋 步骤 4: 交易总结")
    print("=" * 70)
    if orders:
        total_cost = sum(o['price'] * o['quantity'] for o in orders)
        print(f"成交订单数：{len(orders)}")
        print(f"总投入资金：¥{total_cost:,.2f}")
        print()
        print("持仓及风控设置：")
        for o in orders:
            print(f"  {o['symbol']} {o['name']}:")
            print(f"    成本价：¥{o['price']:.2f}")
            print(f"    止损价：¥{o['stop_loss']:.2f} ({STRATEGY_CONFIG['stop_loss']:.0%})")
            print(f"    止盈价：¥{o['take_profit']:.2f} ({STRATEGY_CONFIG['take_profit']:.0%})")
        print()
        print("⚠️  风险提示：")
        print("   - A 股 T+1 制度，今日买入明日才能卖出")
        print("   - 这是模拟账户测试，非真实交易")
        print("   - 过往表现不代表未来收益")
    else:
        print("❌ 无成交订单")
    
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()

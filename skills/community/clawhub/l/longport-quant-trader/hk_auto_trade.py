#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股自动量化交易 - 实盘执行
策略：动量 + 均值回归 v2（最优版）
账户：LBPT10034472
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

# 策略参数（v2 最优版）
STRATEGY = {
    "momentum_threshold": 0.013,  # +1.3% 追涨
    "reversion_threshold": -0.023,  # -2.3% 抄底
    "position_size_pct": 0.15,  # 单笔 15% 仓位
    "stop_loss": -0.10,  # -10% 止损
    "take_profit": 0.20,  # +20% 止盈
    "max_positions": 5,
}

# 港股股票池
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯", "board_lot": 100},
    {"symbol": "9988.HK", "name": "阿里", "board_lot": 100},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100},
]

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

print("=" * 70)
print(f"🚀 港股自动量化交易 - {datetime.now().strftime('%H:%M:%S')}")
print("=" * 70)

# 1. 账户状态
print("\n💰 账户状态")
balances = ctx.account_balance()
cash = 0
for b in balances:
    cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
    print(f"可用现金：HKD {cash:,.2f}")
    print(f"净资产：HKD {b.net_assets:,.2f}")

# 2. 当前持仓
print("\n📈 当前持仓")
resp = ctx.stock_positions()
positions = []
for channel in resp.channels:
    for pos in channel.positions:
        positions.append({
            'symbol': pos.symbol,
            'qty': int(pos.quantity),
            'available': int(pos.available_quantity),
            'cost': float(pos.cost_price),
        })
        print(f"{pos.symbol}: {pos.quantity}股 @ HKD {pos.cost_price:.2f}")

# 3. 获取行情
print("\n📊 实时行情")
symbols = [s["symbol"] for s in HK_STOCKS]
quotes = qctx.quote(symbols)
quote_dict = {}

for q in quotes:
    change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
    quote_dict[q.symbol] = {
        'price': float(q.last_done),
        'change': float(change),
        'prev_close': float(q.prev_close),
    }
    print(f"{q.symbol}: HKD {q.last_done:.2f} ({change*100:+.2f}%)")

# 4. 检查持仓止盈止损
print("\n🎯 持仓交易信号")
trades_executed = 0

for pos in positions:
    symbol = pos['symbol']
    if symbol not in quote_dict:
        continue
    
    q = quote_dict[symbol]
    price = q['price']
    change = q['change'] * 100
    pnl_pct = (price - pos['cost']) / pos['cost'] * 100
    
    print(f"\n{symbol} 现价 HKD {price:.2f} ({change:+.2f}%) 盈亏 {pnl_pct:+.2f}%")
    
    # 止盈检查
    if pnl_pct >= STRATEGY['take_profit'] * 100:
        sell_qty = pos['available']
        print(f"  📤 止盈卖出 {sell_qty}股 @ HKD {price:.2f}")
        try:
            resp = ctx.submit_order(
                side=OrderSide.Sell,
                symbol=symbol,
                order_type=OrderType.LO,
                submitted_price=Decimal(f"{price:.2f}"),
                submitted_quantity=Decimal(str(sell_qty)),
                time_in_force=TimeInForceType.Day,
                remark=f"止盈 +{pnl_pct:.1f}%"
            )
            print(f"  ✅ 订单 ID: {resp.order_id}")
            trades_executed += 1
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    # 止损检查
    elif pnl_pct <= STRATEGY['stop_loss'] * 100:
        sell_qty = pos['available']
        print(f"  📤 止损卖出 {sell_qty}股 @ HKD {price:.2f}")
        try:
            resp = ctx.submit_order(
                side=OrderSide.Sell,
                symbol=symbol,
                order_type=OrderType.LO,
                submitted_price=Decimal(f"{price:.2f}"),
                submitted_quantity=Decimal(str(sell_qty)),
                time_in_force=TimeInForceType.Day,
                remark=f"止损 {pnl_pct:.1f}%"
            )
            print(f"  ✅ 订单 ID: {resp.order_id}")
            trades_executed += 1
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    else:
        print(f"  ⏸️ 持有（止盈 +20% / 止损 -10%）")

# 5. 买入信号（超跌抄底）
print("\n🔍 买入机会")
position_symbols = [p['symbol'] for p in positions]

for stock in HK_STOCKS:
    symbol = stock['symbol']
    if symbol in position_symbols:
        continue  # 已持仓
    
    if symbol not in quote_dict:
        continue
    
    q = quote_dict[symbol]
    change = q['change'] * 100
    
    # 均值回归（超跌抄底）
    if change <= STRATEGY['reversion_threshold'] * 100:
        print(f"\n{symbol} 超跌 {change:.2f}% - 买入信号！")
        
        # 计算买入数量
        buy_value = cash * STRATEGY['position_size_pct']
        qty = int(buy_value / q['price'])
        qty = (qty // stock['board_lot']) * stock['board_lot']
        
        if qty >= stock['board_lot'] and cash > 0:
            limit_price = q['price'] * 1.005  # 限价 +0.5%
            print(f"  📤 买入 {qty}股 @ HKD {limit_price:.2f}")
            print(f"     总额：HKD {qty * limit_price:.2f}")
            
            try:
                resp = ctx.submit_order(
                    side=OrderSide.Buy,
                    symbol=symbol,
                    order_type=OrderType.LO,
                    submitted_price=Decimal(f"{limit_price:.2f}"),
                    submitted_quantity=Decimal(str(qty)),
                    time_in_force=TimeInForceType.Day,
                    remark="超跌抄底"
                )
                print(f"  ✅ 订单 ID: {resp.order_id}")
                trades_executed += 1
            except Exception as e:
                print(f"  ❌ 失败：{e}")
        else:
            print(f"  ⚠️ 资金不足或数量不足 1 手")
    
    # 动量追涨
    elif change >= STRATEGY['momentum_threshold'] * 100:
        print(f"\n{symbol} 动量 +{change:.2f}% - 关注")

# 6. 订单汇总
print("\n" + "=" * 70)
print(f"✅ 本次执行 {trades_executed} 笔交易")
print("=" * 70)

# 7. 查看最新订单
print("\n📋 今日订单")
orders = ctx.today_orders()
for o in orders:
    status_map = {
        'NotReported': '待报送',
        'Submitted': '已报送',
        'PartiallyFilled': '部分成交',
        'Filled': '已成交',
        'Cancelled': '已取消',
        'Rejected': '已拒绝',
    }
    status = status_map.get(str(o.status), str(o.status))
    print(f"{o.symbol} {o.side} {o.quantity}股 - {status}")

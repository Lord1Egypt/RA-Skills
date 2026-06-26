#!/usr/bin/env python3
"""
港股模拟交易 v3 - 修复版
"""
from longport.openapi import TradeContext, QuoteContext, Config, SubType, PushQuote, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()
config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# 港股股票池
HK_STOCKS = {
    "700.HK": "腾讯控股",
    "9988.HK": "阿里巴巴",
    "3690.HK": "美团",
    "1211.HK": "比亚迪股份",
    "9618.HK": "京东",
}

# 策略配置
STRATEGY = {
    "name": "动量 + 均值回归混合策略",
    "momentum_threshold": 0.02,
    "reversion_threshold": -0.03,
    "position_size_pct": 0.1,
    "stop_loss": -0.05,
    "take_profit": 0.10,
}

print("\n" + "=" * 80)
print("🚀 港股模拟交易 v3")
print("=" * 80)
print(f"策略：{STRATEGY['name']}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# 1. 获取账户余额
print("\n💰 账户余额")
print("-" * 80)
balances = ctx.account_balance()
total_cash = 0
for bal in balances:
    if bal.currency == "HKD":
        print(f"可用现金：HKD {bal.cash_infos[0].available_cash:,.2f}")
        print(f"总现金：HKD {bal.total_cash:,.2f}")
        total_cash = float(bal.cash_infos[0].available_cash)

# 2. 获取持仓
print("\n📈 当前持仓")
print("-" * 80)
try:
    positions = ctx.positions()
    if positions:
        for pos in positions:
            print(f"{pos.symbol}: {pos.quantity}股")
    else:
        print("无持仓")
except:
    print("（持仓查询暂时不可用）")

# 3. 获取行情
print("\n📊 实时行情")
print("-" * 80)

quotes = {}
def on_quote(symbol: str, quote: PushQuote):
    quotes[symbol] = quote
    change = (quote.last_done - quote.prev_close) / quote.prev_close * 100 if quote.prev_close > 0 else 0
    name = HK_STOCKS.get(symbol, symbol)
    print(f"{symbol:10} | {name:8} | ${quote.last_done:>8.2f} | {change:>+7.2f}%")

qctx.set_on_quote(on_quote)
qctx.subscribe(list(HK_STOCKS.keys()), [SubType.Quote])
time.sleep(5)

# 4. 分析信号
print("\n🎯 策略信号")
print("-" * 80)

signals = []
for symbol, quote in quotes.items():
    name = HK_STOCKS.get(symbol, symbol)
    change = (quote.last_done - quote.prev_close) / quote.prev_close if quote.prev_close > 0 else 0
    
    # 动量信号
    if change >= STRATEGY["momentum_threshold"]:
        signals.append({
            "symbol": symbol,
            "name": name,
            "type": "BUY",
            "reason": f"动量：涨幅{change*100:.2f}%",
            "price": float(quote.last_done),
            "strength": min(10, int(change * 100)),
        })
    # 均值回归
    elif change <= STRATEGY["reversion_threshold"]:
        signals.append({
            "symbol": symbol,
            "name": name,
            "type": "BUY",
            "reason": f"均值回归：跌幅{change*100:.2f}%",
            "price": float(quote.last_done),
            "strength": min(10, int(abs(change) * 50)),
        })

signals.sort(key=lambda x: x["strength"], reverse=True)

if signals:
    print("\n推荐交易:")
    for i, sig in enumerate(signals[:3], 1):
        print(f"\n{i}. {sig['symbol']} {sig['name']}")
        print(f"   类型：{sig['type']}")
        print(f"   价格：${sig['price']:.2f}")
        print(f"   理由：{sig['reason']}")
        print(f"   强度：⭐{sig['strength']}/10")
else:
    print("\n⚠️ 暂无交易信号")

# 5. 模拟执行
print("\n" + "=" * 80)
print("📤 模拟交易执行")
print("-" * 80)

if signals and total_cash > 0:
    sig = signals[0]
    position_value = total_cash * STRATEGY["position_size_pct"]
    quantity = int(position_value / sig["price"])
    quantity = (quantity // 100) * 100  # 整手
    
    if quantity >= 100:
        total_amount = quantity * sig["price"]
        print(f"\n模拟买入：")
        print(f"  标的：{sig['symbol']} {sig['name']}")
        print(f"  数量：{quantity}股")
        print(f"  价格：${sig['price']:.2f}")
        print(f"  总金额：HKD {total_amount:,.2f}")
        print(f"  仓位：{total_amount/total_cash*100:.1f}%")
        print(f"\n⚠️  模拟模式：未实际下单")
    else:
        print(f"⚠️ 数量不足 1 手，跳过")
else:
    print("无可用信号或现金不足")

print("\n" + "=" * 80)
print("✅ 模拟完成")
print("=" * 80)

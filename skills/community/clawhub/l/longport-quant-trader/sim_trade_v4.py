#!/usr/bin/env python3
"""港股模拟交易 v4 - 最终修复版"""
from longport.openapi import TradeContext, QuoteContext, Config, SubType, PushQuote
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()
config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

HK_STOCKS = {"700.HK": "腾讯", "9988.HK": "阿里", "3690.HK": "美团", "1211.HK": "比亚迪", "9618.HK": "京东"}

print("\n" + "=" * 80)
print("🚀 港股模拟交易 v4")
print("=" * 80)

# 账户余额
balances = ctx.account_balance()
cash = 0
for bal in balances:
    if bal.currency == "HKD":
        cash = float(bal.cash_infos[0].available_cash)
        print(f"\n💰 可用现金：HKD {cash:,.2f}")

# 行情回调
quotes = {}
def on_quote(symbol: str, quote: PushQuote):
    quotes[symbol] = quote

qctx.set_on_quote(on_quote)
qctx.subscribe(list(HK_STOCKS.keys()), [SubType.Quote])
time.sleep(5)

# 分析信号
print("\n📊 行情与信号")
print("-" * 80)

for symbol, q in quotes.items():
    name = HK_STOCKS.get(symbol, symbol)
    # 使用正确的属性
    price = float(q.last_done)
    change = float(q.change if hasattr(q, 'change') else 0)
    change_pct = float(q.change_rate if hasattr(q, 'change_rate') else 0) * 100
    
    print(f"{symbol:10} | {name:6} | ${price:>8.2f} | {change_pct:>+7.2f}%")
    
    # 策略判断
    if change_pct <= -3.0:
        print(f"  ⭐⭐⭐ 均值回归信号！跌幅>{3}%")
    elif change_pct >= 2.0:
        print(f"  ⭐⭐ 动量信号！涨幅>{2}%")

print("\n" + "=" * 80)
print("✅ 分析完成")
print("=" * 80)

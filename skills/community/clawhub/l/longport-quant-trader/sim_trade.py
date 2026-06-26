#!/usr/bin/env python3
"""
港股模拟交易测试 - 验证策略并优化
"""
from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# 港股股票池
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯控股", "board_lot": 100},
    {"symbol": "9988.HK", "name": "阿里巴巴", "board_lot": 100},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100},
]

# 策略配置
STRATEGY = {
    "name": "动量 + 均值回归混合策略",
    "momentum_threshold": 0.02,  # 涨幅>2% 追涨
    "reversion_threshold": -0.03,  # 跌幅>3% 抄底
    "position_size_pct": 0.1,  # 单笔 10% 仓位
    "stop_loss": -0.05,  # 止损 -5%
    "take_profit": 0.10,  # 止盈 +10%
    "max_positions": 3,  # 最多持有 3 只股票
}

def get_account_status():
    """获取账户状态"""
    print("\n" + "=" * 80)
    print("📊 账户状态")
    print("=" * 80)
    
    try:
        balances = ctx.account_balance()
        total_cash = 0
        for balance in balances:
            print(f"  币种：{balance.currency}")
            if balance.cash_infos:
                cash = balance.cash_infos[0]
                print(f"  可用现金：{cash.available_cash:,.2f}")
                print(f"  总现金：{balance.total_cash:,.2f}")
                if balance.currency == "HKD":
                    total_cash = float(balance.total_cash)
        
        # 获取持仓
        positions = ctx.positions()
        total_position_value = 0
        print("\n📈 当前持仓:")
        if positions:
            for pos in positions:
                try:
                    quote = qctx.get_quote(pos.symbol)
                    price = float(quote.last_done)
                except:
                    price = 0
                
                market_value = pos.quantity * price
                total_position_value += market_value
                print(f"  {pos.symbol:12} | 数量：{pos.quantity:>6} | "
                      f"现价：{price:>8.2f} | 市值：{market_value:>12,.2f}")
        else:
            print("  无持仓")
        
        total_assets = total_cash + total_position_value
        print(f"\n💎 总资产：{total_assets:,.2f} HKD")
        print(f"   现金：{total_cash:,.2f} HKD")
        print(f"   持仓：{total_position_value:,.2f} HKD")
        
        return total_cash, total_position_value, positions
        
    except Exception as e:
        print(f"❌ 获取账户状态失败：{e}")
        return 0, 0, []

def get_stock_quotes():
    """获取股票池行情"""
    print("\n" + "=" * 80)
    print("📈 股票池行情")
    print("=" * 80)
    
    symbols = [s["symbol"] for s in HK_STOCKS]
    quotes = []
    
    for stock in HK_STOCKS:
        try:
            q = qctx.get_quote(stock["symbol"])
            change_rate = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
            quotes.append({
                "symbol": stock["symbol"],
                "name": stock["name"],
                "price": float(q.last_done),
                "prev_close": float(q.prev_close),
                "change_rate": float(change_rate),
                "board_lot": stock["board_lot"],
            })
            print(f"  {stock['symbol']:10} | {stock['name']:8} | "
                  f"${q.last_done:>8.2f} | {change_rate*100:>+7.2f}%")
        except Exception as e:
            print(f"  {stock['symbol']:10} | {stock['name']:8} | 获取失败")
    
    return quotes

def analyze_signals(quotes, positions):
    """分析交易信号"""
    print("\n" + "=" * 80)
    print("🎯 策略信号分析")
    print("=" * 80)
    
    signals = []
    position_symbols = [str(pos.symbol) for pos in positions]
    
    for q in quotes:
        symbol = q["symbol"]
        change = q["change_rate"]
        
        # 已持仓的股票检查止盈止损
        if symbol in position_symbols:
            # TODO: 需要记录持仓成本来计算盈亏
            pass
        
        # 动量信号（追涨）
        if change >= STRATEGY["momentum_threshold"]:
            signals.append({
                "symbol": symbol,
                "name": q["name"],
                "type": "BUY",
                "reason": f"动量信号：涨幅{change*100:.2f}% > {STRATEGY['momentum_threshold']*100}%",
                "price": q["price"],
                "strength": min(10, int(change * 100)),
            })
        
        # 均值回归信号（抄底）
        elif change <= STRATEGY["reversion_threshold"]:
            signals.append({
                "symbol": symbol,
                "name": q["name"],
                "type": "BUY",
                "reason": f"均值回归：跌幅{change*100:.2f}% < {STRATEGY['reversion_threshold']*100}%",
                "price": q["price"],
                "strength": min(10, int(abs(change) * 50)),
            })
    
    # 按强度排序
    signals.sort(key=lambda x: x["strength"], reverse=True)
    
    if signals:
        print("\n推荐交易（按信号强度）:")
        for i, sig in enumerate(signals[:5], 1):
            print(f"\n{i}. {sig['symbol']} {sig['name']}")
            print(f"   类型：{sig['type']}")
            print(f"   价格：${sig['price']:.2f}")
            print(f"   理由：{sig['reason']}")
            print(f"   强度：⭐{sig['strength']}/10")
    else:
        print("\n⚠️ 暂无交易信号，保持观望")
    
    return signals

def execute_signal(signal, cash_available):
    """执行交易信号"""
    print("\n" + "=" * 80)
    print("📤 执行交易")
    print("=" * 80)
    
    if signal["type"] != "BUY":
        print("非买入信号，跳过")
        return
    
    # 计算仓位
    position_value = cash_available * STRATEGY["position_size_pct"]
    quantity = int(position_value / signal["price"])
    
    # 调整为整手
    board_lot = next((s["board_lot"] for s in HK_STOCKS if s["symbol"] == signal["symbol"]), 100)
    quantity = (quantity // board_lot) * board_lot
    
    if quantity < board_lot:
        print(f"⚠️ 数量不足 1 手（{board_lot}股），跳过")
        return
    
    print(f"买入 {signal['symbol']} {signal['name']}")
    print(f"  数量：{quantity}股 ({quantity/board_lot}手)")
    print(f"  价格：${signal['price']:.2f}")
    print(f"  总金额：${quantity * signal['price']:.2f}")
    
    # 模拟模式：只输出不实际下单
    print("\n⚠️  模拟模式：未实际下单")
    # 如需实际下单，取消下面注释：
    # resp = ctx.submit_order(
    #     side=OrderSide.Buy,
    #     symbol=signal["symbol"],
    #     order_type=OrderType.LO,
    #     submitted_price=Decimal(str(signal["price"])),
    #     submitted_quantity=Decimal(str(quantity)),
    #     time_in_force=TimeInForceType.Day,
    #     remark=f"Strategy: {STRATEGY['name']}"
    # )
    # print(f"✅ 订单提交成功！订单 ID: {resp.order_id}")
    
    return quantity

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🚀 港股模拟交易测试")
    print("=" * 80)
    print(f"策略：{STRATEGY['name']}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 1. 获取账户状态
    cash, position_value, positions = get_account_status()
    
    # 2. 获取行情
    quotes = get_stock_quotes()
    
    # 3. 分析信号
    signals = analyze_signals(quotes, positions)
    
    # 4. 执行最强信号
    if signals and cash > 0:
        best_signal = signals[0]
        print(f"\n🎯 选择最强信号：{best_signal['symbol']}")
        execute_signal(best_signal, cash)
    
    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)

if __name__ == "__main__":
    main()

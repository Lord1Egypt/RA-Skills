#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股高频量化交易 v3.0 - 新风控版
策略：动量 + 突破 + 网格 + 回归
风控：分策略风控 + 移动止盈 + 8-12 只持仓
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os

load_dotenv()

# ========== 策略配置 v3.0 ==========
STRATEGIES = {
    "momentum": {
        "name": "动量追涨",
        "threshold": 0.013,
        "position_size": 0.10,
        "take_profit": 0.02,      # +2% 止盈
        "stop_loss": -0.01,       # -1% 止损
        "hold_time_min": 30,
        "max_positions": 3,
    },
    "breakout": {
        "name": "突破追涨",
        "threshold": 0.02,
        "volume_ratio": 3.0,
        "position_size": 0.12,
        "take_profit": None,      # 移动止盈
        "trailing_stop": 0.01,    # 回撤 1% 止盈
        "stop_loss": -0.015,      # -1.5% 止损
        "hold_time_min": 60,
        "max_positions": 3,
    },
    "grid": {
        "name": "网格交易",
        "grid_spacing": 0.025,
        "grid_levels": 6,
        "position_size": 0.08,
        "stop_loss": -0.05,       # 破网 -5% 止损
        "target_stocks": ["700.HK", "1211.HK"],
        "max_positions": 2,
    },
    "mean_reversion": {
        "name": "均值回归",
        "threshold": -0.023,
        "position_size": 0.10,
        "take_profit": 0.03,      # +3% 止盈
        "stop_loss": -0.015,      # -1.5% 止损
        "hold_time_min": 90,
        "max_positions": 2,
    },
}

# 股票池 + 策略匹配（8-12 只）
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯", "board_lot": 100, "type": "震荡", "strategy": "grid"},
    {"symbol": "9988.HK", "name": "阿里", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100, "type": "趋势", "strategy": "momentum"},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500, "type": "趋势", "strategy": "grid"},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    {"symbol": "1810.HK", "name": "小米", "board_lot": 500, "type": "高波", "strategy": "breakout"},
    {"symbol": "2015.HK", "name": "理想", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    {"symbol": "9866.HK", "name": "蔚来", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    {"symbol": "1024.HK", "name": "快手", "board_lot": 500, "type": "高波", "strategy": "momentum"},
    {"symbol": "9999.HK", "name": "网易", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    {"symbol": "2318.HK", "name": "平安", "board_lot": 500, "type": "金融", "strategy": "grid"},
    {"symbol": "1299.HK", "name": "友邦", "board_lot": 100, "type": "金融", "strategy": "momentum"},
]

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# 持仓跟踪（用于移动止盈）
position_tracker = {}

# ========== 风控函数 ==========

def check_take_profit(symbol, pos, current_price, strategy):
    """检查止盈（支持移动止盈）"""
    pnl_pct = (current_price - pos['cost']) / pos['cost'] * 100
    cfg = STRATEGIES[strategy]
    
    # 突破策略：移动止盈
    if strategy == "breakout":
        if symbol not in position_tracker:
            position_tracker[symbol] = {
                'highest_price': current_price,
                'trailing_stop': current_price * 0.99
            }
        
        tracker = position_tracker[symbol]
        
        # 更新最高价
        if current_price > tracker['highest_price']:
            tracker['highest_price'] = current_price
            tracker['trailing_stop'] = current_price * 0.99
        
        # 检查移动止盈
        if current_price <= tracker['trailing_stop'] and pnl_pct > 0:
            print(f"   📤 移动止盈！从高点 HKD {tracker['highest_price']:.2f} 回撤")
            return True, "移动止盈"
        
        # 检查止损
        if pnl_pct <= cfg['stop_loss'] * 100:
            print(f"   📤 止损！盈亏 {pnl_pct:.2f}%")
            return True, "止损"
        
        return False, None
    
    # 其他策略：固定止盈止损
    else:
        # 网格交易不检查固定止盈
        if strategy == "grid":
            # 只检查止损
            if pnl_pct <= cfg['stop_loss'] * 100:
                print(f"   📤 破网止损！盈亏 {pnl_pct:.2f}%")
                return True, "破网止损"
            return False, None
        
        if 'take_profit' in cfg and pnl_pct >= cfg['take_profit'] * 100:
            print(f"   📤 止盈！盈亏 +{pnl_pct:.2f}%")
            return True, "止盈"
        
        if pnl_pct <= cfg['stop_loss'] * 100:
            print(f"   📤 止损！盈亏 {pnl_pct:.2f}%")
            return True, "止损"
        
        # 时间止盈
        if 'entry_time' in pos:
            hold_time = (datetime.now() - pos['entry_time']).total_seconds() / 60
            if hold_time >= cfg['hold_time_min'] and pnl_pct > 0:
                print(f"   📤 时间止盈！持仓 {hold_time:.0f}分钟")
                return True, "时间止盈"
        
        return False, None

# ========== 交易执行 ==========

def submit_order(symbol, side, price, quantity, strategy, remark=""):
    """提交订单"""
    try:
        order_price = Decimal(str(round(price, 2)))
        order_qty = Decimal(str(quantity))
        order_type = OrderType.ELO if side == "Buy" else OrderType.LO
        
        resp = ctx.submit_order(
            side=OrderSide.Buy if side == "Buy" else OrderSide.Sell,
            symbol=symbol,
            order_type=order_type,
            submitted_price=order_price,
            submitted_quantity=order_qty,
            time_in_force=TimeInForceType.Day,
            remark=f"量化 v3-{strategy}"
        )
        return {"success": True, "order_id": resp.order_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== 主函数 ==========

def main():
    """主函数 - v3.0 新风控"""
    print()
    print("=" * 80)
    print("🚀 港股高频量化交易 v3.0 - 新风控版")
    print("=" * 80)
    print(f"账户：LBPT10034472")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"风控：分策略 + 移动止盈 + 8-12 只持仓")
    print("=" * 80)
    print()
    
    # 1. 账户状态
    print("💰 账户状态")
    print("-" * 80)
    balances = ctx.account_balance()
    cash = 0
    for b in balances:
        cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
        print(f"可用现金：HKD {cash:,.2f}")
        print(f"净资产：HKD {b.net_assets:,.2f}")
    print()
    
    # 2. 当前持仓
    print("📊 当前持仓")
    print("-" * 80)
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
    
    if not positions:
        print("无持仓")
    print()
    
    # 3. 扫描交易机会
    print("🔍 扫描机会 + 风控检查")
    print("-" * 80)
    symbols = [s["symbol"] for s in HK_STOCKS]
    quotes = qctx.quote(symbols)
    quote_dict = {q.symbol: q for q in quotes}
    
    trades_executed = 0
    position_symbols = [p['symbol'] for p in positions]
    
    # 检查持仓止盈止损
    for pos in positions:
        symbol = pos['symbol']
        if symbol not in quote_dict:
            continue
        
        q = quote_dict[symbol]
        price = float(q.last_done)
        
        # 找到对应策略
        stock_info = next((s for s in HK_STOCKS if s['symbol'] == symbol), None)
        if not stock_info:
            continue
        
        strategy = stock_info['strategy']
        
        print(f"\n{symbol} {stock_info['name']} 现价 HKD {price:.2f}")
        print(f"   策略：{STRATEGIES[strategy]['name']}")
        
        should_sell, reason = check_take_profit(symbol, pos, price, strategy)
        
        if should_sell:
            print(f"   原因：{reason}")
            result = submit_order(symbol, "Sell", price, pos['available'], strategy, reason)
            if result["success"]:
                print(f"   ✅ 订单 ID: {result['order_id']}")
                trades_executed += 1
                # 清除跟踪
                if symbol in position_tracker:
                    del position_tracker[symbol]
    
    # 4. 买入机会
    print("\n\n🔍 买入机会")
    print("-" * 80)
    
    # 检查持仓数量
    current_positions = len(position_symbols)
    max_positions = 12  # 新风控：最多 12 只
    
    if current_positions >= max_positions:
        print(f"⚠️  持仓已达上限 ({current_positions}/{max_positions})")
    else:
        print(f"当前持仓：{current_positions}/{max_positions}")
        
        for stock in HK_STOCKS:
            symbol = stock['symbol']
            if symbol in position_symbols:
                continue
            
            if symbol not in quote_dict:
                continue
            
            q = quote_dict[symbol]
            price = float(q.last_done)
            change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
            
            strategy = stock['strategy']
            cfg = STRATEGIES[strategy]
            
            # 检查买入信号
            should_buy = False
            
            if strategy == "momentum" and change >= cfg['threshold']:
                should_buy = True
                print(f"\n{symbol} {stock['name']} 动量 +{change*100:.2f}% - 买入信号")
            
            elif strategy == "breakout" and change >= cfg['threshold']:
                should_buy = True
                print(f"\n{symbol} {stock['name']} 突破 +{change*100:.2f}% - 买入信号")
            
            elif strategy == "mean_reversion" and change <= cfg['threshold']:
                should_buy = True
                print(f"\n{symbol} {stock['name']} 超跌 {change*100:.2f}% - 买入信号")
            
            if should_buy:
                # 计算买入数量
                buy_value = cash * cfg['position_size']
                qty = int(buy_value / price)
                qty = (qty // stock['board_lot']) * stock['board_lot']
                
                if qty >= stock['board_lot']:
                    result = submit_order(symbol, "Buy", price * 1.005, qty, strategy)
                    if result["success"]:
                        print(f"   ✅ 买入 {qty}股，订单 ID: {result['order_id']}")
                        trades_executed += 1
    
    print()
    print("=" * 80)
    print(f"✅ 本次执行 {trades_executed} 笔交易")
    print("=" * 80)
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()

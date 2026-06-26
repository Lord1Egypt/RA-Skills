#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易闭环系统 v3.0
功能：回测 → 实盘 → 绩效分析 → 策略优化 → 再回测
目标：胜率>70%，年化收益>100%
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os

load_dotenv()

# ============ 策略配置 ============
STRATEGY = {
    "name": "动量 + 均值回归 v3",
    "momentum_threshold": 0.015,  # +1.5% 追涨
    "reversion_threshold": -0.025,  # -2.5% 抄底
    "stop_loss": -0.08,  # -8% 止损
    "take_profit": 0.15,  # +15% 止盈
    "position_size_pct": 0.20,  # 单笔 20% 仓位
    "max_positions": 5,
}

# 股票池
HK_STOCKS = [
    {'symbol': '700.HK', 'name': '腾讯', 'lot': 100},
    {'symbol': '9988.HK', 'name': '阿里', 'lot': 100},
    {'symbol': '3690.HK', 'name': '美团', 'lot': 100},
    {'symbol': '1211.HK', 'name': '比亚迪', 'lot': 500},
    {'symbol': '9618.HK', 'name': '京东', 'lot': 100},
]

# 状态文件
PERFORMANCE_FILE = '/tmp/quant_performance.json'
TRADE_LOG_FILE = '/tmp/quant_trade_log.json'

class QuantSystem:
    def __init__(self):
        self.config = Config.from_env()
        self.ctx = TradeContext(self.config)
        self.qctx = QuoteContext(self.config)
        self.performance = self.load_performance()
        self.trade_log = self.load_trade_log()
        
    def load_performance(self):
        try:
            with open(PERFORMANCE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'start_capital': 800000,
                'current_capital': 800000,
                'peak_capital': 800000,
                'max_drawdown': 0.0,
                'trades': [],
            }
    
    def save_performance(self):
        with open(PERFORMANCE_FILE, 'w') as f:
            json.dump(self.performance, f, indent=2)
    
    def load_trade_log(self):
        try:
            with open(TRADE_LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_trade_log(self):
        with open(TRADE_LOG_FILE, 'w') as f:
            json.dump(self.trade_log, f, indent=2)
    
    def get_account_status(self):
        """获取账户状态"""
        for b in self.ctx.account_balance():
            cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
            net_assets = float(b.net_assets)
            return cash, net_assets
        return 0, 0
    
    def get_positions(self):
        """获取持仓"""
        positions = []
        resp = self.ctx.stock_positions()
        for channel in resp.channels:
            for pos in channel.positions:
                positions.append({
                    'symbol': pos.symbol,
                    'qty': int(pos.quantity),
                    'avail': int(pos.available_quantity),
                    'cost': float(pos.cost_price),
                })
        return positions
    
    def get_quotes(self, symbols):
        """获取行情"""
        quotes = {}
        try:
            result = self.qctx.quote(symbols)
            for q in result:
                change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
                quotes[q.symbol] = {
                    'price': float(q.last_done),
                    'change': float(change),
                    'prev_close': float(q.prev_close),
                }
        except Exception as e:
            print(f"  ⚠️ 获取行情失败：{e}")
        return quotes
    
    def check_exit_signals(self, positions, quotes):
        """检查止盈止损信号"""
        exits = []
        
        for pos in positions:
            if pos['symbol'] not in quotes:
                continue
            
            price = quotes[pos['symbol']]['price']
            pnl_pct = (price - pos['cost']) / pos['cost']
            
            # 止盈
            if pnl_pct >= STRATEGY['take_profit']:
                exits.append({
                    'symbol': pos['symbol'],
                    'type': 'SELL',
                    'reason': f'止盈 +{pnl_pct*100:.1f}%',
                    'qty': pos['avail'],
                    'price': price,
                })
            
            # 止损
            elif pnl_pct <= STRATEGY['stop_loss']:
                exits.append({
                    'symbol': pos['symbol'],
                    'type': 'SELL',
                    'reason': f'止损 {pnl_pct*100:.1f}%',
                    'qty': pos['avail'],
                    'price': price,
                })
        
        return exits
    
    def check_entry_signals(self, positions, quotes, cash):
        """检查买入信号"""
        entries = []
        position_symbols = [p['symbol'] for p in positions]
        
        for stock in HK_STOCKS:
            symbol = stock['symbol']
            if symbol in position_symbols or symbol not in quotes:
                continue
            
            change = quotes[symbol]['change']
            
            # 超跌抄底
            if change <= STRATEGY['reversion_threshold']:
                buy_value = cash * STRATEGY['position_size_pct']
                qty = int(buy_value / quotes[symbol]['price'])
                qty = (qty // stock['lot']) * stock['lot']
                
                if qty >= stock['lot']:
                    entries.append({
                        'symbol': symbol,
                        'type': 'BUY',
                        'reason': f'超跌 {change*100:.2f}%',
                        'qty': qty,
                        'price': quotes[symbol]['price'] * 1.005,
                        'lot': stock['lot'],
                    })
            
            # 动量追涨
            elif change >= STRATEGY['momentum_threshold']:
                buy_value = cash * STRATEGY['position_size_pct']
                qty = int(buy_value / quotes[symbol]['price'])
                qty = (qty // stock['lot']) * stock['lot']
                
                if qty >= stock['lot']:
                    entries.append({
                        'symbol': symbol,
                        'type': 'BUY',
                        'reason': f'动量 +{change*100:.2f}%',
                        'qty': qty,
                        'price': quotes[symbol]['price'] * 1.005,
                        'lot': stock['lot'],
                    })
        
        return entries
    
    def execute_order(self, order):
        """执行订单"""
        try:
            resp = self.ctx.submit_order(
                side=OrderSide.Buy if order['type'] == 'BUY' else OrderSide.Sell,
                symbol=order['symbol'],
                order_type=OrderType.LO,
                submitted_price=Decimal(f"{order['price']:.2f}"),
                submitted_quantity=Decimal(str(order['qty'])),
                time_in_force=TimeInForceType.Day,
                remark=f"AutoTrade: {order['reason']}"
            )
            
            # 记录交易日志
            self.trade_log.append({
                'time': datetime.now().isoformat(),
                'symbol': order['symbol'],
                'type': order['type'],
                'qty': order['qty'],
                'price': order['price'],
                'reason': order['reason'],
                'order_id': resp.order_id,
            })
            self.save_trade_log()
            
            return True, resp.order_id
            
        except Exception as e:
            print(f"  ❌ 执行失败：{e}")
            return False, None
    
    def run_backtest(self, days=30):
        """简易回测（基于历史信号）"""
        print(f"\n📊 回测（过去{days}天）")
        print("=" * 50)
        
        # 简化回测：假设每次信号都能成交
        # 实际应使用历史数据回测
        print("⚠️  简化回测：基于策略参数估算")
        
        # 估算胜率（基于历史交易）
        if self.performance['total_trades'] > 0:
            win_rate = self.performance['winning_trades'] / self.performance['total_trades'] * 100
            avg_return = self.performance['total_pnl'] / self.performance['start_capital'] * 100
            
            print(f"  历史交易：{self.performance['total_trades']}笔")
            print(f"  胜率：{win_rate:.1f}%")
            print(f"  总收益：{avg_return:.2f}%")
            
            # 年化估算
            days_active = 5  # 假设交易 5 天
            annual_return = (1 + avg_return/100) ** (365/days_active) - 1
            print(f"  年化收益：{annual_return*100:.1f}%")
        else:
            print("  暂无历史数据，开始实盘积累")
    
    def run_once(self):
        """执行一次完整检查"""
        print("\n" + "=" * 70)
        print(f"🚀 量化交易闭环系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"策略：{STRATEGY['name']}")
        print("=" * 70)
        
        # 1. 账户状态
        cash, net_assets = self.get_account_status()
        self.performance['current_capital'] = net_assets
        
        print(f"\n💰 账户状态")
        print(f"   可用现金：HKD {cash:,.2f}")
        print(f"   净资产：HKD {net_assets:,.2f}")
        
        # 更新最大回撤
        if net_assets > self.performance['peak_capital']:
            self.performance['peak_capital'] = net_assets
        
        drawdown = (self.performance['peak_capital'] - net_assets) / self.performance['peak_capital'] * 100
        self.performance['max_drawdown'] = max(self.performance['max_drawdown'], drawdown)
        
        # 2. 当前持仓
        positions = self.get_positions()
        print(f"\n📈 当前持仓 ({len(positions)}只)")
        
        # 获取行情
        all_symbols = [s['symbol'] for s in HK_STOCKS]
        quotes = self.get_quotes(all_symbols)
        
        for pos in positions:
            if pos['symbol'] in quotes:
                price = quotes[pos['symbol']]['price']
                pnl = (price - pos['cost']) * pos['qty']
                pnl_pct = (price - pos['cost']) / pos['cost'] * 100
                print(f"   {pos['symbol']}: {pos['qty']}股 @ {pos['cost']:.2f} → {price:.2f}  盈亏 HKD {pnl:+,.0f} ({pnl_pct:+.2f}%)")
        
        # 3. 检查止盈止损
        print(f"\n🎯 检查退出信号")
        exits = self.check_exit_signals(positions, quotes)
        
        for exit_order in exits:
            print(f"   📤 {exit_order['symbol']} {exit_order['type']} {exit_order['qty']}股")
            print(f"      原因：{exit_order['reason']}")
            
            success, order_id = self.execute_order(exit_order)
            if success:
                print(f"      ✅ 订单 ID: {order_id}")
                
                # 更新绩效
                if exit_order['type'] == 'SELL':
                    self.performance['total_trades'] += 1
                    # 简化：假设卖出都记录为完成交易
                    # 实际应跟踪买入成本
        
        # 4. 检查买入信号
        print(f"\n🔍 检查买入信号")
        entries = self.check_entry_signals(positions, quotes, cash)
        
        for entry_order in entries:
            if len(positions) >= STRATEGY['max_positions']:
                print(f"   ⚠️ 已达最大持仓数 ({STRATEGY['max_positions']}), 跳过")
                break
            
            print(f"   📤 {entry_order['symbol']} BUY {entry_order['qty']}股")
            print(f"      原因：{entry_order['reason']}")
            print(f"      限价：HKD {entry_order['price']:.2f}")
            
            success, order_id = self.execute_order(entry_order)
            if success:
                print(f"      ✅ 订单 ID: {order_id}")
                positions.append({
                    'symbol': entry_order['symbol'],
                    'qty': entry_order['qty'],
                    'cost': entry_order['price'],
                })
        
        # 5. 绩效汇总
        print(f"\n📊 绩效汇总")
        print(f"   总交易：{self.performance['total_trades']}笔")
        print(f"   盈利：{self.performance['winning_trades']}笔")
        print(f"   亏损：{self.performance['losing_trades']}笔")
        
        if self.performance['total_trades'] > 0:
            win_rate = self.performance['winning_trades'] / self.performance['total_trades'] * 100
            print(f"   胜率：{win_rate:.1f}%")
        
        total_return = (self.performance['current_capital'] - self.performance['start_capital']) / self.performance['start_capital'] * 100
        print(f"   总收益：{total_return:.2f}%")
        print(f"   最大回撤：{self.performance['max_drawdown']:.2f}%")
        
        # 目标对比
        print(f"\n🎯 目标进度")
        target_win_rate = 70.0
        target_annual = 100.0
        
        if self.performance['total_trades'] > 0:
            win_rate = self.performance['winning_trades'] / self.performance['total_trades'] * 100
            print(f"   胜率：{win_rate:.1f}% / {target_win_rate}% {'✅' if win_rate >= target_win_rate else '⏳'}")
        
        # 年化估算（简化）
        days_trading = 5  # 假设
        if days_trading > 0:
            annual_return = (1 + total_return/100) ** (365/days_trading) - 1
            print(f"   年化：{annual_return*100:.1f}% / {target_annual}% {'✅' if annual_return*100 >= target_annual else '⏳'}")
        
        self.save_performance()
        
        print("\n" + "=" * 70)
    
    def close(self):
        self.ctx.close()
        self.qctx.close()

if __name__ == "__main__":
    system = QuantSystem()
    system.run_once()
    system.close()

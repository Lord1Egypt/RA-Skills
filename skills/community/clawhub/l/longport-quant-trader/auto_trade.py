#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动量化交易系统 - 长桥模拟账户 LBPT10034472
策略：动量 + 均值回归混合策略 (v2 最优版)
支持：港股 + 美股
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os
import time

load_dotenv()

# 配置
CONFIG = {
    "account": "LBPT10034472",
    "strategy_name": "动量 + 均值回归 v2",
    "momentum_threshold": 0.013,  # 涨幅>1.3% 追涨
    "reversion_threshold": -0.023,  # 跌幅>2.3% 抄底
    "position_size_pct": 0.15,  # 单笔 15% 仓位
    "stop_loss": -0.10,  # 止损 -10%
    "take_profit": 0.20,  # 止盈 +20%
    "max_positions": 5,  # 最多持有 5 只股票
}

# 股票池
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯控股", "board_lot": 100},
    {"symbol": "9988.HK", "name": "阿里巴巴", "board_lot": 100},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100},
]

US_STOCKS = [
    {"symbol": "QQQ.US", "name": "纳指 100 ETF", "board_lot": 1},
    {"symbol": "NVDA.US", "name": "英伟达", "board_lot": 1},
    {"symbol": "AAPL.US", "name": "苹果", "board_lot": 1},
    {"symbol": "TSLA.US", "name": "特斯拉", "board_lot": 1},
    {"symbol": "MSFT.US", "name": "微软", "board_lot": 1},
]

# 状态文件
STATE_FILE = '/tmp/auto_trade_state.json'
PERFORMANCE_FILE = '/tmp/auto_trade_performance.json'

class AutoTrader:
    def __init__(self):
        self.config = Config.from_env()
        self.ctx = TradeContext(self.config)
        self.qctx = QuoteContext(self.config)
        self.state = self.load_state()
        self.performance = self.load_performance()
        
    def load_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {
                'positions': {},  # {symbol: {cost, quantity, entry_time}}
                'last_trade': None,
                'trade_count': 0,
            }
    
    def save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def load_performance(self):
        try:
            with open(PERFORMANCE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {
                'trades': [],
                'total_profit': 0,
                'win_count': 0,
                'loss_count': 0,
            }
    
    def save_performance(self):
        with open(PERFORMANCE_FILE, 'w') as f:
            json.dump(self.performance, f, indent=2)
    
    def get_account_status(self):
        """获取账户状态"""
        balances = self.ctx.account_balance()
        for b in balances:
            if b.currency == "HKD":
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
                    'quantity': int(pos.quantity),
                    'available': int(pos.available_quantity),
                    'cost': float(pos.cost_price),
                })
        return positions
    
    def get_quotes(self, symbols):
        """获取行情"""
        quotes = {}
        try:
            # 批量获取行情
            result = self.qctx.quote(symbols)
            for q in result:
                symbol = q.symbol
                change_pct = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
                quotes[symbol] = {
                    'price': float(q.last_done),
                    'prev_close': float(q.prev_close),
                    'change_pct': float(change_pct),
                    'high': float(q.high),
                    'low': float(q.low),
                }
        except Exception as e:
            print(f"  ⚠️ 批量获取行情失败：{e}")
            # 尝试逐个获取
            for symbol in symbols:
                try:
                    result = self.qctx.quote([symbol])
                    if result:
                        q = result[0]
                        change_pct = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
                        quotes[symbol] = {
                            'price': float(q.last_done),
                            'prev_close': float(q.prev_close),
                            'change_pct': float(change_pct),
                            'high': float(q.high),
                            'low': float(q.low),
                        }
                except Exception as e2:
                    print(f"  ⚠️ {symbol} 获取失败：{e2}")
        return quotes
    
    def analyze_signals(self, quotes, positions):
        """分析交易信号"""
        signals = []
        position_symbols = {p['symbol']: p for p in positions}
        
        # 检查持仓止盈止损
        for pos in positions:
            symbol = pos['symbol']
            if symbol not in quotes:
                continue
            
            current_price = quotes[symbol]['price']
            cost = pos['cost']
            pnl_pct = (current_price - cost) / cost
            
            # 止盈
            if pnl_pct >= CONFIG['take_profit']:
                signals.append({
                    'symbol': symbol,
                    'type': 'SELL',
                    'reason': f'止盈 +{pnl_pct*100:.1f}% (目标 +{CONFIG["take_profit"]*100}%)',
                    'price': current_price,
                    'quantity': pos['available'],
                    'strength': 10,
                })
            
            # 止损
            elif pnl_pct <= CONFIG['stop_loss']:
                signals.append({
                    'symbol': symbol,
                    'type': 'SELL',
                    'reason': f'止损 {pnl_pct*100:.1f}% (阈值 {CONFIG["stop_loss"]*100}%)',
                    'price': current_price,
                    'quantity': pos['available'],
                    'strength': 10,
                })
        
        # 检查买入信号
        all_stocks = HK_STOCKS + US_STOCKS
        for stock in all_stocks:
            symbol = stock['symbol']
            if symbol not in quotes:
                continue
            
            # 已持仓则跳过
            if symbol in position_symbols:
                continue
            
            change = quotes[symbol]['change_pct']
            
            # 动量信号
            if change >= CONFIG['momentum_threshold']:
                signals.append({
                    'symbol': symbol,
                    'type': 'BUY',
                    'reason': f'动量 +{change*100:.2f}%',
                    'price': quotes[symbol]['price'],
                    'board_lot': stock['board_lot'],
                    'strength': min(10, int(change * 200)),
                })
            
            # 均值回归信号
            elif change <= CONFIG['reversion_threshold']:
                signals.append({
                    'symbol': symbol,
                    'type': 'BUY',
                    'reason': f'超跌 {change*100:.2f}%',
                    'price': quotes[symbol]['price'],
                    'board_lot': stock['board_lot'],
                    'strength': min(10, int(abs(change) * 150)),
                })
        
        # 按强度排序
        signals.sort(key=lambda x: x['strength'], reverse=True)
        return signals
    
    def execute_buy(self, signal, cash_available):
        """执行买入"""
        # 计算仓位
        position_value = cash_available * CONFIG['position_size_pct']
        quantity = int(position_value / signal['price'])
        
        # 调整为整手
        board_lot = signal.get('board_lot', 1)
        quantity = (quantity // board_lot) * board_lot
        
        if quantity < board_lot:
            print(f"  ⚠️ 数量不足 1 手，跳过")
            return None
        
        total_cost = quantity * signal['price']
        if total_cost > cash_available:
            print(f"  ⚠️ 资金不足，跳过")
            return None
        
        print(f"  📤 提交买入订单:")
        print(f"     标的：{signal['symbol']}")
        print(f"     数量：{quantity}股")
        print(f"     价格：${signal['price']:.2f}")
        print(f"     总额：${total_cost:.2f}")
        
        # 实际下单
        try:
            resp = self.ctx.submit_order(
                side=OrderSide.Buy,
                symbol=signal['symbol'],
                order_type=OrderType.LO,
                submitted_price=Decimal(str(signal['price'])),
                submitted_quantity=Decimal(str(quantity)),
                time_in_force=TimeInForceType.Day,
                remark=f"AutoTrade: {CONFIG['strategy_name']}"
            )
            print(f"  ✅ 订单提交成功！ID: {resp.order_id}")
            
            # 记录状态
            self.state['positions'][signal['symbol']] = {
                'cost': signal['price'],
                'quantity': quantity,
                'entry_time': datetime.now().isoformat(),
                'order_id': resp.order_id,
            }
            self.state['trade_count'] += 1
            self.state['last_trade'] = datetime.now().isoformat()
            self.save_state()
            
            return {'order_id': resp.order_id, 'quantity': quantity}
            
        except Exception as e:
            print(f"  ❌ 下单失败：{e}")
            return None
    
    def execute_sell(self, signal, position):
        """执行卖出"""
        print(f"  📤 提交卖出订单:")
        print(f"     标的：{signal['symbol']}")
        print(f"     数量：{signal['quantity']}股")
        print(f"     价格：${signal['price']:.2f}")
        
        try:
            resp = self.ctx.submit_order(
                side=OrderSide.Sell,
                symbol=signal['symbol'],
                order_type=OrderType.LO,
                submitted_price=Decimal(str(signal['price'])),
                submitted_quantity=Decimal(str(signal['quantity'])),
                time_in_force=TimeInForceType.Day,
                remark=f"AutoTrade: {signal['reason']}"
            )
            print(f"  ✅ 订单提交成功！ID: {resp.order_id}")
            
            # 记录绩效
            pos_info = self.state['positions'].get(signal['symbol'], {})
            if pos_info:
                cost = pos_info.get('cost', 0)
                quantity = pos_info.get('quantity', 0)
                pnl = (signal['price'] - cost) * quantity
                pnl_pct = (signal['price'] - cost) / cost * 100
                
                self.performance['trades'].append({
                    'symbol': signal['symbol'],
                    'entry_time': pos_info.get('entry_time'),
                    'exit_time': datetime.now().isoformat(),
                    'entry_price': cost,
                    'exit_price': signal['price'],
                    'quantity': quantity,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'reason': signal['reason'],
                })
                
                if pnl > 0:
                    self.performance['win_count'] += 1
                else:
                    self.performance['loss_count'] += 1
                
                self.performance['total_profit'] += pnl
            
            # 删除持仓记录
            if signal['symbol'] in self.state['positions']:
                del self.state['positions'][signal['symbol']]
            
            self.state['trade_count'] += 1
            self.state['last_trade'] = datetime.now().isoformat()
            self.save_state()
            self.save_performance()
            
            return {'order_id': resp.order_id}
            
        except Exception as e:
            print(f"  ❌ 下单失败：{e}")
            return None
    
    def run_once(self):
        """执行一次交易检查"""
        print("\n" + "=" * 80)
        print(f"🚀 自动量化交易 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 1. 账户状态
        cash, net_assets = self.get_account_status()
        print(f"\n💰 账户状态")
        print(f"   可用现金：HKD {cash:,.2f}")
        print(f"   净资产：HKD {net_assets:,.2f}")
        
        # 2. 当前持仓
        positions = self.get_positions()
        print(f"\n📈 当前持仓 ({len(positions)}只)")
        for pos in positions:
            print(f"   {pos['symbol']}: {pos['quantity']}股 @ ${pos['cost']:.2f}")
        
        # 3. 获取行情
        all_symbols = [s['symbol'] for s in HK_STOCKS + US_STOCKS]
        quotes = self.get_quotes(all_symbols)
        
        print(f"\n📊 实时行情")
        for symbol, q in quotes.items():
            print(f"   {symbol}: ${q['price']:.2f} ({q['change_pct']*100:+.2f}%)")
        
        # 4. 分析信号
        signals = self.analyze_signals(quotes, positions)
        
        print(f"\n🎯 交易信号 ({len(signals)}个)")
        if not signals:
            print("   暂无交易信号，保持观望")
        else:
            for sig in signals[:5]:
                print(f"   {sig['type']} {sig['symbol']}: {sig['reason']} (强度⭐{sig['strength']})")
        
        # 5. 执行交易
        if signals:
            print(f"\n📤 执行交易")
            for signal in signals:
                if signal['type'] == 'BUY' and len(positions) >= CONFIG['max_positions']:
                    print(f"  ⚠️ 已达最大持仓数 ({CONFIG['max_positions']}), 跳过买入")
                    continue
                
                if signal['type'] == 'BUY':
                    pos_info = next((p for p in positions if p['symbol'] == signal['symbol']), None)
                    if pos_info:
                        print(f"  ⚠️ 已持仓 {signal['symbol']}, 跳过")
                        continue
                    
                    result = self.execute_buy(signal, cash)
                    if result:
                        positions.append({
                            'symbol': signal['symbol'],
                            'quantity': result['quantity'],
                            'cost': signal['price'],
                        })
                        cash -= signal['price'] * result['quantity']
                
                elif signal['type'] == 'SELL':
                    pos_info = next((p for p in positions if p['symbol'] == signal['symbol']), None)
                    if pos_info:
                        self.execute_sell(signal, pos_info)
                        positions = [p for p in positions if p['symbol'] != signal['symbol']]
        
        # 6. 绩效汇总
        print(f"\n📊 绩效汇总")
        print(f"   总交易次数：{self.state['trade_count']}")
        print(f"   盈利次数：{self.performance['win_count']}")
        print(f"   亏损次数：{self.performance['loss_count']}")
        print(f"   总盈亏：HKD {self.performance['total_profit']:,.2f}")
        
        if self.performance['win_count'] + self.performance['loss_count'] > 0:
            win_rate = self.performance['win_count'] / (self.performance['win_count'] + self.performance['loss_count']) * 100
            print(f"   胜率：{win_rate:.1f}%")
        
        print("\n" + "=" * 80)
    
    def run_continuous(self, interval_minutes=5):
        """持续运行"""
        print(f"\n🔄 启动持续监控 (每{interval_minutes}分钟执行一次)")
        print(f"   按 Ctrl+C 停止")
        
        try:
            while True:
                self.run_once()
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print(f"\n👋 停止监控")

def main():
    import sys
    
    trader = AutoTrader()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        trader.run_continuous(interval)
    else:
        trader.run_once()

if __name__ == "__main__":
    main()

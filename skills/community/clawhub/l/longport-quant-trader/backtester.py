#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化策略回测系统
功能：历史数据回测、策略评估、参数优化
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# ============ 技术指标 ============

def calculate_macd(df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
    """MACD 指标"""
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    return df

def calculate_rsi(df: pd.DataFrame, period=14) -> pd.DataFrame:
    """RSI 指标"""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_bollinger(df: pd.DataFrame, period=20, std_dev=2) -> pd.DataFrame:
    """布林带"""
    df['BB_Middle'] = df['Close'].rolling(window=period).mean()
    df['BB_Std'] = df['Close'].rolling(window=period).std()
    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * std_dev)
    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * std_dev)
    return df

def calculate_ma(df: pd.DataFrame, periods=[5, 10, 20, 60]) -> pd.DataFrame:
    """移动平均线"""
    for period in periods:
        df[f'MA{period}'] = df['Close'].rolling(window=period).mean()
    return df

# ============ 策略定义 ============

class BacktestStrategy:
    """回测策略基类"""
    
    def __init__(self, name: str, initial_cash: float = 1000000):
        self.name = name
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        """生成交易信号（子类实现）"""
        raise NotImplementedError
    
    def execute_backtest(self, df: pd.DataFrame) -> Dict:
        """执行回测"""
        signals = self.generate_signals(df)
        
        for signal in signals:
            date = signal['date']
            price = signal['price']
            symbol = signal['symbol']
            action = signal['action']
            
            if action == 'Buy' and self.cash > price * 100:
                # 买入 100 股
                quantity = 100
                cost = price * quantity
                if cost <= self.cash:
                    self.cash -= cost
                    self.positions[symbol] = {
                        'quantity': quantity,
                        'cost_price': price,
                        'buy_date': date
                    }
                    self.trades.append({
                        'date': date,
                        'symbol': symbol,
                        'action': 'Buy',
                        'price': price,
                        'quantity': quantity,
                        'cost': cost
                    })
            
            elif action == 'Sell' and symbol in self.positions:
                # 卖出
                pos = self.positions[symbol]
                revenue = price * pos['quantity']
                pnl = revenue - (pos['cost_price'] * pos['quantity'])
                self.cash += revenue
                self.trades.append({
                    'date': date,
                    'symbol': symbol,
                    'action': 'Sell',
                    'price': price,
                    'quantity': pos['quantity'],
                    'pnl': pnl,
                    'buy_date': pos['buy_date']
                })
                del self.positions[symbol]
        
        return self.calculate_performance(df)
    
    def calculate_performance(self, df: pd.DataFrame) -> Dict:
        """计算绩效"""
        # 计算总资产
        total_value = self.cash
        for symbol, pos in self.positions.items():
            # 使用最新收盘价
            current_price = df[df['Date'] == df['Date'].max()]['Close'].values[0]
            total_value += current_price * pos['quantity']
        
        # 收益率
        total_return = (total_value - self.initial_cash) / self.initial_cash
        
        # 交易统计
        buy_trades = [t for t in self.trades if t['action'] == 'Buy']
        sell_trades = [t for t in self.trades if t['action'] == 'Sell']
        
        wins = [t for t in sell_trades if t.get('pnl', 0) > 0]
        losses = [t for t in sell_trades if t.get('pnl', 0) <= 0]
        
        win_rate = len(wins) / len(sell_trades) if sell_trades else 0
        total_pnl = sum(t.get('pnl', 0) for t in sell_trades)
        
        return {
            'strategy': self.name,
            'initial_cash': self.initial_cash,
            'final_value': total_value,
            'total_return': total_return,
            'total_return_pct': f"{total_return:.2%}",
            'total_trades': len(buy_trades),
            'closed_trades': len(sell_trades),
            'wins': len(wins),
            'losses': len(losses),
            'win_rate': f"{win_rate:.2%}",
            'total_pnl': total_pnl,
            'current_positions': len(self.positions)
        }

# ============ 具体策略 ============

class MACDStrategy(BacktestStrategy):
    """MACD 策略"""
    
    def __init__(self, initial_cash: float = 1000000):
        super().__init__("MACD", initial_cash)
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        df = calculate_macd(df.copy())
        signals = []
        
        for i in range(1, len(df)):
            prev_hist = float(df.iloc[i-1]['Histogram'])
            curr_hist = float(df.iloc[i]['Histogram'])
            
            # 金叉买入
            if prev_hist < 0 and curr_hist > 0:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Buy',
                    'price': float(df.iloc[i]['Close'])
                })
            
            # 死叉卖出
            elif prev_hist > 0 and curr_hist < 0:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Sell',
                    'price': float(df.iloc[i]['Close'])
                })
        
        return signals

class RSIStrategy(BacktestStrategy):
    """RSI 策略"""
    
    def __init__(self, initial_cash: float = 1000000, oversold=30, overbought=70):
        super().__init__("RSI", initial_cash)
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        df = calculate_rsi(df.copy())
        signals = []
        in_position = False
        
        for i in range(1, len(df)):
            rsi = float(df.iloc[i]['RSI'])
            
            # 超卖买入
            if rsi < self.oversold and not in_position:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Buy',
                    'price': float(df.iloc[i]['Close'])
                })
                in_position = True
            
            # 超买卖出
            elif rsi > self.overbought and in_position:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Sell',
                    'price': float(df.iloc[i]['Close'])
                })
                in_position = False
        
        return signals

class BollingerStrategy(BacktestStrategy):
    """布林带策略"""
    
    def __init__(self, initial_cash: float = 1000000):
        super().__init__("Bollinger", initial_cash)
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        df = calculate_bollinger(df.copy())
        signals = []
        in_position = False
        
        for i in range(1, len(df)):
            row = df.iloc[i]
            
            # 触及下轨买入
            if float(row['Close']) < float(row['BB_Lower']) and not in_position:
                signals.append({
                    'date': row['Date'],
                    'symbol': 'TEST',
                    'action': 'Buy',
                    'price': float(row['Close'])
                })
                in_position = True
            
            # 触及上轨卖出
            elif float(row['Close']) > float(row['BB_Upper']) and in_position:
                signals.append({
                    'date': row['Date'],
                    'symbol': 'TEST',
                    'action': 'Sell',
                    'price': float(row['Close'])
                })
                in_position = False
        
        return signals

class DualMAStrategy(BacktestStrategy):
    """双均线策略"""
    
    def __init__(self, initial_cash: float = 1000000, fast=10, slow=30):
        super().__init__(f"DualMA({fast}/{slow})", initial_cash)
        self.fast = fast
        self.slow = slow
    
    def generate_signals(self, df: pd.DataFrame) -> List[Dict]:
        df = calculate_ma(df.copy(), [self.fast, self.slow])
        signals = []
        in_position = False
        
        for i in range(1, len(df)):
            fast_ma = float(df.iloc[i][f'MA{self.fast}'])
            slow_ma = float(df.iloc[i][f'MA{self.slow}'])
            prev_fast = float(df.iloc[i-1][f'MA{self.fast}'])
            prev_slow = float(df.iloc[i-1][f'MA{self.slow}'])
            
            # 金叉买入
            if prev_fast <= prev_slow and fast_ma > slow_ma and not in_position:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Buy',
                    'price': float(df.iloc[i]['Close'])
                })
                in_position = True
            
            # 死叉卖出
            elif prev_fast >= prev_slow and fast_ma < slow_ma and in_position:
                signals.append({
                    'date': df.iloc[i]['Date'],
                    'symbol': 'TEST',
                    'action': 'Sell',
                    'price': float(df.iloc[i]['Close'])
                })
                in_position = False
        
        return signals

# ============ 回测引擎 ============

def run_backtest(symbol: str, start_date: str, end_date: str, strategies: List[BacktestStrategy]) -> Dict:
    """运行回测"""
    print(f"📊 回测 {symbol} ({start_date} ~ {end_date})")
    print("=" * 60)
    
    # 下载数据
    print("📥 下载历史数据...")
    df = yf.download(symbol, start=start_date, end=end_date)
    
    if df.empty:
        return {"error": "No data"}
    
    df = df.reset_index()
    if 'Date' not in df.columns and 'date' in df.columns:
        df['Date'] = df['date']
    
    print(f"✅ 数据量：{len(df)} 天")
    print(f"   开始：{df['Date'].min()}")
    print(f"   结束：{df['Date'].max()}")
    print()
    
    # 运行各策略
    results = []
    for strategy in strategies:
        print(f"🔍 回测策略：{strategy.name}")
        result = strategy.execute_backtest(df.copy())
        results.append(result)
        print(f"   收益率：{result['total_return_pct']}")
        print(f"   交易次数：{result['total_trades']}")
        print(f"   胜率：{result['win_rate']}")
        print()
    
    # 对比结果
    print("=" * 60)
    print("📈 策略对比:")
    print("-" * 60)
    print(f"{'策略':<20} {'收益率':>12} {'交易次数':>10} {'胜率':>10}")
    print("-" * 60)
    for r in sorted(results, key=lambda x: x['total_return'], reverse=True):
        print(f"{r['strategy']:<20} {r['total_return_pct']:>12} {r['total_trades']:>10} {r['win_rate']:>10}")
    
    return {
        'symbol': symbol,
        'period': f"{start_date} ~ {end_date}",
        'data_points': len(df),
        'results': results
    }

# ============ 参数优化 ============

def optimize_strategy(strategy_class, symbol: str, start_date: str, end_date: str, param_grid: Dict) -> Dict:
    """参数优化"""
    print(f"🔧 参数优化：{strategy_class.__name__}")
    print("=" * 60)
    
    best_result = None
    best_params = None
    best_return = -999
    
    # 网格搜索
    import itertools
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    
    for values in itertools.product(*param_values):
        params = dict(zip(param_names, values))
        
        # 创建策略
        strategy = strategy_class(**params)
        
        # 运行回测
        df = yf.download(symbol, start=start_date, end=end_date)
        if df.empty:
            continue
        df = df.reset_index()
        if 'Date' not in df.columns and 'date' in df.columns:
            df['Date'] = df['date']
        
        result = strategy.execute_backtest(df.copy())
        
        if result['total_return'] > best_return:
            best_return = result['total_return']
            best_params = params
            best_result = result
    
    print(f"✅ 最优参数：{best_params}")
    print(f"   收益率：{best_result['total_return_pct']}")
    print(f"   交易次数：{best_result['total_trades']}")
    print(f"   胜率：{best_result['win_rate']}")
    
    return {
        'best_params': best_params,
        'best_result': best_result
    }

# ============ 主函数 ============

if __name__ == "__main__":
    # 示例：回测 AAPL
    strategies = [
        MACDStrategy(),
        RSIStrategy(oversold=30, overbought=70),
        BollingerStrategy(),
        DualMAStrategy(fast=10, slow=30)
    ]
    
    results = run_backtest(
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2024-12-31",
        strategies=strategies
    )
    
    # 参数优化示例
    # optimize_strategy(
    #     RSIStrategy,
    #     symbol="AAPL",
    #     start_date="2023-01-01",
    #     end_date="2024-12-31",
    #     param_grid={
    #         'oversold': [20, 30, 40],
    #         'overbought': [60, 70, 80]
    #     }
    # )

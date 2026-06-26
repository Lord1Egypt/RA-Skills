#!/usr/bin/env python3
"""
终极优化策略 - 缠论+MACD+RSI+ 追踪止损
基于所有回测结果优化参数
目标：高胜率 + 高收益 + 低回撤
"""

import sqlite3
import pandas as pd
import backtrader as bt
from datetime import datetime
import json
import os
import numpy as np

INDICATORS_DB = "/root/data/astock_indicators.db"
HISTORY_DB = "/root/data/astock_history.db"

# 20 支行业偏好股票
INDUSTRY_STOCKS_20 = [
    {'code': '000559', 'name': '万向钱潮', 'sector': '汽配'},
    {'code': '301308', 'name': '江波龙', 'sector': '存储芯片'},
    {'code': '600096', 'name': '云天化', 'sector': '化工'},
    {'code': '300468', 'name': '四方精创', 'sector': '软件'},
    {'code': '600989', 'name': '宝丰能源', 'sector': '化工'},
    {'code': '600256', 'name': '广汇能源', 'sector': '能源'},
    {'code': '601600', 'name': '中国铝业', 'sector': '有色'},
    {'code': '002384', 'name': '东山精密', 'sector': '消费电子'},
    {'code': '002241', 'name': '歌尔股份', 'sector': '消费电子'},
    {'code': '000725', 'name': '京东方 A', 'sector': '消费电子'},
    {'code': '002036', 'name': '联创电子', 'sector': '消费电子'},
    {'code': '603986', 'name': '兆易创新', 'sector': '存储芯片'},
    {'code': '002371', 'name': '北方华创', 'sector': '半导体'},
    {'code': '603501', 'name': '韦尔股份', 'sector': '半导体'},
    {'code': '002202', 'name': '金风科技', 'sector': '风电'},
    {'code': '601615', 'name': '明阳智能', 'sector': '风电'},
    {'code': '000788', 'name': '北大医药', 'sector': '创新医疗'},
    {'code': '002007', 'name': '华兰生物', 'sector': '创新医疗'},
    {'code': '002031', 'name': '巨轮智能', 'sector': '机器人'},
    {'code': '002415', 'name': '海康威视', 'sector': 'AI'},
]

# 优化后的策略参数 (基于回测结果)
OPTIMIZED_PARAMS = [
    # 基准对比
    {
        'name': 'MACD+RSI 基准',
        'use_chan': False,
        'use_macd': True,
        'use_rsi': True,
        'rsi_oversold': 20,
        'stop_loss': 0.05,
        'target_profit': 0.10,
        'use_trailing': False,
    },
    # 优化版 1: 缠论中枢+MACD+RSI+ 追踪
    {
        'name': '优化版 1-缠论综合',
        'use_chan': True,
        'chan_zhongshu_period': 60,
        'chan_zhongshu_range': 0.05,
        'use_macd': True,
        'use_rsi': True,
        'rsi_oversold': 20,
        'stop_loss': 0.05,
        'target_profit': 0.15,
        'use_trailing': True,
        'trailing_pct': 0.08,
        'use_volume_filter': False,
    },
    # 优化版 2: 中枢突破 + 高止盈
    {
        'name': '优化版 2-中枢突破',
        'use_chan': True,
        'chan_zhongshu_period': 60,
        'chan_zhongshu_range': 0.05,
        'use_macd': True,
        'use_rsi': False,
        'stop_loss': 0.04,
        'target_profit': 0.20,
        'use_trailing': True,
        'trailing_pct': 0.10,
    },
    # 优化版 3: 稳健型 (高胜率)
    {
        'name': '优化版 3-稳健型',
        'use_chan': True,
        'chan_zhongshu_period': 60,
        'chan_zhongshu_range': 0.05,
        'use_macd': True,
        'use_rsi': True,
        'rsi_oversold': 25,  # 更宽松
        'stop_loss': 0.04,   # 更紧
        'target_profit': 0.12,
        'use_trailing': True,
        'trailing_pct': 0.06,
    },
    # 优化版 4: 激进型 (高收益)
    {
        'name': '优化版 4-激进型',
        'use_chan': True,
        'chan_zhongshu_period': 60,
        'chan_zhongshu_range': 0.05,
        'use_macd': True,
        'use_rsi': True,
        'rsi_oversold': 15,  # 更严格
        'stop_loss': 0.06,   # 更宽
        'target_profit': 0.18,
        'use_trailing': True,
        'trailing_pct': 0.10,
    },
    # 优化版 5: 存储芯片专用 (针对龙头优化)
    {
        'name': '优化版 5-存储芯片专用',
        'use_chan': True,
        'chan_zhongshu_period': 60,
        'chan_zhongshu_range': 0.08,  # 更宽中枢
        'use_macd': True,
        'use_rsi': True,
        'rsi_oversold': 20,
        'stop_loss': 0.05,
        'target_profit': 0.15,
        'use_trailing': True,
        'trailing_pct': 0.08,
    },
]

class UltimateOptimizedStrategy(bt.Strategy):
    """终极优化策略"""
    params = (
        ('use_chan', True),
        ('chan_zhongshu_period', 60),
        ('chan_zhongshu_range', 0.05),
        ('use_macd', True),
        ('use_rsi', True),
        ('rsi_oversold', 20),
        ('rsi_overbought', 80),
        ('stop_loss', 0.05),
        ('target_profit', 0.15),
        ('use_trailing', True),
        ('trailing_pct', 0.08),
        ('use_volume_filter', False),
    )
    
    def __init__(self):
        self.order = None
        self.buy_price = None
        self.highest_price = None
        self.in_zhongshu = False
        
        # 缠论中枢 (用均线模拟)
        self.sma_zhongshu = bt.ind.SMA(self.data.close, period=self.params.chan_zhongshu_period)
        self.zhongshu_upper = self.sma_zhongshu * (1 + self.params.chan_zhongshu_range)
        self.zhongshu_lower = self.sma_zhongshu * (1 - self.params.chan_zhongshu_range)
        
        # 20 日均线 (短期趋势)
        self.sma20 = bt.ind.SMA(self.data.close, period=20)
        
        # MACD
        if self.params.use_macd:
            self.dif = self.datas[0].lines.dif
            self.dea = self.datas[0].lines.dea
            self.macd = self.datas[0].lines.macd
            self.macd_cross = bt.ind.CrossOver(self.dif, self.dea)
        
        # RSI
        if self.params.use_rsi:
            self.rsi = self.datas[0].lines.rsi6
        
        # 成交量均线
        if self.params.use_volume_filter:
            self.vol_ma = bt.ind.SMA(self.data.volume, period=20)
    
    def check_zhongshu_status(self):
        """检查中枢状态"""
        close = self.data.close[0]
        upper = self.zhongshu_upper[0]
        lower = self.zhongshu_lower[0]
        
        if close >= lower and close <= upper:
            self.in_zhongshu = True
            return 'in'
        elif close > upper:
            self.in_zhongshu = False
            return 'above'
        else:
            self.in_zhongshu = False
            return 'below'
    
    def is_breakout(self):
        """中枢突破"""
        close_now = self.data.close[0]
        close_prev = self.data.close[-1]
        upper_prev = self.zhongshu_upper[-1]
        upper_now = self.zhongshu_upper[0]
        
        # 从中枢内突破到中枢上
        return (close_prev <= upper_prev and close_now > upper_now)
    
    def is_pullback_buy(self):
        """中枢回踩买入"""
        close_now = self.data.close[0]
        close_prev = self.data.close[-1]
        lower_now = self.zhongshu_lower[0]
        sma20_now = self.sma20[0]
        
        # 回踩中枢下沿或 20 日线，但未跌破
        pullback_lower = (close_prev > lower_now and close_now <= lower_now * 1.02)
        pullback_sma20 = (close_prev > sma20_now and close_now <= sma20_now * 1.02)
        
        return (pullback_lower or pullback_sma20) and self.params.use_macd and self.macd_cross > 0
    
    def next(self):
        if self.order:
            # 追踪止损
            if self.params.use_trailing and self.position:
                if self.data.high[0] > self.highest_price:
                    self.highest_price = self.data.high[0]
                if self.data.low[0] < self.highest_price * (1 - self.params.trailing_pct):
                    self.sell()
            return
        
        # 买入信号
        if not self.position:
            buy_signal = False
            zhongshu_status = self.check_zhongshu_status()
            
            # 1. 中枢内 +MACD 金叉+RSI 超卖 (高胜率组合)
            if zhongshu_status == 'in' and self.params.use_macd and self.macd_cross > 0:
                if not self.params.use_rsi or self.rsi[0] < self.params.rsi_oversold:
                    buy_signal = True
            
            # 2. 中枢突破 (高收益)
            if self.params.use_chan and self.is_breakout():
                if self.params.use_macd and self.dif[0] > self.dea[0]:
                    buy_signal = True
            
            # 3. 回踩买入 (稳健)
            if self.params.use_chan and self.is_pullback_buy():
                buy_signal = True
            
            # 4. 纯 MACD+RSI(非缠论模式)
            if not self.params.use_chan and self.params.use_macd and self.macd_cross > 0:
                if self.data.close[0] > self.sma20[0]:
                    if not self.params.use_rsi or self.rsi[0] < self.params.rsi_oversold:
                        buy_signal = True
            
            if buy_signal:
                # 成交量过滤 (可选)
                if self.params.use_volume_filter:
                    if self.data.volume[0] < self.vol_ma[0] * 1.5:
                        return
                
                self.order = self.buy(size=1000)
                self.highest_price = self.data.close[0]
        
        # 卖出信号
        else:
            sell_signal = False
            zhongshu_status = self.check_zhongshu_status()
            
            # 止盈
            if self.data.close[0] >= self.buy_price * (1 + self.params.target_profit):
                sell_signal = True
            # 止损
            elif self.data.close[0] <= self.buy_price * (1 - self.params.stop_loss):
                sell_signal = True
            # MACD 死叉
            elif self.params.use_macd and self.macd_cross < 0:
                sell_signal = True
            # RSI 超买
            elif self.params.use_rsi and self.rsi[0] > self.params.rsi_overbought:
                sell_signal = True
            # 跌破中枢下沿
            elif self.params.use_chan and zhongshu_status == 'below':
                sell_signal = True
            
            if sell_signal:
                self.sell()
    
    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.highest_price = self.buy_price
        self.order = None

class SQLDataWithIndicators(bt.feeds.PandasData):
    lines = ('macd', 'dif', 'dea', 'rsi6', 'rsi12', 'rsi24')
    params = (('macd', -1), ('dif', -1), ('dea', -1), ('rsi6', -1), ('rsi12', -1), ('rsi24', -1),)

def get_stock_data(stock_code, start_date="2023-01-01", end_date="2026-03-12"):
    conn_h = sqlite3.connect(HISTORY_DB)
    conn_i = sqlite3.connect(INDICATORS_DB)
    
    df = pd.read_sql_query("""
        SELECT trade_date, open_price, close_price, high_price, low_price, volume
        FROM stock_daily WHERE stock_code = ? AND trade_date BETWEEN ? AND ?
        ORDER BY trade_date
    """, conn_h, params=(stock_code, start_date, end_date))
    
    if len(df) < 60:
        conn_h.close(); conn_i.close()
        return None
    
    df_macd = pd.read_sql_query("""
        SELECT trade_date, dif, dea, macd FROM stock_macd
        WHERE stock_code = ? AND trade_date BETWEEN ? AND ? ORDER BY trade_date
    """, conn_i, params=(stock_code, start_date, end_date))
    
    df_rsi = pd.read_sql_query("""
        SELECT trade_date, rsi6, rsi12, rsi24 FROM stock_rsi
        WHERE stock_code = ? AND trade_date BETWEEN ? AND ? ORDER BY trade_date
    """, conn_i, params=(stock_code, start_date, end_date))
    
    conn_h.close(); conn_i.close()
    
    df['date'] = pd.to_datetime(df['trade_date'])
    df.set_index('date', inplace=True)
    
    if len(df_macd) > 0:
        df_macd['date'] = pd.to_datetime(df_macd['trade_date'])
        df_macd.set_index('date', inplace=True)
        df = df.join(df_macd[['dif', 'dea', 'macd']], how='left')
    else:
        df['dif'] = 0; df['dea'] = 0; df['macd'] = 0
    
    if len(df_rsi) > 0:
        df_rsi['date'] = pd.to_datetime(df_rsi['trade_date'])
        df_rsi.set_index('date', inplace=True)
        df = df.join(df_rsi[['rsi6', 'rsi12', 'rsi24']], how='left')
    else:
        df['rsi6'] = 50; df['rsi12'] = 50; df['rsi24'] = 50
    
    df = df.fillna(0)
    df.rename(columns={'open_price': 'open', 'close_price': 'close',
                       'high_price': 'high', 'low_price': 'low', 'volume': 'volume'}, inplace=True)
    df['openinterest'] = 0
    
    return df[['open', 'high', 'low', 'close', 'volume', 'openinterest', 'macd', 'dif', 'dea', 'rsi6', 'rsi12', 'rsi24']]

def backtest_stock(df, params):
    try:
        cerebro = bt.Cerebro()
        data = SQLDataWithIndicators(dataname=df)
        cerebro.adddata(data)
        
        cerebro.addstrategy(UltimateOptimizedStrategy,
                          use_chan=params.get('use_chan', True),
                          chan_zhongshu_period=params.get('chan_zhongshu_period', 60),
                          chan_zhongshu_range=params.get('chan_zhongshu_range', 0.05),
                          use_macd=params.get('use_macd', True),
                          use_rsi=params.get('use_rsi', True),
                          rsi_oversold=params.get('rsi_oversold', 20),
                          rsi_overbought=params.get('rsi_overbought', 80),
                          stop_loss=params.get('stop_loss', 0.05),
                          target_profit=params.get('target_profit', 0.15),
                          use_trailing=params.get('use_trailing', True),
                          trailing_pct=params.get('trailing_pct', 0.08),
                          use_volume_filter=params.get('use_volume_filter', False))
        
        cerebro.broker.setcash(100000.0)
        cerebro.broker.setcommission(commission=0.001)
        
        initial = cerebro.broker.getvalue()
        cerebro.run()
        final = cerebro.broker.getvalue()
        
        return (final - initial) / initial
    except:
        return None

def main():
    print("="*70)
    print("【终极优化策略回测】")
    print("="*70)
    print(f"\n股票数量：{len(INDUSTRY_STOCKS_20)}")
    print(f"策略数量：{len(OPTIMIZED_PARAMS)}")
    print(f"回测期间：2023-01-01 ~ 2026-03-12")
    
    all_results = {}
    
    for params in OPTIMIZED_PARAMS:
        strategy_name = params['name']
        print(f"\n【策略：{strategy_name}】")
        
        results = []
        for i, stock in enumerate(INDUSTRY_STOCKS_20):
            code = stock['code']
            name = stock['name']
            
            print(f"  [{i+1:2d}/20] {name} ({code})", end=" ... ")
            
            df = get_stock_data(code)
            if df is None or len(df) < 60:
                print("数据不足")
                continue
            
            ret = backtest_stock(df, params)
            if ret is not None:
                results.append({'code': code, 'name': name, 'sector': stock['sector'], 'return': ret})
                print(f"{ret:.2%}")
            else:
                print("失败")
        
        if results:
            returns = [r['return'] for r in results]
            avg_return = np.mean(returns)
            sharpe = (avg_return / np.std(returns)) if np.std(returns) > 0 else 0
            win_rate = sum(1 for r in returns if r > 0) / len(returns)
            
            # 行业统计
            sector_stats = {}
            for r in results:
                sec = r['sector']
                if sec not in sector_stats:
                    sector_stats[sec] = []
                sector_stats[sec].append(r['return'])
            
            sector_summary = {sec: {'avg': np.mean(rets), 'count': len(rets), 'best': max(rets)} 
                             for sec, rets in sector_stats.items()}
            
            # 用户指定股票统计
            user_stocks = ['000559', '301308', '600096', '300468', '600989', '600256', '601600', '002384']
            user_results = [r for r in results if r['code'] in user_stocks]
            user_avg = np.mean([r['return'] for r in user_results]) if user_results else 0
            
            all_results[strategy_name] = {
                'params': params,
                'avg_return': avg_return,
                'sharpe': sharpe,
                'win_rate': win_rate,
                'count': len(results),
                'details': results,
                'sector_summary': sector_summary,
                'user_stocks_avg': user_avg
            }
            
            print(f"\n  平均收益：{avg_return:.2%} | 夏普：{sharpe:.2f} | 胜率：{win_rate:.1%}")
            print(f"  用户指定股票平均：{user_avg:.2%}")
    
    # 结果分析
    print("\n" + "="*70)
    print("【回测结果分析】")
    print("="*70)
    
    sorted_strategies = sorted(all_results.items(), key=lambda x: x[1]['sharpe'], reverse=True)
    
    print("\n【策略排名 (按夏普)】\n")
    for i, (name, data) in enumerate(sorted_strategies, 1):
        emoji = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"{i}"))
        print(f"{emoji} {name}")
        print(f"   收益：{data['avg_return']:.2%} | 夏普：{data['sharpe']:.2f} | 胜率：{data['win_rate']:.1%}")
        print(f"   用户股票：{data['user_stocks_avg']:.2%}")
        print()
    
    # 按收益排名
    sorted_by_return = sorted(all_results.items(), key=lambda x: x[1]['avg_return'], reverse=True)
    print("\n【策略排名 (按收益)】\n")
    for i, (name, data) in enumerate(sorted_by_return[:3], 1):
        emoji = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"{i}"))
        print(f"{emoji} {name}: {data['avg_return']:.2%} (胜率{data['win_rate']:.1%})")
    
    # 最优策略
    best_name, best_data = sorted_strategies[0]
    best_by_return = sorted_by_return[0]
    
    # 个股排名
    print("\n【个股排名 Top 10】(按最优夏普策略)\n")
    top_stocks = sorted(best_data['details'], key=lambda x: x['return'], reverse=True)[:10]
    for i, stock in enumerate(top_stocks, 1):
        print(f"{i}. {stock['name']} ({stock['code']}) - {stock['sector']}: {stock['return']:.2%}")
    
    # 保存
    output_dir = "/root/.openclaw/workspace/memory/stock-analysis/"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = output_dir + f"终极优化策略回测_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'stocks': INDUSTRY_STOCKS_20,
            'strategies': OPTIMIZED_PARAMS,
            'best_by_sharpe': best_name,
            'best_by_return': best_by_return[0],
            'best_data': best_data,
            'top_stocks': top_stocks,
            'all_results': all_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 结果已保存：{output_file}")
    
    # 生成优化建议
    print("\n" + "="*70)
    print("【策略优化建议】")
    print("="*70)
    
    print(f"\n✅ 最优策略 (夏普): {best_name}")
    print(f"   参数配置:")
    best_params = best_data['params']
    print(f"   - 缠论中枢：{'启用' if best_params.get('use_chan') else '禁用'}")
    print(f"   - 中枢周期：{best_params.get('chan_zhongshu_period', 60)}日")
    print(f"   - MACD: {'启用' if best_params.get('use_macd') else '禁用'}")
    print(f"   - RSI: {'启用' if best_params.get('use_rsi') else '禁用'}")
    print(f"   - 止损：{best_params.get('stop_loss', 0.05):.1%}")
    print(f"   - 止盈：{best_params.get('target_profit', 0.15):.1%}")
    print(f"   - 追踪止损：{'启用' if best_params.get('use_trailing') else '禁用'} ({best_params.get('trailing_pct', 0.08):.1%})")
    
    print(f"\n✅ 最高收益策略：{best_by_return[0]}")
    print(f"   平均收益：{best_by_return[1]['avg_return']:.2%}")
    print(f"   胜率：{best_by_return[1]['win_rate']:.1%}")
    
    print("\n✅ 行业配置建议:")
    sector_all = best_data['sector_summary']
    for sec, stats in sorted(sector_all.items(), key=lambda x: x[1]['avg'], reverse=True)[:5]:
        print(f"   - {sec}: {stats['avg']:.2%} (建议{'超配' if stats['avg'] > 0.1 else '标配'})")
    
    print("\n✅ 个股推荐:")
    for i, stock in enumerate(top_stocks[:5], 1):
        print(f"   {i}. {stock['name']} ({stock['code']}): {stock['return']:.2%}")
    
    print("\n✅ 回测完成")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
港股策略优化 v4 - 超宽松策略
目标：高胜率 + 高收益
策略：宽松信号 + 趋势确认 + 灵活持有期
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

HK_STOCKS = ["9988.HK", "1211.HK", "9618.HK"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=180)

print("\n" + "=" * 80)
print("🚀 策略优化 v4 - 超宽松策略")
print("=" * 80)

# 下载数据
data = {}
for symbol in HK_STOCKS:
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START_DATE, end=END_DATE)
    if len(df) > 20:
        data[symbol] = df
        print(f"  ✅ {symbol}: {len(df)} 天")

def backtest_v4(df, entry_thresh, exit_thresh, hold_min, hold_max):
    """
    超宽松策略：
    1. 宽松入场（涨跌幅>阈值）
    2. 灵活出场（持有 N 天后任意时点平仓）
    3. 趋势确认（价格在 MA20 上方）
    """
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    df['MA20'] = df['Close'].rolling(20).mean()
    
    in_position = False
    entry_price = 0
    entry_idx = 0
    trades = []
    wins = 0
    losses = 0
    
    for idx, (i, row) in enumerate(df.iterrows()):
        ret = row['Return']
        price = float(row['Close'])
        
        if pd.isna(ret) or pd.isna(row.get('MA20', np.nan)):
            continue
        
        # 开仓
        if not in_position:
            # 宽松信号：涨跌幅超过阈值
            if abs(ret) >= entry_thresh:
                # 趋势确认：价格在 MA20 上方（做多）
                if price > row['MA20']:
                    in_position = True
                    entry_price = price
                    entry_idx = idx
                    trades.append({'type': 'BUY', 'price': price, 'idx': idx})
        
        # 平仓
        else:
            days_held = idx - entry_idx
            
            # 持有至少 hold_min 天
            if days_held >= hold_min:
                # 获利平仓 或 持有超过 hold_max 天强制平仓
                pnl = (price - entry_price) / entry_price
                
                if pnl >= exit_thresh or days_held >= hold_max:
                    trades.append({'type': 'SELL', 'price': price, 'pnl': pnl})
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                    in_position = False
    
    total_trades = wins + losses
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    total_return = sum(t.get('pnl', 0) for t in trades if t['type']=='SELL') * 100
    
    return {
        'total_return': total_return,
        'win_rate': win_rate,
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses
    }

# 参数测试
print("\n🔬 测试不同参数组合...")
print("=" * 80)

best_result = None
best_params = None

# 测试多组参数
for entry in [0.01, 0.015, 0.02, 0.025]:
    for exit_p in [0.02, 0.03, 0.05, 0.08]:
        for hold_min in [1, 2, 3]:
            for hold_max in [5, 10, 15, 20]:
                stock_results = []
                for symbol, df in data.items():
                    result = backtest_v4(df, entry, exit_p, hold_min, hold_max)
                    stock_results.append(result)
                
                avg_return = sum(r['total_return'] for r in stock_results) / len(stock_results)
                avg_wr = sum(r['win_rate'] for r in stock_results) / len(stock_results)
                total_trades = sum(r['total_trades'] for r in stock_results)
                
                # 评分：收益 60% + 胜率 40%
                score = avg_return * 0.6 + avg_wr * 0.4
                
                if best_result is None or score > best_result.get('score', -999):
                    best_result = {
                        'avg_return': avg_return,
                        'avg_win_rate': avg_wr,
                        'total_trades': total_trades,
                        'score': score
                    }
                    best_params = (entry, exit_p, hold_min, hold_max)

# 输出
print("\n" + "=" * 80)
print("🏆 最优参数")
print("=" * 80)

if best_params:
    entry, exit_p, hold_min, hold_max = best_params
    print(f"\n参数：")
    print(f"  入场阈值：±{entry*100:.1f}%")
    print(f"  出场阈值：+{exit_p*100:.1f}%")
    print(f"  持有期：{hold_min}-{hold_max} 天")
    print(f"\n绩效（180 天）：")
    print(f"  总收益：{best_result['avg_return']:.2f}%")
    print(f"  胜率：{best_result['avg_win_rate']:.1f}%")
    print(f"  交易数：{best_result['total_trades']} 次")
    print(f"  综合评分：{best_result['score']:.2f}")
    
    # 距离目标
    print(f"\n🎯 距离目标：")
    wr_gap = 90 - best_result['avg_win_rate']
    ret_gap = 200 - best_result['avg_return']
    print(f"  胜率：{best_result['avg_win_rate']:.1f}% / 90% (差距：{wr_gap:.1f}%)")
    print(f"  收益：{best_result['avg_return']:.2f}% / 200% (差距：{ret_gap:.2f}%)")

print("\n" + "=" * 80)
print("✅ 测试完成")
print("=" * 80)

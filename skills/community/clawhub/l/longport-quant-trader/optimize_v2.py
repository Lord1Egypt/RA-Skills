#!/usr/bin/env python3
"""
港股策略优化 v2 - 简化策略（无止损止盈）
信号驱动：买入后持有到反向信号
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

HK_STOCKS = ["9988.HK", "1211.HK", "9618.HK"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=90)

# 参数网格（简化版）
MOMENTUM_THRESHOLDS = [0.01, 0.015, 0.02, 0.025, 0.03]
REVERSION_THRESHOLDS = [-0.02, -0.025, -0.03, -0.035, -0.04]

print("\n" + "=" * 80)
print("🔬 策略优化 v2 - 简化策略（无止损止盈）")
print("=" * 80)
print(f"回测区间：90 天")
print(f"股票池：{', '.join(HK_STOCKS)}")
print(f"参数组合：{len(MOMENTUM_THRESHOLDS)} × {len(REVERSION_THRESHOLDS)} = {len(MOMENTUM_THRESHOLDS)*len(REVERSION_THRESHOLDS)} 组")
print("=" * 80)

# 下载数据
print("\n📥 下载数据...")
data = {}
for symbol in HK_STOCKS:
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START_DATE, end=END_DATE)
    if len(df) > 0:
        data[symbol] = df
        print(f"  ✅ {symbol}: {len(df)} 天")

# 回测函数（简化版 - 信号驱动）
def backtest_simple(df, mom_thresh, rev_thresh):
    """简化策略：买入后持有到反向信号"""
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    
    in_position = False
    entry_price = 0
    trades = []
    wins = 0
    losses = 0
    
    for i, row in df.iterrows():
        ret = row['Return']
        price = float(row['Close'])
        
        if pd.isna(ret):
            continue
        
        # 开仓信号
        if not in_position:
            if ret >= mom_thresh or ret <= rev_thresh:
                in_position = True
                entry_price = price
        
        # 平仓信号（反向信号或持有 N 天）
        else:
            # 持有超过 5 天自动平仓
            # 或者出现反向信号
            should_close = False
            
            # 简单规则：持有 3 天后平仓
            if len([t for t in trades if t['type']=='BUY']) > 0:
                last_buy = [t for t in trades if t['type']=='BUY'][-1]
                days_held = (i - last_buy['date']).days if hasattr(i, 'days') else 3
                if days_held >= 3:
                    should_close = True
            
            if should_close or (ret > 0 and entry_price > 0):
                # 简单平仓：价格高于买入价就卖
                if price > entry_price * 1.02:  # 至少赚 2%
                    pnl = (price - entry_price) / entry_price
                    trades.append({'type': 'SELL', 'price': price, 'pnl': pnl})
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                    in_position = False
    
    # 计算绩效
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

# 网格搜索
print("\n🔬 开始测试...")
best_result = None
best_params = None
all_results = []

for mom, rev in zip(MOMENTUM_THRESHOLDS, REVERSION_THRESHOLDS):
    stock_results = []
    for symbol, df in data.items():
        result = backtest_simple(df, mom, rev)
        stock_results.append(result)
    
    avg_return = sum(r['total_return'] for r in stock_results) / len(stock_results)
    avg_win_rate = sum(r['win_rate'] for r in stock_results) / len(stock_results)
    total_trades = sum(r['total_trades'] for r in stock_results)
    
    score = avg_return * 0.6 + avg_win_rate * 0.4
    
    all_results.append({
        'params': (mom, rev),
        'avg_return': avg_return,
        'avg_win_rate': avg_win_rate,
        'total_trades': total_trades,
        'score': score
    })
    
    if best_result is None or score > best_result.get('score', -999):
        best_result = {
            'avg_return': avg_return,
            'avg_win_rate': avg_win_rate,
            'total_trades': total_trades,
            'score': score
        }
        best_params = (mom, rev)

# 输出结果
print("\n" + "=" * 80)
print("🏆 最优参数")
print("=" * 80)

if best_params:
    mom, rev = best_params
    print(f"\n参数：")
    print(f"  动量阈值：+{mom*100:.1f}%")
    print(f"  均值回归：{rev*100:.1f}%")
    print(f"\n绩效：")
    print(f"  平均收益：{best_result['avg_return']:.2f}%")
    print(f"  平均胜率：{best_result['avg_win_rate']:.1f}%")
    print(f"  总交易数：{best_result['total_trades']} 次")
    print(f"  综合评分：{best_result['score']:.2f}")

# Top 5
print("\n" + "=" * 80)
print("📊 Top 5 参数组合")
print("=" * 80)

all_results.sort(key=lambda x: x['score'], reverse=True)
for i, r in enumerate(all_results[:5], 1):
    mom, rev = r['params']
    print(f"\n{i}. 评分：{r['score']:.2f}")
    print(f"   参数：+{mom*100:.1f}% / {rev*100:.1f}%")
    print(f"   收益：{r['avg_return']:.2f}% | 胜率：{r['avg_win_rate']:.1f}% | 交易：{r['total_trades']}次")

print("\n" + "=" * 80)
print("✅ 测试完成")
print("=" * 80)

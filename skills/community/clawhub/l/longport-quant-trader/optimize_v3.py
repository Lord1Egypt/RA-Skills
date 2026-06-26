#!/usr/bin/env python3
"""
港股策略优化 v3 - 多因子增强策略
目标：胜率>90% + 收益>200%

增强因子：
1. 趋势过滤（均线）
2. 成交量确认
3. 波动率筛选
4. 持有期优化
"""
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from itertools import product

HK_STOCKS = ["9988.HK", "1211.HK", "9618.HK"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=180)  # 延长到 180 天

print("\n" + "=" * 80)
print("🚀 策略优化 v3 - 多因子增强（目标：胜率>90% + 收益>200%）")
print("=" * 80)
print(f"回测区间：180 天")
print(f"股票池：{', '.join(HK_STOCKS)}")
print("=" * 80)

# 下载数据
print("\n📥 下载数据...")
data = {}
for symbol in HK_STOCKS:
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START_DATE, end=END_DATE)
    if len(df) > 20:
        data[symbol] = df
        print(f"  ✅ {symbol}: {len(df)} 天")

# 计算技术指标
def add_indicators(df):
    """添加技术指标"""
    df = df.copy()
    
    # 先计算收益率
    df['Return'] = df['Close'].pct_change()
    
    # 均线
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 成交量变化
    df['Vol_Change'] = df['Volume'].pct_change()
    
    # 波动率
    df['Volatility'] = df['Return'].rolling(20).std()
    
    return df

# 增强策略回测
def backtest_enhanced(df, mom_thresh, rev_thresh, hold_days):
    """
    增强策略：
    1. 趋势过滤：价格在 MA20 上方才做多
    2. RSI 过滤：RSI<70 避免超买
    3. 成交量确认：成交量放大
    4. 固定持有期
    """
    df = add_indicators(df)
    df['Return'] = df['Close'].pct_change()
    
    in_position = False
    entry_price = 0
    entry_date = None
    trades = []
    wins = 0
    losses = 0
    
    for i, row in df.iterrows():
        ret = row['Return']
        price = float(row['Close'])
        
        if pd.isna(ret) or pd.isna(row.get('MA20', np.nan)):
            continue
        
        # 开仓信号
        if not in_position:
            # 基础信号
            base_signal = ret >= mom_thresh or ret <= rev_thresh
            
            # 趋势过滤：价格在 MA20 上方
            trend_ok = price > row['MA20']
            
            # RSI 过滤：未超买
            rsi_ok = row.get('RSI', 50) < 70
            
            # 成交量过滤：放量
            vol_ok = row.get('Vol_Change', 0) > -0.5  # 不缩量即可
            
            if base_signal and trend_ok and rsi_ok and vol_ok:
                in_position = True
                entry_price = price
                entry_date = i
                trades.append({'type': 'BUY', 'price': price, 'date': i})
        
        # 平仓信号
        else:
            # 持有固定天数
            if entry_date:
                days_held = (i - entry_date).days if hasattr(i, 'days') else 1
                if days_held >= hold_days:
                    pnl = (price - entry_price) / entry_price
                    trades.append({'type': 'SELL', 'price': price, 'pnl': pnl})
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                    in_position = False
    
    # 绩效
    total_trades = wins + losses
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    total_return = sum(t.get('pnl', 0) for t in trades if t['type']=='SELL') * 100
    
    # 年化收益率
    if total_trades > 0:
        annual_return = (1 + total_return/100) ** (365/180) - 1
    else:
        annual_return = 0
    
    return {
        'total_return': total_return,
        'annual_return': annual_return * 100,
        'win_rate': win_rate,
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses
    }

# 参数网格
MOMENTUMS = [0.01, 0.015, 0.02]
REVERSIONS = [-0.02, -0.025, -0.03]
HOLD_PERIODS = [3, 5, 7, 10]  # 持有 3/5/7/10 天

print(f"\n参数组合：{len(MOMENTUMS)} × {len(REVERSIONS)} × {len(HOLD_PERIODS)} = {len(MOMENTUMS)*len(REVERSIONS)*len(HOLD_PERIODS)} 组")
print("\n🔬 开始测试...")

best_result = None
best_params = None
all_results = []

for mom, rev, hold in product(MOMENTUMS, REVERSIONS, HOLD_PERIODS):
    stock_results = []
    for symbol, df in data.items():
        result = backtest_enhanced(df, mom, rev, hold)
        stock_results.append(result)
    
    avg_return = sum(r['total_return'] for r in stock_results) / len(stock_results)
    avg_annual = sum(r['annual_return'] for r in stock_results) / len(stock_results)
    avg_win_rate = sum(r['win_rate'] for r in stock_results) / len(stock_results)
    total_trades = sum(r['total_trades'] for r in stock_results)
    
    # 综合评分：收益 50% + 胜率 50%
    score = avg_return * 0.5 + avg_win_rate * 0.5
    
    all_results.append({
        'params': (mom, rev, hold),
        'avg_return': avg_return,
        'avg_annual': avg_annual,
        'avg_win_rate': avg_win_rate,
        'total_trades': total_trades,
        'score': score
    })
    
    if best_result is None or score > best_result.get('score', -999):
        best_result = {
            'avg_return': avg_return,
            'avg_annual': avg_annual,
            'avg_win_rate': avg_win_rate,
            'total_trades': total_trades,
            'score': score
        }
        best_params = (mom, rev, hold)

# 输出结果
print("\n" + "=" * 80)
print("🏆 最优参数")
print("=" * 80)

if best_params:
    mom, rev, hold = best_params
    print(f"\n参数配置：")
    print(f"  动量阈值：+{mom*100:.1f}%")
    print(f"  均值回归：{rev*100:.1f}%")
    print(f"  持有期：{hold} 天")
    print(f"\n增强因子：")
    print(f"  ✅ 趋势过滤（MA20）")
    print(f"  ✅ RSI 过滤（<70）")
    print(f"  ✅ 成交量确认")
    print(f"\n回测绩效（180 天）：")
    print(f"  总收益：{best_result['avg_return']:.2f}%")
    print(f"  年化收益：{best_result['avg_annual']:.2f}%")
    print(f"  胜率：{best_result['avg_win_rate']:.1f}%")
    print(f"  交易数：{best_result['total_trades']} 次")
    print(f"  综合评分：{best_result['score']:.2f}")

# Top 10
print("\n" + "=" * 80)
print("📊 Top 10 参数组合")
print("=" * 80)

all_results.sort(key=lambda x: x['score'], reverse=True)

for i, r in enumerate(all_results[:10], 1):
    mom, rev, hold = r['params']
    print(f"\n{i}. 评分：{r['score']:.2f}")
    print(f"   参数：+{mom*100:.1f}% / {rev*100:.1f}% / {hold}天")
    print(f"   总收益：{r['avg_return']:.2f}% | 年化：{r['avg_annual']:.2f}%")
    print(f"   胜率：{r['avg_win_rate']:.1f}% | 交易：{r['total_trades']}次")

# 距离目标
print("\n" + "=" * 80)
print("🎯 距离目标")
print("=" * 80)

target_win_rate = 90
target_return = 200

best_wr = best_result['avg_win_rate'] if best_result else 0
best_ret = best_result['avg_return'] if best_result else 0

print(f"胜率：{best_wr:.1f}% / {target_win_rate}% (差距：{target_win_rate - best_wr:.1f}%)")
print(f"收益：{best_ret:.2f}% / {target_return}% (差距：{target_return - best_ret:.2f}%)")

if best_wr >= target_win_rate and best_ret >= target_return:
    print("\n✅🎉 目标达成！")
else:
    print("\n⚠️ 继续优化...")

print("\n" + "=" * 80)
print("✅ 测试完成")
print("=" * 80)

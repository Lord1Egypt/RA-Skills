#!/usr/bin/env python3
"""
600323 瀚蓝环境 - 股票分析
"""

import akshare as ak
import pandas as pd
from datetime import datetime

print("=" * 60)
print("📊 600323 瀚蓝环境 - 股票分析报告")
print("=" * 60)
print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

try:
    # 1. 获取实时行情
    print("📈 【实时行情】")
    print("-" * 60)
    spot = ak.stock_zh_a_spot_em()
    stock_data = spot[spot['代码'] == '600323']
    
    if not stock_data.empty:
        current_price = stock_data['最新价'].values[0]
        change = stock_data['涨跌幅'].values[0]
        volume = stock_data['成交量'].values[0]
        amount = stock_data['成交额'].values[0]
        high = stock_data['最高'].values[0]
        low = stock_data['最低'].values[0]
        open_price = stock_data['今开'].values[0]
        prev_close = stock_data['昨收'].values[0]
        
        print(f"当前价格：¥{current_price:.2f}")
        print(f"涨跌幅度：{change:+.2f}%")
        print(f"最高价格：¥{high:.2f}")
        print(f"最低价格：¥{low:.2f}")
        print(f"今开价格：¥{open_price:.2f}")
        print(f"昨日收盘：¥{prev_close:.2f}")
        print(f"成交量：{volume/10000:.2f}万手")
        print(f"成交额：{amount/100000000:.2f}亿元")
    else:
        print("未找到 600323 实时行情数据")
    
    print()
    
    # 2. 获取历史 K 线（最近 90 天）
    print("📉 【近期走势】（最近 90 天）")
    print("-" * 60)
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    kline = ak.stock_zh_a_hist(
        symbol="600323",
        period="daily",
        start_date=start_date.strftime("%Y%m%d"),
        end_date=end_date.strftime("%Y%m%d"),
        adjust="qfq"
    )
    
    if not kline.empty:
        # 计算技术指标
        kline['MA5'] = kline['收盘'].rolling(5).mean()
        kline['MA10'] = kline['收盘'].rolling(10).mean()
        kline['MA20'] = kline['收盘'].rolling(20).mean()
        kline['MA60'] = kline['收盘'].rolling(60).mean()
        
        latest = kline.iloc[-1]
        prev = kline.iloc[-2]
        
        print(f"最新收盘价：¥{latest['收盘']:.2f}")
        print(f"5 日均线：¥{latest['MA5']:.2f}")
        print(f"10 日均线：¥{latest['MA10']:.2f}")
        print(f"20 日均线：¥{latest['MA20']:.2f}")
        print(f"60 日均线：¥{latest['MA60']:.2f}")
        print()
        
        # 90 天涨跌统计
        start_price = kline.iloc[0]['收盘']
        end_price = kline.iloc[-1]['收盘']
        period_change = ((end_price - start_price) / start_price) * 100
        
        print(f"90 天涨幅：{period_change:+.2f}%")
        print(f"90 天最高：¥{kline['最高'].max():.2f}")
        print(f"90 天最低：¥{kline['最低'].min():.2f}")
        
        # 判断趋势
        print()
        print("📊 【趋势判断】")
        print("-" * 60)
        
        if latest['收盘'] > latest['MA5'] > latest['MA10'] > latest['MA20']:
            print("✅ 多头排列 - 短期趋势向好")
        elif latest['收盘'] < latest['MA5'] < latest['MA10'] < latest['MA20']:
            print("❌ 空头排列 - 短期趋势向淡")
        else:
            print("⚠️  震荡整理 - 方向不明")
        
        # 均线支撑/压力
        if latest['收盘'] > latest['MA20']:
            print(f"✅ 股价在 20 日均线上方 - 支撑位：¥{latest['MA20']:.2f}")
        else:
            print(f"❌ 股价在 20 日均线下方 - 压力位：¥{latest['MA20']:.2f}")
        
        if latest['收盘'] > latest['MA60']:
            print(f"✅ 股价在 60 日均线上方 - 中期趋势向好")
        else:
            print(f"❌ 股价在 60 日均线下方 - 中期趋势向淡")
        
        print()
        
        # 3. 买卖信号分析
        print("🎯 【买卖信号分析】")
        print("-" * 60)
        
        signals = []
        
        # 均线金叉/死叉
        if latest['MA5'] > latest['MA10'] and prev['MA5'] <= prev['MA10']:
            signals.append("✅ 5 日/10 日均线金叉 - 买入信号")
        elif latest['MA5'] < latest['MA10'] and prev['MA5'] >= prev['MA10']:
            signals.append("❌ 5 日/10 日均线死叉 - 卖出信号")
        
        # 突破 20 日均线
        if latest['收盘'] > latest['MA20'] and prev['收盘'] <= prev['MA20']:
            signals.append("✅ 突破 20 日均线 - 买入信号")
        elif latest['收盘'] < latest['MA20'] and prev['收盘'] >= prev['MA20']:
            signals.append("❌ 跌破 20 日均线 - 卖出信号")
        
        # 成交量分析
        avg_volume = kline['成交量'].rolling(5).mean().iloc[-1]
        if latest['成交量'] > avg_volume * 1.5:
            signals.append("📈 成交量放大 - 可能有行情")
        elif latest['成交量'] < avg_volume * 0.5:
            signals.append("📉 成交量萎缩 - 观望为主")
        
        if signals:
            for signal in signals:
                print(signal)
        else:
            print("⚠️  无明显买卖信号 - 继续观察")
        
        print()
        
        # 4. 操作建议
        print("💡 【操作建议】")
        print("-" * 60)
        
        # 综合评分
        score = 50  # 基础分
        
        if latest['收盘'] > latest['MA20']:
            score += 10
        if latest['MA5'] > latest['MA10']:
            score += 10
        if latest['MA10'] > latest['MA20']:
            score += 10
        if period_change > 0:
            score += 10
        if latest['成交量'] > avg_volume:
            score += 10
        
        print(f"综合评分：{score}/100")
        print()
        
        if score >= 80:
            print("🟢 强烈建议买入 - 多个指标向好")
            print(f"   建议仓位：30-50%")
            print(f"   止损位：¥{latest['MA20'] * 0.95:.2f} (-5%)")
            print(f"   目标位：¥{latest['收盘'] * 1.1:.2f} (+10%)")
        elif score >= 60:
            print("🟡 可以考虑买入 - 趋势向好")
            print(f"   建议仓位：10-20%")
            print(f"   止损位：¥{latest['MA20'] * 0.95:.2f} (-5%)")
            print(f"   目标位：¥{latest['收盘'] * 1.05:.2f} (+5%)")
        elif score >= 40:
            print("🟠 建议观望 - 方向不明")
            print(f"   等待明确信号再入场")
        else:
            print("🔴 不建议买入 - 趋势向淡")
            print(f"   等待底部信号")
        
        print()
        print("⚠️  风险提示：")
        print("   1. 以上分析仅供参考，不构成投资建议")
        print("   2. 股市有风险，投资需谨慎")
        print("   3. 请结合基本面和消息面综合判断")
        print("   4. 设置止损，控制仓位")
        
    else:
        print("未获取到 K 线数据")
    
except Exception as e:
    print(f"❌ 分析失败：{e}")
    print()
    print("可能原因：")
    print("1. 网络连接问题")
    print("2. 数据源接口变动")
    print("3. 股票代码错误")
    print()
    print("建议：")
    print("1. 检查网络连接")
    print("2. 使用交易软件查看实时数据")
    print("3. 咨询专业投资顾问")

print()
print("=" * 60)

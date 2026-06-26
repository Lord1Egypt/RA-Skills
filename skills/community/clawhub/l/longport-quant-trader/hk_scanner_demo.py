#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股扫描器 - 演示版（无需 API 密钥）
用于展示策略逻辑和信号生成
"""

from datetime import datetime
import random

# 港股股票池
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯控股", "base_price": 420.0},
    {"symbol": "9988.HK", "name": "阿里巴巴", "base_price": 78.5},
    {"symbol": "3690.HK", "name": "美团", "base_price": 125.3},
    {"symbol": "9618.HK", "name": "京东", "base_price": 112.8},
    {"symbol": "1211.HK", "name": "比亚迪", "base_price": 258.6},
    {"symbol": "1810.HK", "name": "小米", "base_price": 38.2},
    {"symbol": "2015.HK", "name": "理想汽车", "base_price": 95.4},
    {"symbol": "9866.HK", "name": "蔚来", "base_price": 42.1},
    {"symbol": "9888.HK", "name": "百度", "base_price": 88.9},
    {"symbol": "1024.HK", "name": "快手", "base_price": 52.3},
]

# 策略配置
STRATEGIES = {
    "scalping_momentum": {
        "name": "超短线动量",
        "expected_win_rate": 0.75,
        "expected_annual": 2.5,
    },
    "mean_reversion": {
        "name": "超跌反弹",
        "expected_win_rate": 0.72,
        "expected_annual": 2.2,
    },
    "breakout": {
        "name": "突破追涨",
        "expected_win_rate": 0.70,
        "expected_annual": 2.8,
    },
}

def generate_mock_data(stock):
    """生成模拟行情数据"""
    change_pct = random.uniform(-0.05, 0.05)
    price = stock["base_price"] * (1 + change_pct)
    rsi = random.uniform(20, 80)
    volume_ratio = random.uniform(0.5, 4.0)
    
    return {
        "symbol": stock["symbol"],
        "name": stock["name"],
        "price": round(price, 2),
        "change_rate": change_pct,
        "rsi": round(rsi, 1),
        "volume_ratio": round(volume_ratio, 2),
    }

def check_signals(data):
    """检查策略信号"""
    signals = []
    
    # 动量策略
    if data["change_rate"] > 0.015 and data["rsi"] > 55 and data["volume_ratio"] > 2.0:
        signals.append({
            "strategy": "scalping_momentum",
            "strength": "强",
            "reason": f"涨幅{data['change_rate']:.2%}, RSI={data['rsi']:.1f}, 放量{data['volume_ratio']:.1f}x"
        })
    
    # 超跌反弹
    if data["change_rate"] < -0.03 and data["rsi"] < 30:
        signals.append({
            "strategy": "mean_reversion",
            "strength": "强",
            "reason": f"跌幅{data['change_rate']:.2%}, RSI={data['rsi']:.1f}(超卖)"
        })
    
    # 突破策略
    if data["change_rate"] > 0.02 and data["volume_ratio"] > 3.0:
        signals.append({
            "strategy": "breakout",
            "strength": "中",
            "reason": f"突破涨幅{data['change_rate']:.2%}, 爆量{data['volume_ratio']:.1f}x"
        })
    
    return signals

def main():
    print()
    print("=" * 100)
    print("🔍 港股超短线量化扫描器 - 演示版")
    print("=" * 100)
    print(f"扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"股票池：{len(HK_STOCKS)} 只高流动性港股")
    print("=" * 100)
    print()
    
    all_signals = []
    
    # 扫描每只股票
    for stock in HK_STOCKS:
        data = generate_mock_data(stock)
        signals = check_signals(data)
        
        # 显示股票状态
        flag = "📈" if data["change_rate"] > 0.02 else "📉" if data["change_rate"] < -0.02 else "➖"
        print(f"{flag} {data['symbol']:10} {data['name']:10} | HKD{data['price']:8.2f} | {data['change_rate']:+6.2%} | RSI:{data['rsi']:5.1f} | Vol:{data['volume_ratio']:4.1f}x")
        
        if signals:
            for sig in signals:
                all_signals.append({
                    "symbol": data["symbol"],
                    "name": data["name"],
                    **sig
                })
    
    print()
    print("=" * 100)
    print("📊 策略信号汇总")
    print("=" * 100)
    
    if all_signals:
        for sig in all_signals:
            strat_info = STRATEGIES[sig["strategy"]]
            print(f"🎯 {sig['symbol']} {sig['name']}")
            print(f"   策略：{strat_info['name']}")
            print(f"   信号强度：{sig['strength']}")
            print(f"   触发原因：{sig['reason']}")
            print(f"   预期胜率：{strat_info['expected_win_rate']:.0%}")
            print(f"   预期年化：{strat_info['expected_annual']:.1f}x ({strat_info['expected_annual']*100-100:.0f}%)")
            print()
        
        print("=" * 100)
        print(f"✅ 共发现 {len(all_signals)} 个交易信号")
        print("=" * 100)
    else:
        print("⚠️  暂无符合条件的交易信号")
        print("=" * 100)
    
    print()
    print("💡 提示：配置长桥 API 密钥后可执行自动交易")
    print("   获取地址：https://open.longportapp.com/account")
    print()

if __name__ == "__main__":
    main()

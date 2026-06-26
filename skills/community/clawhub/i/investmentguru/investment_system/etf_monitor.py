#!/usr/bin/env python3
"""
国家队ETF监测系统 - 增强版 v2
结合：ETF成交额 + 北向资金（绝对值 + 变化）
"""
import requests
import json
from datetime import datetime, timedelta

# ============ ETF配置 ============
ETF_DATA = {
    "510300": "sh510300",
    "510050": "sh510050", 
    "510500": "sh510500",
    "588000": "sh588000",
    "512100": "sh512100",
    "512000": "sh512000",
    "515880": "sh515880",
    "512880": "sh512880",
}

# ============ 北向资金 ============
def get_north_money():
    """获取北向资金（最近5天）"""
    try:
        import tushare as ts
        token = 'b8ef516ff4abecadc1cdb55956458c3fed0378f8f85c30460f0d4500'
        ts.set_token(token)
        pro = ts.pro_api()
        
        results = []
        for i in range(10):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
            try:
                df = pro.moneyflow_hsgt(trade_date=date)
                if df is not None and not df.empty:
                    row = df.iloc[0]
                    north = float(row['north_money']) / 1e4
                    results.append({'date': date, 'north': north})
                    if len(results) >= 5:
                        break
            except:
                continue
        
        return results if results else None
    except:
        return None

# ============ ETF比值 ============
def get_etf_data():
    """获取所有ETF的成交额比值"""
    results = {}
    
    for code, symbol in ETF_DATA.items():
        url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        params = {'_var': 'kline_dayqfq', 'param': f'{symbol},day,,,30,qfq'}
        
        try:
            resp = requests.get(url, params=params, timeout=15)
            data = json.loads(resp.text.split('=')[1])
            
            if symbol in data.get('data', {}):
                stock_data = data['data'][symbol]
                qt = stock_data.get('qt', {}).get(symbol, [])
                klines = stock_data.get('qfqday') or stock_data.get('day', [])
                
                today_amount = float(qt[37]) / 10000 if len(qt) > 37 else 0
                
                if len(klines) >= 5:
                    today_kline = float(klines[-1][2]) * float(klines[-1][5]) / 1e8
                    factor = today_amount / today_kline if today_kline > 0 else 1
                    
                    # 过去4天均值
                    history = []
                    for k in klines[-5:-1]:
                        amt = float(k[2]) * float(k[5]) / 1e8 * factor
                        history.append(amt)
                    
                    avg = sum(history) / len(history) if history else today_amount
                    ratio = today_amount / avg if avg > 0 else 1
                    
                    results[code] = {'today': today_amount, 'ratio': ratio}
        except:
            pass
    
    return results

# ============ 信号判断 ============
def get_signal(north_data, etf_data):
    """综合信号判断"""
    if not north_data or len(north_data) < 2:
        # 无北向数据时只用ETF
        return get_signal_etf_only(etf_data)
    
    # 今日和昨日北向
    today_north = north_data[0]['north']
    yesterday_north = north_data[1]['north'] if len(north_data) > 1 else today_north
    north_change = today_north - yesterday_north
    
    # ETF比值
    ratios = [d['ratio'] for d in etf_data.values()]
    avg_ratio = sum(ratios) / len(ratios) if ratios else 1
    max_ratio = max(ratios) if ratios else 1
    
    # ========== 判断逻辑 ==========
    # 买入信号：ETF放大 + 北向流入 或 北向大幅增加
    buy_conditions = [
        (avg_ratio > 2.5 and today_north > 20),  # ETF强买 + 北向正流入
        (max_ratio > 3 and today_north > 10),    # ETF极端买入
        (avg_ratio > 1.5 and north_change > 15), # ETF温和 + 北向大幅增加
        (today_north > 60),                       # 北向大幅流入（不管ETF）
    ]
    
    # 卖出信号：ETF萎缩 + 北向流出
    sell_conditions = [
        (avg_ratio < 0.4 and today_north < 0),   # ETF强卖 + 北向流出
        (avg_ratio < 0.6 and today_north < -10), # ETF中卖 + 北向大幅流出
        (today_north < -30),                      # 北向大幅流出
    ]
    
    if any(buy_conditions):
        if avg_ratio > 2.5 or today_north > 50:
            return "🔴 强买", "🚀 强烈买入", 3
        elif avg_ratio > 1.8 or today_north > 30:
            return "🟠 中买", "📈 买入", 2
        else:
            return "🟡 弱买", "📈 关注", 1
    
    if any(sell_conditions):
        if avg_ratio < 0.3 or today_north < -30:
            return "⚫ 强卖", "🛑 强烈卖出", -3
        elif avg_ratio < 0.5 or today_north < -15:
            return "🔵 中卖", "📉 减仓", -2
        else:
            return "🟣 弱卖", "📉 谨慎", -1
    
    return "🟢 观望", "🟢 等待", 0

def get_signal_etf_only(etf_data):
    """只用ETF的信号判断"""
    ratios = [d['ratio'] for d in etf_data.values()]
    avg_ratio = sum(ratios) / len(ratios) if ratios else 1
    max_ratio = max(ratios) if ratios else 1
    
    if avg_ratio > 2.5 or max_ratio > 4:
        return "🔴 强买", "🚀 强烈买入", 3
    elif avg_ratio > 2.0 or max_ratio > 3:
        return "🟠 中买", "📈 买入", 2
    elif avg_ratio > 1.5 or max_ratio > 2.5:
        return "🟡 弱买", "📈 关注", 1
    elif avg_ratio < 0.3 or max_ratio < 0.2:
        return "⚫ 强卖", "🛑 强烈卖出", -3
    elif avg_ratio < 0.5:
        return "🔵 中卖", "📉 减仓", -2
    elif avg_ratio < 0.7:
        return "🟣 弱卖", "📉 谨慎", -1
    
    return "🟢 观望", "🟢 等待", 0

def main():
    print("=" * 70)
    print("🏛️ 国家队ETF监测系统（增强版v2）")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 获取数据
    north_data = get_north_money()
    etf_data = get_etf_data()
    
    if north_data:
        print(f"\n📊 北向资金:")
        for n in north_data[:3]:
            print(f"  {n['date']}: {n['north']:.2f}亿")
    
    if etf_data:
        print(f"\n📊 ETF成交额比值:")
        for code, d in etf_data.items():
            r = d['ratio']
            if r > 2.5:
                s = "🔴"
            elif r > 1.5:
                s = "🟡"
            elif r < 0.5:
                s = "🔵"
            elif r < 0.7:
                s = "🟣"
            else:
                s = "🟢"
            print(f"  {s} {code}: {r:.1f}x ({d['today']:.1f}亿)")
    
    # 综合信号
    signal, action, score = get_signal(north_data, etf_data)
    
    print(f"\n📈 综合信号: {signal}")
    print(f"  建议: {action}")
    
    # 结论
    print("\n" + "=" * 70)
    print("🏛️ 结论")
    print("=" * 70)
    
    if score >= 2:
        print(f"\n  🚀 强烈买入信号！")
    elif score == 1:
        print(f"\n  📈 买入信号")
    elif score <= -2:
        print(f"\n  🛑 强烈卖出信号！")
    elif score == -1:
        print(f"\n  📉 卖出信号")
    else:
        print(f"\n  🟢 观望")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
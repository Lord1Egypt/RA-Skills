"""
kline_pattern.py - K线形态检测 + 均线排列分析
用法：python kline_pattern.py <股票代码> [天数]
"""
import requests
import sys


def calc_ma(klines_str, period):
    """计算某周期的均线（简单移动平均）"""
    prices = []
    for k_str in klines_str:
        f = k_str.split(',')
        prices.append(float(f[4]))  # 收盘价
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def detect_patterns(klines_str):
    """检测K线形态"""
    results = []

    for i in range(1, len(klines_str)):
        p_str = klines_str[i-1]
        c_str = klines_str[i]

        p = p_str.split(',')
        c = c_str.split(',')

        d = c[0]
        o = float(c[1])
        close = float(c[2])
        h = float(c[3])
        l = float(c[4])
        v = float(c[5])

        po = float(p[1])
        pc_close = float(p[2])
        ph = float(p[3])
        pl = float(p[4])
        pv = float(p[5])

        is_bull = close > o
        body = abs(close - o)
        upper_shadow = h - max(o, close)
        lower_shadow = min(o, close) - l
        full_range = h - l
        body_ratio = body / full_range if full_range > 0 else 0

        patterns = []

        # 锤子线（底部）
        if is_bull and lower_shadow > body * 2.5 and upper_shadow < body * 0.2:
            patterns.append(('锤子线（底部）', '支撑有效，可能反弹', 'WE'))

        # 吊颈线（顶部）
        if not is_bull and lower_shadow > body * 2.5 and upper_shadow < body * 0.2:
            patterns.append(('吊颈线（顶部）', '上攻乏力，可能回落', 'BE'))

        # 射击之星
        if upper_shadow > body * 2.0 and lower_shadow < body * 0.3 and body_ratio < 0.3:
            if is_bull:
                patterns.append(('射击之星（底部反转）', '可能见底回升', 'WE'))
            else:
                patterns.append(('射击之星（顶部射击）', '可能见顶回落', 'BE'))

        # 吞没形态
        body_prev = abs(pc_close - po)
        if is_bull and pc_close < po and close > po and o < pc_close and body > body_prev * 1.1:
            patterns.append(('阳包阴（看涨吞没）', '底部反转信号', 'WE'))
        if not is_bull and pc_close > po and close < po and o > pc_close and body > body_prev * 1.1:
            patterns.append(('阴包阳（看跌吞没）', '顶部反转信号', 'BE'))

        # 乌云盖顶
        if pc_close > po and o > pc_close and close < (o + pc_close) / 2:
            penetration = (o - close) / full_range if full_range > 0 else 0
            if penetration > 0.4:
                patterns.append(('乌云盖顶', '顶部反转信号', 'BE'))

        # 大阳线放量
        if is_bull and body_ratio > 0.75 and v > pv * 1.5:
            patterns.append(('大阳线（放量）', '多头强势，可能延续', 'WE'))

        # 大阴线放量
        if not is_bull and body_ratio > 0.75 and v > pv * 1.5:
            patterns.append(('大阴线（放量）', '空头强势，可能延续', 'BE'))

        # 三日早晨/黄昏星
        if i >= 2:
            pp_str = klines_str[i-2]
            pp = pp_str.split(',')
            ppo, ppc = float(pp[1]), float(pp[2])
            middle_body = abs(float(c[1]) - float(c[2]))
            if ppc < ppo and middle_body < body * 0.5 and close > o and close > (ppo + ppc) / 2:
                patterns.append(('早晨之星（底部反转）', '三日内底部形态', 'WE'))
            if ppc > ppo and middle_body < body * 0.5 and close < o and close < (ppo + ppc) / 2:
                patterns.append(('黄昏之星（顶部反转）', '三日内顶部形态', 'BE'))

        if patterns:
            for name, meaning, sig in patterns:
                results.append((d, close, name, meaning, sig))

    return results


def judge_arrangement(klines_str):
    """
    判断均线排列：多头/空头/震荡
    """
    ma5 = calc_ma(klines_str, 5)
    ma10 = calc_ma(klines_str, 10)
    ma20 = calc_ma(klines_str, 20)

    if None in (ma5, ma10, ma20):
        try:
            latest = float(klines_str[-1].split(',')[4])
        except:
            latest = 0
        return '数据不足', '无法判断', 0, 0, 0, latest

    # 最新收盘价
    latest = float(klines_str[-1].split(',')[4])

    if ma5 > ma10 > ma20 and latest > ma5:
        arr = '多头排列'
        trend = '上升趋势'
    elif ma5 < ma10 < ma20 and latest < ma5:
        arr = '空头排列'
        trend = '下降趋势'
    else:
        arr = '震荡/混合'
        trend = '趋势不明'

    return arr, trend, round(ma5, 2), round(ma10, 2), round(ma20, 2), round(latest, 2)


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else '000878'
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 15

    market = '1' if code.startswith('6') else '0'
    # 多取一些数据用于计算MA20
    fetch_days = max(days, 25)
    url = (
        f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
        f"?secid={market}.{code}"
        f"&fields1=f1,f2,f3,f4,f5,f6"
        f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
        f"&lmt={fetch_days}&klt=101&fqt=1&end=20260415"
    )
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'}
    r = requests.get(url, timeout=10, headers=headers)
    data = r.json()
    klines = data.get('data', {}).get('klines', [])

    sys.stdout.reconfigure(encoding='utf-8')

    # 均线排列判断
    ma_result = judge_arrangement(klines)
    ma_result = judge_arrangement(klines)
    arr, trend, ma5, ma10, ma20, latest_price = ma_result

    print(f"\n{'='*55}")
    print(f"  股票: {code}  |  近{len(klines)}日数据")
    print(f"{'='*55}")

    if arr:
        print(f"  均线排列: {arr}")
        print(f"  MA5={ma5}  MA10={ma10}  MA20={ma20}  |  收盘={latest_price}")
        print(f"  趋势判断: {trend}")
    print()

    # K线形态
    patterns = detect_patterns(klines)
    print(f"--- K线形态（共检测到{len(patterns)}个信号）---")
    if not patterns:
        print("  未检测到明显形态")
    else:
        bullish = [p for p in patterns if p[4] == 'WE']
        bearish = [p for p in patterns if p[4] == 'BE']
        print(f"  看多信号: {len(bullish)}个  |  看空信号: {len(bearish)}个")
        print()
        for d, close, name, meaning, sig in patterns:
            sig_str = '[WE]' if sig == 'WE' else '[BE]'
            print(f"  {d} {sig_str} {name}")
            print(f"         收盘:{close} | {meaning}")

    print(f"{'='*55}\n")


if __name__ == '__main__':
    main()

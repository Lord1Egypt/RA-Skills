#!/usr/bin/env python3
"""
主力建仓前兆扫描 - 每天盘后自动运行
找出低位横盘缩量、主力悄悄吸筹的候选票

逻辑：
1. 排除ST、高位、成交不活跃
2. 找价格振幅收窄（横盘）
3. 找成交量萎缩后开始温和放量
4. 找近3日内有异动（量增价不涨，可能是吸筹）
5. 位置不能太高（高位横盘是出货不是吸筹）
"""

import urllib.request
import json
import time
from datetime import datetime

# ============ 配置 ============
CONFIG_FILE = "/Users/hushuizhen/.openclaw/workspace/.stock-config.json"
REPORT_FILE = "/Users/hushuizhen/.openclaw/workspace/memory/main-force-scan-{date}.md"
WATCHLIST_FILE = "/Users/hushuizhen/.openclaw/workspace/memory/main-force-watchlist.md"

def get_config(key):
    try:
        import json
        with open(CONFIG_FILE) as f:
            return json.load(f).get(key)
    except:
        return None

def fetch(url, headers=None):
    h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com/'}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def get_main_board_stocks():
    """获取沪深主板全部股票"""
    stocks = []
    # 沪市主板
    url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6&fields=f2,f3,f4,f5,f6,f7,f8,f12,f14,f15,f16,f17,f18'
    try:
        data = fetch(url)
        for item in data['data']['diff']:
            stocks.append(item['f12'])
    except:
        pass
    # 深市主板
    url2 = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:2&fields=f2,f3,f4,f5,f6,f7,f8,f12,f14,f15,f16,f17,f18'
    try:
        data2 = fetch(url2)
        for item in data2['data']['diff']:
            stocks.append(item['f12'])
    except:
        pass
    return stocks

def get_kline_daily(code, days=12):
    """获取近N日日线数据"""
    secid = f'0.{code}' if code.startswith('0') else f'1.{code}'
    url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=bd1d9ddb04089700cf9c27f6f7426281&secid={secid}&klt=101&fqt=1&beg={get_yesterday()}&end=20500101&smplmt={days}'
    try:
        data = fetch(url)
        klines = data['data']['klines']
        result = []
        for k in klines[-days:]:
            parts = k.split(',')
            result.append({
                'date': parts[0],
                'open': float(parts[1]),
                'close': float(parts[2]),
                'high': float(parts[3]),
                'low': float(parts[4]),
                'vol': float(parts[5]),
                'amount': float(parts[6])
            })
        return result
    except:
        return []

def get_yesterday():
    from datetime import date, timedelta
    d = date.today() - timedelta(days=1)
    return d.strftime('%Y%m%d')

def analyze_stock(code, name, price, pct_change, amount):
    """分析单只股票是否符合主力建仓前兆特征"""
    # 过滤条件
    if price <= 0 or price > 100:
        return None
    if amount < 3000:  # 成交额<3000万，不活跃
        return None
    if pct_change > 9.5 or pct_change < -5:  # 涨太猛或跌太狠的不行
        return None
    if 'ST' in name or '*' in name:
        return None
    # 排除60开头但价格>50的高价股（方便排除科创板的类高价股干扰）
    if code.startswith('6') and price > 80:
        return None
    
    klines = get_kline_daily(code, 12)
    if len(klines) < 8:
        return None
    
    # ============ 计算指标 ============
    # 1. 近5日价格振幅（横盘判定）
    recent_5 = klines[-5:]
    price_range_5 = [(k['high'] - k['low']) / k['low'] * 100 for k in recent_5]
    avg_range_5 = sum(price_range_5) / len(price_range_5)
    
    # 前10日平均振幅作为基准
    all_10 = klines[:10]
    price_range_10 = [(k['high'] - k['low']) / k['low'] * 100 for k in all_10]
    avg_range_10 = sum(price_range_10) / len(price_range_10)
    
    # 横盘信号：近5日振幅 < 前10日振幅的70%（波动在收窄）
    if avg_range_5 >= avg_range_10 * 0.7:
        return None
    
    # 2. 成交量萎缩 → 放量
    vols = [k['vol'] for k in klines]
    avg_vol_10 = sum(vols[:10]) / 10
    recent_vol = sum(vols[-3:]) / 3
    
    # 近3日均量显著高于前10日均量，但没有暴涨（温和放量）
    vol_ratio = recent_vol / avg_vol_10 if avg_vol_10 > 0 else 0
    if vol_ratio < 1.3:  # 放量不够明显
        return None
    
    # 3. 价格位置：当前价在近12日的高低点的中间位置（不能太高）
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    max_12 = max(highs)
    min_12 = min(lows)
    mid_price = (max_12 + min_12) / 2
    
    if price < mid_price * 0.95:  # 价格低于中位价5%以上（偏低位）
        return None
    if price > max_12 * 0.97:  # 价格接近12日最高（可能是启动后，追高）
        return None
    
    # 4. 近3日内异动：某日放量但涨幅不大（主力吸筹特征）
    anomaly = False
    for k in klines[-3:]:
        vol_ratio_day = k['vol'] / avg_vol_10
        pct_day = (k['close'] - k['open']) / k['open'] * 100
        if vol_ratio_day > 1.5 and abs(pct_day) < 3:  # 放量但价格波动小
            anomaly = True
            break
    
    # 5. 整体趋势不能是下降通道
    first_close = klines[0]['close']
    last_close = klines[-1]['close']
    trend = (last_close - first_close) / first_close * 100
    if trend < -5:  # 整体趋势向下，不适合
        return None
    
    # 综合评分
    score = 0
    score += min(avg_range_5 / 2, 20)  # 横盘越窄越好
    score += min(vol_ratio * 5, 25)  # 放量越明显越好
    score += 15 if anomaly else 0  # 有异动加分
    score += min(trend + 5, 20)  # 趋势向上加分
    
    return {
        'code': code,
        'name': name,
        'price': price,
        'pct': pct_change,
        'score': round(score, 1),
        'vol_ratio': round(vol_ratio, 2),
        'avg_range_5': round(avg_range_5, 2),
        'anomaly': anomaly,
        'amount': round(amount / 10000, 1),
        'trend': round(trend, 2)
    }

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    report_file = REPORT_FILE.format(date=today)
    
    print(f"开始主力建仓前兆扫描 {today}...")
    
    # 获取全量股票列表（限制数量避免超时）
    print("获取股票列表...")
    try:
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=150&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:1+t:2&fields=f2,f3,f5,f6,f12,f14'
        data = fetch(url)
        stocks_raw = data['data']['diff']
    except Exception as e:
        print(f"获取失败: {e}")
        return
    
    print(f"待扫描: {len(stocks_raw)} 只")
    
    results = []
    for item in stocks_raw[:150]:  # 限制150只，超时则停止
        code = item['f12']
        name = item['f14']
        price = item['f2']
        pct = item['f3']
        amount = item['f6']
        
        if price <= 0 or 'ST' in name:
            continue
        
        result = analyze_stock(code, name, price, pct, amount)
        if result:
            results.append(result)
        
        time.sleep(0.08)  # 避免过快
    
    # 按综合评分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # 输出报告
    with open(report_file, 'w') as f:
        f.write(f"# 主力建仓前兆扫描 {today}\n\n")
        f.write(f"扫描股票数: {len(stocks_raw[:150])}  符合条件: {len(results)}\n\n")
        f.write("## 评分标准: 横盘+温和放量+近3日异动+趋势不差\n\n")
        f.write("| 评分 | 股票名称 | 现价 | 涨幅 | 放量倍数 | 5日振幅 | 异动 | 趋势 | 成交额 |\n")
        f.write("|------|--------|------|------|---------|--------|------|------|--------|\n")
        
        for r in results[:20]:
            flag = "✅" if r['anomaly'] else "⚠️"
            f.write(f"| {r['score']} | {r['name']}({r['code']}) | {r['price']} | {r['pct']:+.2f}% | {r['vol_ratio']}x | {r['avg_range_5']}% | {flag} | {r['trend']:+.1f}% | {r['amount']}亿 |\n")
        
        f.write("\n---\n*仅供参考，不构成投资建议*\n")
    
    print(f"扫描完成，报告已生成: {report_file}")
    print(f"符合条件: {len(results)} 只")
    if results:
        print(f"Top5: {', '.join([r['name'] for r in results[:5]])}")

if __name__ == '__main__':
    main()
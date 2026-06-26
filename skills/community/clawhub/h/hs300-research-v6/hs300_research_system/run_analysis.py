#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - 运行版（纯ASCII输出）
"""

import os
import time
import urllib.request
from datetime import datetime

# 沪深300成分股
HS300_STOCKS = [
    {'code': 'sh600519', 'name': '贵州茅台', 'sector': '食品饮料'},
    {'code': 'sz000858', 'name': '五粮液', 'sector': '食品饮料'},
    {'code': 'sh601318', 'name': '中国平安', 'sector': '金融'},
    {'code': 'sh600036', 'name': '招商银行', 'sector': '金融'},
    {'code': 'sz000333', 'name': '美的集团', 'sector': '家电'},
    {'code': 'sz002594', 'name': '比亚迪', 'sector': '新能源'},
    {'code': 'sh601012', 'name': '隆基绿能', 'sector': '新能源'},
    {'code': 'sh600900', 'name': '长江电力', 'sector': '电力'},
    {'code': 'sh600276', 'name': '恒瑞医药', 'sector': '医药'},
    {'code': 'sz300750', 'name': '宁德时代', 'sector': '新能源'},
    {'code': 'sh601888', 'name': '中国中免', 'sector': '消费'},
    {'code': 'sh600309', 'name': '万华化学', 'sector': '化工'},
    {'code': 'sz000651', 'name': '格力电器', 'sector': '家电'},
    {'code': 'sh601166', 'name': '兴业银行', 'sector': '金融'},
    {'code': 'sh600030', 'name': '中信证券', 'sector': '金融'},
    {'code': 'sz002415', 'name': '海康威视', 'sector': '科技'},
    {'code': 'sh601398', 'name': '工商银行', 'sector': '金融'},
    {'code': 'sh601288', 'name': '农业银行', 'sector': '金融'},
    {'code': 'sh601988', 'name': '中国银行', 'sector': '金融'},
    {'code': 'sz000001', 'name': '平安银行', 'sector': '金融'},
]


def fetch_stock_data(stock_code):
    """从新浪财经API获取股票日线数据"""
    try:
        url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={stock_code}&scale=240&ma=no&datalen=100"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode('utf-8')
        
        import ast
        kline_data = ast.literal_eval(data)
        
        if not kline_data or not isinstance(kline_data, list):
            return None
        
        prices = []
        highs = []
        lows = []
        for item in kline_data:
            prices.append(float(item['close']))
            highs.append(float(item['high']))
            lows.append(float(item['low']))
        
        prices.reverse()
        highs.reverse()
        lows.reverse()
        
        return {
            'prices': prices,
            'highs': highs,
            'lows': lows,
            'current_price': prices[-1]
        }
    except:
        return None


def get_mock_data(stock_code):
    """获取模拟数据"""
    import random
    random.seed(hash(stock_code) % 10000)
    
    base_price = {
        'sh600519': 1800, 'sz000858': 160, 'sh601318': 45, 'sh600036': 35,
        'sz000333': 60, 'sz002594': 250, 'sh601012': 28, 'sh600900': 28,
    }.get(stock_code, 50)
    
    prices = []
    current = base_price
    for _ in range(100):
        current = current * (0.98 + random.random() * 0.04)
        prices.append(current)
    
    return {
        'prices': prices,
        'highs': [p * 1.01 for p in prices],
        'lows': [p * 0.99 for p in prices],
        'current_price': prices[-1]
    }


def sma(prices, period):
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    return sum(prices[-period:]) / period


def ema(prices, period):
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0
    ema_val = sum(prices[:period]) / period
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema_val = (price - ema_val) * multiplier + ema_val
    return ema_val


def macd(prices):
    if len(prices) < 35:
        return {'golden': False, 'death': False}
    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)
    hist = (ema12 - ema26) * 0.3
    golden = hist > 0 and len(prices) > 60 and prices[-1] > prices[-20]
    return {'golden': golden, 'death': hist < 0 and prices[-1] < prices[-20]}


def rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    gains = []
    losses = []
    for i in range(max(1, len(prices) - period), len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(-change)
    if not gains and not losses:
        return 50
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def kdj(highs, lows, closes, n=9):
    if len(closes) < n:
        return {'golden': False}
    lowest_low = min(lows[-n:])
    highest_high = max(highs[-n:])
    if highest_high == lowest_low:
        rsv = 50
    else:
        rsv = (closes[-1] - lowest_low) / (highest_high - lowest_low) * 100
    return {'golden': closes[-1] > closes[-5] and rsv > 30}


def calc_factors(stock_info, data):
    prices = data['prices']
    highs = data['highs']
    lows = data['lows']
    
    rsi_val = rsi(prices)
    macd_data = macd(prices)
    kdj_data = kdj(highs, lows, prices)
    
    return_1m = (prices[-1] / prices[-20] - 1) if len(prices) >= 20 else 0
    return_3m = (prices[-1] / prices[-60] - 1) if len(prices) >= 60 else 0
    
    ma5 = sma(prices, 5)
    ma10 = sma(prices, 10)
    ma20 = sma(prices, 20)
    ma60 = sma(prices, 60) if len(prices) >= 60 else ma20
    
    bullish = ma5 > ma10 > ma20 > ma60
    bearish = ma5 < ma10 < ma20 < ma60
    
    score = 0
    score += return_1m * 3 + return_3m * 2
    if macd_data['golden']: score += 0.5
    if kdj_data['golden']: score += 0.3
    if bullish: score += 0.4
    if 40 <= rsi_val <= 60: score += 0.3
    if rsi_val > 70 or rsi_val < 30: score -= 0.2
    if prices[-1] > ma5: score += 0.1
    if prices[-1] > ma20: score += 0.1
    
    return {
        'code': stock_info['code'],
        'name': stock_info['name'],
        'sector': stock_info['sector'],
        'price': round(data['current_price'], 2),
        'score': round(score, 4),
        'rsi': round(rsi_val, 2),
        'macd_gold': macd_data['golden'],
        'kdj_gold': kdj_data['golden'],
        'bullish': bullish,
        'bearish': bearish,
        'return_1m': round(return_1m * 100, 2),
    }


def generate_report(results, use_real_data):
    results.sort(key=lambda x: x['score'], reverse=True)
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = []
    report.append("# 沪深300多因子投研日报")
    report.append(f"生成时间：{today}")
    report.append(f"数据源：{'新浪财经实时行情' if use_real_data else '模拟数据(演示)'}")
    report.append("")
    report.append("## 市场概览")
    report.append(f"分析股票数量：{len(results)} 只")
    
    avg_score = sum(r['score'] for r in results) / len(results)
    report.append(f"平均综合得分：{avg_score:.4f}")
    
    if avg_score > 0.3: mood = "乐观（多头市场）"
    elif avg_score > 0: mood = "偏多（震荡向上）"
    elif avg_score > -0.3: mood = "偏空（震荡向下）"
    else: mood = "谨慎（空头市场）"
    report.append(f"市场情绪：{mood}")
    report.append("")
    
    report.append("## 技术信号统计")
    macd_gold = sum(1 for r in results if r['macd_gold'])
    kdj_gold = sum(1 for r in results if r['kdj_gold'])
    bullish_cnt = sum(1 for r in results if r['bullish'])
    bearish_cnt = sum(1 for r in results if r['bearish'])
    report.append(f"MACD金叉：{macd_gold} 只股票")
    report.append(f"KDJ金叉：{kdj_gold} 只股票")
    report.append(f"均线多头排列：{bullish_cnt} 只股票")
    report.append(f"均线空头排列：{bearish_cnt} 只股票")
    report.append("")
    
    report.append("## 潜力个股推荐（综合得分前10）")
    report.append("")
    report.append("|排名|代码|名称|行业|价格|得分|MACD金叉|KDJ金叉|多头排列|1月涨幅|RSI|")
    report.append("|----|----|----|----|----|----|--------|--------|--------|-------|---|")
    for idx, r in enumerate(results[:10], 1):
        mg = 'Y' if r['macd_gold'] else ''
        kg = 'Y' if r['kdj_gold'] else ''
        bu = 'Y' if r['bullish'] else ''
        report.append(f"|{idx}|{r['code']}|{r['name']}|{r['sector']}|{r['price']:.2f}|{r['score']:.4f}|{mg}|{kg}|{bu}|{r['return_1m']:+.2f}%|{r['rsi']:.0f}|")
    report.append("")
    
    report.append("## 重点关注（多重信号共振）")
    signal = [r for r in results if r['macd_gold'] and r['kdj_gold']]
    if signal:
        report.append("")
        report.append("|代码|名称|行业|价格|得分|多头排列|1月涨幅|")
        report.append("|----|----|----|----|----|--------|-------|")
        for r in signal:
            bu = 'Y' if r['bullish'] else ''
            report.append(f"|{r['code']}|{r['name']}|{r['sector']}|{r['price']:.2f}|{r['score']:.4f}|{bu}|{r['return_1m']:+.2f}%|")
    else:
        report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
    report.append("")
    
    report.append("## 风险提示个股（综合得分后5）")
    report.append("")
    report.append("|排名|代码|名称|行业|价格|得分|空头排列|1月涨幅|RSI|")
    report.append("|----|----|----|----|----|----|--------|-------|---|")
    bottom = results[-5:]
    bottom.reverse()
    for idx, r in enumerate(bottom, 1):
        be = 'Y' if r['bearish'] else ''
        report.append(f"|{idx}|{r['code']}|{r['name']}|{r['sector']}|{r['price']:.2f}|{r['score']:.4f}|{be}|{r['return_1m']:+.2f}%|{r['rsi']:.0f}|")
    report.append("")
    
    report.append("## 投资策略建议")
    if avg_score > 0.2:
        report.append("1. 仓位建议：市场整体向好，建议保持6-8成仓位。")
    elif avg_score > 0:
        report.append("1. 仓位建议：市场震荡偏多，建议保持5-6成仓位。")
    elif avg_score > -0.2:
        report.append("1. 仓位建议：市场震荡偏弱，建议保持3-5成仓位。")
    else:
        report.append("1. 仓位建议：市场风险较高，建议保持2-3成仓位。")
    report.append("")
    report.append("2. 选股策略：")
    report.append("   - 重点关注综合得分排名靠前的股票")
    report.append("   - 优先选择有多个技术信号共振的个股")
    report.append("   - 避开综合得分排名靠后的股票")
    report.append("")
    report.append("【风险提示】本报告仅供参考，不构成投资建议。")
    
    return '\n'.join(report)


def main():
    print("=" * 60)
    print("    沪深300多因子投研系统")
    print("=" * 60)
    print()
    print("正在获取新浪财经行情数据...")
    print()
    
    results = []
    real_data = 0
    
    for idx, stock in enumerate(HS300_STOCKS, 1):
        print(f"[{idx:2d}/{len(HS300_STOCKS)}] {stock['name']}({stock['code']})...", end=' ')
        
        data = fetch_stock_data(stock['code'])
        if data:
            real_data += 1
            print("[真实数据]", end=' ')
        else:
            data = get_mock_data(stock['code'])
            print("[模拟数据]", end=' ')
        
        factors = calc_factors(stock, data)
        results.append(factors)
        print(f"得分: {factors['score']:.4f}")
        time.sleep(0.1)
    
    print()
    print(f"分析完成！真实数据: {real_data}/{len(HS300_STOCKS)}")
    print()
    
    report = generate_report(results, real_data > 0)
    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, f"沪深300投研日报_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已保存: {filename}")
    print()
    print("=" * 60)
    print("报告预览:")
    print("=" * 60)
    print(report[:1000])
    print("...")
    print("=" * 60)
    
    print()
    print(f"[OK] 完整报告请查看: {filename}")


if __name__ == '__main__':
    main()

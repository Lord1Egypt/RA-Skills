#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - 简化演示版本
不依赖numpy/pandas，使用纯Python实现
"""

import os
import json
from datetime import datetime
import urllib.request
import urllib.parse

# 模拟一些沪深300成分股数据
HS300_STOCKS = [
    {'code': '600519', 'name': '贵州茅台', 'sector': '食品饮料'},
    {'code': '000858', 'name': '五粮液', 'sector': '食品饮料'},
    {'code': '601318', 'name': '中国平安', 'sector': '金融'},
    {'code': '600036', 'name': '招商银行', 'sector': '金融'},
    {'code': '000333', 'name': '美的集团', 'sector': '家电'},
    {'code': '002594', 'name': '比亚迪', 'sector': '新能源'},
    {'code': '601012', 'name': '隆基绿能', 'sector': '新能源'},
    {'code': '600900', 'name': '长江电力', 'sector': '电力'},
    {'code': '600276', 'name': '恒瑞医药', 'sector': '医药'},
    {'code': '300750', 'name': '宁德时代', 'sector': '新能源'},
    {'code': '601888', 'name': '中国中免', 'sector': '消费'},
    {'code': '600309', 'name': '万华化学', 'sector': '化工'},
    {'code': '000651', 'name': '格力电器', 'sector': '家电'},
    {'code': '601166', 'name': '兴业银行', 'sector': '金融'},
    {'code': '600030', 'name': '中信证券', 'sector': '金融'},
    {'code': '002415', 'name': '海康威视', 'sector': '科技'},
    {'code': '601398', 'name': '工商银行', 'sector': '金融'},
    {'code': '600000', 'name': '浦发银行', 'sector': '金融'},
    {'code': '601288', 'name': '农业银行', 'sector': '金融'},
    {'code': '601988', 'name': '中国银行', 'sector': '金融'},
]


def get_stock_price_simple(stock_code):
    """模拟获取股票价格和技术指标"""
    import random
    random.seed(hash(stock_code) % 10000)
    
    base_price = {
        '600519': 1800, '000858': 160, '601318': 45, '600036': 35,
        '000333': 60, '002594': 250, '601012': 28, '600900': 28,
        '600276': 45, '300750': 200, '601888': 85, '600309': 90,
        '000651': 38, '601166': 20, '600030': 22, '002415': 35,
        '601398': 5.5, '600000': 7.5, '601288': 4, '601988': 4.2
    }.get(stock_code, 50)
    
    # 生成一些波动
    price = base_price * (0.95 + random.random() * 0.1)
    
    # 模拟技术指标
    rsi = 30 + random.random() * 40  # 30-70
    macd_hist = (random.random() - 0.5) * 2  # -1 到 1
    volume_ratio = 0.8 + random.random() * 0.8
    
    return {
        'price': round(price, 2),
        'rsi': round(rsi, 2),
        'macd_hist': round(macd_hist, 4),
        'volume_ratio': round(volume_ratio, 2),
        'macd_golden': macd_hist > 0 and random.random() > 0.7,
        'kdj_golden': random.random() > 0.7,
        'bullish_alignment': random.random() > 0.6,
        'bearish_alignment': random.random() > 0.7,
        'return_1m': round((random.random() - 0.5) * 0.2, 4),
        'volatility': round(0.1 + random.random() * 0.2, 4)
    }


def calculate_score(stock_data):
    """计算综合得分"""
    score = 0
    
    # 动量因子（涨幅为正加分）
    score += stock_data['return_1m'] * 5
    
    # 技术因子
    if stock_data['macd_golden']:
        score += 0.5
    if stock_data['kdj_golden']:
        score += 0.3
    if stock_data['bullish_alignment']:
        score += 0.4
    
    # RSI适中为好
    rsi = stock_data['rsi']
    if 40 <= rsi <= 60:
        score += 0.3
    elif rsi > 70 or rsi < 30:
        score -= 0.2
    
    # 波动率（低波动加分）
    score -= stock_data['volatility'] * 2
    
    # 成交量放大加分
    if stock_data['volume_ratio'] > 1.2:
        score += 0.2
    
    return round(score, 4)


def generate_report():
    """生成投研报告"""
    print("正在生成投研报告...")
    
    # 计算所有股票的因子和得分
    results = []
    for stock in HS300_STOCKS:
        price_data = get_stock_price_simple(stock['code'])
        score = calculate_score(price_data)
        
        results.append({
            'code': stock['code'],
            'name': stock['name'],
            'sector': stock['sector'],
            'price': price_data['price'],
            'score': score,
            'rsi': price_data['rsi'],
            'return_1m': price_data['return_1m'],
            'macd_golden': price_data['macd_golden'],
            'kdj_golden': price_data['kdj_golden'],
            'bullish_alignment': price_data['bullish_alignment'],
            'bearish_alignment': price_data['bearish_alignment']
        })
    
    # 按得分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # 生成Markdown报告
    today = datetime.now().strftime('%Y年%m月%d日')
    report_time = datetime.now().strftime('%H:%M:%S')
    
    report = []
    report.append(f"# 沪深300多因子投研日报")
    report.append(f"**生成时间：{today} {report_time}**")
    report.append("")
    report.append("---")
    
    # 市场概览
    report.append("## 📊 市场概览")
    report.append("")
    report.append(f"- **分析股票数量**：{len(results)} 只")
    
    avg_score = sum(r['score'] for r in results) / len(results)
    report.append(f"- **平均综合得分**：{avg_score:.4f}")
    
    # 市场情绪判断
    if avg_score > 0.3:
        mood = "🟢 乐观（多头市场）"
    elif avg_score > 0:
        mood = "🟡 偏多（震荡向上）"
    elif avg_score > -0.3:
        mood = "🟠 偏空（震荡向下）"
    else:
        mood = "🔴 谨慎（空头市场）"
    report.append(f"- **市场情绪**：{mood}")
    report.append("")
    report.append("---")
    
    # 技术信号统计
    report.append("## 📈 技术信号统计")
    report.append("")
    
    macd_gold_count = sum(1 for r in results if r['macd_golden'])
    kdj_gold_count = sum(1 for r in results if r['kdj_golden'])
    bullish_count = sum(1 for r in results if r['bullish_alignment'])
    bearish_count = sum(1 for r in results if r['bearish_alignment'])
    
    report.append(f"- **MACD金叉**：{macd_gold_count} 只股票")
    report.append(f"- **KDJ金叉**：{kdj_gold_count} 只股票")
    report.append(f"- **均线多头排列**：{bullish_count} 只股票")
    report.append(f"- **均线空头排列**：{bearish_count} 只股票")
    report.append("")
    report.append("---")
    
    # 潜力个股推荐
    report.append("## 🌟 潜力个股推荐（综合得分前10）")
    report.append("")
    report.append("| 排名 | 股票代码 | 股票名称 | 所属行业 | 最新价格 | 综合得分 | MACD金叉 | KDJ金叉 | 多头排列 | 1月涨幅 | RSI |")
    report.append("|------|----------|----------|----------|----------|----------|----------|---------|----------|---------|-----|")
    
    for idx, r in enumerate(results[:10], 1):
        macd_gold = '✓' if r['macd_golden'] else ''
        kdj_gold = '✓' if r['kdj_golden'] else ''
        bullish = '✓' if r['bullish_alignment'] else ''
        
        report.append(
            f"| {idx} | {r['code']} | {r['name']} | {r['sector']} | {r['price']:.2f} | {r['score']:.4f} | "
            f"{macd_gold} | {kdj_gold} | {bullish} | {r['return_1m']*100:+.2f}% | {r['rsi']:.1f} |"
        )
    
    report.append("")
    report.append("---")
    
    # 重点关注个股
    report.append("## 🎯 重点关注（多重信号共振）")
    report.append("")
    report.append("以下股票同时出现MACD金叉和KDJ金叉信号，值得重点关注：")
    report.append("")
    
    signal_stocks = [r for r in results if r['macd_golden'] and r['kdj_golden']]
    
    if signal_stocks:
        report.append("| 股票代码 | 股票名称 | 所属行业 | 最新价格 | 综合得分 | 多头排列 | 1月涨幅 |")
        report.append("|----------|----------|----------|----------|----------|----------|---------|")
        
        for r in signal_stocks:
            bullish = '✓' if r['bullish_alignment'] else ''
            report.append(
                f"| {r['code']} | {r['name']} | {r['sector']} | {r['price']:.2f} | "
                f"{r['score']:.4f} | {bullish} | {r['return_1m']*100:+.2f}% |"
            )
    else:
        report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
    
    report.append("")
    report.append("---")
    
    # 风险提示个股
    report.append("## ⚠️ 风险提示个股（综合得分后5）")
    report.append("")
    report.append("以下股票综合得分较低，建议暂时规避：")
    report.append("")
    
    report.append("| 排名 | 股票代码 | 股票名称 | 所属行业 | 最新价格 | 综合得分 | 空头排列 | 1月涨幅 | RSI |")
    report.append("|------|----------|----------|----------|----------|----------|----------|---------|-----|")
    
    bottom_stocks = results[-5:]
    bottom_stocks.reverse()
    
    for idx, r in enumerate(bottom_stocks, 1):
        bearish = '✓' if r['bearish_alignment'] else ''
        report.append(
            f"| {idx} | {r['code']} | {r['name']} | {r['sector']} | {r['price']:.2f} | "
            f"{r['score']:.4f} | {bearish} | {r['return_1m']*100:+.2f}% | {r['rsi']:.1f} |"
        )
    
    report.append("")
    report.append("---")
    
    # 投资策略建议
    report.append("## 💡 投资策略建议")
    report.append("")
    report.append("基于今日多因子模型分析，给出以下投资建议：")
    report.append("")
    
    if avg_score > 0.2:
        report.append("1. **仓位建议**：市场整体向好，建议保持6-8成仓位。")
    elif avg_score > 0:
        report.append("1. **仓位建议**：市场震荡偏多，建议保持5-6成仓位。")
    elif avg_score > -0.2:
        report.append("1. **仓位建议**：市场震荡偏弱，建议保持3-5成仓位。")
    else:
        report.append("1. **仓位建议**：市场风险较高，建议保持2-3成仓位。")
    
    report.append("")
    report.append("2. **选股策略**：")
    report.append("   - 重点关注综合得分排名靠前的股票")
    report.append("   - 优先选择有多个技术信号共振的个股")
    report.append("   - 避开综合得分排名靠后的股票")
    report.append("")
    report.append("3. **操作建议**：")
    report.append("   - 对于金叉股票，可考虑分批建仓")
    report.append("   - 设置合理止损位，控制单笔风险")
    report.append("   - 结合基本面分析进行二次筛选")
    report.append("")
    report.append("---")
    
    # 风险提示
    report.append("## 📢 风险提示")
    report.append("")
    report.append("**【风险提示】**")
    report.append("本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    report.append("基于历史数据的分析不代表未来表现，请结合自身风险承受能力做出投资决策。")
    report.append("")
    report.append("---")
    report.append("*本报告由沪深300多因子投研系统（演示版）自动生成，数据为模拟数据，仅供演示使用。*")
    
    # 保存报告
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f"沪深300投研日报_演示版_{datetime.now().strftime('%Y%m%d')}.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"\n报告生成成功！")
    print(f"报告文件: {filename}")
    print()
    print("报告预览:")
    print("=" * 60)
    print('\n'.join(report[:50]))  # 显示前50行
    print("=" * 60)
    
    return filename


if __name__ == '__main__':
    print("=" * 60)
    print("    沪深300多因子投研系统 - 演示版")
    print("=" * 60)
    print()
    print("注意：这是一个简化演示版本，使用模拟数据。")
    print("完整版本需要AKShare获取真实行情数据。")
    print()
    
    generate_report()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【升级v2.0】沪深300多因子投研系统 - 运行版

新增功能:
✓ 数据质量校验
✓ 黑名单过滤机制
✓ 市场环境判断
✓ 改进的5大类因子体系
✓ 动态权重（牛市/熊市/震荡市）
✓ 信号共振检测
✓ 改进的报告生成
"""

import os
import sys
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime

# 导入升级模块
from factor_calculator_v2 import FactorCalculatorV2
from risk_management import RiskManager
from market_regime import MarketRegimeDetector
from data_quality import DataQualityChecker

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', f'run_v2_{datetime.now().strftime("%Y%m%d")}.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===== 沪深300成分股精简版（用于演示）=====
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


def generate_market_index_data(days=100, base=3000):
    """生成模拟市场指数数据（用于市场环境判断）"""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    prices = base + np.cumsum(np.random.randn(days) * 20)
    
    return pd.DataFrame({
        'date': dates,
        'close': prices,
        'volume': 1000000000 + np.random.randint(-500000000, 500000000, days)
    })


def get_stock_data_simple(stock_code, days=100):
    """获取股票数据（模拟数据，用于演示）"""
    np.random.seed(hash(stock_code) % 10000)
    
    base_prices = {
        'sh600519': 1800, 'sz000858': 160, 'sh601318': 45, 'sh600036': 35,
        'sz000333': 60, 'sz002594': 250, 'sh601012': 28, 'sh600900': 28,
        'sh600276': 42, 'sz300750': 200, 'sh601888': 95, 'sh600309': 90,
    }
    base = base_prices.get(stock_code, 50)
    
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    price_changes = 0.98 + np.random.rand(days) * 0.04
    
    prices = []
    current = base
    for change in price_changes:
        current *= change
        prices.append(current)
    
    df = pd.DataFrame({
        'date': dates,
        'close': prices,
        'high': [p * (1 + np.random.rand() * 0.02) for p in prices],
        'low': [p * (1 - np.random.rand() * 0.02) for p in prices],
        'volume': [10000000 + np.random.randint(-5000000, 5000000) for _ in prices],
        'pct_chg': np.diff([base] + prices) / np.array([base] + prices)[:-1] * 100
    })
    
    return df


def main():
    print()
    print("=" * 70)
    print("   沪深300多因子投研系统 v2.0")
    print("=" * 70)
    print("✓ 数据质量校验   ✓ 黑名单过滤   ✓ 市场环境判断")
    print("✓ 5大类因子      ✓ 动态权重     ✓ 信号共振检测")
    print("=" * 70)
    print()
    
    # ===== 步骤1: 初始化模块 =====
    print("[1/6] 初始化系统模块...")
    factor_calc = FactorCalculatorV2()
    risk_mgr = RiskManager()
    regime_detector = MarketRegimeDetector()
    quality_checker = DataQualityChecker()
    print("      ✓ 所有模块初始化完成")
    print()
    
    # ===== 步骤2: 获取股票数据 =====
    print("[2/6] 获取股票数据...")
    stocks_data = {}
    
    for idx, stock in enumerate(HS300_STOCKS, 1):
        print(f"      [{idx:2d}/{len(HS300_STOCKS)}] {stock['name']}({stock['code']})...", end=' ')
        
        df = get_stock_data_simple(stock['code'])
        if df is not None and len(df) >= 60:
            stocks_data[stock['code']] = {
                'code': stock['code'],
                'name': stock['name'],
                'sector': stock['sector'],
                'daily': df
            }
            print(f"✓ ({len(df)}条数据)")
        else:
            print("✗ 数据不足")
        time.sleep(0.01)
    
    print(f"      ✓ 成功获取 {len(stocks_data)}/{len(HS300_STOCKS)} 只股票数据")
    print()
    
    # ===== 步骤3: 数据质量检查 =====
    print("[3/6] 数据质量检查...")
    quality_report = quality_checker.batch_check_all(stocks_data)
    print(f"      ✓ 平均质量得分: {quality_report['average_score']:.1f}/100")
    print(f"      ✓ 优质数据: {quality_report['quality_distribution'].get('GOOD', 0)} 只")
    print(f"      ✓ 合格数据: {quality_report['quality_distribution'].get('ACCEPTABLE', 0)} 只")
    print(f"      ✓ 不合格: {quality_report['quality_distribution'].get('CRITICAL', 0)} 只")
    print()
    
    # ===== 步骤4: 黑名单过滤 =====
    print("[4/6] 风险过滤（黑名单）...")
    filtered_data, filter_report = risk_mgr.batch_filter_stocks(stocks_data)
    print(f"      ✓ 原始: {filter_report['total']} 只")
    print(f"      ✓ 通过: {filter_report['passed']} 只")
    print(f"      ✓ 过滤: {filter_report['filtered']} 只")
    print(f"      ✓ 原因: {filter_report['reasons']}")
    print()
    
    # ===== 步骤5: 计算因子 =====
    print("[5/6] 因子计算与评分...")
    all_factors = []
    
    for code, stock_info in filtered_data.items():
        factors = factor_calc.calculate_all_factors(stock_info)
        if factors:
            factors['sector'] = stock_info['sector']
            all_factors.append(factors)
    
    factors_df = pd.DataFrame(all_factors)
    print(f"      ✓ 完成 {len(all_factors)} 只股票因子计算")
    print()
    
    # ===== 步骤6: 市场环境判断 =====
    print("[6/6] 市场环境判断与综合评分...")
    index_data = generate_market_index_data()
    regime_analysis = regime_detector.comprehensive_analysis(index_data)
    market_regime = regime_analysis['trend']['trend']
    
    print(f"      ✓ 市场状态: {regime_analysis['market_summary']}")
    print(f"      ✓ 趋势得分: {regime_analysis['trend']['trend_score']}")
    print(f"      ✓ 建议仓位: {regime_analysis['position_suggestion']['suggested_total_position']:.0%}")
    print()
    
    # 根据市场环境计算因子得分
    factors_df = factor_calc.calculate_factor_score(factors_df, market_regime=market_regime)
    
    # 添加风险评分
    factors_df = risk_mgr.calculate_risk_score(factors_df)
    
    # ===== 生成报告 =====
    print("=" * 70)
    print("   生成报告...")
    print("=" * 70)
    print()
    
    report = generate_report_v2(factors_df, regime_analysis, quality_report, filter_report)
    
    # 保存报告
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f"沪深300投研日报_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ 报告已保存: {filename}")
    print()
    print("=" * 70)
    print("   报告预览")
    print("=" * 70)
    print(report[:1500])
    print("...")
    print("=" * 70)
    print()
    print(f"[完成] 完整报告请查看: {filename}")
    print()


def generate_report_v2(factors_df, regime_analysis, quality_report, filter_report):
    """【升级v2.0】生成增强版投研日报"""
    
    today = datetime.now().strftime('%Y年%m月%d日')
    df = factors_df.sort_values('composite_score', ascending=False)
    
    report = []
    
    # 标题
    report.append("# 沪深300多因子投研日报 v2.0")
    report.append(f"**生成时间：{today}**")
    report.append(f"**系统版本：v2.0 升级版**")
    report.append("")
    report.append("---")
    
    # 市场环境分析
    report.append("## 📊 市场环境分析")
    report.append("")
    report.append("| 指标 | 数值 |")
    report.append("|------|------|")
    report.append(f"| **市场状态** | {regime_analysis['market_summary']} |")
    report.append(f"| **趋势得分** | {regime_analysis['trend']['trend_score']} |")
    report.append(f"| **年化波动率** | {regime_analysis['volatility'].get('annualized_volatility', 0)*100:.1f}% |")
    report.append(f"| **建议总仓位** | {regime_analysis['position_suggestion']['suggested_total_position']:.0%} |")
    report.append(f"| **单股上限** | {regime_analysis['position_suggestion']['single_stock_max']:.0%} |")
    report.append("")
    
    # 市场温度
    if 'market_temperature' in regime_analysis:
        temp = regime_analysis['market_temperature']
        report.append(f"🌡️ 市场温度: **{temp['temperature']:.1f}°** - {temp['interpretation']}")
    report.append("")
    report.append("---")
    
    # 数据质量摘要
    report.append("## 🧪 数据质量报告")
    report.append("")
    report.append(f"- **分析股票总数**: {quality_report['total_stocks']} 只")
    report.append(f"- **平均质量得分**: {quality_report['average_score']:.1f}/100")
    report.append(f"- **黑名单过滤**: {filter_report['filtered']} 只股票")
    report.append("")
    report.append("---")
    
    # 技术信号统计
    report.append("## 📈 技术信号统计")
    report.append("")
    
    macd_gold = df['macd_golden'].sum() if 'macd_golden' in df.columns else 0
    kdj_gold = df['kdj_golden'].sum() if 'kdj_golden' in df.columns else 0
    bullish = df['bullish_alignment'].sum() if 'bullish_alignment' in df.columns else 0
    bearish = df['bearish_alignment'].sum() if 'bearish_alignment' in df.columns else 0
    
    double_golden = ((df['macd_golden'].fillna(False) if 'macd_golden' in df.columns else False) & 
                    (df['kdj_golden'].fillna(False) if 'kdj_golden' in df.columns else False)).sum()
    
    report.append(f"- **MACD金叉**: {macd_gold} 只股票")
    report.append(f"- **KDJ金叉**: {kdj_gold} 只股票")
    report.append(f"- **双重金叉共振**: {double_golden} 只股票 ⭐")
    report.append(f"- **均线多头排列**: {bullish} 只股票")
    report.append(f"- **均线空头排列**: {bearish} 只股票")
    report.append("")
    report.append("---")
    
    # 潜力个股推荐
    report.append("## ⭐ 潜力个股推荐（综合得分前10）")
    report.append("")
    report.append("|排名|代码|名称|行业|最新价|综合得分|风险等级|MACD金叉|KDJ金叉|多头排列|1月涨幅|")
    report.append("|----|----|----|----|------|--------|--------|--------|--------|-------|")
    
    for idx, (_, row) in enumerate(df.head(10).iterrows(), 1):
        mg = '✓' if row.get('macd_golden', False) else ''
        kg = '✓' if row.get('kdj_golden', False) else ''
        bu = '✓' if row.get('bullish_alignment', False) else ''
        ret1m = row.get('return_1m', np.nan)
        ret1m_str = f"{ret1m*100:+.1f}%" if not pd.isna(ret1m) else '-'
        
        report.append(
            f"|{idx}|{row['code']}|{row['name']}|{row.get('sector','-')}|"
            f"{row.get('close_price', 0):.2f}|{row.get('composite_score', 0):.4f}|"
            f"{row.get('risk_level','-')}|{mg}|{kg}|{bu}|{ret1m_str}|"
        )
    report.append("")
    report.append("---")
    
    # 重点关注 - 多重信号共振
    report.append("## 🎯 重点关注（多重信号共振）")
    report.append("")
    
    signal_stocks = df[
        (df.get('macd_golden', False) == True) & 
        (df.get('kdj_golden', False) == True)
    ]
    
    if len(signal_stocks) > 0:
        report.append("以下股票同时出现MACD金叉和KDJ金叉信号：")
        report.append("")
        report.append("|代码|名称|行业|综合得分|风险等级|多头排列|")
        report.append("|----|----|----|--------|--------|--------|")
        
        for _, row in signal_stocks.iterrows():
            bu = '✓' if row.get('bullish_alignment', False) else ''
            report.append(
                f"|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('composite_score', 0):.4f}|{row.get('risk_level','-')}|{bu}|"
            )
    else:
        report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
    report.append("")
    report.append("---")
    
    # 因子分析
    report.append("## 🔬 因子表现分析")
    report.append("")
    report.append("### 各因子组得分分布")
    report.append("")
    
    avg_score = df['composite_score'].mean()
    report.append(f"- **平均综合得分**: {avg_score:.4f}")
    report.append("")
    
    # 各因子组平均得分
    for group in ['momentum', 'trend', 'volatility', 'technical', 'volume']:
        col = f'{group}_score'
        if col in df.columns:
            avg = df[col].mean()
            status = "偏强" if avg > 0 else "偏弱" if avg < -0.3 else "中性"
            report.append(f"- **{group}** {status}: 平均分 {avg:.3f}")
    
    report.append("")
    report.append("---")
    
    # 风险提示个股
    report.append("## ⚠️ 风险提示个股（高风险）")
    report.append("")
    
    risk_stocks = df[df['risk_level'] == '高风险'].head(5)
    if len(risk_stocks) > 0:
        report.append("|排名|代码|名称|行业|最新价|综合得分|风险等级|空头排列|")
        report.append("|----|----|----|----|------|--------|--------|--------|")
        
        for idx, (_, row) in enumerate(risk_stocks.iterrows(), 1):
            be = '✓' if row.get('bearish_alignment', False) else ''
            report.append(
                f"|{idx}|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('close_price', 0):.2f}|{row.get('composite_score', 0):.4f}|"
                f"{row.get('risk_level','-')}|{be}|"
            )
    else:
        report.append("当前无高风险股票。")
    report.append("")
    report.append("---")
    
    # 投资策略建议
    report.append("## 💡 投资策略建议")
    report.append("")
    
    pos_sugg = regime_analysis['position_suggestion']
    total_pos = pos_sugg['suggested_total_position']
    
    report.append(f"### 1. 仓位建议")
    report.append(f"- **建议总仓位**: {total_pos:.0%}")
    report.append(f"- **单股上限**: {pos_sugg['single_stock_max']:.1%}")
    report.append("")
    
    report.append("### 2. 选股策略")
    report.append("   - 重点关注综合得分排名靠前的股票")
    report.append("   - 优先选择多重技术信号共振的个股")
    report.append("   - 避开高风险等级的股票")
    report.append("   - 结合行业景气度进行二次筛选")
    report.append("")
    
    report.append("### 3. 操作建议")
    report.append("   - 对于金叉信号股票，可考虑分批建仓")
    report.append("   - 设置合理止损位（5%-8%）")
    report.append("   - 分散持仓，单股不超过仓位上限")
    report.append("")
    report.append("---")
    
    report.append("## 📢 风险提示")
    report.append("")
    report.append("**本报告仅供参考，不构成投资建议。**")
    report.append("- 股市有风险，投资需谨慎")
    report.append("- 基于历史数据的分析不代表未来表现")
    report.append("- 请结合自身风险承受能力做出投资决策")
    report.append("")
    report.append("---")
    
    report.append("*报告由沪深300多因子投研系统 v2.0 自动生成*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"运行出错: {e}")
        print(f"\n错误: {e}")
        sys.exit(1)

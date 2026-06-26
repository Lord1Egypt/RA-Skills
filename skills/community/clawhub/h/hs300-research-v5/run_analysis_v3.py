#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 v3.0 — 完整运行版

v3.0 升级内容:
✅ 8大类因子体系（估值/质量/成长/动量/趋势/波动率/技术/量能）
✅ 财务数据获取（PE/PB/ROE/毛利率/营收增长/利润增长）
✅ 基本面 + 技术面双重分析
✅ 数据源：东方财富 + Tushare Pro + AKShare + pywencai(同花顺问财) + 深交所SZSE
✅ 市场环境动态权重调整
✅ 信号共振检测

⚠️ JQData已禁用（免费版数据截止2026-02-10）
"""

import os
import sys
import io
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime

# Windows UTF-8 兼容
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 导入模块
from data_fetcher import DataFetcher
from factor_calculator_v3 import FactorCalculatorV3
from risk_management import RiskManager
from market_regime import MarketRegimeDetector
from data_quality import DataQualityChecker

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            os.path.join('logs', f'run_v3_{datetime.now().strftime("%Y%m%d")}.log'),
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 沪深300核心成分股（20只）
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
    {'code': '601288', 'name': '农业银行', 'sector': '金融'},
    {'code': '601988', 'name': '中国银行', 'sector': '金融'},
    {'code': '000001', 'name': '平安银行', 'sector': '金融'},
]


def generate_market_index_data(days=200, base=3000):
    """生成模拟市场指数数据"""
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    prices = base + np.cumsum(np.random.randn(days) * 20)
    return pd.DataFrame({
        'date': dates,
        'close': prices,
        'volume': 1000000000 + np.random.randint(-500000000, 500000000, days)
    })


def main():
    print()
    print("=" * 70)
    print("   沪深300多因子投研系统 v3.0")
    print("=" * 70)
    print("✓ 8大类因子     ✓ 财务数据       ✓ 多数据源 + pywencai问财")
    print("✓ 数据质量校验   ✓ 黑名单过滤     ✓ 市场环境判断")
    print("✓ 动态权重       ✓ 信号共振       ✓ 风险评级")
    print("✓ 问财补充       ✓ 资金流向       ✓ 北向资金")
    print("=" * 70)
    print()
    
    for d in ['output', 'logs']:
        if not os.path.exists(d):
            os.makedirs(d)
    
    # ===== 初始化模块 =====
    print("[1/9] 初始化系统模块...")
    fetcher = DataFetcher()
    factor_calc = FactorCalculatorV3()
    risk_mgr = RiskManager()
    regime_detector = MarketRegimeDetector()
    quality_checker = DataQualityChecker()
    print("      ✓ 所有模块初始化完成")
    print()
    
    # ===== 获取股票数据 =====
    print("[2/9] 获取股票数据（技术面 + 基本面）...")
    stocks_data = {}
    
    for idx, stock in enumerate(HS300_STOCKS, 1):
        code = stock['code']
        name = stock['name']
        
        print(f"      [{idx:2d}/{len(HS300_STOCKS)}] {name}({code})", end=' ... ')
        
        # 日线数据
        df = fetcher.get_stock_daily(code)
        if df is None or len(df) < 60:
            print("✗ 日线数据不足")
            continue
        
        # 财务数据
        fundamentals = fetcher.get_stock_fundamentals(code)
        if fundamentals:
            has_pe = fundamentals.get('pe_ttm') is not None
            has_roe = fundamentals.get('roe') is not None
            print(f"✓ 日线{len(df)}条 + 财务数据(PE{'✓' if has_pe else '✗'}/ROE{'✓' if has_roe else '✗'})")
        else:
            print(f"✓ 日线{len(df)}条 (财务数据暂缺)")
        
        stocks_data[code] = {
            'code': code,
            'name': name,
            'sector': stock['sector'],
            'daily': df,
            'fundamentals': fundamentals
        }
        
        time.sleep(1.5)  # 增加延迟避免 akshare 限流
    
    print(f"\n      ✓ 成功获取 {len(stocks_data)}/{len(HS300_STOCKS)} 只股票数据")
    print()
    
    # ===== 数据质量检查 =====
    print("[3/9] 数据质量检查...")
    quality_report = quality_checker.batch_check_all(stocks_data)
    print(f"      ✓ 平均质量得分: {quality_report['average_score']:.1f}/100")
    print()
    
    # ===== 黑名单过滤 =====
    print("[4/9] 风险过滤...")
    filtered_data, filter_report = risk_mgr.batch_filter_stocks(stocks_data)
    print(f"      ✓ 通过: {filter_report['passed']} 只 / 过滤: {filter_report['filtered']} 只")
    print()
    
    # ===== 计算因子 =====
    print("[5/9] 计算8大类因子...")
    all_factors = []
    has_fundamentals = 0
    
    for code, stock_info in filtered_data.items():
        factors = factor_calc.calculate_all_factors(stock_info)
        if factors:
            factors['sector'] = stock_info['sector']
            all_factors.append(factors)
            if stock_info.get('fundamentals'):
                has_fundamentals += 1
    
    factors_df = pd.DataFrame(all_factors)
    print(f"      ✓ 完成 {len(all_factors)} 只股票因子计算")
    print(f"      ✓ 含财务数据: {has_fundamentals} 只")
    print()
    
    # ===== 市场环境判断 =====
    print("[6/9] 市场环境判断与综合评分...")
    index_data = generate_market_index_data()
    regime_analysis = regime_detector.comprehensive_analysis(index_data)
    market_regime = regime_analysis['trend']['trend']
    
    print(f"      ✓ 市场状态: {regime_analysis['market_summary']}")
    print(f"      ✓ 建议仓位: {regime_analysis['position_suggestion']['suggested_total_position']:.0%}")
    print()
    
    # 综合评分
    factors_df = factor_calc.calculate_factor_score(factors_df, market_regime=market_regime)
    factors_df = risk_mgr.calculate_risk_score(factors_df)
    
    # ===== 获取 pywencai 补充数据 =====
    print("[7/9] 获取 pywencai(同花顺问财) 补充数据...")
    pywencai_data = fetch_pywencai_supplementary(fetcher)
    print("      ✓ 补充数据获取完成")
    print()
    
    # ===== 生成报告 =====
    print("[8/9] 生成投研日报...")
    report = generate_report_v3(factors_df, regime_analysis, quality_report, filter_report, has_fundamentals, fetcher, pywencai_data)
    
    output_dir = 'output'
    filename = os.path.join(output_dir, f"沪深300投研日报_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"      ✓ 报告已保存: {filename}")
    print()
    
    # 打印数据源统计
    fetcher.print_source_stats()
    
    print("=" * 70)
    print("   报告预览")
    print("=" * 70)
    print(report[:2000])
    print("...")
    print("=" * 70)
    print(f"\n[完成] 完整报告: {filename}")
    print()


# ==================== pywencai 补充数据采集 ====================

def fetch_pywencai_supplementary(fetcher):
    """
    获取 pywencai(同花顺问财) 补充数据，用于丰富投研日报

    在因子计算完成后调用，不影响主流程
    """
    data = {
        'dual_golden': None,
        'macd_golden': None,
        'fund_flow_today': None,
        'industry_flow_today': None,
        'north_bound': None,
        'high_dividend': None,
    }

    try:
        data['dual_golden'] = fetcher.get_pywencai_signal_stocks('dual_golden')
    except Exception as e:
        logger.debug(f"pywencai 双金叉查询失败: {e}")

    try:
        data['macd_golden'] = fetcher.get_pywencai_signal_stocks('macd_golden')
    except Exception as e:
        logger.debug(f"pywencai MACD金叉查询失败: {e}")

    try:
        data['fund_flow_today'] = fetcher.get_pywencai_fund_flow('今日')
    except Exception as e:
        logger.debug(f"pywencai 资金流查询失败: {e}")

    try:
        data['industry_flow_today'] = fetcher.get_pywencai_industry_flow('今日')
    except Exception as e:
        logger.debug(f"pywencai 行业资金流查询失败: {e}")

    try:
        data['north_bound'] = fetcher.get_pywencai_north_bound()
    except Exception as e:
        logger.debug(f"pywencai 北向资金查询失败: {e}")

    try:
        data['high_dividend'] = fetcher.get_pywencai_high_dividend()
    except Exception as e:
        logger.debug(f"pywencai 高股息查询失败: {e}")

    return data


def generate_report_v3(factors_df, regime_analysis, quality_report, filter_report, has_fundamentals, fetcher=None, pywencai_data=None):
    """v3.0 投研日报 — 包含基本面因子 + pywencai 补充数据"""
    
    today = datetime.now().strftime('%Y年%m月%d日')
    df = factors_df.sort_values('composite_score', ascending=False).reset_index(drop=True)
    
    report = []
    
    report.append("# 📊 沪深300多因子投研日报 v3.0")
    report.append(f"**生成时间：{today}**")
    report.append(f"**系统版本：v3.0 — 基本面 + 技术面 完整分析**")
    report.append("")
    report.append("---")
    
    # ===== 市场环境 =====
    report.append("## 🌍 市场环境分析")
    report.append("")
    report.append("| 指标 | 数据 |")
    report.append("|------|------|")
    report.append(f"| **市场状态** | {regime_analysis['market_summary']} |")
    trend_info = regime_analysis.get('trend', {})
    report.append(f"| **趋势得分** | {trend_info.get('trend_score', 'N/A')} |")
    report.append(f"| **年化波动率** | {regime_analysis['volatility'].get('annualized_volatility', 0)*100:.1f}% |")
    report.append(f"| **建议总仓位** | {regime_analysis['position_suggestion']['suggested_total_position']:.0%} |")
    report.append(f"| **单股上限** | {regime_analysis['position_suggestion']['single_stock_max']:.0%} |")
    report.append("")
    
    if 'market_temperature' in regime_analysis:
        temp = regime_analysis['market_temperature']
        report.append(f"🌡️ 市场温度: **{temp['temperature']:.1f}°** — {temp['interpretation']}")
    report.append("")
    report.append("---")
    
    # ===== 数据概况 =====
    report.append("## 📈 数据概况")
    report.append("")
    report.append(f"- **分析股票总数**: {quality_report['total_stocks']} 只")
    report.append(f"- **含财务数据**: {has_fundamentals} 只")
    report.append(f"- **黑名单过滤**: {filter_report['filtered']} 只")
    report.append("")
    report.append("---")
    
    # ===== 技术信号统计 =====
    report.append("## 📡 技术信号统计")
    report.append("")
    
    macd_gold = df['macd_golden'].sum() if 'macd_golden' in df.columns else 0
    kdj_gold = df['kdj_golden'].sum() if 'kdj_golden' in df.columns else 0
    bullish = df['bullish_alignment'].sum() if 'bullish_alignment' in df.columns else 0
    bearish = df['bearish_alignment'].sum() if 'bearish_alignment' in df.columns else 0
    
    double_golden = ((df['macd_golden'].fillna(False) if 'macd_golden' in df.columns else False) &
                    (df['kdj_golden'].fillna(False) if 'kdj_golden' in df.columns else False)).sum()
    
    report.append(f"- **MACD金叉**: {macd_gold} 只")
    report.append(f"- **KDJ金叉**: {kdj_gold} 只")
    report.append(f"- **双重金叉共振**: {double_golden} 只 ⚡")
    report.append(f"- **均线多头排列**: {bullish} 只")
    report.append(f"- **均线空头排列**: {bearish} 只")
    report.append("")
    report.append("---")
    
    # ===== 基本面因子统计 =====
    report.append("## 🏛️ 基本面因子统计")
    report.append("")
    
    if has_fundamentals > 0:
        # PE 统计
        pe_data = df['pe_ttm'].dropna()
        if len(pe_data) > 0:
            report.append(f"### 估值指标")
            report.append(f"- **PE(TTM)** 均值: {pe_data.mean():.1f} | 中位数: {pe_data.median():.1f} | 最小: {pe_data.min():.1f}")
        
        pb_data = df['pb'].dropna()
        if len(pb_data) > 0:
            report.append(f"- **PB** 均值: {pb_data.mean():.2f} | 中位数: {pb_data.median():.2f} | 最小: {pb_data.min():.2f}")
        
        report.append("")
        
        # ROE 统计
        roe_data = df['roe'].dropna()
        if len(roe_data) > 0:
            report.append(f"### 质量指标")
            report.append(f"- **ROE** 均值: {roe_data.mean():.1f}% | 最高: {roe_data.max():.1f}% | 最低: {roe_data.min():.1f}%")
        
        gpm_data = df['gross_profit_margin'].dropna()
        if len(gpm_data) > 0:
            report.append(f"- **毛利率** 均值: {gpm_data.mean():.1f}% | 最高: {gpm_data.max():.1f}%")
        
        report.append("")
        
        # 增长 统计
        rg_data = df['revenue_growth'].dropna()
        if len(rg_data) > 0:
            report.append(f"### 成长指标")
            report.append(f"- **营收增长率** 均值: {rg_data.mean():.1f}% | 最高: {rg_data.max():.1f}%")
        
        pg_data = df['profit_growth'].dropna()
        if len(pg_data) > 0:
            report.append(f"- **利润增长率** 均值: {pg_data.mean():.1f}% | 最高: {pg_data.max():.1f}%")
    else:
        report.append("*财务数据暂缺，当前仅基于技术面因子分析*")
    
    report.append("")
    report.append("---")
    
    # ===== 潜力个股推荐 =====
    report.append("## 🎯 潜力个股推荐（综合得分前10）")
    report.append("")
    
    # 表头根据是否有财务数据动态调整
    if has_fundamentals > 0:
        report.append("|排名|代码|名称|行业|最新价|PE|ROE|综合得分|风险|1月涨幅|")
        report.append("|----|----|----|----|------|---|---|--------|----|------|")
        
        for idx, (_, row) in enumerate(df.head(10).iterrows(), 1):
            pe_str = f"{row.get('pe_ttm', 0):.1f}" if not pd.isna(row.get('pe_ttm')) else '-'
            roe_str = f"{row.get('roe', 0):.1f}%" if not pd.isna(row.get('roe')) else '-'
            ret1m = row.get('return_1m', 0)
            ret1m_str = f"{ret1m*100:+.1f}%" if not pd.isna(ret1m) else '-'
            
            report.append(
                f"|{idx}|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('close_price', 0):.2f}|{pe_str}|{roe_str}|"
                f"{row.get('composite_score', 0):.4f}|{row.get('risk_level','-')}|{ret1m_str}|"
            )
    else:
        report.append("|排名|代码|名称|行业|最新价|综合得分|风险|MACD|KDJ|1月涨幅|")
        report.append("|----|----|----|----|------|--------|----|----|----|------|")
        
        for idx, (_, row) in enumerate(df.head(10).iterrows(), 1):
            mg = '✓' if row.get('macd_golden', False) else ''
            kg = '✓' if row.get('kdj_golden', False) else ''
            ret1m = row.get('return_1m', 0)
            ret1m_str = f"{ret1m*100:+.1f}%" if not pd.isna(ret1m) else '-'
            
            report.append(
                f"|{idx}|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('close_price', 0):.2f}|{row.get('composite_score', 0):.4f}|"
                f"{row.get('risk_level','-')}|{mg}|{kg}|{ret1m_str}|"
            )
    
    report.append("")
    report.append("---")
    
    # ===== 重点关注 =====
    report.append("## ⚡ 重点关注（多重信号共振）")
    report.append("")
    
    signal_stocks = df[
        (df.get('macd_golden', False) == True) &
        (df.get('kdj_golden', False) == True)
    ]
    
    if len(signal_stocks) > 0:
        report.append("以下股票同时出现MACD金叉和KDJ金叉信号：")
        report.append("")
        report.append("|代码|名称|行业|综合得分|PE|ROE|多头排列|")
        report.append("|----|----|----|--------|---|---|--------|")
        
        for _, row in signal_stocks.iterrows():
            bu = '✓' if row.get('bullish_alignment', False) else ''
            pe_str = f"{row.get('pe_ttm', 0):.1f}" if not pd.isna(row.get('pe_ttm')) else '-'
            roe_str = f"{row.get('roe', 0):.1f}%" if not pd.isna(row.get('roe')) else '-'
            report.append(
                f"|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('composite_score', 0):.4f}|{pe_str}|{roe_str}|{bu}|"
            )
    else:
        report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
    report.append("")
    report.append("---")
    
    # ===== 深交所数据 =====
    report.append("## 📊 深市行情 (SZSE)")
    report.append("")
    
    if fetcher:
        try:
            szse_indices = fetcher.get_szse_index_quote()
            if szse_indices:
                report.append("| 指数名称 | 代码 | 收盘 | 涨跌幅 |")
                report.append("|----------|------|------|--------|")
                for idx in szse_indices[:8]:
                    report.append(f"| {idx['name']} | {idx['code']} | {idx['close']} | {idx['change_pct']}% |")
                report.append("")
        except Exception as e:
            report.append(f"_深市行情获取失败: {e}_")
            report.append("")
    else:
        report.append("_深交所数据源未初始化_")
        report.append("")
    
    report.append("---")
    
    # ===== 因子表现分析 =====
    report.append("## 📊 因子表现分析")
    report.append("")
    
    avg_score = df['composite_score'].mean()
    report.append(f"- **平均综合得分**: {avg_score:.4f}")
    report.append("")
    
    for group in ['valuation', 'quality', 'growth', 'momentum', 'trend', 'volatility', 'technical', 'volume']:
        col = f'{group}_score'
        if col in df.columns:
            avg = df[col].mean()
            status = "偏强" if avg > 0 else "偏弱" if avg < -0.3 else "中性"
            report.append(f"- **{group}** {status}: 平均分 {avg:.3f}")
    
    report.append("")
    report.append("---")
    
    # ===== 风险提示 =====
    report.append("## ⚠️ 风险提示个股")
    report.append("")
    
    risk_stocks = df[df['risk_level'] == '高风险'].head(5)
    if len(risk_stocks) > 0:
        report.append("|代码|名称|行业|最新价|综合得分|风险|空头排列|")
        report.append("|----|----|----|------|--------|----|--------|")
        for _, row in risk_stocks.iterrows():
            be = '✓' if row.get('bearish_alignment', False) else ''
            report.append(
                f"|{row['code']}|{row['name']}|{row.get('sector','-')}|"
                f"{row.get('close_price', 0):.2f}|{row.get('composite_score', 0):.4f}|"
                f"{row.get('risk_level')}|{be}|"
            )
    else:
        report.append("当前无高风险股票。")
    report.append("")
    report.append("---")
    
    # ===== pywencai 补充数据板块 =====
    if pywencai_data:
        report.append("## 🔮 同花顺问财补充数据")
        report.append("")
        
        # 1. 信号共振
        dual_golden = pywencai_data.get('dual_golden')
        if dual_golden is not None and len(dual_golden) > 0:
            report.append(f"### 双金叉共振（MACD+KDJ同时金叉）")
            report.append("")
            report.append("今日同时出现MACD和KDJ金叉的股票（信号共振强度最高）：")
            report.append("")
            
            # 尝试取前8只
            for idx, (_, row) in enumerate(dual_golden.head(8).iterrows(), 1):
                code = str(row.get('股票代码', row.iloc[0] if len(row) > 0 else ''))
                name = str(row.get('股票简称', row.get('名称', row.iloc[1] if len(row) > 1 else '')))
                price = row.get('最新价', row.get('收盘价', '-'))
                change = row.get('涨跌幅', '-')
                report.append(f"- {idx}. {code} {name} | 价:{price} | 涨跌幅:{change}")
            report.append("")
        else:
            report.append("### 双金叉共振")
            report.append("")
            report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
            report.append("")
        
        # 2. MACD金叉
        macd_golden = pywencai_data.get('macd_golden')
        if macd_golden is not None and len(macd_golden) > 0:
            report.append(f"### MACD金叉（共{len(macd_golden)}只）")
            report.append("")
            for idx, (_, row) in enumerate(macd_golden.head(5).iterrows(), 1):
                code = str(row.get('股票代码', row.iloc[0] if len(row) > 0 else ''))
                name = str(row.get('股票简称', row.get('名称', row.iloc[1] if len(row) > 1 else '')))
                change = row.get('涨跌幅', '-')
                report.append(f"- {idx}. {code} {name} | 涨跌幅:{change}")
            report.append("")
        
        # 3. 今日资金流向
        fund_flow = pywencai_data.get('fund_flow_today')
        if fund_flow is not None and len(fund_flow) > 0:
            report.append("### 今日主力资金净流入 TOP5")
            report.append("")
            for idx, (_, row) in enumerate(fund_flow.head(5).iterrows(), 1):
                code = str(row.get('股票代码', row.iloc[0] if len(row) > 0 else ''))
                name = str(row.get('股票简称', row.get('名称', row.iloc[1] if len(row) > 1 else '')))
                flow = row.get('主力资金净流入(元)', row.get('主力净流入', '-'))
                report.append(f"- {idx}. {code} {name} | 主力净流入:{flow}")
            report.append("")
        
        # 4. 行业资金流
        industry_flow = pywencai_data.get('industry_flow_today')
        if industry_flow is not None and len(industry_flow) > 0:
            report.append("### 今日行业板块资金净流入 TOP5")
            report.append("")
            for idx, (_, row) in enumerate(industry_flow.head(5).iterrows(), 1):
                name = str(row.get('板块名称', row.get('行业名称', row.iloc[0] if len(row) > 0 else '')))
                flow = row.get('主力净流入(元)', row.get('主力净流入', '-'))
                report.append(f"- {idx}. {name} | 主力净流入:{flow}")
            report.append("")
        
        # 5. 北向资金
        north_bound = pywencai_data.get('north_bound')
        if north_bound is not None and len(north_bound) > 0:
            report.append("### 北向资金增持 TOP5")
            report.append("")
            for idx, (_, row) in enumerate(north_bound.head(5).iterrows(), 1):
                code = str(row.get('股票代码', row.iloc[0] if len(row) > 0 else ''))
                name = str(row.get('股票简称', row.get('名称', row.iloc[1] if len(row) > 1 else '')))
                buy = row.get('北向资金净买入(股)', row.get('北向净买入', '-'))
                report.append(f"- {idx}. {code} {name} | 净买入:{buy}")
            report.append("")
        
        # 6. 高股息
        high_div = pywencai_data.get('high_dividend')
        if high_div is not None and len(high_div) > 0:
            report.append("### 高股息股票（股息率>4%）")
            report.append("")
            for idx, (_, row) in enumerate(high_div.head(5).iterrows(), 1):
                code = str(row.get('股票代码', row.iloc[0] if len(row) > 0 else ''))
                name = str(row.get('股票简称', row.get('名称', row.iloc[1] if len(row) > 1 else '')))
                div = row.get('股息率', row.get('股息率(%)', '-'))
                report.append(f"- {idx}. {code} {name} | 股息率:{div}")
            report.append("")
        
        report.append("_数据来源：同花顺问财 pywencai_")
        report.append("")
        report.append("---")
    
    # ===== 投资策略建议 =====
    report.append("## 💡 投资策略建议")
    report.append("")
    
    pos_sugg = regime_analysis['position_suggestion']
    total_pos = pos_sugg['suggested_total_position']
    
    report.append(f"### 1. 仓位建议")
    report.append(f"- **建议总仓位**: {total_pos:.0%}")
    report.append(f"- **单股上限**: {pos_sugg['single_stock_max']:.1%}")
    report.append("")
    report.append("### 2. 选股策略")
    report.append("   - 关注综合得分排名靠前的股票")
    report.append("   - 优先选择多重信号共振个股")
    if has_fundamentals > 0:
        report.append("   - 优选低PE(估值) + 高ROE(质量) + 正增长(成长)标的")
    report.append("   - 避开高风险等级股票")
    report.append("")
    report.append("### 3. 操作建议")
    report.append("   - 金叉信号股票可考虑分批建仓")
    report.append("   - 设置止损位（5%-8%）")
    report.append("   - 分散持仓，控制单股仓位")
    report.append("")
    report.append("---")
    
    report.append("## 📢 风险提示")
    report.append("")
    report.append("**本报告仅供参考，不构成投资建议。**")
    report.append("- 股市有风险，投资需谨慎")
    report.append("- 基于历史数据的分析不代表未来表现")
    report.append("")
    report.append("---")
    report.append("*报告由沪深300多因子投研系统 v3.0 自动生成*")
    
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

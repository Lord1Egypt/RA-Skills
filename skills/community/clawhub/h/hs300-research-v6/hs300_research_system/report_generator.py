#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 报告生成模块
"""

import logging
import os
import pandas as pd
import numpy as np
from datetime import datetime
from config import OUTPUT_DIR, REPORT_CONFIG, RISK_DISCLAIMER

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成类"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.top_n = REPORT_CONFIG['top_n']
        self.bottom_n = REPORT_CONFIG['bottom_n']
    
    def generate_markdown_report(self, factors_df, market_data=None):
        """
        生成Markdown格式的投研日报
        
        Args:
            factors_df: 包含所有股票因子和得分的DataFrame
            market_data: 市场数据字典
        
        Returns:
            str: Markdown报告内容
        """
        logger.info("正在生成Markdown报告...")
        
        today = datetime.now().strftime('%Y年%m月%d日')
        report_time = datetime.now().strftime('%H:%M:%S')
        
        # 确保数据已排序
        df = factors_df.sort_values('composite_score', ascending=False)
        
        # 选出前N和后N
        top_stocks = df.head(self.top_n)
        bottom_stocks = df.tail(self.bottom_n)
        
        # 开始生成报告
        report = []
        
        # 标题
        report.append(f"# 沪深300多因子投研日报")
        report.append(f"**生成时间：{today} {report_time}**")
        report.append("")
        report.append("---")
        
        # 市场概览
        report.append("## 📊 市场概览")
        report.append("")
        
        if market_data and 'hs300' in market_data:
            hs300_data = market_data['hs300']
            if hs300_data is not None and len(hs300_data) > 0:
                latest = hs300_data.iloc[-1]
                prev = hs300_data.iloc[-2] if len(hs300_data) > 1 else latest
                change_pct = (latest['close'] - prev['close']) / prev['close'] * 100
                
                report.append(f"- **沪深300指数**：{latest['close']:.2f} 点")
                report.append(f"- **涨跌幅**：{change_pct:+.2f}%")
                report.append(f"- **成交量**：{latest['volume'] / 1e8:.2f} 亿股")
                report.append(f"- **成交额**：{latest['amount'] / 1e8:.2f} 亿元")
        
        # 市场统计
        report.append(f"- **分析股票数量**：{len(df)} 只")
        report.append(f"- **平均综合得分**：{df['composite_score'].mean():.4f}")
        report.append(f"- **得分标准差**：{df['composite_score'].std():.4f}")
        report.append("")
        
        # 市场情绪判断
        avg_score = df['composite_score'].mean()
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
        
        # 金叉死叉统计
        report.append("## 📈 技术信号统计")
        report.append("")
        
        if 'macd_golden' in df.columns:
            macd_gold_count = df['macd_golden'].sum()
            report.append(f"- **MACD金叉**：{macd_gold_count} 只股票")
        
        if 'kdj_golden' in df.columns:
            kdj_gold_count = df['kdj_golden'].sum()
            report.append(f"- **KDJ金叉**：{kdj_gold_count} 只股票")
        
        if 'bullish_alignment' in df.columns:
            bullish_count = df['bullish_alignment'].sum()
            report.append(f"- **均线多头排列**：{bullish_count} 只股票")
        
        if 'bearish_alignment' in df.columns:
            bearish_count = df['bearish_alignment'].sum()
            report.append(f"- **均线空头排列**：{bearish_count} 只股票")
        
        report.append("")
        report.append("---")
        
        # 潜力个股推荐
        report.append("## 🌟 潜力个股推荐（综合得分前20）")
        report.append("")
        report.append("| 排名 | 股票代码 | 股票名称 | 最新价格 | 综合得分 | MACD金叉 | KDJ金叉 | 多头排列 | 1月涨幅 | RSI |")
        report.append("|------|----------|----------|----------|----------|----------|---------|----------|---------|-----|")
        
        for idx, (_, row) in enumerate(top_stocks.iterrows(), 1):
            code = row.get('code', '')
            name = row.get('name', '')
            price = row.get('close_price', 0)
            score = row.get('composite_score', 0)
            macd_gold = '✓' if row.get('macd_golden', False) else ''
            kdj_gold = '✓' if row.get('kdj_golden', False) else ''
            bullish = '✓' if row.get('bullish_alignment', False) else ''
            return_1m = row.get('return_1m', np.nan)
            return_1m_str = f"{return_1m*100:+.2f}%" if not pd.isna(return_1m) else '-'
            rsi = row.get('rsi', np.nan)
            rsi_str = f"{rsi:.1f}" if not pd.isna(rsi) else '-'
            
            report.append(f"| {idx} | {code} | {name} | {price:.2f} | {score:.4f} | {macd_gold} | {kdj_gold} | {bullish} | {return_1m_str} | {rsi_str} |")
        
        report.append("")
        report.append("---")
        
        # 重点关注个股（有多个金叉信号）
        report.append("## 🎯 重点关注（多重信号共振）")
        report.append("")
        report.append("以下股票同时出现MACD金叉和KDJ金叉信号，值得重点关注：")
        report.append("")
        
        signal_stocks = df[
            (df.get('macd_golden', False) == True) & 
            (df.get('kdj_golden', False) == True)
        ]
        
        if len(signal_stocks) > 0:
            report.append("| 股票代码 | 股票名称 | 最新价格 | 综合得分 | 多头排列 | 1月涨幅 |")
            report.append("|----------|----------|----------|----------|----------|---------|")
            
            for _, row in signal_stocks.iterrows():
                code = row.get('code', '')
                name = row.get('name', '')
                price = row.get('close_price', 0)
                score = row.get('composite_score', 0)
                bullish = '✓' if row.get('bullish_alignment', False) else ''
                return_1m = row.get('return_1m', np.nan)
                return_1m_str = f"{return_1m*100:+.2f}%" if not pd.isna(return_1m) else '-'
                
                report.append(f"| {code} | {name} | {price:.2f} | {score:.4f} | {bullish} | {return_1m_str} |")
        else:
            report.append("今日暂无同时出现MACD和KDJ金叉的股票。")
        
        report.append("")
        report.append("---")
        
        # 风险提示个股
        report.append("## ⚠️ 风险提示个股（综合得分后10）")
        report.append("")
        report.append("以下股票综合得分较低，建议暂时规避：")
        report.append("")
        
        report.append("| 排名 | 股票代码 | 股票名称 | 最新价格 | 综合得分 | 空头排列 | 1月涨幅 | RSI |")
        report.append("|------|----------|----------|----------|----------|----------|---------|-----|")
        
        for idx, (_, row) in enumerate(bottom_stocks.iloc[::-1].iterrows(), 1):
            code = row.get('code', '')
            name = row.get('name', '')
            price = row.get('close_price', 0)
            score = row.get('composite_score', 0)
            bearish = '✓' if row.get('bearish_alignment', False) else ''
            return_1m = row.get('return_1m', np.nan)
            return_1m_str = f"{return_1m*100:+.2f}%" if not pd.isna(return_1m) else '-'
            rsi = row.get('rsi', np.nan)
            rsi_str = f"{rsi:.1f}" if not pd.isna(rsi) else '-'
            
            report.append(f"| {idx} | {code} | {name} | {price:.2f} | {score:.4f} | {bearish} | {return_1m_str} | {rsi_str} |")
        
        report.append("")
        report.append("---")
        
        # 因子分析
        report.append("## 🧮 因子分析")
        report.append("")
        report.append("### 各因子分布统计")
        report.append("")
        
        key_factors = ['return_1m', 'std_1m', 'trend_score', 'rsi']
        for factor in key_factors:
            if factor in df.columns:
                valid_data = df[factor].dropna()
                if len(valid_data) > 0:
                    report.append(f"- **{factor}**：")
                    report.append(f"  - 均值: {valid_data.mean():.4f}")
                    report.append(f"  - 中位数: {valid_data.median():.4f}")
                    report.append(f"  - 标准差: {valid_data.std():.4f}")
        
        report.append("")
        report.append("---")
        
        # 投资策略建议
        report.append("## 💡 投资策略建议")
        report.append("")
        report.append("基于今日多因子模型分析，给出以下投资建议：")
        report.append("")
        
        # 根据市场情况给出建议
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
        report.append(RISK_DISCLAIMER)
        report.append("")
        report.append("---")
        
        report.append("*本报告由沪深300多因子投研系统自动生成，仅供参考，不构成投资建议。*")
        
        return "\n".join(report)
    
    def save_report(self, report_content, filename=None, format_type='markdown'):
        """
        保存报告到文件
        
        Args:
            report_content: 报告内容
            filename: 文件名（不含扩展名）
            format_type: 格式类型 (markdown, html, excel)
        """
        if filename is None:
            filename = f"沪深300投研日报_{datetime.now().strftime('%Y%m%d')}"
        
        if format_type == 'markdown':
            filepath = os.path.join(self.output_dir, f'{filename}.md')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            logger.info(f"Markdown报告已保存到: {filepath}")
            return filepath
        elif format_type == 'excel':
            # Excel格式需要特殊处理
            filepath = os.path.join(self.output_dir, f'{filename}.xlsx')
            logger.info(f"Excel报告已保存到: {filepath}")
            return filepath
        else:
            logger.error(f"不支持的格式类型: {format_type}")
            return None
    
    def generate_excel_report(self, factors_df, filename=None):
        """
        生成Excel格式的详细报告
        
        Args:
            factors_df: 因子数据DataFrame
            filename: 文件名
        """
        if filename is None:
            filename = f"沪深300投研日报_{datetime.now().strftime('%Y%m%d')}_详细数据"
        
        filepath = os.path.join(self.output_dir, f'{filename}.xlsx')
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 所有股票得分表
            scored_df = factors_df.sort_values('composite_score', ascending=False)
            scored_df.to_excel(writer, sheet_name='综合得分排名', index=False)
            
            # 推荐股票
            top_stocks = scored_df.head(self.top_n)
            top_stocks.to_excel(writer, sheet_name='推荐股票池', index=False)
            
            # 技术信号表
            signal_cols = ['code', 'name', 'close_price', 'macd_golden', 'kdj_golden', 
                          'bullish_alignment', 'bearish_alignment', 'composite_score']
            if all(col in scored_df.columns for col in signal_cols):
                signal_df = scored_df[signal_cols]
                signal_df.to_excel(writer, sheet_name='技术信号汇总', index=False)
        
        logger.info(f"Excel详细报告已保存到: {filepath}")
        return filepath


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # 测试报告生成
    from data_fetcher import DataFetcher
    from factor_calculator import FactorCalculator
    
    fetcher = DataFetcher()
    calculator = FactorCalculator()
    generator = ReportGenerator()
    
    # 获取测试数据
    stocks = fetcher.get_hs300_stocks()
    if stocks:
        test_stocks = stocks[:10]  # 测试10只股票
        all_factors = []
        
        for stock in test_stocks:
            daily_data = fetcher.get_stock_daily(stock['code'])
            if daily_data is not None:
                stock_data = {
                    'code': stock['code'],
                    'name': stock['name'],
                    'daily': daily_data
                }
                factors = calculator.calculate_all_factors(stock_data)
                if factors:
                    all_factors.append(factors)
        
        if all_factors:
            factors_df = pd.DataFrame(all_factors)
            factors_df = calculator.calculate_factor_score(factors_df)
            
            # 生成报告
            md_report = generator.generate_markdown_report(factors_df)
            print("报告生成成功！")
            print("\n报告预览（前500字符）：")
            print(md_report[:500])
            
            # 保存报告
            saved_path = generator.save_report(md_report)
            print(f"\n报告已保存到: {saved_path}")

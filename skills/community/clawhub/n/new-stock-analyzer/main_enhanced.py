#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析工具 - 增强版主程序
使用增强版分析器，提供更深入的分析
"""

import sys
import os
import logging
import argparse
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_data import StockDataFetcher
from stock_analyzer_enhanced import EnhancedStockAnalyzer
from openclaw_notifier import OpenClawNotifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class EnhancedStockAnalysisTool:
    """增强版新股分析工具"""
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.analyzer = EnhancedStockAnalyzer()
        self.notifier = OpenClawNotifier()
        
    def run_daily_analysis(self, output_file: str = None) -> str:
        """
        执行每日增强分析
        
        Args:
            output_file: 输出文件路径，如果为None则只返回结果
            
        Returns:
            分析结果文本
        """
        logger.info("开始执行每日增强分析...")
        
        try:
            # 获取今日新股
            stocks = self.fetcher.get_today_new_stocks()
            
            if not stocks:
                message = "今日无新股申购"
                logger.info(message)
                
                if output_file:
                    self._save_to_file(output_file, message)
                
                return message
            
            logger.info(f"获取到{len(stocks)}只今日新股")
            
            # 使用增强版分析器分析
            report = self.analyzer.generate_enhanced_report(stocks)
            
            # 添加时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_report = f"📅 分析时间: {timestamp}\n\n{report}"
            
            # 输出到文件
            if output_file:
                self._save_to_file(output_file, full_report)
                logger.info(f"分析结果已保存到: {output_file}")
            
            # 输出到控制台
            print(full_report)
            
            return full_report
            
        except Exception as e:
            error_msg = f"分析失败: {str(e)}"
            logger.error(error_msg)
            
            if output_file:
                self._save_to_file(output_file, error_msg)
            
            return error_msg
    
    def run_weekly_analysis(self, output_file: str = None) -> str:
        """
        执行本周分析
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            分析结果文本
        """
        logger.info("开始执行本周分析...")
        
        try:
            # 获取本周新股
            stocks = self.fetcher.get_weekly_new_stocks()
            
            if not stocks:
                message = "本周无新股申购"
                logger.info(message)
                
                if output_file:
                    self._save_to_file(output_file, message)
                
                return message
            
            logger.info(f"获取到{len(stocks)}只本周新股")
            
            # 使用增强版分析器分析
            report = self.analyzer.generate_enhanced_report(stocks)
            
            # 添加时间戳和标题
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = "📅 本周新股分析报告"
            separator = "=" * 50
            
            full_report = f"{title}\n{separator}\n分析时间: {timestamp}\n分析数量: {len(stocks)}只新股\n{separator}\n\n{report}"
            
            # 输出到文件
            if output_file:
                self._save_to_file(output_file, full_report)
                logger.info(f"本周分析结果已保存到: {output_file}")
            
            # 输出到控制台
            print(full_report)
            
            return full_report
            
        except Exception as e:
            error_msg = f"本周分析失败: {str(e)}"
            logger.error(error_msg)
            
            if output_file:
                self._save_to_file(output_file, error_msg)
            
            return error_msg
    
    def analyze_specific_stock(self, stock_code: str, output_file: str = None) -> str:
        """
        分析特定股票
        
        Args:
            stock_code: 股票代码
            output_file: 输出文件路径
            
        Returns:
            分析结果文本
        """
        logger.info(f"开始分析特定股票: {stock_code}")
        
        try:
            # 获取股票数据
            stock = self.fetcher.get_stock_by_code(stock_code)
            
            if not stock:
                message = f"未找到股票代码: {stock_code}"
                logger.warning(message)
                
                if output_file:
                    self._save_to_file(output_file, message)
                
                return message
            
            # 使用增强版分析器分析
            analysis = self.analyzer.analyze_stock_enhanced(stock)
            
            # 生成详细报告
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_lines = [
                f"📊 个股深度分析报告",
                f"=" * 50,
                f"分析时间: {timestamp}",
                f"股票代码: {stock_code}",
                f"=" * 50,
                "",
                analysis['summary'],
                "",
                "📈 详细分析:",
                "-" * 30,
                f"基本信息:",
                f"  名称: {analysis['basic_info']['name']}",
                f"  市场: {analysis['basic_info']['market']}",
                f"  行业: {analysis['basic_info']['industry']}",
                f"  保荐机构: {analysis['basic_info']['recommend_org']}",
                "",
                f"估值分析:",
                f"  状态: {analysis['valuation_analysis']['valuation_status']}",
                f"  评分: {analysis['valuation_analysis']['valuation_score']}/100",
                f"  PE比率: {analysis['valuation_analysis']['pe_ratio_analysis'].get('pe_ratio', 'N/A')}",
                "",
                f"市场分析:",
                f"  市场评分: {analysis['market_analysis']['market_score']}/100",
                f"  保荐机构: {'头部' if analysis['market_analysis']['underwriter_analysis']['is_top'] else '一般'}",
                "",
                f"风险评估:",
                f"  等级: {analysis['risk_assessment']['risk_level']}",
                f"  评分: {analysis['risk_assessment']['risk_score']}/100",
                f"  风险因素: {', '.join(analysis['risk_assessment']['risk_factors']) if analysis['risk_assessment']['risk_factors'] else '无'}",
                f"  预警信号: {', '.join(analysis['risk_assessment']['warning_signals']) if analysis['risk_assessment']['warning_signals'] else '无'}",
                "",
                f"投资建议:",
                f"  操作: {analysis['investment_advice']['action']}",
                f"  信心度: {analysis['investment_advice']['confidence']}",
                f"  综合评分: {analysis['investment_advice']['total_score']}/100",
                f"  仓位建议: {analysis['investment_advice']['position_suggestion']}",
                "",
                "=" * 50,
                "⚠️ 风险提示: 投资有风险，决策需谨慎",
            ]
            
            full_report = "\n".join(report_lines)
            
            # 输出到文件
            if output_file:
                self._save_to_file(output_file, full_report)
                logger.info(f"个股分析结果已保存到: {output_file}")
            
            # 输出到控制台
            print(full_report)
            
            return full_report
            
        except Exception as e:
            error_msg = f"个股分析失败: {str(e)}"
            logger.error(error_msg)
            
            if output_file:
                self._save_to_file(output_file, error_msg)
            
            return error_msg
    
    def test_connection(self) -> str:
        """测试连接"""
        logger.info("测试数据连接...")
        
        try:
            # 测试数据获取
            stocks = self.fetcher.get_today_new_stocks()
            
            if stocks is None:
                return "❌ 数据获取失败"
            
            return f"✅ 连接正常，获取到{len(stocks)}只今日新股"
            
        except Exception as e:
            return f"❌ 连接测试失败: {str(e)}"
    
    def _save_to_file(self, filepath: str, content: str):
        """保存内容到文件"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
    
    def send_to_openclaw(self, content: str):
        """发送到OpenClaw"""
        try:
            self.notifier.send_notification(content)
            logger.info("已发送通知到OpenClaw")
        except Exception as e:
            logger.error(f"发送到OpenClaw失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='增强版新股分析工具')
    parser.add_argument('--daily', action='store_true', help='执行每日分析')
    parser.add_argument('--weekly', action='store_true', help='执行本周分析')
    parser.add_argument('--stock', type=str, help='分析特定股票代码')
    parser.add_argument('--test', action='store_true', help='测试连接')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--openclaw', action='store_true', help='发送结果到OpenClaw')
    
    args = parser.parse_args()
    
    tool = EnhancedStockAnalysisTool()
    
    if args.test:
        result = tool.test_connection()
        print(result)
        
    elif args.stock:
        result = tool.analyze_specific_stock(args.stock, args.output)
        if args.openclaw:
            tool.send_to_openclaw(result)
            
    elif args.weekly:
        result = tool.run_weekly_analysis(args.output)
        if args.openclaw:
            tool.send_to_openclaw(result)
            
    else:  # 默认执行每日分析
        result = tool.run_daily_analysis(args.output)
        if args.openclaw:
            tool.send_to_openclaw(result)


if __name__ == "__main__":
    main()
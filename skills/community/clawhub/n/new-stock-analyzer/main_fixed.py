#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析工具 - 修复版主程序
修复了市场分类、名称显示、价格显示问题
"""

import sys
import os
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_data_enhanced import EnhancedStockDataFetcher
from stock_analyzer_detailed import DetailedStockAnalyzer
from cfi_manual_validator import CFIManualValidator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def run_detailed_analysis(print_result: bool = True, enable_validation: bool = True) -> str:
    """
    运行详细分析（包含多数据源验证）
    
    Args:
        print_result: 是否打印结果
        enable_validation: 是否启用多数据源验证
        
    Returns:
        分析结果字符串
    """
    try:
        logger.info("开始执行详细分析...")
        
        # 1. 获取数据
        fetcher = EnhancedStockDataFetcher()
        stocks = fetcher.get_today_detailed_stocks()
        
        if not stocks:
            result = "📅 今日无新股申购"
            if print_result:
                print(result)
            return result
        
        logger.info(f"获取到{len(stocks)}只新股")
        
        # 2. 多数据源验证（如果启用）
        validation_info = ""
        if enable_validation:
            try:
                logger.info("执行多数据源验证...")
                validator = MultiSourceValidator()
                validation_result = validator.validate_and_report()
                
                # 提取验证信息
                validation_info = _format_validation_info(validation_result)
                logger.info(f"数据验证完成: {validation_result['comparison']['summary'].get('data_quality', '未知')}")
                
            except Exception as e:
                logger.warning(f"多数据源验证失败（继续执行）: {e}")
                validation_info = "⚠️ 数据验证暂时不可用\n"
        
        # 3. 分析数据
        analyzer = DetailedStockAnalyzer()
        analyses = analyzer.analyze_multiple_stocks(stocks)
        
        # 4. 生成报告（包含验证信息）
        report = analyzer.generate_detailed_report(stocks)
        
        # 添加验证信息到报告开头
        if validation_info:
            report = validation_info + report
        
        if print_result:
            print(report)
        
        return report
        
    except Exception as e:
        error_msg = f"❌ 分析失败: {e}"
        logger.error(error_msg, exc_info=True)
        if print_result:
            print(error_msg)
        return error_msg


def run_recent_analysis(days: int = 7, print_result: bool = True) -> str:
    """
    运行近期分析（包含未来几天）
    
    Args:
        days: 查询天数
        print_result: 是否打印结果
        
    Returns:
        分析结果字符串
    """
    try:
        logger.info(f"开始执行近期分析（{days}天）...")
        
        # 1. 获取近期数据
        fetcher = EnhancedStockDataFetcher()
        stocks = fetcher.get_recent_stocks(days=days)
        
        if not stocks:
            result = f"📅 近期{days}天内无新股申购"
            if print_result:
                print(result)
            return result
        
        logger.info(f"获取到{len(stocks)}只近期新股")
        
        # 2. 按申购日期分组
        from collections import defaultdict
        stocks_by_date = defaultdict(list)
        
        for stock in stocks:
            apply_date = stock.get('apply_date_formatted', '未知日期')
            stocks_by_date[apply_date].append(stock)
        
        # 3. 分析并生成报告
        analyzer = DetailedStockAnalyzer()
        
        lines = [
            f"📊 近期新股分析报告（{days}天内）",
            "=" * 50,
            f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        for date, date_stocks in sorted(stocks_by_date.items()):
            lines.append(f"📅 {date} ({len(date_stocks)}只)")
            lines.append("-" * 40)
            
            analyses = analyzer.analyze_multiple_stocks(date_stocks)
            for analysis in analyses:
                if 'error' in analysis:
                    lines.append(f"❌ 分析失败: {analysis['error']}")
                else:
                    basic = analysis['basic_info']
                    time_info = analysis['time_info']
                    price = analysis['price_info']
                    advice = analysis['investment_advice']
                    
                    lines.append(f"• {basic['name']}({basic['code']})")
                    lines.append(f"  市场: {basic['market']} | 价格: {price['issue_price']}")
                    lines.append(f"  建议: {advice['action']} ({advice['total_score']}/100)")
            
            lines.append("")
        
        # 汇总统计
        total_stocks = len(stocks)
        good_stocks = sum(1 for s in stocks if analyzer.analyze_stock_detailed(s)['investment_advice']['total_score'] >= 65)
        
        lines.append(f"📈 汇总统计")
        lines.append(f"- 新股总数: {total_stocks}只")
        lines.append(f"- 建议申购: {good_stocks}只")
        lines.append(f"- 申购率: {good_stocks/total_stocks*100:.1f}%")
        lines.append("")
        lines.append("⚠️ 风险提示: 投资有风险，申购需谨慎")
        
        report = "\n".join(lines)
        
        if print_result:
            print(report)
        
        return report
        
    except Exception as e:
        error_msg = f"❌ 近期分析失败: {e}"
        logger.error(error_msg, exc_info=True)
        if print_result:
            print(error_msg)
        return error_msg


def run_cfi_validation(print_result: bool = True) -> dict:
    """
    运行中财网数据验证
    
    Args:
        print_result: 是否打印结果
        
    Returns:
        验证结果字典
    """
    try:
        logger.info("开始中财网数据验证...")
        
        # 1. 获取东方财富数据
        fetcher = EnhancedStockDataFetcher()
        eastmoney_stocks = fetcher.get_today_detailed_stocks()
        
        # 2. 获取近期数据用于完整对比
        recent_stocks = fetcher.get_recent_stocks(days=7)
        
        # 3. 运行中财网验证
        validator = CFIManualValidator()
        report = validator.generate_validation_report(recent_stocks)
        
        if print_result:
            print(report)
        
        # 返回验证结果
        comparison = validator.compare_with_eastmoney(recent_stocks)
        result = {
            'eastmoney_data': eastmoney_stocks,
            'cfi_data': validator.get_cfi_stocks(),
            'comparison': comparison,
            'report': report,
        }
        
        return result
        
    except Exception as e:
        error_msg = f"❌ 中财网验证失败: {e}"
        logger.error(error_msg, exc_info=True)
        if print_result:
            print(error_msg)
        return {'error': str(e)}

def _format_validation_info(validation_result: dict) -> str:
    """格式化验证信息"""
    lines = []
    
    comparison = validation_result.get('comparison', {})
    summary = comparison.get('summary', {})
    
    # 数据质量标记
    data_quality = summary.get('data_quality', '未知')
    consistency = summary.get('data_consistency', 0)
    
    if data_quality == '优秀':
        lines.append("✅ 数据验证: 优秀（多数据源高度一致）")
    elif data_quality == '良好':
        lines.append("✅ 数据验证: 良好（数据源基本一致）")
    elif data_quality == '一般':
        lines.append("⚠️ 数据验证: 一般（数据源有差异）")
    else:
        lines.append("⚠️ 数据验证: 需人工确认")
    
    # 详细统计
    lines.append(f"📊 验证统计:")
    lines.append(f"  数据源: {summary.get('total_sources', 0)}个")
    lines.append(f"  股票总数: {summary.get('total_unique_stocks', 0)}只")
    lines.append(f"  共同股票: {summary.get('common_stocks_count', 0)}只")
    lines.append(f"  一致性: {consistency:.1f}%")
    
    # 警告信息
    warnings = comparison.get('warnings', [])
    if warnings:
        lines.append("⚠️ 验证警告:")
        for warning in warnings[:3]:  # 只显示前3个警告
            lines.append(f"  • {warning}")
    
    lines.append("")  # 空行分隔
    return "\n".join(lines)

def test_connection() -> bool:
    """测试连接"""
    try:
        logger.info("测试数据连接...")
        
        fetcher = EnhancedStockDataFetcher()
        stocks = fetcher.get_today_detailed_stocks()
        
        if stocks:
            print(f"✅ 连接正常，获取到{len(stocks)}只今日新股")
            for stock in stocks[:3]:  # 显示前3只
                print(f"  - {stock.get('display_name', stock.get('name'))}({stock.get('code')})")
                print(f"    市场: {stock.get('market')} | 申购: {stock.get('apply_date_formatted')}")
                print(f"    价格: {stock.get('issue_price_formatted')}")
            return True
        else:
            print("✅ 连接正常，今日无新股")
            return True
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新股分析工具 - 修复版（含多数据源验证）')
    parser.add_argument('--test', action='store_true', help='测试连接')
    parser.add_argument('--daily', action='store_true', help='执行每日分析')
    parser.add_argument('--recent', type=int, nargs='?', const=7, help='执行近期分析（默认7天）')
    parser.add_argument('--validate', action='store_true', help='执行多数据源验证')
    parser.add_argument('--no-validate', action='store_true', help='禁用多数据源验证')
    parser.add_argument('--no-print', action='store_true', help='不打印结果（用于定时任务）')
    
    args = parser.parse_args()
    
    if args.test:
        test_connection()
    elif args.validate:
        run_cfi_validation(print_result=not args.no_print)
    elif args.recent:
        run_recent_analysis(days=args.recent, print_result=not args.no_print)
    elif args.daily:
        enable_validation = not args.no_validate
        run_detailed_analysis(print_result=not args.no_print, enable_validation=enable_validation)
    else:
        # 默认执行每日分析（包含验证）
        run_detailed_analysis(print_result=True, enable_validation=True)


if __name__ == "__main__":
    main()
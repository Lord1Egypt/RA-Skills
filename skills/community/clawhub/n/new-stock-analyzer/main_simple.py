#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股分析工具 - 简化版主程序
直接在OpenClaw会话中输出结果
"""

import sys
import os
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_data import fetcher as stock_fetcher
from stock_analyzer import analyzer as stock_analyzer
from openclaw_notifier import notifier as openclaw_notifier

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def run_daily_analysis(print_result: bool = True):
    """
    执行每日分析并输出结果
    
    Args:
        print_result: 是否打印结果到控制台
        
    Returns:
        分析结果和通知消息
    """
    logger.info("开始执行每日新股分析")
    
    try:
        # 1. 获取今日新股数据
        stocks = stock_fetcher.get_today_new_stocks()
        
        if not stocks:
            message = "📭 今日无新股可申购，好好休息吧！😴"
            if print_result:
                print(message)
            return {
                'status': 'success',
                'message': message,
                'stocks_count': 0,
                'analyses_count': 0,
            }
        
        logger.info(f"获取到 {len(stocks)} 只今日新股")
        
        # 2. 分析新股
        analyses = stock_analyzer.analyze_multiple_stocks(stocks)
        
        # 3. 生成汇总报告
        summary = stock_analyzer.generate_summary_report(analyses)
        
        # 4. 生成通知消息
        reminder_message = openclaw_notifier.send_daily_reminder(stocks)
        report_message = openclaw_notifier.send_stock_report(analyses, summary)
        
        # 5. 输出结果
        if print_result:
            print("\n" + "=" * 60)
            print("新股分析工具 - 每日报告")
            print("=" * 60)
            print(reminder_message)
            print("\n" + "=" * 60)
            print("详细分析报告:")
            print("=" * 60)
            print(report_message)
        
        logger.info("每日分析完成")
        
        return {
            'status': 'success',
            'message': f'分析完成，共{len(stocks)}只新股',
            'stocks_count': len(stocks),
            'analyses_count': len(analyses),
            'reminder_message': reminder_message,
            'report_message': report_message,
            'summary': summary,
            'timestamp': datetime.now().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"每日分析失败: {e}", exc_info=True)
        
        # 生成错误消息
        error_message = openclaw_notifier.send_error_notification(str(e))
        
        if print_result:
            print("\n" + "=" * 60)
            print("❌ 新股分析工具错误")
            print("=" * 60)
            print(error_message)
        
        return {
            'status': 'error',
            'message': str(e),
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
        }


def run_weekly_analysis(print_result: bool = True):
    """
    执行每周分析并输出结果
    
    Args:
        print_result: 是否打印结果到控制台
        
    Returns:
        分析结果和通知消息
    """
    logger.info("开始执行每周新股分析")
    
    try:
        # 获取本周新股
        stocks = stock_fetcher.get_week_new_stocks()
        
        if not stocks:
            message = "📅 本周无新股可申购，可以关注其他投资机会。"
            if print_result:
                print(message)
            return {
                'status': 'success',
                'message': message,
                'stocks_count': 0,
            }
        
        logger.info(f"获取到 {len(stocks)} 只本周新股")
        
        # 按日期分组
        from collections import defaultdict
        stocks_by_date = defaultdict(list)
        
        for stock in stocks:
            apply_date = stock.get('apply_date')
            if apply_date:
                stocks_by_date[apply_date].append(stock)
        
        # 生成周报消息
        weekly_message = openclaw_notifier.send_weekly_report(stocks_by_date)
        
        # 输出结果
        if print_result:
            print("\n" + "=" * 60)
            print("新股分析工具 - 每周报告")
            print("=" * 60)
            print(weekly_message)
        
        logger.info("每周分析完成")
        
        return {
            'status': 'success',
            'message': f'周报生成完成，共{len(stocks)}只新股',
            'stocks_count': len(stocks),
            'dates_count': len(stocks_by_date),
            'weekly_message': weekly_message,
            'timestamp': datetime.now().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"每周分析失败: {e}", exc_info=True)
        
        # 生成错误消息
        error_message = openclaw_notifier.send_error_notification(str(e))
        
        if print_result:
            print("\n" + "=" * 60)
            print("❌ 新股分析工具错误")
            print("=" * 60)
            print(error_message)
        
        return {
            'status': 'error',
            'message': str(e),
            'error_message': error_message,
            'timestamp': datetime.now().isoformat(),
        }


def test_connection():
    """测试连接"""
    print("执行连接测试...")
    
    try:
        # 测试数据源
        stocks = stock_fetcher.get_today_new_stocks()
        data_source_ok = len(stocks) >= 0  # 只要不报错就算成功
        
        print(f"数据源测试: {'✅ 正常' if data_source_ok else '❌ 异常'}")
        print(f"获取到新股: {len(stocks)} 只")
        
        if stocks:
            print("示例股票:")
            for i, stock in enumerate(stocks[:2], 1):
                print(f"  {i}. {stock.get('name')} ({stock.get('code')})")
        
        return {
            'data_source': data_source_ok,
            'stocks_count': len(stocks),
            'overall': data_source_ok,
        }
        
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return {
            'data_source': False,
            'error': str(e),
            'overall': False,
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新股分析工具 - 简化版')
    parser.add_argument('--daily', action='store_true', help='执行每日分析')
    parser.add_argument('--weekly', action='store_true', help='执行每周分析')
    parser.add_argument('--test', action='store_true', help='测试连接')
    parser.add_argument('--quiet', action='store_true', help='安静模式，不输出结果')
    
    args = parser.parse_args()
    
    # 创建必要目录
    os.makedirs('data/cache', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    
    if args.test:
        results = test_connection()
        print(f"\n测试结果: {'✅ 全部正常' if results['overall'] else '❌ 存在异常'}")
        
    elif args.weekly:
        print("执行每周分析...")
        result = run_weekly_analysis(not args.quiet)
        if result['status'] == 'success':
            print(f"✅ 周报生成完成: {result['message']}")
        else:
            print(f"❌ 周报生成失败: {result['message']}")
        
    else:  # 默认执行每日分析
        print("执行每日分析...")
        result = run_daily_analysis(not args.quiet)
        if result['status'] == 'success':
            print(f"✅ 分析完成: {result['message']}")
        else:
            print(f"❌ 分析失败: {result['message']}")


if __name__ == "__main__":
    main()
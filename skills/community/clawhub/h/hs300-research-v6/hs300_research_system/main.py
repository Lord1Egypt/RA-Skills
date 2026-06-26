#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300晨间多因子投研系统 - 主程序
"""

import logging
import os
import sys
import time
from datetime import datetime
import pandas as pd
import schedule

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import LOG_CONFIG, REPORT_TIME, OUTPUT_DIR, DATA_DIR
from data_fetcher import DataFetcher
from factor_calculator import FactorCalculator
from report_generator import ReportGenerator


def setup_logging():
    """设置日志"""
    if not os.path.exists(os.path.dirname(LOG_CONFIG['file'])):
        os.makedirs(os.path.dirname(LOG_CONFIG['file']))
    
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG['level']),
        format=LOG_CONFIG['format'],
        handlers=[
            logging.FileHandler(LOG_CONFIG['file'], encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def run_analysis():
    """执行完整的分析流程"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("开始执行沪深300多因子投研分析...")
    logger.info(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    try:
        # 初始化各模块
        fetcher = DataFetcher()
        calculator = FactorCalculator()
        generator = ReportGenerator()
        
        # 1. 获取股票列表
        logger.info("\n[1/5] 获取沪深300成分股列表...")
        stocks = fetcher.get_hs300_stocks()
        if not stocks:
            logger.error("获取沪深300成分股失败，程序终止")
            return False
        logger.info(f"成功获取 {len(stocks)} 只成分股")
        
        # 2. 获取市场数据
        logger.info("\n[2/5] 获取市场整体数据...")
        market_data = fetcher.get_market_status()
        
        # 3. 获取所有股票数据
        logger.info("\n[3/5] 开始获取个股数据...")
        all_stocks_data = fetcher.get_all_stocks_data(stocks[:50])  # 先测试50只
        if not all_stocks_data:
            logger.error("获取个股数据失败，程序终止")
            return False
        
        # 4. 计算因子
        logger.info("\n[4/5] 开始计算各股票因子...")
        all_factors = []
        for code, stock_data in all_stocks_data.items():
            factors = calculator.calculate_all_factors(stock_data)
            if factors:
                all_factors.append(factors)
        
        if not all_factors:
            logger.error("因子计算失败，程序终止")
            return False
        
        logger.info(f"成功计算 {len(all_factors)} 只股票的因子")
        
        # 转换为DataFrame并计算综合得分
        factors_df = pd.DataFrame(all_factors)
        factors_df = calculator.calculate_factor_score(factors_df)
        
        # 保存因子数据
        factors_file = os.path.join(DATA_DIR, f'factors_{datetime.now().strftime("%Y%m%d")}.csv')
        factors_df.to_csv(factors_file, index=False, encoding='utf-8-sig')
        logger.info(f"因子数据已保存到: {factors_file}")
        
        # 5. 生成报告
        logger.info("\n[5/5] 开始生成投研日报...")
        md_report = generator.generate_markdown_report(factors_df, market_data)
        
        # 保存Markdown报告
        md_path = generator.save_report(md_report)
        
        # 保存Excel详细报告
        excel_path = generator.generate_excel_report(factors_df)
        
        # 统计耗时
        elapsed_time = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info("分析完成！")
        logger.info(f"总耗时: {elapsed_time:.2f} 秒")
        logger.info(f"分析股票数量: {len(factors_df)}")
        logger.info(f"Markdown报告: {md_path}")
        logger.info(f"Excel报告: {excel_path}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"分析过程中发生错误: {e}", exc_info=True)
        return False


def run_once():
    """立即运行一次分析"""
    setup_logging()
    success = run_analysis()
    if success:
        print("\n✅ 分析完成！请查看 output 目录下的报告文件。")
    else:
        print("\n❌ 分析失败，请查看日志文件了解详情。")
    return success


def run_scheduled():
    """运行定时任务模式"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"启动定时任务模式，每天 {REPORT_TIME} 自动执行分析")
    logger.info("按 Ctrl+C 停止程序")
    
    # 设置定时任务
    schedule.every().day.at(REPORT_TIME).do(run_analysis)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info("收到停止信号，程序退出")
        print("\n程序已停止")


def main():
    """主函数"""
    print("=" * 60)
    print("    沪深300晨间多因子投研系统")
    print("=" * 60)
    print()
    
    # 确保输出目录存在
    for directory in [OUTPUT_DIR, DATA_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'once':
            run_once()
        elif mode == 'scheduled':
            run_scheduled()
        elif mode == 'test':
            # 测试模式，只分析少量股票
            setup_logging()
            logger = logging.getLogger(__name__)
            logger.info("运行测试模式...")
            run_analysis()
        else:
            print("使用方法:")
            print("  python main.py once      # 立即执行一次分析")
            print("  python main.py scheduled # 启动定时任务模式")
            print("  python main.py test      # 测试模式")
    else:
        # 默认显示帮助信息
        print("使用方法:")
        print("  python main.py once      # 立即执行一次分析")
        print("  python main.py scheduled # 启动定时任务模式")
        print()
        print("提示：首次运行建议先执行 'python main.py once' 测试系统是否正常")


if __name__ == '__main__':
    main()

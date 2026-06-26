#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投放数据分析技能 - ClawHub优化版
简化接口，便于通过ClawHub运行
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# 导入自定义模块
from data_processor import DataProcessor
from calculator import MetricCalculator
from reporter import ReportGenerator
from config import CONFIG

def main():
    """主函数 - ClawHub优化版"""
    print("🎯 ClawHub版投放数据分析技能")
    print("=" * 50)
    
    # 使用环境变量或默认配置
    date_range = os.environ.get('TOUFANG_DATE_RANGE', '2026-01-01:2026-01-31')
    data_dir = os.environ.get('TOUFANG_DATA_DIR', CONFIG['DEFAULT_DATA_DIR'])
    output_dir = os.environ.get('TOUFANG_OUTPUT_DIR', CONFIG['DEFAULT_OUTPUT_DIR'])
    
    print(f"📅 日期范围: {date_range}")
    print(f"📁 数据目录: {data_dir}")
    print(f"💾 输出目录: {output_dir}")
    
    try:
        # 初始化处理器
        processor = DataProcessor(data_dir)
        
        # 自动识别数据文件
        print("\n📁 正在识别数据文件...")
        super_files, taobao_files, financial_files = processor.auto_detect_files()
        
        print(f"✅ 找到 {len(super_files)} 个超级直播文件")
        print(f"✅ 找到 {len(taobao_files)} 个淘宝直播文件")
        print(f"✅ 找到 {len(financial_files)} 个财务文件")
        
        # 读取数据
        print("\n📊 正在读取数据...")
        super_df = processor.read_data(super_files, "超级直播")
        taobao_df = processor.read_data(taobao_files, "淘宝直播")
        financial_df = processor.read_data(financial_files, "财务")
        
        print(f"✅ 成功读取super数据，形状: {super_df.shape}")
        print(f"✅ 成功读取taobao数据，形状: {taobao_df.shape}")
        print(f"✅ 成功读取financial数据，形状: {financial_df.shape}")
        
        # 数据预处理
        print("\n🔄 正在进行数据预处理...")
        super_df = processor.preprocess_data(super_df, "super")
        taobao_df = processor.preprocess_data(taobao_df, "taobao")
        financial_df = processor.preprocess_data(financial_df, "financial")
        
        print(f"✅ super数据预处理完成，形状: {super_df.shape}")
        print(f"✅ taobao数据预处理完成，形状: {taobao_df.shape}")
        print(f"✅ financial数据预处理完成，形状: {financial_df.shape}")
        
        # 计算指标
        print("\n🧮 正在计算指标...")
        calculator = MetricCalculator()
        metrics_result = {}
        
        if not super_df.empty:
            metrics_result['super'] = calculator.calculate_super_metrics(super_df)
        if not taobao_df.empty:
            metrics_result['taobao'] = calculator.calculate_taobao_metrics(taobao_df)
        if not financial_df.empty:
            metrics_result['financial'] = calculator.calculate_financial_metrics(financial_df)
        
        # 生成报告
        print("\n📝 正在生成报告...")
        reporter = ReportGenerator(output_dir)
        html_report = reporter.generate_html_report(
            super_df, taobao_df, financial_df, metrics_result, date_range
        )
        
        print(f"✅ HTML报告已生成: {html_report}")
        
        # 生成CSV报告
        csv_files = reporter.generate_csv_reports(metrics_result, date_range)
        for csv_file in csv_files:
            print(f"✅ CSV报告已生成: {csv_file}")
        
        print("\n🎉 投放数据分析完成!")
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
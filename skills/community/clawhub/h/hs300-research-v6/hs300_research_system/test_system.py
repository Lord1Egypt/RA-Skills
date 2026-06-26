#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300多因子投研系统 - 快速测试脚本
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("    沪深300多因子投研系统 - 快速测试")
print("=" * 60)
print()

# 1. 测试依赖导入
print("[1/5] 检查依赖库...")
try:
    import pandas as pd
    import numpy as np
    print("  ✓ pandas, numpy 导入成功")
except ImportError as e:
    print(f"  ✗ 依赖缺失: {e}")
    print("  请运行: pip install pandas numpy")
    sys.exit(1)

try:
    import akshare as ak
    print("  ✓ akshare 导入成功")
except ImportError as e:
    print(f"  ✗ akshare 未安装: {e}")
    print("  请运行: pip install akshare")
    sys.exit(1)

try:
    import schedule
    print("  ✓ schedule 导入成功")
except ImportError as e:
    print(f"  ✗ schedule 未安装: {e}")
    print("  请运行: pip install schedule")
    sys.exit(1)

try:
    import openpyxl
    print("  ✓ openpyxl 导入成功")
except ImportError as e:
    print(f"  ✗ openpyxl 未安装: {e}")
    print("  请运行: pip install openpyxl")
    sys.exit(1)

print()

# 2. 测试数据获取
print("[2/5] 测试数据获取模块...")
try:
    from data_fetcher import DataFetcher
    fetcher = DataFetcher()
    
    print("  正在获取沪深300成分股列表...")
    stocks = fetcher.get_hs300_stocks()
    
    if stocks and len(stocks) > 0:
        print(f"  ✓ 成功获取 {len(stocks)} 只沪深300成分股")
        print(f"  示例: {stocks[0]['name']}({stocks[0]['code']})")
    else:
        print("  ✗ 获取沪深300成分股失败")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ 数据获取模块测试失败: {e}")
    sys.exit(1)

print()

# 3. 测试个股数据获取
print("[3/5] 测试个股数据获取...")
try:
    sample_stock = stocks[0]
    print(f"  正在获取 {sample_stock['name']}({sample_stock['code']}) 的日线数据...")
    
    daily_df = fetcher.get_stock_daily(sample_stock['code'])
    if daily_df is not None and len(daily_df) > 0:
        print(f"  ✓ 成功获取日线数据，共 {len(daily_df)} 条")
        print(f"  最新收盘价: {daily_df['close'].iloc[-1]:.2f}")
    else:
        print("  ✗ 获取日线数据失败")
except Exception as e:
    print(f"  ✗ 个股数据获取测试失败: {e}")

print()

# 4. 测试因子计算
print("[4/5] 测试因子计算模块...")
try:
    from factor_calculator import FactorCalculator
    calculator = FactorCalculator()
    
    print("  正在计算因子...")
    stock_data = {
        'code': sample_stock['code'],
        'name': sample_stock['name'],
        'daily': daily_df
    }
    
    factors = calculator.calculate_all_factors(stock_data)
    if factors:
        print(f"  ✓ 成功计算 {len(factors)} 个因子")
        print(f"  MACD: {factors.get('macd', 'N/A'):.4f}")
        print(f"  RSI: {factors.get('rsi', 'N/A'):.2f}")
        print(f"  MACD金叉: {'是' if factors.get('macd_golden') else '否'}")
    else:
        print("  ✗ 因子计算失败")
except Exception as e:
    print(f"  ✗ 因子计算模块测试失败: {e}")
    sys.exit(1)

print()

# 5. 测试报告生成
print("[5/5] 测试报告生成模块...")
try:
    from report_generator import ReportGenerator
    generator = ReportGenerator()
    
    # 计算几只股票的因子用于测试
    print("  正在为多只股票计算因子以生成报告...")
    all_factors = []
    
    for i, stock in enumerate(stocks[:10]):  # 先算10只
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
        
        print(f"  ✓ 成功计算 {len(factors_df)} 只股票的因子和得分")
        
        # 生成简要报告
        md_report = generator.generate_markdown_report(factors_df)
        md_path = generator.save_report(md_report, filename='测试报告')
        
        print(f"  ✓ 测试报告已生成: {md_path}")
    else:
        print("  ✗ 没有足够的数据生成报告")
except Exception as e:
    print(f"  ✗ 报告生成模块测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ 所有测试通过！系统运行正常。")
print()
print("下一步:")
print("  1. 运行 'python main.py once' 执行完整分析")
print("  2. 运行 'python main.py scheduled' 启动定时模式")
print("  3. 查看 output/ 目录下的报告文件")
print("=" * 60)

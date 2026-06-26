#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业对比脚本 - 完整版
作者：滚滚家族 🌪️
版本：1.0.0
"""

import sys
import os

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}{'━' * 60}{Colors.ENDC}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠️ {text}{Colors.ENDC}")

def compare_companies(stocks, industry=''):
    """
    多公司对比
    """
    print_header(f"📈 行业对比 - {industry or '自定义'}")
    
    print(f"{Colors.BOLD}【对比公司】{Colors.ENDC}")
    for stock in stocks:
        print(f"• {stock}")
    
    print(f"\n{Colors.BOLD}【估值对比】{Colors.ENDC}")
    print(f"{'公司':<15} {'PE':<10} {'PB':<10} {'PS':<10}")
    print(f"{'-' * 45}")
    
    # 示例数据
    data = {
        "600519.SH": {"pe": 35.2, "pb": 12.8, "ps": 15.6},
        "000858.SZ": {"pe": 28.5, "pb": 8.5, "ps": 10.2},
        "002304.SZ": {"pe": 22.1, "pb": 5.2, "ps": 6.8},
    }
    
    for stock in stocks:
        if stock in data:
            d = data[stock]
            print(f"{stock:<15} {d['pe']:>8.1f}x {d['pb']:>8.1f}x {d['ps']:>8.1f}x")
    
    print(f"\n{Colors.BOLD}【盈利能力对比】{Colors.ENDC}")
    print(f"{'公司':<15} {'ROE':<10} {'净利率':<10} {'毛利率':<10}")
    print(f"{'-' * 45}")
    
    profit_data = {
        "600519.SH": {"roe": 30.2, "net_margin": 52.5, "gross_margin": 92.1},
        "000858.SZ": {"roe": 25.8, "net_margin": 38.2, "gross_margin": 78.5},
        "002304.SZ": {"roe": 18.5, "net_margin": 28.5, "gross_margin": 65.2},
    }
    
    for stock in stocks:
        if stock in profit_data:
            d = profit_data[stock]
            print(f"{stock:<15} {d['roe']:>8.1f}% {d['net_margin']:>8.1f}% {d['gross_margin']:>8.1f}%")
    
    print(f"\n{Colors.BOLD}【成长能力对比】{Colors.ENDC}")
    print(f"{'公司':<15} {'收入增长':<10} {'利润增长':<10} {'资产增长':<10}")
    print(f"{'-' * 45}")
    
    growth_data = {
        "600519.SH": {"rev_growth": 18.2, "profit_growth": 20.5, "asset_growth": 15.8},
        "000858.SZ": {"rev_growth": 15.5, "profit_growth": 18.2, "asset_growth": 12.5},
        "002304.SZ": {"rev_growth": 10.2, "profit_growth": 12.5, "asset_growth": 8.5},
    }
    
    for stock in stocks:
        if stock in growth_data:
            d = growth_data[stock]
            print(f"{stock:<15} {d['rev_growth']:>8.1f}% {d['profit_growth']:>8.1f}% {d['asset_growth']:>8.1f}%")
    
    print(f"\n{Colors.BOLD}【行业地位】{Colors.ENDC}")
    print(f"贵州茅台：{Colors.OKGREEN}⭐⭐⭐⭐⭐ 行业龙头{Colors.ENDC}")
    print(f"五粮液：{Colors.OKGREEN}⭐⭐⭐⭐☆ 行业领先{Colors.ENDC}")
    print(f"洋河股份：{Colors.OKBLUE}⭐⭐⭐☆☆ 行业中游{Colors.ENDC}")
    
    print_success("行业对比完成！")

def industry_ranking(stock_code, industry=''):
    """
    行业地位评估
    """
    print_header(f"📈 行业地位评估 - {stock_code}")
    
    print(f"{Colors.BOLD}【行业排名】{Colors.ENDC}")
    print(f"行业：{industry or '白酒'}")
    print(f"市场份额：35.2%（行业第 1）")
    print(f"营收规模：行业第 1")
    print(f"利润规模：行业第 1")
    print(f"ROE：行业第 1")
    
    print(f"\n{Colors.BOLD}【竞争优势】{Colors.ENDC}")
    print(f"✅ 品牌优势：极强")
    print(f"✅ 渠道优势：强")
    print(f"✅ 产品优势：极强")
    print(f"✅ 成本优势：强")
    
    print(f"\n{Colors.BOLD}【综合评估】{Colors.ENDC}")
    print(f"{Colors.OKGREEN}⭐⭐⭐⭐⭐ 行业龙头{Colors.ENDC}")
    
    print_success("行业地位评估完成！")

def main():
    """测试函数"""
    # 多公司对比测试
    compare_companies(
        stocks=["600519.SH", "000858.SZ", "002304.SZ"],
        industry="白酒"
    )
    
    print("\n" + "="*60 + "\n")
    
    # 行业地位评估测试
    industry_ranking("600519.SH", "白酒")

if __name__ == '__main__':
    main()

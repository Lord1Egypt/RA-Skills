#!/usr/bin/env python3
"""
资产配置计算器

基于马尔基尔生命周期理论，计算资产配置比例。

使用方法：
    python allocation-calculator.py --age 35 --risk balanced --assets 1000000

输出：
    JSON 格式的配置方案
"""

import argparse
import json


def calculate_allocation(age, risk_tolerance, total_assets):
    """
    计算资产配置比例
    
    Args:
        age: 年龄
        risk_tolerance: 风险偏好（conservative/balanced/aggressive）
        total_assets: 总资产（元）
    
    Returns:
        dict: 配置方案
    """
    # 基础股票比例（100 - 年龄）
    base_stock_ratio = 100 - age
    
    # 风险调整
    if risk_tolerance == 'conservative':
        adjustment = -10
    elif risk_tolerance == 'aggressive':
        adjustment = 10
    else:  # balanced
        adjustment = 0
    
    # 最终股票比例
    stock_ratio = max(20, min(90, base_stock_ratio + adjustment))
    
    # 债券比例
    bond_ratio = 100 - stock_ratio
    
    # 股票细分（国内 60%，国际 40%）
    domestic_stock_ratio = stock_ratio * 0.6
    international_stock_ratio = stock_ratio * 0.4
    
    # 债券细分（国债 60%，信用债 40%）
    government_bond_ratio = bond_ratio * 0.6
    corporate_bond_ratio = bond_ratio * 0.4
    
    # 计算金额
    allocation = {
        'stocks': {
            'total': {
                'ratio': stock_ratio,
                'amount': total_assets * stock_ratio / 100
            },
            'domestic': {
                'ratio': domestic_stock_ratio,
                'amount': total_assets * domestic_stock_ratio / 100,
                'recommendation': '沪深 300ETF'
            },
            'international': {
                'ratio': international_stock_ratio,
                'amount': total_assets * international_stock_ratio / 100,
                'recommendation': '标普 500ETF'
            }
        },
        'bonds': {
            'total': {
                'ratio': bond_ratio,
                'amount': total_assets * bond_ratio / 100
            },
            'government': {
                'ratio': government_bond_ratio,
                'amount': total_assets * government_bond_ratio / 100,
                'recommendation': '国债 ETF'
            },
            'corporate': {
                'ratio': corporate_bond_ratio,
                'amount': total_assets * corporate_bond_ratio / 100,
                'recommendation': '信用债基金'
            }
        },
        'cash': {
            'ratio': 5,
            'amount': total_assets * 0.05,
            'recommendation': '货币基金'
        },
        'alternatives': {
            'ratio': 5,
            'amount': total_assets * 0.05,
            'recommendation': '黄金 ETF/REITs'
        }
    }
    
    return allocation


def format_output(allocation):
    """格式化输出"""
    output = []
    output.append("【资产配置方案】")
    output.append("")
    output.append(f"股票：{allocation['stocks']['total']['ratio']:.1f}% ({allocation['stocks']['total']['amount']:,.0f}元)")
    output.append(f"  - 国内指数：{allocation['stocks']['domestic']['ratio']:.1f}% ({allocation['stocks']['domestic']['amount']:,.0f}元，{allocation['stocks']['domestic']['recommendation']})")
    output.append(f"  - 国际指数：{allocation['stocks']['international']['ratio']:.1f}% ({allocation['stocks']['international']['amount']:,.0f}元，{allocation['stocks']['international']['recommendation']})")
    output.append("")
    output.append(f"债券：{allocation['bonds']['total']['ratio']:.1f}% ({allocation['bonds']['total']['amount']:,.0f}元)")
    output.append(f"  - 国债：{allocation['bonds']['government']['ratio']:.1f}% ({allocation['bonds']['government']['amount']:,.0f}元，{allocation['bonds']['government']['recommendation']})")
    output.append(f"  - 信用债：{allocation['bonds']['corporate']['ratio']:.1f}% ({allocation['bonds']['corporate']['amount']:,.0f}元，{allocation['bonds']['corporate']['recommendation']})")
    output.append("")
    output.append(f"现金：{allocation['cash']['ratio']}% ({allocation['cash']['amount']:,.0f}元，{allocation['cash']['recommendation']})")
    output.append(f"另类：{allocation['alternatives']['ratio']}% ({allocation['alternatives']['amount']:,.0f}元，{allocation['alternatives']['recommendation']})")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='资产配置计算器')
    parser.add_argument('--age', type=int, required=True, help='年龄')
    parser.add_argument('--risk', type=str, required=True, 
                       choices=['conservative', 'balanced', 'aggressive'],
                       help='风险偏好')
    parser.add_argument('--assets', type=float, required=True, help='总资产（元）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    allocation = calculate_allocation(args.age, args.risk, args.assets)
    
    if args.json:
        print(json.dumps(allocation, indent=2, ensure_ascii=False))
    else:
        print(format_output(allocation))


if __name__ == '__main__':
    main()

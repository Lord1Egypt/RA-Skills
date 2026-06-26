#!/usr/bin/env python3
"""
资产配置师 - 基于马尔基尔《漫步华尔街》的生命周期配置

无需外部数据，基于年龄和风险承受能力
"""

import sys
import os
from datetime import datetime


def calculate_stock_bond_allocation(age: int, risk_tolerance: str = 'moderate') -> dict:
    """
    计算股票/债券配置比例
    
    Args:
        age: 年龄
        risk_tolerance: 风险承受能力（conservative/moderate/aggressive）
    
    Returns:
        配置比例字典
    """
    # 基础公式：股票比例 = 110 - 年龄
    base_stock = 110 - age
    
    # 根据风险承受能力调整
    adjustments = {
        'conservative': -10,
        'moderate': 0,
        'aggressive': +10,
    }
    
    adjustment = adjustments.get(risk_tolerance, 0)
    stock_pct = max(0, min(100, base_stock + adjustment))
    bond_pct = 100 - stock_pct
    
    return {
        'stock_pct': stock_pct,
        'bond_pct': bond_pct,
        'formula': f'股票比例 = 110 - 年龄 ({age}) {"+" if adjustment > 0 else ""}{adjustment:+d} (风险调整) = {stock_pct}%',
    }


def lifecycle_allocation(age: int) -> dict:
    """
    生命周期配置建议
    
    Args:
        age: 年龄
    
    Returns:
        配置建议字典
    """
    if age < 30:
        stage = '积累期早期'
        strategy = '积极成长'
        stock_range = '80-90%'
        advice = '最大化股票配置，利用时间优势'
    elif age < 40:
        stage = '积累期'
        strategy = '成长为主'
        stock_range = '70-80%'
        advice = '保持高股票配置，定期定额投资'
    elif age < 50:
        stage = '巩固期'
        strategy = '平衡成长'
        stock_range = '60-70%'
        advice = '开始降低风险，增加债券配置'
    elif age < 60:
        stage = '准备退休期'
        strategy = '保守成长'
        stock_range = '50-60%'
        advice = '保护已积累财富，降低波动'
    elif age < 70:
        stage = '退休早期'
        strategy = '收入为主'
        stock_range = '40-50%'
        advice = '产生稳定收入，适度成长'
    else:
        stage = '退休后期'
        strategy = '保值为主'
        stock_range = '30-40%'
        advice = '保护本金，对抗通胀'
    
    return {
        'stage': stage,
        'strategy': strategy,
        'stock_range': stock_range,
        'advice': advice,
    }


def generate_portfolio(age: int, risk_tolerance: str = 'moderate') -> dict:
    """
    生成完整投资组合建议
    
    Args:
        age: 年龄
        risk_tolerance: 风险承受能力
    
    Returns:
        投资组合建议字典
    """
    result = {
        'age': age,
        'risk_tolerance': risk_tolerance,
        'timestamp': datetime.now().isoformat(),
    }
    
    # 计算股债比例
    result['allocation'] = calculate_stock_bond_allocation(age, risk_tolerance)
    
    # 生命周期建议
    result['lifecycle'] = lifecycle_allocation(age)
    
    # 具体配置建议
    result['portfolio'] = {
        'domestic_stocks': f"{result['allocation']['stock_pct'] * 0.6:.0f}%",
        'international_stocks': f"{result['allocation']['stock_pct'] * 0.4:.0f}%",
        'domestic_bonds': f"{result['allocation']['bond_pct'] * 0.7:.0f}%",
        'international_bonds': f"{result['allocation']['bond_pct'] * 0.3:.0f}%",
    }
    
    # 再平衡建议
    result['rebalancing'] = {
        'frequency': '每年 1 次',
        'threshold': '偏离目标配置±5%时调整',
        'method': '卖出高估资产，买入低估资产',
    }
    
    # 风险提示
    result['risks'] = [
        '市场波动风险',
        '通胀风险',
        '利率风险',
        '汇率风险（国际配置）',
    ]
    
    return result


def print_portfolio(result: dict) -> None:
    """打印投资组合建议"""
    print("="*60)
    print("💼 资产配置师")
    print("="*60)
    
    print(f"\n📋 基本信息")
    print(f"   年龄：{result['age']}岁")
    print(f"   风险承受能力：{result['risk_tolerance']}")
    
    print(f"\n📊 生命周期定位")
    print(f"   阶段：{result['lifecycle']['stage']}")
    print(f"   策略：{result['lifecycle']['strategy']}")
    print(f"   建议股票比例：{result['lifecycle']['stock_range']}")
    print(f"   建议：{result['lifecycle']['advice']}")
    
    print(f"\n📈 资产配置比例")
    print(f"   {result['allocation']['formula']}")
    print(f"   股票：{result['allocation']['stock_pct']}%")
    print(f"   债券：{result['allocation']['bond_pct']}%")
    
    print(f"\n🎯 具体配置")
    for asset, pct in result['portfolio'].items():
        asset_name = {
            'domestic_stocks': '国内股票',
            'international_stocks': '国际股票',
            'domestic_bonds': '国内债券',
            'international_bonds': '国际债券',
        }.get(asset, asset)
        print(f"   {asset_name}: {pct}")
    
    print(f"\n🔄 再平衡策略")
    print(f"   频率：{result['rebalancing']['frequency']}")
    print(f"   阈值：{result['rebalancing']['threshold']}")
    print(f"   方法：{result['rebalancing']['method']}")
    
    print(f"\n⚠️  风险提示")
    for risk in result['risks']:
        print(f"   • {risk}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 根据年龄和风险承受能力调整配置")
    print(f"   2. 定期定额投资，降低择时风险")
    print(f"   3. 每年再平衡，保持目标配置")
    print(f"   4. 长期坚持，不要频繁调整")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 allocate-assets.py <年龄> [风险承受能力]")
        print("示例：python3 allocate-assets.py 35 moderate")
        print("风险承受能力：conservative（保守）/ moderate（中等）/ aggressive（积极）")
        return 1
    
    try:
        age = int(sys.argv[1])
    except ValueError:
        print("错误：年龄必须是数字")
        return 1
    
    risk_tolerance = sys.argv[2] if len(sys.argv) > 2 else 'moderate'
    
    if risk_tolerance not in ['conservative', 'moderate', 'aggressive']:
        print(f"错误：风险承受能力必须是 conservative/moderate/aggressive 之一")
        return 1
    
    result = generate_portfolio(age, risk_tolerance)
    print_portfolio(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
组合设计师 - 基于耶鲁模式的组合设计

无需外部数据，基于风险承受能力生成配置方案
"""

import sys
import os
from datetime import datetime


def yale_model_allocation(risk_profile: str = 'moderate') -> dict:
    """
    耶鲁模式配置
    
    Args:
        risk_profile: 风险档案（conservative/moderate/aggressive）
    
    Returns:
        配置字典
    """
    # 标准耶鲁模式
    base_allocation = {
        'us_stocks': 18,
        'international_stocks': 23,
        'bonds': 15,
        'real_estate': 21,
        'alternatives': 23,
    }
    
    # 根据风险档案调整
    adjustments = {
        'conservative': {
            'us_stocks': -5,
            'international_stocks': -5,
            'bonds': +10,
            'real_estate': 0,
            'alternatives': 0,
        },
        'moderate': {
            'us_stocks': 0,
            'international_stocks': 0,
            'bonds': 0,
            'real_estate': 0,
            'alternatives': 0,
        },
        'aggressive': {
            'us_stocks': +5,
            'international_stocks': +5,
            'bonds': -10,
            'real_estate': 0,
            'alternatives': 0,
        },
    }
    
    adj = adjustments.get(risk_profile, adjustments['moderate'])
    
    result = {}
    for key in base_allocation:
        result[key] = max(0, base_allocation[key] + adj.get(key, 0))
    
    # 确保总和为 100%
    total = sum(result.values())
    if total != 100:
        # 调整债券比例使总和为 100
        result['bonds'] += (100 - total)
    
    return result


def simplified_allocation(risk_profile: str = 'moderate') -> dict:
    """
    简化版配置（适合个人投资者）
    
    Args:
        risk_profile: 风险档案
    
    Returns:
        配置字典
    """
    allocations = {
        'conservative': {
            'stocks': 40,
            'bonds': 50,
            'cash': 10,
            'alternatives': 0,
        },
        'moderate': {
            'stocks': 60,
            'bonds': 35,
            'cash': 5,
            'alternatives': 0,
        },
        'aggressive': {
            'stocks': 80,
            'bonds': 15,
            'cash': 5,
            'alternatives': 0,
        },
    }
    
    return allocations.get(risk_profile, allocations['moderate'])


def generate_portfolio(risk_profile: str = 'moderate', use_yale: bool = False) -> dict:
    """
    生成完整投资组合
    
    Args:
        risk_profile: 风险档案
        use_yale: 是否使用耶鲁模式
    
    Returns:
        投资组合字典
    """
    result = {
        'risk_profile': risk_profile,
        'model': 'Yale' if use_yale else 'Simplified',
        'timestamp': datetime.now().isoformat(),
    }
    
    if use_yale:
        result['allocation'] = yale_model_allocation(risk_profile)
        result['description'] = '耶鲁模式（机构级配置）'
    else:
        result['allocation'] = simplified_allocation(risk_profile)
        result['description'] = '简化模式（适合个人）'
    
    # 具体工具建议
    result['tools'] = {
        'stocks': {
            'domestic': '沪深 300ETF / 中证 500ETF',
            'international': '标普 500ETF / 纳斯达克 ETF',
        },
        'bonds': {
            'domestic': '国债 ETF / 信用债基金',
            'international': '全球债券 ETF',
        },
        'alternatives': {
            'real_estate': 'REITs / 房地产基金',
            'gold': '黄金 ETF',
            'commodities': '商品 ETF',
        },
    }
    
    # 再平衡建议
    result['rebalancing'] = {
        'frequency': '每年 1 次',
        'threshold': '偏离±5%时调整',
    }
    
    # 风险提示
    result['risks'] = [
        '市场风险',
        '利率风险',
        '汇率风险',
        '流动性风险',
    ]
    
    return result


def print_portfolio(result: dict) -> None:
    """打印投资组合"""
    print("="*60)
    print("📐 组合设计师")
    print("="*60)
    
    print(f"\n📋 配置模型")
    print(f"   风险档案：{result['risk_profile']}")
    print(f"   模型：{result['model']} - {result['description']}")
    
    print(f"\n📊 资产配置")
    for asset, pct in result['allocation'].items():
        asset_name = {
            'us_stocks': '美国股票',
            'international_stocks': '国际股票',
            'stocks': '股票',
            'bonds': '债券',
            'real_estate': '房地产',
            'alternatives': '另类投资',
            'cash': '现金',
        }.get(asset, asset)
        print(f"   {asset_name}: {pct}%")
    
    print(f"\n🛠️ 工具建议")
    for category, tools in result['tools'].items():
        cat_name = {
            'stocks': '股票',
            'bonds': '债券',
            'alternatives': '另类投资',
        }.get(category, category)
        print(f"\n   {cat_name}:")
        for subcat, tool in tools.items():
            print(f"     • {subcat}: {tool}")
    
    print(f"\n🔄 再平衡")
    print(f"   频率：{result['rebalancing']['frequency']}")
    print(f"   阈值：{result['rebalancing']['threshold']}")
    
    print(f"\n⚠️  风险提示")
    for risk in result['risks']:
        print(f"   • {risk}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 选择适合的风险档案")
    print(f"   2. 使用 ETF 或基金实现配置")
    print(f"   3. 定期再平衡")
    print(f"   4. 长期坚持，不要频繁调整")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 design-portfolio.py <风险档案> [--yale]")
        print("示例：python3 design-portfolio.py moderate")
        print("       python3 design-portfolio.py aggressive --yale")
        print("风险档案：conservative / moderate / aggressive")
        return 1
    
    risk_profile = sys.argv[1]
    use_yale = '--yale' in sys.argv
    
    if risk_profile not in ['conservative', 'moderate', 'aggressive']:
        print(f"错误：风险档案必须是 conservative/moderate/aggressive 之一")
        return 1
    
    result = generate_portfolio(risk_profile, use_yale)
    print_portfolio(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

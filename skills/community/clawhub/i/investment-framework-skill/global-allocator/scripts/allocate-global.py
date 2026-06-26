#!/usr/bin/env python3
"""
全球配置师 - 基于达斯特的全球分散配置

无需外部数据，基于地理区域生成配置方案
"""

import sys
import os
from datetime import datetime


def global_allocation(home_country: str = 'China') -> dict:
    """
    全球资产配置
    
    Args:
        home_country: 本国（China/US/Other）
    
    Returns:
        配置字典
    """
    # 基于市值权重的全球配置
    global_market_cap = {
        'us': 55,
        'china': 10,
        'europe': 15,
        'japan': 6,
        'pacific': 8,
        'emerging': 6,
    }
    
    # 本土偏好调整
    if home_country == 'China':
        allocation = {
            'china': 40,  # 本土偏好
            'us': 35,
            'europe': 10,
            'japan': 5,
            'pacific': 5,
            'emerging': 5,
        }
    elif home_country == 'US':
        allocation = {
            'us': 50,  # 本土偏好
            'china': 5,
            'europe': 15,
            'japan': 8,
            'pacific': 10,
            'emerging': 12,
        }
    else:
        allocation = global_market_cap.copy()
    
    return allocation


def rebalancing_strategy(allocation: dict) -> dict:
    """
    再平衡策略
    
    Args:
        allocation: 当前配置
    
    Returns:
        再平衡策略字典
    """
    return {
        'methods': [
            '阈值再平衡：偏离目标±5% 时调整',
            '定期再平衡：每季度/每年检查',
            '混合再平衡：每季度检查，偏离>5% 时调整',
        ],
        'recommendation': '混合再平衡（灵活且成本可控）',
        'tax_efficiency': '优先在免税账户再平衡',
    }


def generate_portfolio(home_country: str = 'China') -> dict:
    """
    生成全球投资组合
    
    Args:
        home_country: 本国
    
    Returns:
        投资组合字典
    """
    result = {
        'home_country': home_country,
        'timestamp': datetime.now().isoformat(),
    }
    
    # 地理配置
    result['geographic_allocation'] = global_allocation(home_country)
    
    # 再平衡策略
    result['rebalancing'] = rebalancing_strategy(result['geographic_allocation'])
    
    # 工具建议
    result['tools'] = {
        'china': '沪深 300ETF / 中证 500ETF',
        'us': '标普 500ETF / 纳斯达克 ETF',
        'europe': '欧洲 ETF / 斯托克 50ETF',
        'japan': '日经 225ETF',
        'pacific': '亚太 ETF',
        'emerging': '新兴市场 ETF',
    }
    
    # 汇率对冲建议
    result['currency_hedging'] = {
        'recommendation': '适度对冲',
        'methods': [
            '货币对冲 ETF',
            '远期合约',
            '自然对冲（海外收入）',
        ],
    }
    
    # 风险提示
    result['risks'] = [
        '汇率风险',
        '政治风险',
        '流动性风险',
        '信息不对称风险',
    ]
    
    return result


def print_portfolio(result: dict) -> None:
    """打印投资组合"""
    print("="*60)
    print("🌍 全球配置师")
    print("="*60)
    
    print(f"\n📋 基本信息")
    print(f"   本国：{result['home_country']}")
    
    print(f"\n📊 地理配置")
    region_names = {
        'china': '中国',
        'us': '美国',
        'europe': '欧洲',
        'japan': '日本',
        'pacific': '亚太',
        'emerging': '新兴市场',
    }
    
    for region, pct in result['geographic_allocation'].items():
        name = region_names.get(region, region)
        print(f"   {name}: {pct}%")
    
    print(f"\n🛠️ 工具建议")
    for region, tool in result['tools'].items():
        name = region_names.get(region, region)
        print(f"   {name}: {tool}")
    
    print(f"\n🔄 再平衡策略")
    for method in result['rebalancing']['methods']:
        print(f"   • {method}")
    print(f"   推荐：{result['rebalancing']['recommendation']}")
    
    print(f"\n💱 汇率对冲")
    print(f"   建议：{result['currency_hedging']['recommendation']}")
    for method in result['currency_hedging']['methods']:
        print(f"   • {method}")
    
    print(f"\n⚠️  风险提示")
    for risk in result['risks']:
        print(f"   • {risk}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 根据本国选择配置比例")
    print(f"   2. 使用 ETF 实现全球分散")
    print(f"   3. 考虑汇率对冲")
    print(f"   4. 定期再平衡")


def main():
    """主函数"""
    home_country = sys.argv[1] if len(sys.argv) > 1 else 'China'
    
    if home_country not in ['China', 'US', 'Other']:
        print(f"错误：本国必须是 China/US/Other 之一")
        return 1
    
    result = generate_portfolio(home_country)
    print_portfolio(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

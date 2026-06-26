#!/usr/bin/env python3
"""
数据驱动投资 - 基于吴军的数据驱动思维

无需外部数据，基于数据分析方法
"""

import sys
import os
from datetime import datetime


def data_driven_framework() -> dict:
    """
    数据驱动投资框架
    
    Returns:
        框架字典
    """
    return {
        'principles': [
            '用数据说话，而非直觉',
            '量化分析，减少主观判断',
            '持续跟踪，动态调整',
            '大数定律，长期获胜',
        ],
        'data_sources': [
            '财报数据（营收、利润、现金流）',
            '市场数据（价格、成交量、估值）',
            '行业数据（增长率、渗透率、集中度）',
            '另类数据（搜索指数、社交媒体）',
        ],
        'analysis_methods': [
            '趋势分析（同比、环比）',
            '对比分析（同行、历史）',
            '归因分析（驱动因素）',
            '预测分析（模型推演）',
        ],
    }


def quantitative_checklist() -> list:
    """
    量化检查清单
    
    Returns:
        检查清单
    """
    return [
        {
            'category': '成长性',
            'metrics': [
                '营收增长率 > 15%',
                '利润增长率 > 15%',
                '连续 3 年增长',
            ],
        },
        {
            'category': '盈利性',
            'metrics': [
                'ROE > 15%',
                '毛利率 > 30%',
                '净利率 > 10%',
            ],
        },
        {
            'category': '健康度',
            'metrics': [
                '负债率 < 50%',
                '经营现金流为正',
                '自由现金流为正',
            ],
        },
        {
            'category': '估值',
            'metrics': [
                'PE < 行业平均',
                'PEG < 1',
                'PB < 3',
            ],
        },
    ]


def analyze_data_driven(company_name: str) -> dict:
    """
    数据驱动分析
    
    Args:
        company_name: 公司名称
    
    Returns:
        分析结果
    """
    result = {
        'company': company_name,
        'timestamp': datetime.now().isoformat(),
        'framework': '吴军数据驱动思维',
    }
    
    # 框架
    result['framework_details'] = data_driven_framework()
    
    # 量化检查清单
    result['checklist'] = quantitative_checklist()
    
    # 数据驱动决策流程
    result['process'] = [
        '1. 收集数据（财报、市场、行业）',
        '2. 量化分析（计算指标）',
        '3. 对比分析（同行、历史）',
        '4. 建立模型（估值、预测）',
        '5. 做出决策（买入/卖出/持有）',
        '6. 持续跟踪（定期复盘）',
    ]
    
    # 常见误区
    result['pitfalls'] = [
        '数据过载，忽视本质',
        '过度拟合历史数据',
        '忽视定性因素',
        '数据质量问题',
    ]
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"📊 数据驱动投资：{result['company']}")
    print("="*60)
    
    print(f"\n📋 分析框架")
    print(f"   {result['framework']}")
    
    print(f"\n💡 核心原则")
    for principle in result['framework_details']['principles']:
        print(f"   • {principle}")
    
    print(f"\n📈 数据来源")
    for source in result['framework_details']['data_sources']:
        print(f"   • {source}")
    
    print(f"\n🔍 量化检查清单")
    for item in result['checklist']:
        print(f"\n   {item['category']}")
        for metric in item['metrics']:
            print(f"     • {metric}")
    
    print(f"\n📝 决策流程")
    for step in result['process']:
        print(f"   {step}")
    
    print(f"\n⚠️  常见误区")
    for pitfall in result['pitfalls']:
        print(f"   • {pitfall}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 收集完整数据")
    print(f"   2. 逐项检查量化指标")
    print(f"   3. 对比同行和历史")
    print(f"   4. 基于数据决策")


def main():
    """主函数"""
    company_name = sys.argv[1] if len(sys.argv) > 1 else '目标公司'
    
    result = analyze_data_driven(company_name)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

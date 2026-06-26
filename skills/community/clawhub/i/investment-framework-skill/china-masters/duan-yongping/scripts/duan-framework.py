#!/usr/bin/env python3
"""
段永平投资智慧 - 基于"本分"和长期主义

集成文化分析器和长期检查器
"""

import sys
import os
from datetime import datetime


def duan_investment_framework() -> dict:
    """
    段永平投资框架
    
    Returns:
        框架字典
    """
    return {
        'core_principles': [
            '本分：诚信、专注、做对的事',
            '长期主义：10 年持有思维',
            '能力圈：只投懂的公司',
            '企业文化：文化决定长期竞争力',
        ],
        'selection_criteria': [
            '商业模式简单易懂',
            '企业文化优秀',
            '管理层诚信可靠',
            '有持续竞争优势',
            '价格合理或低估',
        ],
        'duan_quotes': [
            '买股票就是买公司',
            '不懂不做',
            '价格合适的好公司，长期持有',
            '本分就是做对的事，把事情做对',
        ],
    }


def analyze_duan(company_name: str) -> dict:
    """
    段永平投资分析
    
    Args:
        company_name: 公司名称
    
    Returns:
        分析结果
    """
    result = {
        'company': company_name,
        'timestamp': datetime.now().isoformat(),
        'framework': '段永平投资智慧',
    }
    
    # 投资框架
    result['framework_details'] = duan_investment_framework()
    
    # 文化分析维度
    result['culture_check'] = [
        '公司是否诚信对待客户和员工？',
        '公司是否专注于做好产品？',
        '公司是否在能力圈内做事？',
        '管理层是否言行一致？',
    ]
    
    # 长期持有检查
    result['longterm_check'] = [
        '这个生意 10 年后还会存在吗？',
        '护城河会变宽还是变窄？',
        '如果股市关闭 5 年，是否愿意持有？',
        '是否理解这个生意？',
    ]
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"📈 段永平投资智慧：{result['company']}")
    print("="*60)
    
    print(f"\n📋 投资框架")
    print(f"   {result['framework']}")
    
    print(f"\n💡 核心原则")
    for principle in result['framework_details']['core_principles']:
        print(f"   • {principle}")
    
    print(f"\n🎯 选股标准")
    for criterion in result['framework_details']['selection_criteria']:
        print(f"   • {criterion}")
    
    print(f"\n🏛️ 文化检查")
    for q in result['culture_check']:
        print(f"   • {q}")
    
    print(f"\n⏰ 长期持有检查")
    for q in result['longterm_check']:
        print(f"   • {q}")
    
    print(f"\n📝 段永平名言")
    for quote in result['framework_details']['duan_quotes']:
        print(f"   • {quote}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 检查企业文化（本分）")
    print(f"   2. 确认在能力圈内")
    print(f"   3. 10 年持有思维")
    print(f"   4. 价格合适时买入并长期持有")


def main():
    """主函数"""
    company_name = sys.argv[1] if len(sys.argv) > 1 else '目标公司'
    
    result = analyze_duan(company_name)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

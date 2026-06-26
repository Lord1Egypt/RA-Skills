#!/usr/bin/env python3
"""
估值分析器 - 基于邱国鹭的估值方法

需要财报数据，使用数据获取层
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def pe_valuation(eps: float, growth_rate: float, industry_pe: float) -> dict:
    """
    PE 估值法
    
    Args:
        eps: 每股收益
        growth_rate: 增长率
        industry_pe: 行业 PE
    
    Returns:
        估值结果
    """
    # 合理 PE = 增长率（PEG=1）
    reasonable_pe = growth_rate
    intrinsic_value = eps * reasonable_pe
    
    return {
        'method': 'PE 估值法',
        'reasonable_pe': reasonable_pe,
        'industry_pe': industry_pe,
        'intrinsic_value': intrinsic_value,
        'formula': f'合理 PE = 增长率 ({growth_rate}%), 内在价值 = EPS × 合理 PE',
    }


def pb_valuation(bvps: float, industry_pb: float) -> dict:
    """
    PB 估值法
    
    Args:
        bvps: 每股净资产
        industry_pb: 行业 PB
    
    Returns:
        估值结果
    """
    intrinsic_value = bvps * industry_pb
    
    return {
        'method': 'PB 估值法',
        'industry_pb': industry_pb,
        'intrinsic_value': intrinsic_value,
        'formula': f'内在价值 = BVPS × 行业 PB',
    }


def dcf_valuation(fcf: float, growth_rate: float, discount_rate: float = 0.1) -> dict:
    """
    DCF 估值法（简化）
    
    Args:
        fcf: 自由现金流
        growth_rate: 增长率
        discount_rate: 折现率
    
    Returns:
        估值结果
    """
    # 简化 DCF：永续增长模型
    if discount_rate > growth_rate / 100:
        intrinsic_value = fcf * (1 + growth_rate / 100) / (discount_rate - growth_rate / 100)
    else:
        intrinsic_value = fcf * 10  # 简化处理
    
    return {
        'method': 'DCF 估值法',
        'discount_rate': discount_rate,
        'intrinsic_value': intrinsic_value,
        'formula': f'内在价值 = FCF × (1+g) / (r-g)',
    }


def analyze_valuation(symbol: str) -> dict:
    """
    估值完整分析
    
    Args:
        symbol: 股票代码
    
    Returns:
        分析结果
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
    }
    
    # 获取数据
    fetcher = DataFetcher()
    
    try:
        quote = fetcher.get_quote(symbol)
        result['quote'] = {
            'price': quote.price,
            'pe': quote.pe,
            'pb': quote.pb,
            'source': quote.source,
        }
        result['data_sources'].append(f"行情：{quote.source}")
        
        # 获取财报
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'eps': financials.eps,
                'roe': financials.roe,
                'bvps': financials.eps / (financials.roe / 100) if financials.roe > 0 else 0,
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
        except DataFetchError:
            result['financials'] = None
        
        # 估值分析
        if result['financials']:
            # PE 估值
            result['pe_valuation'] = pe_valuation(
                result['financials']['eps'],
                15,  # 假设增长率 15%
                result['quote']['pe']
            )
            
            # PB 估值
            result['pb_valuation'] = pb_valuation(
                result['financials']['bvps'],
                result['quote']['pb']
            )
            
            # 综合估值
            avg_intrinsic = (
                result['pe_valuation']['intrinsic_value'] +
                result['pb_valuation']['intrinsic_value']
            ) / 2
            
            result['comprehensive'] = {
                'avg_intrinsic_value': avg_intrinsic,
                'current_price': result['quote']['price'],
                'margin': (avg_intrinsic - result['quote']['price']) / avg_intrinsic * 100,
            }
            
            # 投资建议
            margin = result['comprehensive']['margin']
            if margin > 30:
                result['recommendation'] = '低估（买入）'
            elif margin > 10:
                result['recommendation'] = '合理（持有）'
            else:
                result['recommendation'] = '高估（卖出）'
        else:
            result['recommendation'] = '数据不足，无法估值'
        
        return result
        
    except DataFetchError as e:
        return {
            'symbol': symbol,
            'error': str(e),
            'recommendation': '数据获取失败'
        }


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"💰 估值分析器：{result['symbol']}")
    print("="*60)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        return
    
    # 股价数据
    quote = result.get('quote', {})
    print(f"\n📊 当前价格（来源：{quote.get('source', 'N/A')}）")
    print(f"   ¥{quote.get('price', 0):.2f}")
    print(f"   PE: {quote.get('pe', 0):.1f}")
    print(f"   PB: {quote.get('pb', 0):.1f}")
    
    # 估值分析
    if result.get('pe_valuation'):
        print(f"\n📈 PE 估值")
        print(f"   合理 PE: {result['pe_valuation']['reasonable_pe']}")
        print(f"   内在价值：¥{result['pe_valuation']['intrinsic_value']:.2f}")
    
    if result.get('pb_valuation'):
        print(f"\n📈 PB 估值")
        print(f"   内在价值：¥{result['pb_valuation']['intrinsic_value']:.2f}")
    
    # 综合估值
    if result.get('comprehensive'):
        comp = result['comprehensive']
        print(f"\n💎 综合估值")
        print(f"   平均内在价值：¥{comp['avg_intrinsic_value']:.2f}")
        print(f"   当前价格：¥{comp['current_price']:.2f}")
        print(f"   安全边际：{comp['margin']:.1f}%")
    
    # 投资建议
    print(f"\n💡 投资建议")
    print(f"   {result.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    
    print(f"\n⚠️  免责声明")
    print(f"   估值仅供参考，不构成投资建议")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 analyze-valuation.py <股票代码>")
        print("示例：python3 analyze-valuation.py 600519.SH")
        return 1
    
    symbol = sys.argv[1].upper()
    result = analyze_valuation(symbol)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

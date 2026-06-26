#!/usr/bin/env python3
"""
品质分析器 - 基于邱国鹭的品质投资方法

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


def evaluate_quality(financials: dict) -> dict:
    """
    品质评估
    
    Args:
        financials: 财报数据
    
    Returns:
        评估结果
    """
    result = {
        'score': 0,
        'max_score': 25,
        'dimensions': {},
    }
    
    # ROE 评估（5 分）
    roe = financials.get('roe', 0)
    if roe > 20:
        roe_score = 5
        roe_comment = '优秀'
    elif roe > 15:
        roe_score = 4
        roe_comment = '良好'
    elif roe > 10:
        roe_score = 3
        roe_comment = '一般'
    else:
        roe_score = 1
        roe_comment = '差'
    
    result['dimensions']['roe'] = {
        'value': roe,
        'score': roe_score,
        'comment': roe_comment,
    }
    result['score'] += roe_score
    
    # 毛利率评估（5 分）
    gross_margin = financials.get('gross_margin', 0)
    if gross_margin > 40:
        gm_score = 5
        gm_comment = '优秀'
    elif gross_margin > 30:
        gm_score = 4
        gm_comment = '良好'
    elif gross_margin > 20:
        gm_score = 3
        gm_comment = '一般'
    else:
        gm_score = 1
        gm_comment = '差'
    
    result['dimensions']['gross_margin'] = {
        'value': gross_margin,
        'score': gm_score,
        'comment': gm_comment,
    }
    result['score'] += gm_score
    
    # 净利率评估（5 分）
    net_margin = financials.get('net_margin', 0)
    if net_margin > 20:
        nm_score = 5
        nm_comment = '优秀'
    elif net_margin > 15:
        nm_score = 4
        nm_comment = '良好'
    elif net_margin > 10:
        nm_score = 3
        nm_comment = '一般'
    else:
        nm_score = 1
        nm_comment = '差'
    
    result['dimensions']['net_margin'] = {
        'value': net_margin,
        'score': nm_score,
        'comment': nm_comment,
    }
    result['score'] += nm_score
    
    # 负债率评估（5 分）
    debt_ratio = financials.get('debt_ratio', 0)
    if debt_ratio < 30:
        dr_score = 5
        dr_comment = '优秀'
    elif debt_ratio < 50:
        dr_score = 4
        dr_comment = '良好'
    elif debt_ratio < 70:
        dr_score = 3
        dr_comment = '一般'
    else:
        dr_score = 1
        dr_comment = '差'
    
    result['dimensions']['debt_ratio'] = {
        'value': debt_ratio,
        'score': dr_score,
        'comment': dr_comment,
    }
    result['score'] += dr_score
    
    # 现金流评估（5 分）
    fcf = financials.get('fcf', 0)
    if fcf > 0:
        fcf_score = 5
        fcf_comment = '优秀'
    else:
        fcf_score = 1
        fcf_comment = '差'
    
    result['dimensions']['fcf'] = {
        'value': fcf,
        'score': fcf_score,
        'comment': fcf_comment,
    }
    result['score'] += fcf_score
    
    return result


def analyze_quality(symbol: str) -> dict:
    """
    品质完整分析
    
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
            'source': quote.source,
        }
        result['data_sources'].append(f"行情：{quote.source}")
        
        # 获取财报
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'roe': financials.roe,
                'gross_margin': financials.gross_margin,
                'net_margin': financials.net_margin,
                'debt_ratio': financials.debt_ratio,
                'fcf': 0,  # 简化处理
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
            
            # 品质评估
            result['quality'] = evaluate_quality(result['financials'])
            
            # 综合评级
            score_pct = result['quality']['score'] / result['quality']['max_score'] * 100
            if score_pct >= 80:
                result['rating'] = '优秀'
                result['recommendation'] = '强烈推荐（好公司）'
            elif score_pct >= 60:
                result['rating'] = '良好'
                result['recommendation'] = '推荐（不错的公司）'
            elif score_pct >= 40:
                result['rating'] = '一般'
                result['recommendation'] = '观察（普通公司）'
            else:
                result['rating'] = '差'
                result['recommendation'] = '回避（需谨慎）'
        except DataFetchError:
            result['financials'] = None
            result['recommendation'] = '数据不足，无法评估'
        
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
    print(f"🏆 品质分析器：{result['symbol']}")
    print("="*60)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        return
    
    # 股价数据
    quote = result.get('quote', {})
    print(f"\n📊 当前价格（来源：{quote.get('source', 'N/A')}）")
    print(f"   ¥{quote.get('price', 0):.2f}")
    
    # 品质评估
    if result.get('quality'):
        quality = result['quality']
        print(f"\n📈 品质评估（{quality['score']}/{quality['max_score']}分）")
        
        for dim_key, dim_data in quality['dimensions'].items():
            dim_name = {
                'roe': 'ROE',
                'gross_margin': '毛利率',
                'net_margin': '净利率',
                'debt_ratio': '负债率',
                'fcf': '自由现金流',
            }.get(dim_key, dim_key)
            
            score_icon = '⭐' * dim_data['score']
            print(f"   {dim_name}: {dim_data['value']:.1f}% ({dim_data['comment']}) {score_icon}")
        
        print(f"\n🏆 综合评级")
        print(f"   评级：{result.get('rating', 'N/A')}")
    
    # 投资建议
    print(f"\n💡 投资建议")
    print(f"   {result.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    
    print(f"\n⚠️  免责声明")
    print(f"   分析仅供参考，不构成投资建议")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 analyze-quality.py <股票代码>")
        print("示例：python3 analyze-quality.py 600519.SH")
        return 1
    
    symbol = sys.argv[1].upper()
    result = analyze_quality(symbol)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

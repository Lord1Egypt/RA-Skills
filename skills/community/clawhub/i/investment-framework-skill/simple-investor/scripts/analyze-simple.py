#!/usr/bin/env python3
"""
简单投资者 - 数据获取脚本

基于邱国鹭《投资中最简单的事》选股三要素：估值、品质、时机
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def analyze_valuation(quote: dict) -> dict:
    """
    估值分析（便宜吗？）
    
    Args:
        quote: 股价数据
    
    Returns:
        估值分析结果
    """
    pe = quote.get('pe', 0)
    pb = quote.get('pb', 0)
    
    result = {
        'metrics': {},
        'score': 0,
        'max_score': 4,
        'conclusion': '等待数据',
    }
    
    # PE 分析
    if pe > 0:
        result['metrics']['pe'] = pe
        if pe < 10:
            result['pe_assessment'] = '低估'
            result['score'] += 2
        elif pe < 15:
            result['pe_assessment'] = '合理'
            result['score'] += 1
        elif pe < 25:
            result['pe_assessment'] = '合理偏高'
        else:
            result['pe_assessment'] = '高估'
    
    # PB 分析
    if pb > 0:
        result['metrics']['pb'] = pb
        if pb < 1:
            result['pb_assessment'] = '低估'
            result['score'] += 2
        elif pb < 2:
            result['pb_assessment'] = '合理'
            result['score'] += 1
        elif pb < 4:
            result['pb_assessment'] = '合理偏高'
        else:
            result['pb_assessment'] = '高估'
    
    # 综合结论
    if result['score'] >= 3:
        result['conclusion'] = '便宜（值得关注）'
    elif result['score'] >= 2:
        result['conclusion'] = '合理（可以观察）'
    elif result['score'] >= 1:
        result['conclusion'] = '偏贵（谨慎）'
    else:
        result['conclusion'] = '太贵（回避）'
    
    return result


def analyze_quality(financials: dict) -> dict:
    """
    品质分析（好公司吗？）
    
    Args:
        financials: 财报数据
    
    Returns:
        品质分析结果
    """
    result = {
        'metrics': {},
        'score': 0,
        'max_score': 4,
        'conclusion': '等待数据',
    }
    
    if not financials:
        return result
    
    # ROE 分析
    roe = financials.get('roe', 0)
    if roe > 0:
        result['metrics']['roe'] = roe
        if roe > 20:
            result['roe_assessment'] = '优秀'
            result['score'] += 2
        elif roe > 15:
            result['roe_assessment'] = '良好'
            result['score'] += 1
        elif roe > 10:
            result['roe_assessment'] = '一般'
        else:
            result['roe_assessment'] = '差'
    
    # 毛利率分析
    gross_margin = financials.get('gross_margin', 0)
    if gross_margin > 0:
        result['metrics']['gross_margin'] = gross_margin
        if gross_margin > 40:
            result['gross_margin_assessment'] = '优秀'
            result['score'] += 1
        elif gross_margin > 20:
            result['gross_margin_assessment'] = '良好'
        else:
            result['gross_margin_assessment'] = '一般'
    
    # 负债率分析
    debt_ratio = financials.get('debt_ratio', 0)
    if debt_ratio > 0:
        result['metrics']['debt_ratio'] = debt_ratio
        if debt_ratio < 30:
            result['debt_assessment'] = '优秀'
            result['score'] += 1
        elif debt_ratio < 50:
            result['debt_assessment'] = '良好'
        else:
            result['debt_assessment'] = '偏高'
    
    # 综合结论
    if result['score'] >= 4:
        result['conclusion'] = '优秀（好公司）'
    elif result['score'] >= 3:
        result['conclusion'] = '良好（不错）'
    elif result['score'] >= 2:
        result['conclusion'] = '一般（普通）'
    else:
        result['conclusion'] = '差（需谨慎）'
    
    return result


def analyze_timing(quote: dict, financials: dict = None) -> dict:
    """
    时机分析（现在能买吗？）
    
    Args:
        quote: 股价数据
        financials: 财报数据
    
    Returns:
        时机分析结果
    """
    result = {
        'factors': [],
        'recommendation': '观察',
    }
    
    # 估值位置
    if quote.get('pe', 0) > 0:
        if quote['pe'] < 10:
            result['factors'].append('✅ 估值处于低位')
        elif quote['pe'] < 15:
            result['factors'].append('➡️ 估值合理')
        else:
            result['factors'].append('⚠️ 估值偏高')
    
    # 市场情绪（简化，实际需要通过搜索获取）
    result['factors'].append('❓ 市场情绪：需要搜索分析')
    
    # 行业周期
    result['factors'].append('❓ 行业周期：需要行业分析')
    
    # 催化剂
    result['factors'].append('❓ 催化剂：需要新闻分析')
    
    # 综合建议
    positive = sum(1 for f in result['factors'] if f.startswith('✅'))
    negative = sum(1 for f in result['factors'] if f.startswith('⚠️'))
    
    if positive >= 2 and negative == 0:
        result['recommendation'] = '买入'
    elif positive >= 1 and negative <= 1:
        result['recommendation'] = '观察'
    else:
        result['recommendation'] = '等待更好时机'
    
    return result


def analyze_stock(symbol: str) -> dict:
    """
    简单投资者完整分析（选股三要素）
    
    Args:
        symbol: 股票代码
    
    Returns:
        分析结果字典
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
        
        # 如果 Tushare 没有 PE/PB，尝试从东方财富获取
        pe, pb = quote.pe, quote.pb
        data_sources_detail = [quote.source]
        
        if pe == 0 or pb == 0:
            try:
                from data_fetcher.providers.eastmoney import fetch_eastmoney_quote
                em_quote = fetch_eastmoney_quote(symbol)
                if em_quote.pe > 0 and pe == 0:
                    pe = em_quote.pe
                    data_sources_detail.append('eastmoney(PE)')
                if em_quote.pb > 0 and pb == 0:
                    pb = em_quote.pb
                    data_sources_detail.append('eastmoney(PB)')
            except Exception:
                pass
        
        result['quote'] = {
            'price': quote.price,
            'pe': pe,
            'pb': pb,
            'source': quote.source,
        }
        result['data_sources'].append(f"行情：{', '.join(data_sources_detail)}")
        
        # 尝试获取财报
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'roe': financials.roe,
                'debt_ratio': financials.debt_ratio,
                'gross_margin': financials.gross_margin,
                'eps': financials.eps,
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
            
            # 尝试获取增长率（用于更完整分析）
            try:
                result['financials']['revenue_growth'] = financials.revenue_growth if hasattr(financials, 'revenue_growth') else 15
            except Exception:
                result['financials']['revenue_growth'] = 15  # 默认值
        except DataFetchError:
            result['financials'] = None
        
        # 估值分析
        result['valuation'] = analyze_valuation(result['quote'])
        
        # 品质分析
        result['quality'] = analyze_quality(result.get('financials'))
        
        # 时机分析
        result['timing'] = analyze_timing(result['quote'], result.get('financials'))
        
        # 综合建议
        valuation_score = result['valuation']['score']
        quality_score = result['quality']['score']
        
        if valuation_score >= 3 and quality_score >= 3:
            result['recommendation'] = '强烈推荐（好公司 + 好价格）'
        elif valuation_score >= 2 and quality_score >= 3:
            result['recommendation'] = '推荐（好公司 + 合理价格）'
        elif valuation_score >= 3 and quality_score >= 2:
            result['recommendation'] = '关注（普通公司 + 好价格）'
        else:
            result['recommendation'] = '观察或等待'
        
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
    print(f"📈 简单投资者分析：{result['symbol']}")
    print("="*60)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        return
    
    # 股价数据
    quote = result.get('quote', {})
    print(f"\n📊 股价数据（来源：{quote.get('source', 'N/A')}）")
    print(f"   价格：¥{quote.get('price', 0):.2f}")
    print(f"   PE: {quote.get('pe', 0):.1f}")
    print(f"   PB: {quote.get('pb', 0):.1f}")
    
    # 财报数据
    financials = result.get('financials')
    if financials:
        print(f"\n📋 财报数据（来源：{financials.get('source', 'N/A')}）")
        print(f"   ROE: {financials.get('roe', 0):.1f}%")
        print(f"   毛利率：{financials.get('gross_margin', 0):.1f}%")
        print(f"   负债率：{financials.get('debt_ratio', 0):.1f}%")
    
    # 估值分析
    valuation = result.get('valuation', {})
    print(f"\n💰 估值分析（{valuation.get('score', 0)}/{valuation.get('max_score', 4)}分）")
    if valuation.get('metrics'):
        if 'pe' in valuation['metrics']:
            print(f"   PE: {valuation['metrics']['pe']:.1f} ({valuation.get('pe_assessment', 'N/A')})")
        if 'pb' in valuation['metrics']:
            print(f"   PB: {valuation['metrics']['pb']:.1f} ({valuation.get('pb_assessment', 'N/A')})")
    print(f"   结论：{valuation.get('conclusion', 'N/A')}")
    
    # 品质分析
    quality = result.get('quality', {})
    print(f"\n🏆 品质分析（{quality.get('score', 0)}/{quality.get('max_score', 4)}分）")
    if quality.get('metrics'):
        if 'roe' in quality['metrics']:
            print(f"   ROE: {quality['metrics']['roe']:.1f}% ({quality.get('roe_assessment', 'N/A')})")
        if 'gross_margin' in quality['metrics']:
            print(f"   毛利率：{quality['metrics']['gross_margin']:.1f}% ({quality.get('gross_margin_assessment', 'N/A')})")
        if 'debt_ratio' in quality['metrics']:
            print(f"   负债率：{quality['metrics']['debt_ratio']:.1f}% ({quality.get('debt_assessment', 'N/A')})")
    print(f"   结论：{quality.get('conclusion', 'N/A')}")
    
    # 时机分析
    timing = result.get('timing', {})
    print(f"\n⏰ 时机分析")
    for factor in timing.get('factors', []):
        print(f"   {factor}")
    print(f"   建议：{timing.get('recommendation', 'N/A')}")
    
    # 综合建议
    print(f"\n💡 综合建议")
    print(f"   {result.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 analyze-simple.py <股票代码>")
        print("示例：python3 analyze-simple.py 600519.SH")
        return 1
    
    symbol = sys.argv[1].upper()
    result = analyze_stock(symbol)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

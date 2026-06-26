#!/usr/bin/env python3
"""
内在价值计算器 - 数据获取脚本

基于格雷厄姆公式计算企业内在价值和安全边际
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def graham_formula(eps: float, growth_rate: float, pe_base: float = 8.5) -> dict:
    """
    格雷厄姆公式计算内在价值
    
    V = EPS × (8.5 + 2g)
    
    Args:
        eps: 每股收益
        growth_rate: 预期增长率（%）
        pe_base: 基础 PE（默认 8.5）
    
    Returns:
        计算结果字典
    """
    if eps <= 0:
        return {
            'intrinsic_value': None,
            'formula': 'EPS 为负或零，无法计算',
            'valid': False
        }
    
    # 格雷厄姆公式
    intrinsic_value = eps * (pe_base + 2 * growth_rate)
    
    return {
        'intrinsic_value': round(intrinsic_value, 2),
        'formula': f'V = EPS({eps:.2f}) × (8.5 + 2 × {growth_rate}%) = {intrinsic_value:.2f}',
        'valid': True
    }


def discounted_cash_flow(fcf: float, growth_rate: float, discount_rate: float = 0.1, years: int = 5) -> dict:
    """
    DCF 模型计算内在价值（简化版）
    
    Args:
        fcf: 自由现金流
        growth_rate: 增长率（%）
        discount_rate: 折现率（默认 10%）
        years: 预测年数（默认 5 年）
    
    Returns:
        计算结果字典
    """
    if fcf <= 0:
        return {
            'intrinsic_value': None,
            'formula': '自由现金流为负或零，无法计算',
            'valid': False
        }
    
    # 简化 DCF：计算未来 N 年现金流现值
    total_pv = 0
    growth = growth_rate / 100
    
    for year in range(1, years + 1):
        future_fcf = fcf * (1 + growth) ** year
        present_value = future_fcf / (1 + discount_rate) ** year
        total_pv += present_value
    
    # 加上永续价值（简化：最后一年现金流 / 折现率）
    terminal_value = (fcf * (1 + growth) ** years) / discount_rate
    terminal_pv = terminal_value / (1 + discount_rate) ** years
    
    intrinsic_value = total_pv + terminal_pv
    
    return {
        'intrinsic_value': round(intrinsic_value, 2),
        'formula': f'DCF({years}年) = {intrinsic_value:.2f}',
        'present_value': round(total_pv, 2),
        'terminal_value': round(terminal_pv, 2),
        'valid': True
    }


def calculate_margin_of_safety(intrinsic_value: float, current_price: float) -> dict:
    """
    计算安全边际
    
    Args:
        intrinsic_value: 内在价值
        current_price: 当前价格
    
    Returns:
        安全边际结果
    """
    if intrinsic_value <= 0 or current_price <= 0:
        return {
            'margin': None,
            'recommendation': '数据不足',
            'analysis': '内在价值或当前价格为负/零'
        }
    
    margin = (intrinsic_value - current_price) / intrinsic_value * 100
    
    if margin > 50:
        rec = '强烈买入（极佳机会）'
    elif margin > 30:
        rec = '买入（符合标准）'
    elif margin > 10:
        rec = '观察（价格接近价值）'
    else:
        rec = '不买入（安全边际不足）'
    
    return {
        'margin': round(margin, 1),
        'recommendation': rec,
        'analysis': f'安全边际 = ({intrinsic_value:.2f} - {current_price:.2f}) / {intrinsic_value:.2f} × 100% = {margin:.1f}%'
    }


def analyze_stock(symbol: str, growth_rate: float = 15) -> dict:
    """
    内在价值完整分析
    
    Args:
        symbol: 股票代码
        growth_rate: 预期增长率（%，默认 15%）
    
    Returns:
        分析结果字典
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
        'growth_rate_assumption': growth_rate,
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
        
        # 尝试获取财报
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'eps': financials.eps,
                'roe': financials.roe,
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
            
            # 如果财报有增长率数据，使用实际值
            if hasattr(financials, 'revenue_growth') and financials.revenue_growth > 0:
                result['growth_rate_assumption'] = financials.revenue_growth
        except DataFetchError:
            result['financials'] = None
        
        # 格雷厄姆公式计算
        if result.get('financials') and result['financials'].get('eps', 0) > 0:
            result['graham'] = graham_formula(
                result['financials']['eps'],
                result['growth_rate_assumption']
            )
            
            # 计算安全边际
            if result['graham']['valid']:
                result['margin_graham'] = calculate_margin_of_safety(
                    result['graham']['intrinsic_value'],
                    result['quote']['price']
                )
        
        # DCF 计算（如果有 FCF 数据）
        # 简化：用 EPS 近似 FCF
        if result.get('financials') and result['financials'].get('eps', 0) > 0:
            result['dcf'] = discounted_cash_flow(
                result['financials']['eps'],
                result['growth_rate_assumption']
            )
            
            # 计算安全边际
            if result['dcf']['valid']:
                result['margin_dcf'] = calculate_margin_of_safety(
                    result['dcf']['intrinsic_value'],
                    result['quote']['price']
                )
        
        # 综合建议
        if result.get('margin_graham') and result.get('margin_dcf'):
            margin_graham = result['margin_graham']['margin']
            margin_dcf = result['margin_dcf']['margin']
            avg_margin = (margin_graham + margin_dcf) / 2
            
            if avg_margin > 50:
                result['recommendation'] = '强烈推荐（双重模型确认）'
            elif avg_margin > 30:
                result['recommendation'] = '推荐（符合安全边际标准）'
            elif avg_margin > 10:
                result['recommendation'] = '观察（价格接近价值）'
            else:
                result['recommendation'] = '不推荐（安全边际不足）'
        else:
            result['recommendation'] = '数据不足，无法给出明确建议'
        
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
    print(f"💎 内在价值计算器：{result['symbol']}")
    print("="*60)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        return
    
    # 股价数据
    quote = result.get('quote', {})
    print(f"\n📊 当前价格（来源：{quote.get('source', 'N/A')}）")
    print(f"   ¥{quote.get('price', 0):.2f}")
    
    # 财报数据
    financials = result.get('financials')
    if financials:
        print(f"\n📋 财报数据（来源：{financials.get('source', 'N/A')}）")
        print(f"   EPS: {financials.get('eps', 0):.2f}元")
        print(f"   ROE: {financials.get('roe', 0):.1f}%")
    
    # 增长率假设
    print(f"\n📈 增长率假设：{result.get('growth_rate_assumption', 15):.1f}%")
    
    # 格雷厄姆公式
    graham = result.get('graham')
    if graham:
        print(f"\n📐 格雷厄姆公式")
        if graham.get('valid'):
            print(f"   {graham.get('formula', 'N/A')}")
            print(f"   内在价值：¥{graham.get('intrinsic_value', 0):.2f}")
            
            margin = result.get('margin_graham')
            if margin:
                print(f"   安全边际：{margin.get('margin', 0):.1f}%")
                print(f"   建议：{margin.get('recommendation', 'N/A')}")
        else:
            print(f"   {graham.get('formula', '无法计算')}")
    
    # DCF 模型
    dcf = result.get('dcf')
    if dcf:
        print(f"\n💵 DCF 模型")
        if dcf.get('valid'):
            print(f"   {dcf.get('formula', 'N/A')}")
            print(f"   内在价值：¥{dcf.get('intrinsic_value', 0):.2f}")
            
            margin = result.get('margin_dcf')
            if margin:
                print(f"   安全边际：{margin.get('margin', 0):.1f}%")
                print(f"   建议：{margin.get('recommendation', 'N/A')}")
        else:
            print(f"   {dcf.get('formula', '无法计算')}")
    
    # 综合建议
    print(f"\n💡 综合建议")
    print(f"   {result.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    
    # 免责声明
    print(f"\n⚠️  免责声明")
    print(f"   本计算仅供参考，不构成投资建议")
    print(f"   请结合其他因素综合判断")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 calculate-value.py <股票代码> [增长率%]")
        print("示例：python3 calculate-value.py 600519.SH 15")
        return 1
    
    symbol = sys.argv[1].upper()
    growth_rate = float(sys.argv[2]) if len(sys.argv) > 2 else 15
    
    result = analyze_stock(symbol, growth_rate)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

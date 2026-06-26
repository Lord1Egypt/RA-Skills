#!/usr/bin/env python3
"""
选股专家 - 数据获取脚本

基于彼得·林奇 13 条原则选股，PEG 估值
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def classify_company_type(symbol: str, quote: dict, financials: dict = None) -> str:
    """
    公司类型分类（6 种）
    
    Args:
        symbol: 股票代码
        quote: 股价数据
        financials: 财报数据
    
    Returns:
        公司类型
    """
    pe = quote.get('pe', 0)
    pb = quote.get('pb', 0)
    market_cap = quote.get('market_cap', 0)
    
    # 获取增长率（如果有财报数据）
    growth_rate = 0
    if financials:
        growth_rate = financials.get('revenue_growth', 0)
    
    # 简化分类逻辑
    if growth_rate > 25:
        return '快速增长型'
    elif growth_rate > 10:
        return '稳定增长型'
    elif growth_rate > 0:
        return '缓慢增长型'
    elif growth_rate < 0:
        return '困境反转型'
    else:
        return '周期型'


def calculate_peg(pe: float, growth_rate: float) -> dict:
    """
    计算 PEG 指标
    
    Args:
        pe: 市盈率
        growth_rate: 盈利增长率（%）
    
    Returns:
        PEG 结果字典
    """
    if pe <= 0 or growth_rate <= 0:
        return {
            'peg': None,
            'recommendation': '数据不足',
            'analysis': 'PE 或增长率为负/零，无法计算 PEG'
        }
    
    peg = pe / growth_rate
    
    if peg < 1:
        rec = '低估（强烈关注）'
    elif peg < 1.5:
        rec = '合理（可以关注）'
    elif peg < 2:
        rec = '高估（谨慎）'
    else:
        rec = '严重高估（回避）'
    
    return {
        'peg': round(peg, 2),
        'recommendation': rec,
        'analysis': f'PEG = PE({pe}) / 增长率({growth_rate}%) = {peg:.2f}'
    }


def lynch_13_check(symbol: str, quote: dict, financials: dict = None) -> dict:
    """
    林奇 13 条原则检查（简化版）
    
    Args:
        symbol: 股票代码
        quote: 股价数据
        financials: 财报数据
    
    Returns:
        检查结果字典
    """
    checks = []
    passed = 0
    
    # 1-5: 定性分析（需要人工判断或搜索）
    qualitative_checks = [
        ('名字枯燥', '❓', '枯燥名字往往被忽视'),
        ('业务枯燥', '❓', '枯燥业务竞争少'),
        ('机构不持有', '❓', '需要查询机构持仓'),
        ('充满谣言', '❓', '需要市场情绪分析'),
        ('利基行业', '❓', '需要行业分析'),
    ]
    
    for name, status, desc in qualitative_checks:
        checks.append({
            'name': name,
            'status': status,
            'description': desc,
        })
    
    # 6-13: 定量分析（可以用数据判断）
    if financials:
        # 6. 不断回购
        buyback = financials.get('shares_change', 0) < 0
        checks.append({
            'name': '不断回购',
            'status': '✅' if buyback else '❌',
            'description': f'股本变化：{financials.get("shares_change", 0):.1f}%',
        })
        if buyback:
            passed += 1
        
        # 7. 内部人买入（需要额外数据）
        checks.append({
            'name': '内部人买入',
            'status': '❓',
            'description': '需要查询内部人交易',
        })
        
        # 8. 盈利持续增长
        roe = financials.get('roe', 0)
        growth_consistent = roe > 15
        checks.append({
            'name': '盈利持续增长',
            'status': '✅' if growth_consistent else '❌',
            'description': f'ROE: {roe:.1f}%',
        })
        if growth_consistent:
            passed += 1
        
        # 9. 资产负债表强
        debt_ratio = financials.get('debt_ratio', 0)
        debt_ok = debt_ratio < 50
        checks.append({
            'name': '资产负债表强',
            'status': '✅' if debt_ok else '❌',
            'description': f'负债率：{debt_ratio:.1f}%',
        })
        if debt_ok:
            passed += 1
        
        # 10. PEG<1
        pe = quote.get('pe', 0)
        growth_rate = financials.get('revenue_growth', 0)
        if pe > 0 and growth_rate > 0:
            peg = pe / growth_rate
            peg_ok = peg < 1
            checks.append({
                'name': 'PEG<1',
                'status': '✅' if peg_ok else '❌',
                'description': f'PEG: {peg:.2f}',
            })
            if peg_ok:
                passed += 1
        
        # 11. 自由现金流
        fcf = financials.get('fcf_per_share', 0)
        eps = financials.get('eps', 0)
        fcf_ok = fcf > eps * 0.8
        checks.append({
            'name': '自由现金流',
            'status': '✅' if fcf_ok else '❌',
            'description': f'FCF/股：{fcf:.2f}, EPS: {eps:.2f}',
        })
        if fcf_ok:
            passed += 1
    
    # 12-13: 定性分析
    checks.append({
        'name': '生活可观察',
        'status': '❓',
        'description': '生活选股法',
    })
    
    checks.append({
        'name': '简单易懂',
        'status': '❓',
        'description': '业务简单易懂',
    })
    
    # 统计
    total_quantitative = sum(1 for c in checks if c['status'] in ['✅', '❌'])
    passed_quantitative = sum(1 for c in checks if c['status'] == '✅')
    
    return {
        'checks': checks,
        'passed': passed,
        'total_quantitative': total_quantitative,
        'passed_quantitative': passed_quantitative,
        'score': f'{passed_quantitative}/{total_quantitative}' if total_quantitative > 0 else '需补充数据',
    }


def analyze_stock(symbol: str) -> dict:
    """
    选股专家完整分析
    
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
        result['quote'] = {
            'price': quote.price,
            'pe': quote.pe,
            'pb': quote.pb,
            'market_cap': quote.market_cap,
            'source': quote.source,
        }
        result['data_sources'].append(f"行情：{quote.source}")
        
        # 尝试获取财报
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'roe': financials.roe,
                'debt_ratio': financials.debt_ratio,
                'eps': financials.eps,
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
            
            # 如果 Tushare 没有 PE/PB，尝试从东方财富获取
            if quote.pe == 0 or quote.pb == 0:
                try:
                    from data_fetcher.providers.eastmoney import fetch_eastmoney_quote
                    em_quote = fetch_eastmoney_quote(symbol)
                    if em_quote.pe > 0:
                        result['quote']['pe'] = em_quote.pe
                    if em_quote.pb > 0:
                        result['quote']['pb'] = em_quote.pb
                    result['data_sources'].append(f"估值：eastmoney")
                except Exception:
                    pass
        except DataFetchError:
            result['financials'] = None
        
        # 公司类型分类
        result['company_type'] = classify_company_type(
            symbol,
            result['quote'],
            result.get('financials')
        )
        
        # PEG 估值
        if result['quote']['pe'] > 0 and result.get('financials'):
            growth = result['financials'].get('revenue_growth', 15)  # 默认 15%
            result['peg'] = calculate_peg(result['quote']['pe'], growth)
        
        # 林奇 13 条原则检查
        result['lynch_check'] = lynch_13_check(
            symbol,
            result['quote'],
            result.get('financials')
        )
        
        # 综合建议
        if result.get('peg') and result['peg']['peg']:
            if result['peg']['peg'] < 1:
                result['recommendation'] = '强烈关注（PEG<1）'
            elif result['peg']['peg'] < 1.5:
                result['recommendation'] = '可以关注（PEG 合理）'
            else:
                result['recommendation'] = '谨慎（PEG 偏高）'
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
    print(f"📊 选股专家分析：{result['symbol']}")
    print("="*60)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        return
    
    # 股价数据
    quote = result.get('quote', {})
    print(f"\n📈 股价数据（来源：{quote.get('source', 'N/A')}）")
    print(f"   价格：¥{quote.get('price', 0):.2f}")
    print(f"   PE: {quote.get('pe', 0):.1f}")
    print(f"   PB: {quote.get('pb', 0):.1f}")
    
    # 财报数据
    financials = result.get('financials')
    if financials:
        print(f"\n📋 财报数据（来源：{financials.get('source', 'N/A')}）")
        print(f"   ROE: {financials.get('roe', 0):.1f}%")
        print(f"   负债率：{financials.get('debt_ratio', 0):.1f}%")
        print(f"   EPS: {financials.get('eps', 0):.2f}元")
    
    # 公司类型
    print(f"\n🏢 公司类型：{result.get('company_type', '未知')}")
    
    # PEG 估值
    peg = result.get('peg')
    if peg:
        print(f"\n💰 PEG 估值")
        print(f"   {peg.get('analysis', 'N/A')}")
        print(f"   建议：{peg.get('recommendation', 'N/A')}")
    
    # 林奇 13 条
    lynch = result.get('lynch_check', {})
    if lynch:
        print(f"\n🎯 林奇 13 条原则检查")
        print(f"   定量评分：{lynch.get('score', 'N/A')}")
        
        for check in lynch.get('checks', []):
            status = check.get('status', '?')
            name = check.get('name', 'Unknown')
            desc = check.get('description', '')
            print(f"   {status} {name}: {desc}")
    
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
        print("用法：python3 analyze-stock.py <股票代码>")
        print("示例：python3 analyze-stock.py 000001.SZ")
        return 1
    
    symbol = sys.argv[1].upper()
    result = analyze_stock(symbol)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
护城河评估师 - 基于巴菲特的护城河理论

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


# 护城河类型
MOAT_TYPES = {
    'intangible_assets': {
        'name': '无形资产',
        'indicators': ['品牌溢价', '专利保护', '政府牌照'],
        'questions': [
            '产品是否有定价权？',
            '是否有强大的品牌认知？',
            '是否有专利或牌照保护？',
        ],
    },
    'switching_costs': {
        'name': '转换成本',
        'indicators': ['客户粘性', '学习成本', '数据迁移成本'],
        'questions': [
            '客户更换供应商的成本高吗？',
            '用户是否形成使用习惯？',
            '是否有网络效应？',
        ],
    },
    'network_effect': {
        'name': '网络效应',
        'indicators': ['用户越多价值越大', '双边市场', '平台效应'],
        'questions': [
            '每增加一个用户，产品价值是否增加？',
            '是否形成赢家通吃？',
            '是否有临界点效应？',
        ],
    },
    'cost_advantage': {
        'name': '成本优势',
        'indicators': ['规模经济', '独特资源', '工艺优势'],
        'questions': [
            '是否有规模经济？',
            '是否拥有独特资源？',
            '毛利率是否显著高于同行？',
        ],
    },
    'efficient_scale': {
        'name': '有效规模',
        'indicators': ['市场有限', '进入不划算', '自然垄断'],
        'questions': [
            '市场是否有限？',
            '新进入者是否无利可图？',
            '是否形成自然垄断？',
        ],
    },
}


def evaluate_moat_type(moat_key: str, financials: dict, company_info: dict = None) -> dict:
    """
    评估护城河类型
    
    Args:
        moat_key: 护城河类型键
        financials: 财报数据
        company_info: 公司信息
    
    Returns:
        评估结果
    """
    moat = MOAT_TYPES[moat_key]
    
    result = {
        'type': moat['name'],
        'score': 0,
        'max_score': 5,
        'evidence': [],
        'questions': [],
    }
    
    # 基于财务数据评估
    if financials:
        # 毛利率评估（成本优势）
        if moat_key == 'cost_advantage':
            gross_margin = financials.get('gross_margin', 0)
            if gross_margin > 50:
                result['score'] = 5
                result['evidence'].append(f'毛利率 {gross_margin:.1f}%，显著高于同行')
            elif gross_margin > 30:
                result['score'] = 3
                result['evidence'].append(f'毛利率 {gross_margin:.1f}%，处于中等水平')
            else:
                result['score'] = 1
                result['evidence'].append(f'毛利率 {gross_margin:.1f}%，无明显优势')
        
        # ROE 评估（无形资产）
        elif moat_key == 'intangible_assets':
            roe = financials.get('roe', 0)
            if roe > 20:
                result['score'] = 5
                result['evidence'].append(f'ROE {roe:.1f}%，显示强大竞争优势')
            elif roe > 15:
                result['score'] = 3
                result['evidence'].append(f'ROE {roe:.1f}%，表现良好')
            else:
                result['score'] = 1
                result['evidence'].append(f'ROE {roe:.1f}%，无明显优势')
        
        # 其他类型需要定性分析
        else:
            result['score'] = 3  # 默认中等
            result['evidence'].append('需要定性分析')
    
    # 添加评估问题
    result['questions'] = moat['questions']
    
    return result


def calculate_moat_width(moat_scores: dict) -> dict:
    """
    计算护城河宽度
    
    Args:
        moat_scores: 各护城河类型评分
    
    Returns:
        护城河宽度评估
    """
    total_score = sum(m['score'] for m in moat_scores.values())
    max_score = sum(m['max_score'] for m in moat_scores.values())
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    if percentage >= 70:
        width = '宽'
        description = '强大且持久的竞争优势'
    elif percentage >= 50:
        width = '中等'
        description = '一定的竞争优势'
    elif percentage >= 30:
        width = '窄'
        description = '微弱的竞争优势'
    else:
        width = '无'
        description = '无明显竞争优势'
    
    return {
        'width': width,
        'description': description,
        'score': f'{total_score}/{max_score}',
        'percentage': f'{percentage:.1f}%',
    }


def analyze_moat(symbol: str) -> dict:
    """
    护城河完整分析
    
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
            'source': quote.source,
        }
        result['data_sources'].append(f"行情：{quote.source}")
        
        # 获取财报数据
        try:
            financials = fetcher.get_financials(symbol)
            result['financials'] = {
                'roe': financials.roe,
                'gross_margin': financials.gross_margin,
                'debt_ratio': financials.debt_ratio,
                'source': financials.source,
            }
            result['data_sources'].append(f"财报：{financials.source}")
        except DataFetchError:
            result['financials'] = None
        
        # 评估各类型护城河
        result['moat_types'] = {}
        for moat_key in MOAT_TYPES.keys():
            result['moat_types'][moat_key] = evaluate_moat_type(
                moat_key,
                result.get('financials')
            )
        
        # 计算护城河宽度
        result['moat_width'] = calculate_moat_width(result['moat_types'])
        
        # 综合建议
        width = result['moat_width']['width']
        if width == '宽':
            result['recommendation'] = '强烈推荐（宽护城河）'
        elif width == '中等':
            result['recommendation'] = '推荐（中等护城河）'
        elif width == '窄':
            result['recommendation'] = '观察（窄护城河）'
        else:
            result['recommendation'] = '谨慎（无明显护城河）'
        
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
    print(f"🏰 护城河评估师：{result['symbol']}")
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
        print(f"   ROE: {financials.get('roe', 0):.1f}%")
        print(f"   毛利率：{financials.get('gross_margin', 0):.1f}%")
        print(f"   负债率：{financials.get('debt_ratio', 0):.1f}%")
    
    # 护城河类型评估
    print(f"\n🏰 护城河类型评估")
    for moat_key, moat_data in result['moat_types'].items():
        score_icon = '⭐' * (moat_data['score'] // 2)
        print(f"\n   {moat_data['type']} ({moat_data['score']}/{moat_data['max_score']}分) {score_icon}")
        if moat_data['evidence']:
            for ev in moat_data['evidence']:
                print(f"     • {ev}")
    
    # 护城河宽度
    width = result.get('moat_width', {})
    print(f"\n📏 护城河宽度")
    print(f"   {width.get('width', '未知')} - {width.get('description', 'N/A')}")
    print(f"   评分：{width.get('score', 'N/A')} ({width.get('percentage', 'N/A')})")
    
    # 综合建议
    print(f"\n💡 综合建议")
    print(f"   {result.get('recommendation', 'N/A')}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    
    # 免责声明
    print(f"\n⚠️  免责声明")
    print(f"   本分析仅供参考，不构成投资建议")
    print(f"   请结合其他因素综合判断")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 evaluate-moat.py <股票代码>")
        print("示例：python3 evaluate-moat.py 600519.SH")
        return 1
    
    symbol = sys.argv[1].upper()
    result = analyze_moat(symbol)
    print_analysis(result)
    
    return 0 if 'error' not in result else 1


if __name__ == '__main__':
    sys.exit(main())

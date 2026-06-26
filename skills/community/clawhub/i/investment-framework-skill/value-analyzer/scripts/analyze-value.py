#!/usr/bin/env python3
"""
价值分析师 - 数据获取脚本

基于格雷厄姆原则分析股票价值
"""

import sys
import os

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def analyze_graham_standards(symbol: str, quote: dict, financials: dict = None) -> dict:
    """
    格雷厄姆标准分析
    
    Args:
        symbol: 股票代码
        quote: 股价数据
        financials: 财报数据（可选）
    
    Returns:
        分析结果字典
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
        'graham_check': {
            'defensive': [],  # 防御型标准
            'enterprising': [],  # 积极型标准
        },
        'recommendation': '观察',
        'confidence': '低',
    }
    
    # 数据源
    if quote.get('source'):
        result['data_sources'].append(f"行情：{quote['source']}")
    if financials and financials.get('source'):
        result['data_sources'].append(f"财报：{financials['source']}")
    
    # 防御型投资者标准检查
    pe = quote.get('pe', 0)
    pb = quote.get('pb', 0)
    price = quote.get('price', 0)
    
    # 1. 市盈率 < 15
    if pe > 0:
        pe_check = pe < 15
        result['graham_check']['defensive'].append({
            'standard': '市盈率',
            'requirement': '< 15',
            'value': f'{pe:.1f}',
            'pass': pe_check,
        })
    
    # 2. 市净率 < 1.5
    if pb > 0:
        pb_check = pb < 1.5
        result['graham_check']['defensive'].append({
            'standard': '市净率',
            'requirement': '< 1.5',
            'value': f'{pb:.1f}',
            'pass': pb_check,
        })
    
    # 3. 财务稳健（如果有财报数据）
    if financials:
        debt_ratio = financials.get('debt_ratio', 0)
        if debt_ratio > 0:
            debt_check = debt_ratio < 50
            result['graham_check']['defensive'].append({
                'standard': '负债率',
                'requirement': '< 50%',
                'value': f'{debt_ratio:.1f}%',
                'pass': debt_check,
            })
        
        roe = financials.get('roe', 0)
        if roe > 0:
            roe_check = roe > 10
            result['graham_check']['defensive'].append({
                'standard': 'ROE',
                'requirement': '> 10%',
                'value': f'{roe:.1f}%',
                'pass': roe_check,
            })
    
    # 计算通过数量
    defensive_checks = result['graham_check']['defensive']
    passed = sum(1 for check in defensive_checks if check.get('pass', False))
    total = len(defensive_checks)
    
    # 生成建议
    if total == 0:
        result['recommendation'] = '数据不足，无法分析'
        result['confidence'] = '无'
    elif passed / total >= 0.8:
        result['recommendation'] = '符合格雷厄姆标准'
        result['confidence'] = '高'
    elif passed / total >= 0.5:
        result['recommendation'] = '部分符合，需进一步分析'
        result['confidence'] = '中'
    else:
        result['recommendation'] = '不符合格雷厄姆标准'
        result['confidence'] = '高'
    
    # 安全边际计算（简化版）
    if pe > 0 and pb > 0:
        # 简化内在价值估算
        intrinsic_value = price * (15 / pe) * 0.5 + price * (1.5 / pb) * 0.5
        margin_of_safety = (intrinsic_value - price) / intrinsic_value * 100
        
        result['margin_of_safety'] = {
            'intrinsic_value': round(intrinsic_value, 2),
            'current_price': round(price, 2),
            'margin': round(margin_of_safety, 1),
            'recommendation': get_margin_recommendation(margin_of_safety),
        }
    
    return result


def get_margin_recommendation(margin: float) -> str:
    """根据安全边际给出建议"""
    if margin > 50:
        return '强烈买入'
    elif margin > 30:
        return '买入'
    elif margin > 10:
        return '观察'
    else:
        return '不买入'


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 analyze-value.py <股票代码>")
        print("示例：python3 analyze-value.py 600519.SH")
        return 1
    
    symbol = sys.argv[1].upper()
    
    print(f"📊 价值分析：{symbol}")
    print("="*50)
    
    # 获取数据
    fetcher = DataFetcher()
    
    try:
        print("📈 获取股价数据...")
        quote = fetcher.get_quote(symbol)
        print(f"✅ {symbol}: ¥{quote.price} (PE: {quote.pe}, PB: {quote.pb})")
        print(f"   数据来源：{quote.source}")
        
        # 尝试获取财报
        print("\n📋 获取财报数据...")
        try:
            financials = fetcher.get_financials(symbol)
            print(f"✅ ROE: {financials.roe}%, 负债率：{financials.debt_ratio}%")
            print(f"   数据来源：{financials.source}")
            
            fin_dict = {
                'roe': financials.roe,
                'debt_ratio': financials.debt_ratio,
                'source': financials.source,
            }
        except DataFetchError as e:
            print(f"⚠️  财报获取失败：{e}")
            print(f"   使用免费数据源（东方财富）")
            fin_dict = None
        
        # 执行分析
        print("\n🔍 格雷厄姆标准分析...")
        result = analyze_graham_standards(
            symbol,
            {
                'price': quote.price,
                'pe': quote.pe,
                'pb': quote.pb,
                'source': quote.source,
            },
            fin_dict
        )
        
        # 输出结果
        print("\n" + "="*50)
        print("📊 分析结果")
        print("="*50)
        
        print(f"\n建议：{result['recommendation']}")
        print(f"置信度：{result['confidence']}")
        
        print(f"\n防御型标准检查：")
        for check in result['graham_check']['defensive']:
            status = "✅" if check['pass'] else "❌"
            print(f"  {status} {check['standard']}: {check['value']} (要求：{check['requirement']})")
        
        if 'margin_of_safety' in result:
            mos = result['margin_of_safety']
            print(f"\n安全边际：")
            print(f"  内在价值：¥{mos['intrinsic_value']}")
            print(f"  当前价格：¥{mos['current_price']}")
            print(f"  安全边际：{mos['margin']}%")
            print(f"  建议：{mos['recommendation']}")
        
        print(f"\n数据来源：{', '.join(result['data_sources'])}")
        
        return 0
        
    except DataFetchError as e:
        print(f"\n❌ 数据获取失败：{e}")
        print(f"\n💡 建议：")
        print(f"   1. 检查股票代码是否正确")
        print(f"   2. 确认网络连接")
        print(f"   3. 稍后重试")
        return 1
    except Exception as e:
        print(f"\n❌ 分析失败：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

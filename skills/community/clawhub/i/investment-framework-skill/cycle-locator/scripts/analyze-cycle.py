#!/usr/bin/env python3
"""
周期定位师 - 数据获取脚本

基于达利欧《经济机器是怎样运行的》判断经济周期位置
集成 searxng 搜索获取宏观经济数据
"""

import sys
import os
import subprocess
import json

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from datetime import datetime


def search_macro_data(country: str = '中国') -> dict:
    """
    使用 searxng 搜索宏观经济数据
    
    Args:
        country: 国家名称
    
    Returns:
        搜索到的数据字典
    """
    result = {
        'gdp_growth': None,
        'interest_rate': None,
        'debt_to_gdp': None,
        'sources': [],
    }
    
    try:
        # 搜索 GDP 增长率
        search_query = f"{country} GDP 增长率 2024 2025"
        env = os.environ.copy()
        env['SEARXNG_URL'] = 'http://localhost:8080'
        
        cmd = [
            'uv', 'run',
            f'{framework_dir}/../skills/searxng/scripts/searxng.py',
            'search', search_query,
            '-n', '3',
            '--format', 'json'
        ]
        
        proc_result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if proc_result.returncode == 0:
            search_data = json.loads(proc_result.stdout)
            if 'results' in search_data:
                result['sources'].extend(search_data['results'][:3])
    except Exception as e:
        result['error'] = str(e)
    
    return result


def analyze_short_term_debt_cycle(indicators: dict) -> dict:
    """
    短期债务周期分析（5-8 年）
    
    Args:
        indicators: 经济指标字典
    
    Returns:
        短期周期分析结果
    """
    result = {
        'stage': '未知',
        'indicators': {},
        'signals': [],
    }
    
    # GDP 增长率
    gdp_growth = indicators.get('gdp_growth', None)
    if gdp_growth is not None:
        result['indicators']['gdp_growth'] = gdp_growth
        if gdp_growth > 6:
            result['signals'].append('✅ 经济强劲')
        elif gdp_growth > 3:
            result['signals'].append('➡️ 经济温和')
        else:
            result['signals'].append('⚠️ 经济放缓')
    
    # 利率水平
    interest_rate = indicators.get('interest_rate', None)
    if interest_rate is not None:
        result['indicators']['interest_rate'] = interest_rate
        if interest_rate > 5:
            result['signals'].append('⚠️ 利率偏高')
        elif interest_rate > 2:
            result['signals'].append('➡️ 利率正常')
        else:
            result['signals'].append('✅ 利率宽松')
    
    # 信贷条件
    credit_condition = indicators.get('credit_condition', '未知')
    result['indicators']['credit_condition'] = credit_condition
    if credit_condition == '宽松':
        result['signals'].append('✅ 信贷宽松')
    elif credit_condition == '紧缩':
        result['signals'].append('⚠️ 信贷紧缩')
    else:
        result['signals'].append('➡️ 信贷正常')
    
    # 判断周期阶段
    positive_signals = sum(1 for s in result['signals'] if s.startswith('✅'))
    negative_signals = sum(1 for s in result['signals'] if s.startswith('⚠️'))
    
    if positive_signals >= 2 and negative_signals == 0:
        result['stage'] = '扩张早期'
    elif positive_signals >= 1:
        result['stage'] = '扩张晚期'
    elif negative_signals >= 2:
        result['stage'] = '衰退早期'
    else:
        result['stage'] = '衰退晚期'
    
    return result


def analyze_long_term_debt_cycle(indicators: dict) -> dict:
    """
    长期债务周期分析（50-75 年）
    
    Args:
        indicators: 经济指标字典
    
    Returns:
        长期周期分析结果
    """
    result = {
        'stage': '未知',
        'indicators': {},
        'analysis': [],
    }
    
    # 债务/GDP 比率
    debt_to_gdp = indicators.get('debt_to_gdp', None)
    if debt_to_gdp is not None:
        result['indicators']['debt_to_gdp'] = debt_to_gdp
        if debt_to_gdp > 300:
            result['analysis'].append('⚠️ 债务负担极重')
            result['stage'] = '后期/去杠杆化'
        elif debt_to_gdp > 200:
            result['analysis'].append('⚠️ 债务负担较重')
            result['stage'] = '后期'
        elif debt_to_gdp > 100:
            result['analysis'].append('➡️ 债务负担中等')
            result['stage'] = '中期'
        else:
            result['analysis'].append('✅ 债务负担较轻')
            result['stage'] = '早期'
    else:
        result['analysis'].append('❓ 需要债务/GDP 数据')
    
    # 利率空间
    rate_space = indicators.get('rate_space', None)
    if rate_space is not None:
        result['indicators']['rate_space'] = rate_space
        if rate_space > 3:
            result['analysis'].append('✅ 货币政策空间充足')
        elif rate_space > 0:
            result['analysis'].append('➡️ 货币政策空间有限')
        else:
            result['analysis'].append('⚠️ 货币政策空间耗尽')
    
    return result


def asset_allocation_recommendation(short_cycle: str, long_cycle: str) -> dict:
    """
    根据周期阶段给出资产配置建议
    
    Args:
        short_cycle: 短期周期阶段
        long_cycle: 长期周期阶段
    
    Returns:
        资产配置建议
    """
    result = {
        'stocks': '中性',
        'bonds': '中性',
        'cash': '中性',
        'gold': '中性',
        'explanation': [],
    }
    
    # 短期周期配置
    if short_cycle == '扩张早期':
        result['stocks'] = '高配'
        result['bonds'] = '低配'
        result['explanation'].append('扩张早期：股票表现最佳')
    elif short_cycle == '扩张晚期':
        result['stocks'] = '中性'
        result['bonds'] = '中性'
        result['explanation'].append('扩张晚期：保持中性')
    elif short_cycle == '衰退早期':
        result['stocks'] = '低配'
        result['bonds'] = '高配'
        result['cash'] = '高配'
        result['gold'] = '高配'
        result['explanation'].append('衰退早期：防御性配置')
    elif short_cycle == '衰退晚期':
        result['stocks'] = '中性'
        result['bonds'] = '中性'
        result['explanation'].append('衰退晚期：准备转向')
    
    # 长期周期调整
    if '去杠杆化' in long_cycle or '后期' in long_cycle:
        result['cash'] = '高配'
        result['gold'] = '高配'
        result['explanation'].append('长期债务周期后期：增加现金和黄金')
    
    return result


def analyze_cycle(gdp_growth: float = None, interest_rate: float = None, 
                  debt_to_gdp: float = None, credit_condition: str = None,
                  use_search: bool = False, country: str = '中国') -> dict:
    """
    经济周期完整分析
    
    Args:
        gdp_growth: GDP 增长率（%）
        interest_rate: 利率水平（%）
        debt_to_gdp: 债务/GDP 比率（%）
        credit_condition: 信贷条件（宽松/正常/紧缩）
        use_search: 是否使用 searxng 搜索
        country: 国家名称
    
    Returns:
        分析结果字典
    """
    result = {
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
    }
    
    # 使用 searxng 搜索获取宏观数据
    if use_search:
        search_data = search_macro_data(country)
        if search_data.get('sources'):
            result['data_sources'].append(f"searxng: {len(search_data['sources'])} 条结果")
    
    # 准备指标
    indicators = {
        'gdp_growth': gdp_growth,
        'interest_rate': interest_rate,
        'debt_to_gdp': debt_to_gdp,
        'credit_condition': credit_condition,
    }
    
    # 短期债务周期分析
    result['short_term_cycle'] = analyze_short_term_debt_cycle(indicators)
    
    # 长期债务周期分析
    result['long_term_cycle'] = analyze_long_term_debt_cycle(indicators)
    
    # 资产配置建议
    result['asset_allocation'] = asset_allocation_recommendation(
        result['short_term_cycle']['stage'],
        result['long_term_cycle']['stage']
    )
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print("📊 周期定位师")
    print("="*60)
    
    # 短期周期
    short = result.get('short_term_cycle', {})
    print(f"\n📈 短期债务周期（5-8 年）")
    print(f"   阶段：{short.get('stage', '未知')}")
    for signal in short.get('signals', []):
        print(f"   {signal}")
    
    # 长期周期
    long = result.get('long_term_cycle', {})
    print(f"\n📉 长期债务周期（50-75 年）")
    print(f"   阶段：{long.get('stage', '未知')}")
    for analysis in long.get('analysis', []):
        print(f"   {analysis}")
    
    # 资产配置建议
    allocation = result.get('asset_allocation', {})
    print(f"\n💼 资产配置建议")
    print(f"   股票：{allocation.get('stocks', '中性')}")
    print(f"   债券：{allocation.get('bonds', '中性')}")
    print(f"   现金：{allocation.get('cash', '中性')}")
    print(f"   黄金：{allocation.get('gold', '中性')}")
    
    if allocation.get('explanation'):
        print(f"\n   说明：")
        for exp in allocation['explanation']:
            print(f"   • {exp}")
    
    # 数据来源
    sources = result.get('data_sources', [])
    if sources:
        print(f"\n📊 数据来源：{', '.join(sources)}")
    else:
        print(f"\n⚠️  数据来源：手动输入（需要搜索补充）")
        print(f"   建议数据来源：")
        print(f"   • 国家统计局（GDP）")
        print(f"   • 央行（利率）")
        print(f"   • 国际清算银行（债务/GDP）")
    
    # 免责声明
    print(f"\n⚠️  免责声明")
    print(f"   本分析仅供参考，不构成投资建议")
    print(f"   请结合其他因素综合判断")


def main():
    """主函数"""
    use_search = '--search' in sys.argv
    country = '中国'
    
    # 检查是否使用默认数据
    if len(sys.argv) >= 2 and sys.argv[1] == 'default':
        # 使用默认数据（中国 2024 年近似值）
        gdp_growth = 5.2
        interest_rate = 2.5
        debt_to_gdp = 280
        credit_condition = '正常'
    elif len(sys.argv) >= 2 and sys.argv[1] == '--search':
        # 使用搜索获取数据
        gdp_growth = None
        interest_rate = None
        debt_to_gdp = None
        credit_condition = '正常'
        if len(sys.argv) > 2:
            country = sys.argv[2]
    elif len(sys.argv) < 5:
        print("用法：python3 analyze-cycle.py <GDP 增长率%> <利率%> <债务/GDP%> <信贷条件>")
        print("示例：python3 analyze-cycle.py 5.2 2.5 280 正常")
        print("\n或使用默认数据：")
        print("python3 analyze-cycle.py default")
        print("\n或使用 searxng 搜索：")
        print("python3 analyze-cycle.py --search [国家]")
        return 1
    else:
        gdp_growth = float(sys.argv[1])
        interest_rate = float(sys.argv[2])
        debt_to_gdp = float(sys.argv[3])
        credit_condition = sys.argv[4]
    
    if sys.argv[1] == 'default':
        # 使用默认数据（中国 2024 年近似值）
        gdp_growth = 5.2
        interest_rate = 2.5
        debt_to_gdp = 280
        credit_condition = '正常'
    else:
        gdp_growth = float(sys.argv[1])
        interest_rate = float(sys.argv[2])
        debt_to_gdp = float(sys.argv[3])
        credit_condition = sys.argv[4]
    
    if use_search:
        print(f"🔍 搜索 {country} 宏观经济数据...")
    
    result = analyze_cycle(gdp_growth, interest_rate, debt_to_gdp, credit_condition, use_search, country)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

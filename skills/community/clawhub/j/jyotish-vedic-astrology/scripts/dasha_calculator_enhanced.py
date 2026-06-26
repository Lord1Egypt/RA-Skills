#!/usr/bin/env python3
"""
Vedic Astrology Enhanced Dasha Calculator
增强版印度占星大运计算器

Features:
- 精确日期计算（基于Moon在Nakshatra中的精确度数）
- 五级大运联动（Mahadasha → Bhukti → Pratyantar → Sookshma → Prana）
- Transit集成（计算当前Transit对Dasha的影响）
- 事件预测功能
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math

# =============================================================================
# 常量定义
# =============================================================================

# Vimshottari Dasha周期（年）
VIMSHOTTARI_PERIODS = {
    'Ketu': 7,
    'Venus': 20,
    'Sun': 6,
    'Moon': 10,
    'Mars': 7,
    'Rahu': 18,
    'Jupiter': 16,
    'Saturn': 19,
    'Mercury': 17
}

# Dasha顺序
DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

# Nakshatra名称
NAKSHATRA_NAMES = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Nakshatra到Dasha Lord的映射
NAKSHATRA_LORDS = {
    1: 'Ketu', 2: 'Venus', 3: 'Sun', 4: 'Moon', 5: 'Mars', 6: 'Rahu',
    7: 'Jupiter', 8: 'Saturn', 9: 'Mercury',
    10: 'Ketu', 11: 'Venus', 12: 'Sun', 13: 'Moon', 14: 'Mars', 15: 'Rahu',
    16: 'Jupiter', 17: 'Saturn', 18: 'Mercury',
    19: 'Ketu', 20: 'Venus', 21: 'Sun', 22: 'Moon', 23: 'Mars', 24: 'Rahu',
    25: 'Jupiter', 26: 'Saturn', 27: 'Mercury'
}

# 行星现代含义
PLANET_MODERN_MEANINGS = {
    'Sun': {'theme': '自我发展、创业期', 'keywords': ['个人品牌', '创业启动', '自我表达']},
    'Moon': {'theme': '情感成长、内在探索', 'keywords': ['心理成长', '内在探索', '情绪管理']},
    'Mars': {'theme': '行动爆发、竞争期', 'keywords': ['执行力爆发', '竞争激烈', '创业冲动']},
    'Mercury': {'theme': '智力发展、商业期', 'keywords': ['商业谈判', '智力发展', '信息处理']},
    'Jupiter': {'theme': '成长扩张、教育期', 'keywords': ['知识积累', '教育投资', '成长扩张']},
    'Venus': {'theme': '艺术发展、关系期', 'keywords': ['艺术创作', '关系发展', '美学提升']},
    'Saturn': {'theme': '成熟稳定、职业期', 'keywords': ['职业稳定', '长期投资', '成熟稳重']},
    'Rahu': {'theme': '创新突破、非传统期', 'keywords': ['创新突破', '非传统职业', '国际化']},
    'Ketu': {'theme': '灵性探索、内在转化', 'keywords': ['灵性探索', '内在转化', '隐秘研究']}
}

# =============================================================================
# 核心计算函数
# =============================================================================

def calculate_precise_remaining_years(moon_degree: float) -> Dict:
    """
    基于Moon在Nakshatra中的精确度数计算剩余年数
    
    Args:
        moon_degree: Moon在黄道带中的度数（0-360）
    
    Returns:
        Dict with nakshatra info and remaining years
    """
    # 每个Nakshatra占13°20'（800分钟或13.333度）
    nakshatra_size = 360 / 27  # ≈ 13.333度
    
    # 确定Moon所在的Nakshatra（1-27）
    nakshatra_num = int(moon_degree / nakshatra_size) + 1
    if nakshatra_num > 27:
        nakshatra_num = 27
    
    # Moon在该Nakshatra中的位置（度数）
    nakshatra_start = (nakshatra_num - 1) * nakshatra_size
    position_in_nakshatra = moon_degree - nakshatra_start
    
    # 该Nakshatra的Dasha Lord
    lord = NAKSHATRA_LORDS[nakshatra_num]
    
    # 该Lord的总周期
    total_years = VIMSHOTTARI_PERIODS[lord]
    
    # 精确计算剩余年数（基于Moon在Nakshatra中的比例）
    percentage_in_nakshatra = position_in_nakshatra / nakshatra_size
    remaining_years = total_years * (1 - percentage_in_nakshatra)
    
    return {
        'nakshatra_num': nakshatra_num,
        'nakshatra_name': NAKSHATRA_NAMES[nakshatra_num - 1],
        'lord': lord,
        'total_years': total_years,
        'remaining_years': remaining_years,
        'percentage_elapsed': percentage_in_nakshatra * 100
    }


def calculate_dasha_dates(birth_date: datetime, moon_degree: float) -> List[Dict]:
    """
    计算完整的Dasha日期序列
    
    Args:
        birth_date: 出生日期
        moon_degree: Moon在黄道带中的度数
    
    Returns:
        List of Dasha periods with start/end dates
    """
    # 获取起始Dasha信息
    start_info = calculate_precise_remaining_years(moon_degree)
    starting_lord = start_info['lord']
    remaining_years = start_info['remaining_years']
    
    # 构建完整的Dasha序列
    start_index = DASHA_ORDER.index(starting_lord)
    dasha_sequence = []
    
    current_date = birth_date
    first_period = True
    
    for i in range(9):
        planet_index = (start_index + i) % 9
        planet = DASHA_ORDER[planet_index]
        years = VIMSHOTTARI_PERIODS[planet]
        
        if first_period:
            # 第一个周期使用剩余年数
            period_years = remaining_years
            first_period = False
        else:
            period_years = years
        
        start_date = current_date
        end_date = current_date + timedelta(days=period_years * 365.25)
        
        dasha_sequence.append({
            'lord': planet,
            'years': period_years,
            'start_date': start_date,
            'end_date': end_date,
            'theme': PLANET_MODERN_MEANINGS[planet]['theme'],
            'keywords': PLANET_MODERN_MEANINGS[planet]['keywords']
        })
        
        current_date = end_date
    
    return dasha_sequence


def calculate_five_level_dasha(mahadasha_lord: str, years_into_mahadasha: float) -> Dict:
    """
    计算五级大运联动（Mahadasha → Bhukti → Pratyantar → Sookshma → Prana）
    
    Args:
        mahadasha_lord: 当前Mahadasha Lord
        years_into_mahadasha: 进入当前Mahadasha的年数
    
    Returns:
        Dict with all five levels
    """
    def calculate_sub_periods(lord: str, total_years: float, elapsed: float, level_name: str) -> Dict:
        """递归计算子周期"""
        sequence = get_mahadasha_sequence(lord)
        
        years_remaining = elapsed
        current_lord = None
        years_into_period = 0
        
        for planet, years in sequence:
            sub_years = (years / 120) * total_years
            if years_remaining < sub_years:
                current_lord = planet
                years_into_period = years_remaining
                break
            years_remaining -= sub_years
        
        if not current_lord:
            current_lord = sequence[0][0]
            years_into_period = 0
        
        return {
            'lord': current_lord,
            'years_into_period': years_into_period,
            'total_years': (VIMSHOTTARI_PERIODS[current_lord] / 120) * total_years,
            'level': level_name
        }
    
    # Level 1: Mahadasha
    mahadasha_total = VIMSHOTTARI_PERIODS[mahadasha_lord]
    
    # Level 2: Bhukti (Antar Dasha)
    bhukti = calculate_sub_periods(mahadasha_lord, mahadasha_total, years_into_mahadasha, 'Bhukti')
    
    # Level 3: Pratyantar Dasha
    pratyantar = calculate_sub_periods(
        bhukti['lord'], 
        bhukti['total_years'], 
        bhukti['years_into_period'], 
        'Pratyantar'
    )
    
    # Level 4: Sookshma Dasha
    sookshma = calculate_sub_periods(
        pratyantar['lord'],
        pratyantar['total_years'],
        pratyantar['years_into_period'],
        'Sookshma'
    )
    
    # Level 5: Prana Dasha
    prana = calculate_sub_periods(
        sookshma['lord'],
        sookshma['total_years'],
        sookshma['years_into_period'],
        'Prana'
    )
    
    return {
        'mahadasha': {
            'lord': mahadasha_lord,
            'years_into_period': years_into_mahadasha,
            'total_years': mahadasha_total,
            'level': 'Mahadasha'
        },
        'bhukti': bhukti,
        'pratyantar': pratyantar,
        'sookshma': sookshma,
        'prana': prana
    }


def get_mahadasha_sequence(starting_planet: str) -> List[Tuple[str, int]]:
    """获取Mahadasha序列"""
    start_index = DASHA_ORDER.index(starting_planet)
    sequence = []
    for i in range(9):
        planet_index = (start_index + i) % 9
        planet = DASHA_ORDER[planet_index]
        years = VIMSHOTTARI_PERIODS[planet]
        sequence.append((planet, years))
    return sequence


# =============================================================================
# Transit集成
# =============================================================================

def get_current_transit_info() -> Dict:
    """
    获取当前Transit信息（简化版，实际应用需要专业天文计算）
    
    Returns:
        Dict with current transit positions
    """
    # 这里返回示例数据，实际应用需要调用天文计算API
    # 如Swiss Ephemeris或Jagannatha Hora
    today = datetime.now()
    
    # 简化的Transit计算（实际需要精确的天文计算）
    # 这里仅作演示
    return {
        'date': today,
        'jupiter_sign': 'Taurus',  # 示例
        'saturn_sign': 'Aquarius',  # 示例
        'rahu_sign': 'Pisces',  # 示例
        'ketu_sign': 'Virgo',  # 示例
        'note': '实际应用需要专业天文计算API'
    }


def analyze_transit_dasha_interaction(
    dasha_lord: str,
    transit_jupiter_sign: str,
    transit_saturn_sign: str
) -> Dict:
    """
    分析Transit与Dasha的互动
    
    Args:
        dasha_lord: 当前Dasha Lord
        transit_jupiter_sign: Jupiter当前所在星座
        transit_saturn_sign: Saturn当前所在星座
    
    Returns:
        Dict with interaction analysis
    """
    # Jupiter Transit影响（成长、扩张、机会）
    jupiter_effects = {
        'Aries': '自我认知突破、创业机会',
        'Taurus': '财富增长、事业扩张',
        'Gemini': '学习成长、沟通机会',
        'Cancer': '家庭稳定、内在成长',
        'Leo': '个人品牌、领导力提升',
        'Virgo': '工作改善、健康提升',
        'Libra': '关系发展、合作机会',
        'Scorpio': '深度转化、研究突破',
        'Sagittarius': '教育投资、国际视野',
        'Capricorn': '职业稳定、长期规划',
        'Aquarius': '创新突破、社群发展',
        'Pisces': '灵性成长、艺术创作'
    }
    
    # Saturn Transit影响（考验、成熟、责任）
    saturn_effects = {
        'Aries': '自我挑战、行动力考验',
        'Taurus': '财富管理、资产重组',
        'Gemini': '沟通严谨、学习压力',
        'Cancer': '家庭责任、内在考验',
        'Leo': '领导力考验、个人品牌重塑',
        'Virgo': '工作压力、健康考验',
        'Libra': '关系考验、合作重组',
        'Scorpio': '深度转化、危机管理',
        'Sagittarius': '信仰考验、教育压力',
        'Capricorn': '职业巅峰、责任重大',
        'Aquarius': '创新考验、社群责任',
        'Pisces': '灵性考验、隐秘研究'
    }
    
    return {
        'dasha_lord': dasha_lord,
        'jupiter_transit': {
            'sign': transit_jupiter_sign,
            'effect': jupiter_effects.get(transit_jupiter_sign, '成长机会')
        },
        'saturn_transit': {
            'sign': transit_saturn_sign,
            'effect': saturn_effects.get(transit_saturn_sign, '成熟考验')
        },
        'combined_effect': f"Jupiter带来{jupiter_effects.get(transit_jupiter_sign, '成长机会')}，Saturn带来{saturn_effects.get(transit_saturn_sign, '成熟考验')}"
    }


# =============================================================================
# 事件预测
# =============================================================================

def predict_events(
    birth_date: datetime,
    moon_degree: float,
    target_year: int
) -> Dict:
    """
    预测特定年份的事件
    
    Args:
        birth_date: 出生日期
        moon_degree: Moon在黄道带中的度数
        target_year: 目标年份
    
    Returns:
        Dict with event predictions
    """
    # 计算Dasha序列
    dasha_sequence = calculate_dasha_dates(birth_date, moon_degree)
    
    # 找到目标年份对应的Dasha
    target_date = datetime(target_year, 1, 1)
    current_dasha = None
    years_into_mahadasha = 0
    
    for dasha in dasha_sequence:
        if dasha['start_date'] <= target_date < dasha['end_date']:
            current_dasha = dasha
            years_into_mahadasha = (target_date - dasha['start_date']).days / 365.25
            break
    
    if not current_dasha:
        return {'error': 'Target year out of Dasha range'}
    
    # 计算五级Dasha
    five_levels = calculate_five_level_dasha(current_dasha['lord'], years_into_mahadasha)
    
    # 预测事件类型
    event_predictions = {
        'career': predict_career_events(five_levels),
        'relationship': predict_relationship_events(five_levels),
        'wealth': predict_wealth_events(five_levels),
        'health': predict_health_events(five_levels)
    }
    
    return {
        'target_year': target_year,
        'dasha': current_dasha,
        'five_levels': five_levels,
        'predictions': event_predictions
    }


def predict_career_events(five_levels: Dict) -> Dict:
    """预测事业事件"""
    lord = five_levels['mahadasha']['lord']
    
    career_themes = {
        'Sun': {'events': ['创业机会', '领导力提升', '个人品牌建设'], 'timing': '高'},
        'Moon': {'events': ['职业转型', '内在探索', '情绪管理'], 'timing': '中'},
        'Mars': {'events': ['行动爆发', '竞争激烈', '创业冲动'], 'timing': '高'},
        'Mercury': {'events': ['商业谈判', '技能提升', '信息处理'], 'timing': '高'},
        'Jupiter': {'events': ['职业扩张', '教育投资', '国际视野'], 'timing': '高'},
        'Venus': {'events': ['艺术创作', '关系发展', '美学提升'], 'timing': '中'},
        'Saturn': {'events': ['职业稳定', '长期规划', '责任重大'], 'timing': '高'},
        'Rahu': {'events': ['创新突破', '非传统职业', '国际化'], 'timing': '高'},
        'Ketu': {'events': ['灵性探索', '内在转化', '隐秘研究'], 'timing': '低'}
    }
    
    return career_themes.get(lord, {'events': [], 'timing': '未知'})


def predict_relationship_events(five_levels: Dict) -> Dict:
    """预测关系事件"""
    lord = five_levels['mahadasha']['lord']
    bhukti_lord = five_levels['bhukti']['lord']
    
    # Venus、Moon、Jupiter是关系相关行星
    relationship_planets = ['Venus', 'Moon', 'Jupiter']
    
    if lord in relationship_planets or bhukti_lord in relationship_planets:
        return {
            'events': ['关系发展', '婚姻机会', '合作机会'],
            'timing': '高',
            'note': f'{lord}大运 + {bhukti_lord}小运，关系领域活跃'
        }
    else:
        return {
            'events': ['关系稳定', '内在反思'],
            'timing': '低',
            'note': f'{lord}大运，关系领域不是重点'
        }


def predict_wealth_events(five_levels: Dict) -> Dict:
    """预测财富事件"""
    lord = five_levels['mahadasha']['lord']
    
    wealth_planets = {
        'Jupiter': {'events': ['财富扩张', '投资机会', '教育投资'], 'timing': '高'},
        'Venus': {'events': ['艺术收入', '美学变现', '关系财富'], 'timing': '高'},
        'Mercury': {'events': ['商业收入', '技能变现', '信息变现'], 'timing': '高'},
        'Saturn': {'events': ['长期投资', '稳定收入', '资产管理'], 'timing': '中'}
    }
    
    return wealth_planets.get(lord, {'events': ['财富稳定'], 'timing': '低'})


def predict_health_events(five_levels: Dict) -> Dict:
    """预测健康事件"""
    lord = five_levels['mahadasha']['lord']
    
    health_themes = {
        'Sun': {'events': ['活力提升', '自我关注'], 'timing': '中'},
        'Moon': {'events': ['情绪管理', '心理健康'], 'timing': '高'},
        'Mars': {'events': ['运动增加', '能量爆发'], 'timing': '高'},
        'Saturn': {'events': ['慢性管理', '长期规划'], 'timing': '中'},
        'Ketu': {'events': ['灵性健康', '内在转化'], 'timing': '中'}
    }
    
    return health_themes.get(lord, {'events': ['健康稳定'], 'timing': '低'})


# =============================================================================
# 主函数和示例
# =============================================================================

def print_comprehensive_report(birth_date: datetime, moon_degree: float, current_date: datetime = None):
    """
    打印综合报告
    """
    if current_date is None:
        current_date = datetime.now()
    
    # 计算年龄
    age = (current_date - birth_date).days / 365.25
    
    # 计算Dasha序列
    dasha_sequence = calculate_dasha_dates(birth_date, moon_degree)
    
    # 找到当前Dasha
    current_dasha = None
    years_into_mahadasha = 0
    
    for dasha in dasha_sequence:
        if dasha['start_date'] <= current_date < dasha['end_date']:
            current_dasha = dasha
            years_into_mahadasha = (current_date - dasha['start_date']).days / 365.25
            break
    
    # 计算五级Dasha
    five_levels = calculate_five_level_dasha(current_dasha['lord'], years_into_mahadasha)
    
    # 打印报告
    print("=" * 70)
    print("印度占星大运分析报告")
    print("=" * 70)
    print(f"出生日期: {birth_date.strftime('%Y-%m-%d')}")
    print(f"Moon度数: {moon_degree:.2f}°")
    print(f"当前日期: {current_date.strftime('%Y-%m-%d')}")
    print(f"当前年龄: {age:.1f}岁")
    print("-" * 70)
    
    print("\n【五级大运联动】")
    for level_name, level_info in five_levels.items():
        print(f"  {level_info['level']}: {level_info['lord']}")
        print(f"    进度: {level_info['years_into_period']:.2f} / {level_info['total_years']:.2f}年")
    
    print("\n【当前大运主题】")
    print(f"  {current_dasha['lord']}大运: {current_dasha['theme']}")
    print(f"  关键词: {', '.join(current_dasha['keywords'])}")
    
    print("\n【事件预测】")
    predictions = predict_events(birth_date, moon_degree, current_date.year)
    for category, pred in predictions['predictions'].items():
        print(f"  {category}: {pred['events']} (时机: {pred['timing']})")
    
    print("=" * 70)


if __name__ == "__main__":
    # 示例：Obama的星盘
    # 出生：1961-08-04 19:24
    # Moon在金牛座（约50度）
    print("示例1：Barack Obama")
    print_comprehensive_report(
        birth_date=datetime(1961, 8, 4, 19, 24),
        moon_degree=50.0,  # 金牛座约50度
        current_date=datetime(2026, 4, 22)
    )
    
    print("\n\n")
    
    # 示例2：测试用例
    print("示例2：测试用例（Moon在Rohini）")
    print_comprehensive_report(
        birth_date=datetime(1990, 1, 1, 12, 0),
        moon_degree=53.0,  # Rohini Nakshatra
        current_date=datetime(2026, 4, 22)
    )

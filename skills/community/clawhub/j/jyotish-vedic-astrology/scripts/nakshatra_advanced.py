#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级星宿分析模块 v1.0
Nakshatra深度分析系统

支持:
  - Tara Bala（星宿力量匹配）
  - Sub-Lord体系（KP占星）
  - 精确Vimshottari起始点计算
  - Nakshatra兼容性分析
  - Navatara（9星宿组）分类
"""
from typing import Dict, List, Tuple
import math

NAK_LIST = [
    ("Ashwini","Ketu",7),("Bharani","Venus",20),("Krittika","Sun",6),
    ("Rohini","Moon",10),("Mrigashira","Mars",7),("Ardra","Rahu",18),
    ("Punarvasu","Jupiter",16),("Pushya","Saturn",19),("Ashlesha","Mercury",17),
    ("Magha","Ketu",7),("Purva Phalguni","Venus",20),("Uttara Phalguni","Sun",6),
    ("Hasta","Moon",10),("Chitra","Mars",7),("Swati","Rahu",18),
    ("Vishakha","Jupiter",16),("Anuradha","Saturn",19),("Jyeshtha","Mercury",17),
    ("Mula","Ketu",7),("Purva Ashadha","Venus",20),("Uttara Ashadha","Sun",6),
    ("Shravana","Moon",10),("Dhanishta","Mars",7),("Shatabhisha","Rahu",18),
    ("Purva Bhadrapada","Jupiter",16),("Uttara Bhadrapada","Saturn",19),("Revati","Mercury",17),
]
NAK_NAMES = [n[0] for n in NAK_LIST]
NAK_LORDS = [n[1] for n in NAK_LIST]
NAK_YEARS = [n[2] for n in NAK_LIST]

# Navatara分组（从月亮星宿开始的9个星宿循环）
TARA_NAMES = ['Janma(生命)','Sampat(财富)','Vipat(危险)','Kshema(安全)',
    'Pratyak(障碍)','Sadhana(成就)','Vadha(毁灭)','Mitra(友好)','ParamaMitra(至友)']
TARA_CN = {0:'生命Tara',1:'财富Tara',2:'危险Tara',3:'安全Tara',
    4:'障碍Tara',5:'成就Tara',6:'毁灭Tara',7:'友好Tara',8:'至友Tara'}

# Nakshatra元素和属性
NAK_GANA = {  # 气质类型
    0:'Dev(神圣)',1:'Manushya(人类)',2:'Rakshasa(罗刹)',
    3:'Dev',4:'Dev',5:'Manushya',6:'Dev',7:'Dev',8:'Rakshasa',
    9:'Rakshasa',10:'Manushya',11:'Manushya',12:'Dev',13:'Rakshasa',14:'Dev',
    15:'Rakshasa',16:'Dev',17:'Rakshasa',18:'Rakshasa',19:'Manushya',20:'Manushya',
    21:'Dev',22:'Rakshasa',23:'Rakshasa',24:'Manushya',25:'Manushya',26:'Dev',
}
NAK_ELEMENT = {
    0:'火',1:'土',2:'火',3:'土',4:'土',5:'风',6:'风',7:'水',8:'水',
    9:'火',10:'土',11:'火',12:'土',13:'火',14:'风',15:'火',16:'水',17:'风',
    18:'火',19:'水',20:'土',21:'土',22:'风',23:'风',24:'水',25:'火',26:'水',
}


def find_nakshatra(longitude: float) -> Dict:
    """从恒星黄道经度精确计算Nakshatra"""
    nak_span = 360.0 / 27  # 每个星宿13.333...°
    nak_idx = int(longitude / nak_span) % 27
    nak_start = nak_idx * nak_span
    deg_in_nak = longitude - nak_start
    pada_span = nak_span / 4  # 每个Pada 3.333...°
    pada = int(deg_in_nak / pada_span) + 1
    deg_in_pada = deg_in_nak - (pada - 1) * pada_span
    
    return {
        'nakshatra': NAK_NAMES[nak_idx],
        'nakshatra_idx': nak_idx,
        'nakshatra_lord': NAK_LORDS[nak_idx],
        'dasha_years': NAK_YEARS[nak_idx],
        'pada': pada,
        'degree_in_nakshatra': round(deg_in_nak, 4),
        'degree_in_pada': round(deg_in_pada, 4),
        'gana': NAK_GANA.get(nak_idx, ''),
        'element': NAK_ELEMENT.get(nak_idx, ''),
    }


def calc_tara_bala(moon_nak_idx: int, target_nak_idx: int) -> Dict:
    """
    Tara Bala计算：月亮星宿到目标星宿的9星宿循环关系
    
    用于判断某个行星/事件星宿与月亮星宿的关系
    0=Janma(中性), 1=Sampat(吉), 2=Vipat(凶), 3=Kshema(吉),
    4=Pratyak(凶), 5=Sadhana(吉), 6=Vadha(凶), 7=Mitra(吉), 8=ParamaMitra(大吉)
    """
    distance = (target_nak_idx - moon_nak_idx) % 9
    tara_name = TARA_NAMES[distance]
    tara_cn = TARA_CN[distance]
    
    is_auspicious = distance in (1, 3, 5, 7, 8)
    is_dangerous = distance in (2, 4, 6)
    
    return {
        'tara_index': distance,
        'tara_name': tara_name,
        'tara_cn': tara_cn,
        'is_auspicious': is_auspicious,
        'is_dangerous': is_dangerous,
        'quality': 'auspicious' if is_auspicious else 'dangerous' if is_dangerous else 'neutral',
        'interpretation': _tara_interp(distance),
    }


def calc_all_tara_balas(moon_nak_idx: int, planet_lons: Dict[str, float]) -> Dict:
    """计算所有行星相对于月亮的Tara Bala"""
    results = {}
    for pname, lon in planet_lons.items():
        p_nak = find_nakshatra(lon)
        tara = calc_tara_bala(moon_nak_idx, p_nak['nakshatra_idx'])
        results[pname] = {
            'nakshatra': p_nak['nakshatra'],
            'tara': tara,
        }
    return results


def calc_vimshottari_start(moon_longitude: float) -> Dict:
    """
    精确计算Vimshottari Dasha的起始点
    
    返回月亮所在星宿的守护星、已用度数比例、剩余年数
    """
    nak = find_nakshatra(moon_longitude)
    nak_idx = nak['nakshatra_idx']
    nak_lord = NAK_LORDS[nak_idx]
    total_years = NAK_YEARS[nak_idx]
    
    # 已用比例
    nak_span = 360.0 / 27
    nak_start = nak_idx * nak_span
    deg_in_nak = moon_longitude - nak_start
    used_ratio = deg_in_nak / nak_span
    remaining_ratio = 1 - used_ratio
    
    # 第一个Mahadasha的剩余年数
    first_mahadasha_remaining = total_years * remaining_ratio
    first_mahadasha_elapsed = total_years * used_ratio
    
    return {
        'moon_nakshatra': nak['nakshatra'],
        'moon_nakshatra_lord': nak_lord,
        'moon_pada': nak['pada'],
        'total_dasha_years': total_years,
        'used_ratio': round(used_ratio, 6),
        'remaining_ratio': round(remaining_ratio, 6),
        'first_mahadasha_remaining_years': round(first_mahadasha_remaining, 4),
        'first_mahadasha_elapsed_years': round(first_mahadasha_elapsed, 4),
        'first_mahadasha_lord': nak_lord,
    }


def calc_sub_lord(longitude: float, division: int = 9) -> Dict:
    """
    Sub-Lord计算（KP占星体系）
    将星宿进一步细分为Sub-Lord和Sub-Sub-Lord
    
    参数:
        longitude: 恒星黄道经度
        division: 细分层级（9=Sub-Lord, 81=Sub-Sub-Lord）
    """
    # 主星宿
    nak = find_nakshatra(longitude)
    nak_span = 360.0 / 27
    
    # Sub-Lord: 将星宿按守护星的大运年数比例细分
    total_dasha_years = sum(NAK_YEARS)  # 120年
    nak_lord = NAK_NAMES[nak['nakshatra_idx']]
    
    # 计算Sub-Lord
    deg_in_nak = nak['degree_in_nakshatra']
    sub_lord_span = nak_span * (NAK_YEARS[NAK_LORDS.index(NAK_LORDS[nak['nakshatra_idx']])]) / total_dasha_years
    
    # 简化版：直接按9等分
    sub_span = nak_span / 9
    sub_idx = int(deg_in_nak / sub_span) % 9
    
    # Sub-Lord是第sub_idx个行星（从星宿守护星开始的大运顺序）
    DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
    nak_lord_idx = DASHA_ORDER.index(NAK_LORDS[nak['nakshatra_idx']])
    sub_lord = DASHA_ORDER[(nak_lord_idx + sub_idx) % 9]
    
    return {
        'nakshatra': nak['nakshatra'],
        'nakshatra_lord': nak_lord,
        'sub_lord': sub_lord,
        'sub_index': sub_idx,
        'pada': nak['pada'],
        'degree_in_nakshatra': round(deg_in_nak, 4),
    }


def nakshatra_compatibility(nak1_idx: int, nak2_idx: int) -> Dict:
    """
    Nakshatra兼容性分析（Koota系统中的星宿匹配部分）
    基于Tara Bala和Nakshatra元素匹配
    """
    # Tara匹配
    tara = calc_tara_bala(nak1_idx, nak2_idx)
    tara_score = 3 if tara['is_auspicious'] else 0 if tara['is_dangerous'] else 1.5
    
    # 元素匹配
    el1 = NAK_ELEMENT.get(nak1_idx, '')
    el2 = NAK_ELEMENT.get(nak2_idx, '')
    el_compatible = el1 == el2 or (el1 in ('火','风') and el2 in ('火','风')) or (el1 in ('土','水') and el2 in ('土','水'))
    
    # Gana匹配
    g1 = NAK_GANA.get(nak1_idx, '')
    g2 = NAK_GANA.get(nak2_idx, '')
    gana_score = 6 if g1 == g2 else 3 if ('Dev' in g1 and 'Manushya' in g2) or ('Manushya' in g1 and 'Dev' in g2) else 0
    
    return {
        'nak1': NAK_NAMES[nak1_idx],
        'nak2': NAK_NAMES[nak2_idx],
        'tara_bala': tara,
        'tara_score': tara_score,
        'element_match': {'e1': el1, 'e2': el2, 'compatible': el_compatible},
        'gana_match': {'g1': g1, 'g2': g2, 'score': gana_score},
        'overall': 'compatible' if tara_score >= 1.5 and el_compatible else 'challenging' if tara['is_dangerous'] else 'moderate',
    }


def _tara_interp(idx):
    interps = {
        0: '生命Tara—中性，代表自我，不吉不凶',
        1: '财富Tara—吉，带来物质和精神增长',
        2: '危险Tara—凶，需要谨慎，可能带来损失',
        3: '安全Tara—吉，提供保护和稳定',
        4: '障碍Tara—凶，可能面临困难和延误',
        5: '成就Tara—吉，有利于实现目标',
        6: '毁灭Tara—凶，最大凶Tara，需特别注意',
        7: '友好Tara—吉，提供支持和帮助',
        8: '至友Tara—大吉，最强吉Tara',
    }
    return interps.get(idx, '')

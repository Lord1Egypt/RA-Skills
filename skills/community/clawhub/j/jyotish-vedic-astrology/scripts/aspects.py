#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
吠陀占星精确相位模块 v1.0
基于度数的Drishti（相位）计算系统

支持:
  - 标准7宫对冲相位
  - 特殊相位: Mars(4/7/8), Jupiter(5/7/9), Saturn(3/7/10)
  - 度数容许度（orb）: 紧密/中等/松散三级
  - 入相位(applying)/出相位(separating)判断
  - 合相(conjunction)精度分析
"""
from typing import Dict, List, Tuple, Optional

# 标准容许度（度）
DEFAULT_ORBS = {
    'Sun': 10, 'Moon': 10, 'Mars': 8, 'Mercury': 7,
    'Jupiter': 9, 'Venus': 7, 'Saturn': 9, 'Rahu': 8, 'Ketu': 8,
    'default': 7
}
ORBIT_CATEGORIES = {
    'tight': 3,      # 紧密相位（最强）
    'moderate': 6,   # 中等相位
    'loose': 10,     # 松散相位（最弱）
}

# 特殊相位规则（从行星所在宫位算起）
SPECIAL_ASPECTS = {
    'Mars': [4, 7, 8],
    'Jupiter': [5, 7, 9],
    'Saturn': [3, 7, 10],
}
# 所有行星都有7宫相位
ALL_HAVE_7TH = True


def calc_all_aspects(planet_longitudes: Dict[str, float], 
                     ascendant_longitude: float) -> Dict:
    """
    计算所有行星之间的精确相位关系
    
    参数:
        planet_longitudes: {'Sun': 12.5, 'Moon': 45.3, ...} 恒星黄道经度
        ascendant_longitude: 上升点经度
    
    返回: {
        'aspects': [每对行星的相位详情],
        'conjunctions': [合相详情],
        'asc_aspects': [上升点被哪些星相位],
        'tight_aspects': [紧密相位（<3°）],
        'summary': 统计摘要
    }
    """
    planets = {k: v for k, v in planet_longitudes.items() 
               if k not in ('Ketu',) and isinstance(v, (int, float))}
    # Ketu = Rahu + 180
    if 'Rahu' in planet_longitudes and 'Ketu' not in planets:
        planets['Ketu'] = (planet_longitudes['Rahu'] + 180) % 360
    
    aspects = []
    conjunctions = []
    tight_aspects = []
    planet_names = list(planets.keys())
    
    for i, p1 in enumerate(planet_names):
        for j, p2 in enumerate(planet_names):
            if j <= i:
                continue
            lon1, lon2 = planets[p1], planets[p2]
            pair_aspects = _calc_pair_aspects(p1, lon1, p2, lon2)
            for asp in pair_aspects:
                aspects.append(asp)
                if asp['type'] == 'conjunction':
                    conjunctions.append(asp)
                if asp['orb'] <= ORBIT_CATEGORIES['tight']:
                    tight_aspects.append(asp)
    
    # 上升点相位
    asc_aspects = []
    for pname, plon in planets.items():
        diff = abs(ascendant_longitude - plon) % 360
        if diff > 180: diff = 360 - diff
        if diff <= 15:  # 上升点容许度
            asc_aspects.append({
                'planet': pname, 'degree_diff': round(diff, 2),
                'orb_category': _orb_category(diff, 15),
                'applying': plon > ascendant_longitude,  # 简化判断
            })
    
    return {
        'aspects': aspects,
        'conjunctions': conjunctions,
        'tight_aspects': tight_aspects,
        'asc_aspects': asc_aspects,
        'summary': {
            'total_aspects': len(aspects),
            'conjunctions': len(conjunctions),
            'tight_aspects': len(tight_aspects),
            'by_type': _count_by_type(aspects),
        }
    }


def _calc_pair_aspects(p1, lon1, p2, lon2) -> List[Dict]:
    """计算两颗行星之间的所有相位"""
    results = []
    diff = (lon2 - lon1) % 360
    if diff > 180:
        diff = 360 - diff
    
    # 1. 合相 (conjunction): 同一星座内或跨星座但距离很近
    max_conj_orb = max(DEFAULT_ORBS.get(p1, 7), DEFAULT_ORBS.get(p2, 7))
    if diff <= max_conj_orb:
        results.append({
            'planet1': p1, 'planet2': p2,
            'type': 'conjunction', 'aspect_degree': 0,
            'actual_diff': round(diff, 2), 'orb': round(diff, 2),
            'orb_category': _orb_category(diff, max_conj_orb),
            'applying': (lon2 - lon1) % 360 < 180,
            'strength': _aspect_strength(diff, max_conj_orb),
            'description': f"{p1}与{p2}合相（差距{diff:.1f}°）"
        })
    
    # 2. 对冲 (opposition): 7宫相位
    opp_diff = abs(diff - 180)
    opp_orb = max(DEFAULT_ORBS.get(p1, 7), DEFAULT_ORBS.get(p2, 7))
    if opp_diff <= opp_orb and diff > max_conj_orb:
        results.append({
            'planet1': p1, 'planet2': p2,
            'type': 'opposition', 'aspect_degree': 180,
            'actual_diff': round(diff, 2), 'orb': round(opp_diff, 2),
            'orb_category': _orb_category(opp_diff, opp_orb),
            'applying': (lon2 - lon1) % 360 < 180,
            'strength': _aspect_strength(opp_diff, opp_orb),
            'description': f"{p1}对冲{p2}（差距{opp_diff:.1f}°）"
        })
    
    # 3. 特殊相位
    for planet, aspect_degrees in SPECIAL_ASPECTS.items():
        if planet == p1:
            for asp_deg in aspect_degrees:
                if asp_deg == 7:
                    continue  # 已在对冲中处理
                target = asp_deg * 30  # 转换为度数（每宫30°）
                asp_diff = abs(diff - target)
                if asp_diff > 180: asp_diff = 360 - asp_diff
                asp_orb = 8  # 特殊相位容许度
                if asp_diff <= asp_orb:
                    results.append({
                        'planet1': p1, 'planet2': p2,
                        'type': f'{planet}_aspect_{asp_deg}',
                        'aspect_degree': target,
                        'actual_diff': round(diff, 2), 'orb': round(asp_diff, 2),
                        'orb_category': _orb_category(asp_diff, asp_orb),
                        'applying': (lon2 - lon1) % 360 < 180,
                        'strength': _aspect_strength(asp_diff, asp_orb),
                        'description': f"{p1}({asp_deg}宫相位){p2}（差距{asp_diff:.1f}°）"
                    })
    
    return results


def calc_house_aspects(planet_lon: float, planet_name: str, 
                       asc_lon: float) -> Dict:
    """计算单颗行星对所有12宫的相位"""
    planet_sign = int(planet_lon / 30) % 12
    asc_sign = int(asc_lon / 30) % 12
    planet_house = ((planet_sign - asc_sign) % 12) + 1
    
    aspect_houses = [7]  # 所有行星都有7宫相位
    if planet_name in SPECIAL_ASPECTS:
        aspect_houses = SPECIAL_ASPECTS[planet_name]
    
    result = {'planet': planet_name, 'house': planet_house, 'aspects_to': {}}
    for ah in aspect_houses:
        target_house = ((planet_house - 1 + ah - 1) % 12) + 1
        result['aspects_to'][target_house] = {
            'from_house': planet_house,
            'aspect_type': f'{ah}宫相位',
            'is_special': ah != 7,
        }
    return result


def _orb_category(diff, max_orb):
    if diff <= ORBIT_CATEGORIES['tight']: return 'tight'
    if diff <= ORBIT_CATEGORIES['moderate']: return 'moderate'
    return 'loose'


def _aspect_strength(diff, max_orb):
    """相位强度评分 0-100"""
    if diff == 0: return 100
    ratio = diff / max_orb
    return max(0, round(100 * (1 - ratio), 1))


def _count_by_type(aspects):
    counts = {}
    for a in aspects:
        t = a['type']
        counts[t] = counts.get(t, 0) + 1
    return counts

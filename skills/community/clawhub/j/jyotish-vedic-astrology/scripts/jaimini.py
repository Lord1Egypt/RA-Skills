#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jaimini占星体系模块 v1.0
Parashara传承中的Jaimini子系统

支持:
  - Chara Karaka: 7/8个功能指示星（按度数排序）
  - Chara Dasha: 基于星座的大运系统
  - Karakamsha: AK在Navamsa中的上升（灵魂方向）
  - Jaimini Sutras关键规则
"""
from typing import Dict, List, Tuple, Optional
import math

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_LORDS = {'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury','Cancer':'Moon',
    'Leo':'Sun','Virgo':'Mercury','Libra':'Venus','Scorpio':'Mars',
    'Sagittarius':'Jupiter','Capricorn':'Saturn','Aquarius':'Saturn','Pisces':'Jupiter'}

# Chara Karaka 定义（7星制，排除Rahu）
KARAKA_7 = {
    1: 'Atmakaraka',    # AK - 灵魂指示星（度数最高）
    2: 'Amatyakaraka',  # AmK - 事业/顾问
    3: 'Bhratrikaraka', # BK - 兄弟/勇气
    4: 'Matrikaraka',   # MK - 母亲
    5: 'Putrakaraka',   # PK - 子女
    6: 'Gnatikaraka',   # GK - 敌人/障碍
    7: 'Darakaraka',    # DK - 配偶（度数最低）
}

# 8星制（含Rahu，用绝对度数）
KARAKA_8 = {
    1: 'Atmakaraka', 2: 'Amatyakaraka', 3: 'Bhratrikaraka', 4: 'Matrikaraka',
    5: 'Putrakaraka', 6: 'Gnatikaraka', 7: 'Darakaraka', 8: 'Pitrukaraka',
}

KARAKA_CN = {
    'Atmakaraka': '灵魂星AK', 'Amatyakaraka': '事业星AmK',
    'Bhratrikaraka': '兄弟星BK', 'Matrikaraka': '母亲星MK',
    'Putrakaraka': '子女星PK', 'Gnatikaraka': '障碍星GK',
    'Darakaraka': '配偶星DK', 'Pitrukaraka': '父亲星PiK',
}

KARAKA_DOMAINS = {
    'Atmakaraka': '灵魂使命、核心自我、人生最高目标',
    'Amatyakaraka': '事业方向、主要谋士、权力代理',
    'Bhratrikaraka': '兄弟姐妹、勇气、冒险精神',
    'Matrikaraka': '母亲、家庭根基、情感安全感',
    'Putrakaraka': '子女、创造力、学生、智能成果',
    'Gnatikaraka': '竞争对手、疾病、障碍、转化力量',
    'Darakaraka': '配偶特质、伴侣关系、婚姻质量',
    'Pitrukaraka': '父亲、祖先业力、传统传承',
}


def calc_chara_karaka_7(planet_degrees: Dict[str, float]) -> Dict:
    """
    计算7星制Chara Karaka（度数最高→AK，最低→DK）
    
    参数: planet_degrees = {'Sun': 12.5, 'Moon': 8.3, ...}
          每个行星在星座内的度数（0-30）
    
    返回: {karaka_name: {'planet': str, 'degree': float, 'domain': str}}
    """
    # 排除Rahu和Ketu
    exclude = {'Rahu', 'Ketu'}
    planets = {k: v for k, v in planet_degrees.items() if k not in exclude}
    
    # 按度数降序排列（度数最高的=AK）
    sorted_planets = sorted(planets.items(), key=lambda x: x[1], reverse=True)
    
    results = {}
    for rank, (pname, deg) in enumerate(sorted_planets, 1):
        if rank > 7:
            break
        karaka = KARAKA_7[rank]
        results[karaka] = {
            'planet': pname,
            'degree_in_sign': round(deg, 4),
            'rank': rank,
            'domain': KARAKA_DOMAINS.get(karaka, ''),
            'cn_name': KARAKA_CN.get(karaka, karaka),
        }
    
    # 额外分析
    ak = results.get('Atmakaraka', {})
    dk = results.get('Darakaraka', {})
    
    return {
        'karaka_table': results,
        'summary': {
            'AK': f"{ak.get('planet','?')} ({ak.get('degree_in_sign',0):.1f}°)",
            'DK': f"{dk.get('planet','?')} ({dk.get('degree_in_sign',0):.1f}°)",
            'AK_domain': ak.get('domain', ''),
            'DK_domain': dk.get('domain', ''),
        }
    }


def calc_chara_karaka_8(planet_degrees: Dict[str, float]) -> Dict:
    """
    计算8星制Chara Karaka（含Rahu，使用30-度数来处理Rahu逆行）
    """
    planets = {}
    for pname, deg in planet_degrees.items():
        if pname == 'Ketu':
            continue
        if pname == 'Rahu':
            # Rahu直接使用星座内度数（与其它行星相同），不做取反
            planets[pname] = deg
        else:
            planets[pname] = deg
    
    sorted_planets = sorted(planets.items(), key=lambda x: x[1], reverse=True)
    
    results = {}
    for rank, (pname, deg) in enumerate(sorted_planets, 1):
        if rank > 8:
            break
        karaka = KARAKA_8[rank]
        results[karaka] = {
            'planet': pname,
            'degree_in_sign': round(deg, 4),
            'rank': rank,
            'domain': KARAKA_DOMAINS.get(karaka, ''),
            'cn_name': KARAKA_CN.get(karaka, karaka),
        }
    
    return {'karaka_table_8': results}


def calc_chara_dasha(asc_sign_idx: int, 
                     planet_longitudes: Dict[str, float],
                     birth_year: int, birth_month: int) -> Dict:
    """
    Chara Dasha计算（基于星座的大运系统）
    
    规则:
      - 从上升星座开始
      - 奇数星座（Aries, Gemini...）：正向顺序
      - 偶数星座（Taurus, Cancer...）：反向顺序
      - 每个大运长度 = 12 - 该星座内的行星数量（用特定规则）
      - 标准版：每个大运固定1-12年
    """
    # 确定顺序方向
    is_odd = asc_sign_idx % 2 == 0
    direction = 1 if is_odd else -1
    
    # 生成大运序列
    dasha_sequence = []
    current = asc_sign_idx
    
    # 标准Chara Dasha: 每个星座1年，按正/反向排列
    for i in range(12):
        sign_idx = (current + direction * i) % 12
        sign_name = SIGNS[sign_idx]
        lord = SIGN_LORDS[sign_name]
        
        # 大运长度计算（简化版：基于星座的默认年数）
        # 标准法：大运长度 = 基于该星座中行星的Karakamsa计算
        # 简化法：每个大运1年
        duration = _chara_dasha_duration(sign_idx, planet_longitudes)
        
        dasha_sequence.append({
            'sign': sign_name,
            'sign_idx': sign_idx,
            'lord': lord,
            'duration_years': duration,
            'order': i + 1,
        })
    
    # 计算日期
    total_years = sum(d['duration_years'] for d in dasha_sequence)
    current_year = birth_year
    current_month = birth_month
    
    for d in dasha_sequence:
        d['start_date'] = f"{current_year}-{current_month:02d}"
        end_month = current_month + int(d['duration_years'] * 12)
        end_year = current_year + end_month // 12
        end_month = end_month % 12
        if end_month == 0:
            end_month = 12
            end_year -= 1
        d['end_date'] = f"{end_year}-{end_month:02d}"
        current_year = end_year
        current_month = end_month + 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    return {
        'ascendant': SIGNS[asc_sign_idx],
        'direction': 'forward' if is_odd else 'backward',
        'dasha_sequence': dasha_sequence,
        'total_years': total_years,
    }


def calc_chara_dasha_with_antardasha(asc_sign_idx: int,
                                      planet_longitudes: Dict[str, float],
                                      birth_year: int, birth_month: int) -> Dict:
    """
    Chara Dasha 计算含 Antardasha 子周期

    Antardasha 规则:
      - 在每个 Mahadasha 内，Antardasha 从 Mahadasha 星座开始
      - 方向与 Mahadasha 方向相同
      - 每个 Antardasha 时长 = (该子星座大运年数 / 总大运年数) * Mahadasha 年数
      - 生成 12 个 Antardasha
    """
    # 先算 Mahadasha
    base = calc_chara_dasha(asc_sign_idx, planet_longitudes, birth_year, birth_month)
    is_odd = asc_sign_idx % 2 == 0
    direction = 1 if is_odd else -1
    base_total = sum(_chara_dasha_duration((asc_sign_idx + direction * i) % 12, planet_longitudes) for i in range(12))

    # 为每个 Mahadasha 计算 Antardasha
    for md in base['dasha_sequence']:
        md_sign_idx = md['sign_idx']
        md_duration = md['duration_years']
        antardasha_list = []

        # Antardasha 也从该 Mahadasha 星座开始，同方向
        for j in range(12):
            ad_sign_idx = (md_sign_idx + direction * j) % 12
            ad_sign = SIGNS[ad_sign_idx]
            ad_lord = SIGN_LORDS[ad_sign]

            # 子周期时长 = (该星座独立年数 / 总年数) * Mahadasha 年数
            ad_independent_duration = _chara_dasha_duration(ad_sign_idx, planet_longitudes)
            ad_duration = round((ad_independent_duration / base_total) * md_duration, 2)
            if ad_duration < 0.01:
                ad_duration = 0.01  # 最小约4天

            antardasha_list.append({
                'sign': ad_sign,
                'sign_idx': ad_sign_idx,
                'lord': ad_lord,
                'duration_years': ad_duration,
                'order': j + 1,
            })

        # 计算 Antardasha 日期
        start_year, start_month = map(int, md['start_date'].split('-'))
        for ad in antardasha_list:
            ad['start_date'] = f"{start_year}-{start_month:02d}"
            total_months = round(ad['duration_years'] * 12)
            end_month = start_month + total_months
            end_year = start_year + (end_month - 1) // 12
            end_month = ((end_month - 1) % 12) + 1
            ad['end_date'] = f"{end_year}-{end_month:02d}"
            # 下一个 Antardasha 的开始
            if end_month < 12:
                start_year = end_year
                start_month = end_month + 1
            else:
                start_year = end_year + 1
                start_month = 1

        md['antardashas'] = antardasha_list

    base['has_antardasha'] = True
    return base


def _chara_dasha_duration(sign_idx, planet_lons):
    """计算Chara Dasha单个大运的年数"""
    # 标准方法：12 - 落入该星座的行星数量（最少1年，最多12年）
    count = 0
    for pname, lon in planet_lons.items():
        if pname in ('Rahu', 'Ketu'):
            continue
        p_sign = int(lon / 30) % 12
        if p_sign == sign_idx:
            count += 1
    return max(1, 12 - count)


def calc_karakamsha(ak_sign_in_d9: str, ak_degree_in_d9: float) -> Dict:
    """
    Karakamsha分析：AK（Atmakaraka，灵魂星）在D9中的位置作为"灵魂上升"
    这是Jaimini体系中判断人生终极方向的关键技法
    
    经典定义：Karakamsha = Atmakaraka在Navamsa(D9)中落入的星座
    从这个星座看12宫的布局，分析灵魂方向
    
    ⚠️ 2026-05-03修正：此前版本错误使用DK（配偶星），现已修正为AK（灵魂星）
    
    参数:
        ak_sign_in_d9: AK（灵魂星）在D9中的星座
        ak_degree_in_d9: AK在D9中的度数
    """
    sign_idx = SIGNS.index(ak_sign_in_d9) if ak_sign_in_d9 in SIGNS else 0
    lord = SIGN_LORDS.get(ak_sign_in_d9, '')
    
    # Karakamsha Lagna = AK（灵魂星）在D9中的位置
    # 从这个位置看12宫的布局，分析灵魂方向
    interpretations = _karakamsha_interpretations(ak_sign_in_d9, lord)
    
    return {
        'karakamsha_sign': ak_sign_in_d9,
        'karakamsha_degree': ak_degree_in_d9,
        'karakamsha_lord': lord,
        'soul_direction': interpretations,
    }


def _karakamsha_interpretations(sign, lord):
    """Karakamsha的灵魂方向解读"""
    directions = {
        'Aries': '灵魂追求独立、开拓、成为先驱',
        'Taurus': '灵魂追求稳定、物质安全感、感官和谐',
        'Gemini': '灵魂追求知识、沟通、多元体验',
        'Cancer': '灵魂追求情感连接、家庭、滋养他人',
        'Leo': '灵魂追求创造力、领导力、自我表达',
        'Virgo': '灵魂追求服务、完善、分析能力',
        'Libra': '灵魂追求平衡、关系和谐、美学',
        'Scorpio': '灵魂追求转化、深层真相、神秘学',
        'Sagittarius': '灵魂追求真理、哲学、智慧传播',
        'Capricorn': '灵魂追求成就、结构、社会贡献',
        'Aquarius': '灵魂追求革新、人道主义、群体觉醒',
        'Pisces': '灵魂追求灵性、超越、无条件的爱',
    }
    lord_meanings = {
        'Sun': '通过权威、创造力和自我实现达成',
        'Moon': '通过情感智慧、直觉和公众影响力达成',
        'Mars': '通过行动力、勇气和技术能力达成',
        'Mercury': '通过智慧、沟通和学习能力达成',
        'Jupiter': '通过智慧、教导和灵性成长达成',
        'Venus': '通过美学、关系和创造力达成',
        'Saturn': '通过耐力、自律和长期承诺达成',
    }
    return {
        'sign_direction': directions.get(sign, ''),
        'lord_method': lord_meanings.get(lord, ''),
    }

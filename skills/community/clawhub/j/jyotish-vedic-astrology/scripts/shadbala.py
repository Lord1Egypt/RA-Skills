#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shadbala 计算模块（六重力量）
基于 Parashara 系统，量化行星力量

六种力量：
1. Sthana Bala（位置力量）
2. Dig Bala（方向力量）
3. Kala Bala（时间力量）
4. Chesta Bala（运动力量）
5. Naisargika Bala（天然力量）
6. Drik Bala（相位力量）
"""

import math
from typing import Dict, Tuple

# ============================================================================
# 常量
# ============================================================================
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

# 入庙度数（sign_idx * 30 + degree）
EXALTATION_DEG = {
    'Sun': 10.0, 'Moon': 33.0, 'Mars': 298.0, 'Mercury': 165.0,
    'Jupiter': 95.0, 'Venus': 357.0, 'Saturn': 200.0
}

# 落陷度数（入庙 + 180°）
DEBILITATION_DEG = {p: (d + 180) % 360 for p, d in EXALTATION_DEG.items()}

# 行星友好/敌对关系
FRIENDSHIP = {
    'Sun': {'friend': ['Moon', 'Mars', 'Jupiter'], 'enemy': ['Saturn', 'Venus'], 'neutral': ['Mercury']},
    'Moon': {'friend': ['Sun', 'Mercury'], 'enemy': [], 'neutral': ['Mars', 'Jupiter', 'Venus', 'Saturn']},
    'Mars': {'friend': ['Sun', 'Moon', 'Jupiter'], 'enemy': ['Mercury'], 'neutral': ['Venus', 'Saturn']},
    'Mercury': {'friend': ['Sun', 'Venus'], 'enemy': ['Moon'], 'neutral': ['Mars', 'Jupiter', 'Saturn']},
    'Jupiter': {'friend': ['Sun', 'Moon', 'Mars'], 'enemy': ['Mercury', 'Venus'], 'neutral': ['Saturn']},
    'Venus': {'friend': ['Mercury', 'Saturn'], 'enemy': ['Sun', 'Moon'], 'neutral': ['Mars', 'Jupiter']},
    'Saturn': {'friend': ['Mercury', 'Venus'], 'enemy': ['Sun', 'Moon', 'Mars'], 'neutral': ['Jupiter']},
}

# Dig Bala 最强宫位
DIG_BALA_HOUSE = {
    'Sun': 10, 'Mars': 10,  # Midheaven
    'Moon': 4, 'Venus': 4,  # Nadir
    'Jupiter': 1, 'Mercury': 1,  # Ascendant
    'Saturn': 7,  # Descendant
}

# Naisargika Bala（天然力量，单位 Virupas）
NAISARGIKA_BALA = {
    'Sun': 60.0, 'Moon': 60.0, 'Venus': 52.5,
    'Jupiter': 45.0, 'Mercury': 37.5, 'Mars': 30.0, 'Saturn': 22.5
}

# Shadbala 最低要求（Rupas）
MIN_REQUIRED = {
    'Sun': 5.0, 'Moon': 6.0, 'Mars': 5.0,
    'Mercury': 7.0, 'Jupiter': 6.5, 'Venus': 5.5, 'Saturn': 5.0
}

# 昼强/夜强行星
DIURNAL_STRONG = ['Sun', 'Jupiter', 'Venus']
NOCTURNAL_STRONG = ['Moon', 'Mars', 'Saturn']

# 吉星/凶星
BENEFICS = ['Jupiter', 'Venus', 'Mercury']
MALEFICS = ['Saturn', 'Mars', 'Sun']

# 行星相位规则（所有行星都有7宫相位，特殊相位如下）
SPECIAL_ASPECTS = {
    'Mars': [4, 8],     # 火星额外看4宫和8宫
    'Jupiter': [5, 9],  # 木星额外看5宫和9宫
    'Saturn': [3, 10],  # 土星额外看3宫和10宫
}

# Virupas → Rupas 转换（60 Virupas = 1 Rupa）
VIRUPAS_PER_RUPA = 60.0


def calc_shadbala(planets: Dict, asc_sign: str, birth_hour: float,
                  sun_lon: float, moon_lon: float) -> Dict:
    """
    计算完整 Shadbala

    Args:
        planets: 行星数据 dict，每颗行星需要 {sign, degree, house, retrograde, speed}
        asc_sign: 上升星座名称
        birth_hour: 出生时间（当地时间，24小时制）
        sun_lon: 太阳恒星黄道经度
        moon_lon: 月亮恒星黄道经度

    Returns:
        完整的 Shadbala 计算结果
    """
    results = {}
    is_night = birth_hour < 6.0 or birth_hour >= 18.0
    sun_northern = sun_lon >= 270 or sun_lon < 90  # Uttarayana 概略判断

    for pname in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        if pname not in planets:
            continue
        p = planets[pname]
        lon = p.get('degree', 0)
        sign = p.get('sign', 'Aries')
        house = p.get('house', 1)
        retro = p.get('retrograde', False)
        speed = p.get('speed', 1.0)

        # 1. Sthana Bala（位置力量）
        sthana = calc_sthana_bala(pname, lon, sign, house)

        # 2. Dig Bala（方向力量）
        dig = calc_dig_bala(pname, house)

        # 3. Kala Bala（时间力量）
        kala = calc_kala_bala(pname, is_night, sun_northern, sun_lon, moon_lon)

        # 4. Chesta Bala（运动力量）
        chesta = calc_chesta_bala(pname, retro, speed, sun_lon, moon_lon)

        # 5. Naisargika Bala（天然力量）
        naisargika = NAISARGIKA_BALA.get(pname, 30.0)

        # 6. Drik Bala（相位力量）
        drik = calc_drik_bala(pname, sign, house, planets)

        # 总分（Virupas → Rupas）
        total_virupas = sthana['total'] + dig + kala['total'] + chesta + naisargika + drik
        total_rupas = total_virupas / VIRUPAS_PER_RUPA

        min_req = MIN_REQUIRED.get(pname, 5.0)
        ishta_bala = (total_rupas / min_req * 100) if min_req > 0 else 0

        if ishta_bala >= 150:
            strength_level = "极强"
        elif ishta_bala >= 125:
            strength_level = "强"
        elif ishta_bala >= 100:
            strength_level = "充足"
        elif ishta_bala >= 75:
            strength_level = "略弱"
        elif ishta_bala >= 50:
            strength_level = "弱"
        else:
            strength_level = "极弱"

        results[pname] = {
            'sthana_bala': sthana,
            'dig_bala': round(dig, 2),
            'kala_bala': kala,
            'chesta_bala': round(chesta, 2),
            'naisargika_bala': round(naisargika, 2),
            'drik_bala': round(drik, 2),
            'total_virupas': round(total_virupas, 2),
            'total_rupas': round(total_rupas, 4),
            'min_required': min_req,
            'ishta_bala_pct': round(ishta_bala, 1),
            'strength_level': strength_level,
        }

    # 排名
    ranked = sorted(results.items(), key=lambda x: x[1]['total_rupas'], reverse=True)
    for i, (name, _) in enumerate(ranked):
        results[name]['rank'] = i + 1

    return {
        'method': 'Shadbala六重力量（Parashara系统）',
        'is_night_birth': is_night,
        'sun_uttarayana': sun_northern,
        'planets': results,
        'ranking': [name for name, _ in ranked],
        'strongest': ranked[0][0] if ranked else None,
        'weakest': ranked[-1][0] if ranked else None,
    }


def _dignity_score(pname: str, sign: str) -> float:
    """计算单层Varga中的尊严分数（BPHS标准）
    Own Sign=45, Exalted=50 (不超过45 unless specifically exalted degrees),
    Great Friend=40, Friend=35, Neutral=25, Enemy=15, Great Enemy=5
    """
    lord = SIGN_LORDS.get(sign, '')
    if lord == pname:
        # 检查是否在Moolatrikona度数范围内（作为Own Sign的增强）
        return 45.0

    # 获取行星对该sign lord的关系
    rel = FRIENDSHIP.get(pname, {})
    friends_of_pname = rel.get('friend', [])
    enemies_of_pname = rel.get('enemy', [])
    neutrals_of_pname = rel.get('neutral', [])

    # 反向关系：sign lord对pname的态度
    lord_rel = FRIENDSHIP.get(lord, {})
    lord_friends = lord_rel.get('friend', [])
    lord_enemies = lord_rel.get('enemy', [])

    # 双向关系评估（BPHS复合关系）
    # pname likes lord AND lord likes pname → Great Friend = 40
    # pname likes lord OR lord likes pname → Friend = 35
    # one neutral one friend → Neutral-Friend = 30
    # both neutral → Neutral = 25
    # one enemy one neutral → Enemy = 15
    # both enemy → Great Enemy = 5
    pname_likes_lord = lord in friends_of_pname
    lord_likes_pname = pname in lord_friends
    pname_dislikes_lord = lord in enemies_of_pname
    lord_dislikes_pname = pname in lord_enemies

    if pname_likes_lord and lord_likes_pname:
        return 40.0  # Adhi mitra (Great Friend)
    elif pname_likes_lord or lord_likes_pname:
        if pname_dislikes_lord or lord_dislikes_pname:
            return 25.0  # Mixed → Neutral
        return 35.0  # Mitra (Friend)
    elif pname_dislikes_lord and lord_dislikes_pname:
        return 5.0  # Adhi satru (Great Enemy)
    elif pname_dislikes_lord or lord_dislikes_pname:
        return 15.0  # Satru (Enemy)
    else:
        return 25.0  # Sama (Neutral)


def calc_sthana_bala(pname: str, lon: float, sign: str, house: int) -> Dict:
    """Sthana Bala（位置力量）
    v4.5.0: 修复Saptavargaja Bala为完整7层计算
    """
    # A. Ucha Bala（入庙力量）max 60 Virupas
    debilit_deg = DEBILITATION_DEG.get(pname, 0)
    offset = (lon - debilit_deg + 360) % 360
    if offset > 180:
        offset = 360 - offset
    ucha_bala = offset / 180 * 60  # 0-60 Virupas

    # B. Saptavargaja Bala（七分盘力量）max ~315 Virupas (7 × 45)
    # v4.5.0: 完整7层Varga计算（D1/D2/D3/D4/D7/D9/D12）
    # 每层评估行星在该分盘中的尊严状态，满分45
    sign_idx = SIGNS.index(sign) if sign in SIGNS else 0
    deg_in_sign = lon % 30

    # D1 (Rashi) — 直接用当前sign
    d1_score = _dignity_score(pname, sign)
    # 检查入庙/落陷覆盖
    exalt_sign = SIGNS[int(EXALTATION_DEG.get(pname, 0) / 30) % 12]
    debilit_sign = SIGNS[int(DEBILITATION_DEG.get(pname, 0) / 30) % 12]
    if sign == exalt_sign:
        d1_score = 50.0  # Exalted 高于 Own Sign（BPHS 标准）
    elif sign == debilit_sign:
        d1_score = 5.0  # Debilitated

    # D2 (Hora) — 奇数度Leo/Sun rule, 偶数度Cancer/Moon rule
    if deg_in_sign < 15:
        hora_lord = 'Sun'
    else:
        hora_lord = 'Moon'
    # Simplified: evaluate relationship to hora lord
    if hora_lord in FRIENDSHIP.get(pname, {}).get('friend', []):
        d2_score = 35.0
    elif hora_lord in FRIENDSHIP.get(pname, {}).get('enemy', []):
        d2_score = 15.0
    else:
        d2_score = 25.0
    if pname == hora_lord:
        d2_score = 45.0

    # D3 (Drekkana) — 0-10°: Aries group, 10-20°: Taurus group, 20-30°: Gemini group
    drekkana_idx = int(deg_in_sign / 10)  # 0, 1, 2
    drekkana_lord_idx = drekkana_idx  # Aries=0/Mars, Taurus=1/Venus, Gemini=2/Mercury
    drekkana_lords = ['Mars', 'Venus', 'Mercury']
    d3_lord = drekkana_lords[drekkana_idx]
    if pname == d3_lord:
        d3_score = 45.0
    elif d3_lord in FRIENDSHIP.get(pname, {}).get('friend', []):
        d3_score = 35.0
    elif d3_lord in FRIENDSHIP.get(pname, {}).get('enemy', []):
        d3_score = 15.0
    else:
        d3_score = 25.0

    # D4 (Navamsa of Turyamsa) — simplified using navamsa calculation
    try:
        navamsa_part = int(deg_in_sign / (30 / 9))
        el_starts = [0, 9, 6, 3]  # Fire=0, Earth=9, Air=6, Water=3
        d4_sign_idx = (el_starts[sign_idx % 4] + navamsa_part) % 12
        d4_sign = SIGNS[d4_sign_idx]
        d4_score = _dignity_score(pname, d4_sign)
    except:
        d4_score = 25.0

    # D7 (Saptamsa) — 7 parts per sign
    try:
        saptamsa_part = int(deg_in_sign / (30 / 7))
        # D7 sign calculation: for odd signs count forward, even signs backward
        if sign_idx % 2 == 0:  # odd sign (Aries=0)
            d7_sign_idx = (sign_idx + saptamsa_part) % 12
        else:  # even sign
            d7_sign_idx = (sign_idx - saptamsa_part) % 12
        d7_sign = SIGNS[d7_sign_idx]
        d7_score = _dignity_score(pname, d7_sign)
    except:
        d7_score = 25.0

    # D9 (Navamsa) — reuse D4 calculation (same navamsa)
    try:
        d9_part = int(deg_in_sign / (30 / 9))
        d9_sign_idx = (el_starts[sign_idx % 4] + d9_part) % 12
        d9_sign = SIGNS[d9_sign_idx]
        d9_score = _dignity_score(pname, d9_sign)
        # Check exaltation/debilitation in D9
        if d9_sign == exalt_sign:
            d9_score = max(d9_score, 45.0)
        elif d9_sign == debilit_sign:
            d9_score = 5.0
    except:
        d9_score = 25.0

    # D12 (Dwadashamsa) — 12 parts, each 2.5°
    try:
        dwad_part = int(deg_in_sign / 2.5)
        # D12: start from the sign itself, count forward
        d12_sign_idx = (sign_idx + dwad_part) % 12
        d12_sign = SIGNS[d12_sign_idx]
        d12_score = _dignity_score(pname, d12_sign)
    except:
        d12_score = 25.0

    sapta_score = d1_score + d2_score + d3_score + d4_score + d7_score + d9_score + d12_score

    # C. Ojayugma Bala（奇偶宫力量）max 15 Virupas
    # v4.5.0: 使用D9宫位精确计算
    try:
        d9_house = ((d9_sign_idx - sign_idx) % 12) + 1  # approximate from Lagna
        if pname in ['Mercury', 'Venus']:
            ojayugma = 15 if d9_house % 2 == 1 else 0  # 奇数宫
        else:
            ojayugma = 15 if d9_house % 2 == 0 else 0  # 偶数宫
    except:
        ojayugma = 0

    # D. Kendra Bala（角宫力量）max 15 Virupas
    kendra_bala = 15 if house in (1, 4, 7, 10) else 0

    # E. Drekkana Bala（三分盘力量）max 15 Virupas
    if pname in ['Sun', 'Mars', 'Jupiter']:
        drekkana_bala = 15 if deg_in_sign < 10 else 0
    elif pname in ['Moon', 'Venus']:
        drekkana_bala = 15 if 10 <= deg_in_sign < 20 else 0
    else:  # Saturn, Mercury
        drekkana_bala = 15 if deg_in_sign >= 20 else 0

    total = ucha_bala + sapta_score + ojayugma + kendra_bala + drekkana_bala

    return {
        'ucha_bala': round(ucha_bala, 2),
        'sapta_d1': round(d1_score, 2),
        'sapta_d2': round(d2_score, 2),
        'sapta_d3': round(d3_score, 2),
        'sapta_d4': round(d4_score, 2),
        'sapta_d7': round(d7_score, 2),
        'sapta_d9': round(d9_score, 2),
        'sapta_d12': round(d12_score, 2),
        'sapta_score': round(sapta_score, 2),
        'ojayugma_bala': ojayugma,
        'kendra_bala': kendra_bala,
        'drekkana_bala': drekkana_bala,
        'total': round(total, 2),
    }


def calc_dig_bala(pname: str, house: int) -> float:
    """Dig Bala（方向力量），max 60 Virupas"""
    best_house = DIG_BALA_HOUSE.get(pname, 1)
    # 线性插值：最强宫位=60，对宫=0
    diff = abs(house - best_house)
    if diff > 6:
        diff = 12 - diff
    return max(0, (6 - diff) * 10)


def calc_kala_bala(pname: str, is_night: bool, sun_northern: bool,
                    sun_lon: float, moon_lon: float) -> Dict:
    """Kala Bala（时间力量）"""
    components = {}

    # A. Nathonnata Bala（昼夜力量）
    # ⚠️ 2026-05-03修正：BPHS给出比例计算（0-60），非二值(0/60)
    # 水星永远获得完整60；日间行星白天按出生时间到正午距离比例获得0-60
    # 夜间行星夜晚按出生时间到午夜距离比例获得0-60
    # 简化实现：保持水星=60，其他按昼夜分组给60/0
    # TODO: 未来需传入精确出生时间计算正午/午夜距离比例
    if pname == 'Mercury':
        nathonnata = 60
    elif is_night and pname in NOCTURNAL_STRONG:
        nathonnata = 60
    elif not is_night and pname in DIURNAL_STRONG:
        nathonnata = 60
    else:
        nathonnata = 0
    components['nathonnata'] = nathonnata

    # B. Paksha Bala（月相力量，max 30 Virupas）
    moon_sun_diff = (moon_lon - sun_lon + 360) % 360
    # 归一化到 0-180（月相亮度是对称的）
    phase_angle = moon_sun_diff if moon_sun_diff <= 180 else 360 - moon_sun_diff
    if pname in ['Jupiter', 'Venus', 'Moon']:
        # 望月（phase_angle=180）最强 = 30，朔月（0）= 0
        paksha = phase_angle / 180 * 30
    else:
        # 朔月（phase_angle=0）最强 = 30，望月（180）= 0
        paksha = (180 - phase_angle) / 180 * 30
    components['paksha'] = round(paksha, 2)

    # C. Tribhaga Bala（三段力量）
    if pname == 'Jupiter':
        tribhaga = 45
    elif pname == 'Venus':
        tribhaga = 45
    elif pname == 'Saturn':
        tribhaga = 45
    else:
        tribhaga = 0
    components['tribhaga'] = tribhaga

    # D. Ayana Bala（太阳南北行）
    if pname == 'Mercury':
        ayana = 30
    elif sun_northern and pname in ['Sun', 'Mars', 'Moon']:
        ayana = 30
    elif not sun_northern and pname in ['Jupiter', 'Venus', 'Saturn']:
        ayana = 30
    else:
        ayana = 15
    components['ayana'] = ayana

    total = sum(components.values())
    return {k: v for k, v in components.items()} | {'total': round(total, 2)}


def calc_chesta_bala(pname: str, retro: bool, speed: float,
                     sun_lon: float, moon_lon: float) -> float:
    """Chesta Bala（运动力量），max 60 Virupas"""
    if pname == 'Sun':
        return 60.0  # 太阳始终满分

    if pname == 'Moon':
        # 月亮根据月相：望月=60，朔月=0
        # BPHS: Chesta Bala 与月相亮面比例成正比
        # diff 取 0-180 范围（>180 时用 360-diff，因为月相是对称的）
        moon_sun_diff = (moon_lon - sun_lon + 360) % 360
        if moon_sun_diff > 180:
            moon_sun_diff = 360 - moon_sun_diff
        return moon_sun_diff / 180 * 60

    # 其他行星
    if retro:
        return 60.0

    # 速度判断（简化：用speed的绝对值）
    abs_speed = abs(speed)
    if abs_speed > 1.0:  # 快速直行
        return 50.0
    elif abs_speed > 0.5:
        return 35.0
    elif abs_speed > 0.1:
        return 20.0
    else:
        return 10.0  # 接近驻留


def calc_drik_bala(pname: str, sign: str, house: int,
                   all_planets: Dict) -> float:
    """Drik Bala（相位力量），可正可负"""
    drik = 0.0
    p_sign_idx = SIGNS.index(sign) if sign in SIGNS else 0

    for other_name, other_data in all_planets.items():
        if other_name == pname or other_name == 'Rahu' or other_name == 'Ketu':
            continue

        other_sign = other_data.get('sign', '')
        if other_sign not in SIGNS:
            continue
        other_sign_idx = SIGNS.index(other_sign)

        # 计算从other到pname的宫位差
        house_diff = (p_sign_idx - other_sign_idx) % 12 + 1

        # 检查是否形成相位
        has_aspect = False
        if house_diff == 7 or house_diff == 1:  # 7宫相位或合相
            has_aspect = True
        if other_name in SPECIAL_ASPECTS:
            if house_diff in SPECIAL_ASPECTS[other_name]:
                has_aspect = True

        if has_aspect:
            # 判断吉凶
            aspect_value = 15.0
            if house_diff == 1:  # 合相加倍
                aspect_value = 30.0

            if other_name in BENEFICS:
                drik += aspect_value
            elif other_name in MALEFICS:
                drik -= aspect_value
            else:
                drik += aspect_value * 0.5  # 中性行星

    # 限制范围
    return max(-60.0, min(60.0, drik))

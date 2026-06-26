#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ashtakavarga 计算模块 v2.0（八分法）
基于 Brihat Parashara Hora Shastra (BPHS) 完整标准表

核心修正（v2.0 vs v1.0）：
- v1.0: BAV_BASE 只有自贡献 + 少量跨源贡献 → SAV=94 ❌
- v2.0: 完整 8×8 贡献矩阵（每颗行星 × 8来源）→ SAV=337 ✅

架构：
- BAV_CONTRIBUTION[planet][source] = 有利宫位列表
- 每颗行星的 BAV = 所有 8 个来源（7行星+Lagna）的贡献之和
- SAV = 7 颗行星 BAV 之和（Lagna 自身 BAV 单独展示，不计入 SAV）
- SAV 总和 = 337（宇宙常数）

BPHS 校正：
- 月亮 BAV → 木星贡献：1,4,7,8,10,11（6宫，不含12）→ 总49
- 金星 BAV → 水星贡献：3,5,6,9,11,12（6宫，含12）→ 总52
"""

from typing import Dict, List, Tuple

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# ============================================================================
# 完整 BAV 贡献表（BPHS 标准法）
# BAV_CONTRIBUTION[planet][source] = 从 source 数起的有利宫位列表
# 每颗行星的 BAV 总和 = 所有 8 个来源的贡献数之和
# ============================================================================

# --- 太阳 BAV（总48） ---
# 来源: Sun(8) + Moon(4) + Mars(8) + Mercury(7) + Jupiter(4) + Venus(3) + Saturn(8) + Lagna(6) = 48
_SUN_BAV = {
    'Sun':     [1, 2, 4, 7, 8, 9, 10, 11],
    'Moon':    [3, 6, 10, 11],
    'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
    'Mercury': [3, 5, 6, 9, 10, 11, 12],
    'Jupiter': [5, 6, 9, 11],
    'Venus':   [6, 7, 12],
    'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
    'Lagna':   [3, 4, 6, 10, 11, 12],
}

# --- 月亮 BAV（总49） ---
# 来源: Sun(6) + Moon(6) + Mars(7) + Mercury(8) + Jupiter(6) + Venus(7) + Saturn(4) + Lagna(5) = 49
# BPHS校正：木星贡献为 1,4,7,8,10,11（6宫），非 1,4,7,8,10,11,12（7宫）
_MOON_BAV = {
    'Sun':     [3, 6, 7, 8, 10, 11],
    'Moon':    [1, 3, 6, 7, 10, 11],
    'Mars':    [2, 3, 5, 6, 9, 10, 11],
    'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
    'Jupiter': [1, 4, 7, 8, 10, 11],       # BPHS校正：不含12
    'Venus':   [3, 4, 5, 7, 9, 10, 11],
    'Saturn':  [3, 5, 6, 11],
    'Lagna':   [3, 6, 10, 11, 12],
}

# --- 火星 BAV（总39） ---
# 来源: Sun(5) + Moon(3) + Mars(7) + Mercury(4) + Jupiter(4) + Venus(4) + Saturn(7) + Lagna(5) = 39
_MARS_BAV = {
    'Sun':     [3, 5, 6, 10, 11],
    'Moon':    [3, 6, 11],
    'Mars':    [1, 2, 4, 7, 8, 10, 11],
    'Mercury': [3, 5, 6, 11],
    'Jupiter': [6, 10, 11, 12],
    'Venus':   [6, 8, 11, 12],
    'Saturn':  [1, 4, 7, 8, 9, 10, 11],
    'Lagna':   [1, 3, 6, 10, 11],
}

# --- 水星 BAV（总54） ---
# 来源: Sun(5) + Moon(6) + Mars(8) + Mercury(8) + Jupiter(4) + Venus(8) + Saturn(8) + Lagna(7) = 54
_MERCURY_BAV = {
    'Sun':     [5, 6, 9, 11, 12],
    'Moon':    [2, 4, 6, 8, 10, 11],
    'Mars':    [1, 2, 4, 7, 8, 9, 10, 11],
    'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
    'Jupiter': [6, 8, 11, 12],
    'Venus':   [1, 2, 3, 4, 5, 8, 9, 11],
    'Saturn':  [1, 2, 4, 7, 8, 9, 10, 11],
    'Lagna':   [1, 2, 4, 6, 8, 10, 11],
}

# --- 木星 BAV（总56） ---
# 来源: Sun(9) + Moon(5) + Mars(7) + Mercury(8) + Jupiter(8) + Venus(6) + Saturn(4) + Lagna(9) = 56
_JUPITER_BAV = {
    'Sun':     [1, 2, 3, 4, 7, 8, 9, 10, 11],
    'Moon':    [2, 5, 7, 9, 11],
    'Mars':    [1, 2, 4, 7, 8, 10, 11],
    'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
    'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
    'Venus':   [2, 5, 6, 9, 10, 11],
    'Saturn':  [3, 5, 6, 12],
    'Lagna':   [1, 2, 4, 5, 6, 7, 9, 10, 11],
}

# --- 金星 BAV（总52） ---
# 来源: Sun(3) + Moon(9) + Mars(6) + Mercury(6) + Jupiter(5) + Venus(9) + Saturn(7) + Lagna(7) = 52
# BPHS校正：水星贡献为 3,5,6,9,11,12（6宫，含12），非 3,5,6,9,11（5宫）
_VENUS_BAV = {
    'Sun':     [8, 11, 12],
    'Moon':    [1, 2, 3, 4, 5, 8, 9, 11, 12],
    'Mars':    [3, 5, 6, 9, 11, 12],
    'Mercury': [3, 5, 6, 9, 11, 12],       # BPHS校正：含12
    'Jupiter': [5, 8, 9, 10, 11],
    'Venus':   [1, 2, 3, 4, 5, 8, 9, 10, 11],
    'Saturn':  [3, 4, 5, 8, 9, 10, 11],
    'Lagna':   [1, 2, 3, 4, 5, 8, 9],
}

# --- 土星 BAV（总39） ---
# 来源: Sun(7) + Moon(3) + Mars(6) + Mercury(6) + Jupiter(4) + Venus(3) + Saturn(4) + Lagna(6) = 39
_SATURN_BAV = {
    'Sun':     [1, 2, 4, 7, 8, 10, 11],
    'Moon':    [3, 6, 11],
    'Mars':    [3, 5, 6, 10, 11, 12],
    'Mercury': [6, 8, 9, 10, 11, 12],
    'Jupiter': [5, 6, 11, 12],
    'Venus':   [6, 11, 12],
    'Saturn':  [3, 5, 6, 11],
    'Lagna':   [1, 3, 4, 6, 10, 11],
}

# --- Lagna BAV（总49，不计入 SAV 337） ---
# 来源: Sun(6) + Moon(5) + Mars(5) + Mercury(7) + Jupiter(9) + Venus(7) + Saturn(6) + Lagna(4) = 49
_LAGNA_BAV = {
    'Sun':     [3, 4, 6, 10, 11, 12],
    'Moon':    [3, 6, 10, 11, 12],
    'Mars':    [1, 3, 6, 10, 11],
    'Mercury': [1, 2, 4, 6, 8, 10, 11],
    'Jupiter': [1, 2, 4, 5, 6, 7, 9, 10, 11],
    'Venus':   [1, 2, 3, 4, 5, 8, 9],
    'Saturn':  [1, 3, 4, 6, 10, 11],
    'Lagna':   [3, 6, 10, 11],
}

# 汇总为统一查找表
BAV_CONTRIBUTION = {
    'Sun':     _SUN_BAV,
    'Moon':    _MOON_BAV,
    'Mars':    _MARS_BAV,
    'Mercury': _MERCURY_BAV,
    'Jupiter': _JUPITER_BAV,
    'Venus':   _VENUS_BAV,
    'Saturn':  _SATURN_BAV,
    'Lagna':   _LAGNA_BAV,
}

# 各行星BAV固定总数（宇宙常数）
BAV_TOTALS = {
    'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54,
    'Jupiter': 56, 'Venus': 52, 'Saturn': 39, 'Lagna': 49
}

# 7颗行星 BAV 总和 = SAV 337
EXPECTED_SAV_TOTAL = 337

# Shodhya Pinda 行星权重
PLANET_WEIGHTS = {
    'Sun': 5, 'Moon': 5, 'Mars': 8, 'Mercury': 5,
    'Jupiter': 10, 'Venus': 7, 'Saturn': 5
}

# 行星列表
SEVEN_PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
ALL_SOURCES = SEVEN_PLANETS + ['Lagna']


def _get_sign_idx(sign_name: str) -> int:
    """星座名称转索引"""
    return SIGNS.index(sign_name) if sign_name in SIGNS else 0


def calc_ashtakavarga(planets: Dict, asc_sign_idx: int) -> Dict:
    """
    计算完整 Ashtakavarga（v2.0 BPHS标准法）

    Args:
        planets: 行星数据 dict，每颗行星需要 {sign, degree, ...}
                 sign 是星座名称
        asc_sign_idx: 上升星座在 SIGNS 中的索引 (0-11)

    Returns:
        完整的 Ashtakavarga 计算结果，含 BAV、SAV、校验
    """
    # 1. 确定每个来源（7行星+Lagna）的星座索引
    source_sign_idx = {}
    for pname in SEVEN_PLANETS:
        if pname in planets:
            sign = planets[pname].get('sign', '')
            if sign in SIGNS:
                source_sign_idx[pname] = SIGNS.index(sign)
    source_sign_idx['Lagna'] = asc_sign_idx

    # 2. 为每颗行星计算 BAV
    #    BAV[planet][sign_i] = count of sources that contribute bindhu to sign_i
    bav_results = {}
    sav = [0] * 12  # 12星座的SAV（仅统计7行星贡献）
    lagna_sav = [0] * 12  # Lagna单独的贡献

    for planet in ALL_SOURCES:
        contribution_rules = BAV_CONTRIBUTION[planet]
        bav = [0] * 12  # 12星座的 bindhu 数

        for source in ALL_SOURCES:
            if source not in source_sign_idx:
                continue
            # 获取该 source 对该 planet BAV 的有利宫位
            favorable_houses = contribution_rules.get(source, [])
            source_idx = source_sign_idx[source]

            # 从 source 所在星座开始，将有利宫位映射到实际星座
            for house in favorable_houses:
                target_sign = (source_idx + house - 1) % 12
                bav[target_sign] += 1

        bav_total = sum(bav)
        expected = BAV_TOTALS.get(planet, 0)

        bav_results[planet] = {
            'bindus': bav,
            'total': bav_total,
            'expected_total': expected,
            'valid': bav_total == expected,
            'deviation': abs(bav_total - expected),
        }

        # 累加到 SAV（仅7行星）
        if planet in SEVEN_PLANETS:
            for i in range(12):
                sav[i] += bav[i]
        else:
            # Lagna 的贡献单独记录
            for i in range(12):
                lagna_sav[i] += bav[i]

    # 3. 校验 SAV 总分
    sav_total = sum(sav)

    # 4. SAV 评估
    sav_assessment = []
    for i in range(12):
        score = sav[i]
        if score >= 30:
            level = "极吉"
        elif score >= 28:
            level = "吉利"
        elif score >= 25:
            level = "中等"
        else:
            level = "挑战"
        sav_assessment.append({
            'sign': SIGNS[i],
            'score': score,
            'level': level,
        })

    # 5. 含 Lagna 的完整 SAV（386 = 337 + 49）
    full_sav = [sav[i] + lagna_sav[i] for i in range(12)]

    # 6. Shodhya Pinda 计算
    shodhya = {}
    for pname in SEVEN_PLANETS:
        if pname in source_sign_idx and pname in bav_results:
            own_sign = source_sign_idx[pname]
            bindu_at_own = bav_results[pname]['bindus'][own_sign]
            sign_weight = 4  # 简化：星座权重统一为4
            rashi_pinda = bindu_at_own * sign_weight
            graha_pinda = bindu_at_own * PLANET_WEIGHTS.get(pname, 5)
            shodhya[pname] = {
                'rashi_pinda': rashi_pinda,
                'graha_pinda': graha_pinda,
                'total_pinda': rashi_pinda + graha_pinda,
                'bindu_at_own_sign': bindu_at_own,
            }

    # 7. 排名
    ranked_sav = sorted(enumerate(sav_assessment), key=lambda x: x[1]['score'], reverse=True)

    # 8. BAV 校验报告
    bav_validation = []
    all_valid = True
    for planet in ALL_SOURCES:
        r = bav_results[planet]
        status = "✅" if r['valid'] else f"❌ 偏差{r['deviation']}"
        if not r['valid']:
            all_valid = False
        bav_validation.append({
            'planet': planet,
            'actual': r['total'],
            'expected': r['expected_total'],
            'status': status,
        })

    return {
        'method': 'Ashtakavarga八分法（BPHS标准v2.0）',
        'version': '2.0',
        'bav': bav_results,
        'sav': {
            'scores': {SIGNS[i]: sav[i] for i in range(12)},
            'full_scores_with_lagna': {SIGNS[i]: full_sav[i] for i in range(12)},
            'assessment': sav_assessment,
            'total': sav_total,
            'expected_total': EXPECTED_SAV_TOTAL,
            'valid': sav_total == EXPECTED_SAV_TOTAL,
            'deviation': abs(sav_total - EXPECTED_SAV_TOTAL),
            'full_total_with_lagna': sum(full_sav),
        },
        'bav_validation': bav_validation,
        'all_bav_valid': all_valid,
        'shodhya_pinda': shodhya,
        'strongest_signs': [SIGNS[i] for i, _ in ranked_sav[:3]],
        'weakest_signs': [SIGNS[i] for i, _ in ranked_sav[-3:]],
        'house_scores': _map_to_houses(sav_assessment, asc_sign_idx),
        'house_scores_full': _map_to_houses_values(full_sav, asc_sign_idx),
    }


def _map_to_houses(sav_assessment: List[Dict], asc_sign_idx: int) -> Dict:
    """将 SAV 分数映射到宫位"""
    houses = {}
    for house_num in range(1, 13):
        sign_idx = (asc_sign_idx + house_num - 1) % 12
        score = sav_assessment[sign_idx]['score']
        level = sav_assessment[sign_idx]['level']
        houses[f"house_{house_num}"] = {
            'sign': SIGNS[sign_idx],
            'sav_score': score,
            'level': level,
        }
    return houses


def _map_to_houses_values(scores: List[int], asc_sign_idx: int) -> Dict:
    """将含Lagna的完整SAV映射到宫位"""
    houses = {}
    for house_num in range(1, 13):
        sign_idx = (asc_sign_idx + house_num - 1) % 12
        houses[f"house_{house_num}"] = {
            'sign': SIGNS[sign_idx],
            'sav_score': scores[sign_idx],
        }
    return houses

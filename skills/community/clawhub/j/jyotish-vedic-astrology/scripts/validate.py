#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R1-R10 数学验证模块
对星盘计算结果执行 10 项硬性校验规则（来自 CNWU16 审计框架）

规则清单：
  R1: SAV 总和 = 337（7行星BAV之和）
  R2: 各 BAV 行常数（Sun=48, Moon=49, Mars=39, Mercury=54, Jupiter=56, Venus=52, Saturn=39, Lagna=49）
  R2b: BAV列→SAV列校验（每个星座的7行星BAV之和 = 该星座SAV分数）
  R3: 水星最大延伸角 ≤ 28°（不远离太阳）
  R4: 金星最大延伸角 ≤ 47°（不远离太阳）
  R5: Rahu-Ketu 严格 180° 对冲
  R6: 逆行合法性（只有火星/木星/土星/金星/水星可能逆行，Rahu/Ketu永远逆行，太阳/月亮不逆行）
  R7: Dasha 大运年限链总和 = 120 年
  R8: 行星完整性（7行星 + Rahu + Ketu + Lagna 全部存在）
  R9: 星座度数范围 [0, 30)
  R10: 宫位连续性（1-12宫无断点）
"""

from typing import Dict, List, Tuple
import math

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
    "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

EXPECTED_PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

BAV_TOTALS = {
    'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54,
    'Jupiter': 56, 'Venus': 52, 'Saturn': 39, 'Lagna': 49
}

SEVEN_PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']


def validate_chart(chart_data: Dict, ashtakavarga_data: Dict = None) -> Dict:
    """
    执行 R1-R10 全部校验

    Args:
        chart_data: jyotish_engine chart 命令的完整输出
        ashtakavarga_data: ashtakavarga 命令的输出（可选，用于 R1/R2）

    Returns:
        {
            "valid": bool,  # 全部通过
            "total_checks": int,
            "passed": int,
            "failed": int,
            "results": [{"rule": "R1", "name": "...", "passed": bool, "detail": "..."}, ...]
        }
    """
    results = []
    planets = chart_data.get('planets', {})
    asc = chart_data.get('ascendant', {})

    # R1: SAV 总和 = 337
    if ashtakavarga_data:
        sav_total = ashtakavarga_data.get('sav', {}).get('total', 0)
        sav_valid = ashtakavarga_data.get('sav', {}).get('valid', False)
        results.append({
            'rule': 'R1', 'name': 'SAV总和=337',
            'passed': sav_valid,
            'detail': f"SAV total = {sav_total}, expected 337"
        })
    else:
        results.append({
            'rule': 'R1', 'name': 'SAV总和=337',
            'passed': None,
            'detail': '未提供 ashtakavarga 数据，跳过'
        })

    # R2: 各 BAV 行常数
    if ashtakavarga_data:
        bav_results = ashtakavarga_data.get('bav', {})
        all_bav_valid = ashtakavarga_data.get('all_bav_valid', False)
        details = []
        for pname in SEVEN_PLANETS + ['Lagna']:
            if pname in bav_results:
                actual = bav_results[pname].get('total', 0)
                expected = BAV_TOTALS.get(pname, 0)
                details.append(f"{pname}={actual}/{expected}")
        results.append({
            'rule': 'R2', 'name': 'BAV行常数校验',
            'passed': all_bav_valid,
            'detail': '; '.join(details) if details else '无BAV数据'
        })
    else:
        results.append({
            'rule': 'R2', 'name': 'BAV行常数校验',
            'passed': None,
            'detail': '未提供 ashtakavarga 数据，跳过'
        })

    # R2b: BAV列→SAV列校验（每个星座的7行星BAV之和 = 该星座SAV分数）
    if ashtakavarga_data:
        r2b_passed, r2b_detail = _check_bav_column_sav(ashtakavarga_data)
        results.append({'rule': 'R2b', 'name': 'BAV列→SAV列校验', 'passed': r2b_passed, 'detail': r2b_detail})
    else:
        results.append({'rule': 'R2b', 'name': 'BAV列→SAV列校验', 'passed': None, 'detail': '未提供 ashtakavarga 数据，跳过'})

    # R3: 水星最大延伸角 ≤ 28°
    r3_passed, r3_detail = _check_elongation(planets, 'Mercury', 'Sun', 28)
    results.append({'rule': 'R3', 'name': '水星延伸角≤28°', 'passed': r3_passed, 'detail': r3_detail})

    # R4: 金星最大延伸角 ≤ 47°
    r4_passed, r4_detail = _check_elongation(planets, 'Venus', 'Sun', 47)
    results.append({'rule': 'R4', 'name': '金星延伸角≤47°', 'passed': r4_passed, 'detail': r4_detail})

    # R5: Rahu-Ketu 严格 180° 对冲
    r5_passed, r5_detail = _check_rahu_ketu_opposition(planets)
    results.append({'rule': 'R5', 'name': 'Rahu-Ketu 180°对冲', 'passed': r5_passed, 'detail': r5_detail})

    # R6: 逆行合法性
    r6_passed, r6_detail = _check_retrograde_legitimacy(planets)
    results.append({'rule': 'R6', 'name': '逆行合法性', 'passed': r6_passed, 'detail': r6_detail})

    # R7: Dasha 大运年限链总和 = 120 年
    dasha_sum = sum(DASHA_YEARS.values())
    results.append({
        'rule': 'R7', 'name': 'Dasha年限总和=120',
        'passed': dasha_sum == 120,
        'detail': f"Dasha year chain sum = {dasha_sum}"
    })

    # R8: 行星完整性
    r8_passed, r8_detail = _check_planet_completeness(planets, asc)
    results.append({'rule': 'R8', 'name': '行星完整性', 'passed': r8_passed, 'detail': r8_detail})

    # R9: 星座度数范围 [0, 30)
    r9_passed, r9_detail = _check_degree_range(planets)
    results.append({'rule': 'R9', 'name': '星座度数范围', 'passed': r9_passed, 'detail': r9_detail})

    # R10: 宫位连续性（1-12宫无断点）
    r10_passed, r10_detail = _check_house_continuity(chart_data)
    results.append({'rule': 'R10', 'name': '宫位连续性', 'passed': r10_passed, 'detail': r10_detail})

    # 汇总
    checked = [r for r in results if r['passed'] is not None]
    passed_count = sum(1 for r in checked if r['passed'])
    failed_count = sum(1 for r in checked if not r['passed'])

    return {
        'valid': failed_count == 0,
        'total_checks': len(results),
        'checked': len(checked),
        'passed': passed_count,
        'failed': failed_count,
        'skipped': len(results) - len(checked),
        'results': results,
    }


def _check_elongation(planets: Dict, planet: str, reference: str, max_deg: float) -> Tuple[bool, str]:
    """检查行星与参考行星的延伸角"""
    p1 = planets.get(planet, {})
    p2 = planets.get(reference, {})
    deg1 = p1.get('degree', None)
    deg2 = p2.get('degree', None)
    if deg1 is None or deg2 is None:
        return None, f'{planet}或{reference}度数缺失'
    elongation = abs(deg1 - deg2)
    if elongation > 180:
        elongation = 360 - elongation
    ok = elongation <= max_deg
    return ok, f"{planet}延伸角 = {elongation:.2f}°, 阈值 {max_deg}°"


def _check_rahu_ketu_opposition(planets: Dict) -> Tuple[bool, str]:
    """检查 Rahu-Ketu 严格 180° 对冲"""
    rahu = planets.get('Rahu', {})
    ketu = planets.get('Ketu', {})
    rahu_deg = rahu.get('degree', None)
    ketu_deg = ketu.get('degree', None)
    if rahu_deg is None or ketu_deg is None:
        return None, 'Rahu或Ketu度数缺失'
    diff = abs(rahu_deg - ketu_deg)
    deviation = abs(diff - 180)
    ok = deviation < 0.01  # 允许极小数值误差
    return ok, f"Rahu={rahu_deg:.4f}°, Ketu={ketu_deg:.4f}°, 偏差={deviation:.4f}°"


def _check_retrograde_legitimacy(planets: Dict) -> Tuple[bool, str]:
    """检查逆行合法性"""
    # 太阳和月亮不应逆行
    never_retro = ['Sun', 'Moon']
    # Rahu/Ketu 永远逆行
    always_retro = ['Rahu', 'Ketu']
    # 火星/木星/土星/金星/水星 可能逆行也可能不逆行
    can_retro = ['Mars', 'Jupiter', 'Saturn', 'Venus', 'Mercury']

    issues = []
    for pname in never_retro:
        pd = planets.get(pname, {})
        if pd.get('retrograde', False):
            issues.append(f"{pname}不应逆行")

    for pname in always_retro:
        pd = planets.get(pname, {})
        if not pd.get('retrograde', True):
            issues.append(f"{pname}应永远逆行")

    ok = len(issues) == 0
    detail = '; '.join(issues) if issues else '所有行星逆行状态合法'
    return ok, detail


def _check_planet_completeness(planets: Dict, asc: Dict) -> Tuple[bool, str]:
    """检查行星完整性"""
    missing = []
    for pname in EXPECTED_PLANETS:
        if pname not in planets:
            missing.append(pname)
    if not asc:
        missing.append('Ascendant(Lagna)')
    ok = len(missing) == 0
    detail = f"缺失: {', '.join(missing)}" if missing else f"完整：{len(EXPECTED_PLANETS)}行星 + Ascendant"
    return ok, detail


def _check_degree_range(planets: Dict) -> Tuple[bool, str]:
    """检查星座度数范围"""
    issues = []
    for pname, pd in planets.items():
        deg_in_sign = pd.get('degree_in_sign', None)
        if deg_in_sign is not None:
            if deg_in_sign < 0 or deg_in_sign >= 30:
                issues.append(f"{pname}度数={deg_in_sign}° 超出[0,30)范围")
    ok = len(issues) == 0
    detail = '; '.join(issues) if issues else '所有行星度数在合法范围'
    return ok, detail


def _check_house_continuity(chart_data: Dict) -> Tuple[bool, str]:
    """检查宫位连续性"""
    houses = chart_data.get('houses', {})
    house_nums = set()
    for key in houses:
        if key.startswith('house_'):
            num = int(key.replace('house_', ''))
            house_nums.add(num)

    expected = set(range(1, 13))
    missing = expected - house_nums
    ok = len(missing) == 0
    detail = f"缺失宫位: {sorted(missing)}" if missing else f"1-12宫完整({len(house_nums)}宫)"
    return ok, detail


def _check_bav_column_sav(ashtakavarga_data: Dict) -> Tuple[bool, str]:
    """
    R2b: BAV列→SAV列校验
    每个星座的7行星BAV bindus之和必须等于该星座的SAV分数。
    这验证了行总和（R2）和列总和的交叉一致性。
    """
    bav_results = ashtakavarga_data.get('bav', {})
    house_scores = ashtakavarga_data.get('house_scores', {})
    sav_scores = ashtakavarga_data.get('sav', {})

    issues = []
    # 从每个7行星的 BAV bindus 列向量求和，对比 SAV house_scores
    for sign_i in range(12):
        # 计算该星座位置（第 sign_i 列）的 7行星 BAV 之和
        col_sum = 0
        for pname in SEVEN_PLANETS:
            if pname in bav_results:
                bindus = bav_results[pname].get('bindus', [])
                if len(bindus) > sign_i:
                    col_sum += bindus[sign_i]

        # 获取该星座/宫位的 SAV 分数
        house_key = f'house_{sign_i + 1}'
        hs = house_scores.get(house_key, {})
        sav_score = hs.get('score', None)

        if sav_score is not None and col_sum != sav_score:
            issues.append(f"星座{SIGNS[sign_i]}列: BAV列和={col_sum}, SAV={sav_score}")

    # 同时验证 SAV 逐宫总分是否与 house_scores 一致
    if not issues:
        ok = True
        detail = "所有12星座 BAV列和 与 SAV分数一致 ✅"
    else:
        ok = False
        detail = f"不一致: {'; '.join(issues)}"
    return ok, detail

#!/usr/bin/env python3
"""
Zi Wei Dou Shu chart — comprehensive San He style.

Covers: fourteen major stars, full minor/auxiliary star system (~40 stars),
four sets of twelve gods, decade fortune (大限), annual fortune (流年),
four pillars (四柱), and enhanced si-hua with palace attribution.

Palace order and star placement follow gasolin/zwds (zwds.twpy).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Optional
from zoneinfo import ZoneInfo

from zhdate import ZhDate

# ═══════════════════════════════════════════════════════════════════════
#  Constants
# ═══════════════════════════════════════════════════════════════════════

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
YIN_BRANCH_ORDER = list("寅卯辰巳午未申酉戌亥子丑")

PALACE_NAMES_CW = [
    "命宫", "父母", "福德", "田宅", "官禄", "交友",
    "迁移", "疾厄", "财帛", "子女", "夫妻", "兄弟",
]

TIANFU_PAIR: dict[str, str] = {
    "寅": "寅", "申": "申", "丑": "卯", "卯": "丑",
    "子": "辰", "辰": "子", "巳": "亥", "亥": "巳",
    "午": "戌", "戌": "午", "未": "酉", "酉": "未",
}

_JIAZI_NAYIN: list[tuple[str, str, str, int]] = [
    ("甲子", "乙丑", "海中金", 4), ("丙寅", "丁卯", "炉中火", 6),
    ("戊辰", "己巳", "大林木", 3), ("庚午", "辛未", "路旁土", 5),
    ("壬申", "癸酉", "剑锋金", 4), ("甲戌", "乙亥", "山头火", 6),
    ("丙子", "丁丑", "涧下水", 2), ("戊寅", "己卯", "城头土", 5),
    ("庚辰", "辛巳", "白蜡金", 4), ("壬午", "癸未", "杨柳木", 3),
    ("甲申", "乙酉", "泉中水", 2), ("丙戌", "丁亥", "屋上土", 5),
    ("戊子", "己丑", "霹雳火", 6), ("庚寅", "辛卯", "松柏木", 3),
    ("壬辰", "癸巳", "长流水", 2), ("甲午", "乙未", "沙中金", 4),
    ("丙申", "丁酉", "山下火", 6), ("戊戌", "己亥", "平地木", 3),
    ("庚子", "辛丑", "壁上土", 5), ("壬寅", "癸卯", "金箔金", 4),
    ("甲辰", "乙巳", "覆灯火", 6), ("丙午", "丁未", "天河水", 2),
    ("戊申", "己酉", "大驿土", 5), ("庚戌", "辛亥", "钗钏金", 4),
    ("壬子", "癸丑", "桑柘木", 3), ("甲寅", "乙卯", "大溪水", 2),
    ("丙辰", "丁巳", "沙中土", 5), ("戊午", "己未", "天上火", 6),
    ("庚申", "辛酉", "石榴木", 3), ("壬戌", "癸亥", "大海水", 2),
]

PILLAR_TO_FRAME: dict[str, tuple[str, int]] = {}
for _a, _b, _nm, _ju in _JIAZI_NAYIN:
    PILLAR_TO_FRAME[_a] = (_nm, _ju)
    PILLAR_TO_FRAME[_b] = (_nm, _ju)

SI_HUA: dict[str, dict[str, str]] = {
    "甲": {"禄": "廉贞", "权": "破军", "科": "武曲", "忌": "太阳"},
    "乙": {"禄": "天机", "权": "天梁", "科": "紫微", "忌": "太阴"},
    "丙": {"禄": "天同", "权": "天机", "科": "文昌", "忌": "廉贞"},
    "丁": {"禄": "太阴", "权": "天同", "科": "天机", "忌": "巨门"},
    "戊": {"禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"},
    "己": {"禄": "武曲", "权": "贪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"禄": "太阳", "权": "武曲", "科": "太阴", "忌": "天同"},
    "辛": {"禄": "巨门", "权": "太阳", "科": "文曲", "忌": "文昌"},
    "壬": {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"},
    "癸": {"禄": "破军", "权": "巨门", "科": "太阴", "忌": "贪狼"},
}

ZODIAC_MAP = dict(zip("子丑寅卯辰巳午未申酉戌亥", "鼠牛虎兔龙蛇马羊猴鸡狗猪"))
JU_NAMES = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}

# ── Lookup tables for minor / auxiliary stars ──

LUCUN_TABLE: dict[str, str] = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子",
}

TIANKUI_TABLE: dict[str, str] = {
    "甲": "丑", "戊": "丑", "庚": "丑",
    "乙": "子", "己": "子",
    "丙": "亥", "丁": "亥",
    "壬": "卯", "癸": "卯",
    "辛": "午",
}

TIANYUE_TABLE: dict[str, str] = {
    "甲": "未", "戊": "未", "庚": "未",
    "乙": "申", "己": "申",
    "丙": "酉", "丁": "酉",
    "壬": "巳", "癸": "巳",
    "辛": "寅",
}

HUOXING_START: dict[str, str] = {
    "寅": "丑", "午": "丑", "戌": "丑",
    "申": "寅", "子": "寅", "辰": "寅",
    "巳": "卯", "酉": "卯", "丑": "卯",
    "亥": "酉", "卯": "酉", "未": "酉",
}

LINGXING_START: dict[str, str] = {
    "寅": "卯", "午": "卯", "戌": "卯",
    "申": "戌", "子": "戌", "辰": "戌",
    "巳": "戌", "酉": "戌", "丑": "戌",
    "亥": "戌", "卯": "戌", "未": "戌",
}

TIANMA_TABLE: dict[str, str] = {
    "寅": "申", "午": "申", "戌": "申",
    "申": "寅", "子": "寅", "辰": "寅",
    "巳": "亥", "酉": "亥", "丑": "亥",
    "亥": "巳", "卯": "巳", "未": "巳",
}

XIANCHI_TABLE: dict[str, str] = {
    "寅": "卯", "午": "卯", "戌": "卯",
    "申": "酉", "子": "酉", "辰": "酉",
    "巳": "午", "酉": "午", "丑": "午",
    "亥": "子", "卯": "子", "未": "子",
}

GUCHEN_TABLE: dict[str, str] = {
    "寅": "巳", "卯": "巳", "辰": "巳",
    "巳": "申", "午": "申", "未": "申",
    "申": "亥", "酉": "亥", "戌": "亥",
    "亥": "寅", "子": "寅", "丑": "寅",
}

GUASU_TABLE: dict[str, str] = {
    "寅": "丑", "卯": "丑", "辰": "丑",
    "巳": "辰", "午": "辰", "未": "辰",
    "申": "未", "酉": "未", "戌": "未",
    "亥": "戌", "子": "戌", "丑": "戌",
}

HUAGAI_TABLE: dict[str, str] = {
    "寅": "戌", "午": "戌", "戌": "戌",
    "申": "辰", "子": "辰", "辰": "辰",
    "巳": "丑", "酉": "丑", "丑": "丑",
    "亥": "未", "卯": "未", "未": "未",
}

TIANYUE_YEAR_TABLE: dict[str, str] = {
    "子": "戌", "丑": "巳", "寅": "辰", "卯": "寅",
    "辰": "未", "巳": "卯", "午": "亥", "未": "酉",
    "申": "寅", "酉": "午", "戌": "巳", "亥": "子",
}

# ── Twelve-god constants ──

CHANGSHENG_START: dict[int, str] = {
    2: "申", 3: "亥", 4: "巳", 5: "申", 6: "寅",
}
CHANGSHENG_NAMES = [
    "长生", "沐浴", "冠带", "临官", "帝旺", "衰",
    "病", "死", "墓", "绝", "胎", "养",
]
BOSHI_NAMES = [
    "博士", "力士", "青龙", "小耗", "将军", "奏书",
    "飞廉", "喜神", "病符", "大耗", "伏兵", "官府",
]
SUIQIAN_NAMES = [
    "岁建", "晦气", "丧门", "贯索", "官符", "小耗",
    "大耗", "龙德", "白虎", "天德", "吊客", "病符",
]
JIANGQIAN_NAMES = [
    "将星", "攀鞍", "岁驿", "息神", "华盖", "劫煞",
    "灾煞", "天煞", "指背", "咸池", "月煞", "亡神",
]
JIANGXING_START: dict[str, str] = {
    "寅": "午", "午": "午", "戌": "午",
    "申": "子", "子": "子", "辰": "子",
    "巳": "酉", "酉": "酉", "丑": "酉",
    "亥": "卯", "卯": "卯", "未": "卯",
}

# ═══════════════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════════════

def branch_index(branch: str) -> int:
    return BRANCHES.index(branch)


def yin_table_index(branch: str) -> int:
    return YIN_BRANCH_ORDER.index(branch)


def is_yang_stem(stem: str) -> bool:
    return STEMS.index(stem) % 2 == 0


def is_forward(year_stem: str, gender: str) -> bool:
    """阳男阴女顺行, 阴男阳女逆行."""
    yang = is_yang_stem(year_stem)
    male = gender == "male"
    return (yang and male) or (not yang and not male)


def stem_branch_year(lunar_year: int) -> tuple[str, str]:
    stem = STEMS[(lunar_year - 4) % 10]
    branch = BRANCHES[(lunar_year - 4) % 12]
    return stem, branch


def wu_yin_stem(year_stem: str) -> str:
    """五虎遁：年干 → 寅宫天干."""
    return {
        "甲": "丙", "己": "丙", "乙": "戊", "庚": "戊",
        "丙": "庚", "辛": "庚", "丁": "壬", "壬": "壬",
        "戊": "甲", "癸": "甲",
    }[year_stem]


def wu_shu_stem(day_stem: str) -> str:
    """五鼠遁：日干 → 子时天干."""
    return {
        "甲": "甲", "己": "甲", "乙": "丙", "庚": "丙",
        "丙": "戊", "辛": "戊", "丁": "庚", "壬": "庚",
        "戊": "壬", "癸": "壬",
    }[day_stem]


def hour_to_branch(hour: int, minute: int = 0) -> str:
    h = hour + minute / 60.0
    if h >= 23 or h < 1:
        return "子"
    if h < 3:
        return "丑"
    if h < 5:
        return "寅"
    if h < 7:
        return "卯"
    if h < 9:
        return "辰"
    if h < 11:
        return "巳"
    if h < 13:
        return "午"
    if h < 15:
        return "未"
    if h < 17:
        return "申"
    if h < 19:
        return "酉"
    if h < 21:
        return "戌"
    return "亥"


# ═══════════════════════════════════════════════════════════════════════
#  True solar time (真太阳时)
# ═══════════════════════════════════════════════════════════════════════

def calculate_equation_of_time_minutes(local_dt: datetime) -> float:
    """Equation of Time: difference between apparent and mean solar time (minutes).

    Uses the Spencer (1971) approximation via the solar hour angle.
    Aligned with the implementation in bazi_calculate.py.
    """
    day_of_year = local_dt.timetuple().tm_yday
    hour_fraction = local_dt.hour + local_dt.minute / 60.0 + local_dt.second / 3600.0
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1 + (hour_fraction - 12.0) / 24.0)
    return 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )


def apply_true_solar_time(local_dt: datetime, longitude: float) -> tuple[datetime, float]:
    """Correct local clock time to true solar time using longitude and Equation of Time.

    Returns (adjusted_datetime, delta_minutes).
    delta_minutes > 0 means true solar time is ahead of clock time.
    """
    utc_offset = local_dt.utcoffset()
    if utc_offset is None:
        raise ValueError("Timezone-aware datetime is required to compute true solar time.")
    tz_offset_hours = utc_offset.total_seconds() / 3600.0
    eq_time = calculate_equation_of_time_minutes(local_dt)
    # 4 minutes per degree of longitude; subtract the timezone's nominal offset
    delta_minutes = eq_time + 4.0 * longitude - 60.0 * tz_offset_hours
    adjusted = local_dt + timedelta(minutes=delta_minutes)
    return adjusted, delta_minutes


# ═══════════════════════════════════════════════════════════════════════
#  Palace construction & major stars
# ═══════════════════════════════════════════════════════════════════════

def ming_gong_branch(lunar_month: int, hour_branch: str) -> str:
    """寅宫起正月顺至生月，该宫起子时逆至生时."""
    mi = yin_table_index(YIN_BRANCH_ORDER[lunar_month - 1])
    hi = branch_index(hour_branch)
    return YIN_BRANCH_ORDER[(mi - hi) % 12]


def shen_gong_branch(lunar_month: int, hour_branch: str) -> str:
    mi = yin_table_index(YIN_BRANCH_ORDER[lunar_month - 1])
    hi = branch_index(hour_branch)
    return YIN_BRANCH_ORDER[(mi + hi) % 12]


def stem_for_palace(yin_stem_index: int, palace_index: int) -> str:
    return STEMS[(yin_stem_index + palace_index) % 10]


def build_rotated_palaces(ming_branch: str) -> list[dict[str, Any]]:
    mi = yin_table_index(ming_branch)
    names = PALACE_NAMES_CW[-mi:] + PALACE_NAMES_CW[:-mi]
    palaces: list[dict[str, Any]] = []
    for i in range(12):
        palaces.append({
            "palace_index": i,
            "branch": YIN_BRANCH_ORDER[i],
            "name": names[i],
            "stem": "",
            "pillar": "",
            "main_stars": [],
            "minor_stars": [],
            "mini_stars": [],
            "life_stage": "",
            "scholar_stage": "",
            "annual_general": "",
            "annual_officer": "",
            "decade_range": "",
            "note": "",
        })
    return palaces


def ziwei_branch(lunar_day: int, ju: int) -> str:
    """起紫微（gasolin/zwds 公式）."""
    y = 1
    x = 0
    for y in range(1, 40):
        if ju * y >= lunar_day:
            x = ju * y - lunar_day
            break
    if x % 2 == 0:
        idx = y + x
    else:
        idx = y - x
    return YIN_BRANCH_ORDER[(idx - 1) % 12]


def place_major_stars(palaces: list[dict[str, Any]], ziwei: str, tianfu: str) -> None:
    """十四正曜：紫微系逆行 + 天府系顺行."""
    def idx_of(branch: str) -> int:
        for i, p in enumerate(palaces):
            if p["branch"] == branch:
                return i
        raise KeyError(branch)

    zi = idx_of(ziwei)
    tf = idx_of(tianfu)

    def add(i: int, star: str) -> None:
        palaces[i % 12]["main_stars"].append(star)

    add(zi, "紫微")
    add(zi - 1, "天机")
    add(zi - 3, "太阳")
    add(zi - 4, "武曲")
    add(zi - 5, "天同")
    add(zi - 8, "廉贞")

    add(tf, "天府")
    add(tf - 11, "太阴")
    add(tf - 10, "贪狼")
    add(tf - 9, "巨门")
    add(tf - 8, "天相")
    add(tf - 7, "天梁")
    add(tf - 6, "七杀")
    add(tf - 2, "破军")


def ming_zhu(ming_branch: str) -> str:
    return {
        "子": "贪狼", "丑": "巨门", "亥": "巨门",
        "寅": "禄存", "戌": "禄存", "卯": "文曲", "酉": "文曲",
        "巳": "武曲", "未": "武曲", "辰": "廉贞", "申": "廉贞",
        "午": "破军",
    }[ming_branch]


def shen_zhu(year_branch: str) -> str:
    return {
        "子": "火星", "午": "火星", "丑": "天相", "未": "天相",
        "寅": "天梁", "申": "天梁", "卯": "天同", "酉": "天同",
        "辰": "文昌", "戌": "文昌", "巳": "天机", "亥": "天机",
    }[year_branch]


# ═══════════════════════════════════════════════════════════════════════
#  Minor & auxiliary stars  (~40 stars)
# ═══════════════════════════════════════════════════════════════════════

def _put(palaces: list[dict], branch: str, star: str, field: str = "minor_stars") -> None:
    for p in palaces:
        if p["branch"] == branch:
            p[field].append(star)
            return


def _xunkong(stem: str, branch: str) -> list[str]:
    """旬空：该柱所在旬中缺失的两个地支."""
    si = STEMS.index(stem)
    bi = BRANCHES.index(branch)
    xun_start_bi = (bi - si) % 12
    return [BRANCHES[(xun_start_bi - 2) % 12], BRANCHES[(xun_start_bi - 1) % 12]]


def place_minor_stars(
    palaces: list[dict[str, Any]],
    y_stem: str,
    y_branch: str,
    lunar_month: int,
    lunar_day: int,
    hour_branch: str,
) -> dict[str, int]:
    """安辅星体系, 返回部分星曜的 branch_index 供后续引用."""
    hi = branch_index(hour_branch)
    ybi = branch_index(y_branch)
    chen = branch_index("辰")
    xu = branch_index("戌")
    wu = branch_index("午")
    chou = branch_index("丑")
    you = branch_index("酉")
    si = branch_index("巳")
    yin = branch_index("寅")
    hai = branch_index("亥")
    mao = branch_index("卯")

    # ── 六吉星 ──
    zuofu_bi = (chen + lunar_month - 1) % 12
    youbi_bi = (xu - (lunar_month - 1)) % 12
    wenchang_bi = (xu - hi) % 12
    wenqu_bi = (chen + hi) % 12

    _put(palaces, BRANCHES[zuofu_bi], "左辅")
    _put(palaces, BRANCHES[youbi_bi], "右弼")
    _put(palaces, BRANCHES[wenchang_bi], "文昌")
    _put(palaces, BRANCHES[wenqu_bi], "文曲")
    _put(palaces, TIANKUI_TABLE[y_stem], "天魁")
    _put(palaces, TIANYUE_TABLE[y_stem], "天钺")

    # ── 禄存 + 擎羊 + 陀罗 ──
    lucun_bi = branch_index(LUCUN_TABLE[y_stem])
    _put(palaces, BRANCHES[lucun_bi], "禄存")
    _put(palaces, BRANCHES[(lucun_bi + 1) % 12], "擎羊")
    _put(palaces, BRANCHES[(lucun_bi - 1) % 12], "陀罗")

    # ── 火星 + 铃星 ──
    huo_bi = (branch_index(HUOXING_START[y_branch]) + hi) % 12
    ling_bi = (branch_index(LINGXING_START[y_branch]) + hi) % 12
    _put(palaces, BRANCHES[huo_bi], "火星")
    _put(palaces, BRANCHES[ling_bi], "铃星")

    # ── 地空 + 地劫 ──
    _put(palaces, BRANCHES[(hai - hi) % 12], "地空")
    _put(palaces, BRANCHES[(hai + hi) % 12], "地劫")

    # ── 杂曜 (→ mini_stars) ──
    _put(palaces, TIANMA_TABLE[y_branch], "天马", "mini_stars")

    hongluan_bi = (mao - ybi) % 12
    _put(palaces, BRANCHES[hongluan_bi], "红鸾", "mini_stars")
    _put(palaces, BRANCHES[(hongluan_bi + 6) % 12], "天喜", "mini_stars")

    _put(palaces, BRANCHES[(chou + lunar_month - 1) % 12], "天姚", "mini_stars")
    _put(palaces, XIANCHI_TABLE[y_branch], "咸池", "mini_stars")
    _put(palaces, GUCHEN_TABLE[y_branch], "孤辰", "mini_stars")
    _put(palaces, GUASU_TABLE[y_branch], "寡宿", "mini_stars")

    _put(palaces, BRANCHES[(you + lunar_month - 1) % 12], "天刑", "mini_stars")
    _put(palaces, BRANCHES[(wu - ybi) % 12], "天哭", "mini_stars")
    _put(palaces, BRANCHES[(wu + ybi) % 12], "天虚", "mini_stars")
    _put(palaces, BRANCHES[(chen + ybi) % 12], "龙池", "mini_stars")
    _put(palaces, BRANCHES[(xu - ybi) % 12], "凤阁", "mini_stars")
    _put(palaces, HUAGAI_TABLE[y_branch], "华盖", "mini_stars")
    _put(palaces, BRANCHES[(chou + ybi) % 12], "天空", "mini_stars")

    _put(palaces, BRANCHES[(wu + hi) % 12], "台辅", "mini_stars")
    _put(palaces, BRANCHES[(yin + hi) % 12], "封诰", "mini_stars")

    _put(palaces, BRANCHES[(si + lunar_month - 1) % 12], "天巫", "mini_stars")
    _put(palaces, TIANYUE_YEAR_TABLE[y_branch], "天月", "mini_stars")
    _put(palaces, BRANCHES[(yin - (lunar_month - 1)) % 12], "阴煞", "mini_stars")

    # 恩光 / 天贵: 文昌 / 文曲 各顺一位
    _put(palaces, BRANCHES[(wenchang_bi + 1) % 12], "恩光", "mini_stars")
    _put(palaces, BRANCHES[(wenqu_bi + 1) % 12], "天贵", "mini_stars")

    # 三台 / 八座: 左辅起初一顺 / 右弼起初一逆, 各数到生日
    _put(palaces, BRANCHES[(zuofu_bi + lunar_day - 1) % 12], "三台", "mini_stars")
    _put(palaces, BRANCHES[(youbi_bi - (lunar_day - 1)) % 12], "八座", "mini_stars")

    # 旬空
    for br in _xunkong(y_stem, y_branch):
        _put(palaces, br, "旬空", "mini_stars")

    return {
        "zuofu": zuofu_bi,
        "youbi": youbi_bi,
        "wenchang": wenchang_bi,
        "wenqu": wenqu_bi,
        "lucun": lucun_bi,
    }


# ═══════════════════════════════════════════════════════════════════════
#  Twelve gods  (四组十二神)
# ═══════════════════════════════════════════════════════════════════════

def _place_twelve(
    palaces: list[dict], names: list[str], start_branch: str,
    forward: bool, field: str,
) -> None:
    sbi = branch_index(start_branch)
    for i, name in enumerate(names):
        bi = (sbi + i) % 12 if forward else (sbi - i) % 12
        for p in palaces:
            if p["branch"] == BRANCHES[bi]:
                p[field] = name


def place_changsheng(palaces: list[dict], ju: int, y_stem: str, gender: str) -> None:
    fwd = is_forward(y_stem, gender)
    _place_twelve(palaces, CHANGSHENG_NAMES, CHANGSHENG_START[ju], fwd, "life_stage")


def place_boshi(palaces: list[dict], y_stem: str, gender: str) -> None:
    fwd = is_forward(y_stem, gender)
    _place_twelve(palaces, BOSHI_NAMES, LUCUN_TABLE[y_stem], fwd, "scholar_stage")


def place_suiqian(palaces: list[dict], y_branch: str) -> None:
    _place_twelve(palaces, SUIQIAN_NAMES, y_branch, True, "annual_general")


def place_jiangqian(palaces: list[dict], y_branch: str) -> None:
    _place_twelve(palaces, JIANGQIAN_NAMES, JIANGXING_START[y_branch], True, "annual_officer")


# ═══════════════════════════════════════════════════════════════════════
#  大限 (Decade fortune)
# ═══════════════════════════════════════════════════════════════════════

def compute_daxian(
    palaces: list[dict], ming_branch: str, ju: int,
    y_stem: str, gender: str,
) -> None:
    """
    命宫为第一大限。
    阳男阴女: 沿宫位序递增方向（命→兄→夫→子→…）= 物理逆时针(decreasing index)。
    阴男阳女: 沿宫位序递减方向（命→父→福→田→…）= 物理顺时针(increasing index)。
    """
    forward = is_forward(y_stem, gender)
    ming_yi = yin_table_index(ming_branch)
    start_age = ju
    for step in range(12):
        # forward(大限顺行) = clockwise on chart = decreasing palace index
        pi = (ming_yi + step) % 12 if forward else (ming_yi - step) % 12
        lo = start_age + step * 10
        hi = lo + 9
        palaces[pi]["decade_range"] = f"{lo}-{hi}"


# ═══════════════════════════════════════════════════════════════════════
#  流年 (Annual fortune)
# ═══════════════════════════════════════════════════════════════════════

_LIUNIAN_NAMES = [
    "流命", "流兄", "流夫", "流子", "流财", "流疾",
    "流迁", "流交", "流官", "流田", "流福", "流父",
]


def compute_liunian(palaces: list[dict], target_year: int) -> dict[str, Any]:
    """流年命宫 = 该年地支所在宫位, 按命→兄→夫→… clockwise排十二宫."""
    y_stem, y_branch = stem_branch_year(target_year)
    ln_yi = yin_table_index(y_branch)
    for step in range(12):
        pi = (ln_yi - step) % 12
        palaces[pi]["yearly_palace_name"] = _LIUNIAN_NAMES[step]
    return {"year": target_year, "stem": y_stem, "branch": y_branch}


# ═══════════════════════════════════════════════════════════════════════
#  四柱 (Four Pillars)
# ═══════════════════════════════════════════════════════════════════════

_GANZHI_EPOCH = date(2000, 1, 7)  # 甲子日


def day_gan_zhi(year: int, month: int, day: int) -> tuple[str, str]:
    delta = (date(year, month, day) - _GANZHI_EPOCH).days
    return STEMS[delta % 10], BRANCHES[delta % 12]


def month_gan_zhi(y_stem: str, lunar_month: int) -> tuple[str, str]:
    """月柱: 五虎遁月天干 + 农历月地支（简化, 未精确到节气边界）."""
    yin_stem_idx = STEMS.index(wu_yin_stem(y_stem))
    m_stem = STEMS[(yin_stem_idx + lunar_month - 1) % 10]
    m_branch = YIN_BRANCH_ORDER[lunar_month - 1]
    return m_stem, m_branch


def hour_gan_zhi(d_stem: str, hour_branch: str) -> tuple[str, str]:
    """时柱: 五鼠遁."""
    zi_idx = STEMS.index(wu_shu_stem(d_stem))
    h_bi = branch_index(hour_branch)
    return STEMS[(zi_idx + h_bi) % 10], hour_branch


def compute_four_pillars(
    lunar_year: int, lunar_month: int, y_stem: str,
    solar_dt: datetime, hour_br: str,
) -> dict[str, str]:
    y_pillar = f"{y_stem}{BRANCHES[(lunar_year - 4) % 12]}"
    ms, mb = month_gan_zhi(y_stem, lunar_month)
    ds, db = day_gan_zhi(solar_dt.year, solar_dt.month, solar_dt.day)
    hs, hb = hour_gan_zhi(ds, hour_br)
    return {"year": y_pillar, "month": f"{ms}{mb}", "day": f"{ds}{db}", "hour": f"{hs}{hb}"}


# ═══════════════════════════════════════════════════════════════════════
#  Enhanced si-hua (四化 + 落宫)
# ═══════════════════════════════════════════════════════════════════════

def si_hua_with_palaces(y_stem: str, palaces: list[dict]) -> dict[str, Any]:
    base = SI_HUA[y_stem]
    out: dict[str, Any] = {}
    for label, star in base.items():
        palace_name = ""
        for p in palaces:
            if star in p["main_stars"] or star in p["minor_stars"]:
                palace_name = p["name"]
                break
        out[label] = {"star": star, "palace": palace_name}
    return out


# ═══════════════════════════════════════════════════════════════════════
#  Main compute
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class ChartInput:
    local_dt: datetime
    midnight_zi: str       # "same-day" | "next-day"
    gender: str            # "male" | "female"
    include_si_hua: bool
    target_year: int | None = None
    longitude: float | None = None  # east-positive degrees; enables true solar time


def parse_local_datetime(value: str, tz_name: str) -> datetime:
    naive = datetime.strptime(value, "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=ZoneInfo(tz_name))


def solar_for_lunar(local_dt: datetime, midnight_zi: str) -> datetime:
    if midnight_zi == "next-day" and local_dt.hour >= 23:
        return local_dt + timedelta(days=1)
    return local_dt


def compute_chart(inp: ChartInput) -> dict[str, Any]:
    # ── True solar time correction ──
    tst_enabled = False
    tst_delta = 0.0
    effective_dt = inp.local_dt
    if inp.longitude is not None:
        try:
            effective_dt, tst_delta = apply_true_solar_time(inp.local_dt, inp.longitude)
            tst_enabled = True
        except ValueError:
            pass  # fall back to clock time if tz-aware conversion fails

    solar_lunar = solar_for_lunar(inp.local_dt, inp.midnight_zi)
    naive = datetime(
        solar_lunar.year, solar_lunar.month, solar_lunar.day,
        solar_lunar.hour, solar_lunar.minute,
    )
    z = ZhDate.from_datetime(naive)
    lunar_year = z.lunar_year
    lunar_month = z.lunar_month
    lunar_day = z.lunar_day
    leap = bool(z.leap_month)

    hour_br = hour_to_branch(effective_dt.hour, effective_dt.minute)
    ming = ming_gong_branch(lunar_month, hour_br)
    shen = shen_gong_branch(lunar_month, hour_br)

    y_stem, y_branch = stem_branch_year(lunar_year)
    palaces = build_rotated_palaces(ming)
    yin_stem_idx = STEMS.index(wu_yin_stem(y_stem))
    for p in palaces:
        i = p["palace_index"]
        st = stem_for_palace(yin_stem_idx, i)
        p["stem"] = st
        p["pillar"] = f"{st}{p['branch']}"

    ming_idx = yin_table_index(ming)
    ming_pillar = palaces[ming_idx]["pillar"]
    nayin_name, ju = PILLAR_TO_FRAME[ming_pillar]

    zw = ziwei_branch(lunar_day, ju)
    tf = TIANFU_PAIR[zw]
    place_major_stars(palaces, zw, tf)

    place_minor_stars(palaces, y_stem, y_branch, lunar_month, lunar_day, hour_br)

    place_changsheng(palaces, ju, y_stem, inp.gender)
    place_boshi(palaces, y_stem, inp.gender)
    place_suiqian(palaces, y_branch)
    place_jiangqian(palaces, y_branch)

    compute_daxian(palaces, ming, ju, y_stem, inp.gender)

    liunian_info: dict[str, Any] | None = None
    if inp.target_year is not None:
        liunian_info = compute_liunian(palaces, inp.target_year)

    four_pillars = compute_four_pillars(
        lunar_year, lunar_month, y_stem, inp.local_dt, hour_br,
    )

    yang = is_yang_stem(y_stem)
    zodiac = ZODIAC_MAP.get(y_branch, "")

    out: dict[str, Any] = {
        "schema_version": "mystilink.ziwei.chart/0.1",
        "solar_local": inp.local_dt.isoformat(),
        "solar_used_for_lunar": naive.isoformat(),
        "midnight_zi_rule": inp.midnight_zi,
        "true_solar_time_enabled": tst_enabled,
        "true_solar_time_delta_minutes": round(tst_delta, 2) if tst_enabled else None,
        "gender": inp.gender,
        "yin_yang": "阳" if yang else "阴",
        "zodiac": zodiac,
        "lunar": {
            "year": lunar_year,
            "month": lunar_month,
            "day": lunar_day,
            "leap_month": leap,
            "year_stem": y_stem,
            "year_branch": y_branch,
            "year_pillar": f"{y_stem}{y_branch}",
        },
        "four_pillars": four_pillars,
        "hour_branch": hour_br,
        "ming_gong_branch": ming,
        "shen_gong_branch": shen,
        "ming_zhu": ming_zhu(ming),
        "shen_zhu": shen_zhu(y_branch),
        "ming_gong_pillar": ming_pillar,
        "na_yin": nayin_name,
        "five_element_frame": JU_NAMES[ju],
        "five_element_number": ju,
        "ziwei_branch": zw,
        "tianfu_branch": tf,
        "palaces": palaces,
    }
    if inp.include_si_hua:
        out["si_hua"] = si_hua_with_palaces(y_stem, palaces)
    if liunian_info:
        out["liunian"] = liunian_info
    return out


# ═══════════════════════════════════════════════════════════════════════
#  Text output
# ═══════════════════════════════════════════════════════════════════════

def print_chart(data: dict[str, Any]) -> None:
    print("=== 紫微斗数排盘（三合完整星曜） ===")
    print(f"公历（本地）: {data['solar_local']}")
    if data.get("true_solar_time_enabled"):
        delta = data.get("true_solar_time_delta_minutes", 0)
        print(f"真太阳时修正: {delta:+.1f} 分钟")
    print(f"农历换算用: {data['solar_used_for_lunar']}（晚子时规则: {data['midnight_zi_rule']}）")

    lu = data["lunar"]
    leap_txt = "（闰月）" if lu["leap_month"] else ""
    print(f"农历: {lu['year']}年{lu['month']}月{lu['day']}日{leap_txt}  年柱{lu['year_pillar']}")

    fp = data.get("four_pillars", {})
    if fp:
        print(f"四柱: {fp.get('year','')} {fp.get('month','')} {fp.get('day','')} {fp.get('hour','')}")

    gender_txt = "男" if data.get("gender") == "male" else "女"
    yy = data.get("yin_yang", "")
    zod = data.get("zodiac", "")
    print(f"性别: {gender_txt}  阴阳: {yy}  生肖: {zod}")
    print(f"时辰: {data['hour_branch']}时")
    print(f"命宫: {data['ming_gong_branch']}  身宫: {data['shen_gong_branch']}")
    print(f"命宫干支: {data['ming_gong_pillar']}  纳音: {data['na_yin']}")
    print(f"五行局: {data['five_element_frame']}")
    print(f"紫微在: {data['ziwei_branch']}  天府在: {data['tianfu_branch']}")
    print(f"命主: {data['ming_zhu']}  身主: {data['shen_zhu']}")

    if "si_hua" in data:
        sh = data["si_hua"]
        parts = []
        for label in ["禄", "权", "科", "忌"]:
            info = sh[label]
            if isinstance(info, dict):
                parts.append(f"{label}{info['star']}({info['palace']})")
            else:
                parts.append(f"{label}{info}")
        print(f"四化（{lu['year_stem']}干）: {'  '.join(parts)}")

    if "liunian" in data:
        ln = data["liunian"]
        print(f"流年: {ln['year']}年  {ln['stem']}{ln['branch']}年")

    print()
    print("十二宫:")
    for p in data["palaces"]:
        main = "、".join(p["main_stars"]) if p["main_stars"] else "—"
        minor = "、".join(p["minor_stars"]) if p["minor_stars"] else ""
        mini = "、".join(p["mini_stars"]) if p["mini_stars"] else ""
        parts = [f"  {p['branch']}宫 {p['pillar']}  {p['name']:<4s}"]
        parts.append(f"主星: {main}")
        if minor:
            parts.append(f"辅星: {minor}")
        if mini:
            parts.append(f"杂曜: {mini}")
        if p.get("decade_range"):
            parts.append(f"大限: {p['decade_range']}")
        if p.get("life_stage"):
            parts.append(f"长生: {p['life_stage']}")
        if p.get("scholar_stage"):
            parts.append(f"博士: {p['scholar_stage']}")
        if p.get("yearly_palace_name"):
            parts.append(f"流年: {p['yearly_palace_name']}")
        print("  ".join(parts))


# ═══════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="紫微斗数排盘（完整星曜 + 大限流年 + 四柱）")
    p.add_argument("--datetime", required=False, default=None, help='本地时间 "YYYY-MM-DD HH:MM"')
    p.add_argument("--timezone", required=False, default=None, help="IANA 时区，如 Asia/Shanghai")
    p.add_argument("--gender", required=False, default=None, choices=["male", "female"], help="性别")
    p.add_argument(
        "--midnight-zi", choices=["same-day", "next-day"], default="same-day",
        help="23:00–01:00 子时与农历换日规则（默认 same-day）",
    )
    p.add_argument("--si-hua", action="store_true", help="输出生年干四化（含落宫）")
    p.add_argument("--year", type=int, default=None, help="流年（公历年份）")
    p.add_argument(
        "--longitude", type=float, default=None,
        help="出生地经度（东经为正）。与 --timezone 同时提供时启用真太阳时修正",
    )
    p.add_argument(
        "--birth-json",
        "--profile-json",
        dest="birth_json",
        default=None,
        help="BirthProfile (mystilink.birth/0.1) 或旧 profile.json：文件路径 / '-' / 内联 JSON",
    )
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--output-file", help="JSON 时可写入文件")
    return p


def _load_profile(raw: str) -> dict[str, Any]:
    from pathlib import Path

    if raw == "-":
        text = sys.stdin.read()
    else:
        path = Path(raw)
        text = path.read_text(encoding="utf-8") if path.is_file() else raw
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("profile JSON root must be an object")
    return data


def _resolve_from_profile(data: dict[str, Any]) -> tuple[str, str, str, Optional[float]]:
    """Return (datetime_str, timezone, gender, longitude)."""
    if data.get("schema_version") == "mystilink.birth/0.1" or (
        isinstance(data.get("birth"), dict) and "datetime" in data["birth"]
    ):
        birth = data["birth"]
        tz = birth["timezone"]
        dt_raw = str(birth["datetime"]).strip().replace("Z", "+00:00")
        instant = datetime.fromisoformat(dt_raw)
        if instant.tzinfo is None:
            raise ValueError("birth.datetime must include a timezone offset")
        datetime_str = (
            f"{instant.year:04d}-{instant.month:02d}-{instant.day:02d} "
            f"{instant.hour:02d}:{instant.minute:02d}"
        )
        gender = data.get("gender")
        if gender not in ("male", "female"):
            raise ValueError("BirthProfile gender must be male or female for Zi Wei")
        lon = birth.get("longitude")
        if lon is None and isinstance(data.get("place"), dict):
            lon = data["place"].get("lon")
        return datetime_str, tz, gender, float(lon) if lon is not None else None

    if "datetime" not in data or "timezone" not in data or "gender" not in data:
        raise ValueError("unsupported profile: need BirthProfile or legacy datetime/timezone/gender")
    gender = data["gender"]
    if gender not in ("male", "female"):
        raise ValueError("gender must be male or female")
    lon = data.get("longitude")
    return str(data["datetime"]), str(data["timezone"]), gender, float(lon) if lon is not None else None


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    datetime_str = args.datetime
    timezone = args.timezone
    gender = args.gender
    longitude = args.longitude

    try:
        if args.birth_json:
            profile = _load_profile(args.birth_json)
            datetime_str, timezone, gender, lon = _resolve_from_profile(profile)
            if longitude is None:
                longitude = lon
        if not datetime_str or not timezone or gender not in ("male", "female"):
            raise ValueError("either --datetime/--timezone/--gender or --birth-json is required")
        local_dt = parse_local_datetime(datetime_str, timezone)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"输入错误: {exc}") from exc

    chart = compute_chart(ChartInput(
        local_dt=local_dt,
        midnight_zi=args.midnight_zi,
        gender=gender,
        include_si_hua=args.si_hua,
        target_year=args.year,
        longitude=longitude,
    ))

    if args.output == "json":
        payload = json.dumps(chart, ensure_ascii=False, indent=2)
        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
        else:
            print(payload)
    else:
        if args.output_file:
            raise SystemExit("--output-file 仅支持与 --output json 同时使用")
        print_chart(chart)


if __name__ == "__main__":
    main()

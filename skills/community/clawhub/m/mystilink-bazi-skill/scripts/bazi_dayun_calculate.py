#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字大运计算。

核心逻辑：
  1. 由年柱天干阴阳 + 性别 → 确定大运顺逆（阳男阴女顺行，阴男阳女逆行）
  2. 由出生日 → 最近的节气交界 → 计算起运年龄（天数 ÷ 3，每 3 天折 1 岁）
  3. 以月柱干支为起点，沿六十甲子顺/逆排列，每步管 10 年

输出 JSON：大运列表 + 起运信息。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any, Dict, List

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

STEM_ELEMENTS = {
    "甲": "Wood", "乙": "Wood", "丙": "Fire", "丁": "Fire", "戊": "Earth",
    "己": "Earth", "庚": "Metal", "辛": "Metal", "壬": "Water", "癸": "Water",
}
BRANCH_ELEMENTS: Dict[str, str] = {
    "寅": "Wood", "卯": "Wood", "巳": "Fire", "午": "Fire",
    "辰": "Earth", "戌": "Earth", "丑": "Earth", "未": "Earth",
    "申": "Metal", "酉": "Metal", "亥": "Water", "子": "Water",
}

# ─── 节气日期表（简化版：固定公历日，用于起运年龄计算） ───────────────
# 每个月有两个节气，大运起运只看"节"（非"气"），即每月第一个节气
# 索引 0-11 对应节气：立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒
# (month, day) 为近似日期
JIEQI_APPROXIMATE: List[tuple[int, int]] = [
    (2, 4),    # 立春
    (3, 6),    # 惊蛰
    (4, 5),    # 清明
    (5, 6),    # 立夏
    (6, 6),    # 芒种
    (7, 7),    # 小暑
    (8, 8),    # 立秋
    (9, 8),    # 白露
    (10, 8),   # 寒露
    (11, 7),   # 立冬
    (12, 7),   # 大雪
    (1, 6),    # 小寒
]


def _jieqi_dates_for_year(year: int) -> List[date]:
    """生成一年中 12 个月节的近似日期列表（按日历顺序排列）。"""
    dates = []
    for month, day in JIEQI_APPROXIMATE:
        y = year if month >= 2 else year + 1
        dates.append(date(y, month, day))
    # 按日期排序
    dates.sort()
    return dates


def compute_start_age(birth_date: date, forward: bool) -> tuple[int, int, int]:
    """
    计算起运年龄。
    - forward=True: 数到下一个节气
    - forward=False: 数到上一个节气
    返回 (起运岁数, 起运月数, 间隔天数)
    """
    year = birth_date.year
    all_jieqi: List[date] = []
    for y in range(year - 1, year + 2):
        all_jieqi.extend(_jieqi_dates_for_year(y))
    all_jieqi.sort()

    if forward:
        # 找到出生日之后的第一个节气
        target = None
        for jq in all_jieqi:
            if jq > birth_date:
                target = jq
                break
        if target is None:
            target = birth_date
        delta_days = (target - birth_date).days
    else:
        # 找到出生日之前（含当天）的最近一个节气
        target = None
        for jq in reversed(all_jieqi):
            if jq <= birth_date:
                target = jq
                break
        if target is None:
            target = birth_date
        delta_days = (birth_date - target).days

    # 3 天 = 1 岁，余数折月（余 1 天 ≈ 4 个月，余 2 天 ≈ 8 个月）
    start_age = delta_days // 3
    remainder = delta_days % 3
    extra_months = remainder * 4
    return start_age, extra_months, delta_days


def compute_month_pillar(birth_date: date, year_stem: str) -> tuple[str, str]:
    """简化月柱计算（与 bazi_calculate.py 对齐）。"""
    month, day = birth_date.month, birth_date.day
    if (month == 2 and day >= 4) or (month == 3 and day < 5):
        branch = "寅"
    elif (month == 3 and day >= 5) or (month == 4 and day < 5):
        branch = "卯"
    elif (month == 4 and day >= 5) or (month == 5 and day < 6):
        branch = "辰"
    elif (month == 5 and day >= 6) or (month == 6 and day < 6):
        branch = "巳"
    elif (month == 6 and day >= 6) or (month == 7 and day < 7):
        branch = "午"
    elif (month == 7 and day >= 7) or (month == 8 and day < 8):
        branch = "未"
    elif (month == 8 and day >= 8) or (month == 9 and day < 8):
        branch = "申"
    elif (month == 9 and day >= 8) or (month == 10 and day < 9):
        branch = "酉"
    elif (month == 10 and day >= 9) or (month == 11 and day < 8):
        branch = "戌"
    elif (month == 11 and day >= 8) or (month == 12 and day < 7):
        branch = "亥"
    elif (month == 12 and day >= 7) or (month == 1 and day < 6):
        branch = "子"
    else:
        branch = "丑"

    month_stem_rules = {
        "甲": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
        "乙": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
        "丙": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
        "丁": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
        "戊": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
        "己": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
        "庚": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
        "辛": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
        "壬": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
        "癸": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
    }
    branch_index = EARTHLY_BRANCHES.index(branch)
    month_index = (branch_index - 2) % 12
    stem = month_stem_rules[year_stem][month_index]
    return stem, branch


def compute_year_pillar(birth_date: date) -> tuple[str, str]:
    """简化年柱计算（与 bazi_calculate.py 对齐）。"""
    year = birth_date.year
    if birth_date.month < 2 or (birth_date.month == 2 and birth_date.day < 4):
        year -= 1
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


def is_dayun_forward(year_stem: str, gender: str) -> bool:
    """阳男阴女顺行，阴男阳女逆行。"""
    stem_idx = HEAVENLY_STEMS.index(year_stem)
    yang_stem = (stem_idx % 2 == 0)
    is_male = (gender == "male")
    return yang_stem == is_male


def compute_dayun(
    birth_date: date,
    gender: str,
    count: int = 8,
) -> Dict[str, Any]:
    """计算大运列表。"""
    year_stem, year_branch = compute_year_pillar(birth_date)
    month_stem, month_branch = compute_month_pillar(birth_date, year_stem)

    forward = is_dayun_forward(year_stem, gender)
    start_age, extra_months, delta_days = compute_start_age(birth_date, forward)

    stem_idx = HEAVENLY_STEMS.index(month_stem)
    branch_idx = EARTHLY_BRANCHES.index(month_branch)

    dayun_list: List[Dict[str, Any]] = []
    for i in range(1, count + 1):
        step = i if forward else -i
        s = HEAVENLY_STEMS[(stem_idx + step) % 10]
        b = EARTHLY_BRANCHES[(branch_idx + step) % 12]
        lo = start_age + (i - 1) * 10
        hi = lo + 9
        dayun_list.append({
            "index": i,
            "stem": s,
            "branch": b,
            "ganzhi": s + b,
            "stem_element": STEM_ELEMENTS.get(s),
            "branch_element": BRANCH_ELEMENTS.get(b),
            "start_age": lo,
            "end_age": hi,
            "age_range": f"{lo}-{hi}",
        })

    direction_zh = "顺行" if forward else "逆行"
    start_desc = f"{start_age}岁"
    if extra_months > 0:
        start_desc += f"{extra_months}个月"

    # 文本摘要
    summary_parts = [
        f"出生日期：{birth_date.isoformat()}，性别：{'男' if gender == 'male' else '女'}",
        f"年柱：{year_stem}{year_branch}，月柱：{month_stem}{month_branch}",
        f"大运方向：{direction_zh}，起运年龄：{start_desc}（距节气{delta_days}天）",
        "",
        "大运排列：",
    ]
    for d in dayun_list:
        summary_parts.append(
            f"  第{d['index']}步大运：{d['ganzhi']}（{d['age_range']}岁）"
        )

    return {
        "dayun_schema_version": "1.0",
        "birth_date": birth_date.isoformat(),
        "gender": gender,
        "year_pillar": {"stem": year_stem, "branch": year_branch, "ganzhi": year_stem + year_branch},
        "month_pillar": {"stem": month_stem, "branch": month_branch, "ganzhi": month_stem + month_branch},
        "direction": "forward" if forward else "reverse",
        "direction_zh": direction_zh,
        "start_age": start_age,
        "start_extra_months": extra_months,
        "delta_days_to_jieqi": delta_days,
        "dayun_list": dayun_list,
        "summary_zh": "\n".join(summary_parts),
    }


def parse_date(s: str) -> date:
    parts = s.strip().replace("/", "-").split("-")
    if len(parts) != 3:
        raise ValueError("date must be YYYY-MM-DD")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return date(y, m, d)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate BaZi DaYun (decade fortune) as JSON.")
    parser.add_argument("--date", required=True, help="Birth date YYYY-MM-DD")
    parser.add_argument("--gender", required=True, choices=["male", "female"], help="Gender")
    parser.add_argument("--count", type=int, default=8, help="Number of decade fortune periods (default 8)")
    args = parser.parse_args()

    try:
        birth = parse_date(args.date)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    out = compute_dayun(birth, args.gender, args.count)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

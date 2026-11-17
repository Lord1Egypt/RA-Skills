#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字流年计算。

核心逻辑：
  流年干支 = 目标年份的年柱干支（与四柱年柱同一套算法）。
  流年的分析价值在于其与原局日主的十神关系、与大运的叠加效应、与原局各柱的合冲刑害关系。

  本脚本额外输出流年天干对应的十神（相对于日主），以及流年干支与原局四柱的基础作用关系。

输出 JSON：流年干支 + 十神 + 与原局的作用关系提示。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any, Dict, List, Optional

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

# ─── 十神映射 ──────────────────────────────────────────────────
# 十神由日干与目标干的五行生克 + 阴阳同异决定
SHISHEN_TABLE = {
    ("same", "same_polarity"): "比肩",
    ("same", "diff_polarity"): "劫财",
    ("i_generate", "same_polarity"): "食神",
    ("i_generate", "diff_polarity"): "伤官",
    ("i_am_generated", "same_polarity"): "偏印",
    ("i_am_generated", "diff_polarity"): "正印",
    ("i_克", "same_polarity"): "偏财",
    ("i_克", "diff_polarity"): "正财",
    ("克_me", "same_polarity"): "七杀",
    ("克_me", "diff_polarity"): "正官",
}

WUXING_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
# 生：木→火→土→金→水→木
# 克：木→土→水→火→金→木


def _wuxing_relation(me: str, target: str) -> str:
    """返回我(me)与目标(target)的五行关系。"""
    if me == target:
        return "same"
    mi = WUXING_ORDER.index(me)
    ti = WUXING_ORDER.index(target)
    if (mi + 1) % 5 == ti:
        return "i_generate"
    if (ti + 1) % 5 == mi:
        return "i_am_generated"
    if (mi + 2) % 5 == ti:
        return "i_克"
    return "克_me"


def _polarity(stem: str) -> str:
    return "yang" if HEAVENLY_STEMS.index(stem) % 2 == 0 else "yin"


def compute_shishen(day_stem: str, target_stem: str) -> str:
    """计算目标天干相对于日主的十神。"""
    me_el = STEM_ELEMENTS[day_stem]
    tgt_el = STEM_ELEMENTS[target_stem]
    relation = _wuxing_relation(me_el, tgt_el)
    same_pol = "same_polarity" if _polarity(day_stem) == _polarity(target_stem) else "diff_polarity"
    return SHISHEN_TABLE.get((relation, same_pol), "未知")


# ─── 地支六冲 ─────────────────────────────────────────────────
DIZHI_CHONG = {
    "子": "午", "午": "子", "丑": "未", "未": "丑",
    "寅": "申", "申": "寅", "卯": "酉", "酉": "卯",
    "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳",
}

# ─── 地支六合 ─────────────────────────────────────────────────
DIZHI_HE = {
    "子": "丑", "丑": "子", "寅": "亥", "亥": "寅",
    "卯": "戌", "戌": "卯", "辰": "酉", "酉": "辰",
    "巳": "申", "申": "巳", "午": "未", "未": "午",
}

# ─── 天干五合 ─────────────────────────────────────────────────
TIANGAN_HE = {
    "甲": "己", "己": "甲", "乙": "庚", "庚": "乙",
    "丙": "辛", "辛": "丙", "丁": "壬", "壬": "丁",
    "戊": "癸", "癸": "戊",
}

# ─── 天干相冲 ─────────────────────────────────────────────────
TIANGAN_CHONG = {
    "甲": "庚", "庚": "甲", "乙": "辛", "辛": "乙",
    "丙": "壬", "壬": "丙", "丁": "癸", "癸": "丁",
}


def compute_liunian_year(target_year: int) -> tuple[str, str]:
    """计算流年干支。"""
    stem_idx = (target_year - 4) % 10
    branch_idx = (target_year - 4) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def compute_interactions(
    ln_stem: str, ln_branch: str,
    pillars: Optional[Dict[str, Dict[str, str]]],
) -> List[Dict[str, str]]:
    """计算流年干支与原局四柱的基础作用关系。"""
    if not pillars:
        return []
    interactions: List[Dict[str, str]] = []
    pillar_names = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
    for key, label in pillar_names.items():
        p = pillars.get(key)
        if not p:
            continue
        p_stem = p.get("stem", "")
        p_branch = p.get("branch", "")
        # 天干合
        if TIANGAN_HE.get(ln_stem) == p_stem:
            interactions.append({"type": "天干合", "detail": f"流年{ln_stem}合{label}{p_stem}"})
        # 天干冲
        if TIANGAN_CHONG.get(ln_stem) == p_stem:
            interactions.append({"type": "天干冲", "detail": f"流年{ln_stem}冲{label}{p_stem}"})
        # 地支冲
        if DIZHI_CHONG.get(ln_branch) == p_branch:
            interactions.append({"type": "地支冲", "detail": f"流年{ln_branch}冲{label}{p_branch}"})
        # 地支合
        if DIZHI_HE.get(ln_branch) == p_branch:
            interactions.append({"type": "地支合", "detail": f"流年{ln_branch}合{label}{p_branch}"})
    return interactions


def compute_liunian(
    target_year: int,
    day_stem: Optional[str] = None,
    pillars: Optional[Dict[str, Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """计算流年完整信息。"""
    ln_stem, ln_branch = compute_liunian_year(target_year)

    result: Dict[str, Any] = {
        "liunian_schema_version": "1.0",
        "target_year": target_year,
        "stem": ln_stem,
        "branch": ln_branch,
        "ganzhi": ln_stem + ln_branch,
        "stem_element": STEM_ELEMENTS.get(ln_stem),
        "branch_element": BRANCH_ELEMENTS.get(ln_branch),
    }

    if day_stem:
        shishen = compute_shishen(day_stem, ln_stem)
        result["shishen"] = shishen
        result["shishen_detail"] = f"流年天干{ln_stem}为日主{day_stem}的{shishen}"

    interactions = compute_interactions(ln_stem, ln_branch, pillars)
    if interactions:
        result["interactions"] = interactions

    # 文本摘要
    summary_parts = [f"流年：{target_year}年 {ln_stem}{ln_branch}"]
    if day_stem:
        result_shishen = result.get("shishen", "")
        summary_parts.append(f"流年天干{ln_stem}为日主{day_stem}的{result_shishen}")
    for inter in interactions:
        summary_parts.append(f"  {inter['detail']}")

    result["summary_zh"] = "\n".join(summary_parts)
    return result


def parse_date(s: str) -> date:
    parts = s.strip().replace("/", "-").split("-")
    if len(parts) != 3:
        raise ValueError("date must be YYYY-MM-DD")
    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    return date(y, m, d)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate BaZi LiuNian (annual fortune) as JSON.")
    parser.add_argument("--year", type=int, required=True, help="Target year (solar calendar)")
    parser.add_argument("--day-stem", type=str, default=None, help="Day pillar stem (日主天干) for shishen calculation")
    parser.add_argument("--pillars-json", type=str, default=None,
                        help='Original four pillars as JSON, e.g. \'{"year":{"stem":"甲","branch":"子"},...}\'')
    args = parser.parse_args()

    day_stem = args.day_stem
    pillars = None
    if args.pillars_json:
        try:
            pillars = json.loads(args.pillars_json)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid pillars JSON: {e}"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

    out = compute_liunian(args.year, day_stem, pillars)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

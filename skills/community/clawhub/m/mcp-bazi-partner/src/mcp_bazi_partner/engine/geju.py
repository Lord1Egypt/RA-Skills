"""GeJu (格局) - Pattern determination, rule layer only."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import (
    SHISHEN_TO_PATTERN, JIANLU_TABLE, YANGREN_TABLE, ZAQI_ZHI,
    get_shishen,
)
from .paipan import SiZhu
from .shishen import ShiShenMap


@dataclass
class PatternResult:
    month_zhi: str
    month_benqi: str
    month_benqi_shishen: str
    is_lu_or_ren: bool
    raw_pattern: str | None
    tougan_check: list[dict]
    final_pattern: str
    pattern_category: str


def is_jianlu(day_gan: str, month_zhi: str) -> bool:
    return JIANLU_TABLE.get(day_gan) == month_zhi


def is_yangren(day_gan: str, month_zhi: str) -> bool:
    return YANGREN_TABLE.get(day_gan) == month_zhi


def check_tougan(sizhu: SiZhu, month_hide_gan: list[str]) -> list[dict]:
    """Check if month branch hidden stems are transparent in year/month/time stems."""
    tiangan_in_chart = [
        ("year_gan", sizhu.year.gan),
        ("month_gan", sizhu.month.gan),
        ("time_gan", sizhu.time.gan),
    ]
    result = []
    for hg in month_hide_gan:
        for pos, tg in tiangan_in_chart:
            if tg == hg:
                result.append({
                    "gan": hg,
                    "shishen": get_shishen(sizhu.day_master, hg),
                    "position": pos,
                })
    return result


def find_pattern_for_lu_ren(sizhu: SiZhu, shishen: ShiShenMap) -> str:
    """For JianLu/YangRen months: find pattern from other stems."""
    gan_shishen_list = [
        (shishen.year_gan.shishen, shishen.year_gan.gan),
        (shishen.month_gan.shishen, shishen.month_gan.gan),
        (shishen.time_gan.shishen, shishen.time_gan.gan),
    ]
    priority = ["七杀", "正官", "食神", "伤官", "正财", "偏财", "正印", "偏印"]
    for target_ss in priority:
        for ss, gan in gan_shishen_list:
            if ss == target_ss:
                return SHISHEN_TO_PATTERN.get(ss, f"{ss}格")

    if is_yangren(sizhu.day_master, sizhu.month.zhi):
        return "阳刃格"
    return "建禄格"


def determine_pattern_by_rules(sizhu: SiZhu, shishen: ShiShenMap) -> PatternResult:
    """Determine pattern using rules only (no AI)."""
    month_zhi = sizhu.month.zhi
    month_hide = sizhu.month.hide_gan
    month_benqi = month_hide[0] if month_hide else ""
    month_benqi_ss = shishen.month_zhi_benqi_shishen

    lu = is_jianlu(sizhu.day_master, month_zhi)
    ren = is_yangren(sizhu.day_master, month_zhi)

    if lu or ren:
        pattern = find_pattern_for_lu_ren(sizhu, shishen)
        category = "阳刃格" if ren else "建禄格"
        return PatternResult(
            month_zhi=month_zhi, month_benqi=month_benqi,
            month_benqi_shishen=month_benqi_ss,
            is_lu_or_ren=True, raw_pattern=None,
            tougan_check=[], final_pattern=pattern,
            pattern_category=category,
        )

    if month_zhi in ZAQI_ZHI:
        tougan = check_tougan(sizhu, month_hide)
        if tougan:
            benqi_tougan = [t for t in tougan if t["gan"] == month_benqi]
            if benqi_tougan:
                ss = benqi_tougan[0]["shishen"]
            else:
                ss = tougan[0]["shishen"]
            pattern = SHISHEN_TO_PATTERN.get(ss, f"{ss}格")
        else:
            pattern = SHISHEN_TO_PATTERN.get(month_benqi_ss, f"{month_benqi_ss}格")
        return PatternResult(
            month_zhi=month_zhi, month_benqi=month_benqi,
            month_benqi_shishen=month_benqi_ss,
            is_lu_or_ren=False,
            raw_pattern=SHISHEN_TO_PATTERN.get(month_benqi_ss),
            tougan_check=tougan, final_pattern=pattern,
            pattern_category="正格",
        )

    if month_benqi_ss in ("比肩", "劫财"):
        pattern = find_pattern_for_lu_ren(sizhu, shishen)
        category = "建禄格"
    else:
        pattern = SHISHEN_TO_PATTERN.get(month_benqi_ss, f"{month_benqi_ss}格")
        category = "正格"

    return PatternResult(
        month_zhi=month_zhi, month_benqi=month_benqi,
        month_benqi_shishen=month_benqi_ss,
        is_lu_or_ren=False, raw_pattern=pattern,
        tougan_check=[], final_pattern=pattern,
        pattern_category=category,
    )

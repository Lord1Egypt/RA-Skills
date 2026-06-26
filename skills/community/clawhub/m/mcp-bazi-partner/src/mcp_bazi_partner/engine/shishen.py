"""ShiShen (十神) - Ten Gods calculation, thin wrapper over lunar-python."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .constants import TIANGAN_WUXING, TIANGAN_YINYANG


@dataclass
class GanShiShen:
    gan: str
    shishen: str
    wuxing: str
    yinyang: str


@dataclass
class ZhiShiShen:
    zhi: str
    hide_gan_shishen: list[GanShiShen]


@dataclass
class ShiShenMap:
    year_gan: GanShiShen
    month_gan: GanShiShen
    time_gan: GanShiShen
    year_zhi: ZhiShiShen
    month_zhi: ZhiShiShen
    day_zhi: ZhiShiShen
    time_zhi: ZhiShiShen
    all_shishen: dict[str, int]
    month_zhi_benqi_shishen: str


def _gan_shishen(gan: str, ss: str) -> GanShiShen:
    return GanShiShen(
        gan=gan, shishen=ss,
        wuxing=TIANGAN_WUXING[gan],
        yinyang=TIANGAN_YINYANG[gan],
    )


def _zhi_shishen(zhi: str, hide_gans: list[str], hide_ss: list[str]) -> ZhiShiShen:
    items = [_gan_shishen(g, s) for g, s in zip(hide_gans, hide_ss)]
    return ZhiShiShen(zhi=zhi, hide_gan_shishen=items)


def calculate_shishen(bazi_obj, sizhu) -> ShiShenMap:
    """Extract ShiShen from lunar-python's EightChar object."""
    year_ss = bazi_obj.getYearShiShenGan()
    month_ss = bazi_obj.getMonthShiShenGan()
    time_ss = bazi_obj.getTimeShiShenGan()

    year_gan_ss = _gan_shishen(sizhu.year.gan, year_ss)
    month_gan_ss = _gan_shishen(sizhu.month.gan, month_ss)
    time_gan_ss = _gan_shishen(sizhu.time.gan, time_ss)

    year_zhi_ss_list = list(bazi_obj.getYearShiShenZhi())
    month_zhi_ss_list = list(bazi_obj.getMonthShiShenZhi())
    day_zhi_ss_list = list(bazi_obj.getDayShiShenZhi())
    time_zhi_ss_list = list(bazi_obj.getTimeShiShenZhi())

    year_zhi_ss = _zhi_shishen(sizhu.year.zhi, sizhu.year.hide_gan, year_zhi_ss_list)
    month_zhi_ss = _zhi_shishen(sizhu.month.zhi, sizhu.month.hide_gan, month_zhi_ss_list)
    day_zhi_ss = _zhi_shishen(sizhu.day.zhi, sizhu.day.hide_gan, day_zhi_ss_list)
    time_zhi_ss = _zhi_shishen(sizhu.time.zhi, sizhu.time.hide_gan, time_zhi_ss_list)

    counter: Counter[str] = Counter()
    counter[year_ss] += 1
    counter[month_ss] += 1
    counter[time_ss] += 1
    for ss_list in [year_zhi_ss_list, month_zhi_ss_list, day_zhi_ss_list, time_zhi_ss_list]:
        for ss in ss_list:
            counter[ss] += 1

    month_benqi_ss = month_zhi_ss_list[0] if month_zhi_ss_list else "未知"

    return ShiShenMap(
        year_gan=year_gan_ss,
        month_gan=month_gan_ss,
        time_gan=time_gan_ss,
        year_zhi=year_zhi_ss,
        month_zhi=month_zhi_ss,
        day_zhi=day_zhi_ss,
        time_zhi=time_zhi_ss,
        all_shishen=dict(counter),
        month_zhi_benqi_shishen=month_benqi_ss,
    )

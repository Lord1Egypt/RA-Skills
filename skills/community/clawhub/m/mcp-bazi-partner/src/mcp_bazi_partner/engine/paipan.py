"""PaiPan (排盘) - Four Pillars calculation using lunar-python."""

from __future__ import annotations

from dataclasses import dataclass, field
from lunar_python import Solar

from .constants import TIANGAN_WUXING, TIANGAN_YINYANG, HOUR_TO_SHICHEN_MID


@dataclass
class Pillar:
    ganzhi: str
    gan: str
    zhi: str
    hide_gan: list[str]
    nayin: str


@dataclass
class SiZhu:
    year: Pillar
    month: Pillar
    day: Pillar
    time: Pillar
    day_master: str
    day_master_yinyang: str
    day_master_wuxing: str


def _make_pillar(gz: str, gan: str, zhi: str, hide_gan: list[str], nayin: str) -> Pillar:
    return Pillar(ganzhi=gz, gan=gan, zhi=zhi, hide_gan=hide_gan, nayin=nayin)


def calculate_sizhu(year: int, month: int, day: int, hour: int) -> tuple[SiZhu, object]:
    """Calculate the Four Pillars from a solar date."""
    h, m = HOUR_TO_SHICHEN_MID[hour]
    solar = Solar.fromYmdHms(year, month, day, h, m, 0)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    bazi.setSect(1)

    def _pillar(pos: str) -> Pillar:
        gz = getattr(bazi, f"get{pos}")()
        gan = getattr(bazi, f"get{pos}Gan")()
        zhi = getattr(bazi, f"get{pos}Zhi")()
        hide_gan = list(getattr(bazi, f"get{pos}HideGan")())
        nayin = getattr(bazi, f"get{pos}NaYin")()
        return _make_pillar(gz, gan, zhi, hide_gan, nayin)

    year_p = _pillar("Year")
    month_p = _pillar("Month")
    day_p = _pillar("Day")
    time_p = _pillar("Time")

    day_gan = day_p.gan
    sizhu = SiZhu(
        year=year_p, month=month_p, day=day_p, time=time_p,
        day_master=day_gan,
        day_master_yinyang=TIANGAN_YINYANG[day_gan],
        day_master_wuxing=TIANGAN_WUXING[day_gan],
    )
    return sizhu, bazi

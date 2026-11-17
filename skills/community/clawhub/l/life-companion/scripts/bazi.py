#!/usr/bin/env python3
"""
bazi.py — deterministic 八字/四柱 (BaZi / Four Pillars) computation.

This script computes ONLY the reproducible, rule-based layer of a BaZi chart:
four pillars, day master, five-element tally, ten gods (incl. hidden stems),
na-yin, luck pillars (大运) and the current annual pillar (流年). It also emits a
transparent, clearly-LABELED day-master strength heuristic — that number is a
convention, not a fact, and the JSON marks it as such.

It does NOT interpret. Meaning ("你适合…", "今年运势…") is authored elsewhere by
the model, grounded on curated reference notes and always labeled as reflective.

Engine: lunar-python (6tail, MIT) — computes 干支 on the correct astronomical
solar-term (节气) boundaries: the year pillar rolls at 立春, the month pillar at
the 12 节. sxtwl (BSD) is used as an independent cross-check of the year boundary
when available. Both run fully offline; birth data never leaves the machine.

Usage:
  python3 bazi.py --date 1993-04-12 --time 07:35 --gender m --place "Beijing, CN"
  python3 bazi.py --date 1993-04-12 --gender f            # time unknown
  python3 bazi.py --date 1993-04-12 --time 07:35 --gender m \
                  --lon 116.407 --true-solar-time         # TST toggle (off by default)
  python3 bazi.py ... --format text                       # human-readable table
"""
import argparse
import datetime
import json
import math
import sys


# ---------------------------------------------------------------------------
# Dependency bootstrap — the skill should "just work" on a fresh machine.
# lunar-python is MIT, sxtwl is BSD; both are pure-offline at compute time.
# ---------------------------------------------------------------------------
import os
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deps import ensure as _ensure  # noqa: E402

_ensure("lunar-python", "lunar_python")
from lunar_python import Solar  # noqa: E402
from _branches import relations_between  # noqa: E402
from _tz import argv_with_offsets, parse_tz  # noqa: E402  (synastry.py reads bazi.parse_tz)


# ---------------------------------------------------------------------------
# Disclosed element / polarity maps (standard 命理 tables — deterministic).
# ---------------------------------------------------------------------------
GAN_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}
GAN_YINYANG = {  # 阳=+, 阴=-
    "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
    "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴",
}
ZHI_MAIN_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
# 五行生克 for the strength heuristic.
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}  # 生
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}   # 克
ELEMENTS = ["木", "火", "土", "金", "水"]

ZHI_MAIN_GAN = {  # 本气 (main-qi) stem of each branch — for the branch's 十神/favor
    "子": "癸", "丑": "己", "寅": "甲", "卯": "乙", "辰": "戊", "巳": "丙",
    "午": "丁", "未": "己", "申": "庚", "酉": "辛", "戌": "戊", "亥": "壬",
}
# 十神 → life-domain category (for a reading; not used by the favor heuristic).
TEN_GOD_CATEGORY = {
    "比肩": "比劫", "劫财": "比劫", "食神": "食伤", "伤官": "食伤",
    "正财": "财", "偏财": "财", "正官": "官杀", "七杀": "官杀",
    "正印": "印", "偏印": "印",
}


def _ten_god(day_gan, other_gan):
    """十神 of `other_gan` relative to the day master `day_gan` — pure element+polarity
    derivation (同/生/克 × 同性/异性). Covers 大运/流年 stems the per-pillar library
    methods can't. Deterministic; standard 子平 table."""
    dm_el, dm_yy = GAN_ELEMENT[day_gan], GAN_YINYANG[day_gan]
    o_el, o_yy = GAN_ELEMENT[other_gan], GAN_YINYANG[other_gan]
    same = (dm_yy == o_yy)
    if o_el == dm_el:                # 同我 (peers)
        return "比肩" if same else "劫财"
    if GENERATES[dm_el] == o_el:     # 我生 (output)
        return "食神" if same else "伤官"
    if CONTROLS[dm_el] == o_el:      # 我克 (wealth)
        return "偏财" if same else "正财"
    if CONTROLS[o_el] == dm_el:      # 克我 (officer)
        return "七杀" if same else "正官"
    if GENERATES[o_el] == dm_el:     # 生我 (resource)
        return "偏印" if same else "正印"
    return None


def _favor_sets(day_gan, strength_label):
    """Which ELEMENTS the disclosed 扶抑 heuristic reads as 喜/忌, given the day-master
    strength LABEL. 扶(support)=比劫(same element as DM)+印(element that generates DM);
    抑(drain)=食伤+财+官杀. 偏弱→喜扶忌抑; 偏强→喜抑忌扶; 中和→无硬喜忌(全平).
    HEURISTIC, not 用神 (real 用神 also needs 调候/病药/通关/格局)."""
    dm_el = GAN_ELEMENT[day_gan]
    yin_el = next(k for k, v in GENERATES.items() if v == dm_el)  # 生我者 (印)
    support = {dm_el, yin_el}
    drain = set(ELEMENTS) - support
    if "偏弱" in strength_label:
        return {"favorable": sorted(support), "unfavorable": sorted(drain), "mode": "weak→喜扶(比劫+印)"}
    if "偏强" in strength_label:
        return {"favorable": sorted(drain), "unfavorable": sorted(support), "mode": "strong→喜抑(食伤+财+官杀)"}
    return {"favorable": [], "unfavorable": [], "mode": "near-balanced→无硬喜忌(全平)"}


def _favor_tag(element, favor_sets):
    """喜 / 忌 / 平 for one element under the current strength read."""
    if element in favor_sets["favorable"]:
        return "喜"
    if element in favor_sets["unfavorable"]:
        return "忌"
    return "平"


# 生肖 (year-branch animal) + traditional branch relations, for a 生肖 daily read.
ZHI_ANIMAL = {"子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔", "辰": "龙", "巳": "蛇",
              "午": "马", "未": "羊", "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"}
# What each relation reads as for the day, on the person's 生肖. The relations themselves
# come from _branches.py, the table 合婚 and natal_relations read.
_ZODIAC_READING = {
    "六合": "顺、易得助力/合作",
    "半合": "气场相合、做事顺手",
    "三会": "同一季的地支相会，气场同类、做事顺手",
    "六冲": "变动、冲动、易有摩擦——悠着点、别拍板大事",
    "六害": "小别扭、易被小事绊——留意人际口舌",
    "六破": "节奏易被打断、计划易变卦——留点余地",
    "相刑": "内耗/急躁/是非——稳住节奏",
    "自刑": "与你生肖同支，自我感强——别跟自己较劲",
}
_ZODIAC_GOOD = {"六合", "半合", "三会"}                      # the 合 group
_ZODIAC_BAD = {"六冲", "六害", "六破", "相刑", "自刑"}          # 刑冲破害


def _zodiac_day(year_zhi, day_zhi):
    """今日生肖运: the person's 生肖 (year branch) against today's 流日 branch, by the shared
    relation table in _branches.py. It used to read a private copy that knew no 三会 or
    六破 and called every repeated branch 自刑, so the card and its own natal_relations
    year row could disagree on the same day."""
    rels = [dict(r, reading=_ZODIAC_READING[r["relation"]])
            for r in relations_between(day_zhi, year_zhi)]
    names = {r["relation"] for r in rels}
    good, bad = names & _ZODIAC_GOOD, names & _ZODIAC_BAD
    tone = ("顺" if good and not bad else "偏磕碰,悠着点" if bad and not good
            else "有助力也有磕碰,混着来" if good and bad else "平平,按自己节奏")
    return {"animal": ZHI_ANIMAL[year_zhi], "day_branch": day_zhi,
            "relations": rels, "tone": tone, "uncertain": False}


_WX_COLOR = {"木": "青/绿", "火": "红/橙紫", "土": "黄/棕", "金": "白/金银", "水": "蓝/黑"}
_WX_DIR = {"木": "东", "火": "南", "土": "西南/中", "金": "西", "水": "北"}
_WX_NUM = {"木": [3, 8], "火": [2, 7], "土": [5, 10], "金": [4, 9], "水": [1, 6]}


def _wuxing_tips(favor_sets):
    """幸运色/方位/数, derived from the person's 喜用五行 by TRADITIONAL 五行 (河图)
    correspondence — a labeled cultural 彩头, not a fabricated 'lucky number'."""
    fav = favor_sets.get("favorable") or []
    if not fav:
        return {"colors": [], "directions": [], "numbers": [],
                "note": "你八字偏中和、五行无强喜忌,以下从略——不硬凑幸运色数。"}
    return {"colors": [_WX_COLOR[e] for e in fav],
            "directions": [_WX_DIR[e] for e in fav],
            "numbers": sorted({n for e in fav for n in _WX_NUM[e]}),
            "note": "按你喜用五行(" + "、".join(fav) + ")的传统对应,图个彩头,不是保证。"}

# Standard-meridian longitude by IANA-ish offset, for True Solar Time correction.
# (Only the longitude term is applied here; equation-of-time added separately.)


# ---------------------------------------------------------------------------
def _equation_of_time_minutes(dt):
    """Approximate equation of time (minutes) for a date — small TST refinement."""
    n = dt.timetuple().tm_yday
    b = 2 * math.pi * (n - 81) / 364.0
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


CST = "Asia/Shanghai"


def _offset_hours(tz, dt):
    """UTC offset in force at `dt` for an IANA name, or the number itself."""
    if isinstance(tz, (int, float)):
        return float(tz)
    from zoneinfo import ZoneInfo
    import datetime as _dt
    return _dt.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                        tzinfo=ZoneInfo(tz)).utcoffset().total_seconds() / 3600.0


def _to_china_clock(dt, tz):
    """The same instant, expressed on a Beijing wall clock.

    lunar-python takes a NAIVE datetime and resolves 節氣 against China Standard Time.
    節氣 are absolute astronomical instants, so a birth outside China must be moved
    into that frame before the 年柱/月柱 can be right. Without this the engine silently
    reads an Amsterdam clock as a Beijing one and can hand back the wrong year pillar
    — while confidently describing the wrong side of the boundary.
    """
    if tz is None:
        return dt, 0.0
    off = _offset_hours(tz, dt)
    shift = 8.0 - off
    return dt + datetime.timedelta(hours=shift), shift


def _on_birth_clock(moment, tz):
    """A Beijing-clock moment — the way the 節氣 table keeps them — on the birthplace's own
    wall clock."""
    if tz is None:
        return moment
    utc = moment - datetime.timedelta(hours=8)
    if isinstance(tz, (int, float)):
        return utc + datetime.timedelta(hours=float(tz))
    from zoneinfo import ZoneInfo
    return utc.replace(tzinfo=datetime.timezone.utc).astimezone(ZoneInfo(tz)).replace(tzinfo=None)


def _when(moment, tz):
    """A 節氣 moment as a note prints it: on the birthplace's clock, saying whose clock. An
    Amsterdam birth used to read 立春 03:37 for a moment that was 20:37 the evening before
    on its own clock."""
    local = _on_birth_clock(moment, tz)
    if local == moment:
        return f"北京时间 {moment:%Y-%m-%d %H:%M}"
    return f"当地时间 {local:%Y-%m-%d %H:%M}，北京时间 {moment:%Y-%m-%d %H:%M}"


def _apply_true_solar_time(dt, lon, standard_meridian):
    """Shift civil clock time to local True Solar Time (traditional convention)."""
    lon_correction_min = (lon - standard_meridian) * 4.0  # 4 min per degree
    eot_min = _equation_of_time_minutes(dt)
    return dt + datetime.timedelta(minutes=lon_correction_min + eot_min)


def _element_tally(ec, hour_known):
    """
    Transparent five-element counts. Two disclosed schemes are returned so the
    reader can see the weighting, not just a black-box number:
      • main_only : the 8 characters by their primary element (4 stems + 4 branch
                    main-qi). The classic 'is the chart balanced' view.
      • with_hidden: adds every 藏干 (hidden stem) at weight 1. Fuller, but the
                    branch weighting scheme is itself a convention.
    """
    main = {e: 0 for e in ELEMENTS}
    hidden = {e: 0 for e in ELEMENTS}

    gans = [ec.getYearGan(), ec.getMonthGan(), ec.getDayGan()]
    zhis = [ec.getYearZhi(), ec.getMonthZhi(), ec.getDayZhi()]
    hide_lists = [ec.getYearHideGan(), ec.getMonthHideGan(), ec.getDayHideGan()]
    if hour_known:
        gans.append(ec.getTimeGan())
        zhis.append(ec.getTimeZhi())
        hide_lists.append(ec.getTimeHideGan())

    for g in gans:
        main[GAN_ELEMENT[g]] += 1
    for z in zhis:
        main[ZHI_MAIN_ELEMENT[z]] += 1
    for hl in hide_lists:
        for hg in hl:
            hidden[GAN_ELEMENT[hg]] += 1

    with_hidden = {e: main[e] + hidden[e] for e in ELEMENTS}
    return {"main_only": main, "with_hidden": with_hidden}


def _strength_heuristic(day_gan, tally):
    """
    A CLEARLY-LABELED 扶抑 (support/drain) heuristic for 身强/身弱. This is one
    school's rule of thumb, not an objective fact — the caller must present it as
    interpretation. Supporting = same element (比劫) + the element that generates
    the day master (印). Draining = output (食伤) + wealth (财) + officer (官杀).
    """
    dm_el = GAN_ELEMENT[day_gan]
    supports_el = next(k for k, v in GENERATES.items() if v == dm_el)  # 生我者 (印)
    counts = tally["with_hidden"]
    supportive = counts[dm_el] + counts[supports_el]
    total = sum(counts.values())
    draining = total - supportive
    ratio = supportive / total if total else 0.0
    if ratio >= 0.55:
        label = "偏强 (leaning strong)"
    elif ratio <= 0.35:
        label = "偏弱 (leaning weak)"
    else:
        label = "中和/接近平衡 (near balanced)"
    return {
        "day_master_element": dm_el,
        "supportive_units": round(supportive, 1),
        "draining_units": round(draining, 1),
        "supportive_ratio": round(ratio, 3),
        "label": label,
        "school": "扶抑 (fú-yì / support-vs-drain)",
        "_note": "HEURISTIC, not a system fact. 用神/喜忌 depend on season, "
                 "combinations and school; present as one reading, not the truth.",
    }


def _pillar(ec, which):
    g = getattr(ec, f"get{which}Gan")()
    z = getattr(ec, f"get{which}Zhi")()
    return {
        "gan": g,
        "zhi": z,
        "ganzhi": g + z,
        "gan_element": GAN_ELEMENT[g],
        "gan_yinyang": GAN_YINYANG[g],
        "zhi_main_element": ZHI_MAIN_ELEMENT[z],
        "hidden_gan": list(getattr(ec, f"get{which}HideGan")()),
        "nayin": getattr(ec, f"get{which}NaYin")(),
        "xunkong": getattr(ec, f"get{which}XunKong")(),
        "ten_god_gan": (None if which == "Day"
                        else getattr(ec, f"get{which}ShiShenGan")()),
        "ten_god_hidden": list(getattr(ec, f"get{which}ShiShenZhi")()),
    }


def _luck_pillars(ec, gender_code, day_gan, favor_sets, current_age):
    """
    大运 sequence + 起运, each decade tagged with: the 十神 of its stem vs the day
    master (`ten_god`) + a 喜/忌/平 tag from the 扶抑 heuristic (`favor`); the branch
    本气's secondary 十神/favor (`zhi_ten_god`/`zhi_favor`); and whether it is the
    CURRENT decade. These are the hooks the stage-by-stage reading consumes.
    """
    try:
        yun = ec.getYun(gender_code)
    except Exception as e:  # pragma: no cover
        return {"error": f"getYun failed: {e}"}
    out = {
        "qiyun_after": {
            "years": yun.getStartYear(),
            "months": yun.getStartMonth(),
            "days": yun.getStartDay(),
        },
        "direction": "顺行 (forward)" if gender_code == _forward_gender(ec) else "逆行 (backward)",
        "pillars": [],
    }
    for dy in yun.getDaYun():
        gz = dy.getGanZhi()
        if not gz:  # index 0 is the pre-起运 stub
            continue
        stem, branch = gz[0], gz[1]
        zhi_gan = ZHI_MAIN_GAN[branch]
        start_age, end_age = dy.getStartAge(), dy.getEndAge()
        out["pillars"].append({
            "start_age": start_age,
            "end_age": end_age,
            "start_year": dy.getStartYear(),
            "ganzhi": gz,
            "gan_element": GAN_ELEMENT.get(stem),
            "zhi_main_element": ZHI_MAIN_ELEMENT.get(branch),
            "ten_god": _ten_god(day_gan, stem),                     # 大运干十神 (primary)
            "ten_god_category": TEN_GOD_CATEGORY.get(_ten_god(day_gan, stem)),
            "favor": _favor_tag(GAN_ELEMENT[stem], favor_sets),     # 喜/忌/平 (stem)
            "zhi_ten_god": _ten_god(day_gan, zhi_gan),              # 大运支本气十神 (secondary)
            "zhi_favor": _favor_tag(ZHI_MAIN_ELEMENT[branch], favor_sets),
            "is_current": (current_age is not None
                           and start_age <= current_age <= end_age),
        })
    return out


def _upcoming_annual_pillars(day_gan, favor_sets, birth_year, years=10):
    """
    The next `years` annual pillars (流年) from the current civil year: each with its
    立春-based 干支, the stem's 十神 vs the day master, and a 喜/忌/平 tag (same 扶抑
    heuristic). Sampled mid-year (safely past 立春). Interaction with the natal chart
    is interpretive; entry [0] is the current year.
    """
    today = datetime.date.today()
    out = []
    for yr in range(today.year, today.year + years):
        gz = Solar.fromYmdHms(yr, 6, 1, 12, 0, 0).getLunar().getYearInGanZhiExact()
        stem = gz[0]
        out.append({
            "civil_year": yr,
            "age": (yr - birth_year) if birth_year else None,
            "ganzhi": gz,
            "ten_god": _ten_god(day_gan, stem),
            "favor": _favor_tag(GAN_ELEMENT[stem], favor_sets),
            "is_current": (yr == today.year),
        })
    return out


def _forward_gender(ec):
    """阳男阴女 顺行 → returns the gender_code (1 male / 0 female) that goes forward."""
    year_gan = ec.getYearGan()
    return 1 if GAN_YINYANG[year_gan] == "阳" else 0


def _daily_pillars(day_gan, favor_sets, on_date, year_zhi, natal=None):
    """
    流年 / 流月 / 流日 for a target date, each with the pillar-stem's 十神 vs the day
    master and a 喜/忌/平 tag (同扶抑 heuristic); PLUS today's 生肖运 (year branch vs
    流日 branch) and 五行 tips (幸运色/方位/数 from 喜用). The real hooks for a *daily*
    reading. 节气-based boundaries. Interaction with the natal chart is interpretive.
    """
    lunar = Solar.fromYmdHms(on_date.year, on_date.month, on_date.day, 12, 0, 0).getLunar()
    out = {"date": on_date.isoformat()}
    for key, gz in (("liunian", lunar.getYearInGanZhiExact()),    # 流年 (year)
                    ("liuyue", lunar.getMonthInGanZhiExact()),    # 流月 (month)
                    ("liuri", lunar.getDayInGanZhiExact())):      # 流日 (day)
        stem = gz[0]
        out[key] = {
            "ganzhi": gz,
            "ten_god": _ten_god(day_gan, stem),
            "ten_god_category": TEN_GOD_CATEGORY.get(_ten_god(day_gan, stem)),
            "favor": _favor_tag(GAN_ELEMENT[stem], favor_sets),
        }
    out["zodiac_day"] = _zodiac_day(year_zhi, out["liuri"]["ganzhi"][1])
    out["wuxing_tips"] = _wuxing_tips(favor_sets)
    # The day's branch against each of the person's own pillars, by the same tables 合婚
    # reads between two charts. For a near-balanced chart every 喜/忌 above is 平 and the
    # 五行 tips are empty, so this is the one day-specific signal it has.
    if natal:
        day_gz = out["liuri"]["ganzhi"]
        rows = [
            {"pillar": key, "natal": natal[key]["ganzhi"],
             "relations": relations_between(day_gz[1], natal[key]["zhi"]),
             "same_pillar": day_gz == natal[key]["ganzhi"],
             "uncertain": False}      # compute() sets it when --time-window moves this pillar
            for key in ("year", "month", "day", "hour") if natal.get(key)]
        # Some relation lands somewhere in the four pillars on 29.5 days of 30 (measured
        # over 186 near-balanced charts), so a card that reports them all says nothing.
        # 冲, 合 and 伏吟 on the 日支 and 月支 land on about 10 days a month.
        for r in rows:
            r["notable"] = r["pillar"] in ("day", "month") and (
                r["same_pillar"] or any(x["relation"] in ("六冲", "六合") for x in r["relations"]))
        out["natal_relations"] = rows
    return out


def _current_liunian(birth_solar):
    """The annual pillar (流年) for the current civil year — deterministic 干支."""
    # Use Jan-of-this-year is wrong (rolls at 立春); ask lunar-python for 'today'.
    now = datetime.date.today()
    s = Solar.fromYmdHms(now.year, now.month, now.day, 12, 0, 0)
    l = s.getLunar()
    return {
        "civil_year": now.year,
        "ganzhi": l.getYearInGanZhiExact(),  # exact = 立春-based
        "_note": "Annual pillar for the current date (立春-based). Interaction with "
                 "the natal chart is interpretive.",
    }


def _cross_check(y, m, d, engine_year_ganzhi, on_lichun_day, ambiguities):
    """Run the sxtwl cross-check, DECIDE whether it agrees, and make a genuine
    disagreement audible in `ambiguities` — the model must not have to notice a
    mismatch by eyeballing two separate JSON fields."""
    res = _sxtwl_year_boundary_check(y, m, d, on_lichun_day=on_lichun_day)
    other = res.get("year_ganzhi")
    if not other:
        res["agrees"] = None
        return res
    res["engine_year_ganzhi"] = engine_year_ganzhi
    res["agrees"] = (other == engine_year_ganzhi)
    if res["agrees"]:
        return res
    if on_lichun_day:
        # Expected: sxtwl has no birth time, so on the boundary day it cannot agree.
        # The 立春-proximity ambiguity is already recorded; don't double-warn, and
        # don't let this masquerade as evidence against the chart.
        res["_disagreement"] = ("expected — date-granularity check on the 立春 day; "
                                "the main engine uses the exact 立春 moment and stands.")
    else:
        res["_disagreement"] = "UNEXPECTED — not a 立春-day granularity artifact."
        ambiguities.append(
            f"年柱交叉核验不一致：本引擎算得 {engine_year_ganzhi}，独立核验(sxtwl)算得 "
            f"{other}，且出生日不在立春当天——请把这张盘当作不确定，如实告诉本人，"
            "不要择一而不说。"
        )
    return res


def _lichun_gap_hours(dt):
    """Hours from `dt` to the nearest 立春 (negative = born before it).

    立春 is the year-pillar boundary and it is a MOMENT, not a date — a birth a few
    hours either side of it belongs to a different 年柱. Returns (gap_hours, moment)
    or (None, None) if the table can't be read.
    """
    try:
        table = Solar.fromYmdHms(dt.year, dt.month, dt.day, 12, 0, 0).getLunar().getJieQiTable()
    except Exception:  # pragma: no cover
        return None, None
    best = None
    for name, solar in (table or {}).items():
        if "立春" not in str(name) and str(name).upper() != "LI_CHUN":
            continue
        try:
            moment = datetime.datetime(solar.getYear(), solar.getMonth(), solar.getDay(),
                                       solar.getHour(), solar.getMinute(), solar.getSecond())
        except Exception:  # pragma: no cover
            continue
        gap = (dt - moment).total_seconds() / 3600.0
        if best is None or abs(gap) < abs(best[0]):
            best = (gap, moment)
    return best if best else (None, None)


def _sxtwl_year_boundary_check(y, m, d, on_lichun_day=False):
    """Independent cross-check of the year pillar (立春 boundary).

    IMPORTANT GRANULARITY CAVEAT: `sxtwl.fromSolar` takes a DATE, not a time, so on
    the 立春 day itself — the one day this check exists for — it cannot know which
    side of the boundary a given birth *time* falls on. A disagreement there is
    therefore expected and is NOT evidence the main engine is wrong; the payload says
    so explicitly rather than leaving the model to infer it from two bare fields.
    """
    try:
        import sxtwl
    except ImportError:
        return {"available": False,
                "_note": "sxtwl not installed — the year pillar has no independent "
                         "cross-check this run. Say so if the birth is near 立春."}
    try:
        day = sxtwl.fromSolar(y, m, d)
        gz = day.getYearGZ()  # uses 立春 boundary, at DATE granularity
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        out = {"available": True, "year_ganzhi": Gan[gz.tg] + Zhi[gz.dz],
               "granularity": "date-only (no birth time)"}
        if on_lichun_day:
            out["_note"] = ("Birth falls on the 立春 DAY, where this date-granularity "
                            "check cannot resolve the boundary. If it disagrees with the "
                            "main engine, the main engine (which uses the exact 立春 "
                            "moment) is the one to trust — do NOT call the chart "
                            "unreliable on the strength of this field alone.")
        return out
    except Exception as e:  # pragma: no cover
        return {"available": True, "error": str(e)}


# ---------------------------------------------------------------------------
# One chart, two clocks.
#
# A birth is read on two clocks, and mixing them up is how this engine has gone wrong
# more than once:
#   * the INSTANT: the civil birth clock moved onto Beijing time. 節氣 are absolute
#     astronomical moments, so 年柱/月柱, the 立春 check, 大运 direction and 起运 are all
#     decided on it. True Solar Time must never touch it: TST reinterprets a clock, it
#     does not move the moment of birth.
#   * the LOCAL clock: the civil clock, or its True Solar Time. 日柱/時柱 hang off the
#     local day and the local 時辰.
# lunar-python builds a chart from ONE datetime, so two clocks mean two EightChar objects.
# The first timezone fix swapped only the two displayed pillars; the 五行 tally, 十神, 大运,
# 生肖 and 命宫 kept reading the local-clock chart, so an Amsterdam birth was shown one
# year pillar and read against another. TST had the opposite bug: it shifted the instant,
# so switching it on could move 立春. Everything derived now goes through one _FramedChart.
_SHISHEN_METHODS = {f"get{w}ShiShen{p}": (w, p)
                    for w in ("Year", "Month", "Day", "Time") for p in ("Gan", "Zhi")}


class _FramedChart:
    """年/月 from the 節氣 frame, 日/時 from the local clock, and 十神 always counted from
    the day master actually shown. The library's own 十神 methods use the day stem of
    whichever clock their pillar was read on, which for an evening birth west of Beijing
    is the NEXT day's."""

    def __init__(self, jieqi_chart, local_chart):
        self._jq = jieqi_chart
        self._local = local_chart

    def __getattr__(self, name):
        if name in _SHISHEN_METHODS:
            which, part = _SHISHEN_METHODS[name]
            src = self._jq if which in ("Year", "Month") else self._local
            day_gan = self._local.getDayGan()
            if part == "Gan":
                return lambda: _ten_god(day_gan, getattr(src, f"get{which}Gan")())
            return lambda: [_ten_god(day_gan, h) for h in getattr(src, f"get{which}HideGan")()]
        src = self._jq if name.startswith(("getYear", "getMonth")) else self._local
        return getattr(src, name)


def _extras(chart, hour_known):
    """命宫 / 身宫 / 胎元 by lunar-python's own formulas, fed the pillars actually shown.

    The library derives them from one clock's month and hour, so a chart read on two
    clocks got them from the wrong month. And with no birth hour the engine read its
    12:00 placeholder and printed a real-looking 命宫, the fabrication 紫微 was already
    fixed for: 命宫 and 身宫 hang off the hour, so without one they are None. The
    formulas are pinned against the library on one-clock charts in tests/test_scripts.py."""
    from lunar_python import EightChar
    from lunar_python.util import LunarUtil
    year_gan = LunarUtil.GAN.index(chart.getYearGan()) - 1            # 0-based, 甲 = 0
    month_gan = LunarUtil.GAN.index(chart.getMonthGan()) - 1
    month_zhi = chart.getMonthZhi()
    taiyuan = (LunarUtil.GAN[(month_gan + 1) % 10 + 1]                 # getTaiYuan
               + LunarUtil.ZHI[(LunarUtil.ZHI.index(month_zhi) - 1 + 3) % 12 + 1])
    if not hour_known:
        return {"mingong": None, "shengong": None, "taiyuan": taiyuan}
    time_zhi = chart.getTimeZhi()

    def stem(offset):
        gi = (year_gan + 1) * 2 + offset
        while gi > 10:
            gi -= 10
        return LunarUtil.GAN[gi]

    m_i = EightChar.MONTH_ZHI.index(month_zhi)                         # 寅 = 1 … 丑 = 12
    off = m_i + EightChar.MONTH_ZHI.index(time_zhi)                    # getMingGong
    off = 26 - off if off >= 14 else 14 - off
    mingong = stem(off) + EightChar.MONTH_ZHI[off]
    off = m_i + LunarUtil.ZHI.index(time_zhi)                          # getShenGong
    if off > 12:
        off -= 12
    shengong = stem(off) + EightChar.MONTH_ZHI[off]
    return {"mingong": mingong, "shengong": shengong, "taiyuan": taiyuan}


# A recorded birth time is rarely right to the minute, so a chart sitting on a boundary
# has to say so. The engine used to do that for 子时 and 立春 only.
SHICHEN_MARGIN_MIN = 15      # a 時辰 changes on every odd hour
JIE_MARGIN_HOURS = 24        # each 節 moves the 月柱 (立春 moves the 年柱 too, checked apart)
MAX_TIME_WINDOW_MIN = 240
_JIE = ("立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "小寒")
# lunar-python keys the table's edge entries (the neighbouring years) in pinyin
_JIE_PINYIN = {"LI_CHUN": "立春", "JING_ZHE": "惊蛰", "QING_MING": "清明", "LI_XIA": "立夏",
               "MANG_ZHONG": "芒种", "XIAO_SHU": "小暑", "LI_QIU": "立秋", "BAI_LU": "白露",
               "HAN_LU": "寒露", "LI_DONG": "立冬", "DA_XUE": "大雪", "XIAO_HAN": "小寒"}


def _nearest_jie(dt):
    """(name, hours from `dt` to it — negative means born before it, moment) for the
    nearest 節 other than 立春, which has its own check; (None, None, None) if the table
    can't be read."""
    try:
        table = Solar.fromYmdHms(dt.year, dt.month, dt.day, 12, 0, 0).getLunar().getJieQiTable()
    except Exception:  # pragma: no cover
        return None, None, None
    best = (None, None, None)
    for key, solar in (table or {}).items():
        name = _JIE_PINYIN.get(str(key), str(key))
        if name not in _JIE or name == "立春":
            continue
        moment = datetime.datetime(solar.getYear(), solar.getMonth(), solar.getDay(),
                                   solar.getHour(), solar.getMinute(), solar.getSecond())
        gap = (dt - moment).total_seconds() / 3600.0
        if best[1] is None or abs(gap) < abs(best[1]):
            best = (name, gap, moment)
    return best


def _pillar_at(dt, late_zishi, which):
    ec = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0).getLunar().getEightChar()
    ec.setSect(2 if late_zishi else 1)
    return getattr(ec, f"get{which}")()


def _moved_pillars(chart_clock, other_clock, late_zishi):
    """The 日柱 and 时柱 that differ between the clock the chart uses and another reading of
    the same birth, as [(name, on the chart's clock, on the other)]. Compared as pillars,
    never as calendar dates: under 早子时 the 日柱 turns at 23:00, so a date that changes
    can leave it alone and a date that stays can move it."""
    moved = []
    for name, which in (("日柱", "Day"), ("时柱", "Time")):
        mine = _pillar_at(chart_clock, late_zishi, which)
        other = _pillar_at(other_clock, late_zishi, which)
        if mine != other:
            moved.append((name, mine, other))
    return moved


def _say_moved(moved):
    """('日柱会是壬戌（日主变成壬）、时柱会是辛亥', '日柱癸亥、时柱壬子') for a note."""
    would = "、".join(f"{name}会是{other}" + (f"（日主变成{other[0]}）" if name == "日柱" else "")
                     for name, _, other in moved)
    used = "、".join(f"{name}{mine}" for name, mine, _ in moved)
    return would, used


def _clock_text(dt, reference):
    """HH:MM, with the date in front when it isn't `reference`'s date."""
    return dt.strftime("%H:%M" if dt.date() == reference.date() else "%Y-%m-%d %H:%M")


def compute(date, time, gender, lon=None, true_solar_time=False,
            standard_meridian=None, late_zishi=True, on_date=None, tz=None,
            time_window=None):
    y, m, d = [int(x) for x in date.split("-")]
    hour_known = time is not None
    hh, mm = (int(x) for x in time.split(":")) if hour_known else (12, 0)
    given_meridian = standard_meridian
    if tz is not None:
        tz = parse_tz(tz)       # the CLI parsed it already; any other caller has not
    if time_window is not None and not 1 <= int(time_window) <= MAX_TIME_WINDOW_MIN:
        raise ValueError(f"--time-window must be 1–{MAX_TIME_WINDOW_MIN} minutes")

    ambiguities = []
    civil = datetime.datetime(y, m, d, hh, mm)

    # The standard meridian belongs to the BIRTHPLACE's zone, not to China. It used to
    # default to 120°E for everyone, so an unmodified TST run silently corrected a
    # European birth against Beijing's meridian — hours of error.
    if standard_meridian is None:
        standard_meridian = (_offset_hours(tz, civil) * 15.0) if tz is not None else 120.0

    # The LOCAL clock (日柱/時柱). True Solar Time only ever changes this one.
    local = civil
    tst_applied = bool(true_solar_time and lon is not None and hour_known)
    if tst_applied:
        local = _apply_true_solar_time(civil, lon, standard_meridian)
        ambiguities.append(
            f"真太阳时已启用：时柱按修正后的钟点 {local.strftime('%H:%M')} 取（经度+均时差）；"
            "年柱、月柱和起运按出生的实际时刻对节气，真太阳时不改变它们。")
        # Compared as pillars: under 早子时 the 日柱 turns at 23:00, so a date that changes
        # can leave it alone and a date that stays can move it.
        moved_day = [m for m in _moved_pillars(local, civil, late_zishi) if m[0] == "日柱"]
        if moved_day:
            _, solar_day, clock_day = moved_day[0]
            ambiguities.append(
                f"真太阳时把钟点移到了 {_clock_text(local, civil)}，日柱也跟着换了：本盘按修正后"
                f"的钟点取{solar_day}（日主{solar_day[0]}）；按钟表时间取是{clock_day}（日主"
                f"{clock_day[0]}）。")
    elif true_solar_time and lon is None:
        ambiguities.append("请求真太阳时但未提供经度，已回退为民用标准时。")
    elif true_solar_time:
        ambiguities.append("出生时刻未知：真太阳时无从修正（时柱本来就不计算）。")

    # Knowing the longitude but charting on the clock is a real choice, and a common reason
    # two charts of one person disagree. If True Solar Time would give another 日柱 or 时柱,
    # say which.
    if hour_known and lon is not None and not true_solar_time:
        solar_clock = _apply_true_solar_time(civil, lon, standard_meridian)
        moved = _moved_pillars(civil, solar_clock, late_zishi)
        if moved:
            would, used = _say_moved(moved)
            ambiguities.append(
                f"按真太阳时（经度 {lon:g}°）算，出生时刻是 {_clock_text(solar_clock, civil)}，"
                f"{would}；本盘按钟表时间取{used}。不同排盘软件的默认做法不一样，对照时看到的"
                "四柱可能不同。想按真太阳时起盘，加 --true-solar-time。")

    # Daylight-saving time runs the clock ahead of the zone's standard time (an hour; half
    # an hour on Lord Howe), and many charting apps take it off before reading the 日柱 and
    # 时柱. True Solar Time reads the real instant, so it has nothing to add there.
    if hour_known and isinstance(tz, str) and not tst_applied:
        from zoneinfo import ZoneInfo
        dst = civil.replace(tzinfo=ZoneInfo(tz)).dst() or datetime.timedelta(0)
        # zoneinfo gives Dublin's winters and Morocco's Ramadan months a NEGATIVE dst: those
        # clocks sit behind the zone's nominal offset, which is not summer time
        if dst > datetime.timedelta(0):
            standard = civil - dst
            moved = _moved_pillars(civil, standard, late_zishi)
            if moved:
                would, used = _say_moved(moved)
                mins = int(dst.total_seconds() // 60)
                ahead = f"{mins // 60} 小时" if mins % 60 == 0 else f"{mins} 分钟"
                ambiguities.append(
                    f"出生时 {tz} 正实行夏令时，钟表比标准时间快 {ahead}：本盘按记录的钟点 "
                    f"{civil.strftime('%H:%M')} 取{used}；按标准时间 {_clock_text(standard, civil)}"
                    f" 取，{would}。有的排盘软件会先减去夏令时，对照时看到的四柱可能不同。")

    if hour_known and local.hour == 23:
        ambiguities.append(
            "23:00–24:00 出生属子时边界（早/晚子时分歧），当前采用"
            + ("晚子时（子时不换日，日柱用当日）" if late_zishi
               else "早子时（子时换日，日柱用次日）")
            + "，换一种规则日柱可能不同。"
        )
    if not hour_known:
        ambiguities.append("出生时刻未知：时柱不可计算，与时柱相关的十神/藏干省略。")
        ambiguities.append("出生时刻未知也会影响起运：起运时刻由出生到节气的间隔折算，"
                           "时辰不同可差数月，大运的换运年份因此有出入。")

    # A 時辰 turns on every odd hour, and the 日柱 turns at midnight under 晚子时 and at 23:00
    # under 早子时. Within a few minutes of either, the recorded time decides the pillar, and
    # recorded times are often a few minutes off. Judged on the clock the chart actually uses
    # (the TST clock when TST is on).
    if hour_known:
        said = "修正后的出生时刻" if tst_applied else "出生时刻"
        minutes = local.hour * 60 + local.minute
        midnight = local.replace(hour=0, minute=0)
        edge = min(range(-60, 24 * 60 + 61, 120), key=lambda b: abs(minutes - b))
        gap = abs(minutes - edge)
        if gap <= SHICHEN_MARGIN_MIN:
            turn = midnight + datetime.timedelta(minutes=edge)
            before = _pillar_at(turn - datetime.timedelta(minutes=1), late_zishi, "Time")
            after = _pillar_at(turn, late_zishi, "Time")
            ambiguities.append(
                f"{said} {local.strftime('%H:%M')} 离时辰分界（{turn.strftime('%H:%M')}）只有 "
                f"{gap} 分钟：分界之前是{before}时，之后是{after}时。记录差几分钟，时柱就会换"
                "一柱，请确认出生时间。")
        edge = min((0, 24 * 60) if late_zishi else (-60, 23 * 60), key=lambda b: abs(minutes - b))
        gap = abs(minutes - edge)
        if gap <= SHICHEN_MARGIN_MIN:
            turn = midnight + datetime.timedelta(minutes=edge)
            before = _pillar_at(turn - datetime.timedelta(minutes=1), late_zishi, "Day")
            after = _pillar_at(turn, late_zishi, "Day")
            ambiguities.append(
                f"{said} {local.strftime('%H:%M')} 离日柱的分界（{turn.strftime('%H:%M')}，"
                + ("晚子时零点换日" if late_zishi else "早子时 23:00 换日")
                + f"）只有 {gap} 分钟：分界之前是{before}日，之后是{after}日。日柱带着日主，"
                "记录差几分钟日主就会换，请确认出生时间。")

    # The INSTANT (年柱/月柱, 立春, 大运, 起运): the civil clock on a Beijing wall clock.
    # Always from `civil`, never from `local`.
    instant, tz_shift = _to_china_clock(civil, tz)
    if tz is None:
        ambiguities.append(
            "未提供出生地时区（--tz）：本引擎的節氣/立春表以东八区为准，此盘按"
            "「出生钟点即北京时间」计算。出生地不在东八区时，年柱与月柱可能算错——"
            "请补上 --tz（如 Europe/Amsterdam）。")
    elif abs(tz_shift) > 1e-9:
        ambiguities.append(
            f"出生地时区 {tz}：节气按绝对时刻比对（等效北京时间 "
            f"{instant.strftime('%Y-%m-%d %H:%M')}），年柱月柱据此定；日柱与时柱仍按"
            f"当地钟点。海外出生的日/时柱取法各家不同，此为本引擎的公开约定。")

    # With no birth time, a 節 decides a pillar only when it falls inside the birth DAY, and
    # that is the birthplace's day: [local 00:00, next local 00:00) on the Beijing clock the
    # table keeps. Each end takes its own offset, so a daylight-saving change that day is
    # counted. The notes used to compare Beijing calendar dates, which abroad both missed
    # real doubt and invented it.
    local_midnight = civil.replace(hour=0, minute=0)
    day_start = _to_china_clock(local_midnight, tz)[0]
    day_end = _to_china_clock(local_midnight + datetime.timedelta(days=1), tz)[0]

    def falls_on_birth_day(moment):
        return moment is not None and day_start <= moment < day_end

    # 立春 is a MOMENT: a birth within a few hours of it flips the whole year pillar.
    # Surface that as an ambiguity — it is exactly the kind of thing the person must be
    # told, and it is invisible unless the script says it.
    lichun_gap, lichun_moment = _lichun_gap_hours(instant)
    on_lichun_day = bool(lichun_moment and lichun_moment.date() == instant.date())
    if not hour_known:
        if falls_on_birth_day(lichun_moment):
            ambiguities.append(
                f"这一天立春交节（{_when(lichun_moment, tz)}）——出生时刻未知，年柱和月柱都"
                "取决于出生在交节之前还是之后，需要确认出生时间。")
    elif lichun_gap is not None and abs(lichun_gap) <= 24:
        side = "之后" if lichun_gap >= 0 else "之前"
        ambiguities.append(
            f"出生在立春（{_when(lichun_moment, tz)}）{side}约{abs(lichun_gap):.1f}小时——"
            "年柱以立春交节的『时刻』为界，差几十分钟年柱就会换一柱，请确认出生时刻（含出生地"
            "时区）准确。")

    # The other eleven 節 move the 月柱 exactly as 立春 moves the 年柱, and nothing said so.
    jie, jie_gap, jie_moment = _nearest_jie(instant)
    if jie is not None:
        when = _when(jie_moment, tz)
        if not hour_known:
            if falls_on_birth_day(jie_moment):
                ambiguities.append(
                    f"这一天{jie}交节（{when}）——出生时刻未知，月柱取决于出生在交节之前还是"
                    "之后，需要确认出生时间。")
        elif abs(jie_gap) <= JIE_MARGIN_HOURS:
            side = "之后" if jie_gap >= 0 else "之前"
            head = (f"出生在{jie}（{when}）{side}约{abs(jie_gap):.1f}小时——月柱以{jie}交节"
                    "的『时刻』为界")
            ambiguities.append(head + (
                "，出生时间或时区差几个小时月柱就会换一柱，请确认。" if abs(jie_gap) < 6 else
                "；出生时间和时区没有记错的话，月柱不受影响。"))

    def eight_char(dt):
        ec = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0) \
            .getLunar().getEightChar()
        # Verified vs lunar-python: sect 2 (晚子时/子时不换日) keeps a 23:00–24:00 birth on
        # TODAY's 日柱; sect 1 (早子时/子时换日) rolls it to the NEXT day's 日柱. Default sect 2.
        ec.setSect(2 if late_zishi else 1)
        return ec

    ec_local = eight_char(local)
    # The same object when both clocks agree, so a China birth computes exactly as before.
    ec_jieqi = ec_local if instant == local else eight_char(instant)
    chart = _FramedChart(ec_jieqi, ec_local)
    solar = Solar.fromYmdHms(local.year, local.month, local.day, local.hour, local.minute, 0)

    gender_code = 1 if gender.lower().startswith("m") else 0

    pillars = {
        "year": _pillar(chart, "Year"),
        "month": _pillar(chart, "Month"),
        "day": _pillar(chart, "Day"),
    }
    if hour_known:
        pillars["hour"] = _pillar(chart, "Time")
    else:
        pillars["hour"] = None

    day_gan = chart.getDayGan()
    tally = _element_tally(chart, hour_known)
    strength = _strength_heuristic(day_gan, tally)
    strength_label = strength["label"]
    favor_sets = _favor_sets(day_gan, strength_label)
    # A year-difference is NOT an age: before the birthday it is one too high, which
    # pushed anyone sitting on a 大运 boundary into the NEXT decade entirely. The
    # "current decade" drives the whole stage reading, so that is a ten-year error,
    # not an off-by-one.
    _today = datetime.date.today()
    current_age = None
    if y:
        current_age = _today.year - y - ((_today.month, _today.day) < (m, d))

    result = {
        "computed": {  # ---- reproducible system facts ----
            "input": {
                "date": date, "time": time, "time_known": hour_known,
                "gender": "male" if gender_code == 1 else "female",
                "conventions": {
                    "tz": tz,
                    "jieqi_frame": ("birthplace tz → Beijing clock (節氣 are absolute "
                                    "instants)" if tz is not None
                                    else "ASSUMED: birth clock is Beijing time"),
                    "jieqi_instant_beijing_clock": instant.strftime("%Y-%m-%d %H:%M"),
                    "day_hour_frame": ("True Solar Time of the birth clock" if tst_applied
                                       else "local birth clock"),
                    "standard_meridian": standard_meridian,
                    # honest: reflects whether TST was ACTUALLY applied (needs lon + hour)
                    "true_solar_time": tst_applied,
                    "zishi_rule": "late" if late_zishi else "early",
                    "canggan_weighting": "main+hidden (disclosed)",
                    "engine": "lunar-python (MIT), 节气-based boundaries",
                },
            },
            "pillars": pillars,
            "day_master": {
                "gan": day_gan,
                "element": GAN_ELEMENT[day_gan],
                "yinyang": GAN_YINYANG[day_gan],
                "as_text": f"{GAN_YINYANG[day_gan]}{GAN_ELEMENT[day_gan]}（{day_gan}）",
            },
            "element_tally": tally,
            "extras": _extras(chart, hour_known),
            "current_age_approx": current_age,
            # 大运 hang off the instant: direction from the year stem shown, the sequence
            # from the month pillar shown, 起运 from the real distance to the 節.
            "luck_pillars": _luck_pillars(ec_jieqi, gender_code, day_gan, favor_sets,
                                          current_age),
            "current_annual_pillar": _current_liunian(solar),
            "upcoming_annual_pillars": _upcoming_annual_pillars(day_gan, favor_sets, y, years=10),
            "daily": (_daily_pillars(day_gan, favor_sets, on_date, chart.getYearZhi(), natal=pillars)
                      if on_date else None),
            # sxtwl is date-granular, so give it the date the 節氣 frame actually uses
            "cross_check_sxtwl": _cross_check(
                instant.year, instant.month, instant.day, pillars["year"]["ganzhi"],
                on_lichun_day, ambiguities),
        },
        "heuristic": {  # ---- clearly labeled, NOT a fact ----
            "strength": strength,
            "favor_sets": {**favor_sets, "_note":
                "喜/忌 tags on 大运/流年 derive SOLELY from the 扶抑 strength heuristic "
                "(比劫+印=扶, 食伤+财+官杀=抑); near-balanced charts get 平. Real 用神 also "
                "needs 调候/病药/通关/格局, uncomputed here — one school's rule of thumb."},
        },
        "ambiguities": ambiguities,
        "disclaimer": (
            "四柱/日主/五行/十神/大运为传统规则的确定性推算（可复现）；身强弱、"
            "用神喜忌及一切吉凶解读为流派性的『反思视角』，非科学预测。"
        ),
    }

    # "Around nine" is a real answer. Chart every ten minutes across the window and report
    # which pillars actually move, instead of pretending the recorded minute is exact.
    if time_window is not None:
        if not hour_known:
            ambiguities.append("没有出生时间，时间范围（--time-window）不起作用。")
        else:
            w = int(time_window)
            seen = {k: [] for k in ("year", "month", "day", "hour")}
            for off in sorted(set(range(-w, w + 1, 10)) | {-w, w}):
                t = civil + datetime.timedelta(minutes=off)
                sample = compute(t.date().isoformat(), t.strftime("%H:%M"), gender, lon=lon,
                                 true_solar_time=true_solar_time,
                                 standard_meridian=given_meridian, late_zishi=late_zishi,
                                 tz=tz)["computed"]["pillars"]
                for k in seen:
                    if sample[k]["ganzhi"] not in seen[k]:
                        seen[k].append(sample[k]["ganzhi"])
            changes = [k for k in seen if len(seen[k]) > 1]
            result["computed"]["time_window"] = {"minutes": w, "pillars": seen,
                                                 "changes": changes}
            # A relation on a pillar the window can't settle is not a fact about this person.
            daily = result["computed"]["daily"]
            if daily:
                for row in daily.get("natal_relations", []):
                    row["uncertain"] = row["pillar"] in changes
                daily["zodiac_day"]["uncertain"] = "year" in changes
            label = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
            ambiguities.append(
                f"出生时间按 ±{w} 分钟估：" + ("；".join(
                    f"{label[k]}可能是 {' / '.join(seen[k])}" for k in changes)
                    + "。其余各柱在这个范围里不变。" if changes else "四柱在这个范围里都不变。"))
    return result


def _format_text(r):
    c = r["computed"]
    L = []
    p = c["pillars"]
    order = [("年", "year"), ("月", "month"), ("日", "day"), ("时", "hour")]
    L.append("四柱 (Four Pillars):")
    header = "  " + "".join(f"{k:<6}" for k, _ in order)
    row_gz = "  " + "".join(
        f"{(p[v]['ganzhi'] if p[v] else '——'):<6}" for _, v in order
    )
    L.append(header)
    L.append(row_gz)
    dm = c["day_master"]
    L.append(f"\n日主 Day Master: {dm['as_text']}")
    t = c["element_tally"]["with_hidden"]
    L.append("五行(含藏干) Elements: " + "  ".join(f"{e}:{t[e]}" for e in ELEMENTS))
    h = r["heuristic"]["strength"]
    L.append(f"强弱(扶抑,启发式): {h['label']}  ratio={h['supportive_ratio']}")
    lp = c["luck_pillars"]
    q = lp["qiyun_after"]
    L.append(f"\n大运 {lp['direction']}  起运: 约{q['years']}年{q['months']}月后  (当前约{c['current_age_approx']}岁)")
    for dy in lp["pillars"][:8]:
        cur = " ← 当前" if dy.get("is_current") else ""
        L.append(f"  {dy['start_age']:>2}-{dy['end_age']:>2}岁 ({dy['start_year']}) "
                 f"{dy['ganzhi']}  {dy['ten_god']}/{dy['ten_god_category']} [{dy['favor']}]{cur}")
    ul = c.get("upcoming_annual_pillars", [])
    if ul:
        L.append("\n近年流年:")
        for ly in ul[:6]:
            L.append(f"  {ly['civil_year']} {ly['ganzhi']}  {ly['ten_god']} [{ly['favor']}]")
    dl = c.get("daily")
    if dl:
        L.append(f"\n今日({dl['date']})流盘:  流年 {dl['liunian']['ganzhi']}({dl['liunian']['ten_god']})"
                 f"  流月 {dl['liuyue']['ganzhi']}({dl['liuyue']['ten_god']})"
                 f"  流日 {dl['liuri']['ganzhi']}({dl['liuri']['ten_god']}) [{dl['liuri']['favor']}]")
    if r["ambiguities"]:
        L.append("\n注意:")
        for a in r["ambiguities"]:
            L.append("  · " + a)
    L.append("\n" + r["disclaimer"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Deterministic BaZi / 四柱 computation.")
    ap.add_argument("--date", required=True, help="Birth date YYYY-MM-DD (solar/公历)")
    ap.add_argument("--time", default=None, help="Birth clock time HH:MM (omit if unknown)")
    ap.add_argument("--gender", required=True, choices=["m", "f", "male", "female"])
    ap.add_argument("--place", default=None, help="Birthplace label (metadata only)")
    ap.add_argument("--lon", type=float, default=None, help="Longitude (for True Solar Time)")
    ap.add_argument("--true-solar-time", action="store_true",
                    help="Apply True Solar Time (真太阳时) correction — off by default")
    ap.add_argument("--tz", default=None,
                    help="BIRTHPLACE timezone — IANA name (Europe/Amsterdam) or UTC offset "
                         "(1, -5, +05:30, UTC+8). REQUIRED for a birth outside UTC+8: 節氣 are absolute "
                         "instants and the engine's tables are Beijing-based, so without "
                         "this the year/month pillar can be wrong.")
    ap.add_argument("--standard-meridian", type=float, default=None,
                    help="Timezone standard meridian (China=120)")
    ap.add_argument("--early-zishi", action="store_true",
                    help="Use 早子时/子时换日 (23:00–24:00 → NEXT day's 日柱); "
                         "default 晚子时 keeps it on the same day")
    ap.add_argument("--on-date", default=None,
                    help="Add a 流年/流月/流日 daily block for this date (YYYY-MM-DD, or 'today')")
    ap.add_argument("--time-window", type=int, default=None, metavar="MINUTES",
                    help="the birth time is only known to ± this many minutes (e.g. 60 for "
                         "'around nine'): lists every pillar the chart could have in that window")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    args = ap.parse_args(argv_with_offsets(("--tz",)))

    try:
        tz = parse_tz(args.tz) if args.tz is not None else None
    except ValueError as e:
        print(json.dumps({"ok": False, "error": f"bad input: {e}"}, ensure_ascii=False))
        sys.exit(2)
    try:
        on_date = None
        if args.on_date:
            on_date = (datetime.date.today() if args.on_date == "today"
                       else datetime.date.fromisoformat(args.on_date))
        r = compute(
            date=args.date, time=args.time, gender=args.gender, lon=args.lon,
            true_solar_time=args.true_solar_time,
            standard_meridian=args.standard_meridian, tz=tz,
            late_zishi=not args.early_zishi, on_date=on_date,
            time_window=args.time_window,
        )
    except (ValueError, TypeError) as e:
        print(json.dumps({"ok": False, "error": f"bad input: {e}. "
                          "Expect --date YYYY-MM-DD and --time HH:MM (24h)."},
                         ensure_ascii=False))
        sys.exit(2)
    if args.format == "text":
        print(_format_text(r))
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

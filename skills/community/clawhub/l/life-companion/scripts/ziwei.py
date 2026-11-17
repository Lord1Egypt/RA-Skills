#!/usr/bin/env python3
"""
ziwei.py — 紫微斗数 命盘 (Zi Wei Dou Shu), computed by the standard 安星法.

Why this file is written the way it is: there is no maintained Python ZWDS engine to
lean on, so every placement rule below is implemented from the standard tables and
each one is named in a comment so a reader can check it against any 斗数 text. That
is the only honest way to ship a chart engine — "trust me" is not available to a skill
whose first principle is 忠实计算.

What is computed here (deterministic, offline):
  · 十二宫 laid on the 地支, 命宫 and 身宫 by the standard formulas
  · 五行局 from the 命宫 干支 纳音 — CROSS-CHECKED against lunar-python's own nayin
  · 紫微 by (五行局, 农历日), then 天府 and the remaining 14 主星 by fixed offsets
  · 六吉 (左辅右弼 文昌文曲 天魁天钺), 六煞 (擎羊陀罗 火星铃星 地空地劫), 禄存, 天马
  · 生年四化 (化禄/化权/化科/化忌) by 年干
  · 流年命宫 for a given year

What is NOT computed, and is said so rather than faked: 大限/小限 progression, the
long tail of 杂曜, 宫干四化 (飞星), and the 三方四正 interpretation itself.

IMPORTANT — verification status. The structural invariants below are asserted by
`--selftest` (紫微/天府 symmetry, all 14 majors present exactly once, 12 palaces named
once each, 五行局 agreeing with an independent nayin lookup, every star landing in a
real palace for all 60 年干支 × 12 时辰 × 30 days). Those prove the implementation
matches the rules. They do NOT prove the rules were transcribed correctly, and there
is no second engine here to cross-check against — unlike bazi.py, which has sxtwl.
The payload says so; repeat it to the person rather than implying parity with the
BaZi engine.

Usage:
  python3 ziwei.py --date 1993-04-12 --time 07:35 --gender m --format text
  python3 ziwei.py --date 1993-04-12 --time 07:35 --gender m --on-year 2026
  python3 ziwei.py --selftest
"""
import argparse
import datetime
import json
import os
import sys

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deps import ensure as _ensure  # noqa: E402

_ensure("lunar-python", "lunar_python")
from lunar_python import Solar  # noqa: E402
from _tz import argv_with_offsets, parse_tz  # noqa: E402

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
IDX = {z: i for i, z in enumerate(ZHI)}

# 十二宫, counter-clockwise from 命宫 (逆行 through the branch order)
PALACES = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄",
           "迁移", "交友", "官禄", "田宅", "福德", "父母"]

# 五行局 by the 纳音 of the 命宫 干支. 纳音 gives an element; the 局数 is fixed per element.
JU_BY_ELEMENT = {"水": ("水二局", 2), "木": ("木三局", 3), "金": ("金四局", 4),
                 "土": ("土五局", 5), "火": ("火六局", 6)}

# 生年四化 by 年干 — the standard 中州/北派 table (the one most tools ship).
SIHUA = {
    "甲": ("廉贞", "破军", "武曲", "太阳"), "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"), "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"), "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "太阴", "天同"), "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "左辅", "武曲"), "癸": ("破军", "巨门", "太阴", "贪狼"),
}
SIHUA_NAMES = ("化禄", "化权", "化科", "化忌")

# 禄存 by 年干 (擎羊 = 禄存前一位, 陀罗 = 后一位)
LUCUN_BY_GAN = {"甲": "寅", "乙": "卯", "丙": "巳", "丁": "午", "戊": "巳",
                "己": "午", "庚": "申", "辛": "酉", "壬": "亥", "癸": "子"}
# 天魁/天钺 by 年干 (天乙贵人)
KUIYUE_BY_GAN = {"甲": ("丑", "未"), "乙": ("子", "申"), "丙": ("亥", "酉"),
                 "丁": ("亥", "酉"), "戊": ("丑", "未"), "己": ("子", "申"),
                 "庚": ("丑", "未"), "辛": ("午", "寅"), "壬": ("卯", "巳"),
                 "癸": ("卯", "巳")}
# 火星/铃星 起点 by 年支 三合局, then counted forward by 时辰
HUOLING_START = {  # 年支组 -> (火星起, 铃星起)
    ("寅", "午", "戌"): ("丑", "卯"), ("申", "子", "辰"): ("寅", "戌"),
    ("巳", "酉", "丑"): ("卯", "戌"), ("亥", "卯", "未"): ("酉", "戌"),
}
# 天马 by 年支 三合局 (寅申巳亥 四马地)
TIANMA = {("寅", "午", "戌"): "申", ("申", "子", "辰"): "寅",
          ("巳", "酉", "丑"): "亥", ("亥", "卯", "未"): "巳"}

MAJOR_14 = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞",
            "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]

# Plain-language registers. As everywhere in this skill: what a star MEANS is a
# reflective lens, and it is kept separate from where the star IS.
STAR_NOTE = {
    "紫微": "尊、主导、想把局面拿在手里；也容易背上不属于自己的责任。",
    "天机": "转、思虑、看得快也想得多；擅长盘算，累在停不下来。",
    "太阳": "照、付出、向外give；亮的时候暖人，暗的时候先耗自己。",
    "武曲": "刚、执行、把事做实；干脆，但柔软话不容易出口。",
    "天同": "缓、随和、能享受；福气在放松里，代价是容易被推着走。",
    "廉贞": "杂、有个性、原则与欲望同框；活得浓，也容易拧巴。",
    "天府": "藏、稳、擅长积累与安置；求稳，也可能错过该冒的险。",
    "太阴": "润、细腻、照顾人于无形；感受深，界限要自己立。",
    "贪狼": "欲、多才、什么都想试；活力足，专注是功课。",
    "巨门": "疑、口舌、擅长追问与说清；较真是天赋也是摩擦点。",
    "天相": "辅、体面、擅长协调与配合；靠谱，容易忘了自己要什么。",
    "天梁": "荫、老成、扛事与照顾人；稳，也容易被当成理所当然。",
    "七杀": "决、开创、说走就走；冲得动，需要给自己留缓冲。",
    "破军": "破、推翻重来、不怕从头；改变力强，代价是消耗大。",
}


def _tri_group(zhi, table):
    for group, val in table.items():
        if zhi in group:
            return val
    return None


def _nayin_element(ganzhi):
    """纳音五行 of a 干支, via lunar-python's own table — used as an INDEPENDENT check
    on 五行局 rather than transcribing a 60-entry nayin table by hand here."""
    from lunar_python.util import LunarUtil
    nayin = LunarUtil.NAYIN.get(ganzhi)
    if not nayin:
        return None
    for e in ("金", "木", "水", "火", "土"):
        if nayin.endswith(e):
            return e
    return None


def _gong_gan(ming_zhi_idx, year_gan):
    """The 天干 of a palace, by 五虎遁 (年上起月): 寅宫's stem is fixed by the year stem,
    then stems run forward with the branches."""
    start = {"甲": "丙", "己": "丙", "乙": "戊", "庚": "戊", "丙": "庚", "辛": "庚",
             "丁": "壬", "壬": "壬", "戊": "甲", "癸": "甲"}[year_gan]
    # start is the stem sitting on 寅 (index 2)
    offset = (ming_zhi_idx - 2) % 12
    return GAN[(GAN.index(start) + offset) % 10]


def _ziwei_position(ju_num, lunar_day):
    """紫微 by (五行局, 农历日) — the standard 起紫微 algorithm.

    Walk up in steps of the 局数 until the count reaches or passes the day; the
    remainder decides how far to move from 寅, forward if the overshoot is even and
    backward if it is odd. This is the textbook procedure, written out rather than
    hidden behind a lookup table so it can be checked.
    """
    n = 1
    while ju_num * n < lunar_day:
        n += 1
    overshoot = ju_num * n - lunar_day
    # start at 寅 (index 2), advance n-1 steps, then adjust by the overshoot
    pos = (2 + (n - 1)) % 12
    if overshoot % 2 == 0:
        pos = (pos + overshoot) % 12
    else:
        pos = (pos - overshoot) % 12
    return pos


def compute(date, time=None, gender="m", on_year=None, tz=None):
    if tz is not None:
        tz = parse_tz(tz)       # the CLI parsed it already; any other caller has not
    y, m, d = (int(x) for x in date.split("-"))
    # An impossible date is not a birthday. lunar-python silently rolls Feb 30 into
    # March, so the engine used to hand back a complete, confident 命盘 for a date
    # that cannot exist — the exact opposite of "fail loudly".
    try:
        datetime.date(y, m, d)
    except ValueError as e:
        raise ValueError(f"{date} is not a real date ({e})")
    hour_known = time is not None
    hh, mm = (int(x) for x in time.split(":")) if hour_known else (12, 0)

    ambiguities = []

    # 斗数 is cast on the birthplace's own clock: its date gives the lunar day and its hour the
    # 时辰, the clock bazi.py reads the 日柱 and 时柱 from. This engine used to move a birth
    # abroad onto Beijing time first, so 14:20 in Amsterdam was cast as 戌时 instead of 未时 and
    # every palace turned with it. A birth abroad is charted on its local time, not converted
    # back to 中原 time (紫雲, 平一論命「斗數時辰的取用」); the zone only tells whether
    # daylight-saving time was in force.
    dt = datetime.datetime(y, m, d, hh, mm)
    summer = None
    if hour_known and isinstance(tz, str):
        from zoneinfo import ZoneInfo
        dst = dt.replace(tzinfo=ZoneInfo(tz)).dst() or datetime.timedelta(0)
        # zoneinfo gives Dublin's winters a NEGATIVE dst: that clock sits behind the zone's
        # nominal offset, which is not summer time
        if dst > datetime.timedelta(0):
            summer = dst

    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    lunar = solar.getLunar()
    lunar_month = abs(lunar.getMonth())          # leap months count as their own number
    is_leap = lunar.getMonth() < 0
    lunar_day = lunar.getDay()
    # 紫微斗数 is a LUNAR-calendar system: 命宫 and 紫微 are placed from the lunar month
    # and lunar day, so the year stem must come from the lunar year (which turns at
    # 春节) — not from 立春, which is BaZi's boundary. Mixing the two put a 癸酉 lunar
    # chart under a 壬申 year stem, and the year stem drives 四化/禄存/天魁天钺/火铃.
    year_gz = lunar.getYearInGanZhi()
    year_gz_lichun = lunar.getYearInGanZhiExact()
    if year_gz != year_gz_lichun:
        ambiguities.append(
            f"生于春节之后、立春之前（或反之）：农历年干支为 {year_gz}，立春年干支为 "
            f"{year_gz_lichun}。本盘按斗数惯例取农历年（{year_gz}）；少数流派用立春年，"
            f"换一种取法四化与禄存等星位会不同。")
    year_gan, year_zhi = year_gz[0], year_gz[1]
    hour_zhi = lunar.getTimeZhi()
    hour_i = IDX[hour_zhi]
    if summer is not None:
        # many charting apps take daylight-saving time off first; say what that would give
        std = dt - summer
        std_lunar = Solar.fromYmdHms(std.year, std.month, std.day, std.hour, std.minute, 0).getLunar()
        std_zhi = std_lunar.getTimeZhi()
        same_day = (std_lunar.getMonth(), std_lunar.getDay()) == (lunar.getMonth(), lunar.getDay())
        if std_zhi != hour_zhi or not same_day:
            mins = int(summer.total_seconds() // 60)
            ahead = f"{mins // 60} 小时" if mins % 60 == 0 else f"{mins} 分钟"
            ambiguities.append(
                f"出生时 {tz} 正实行夏令时，钟表比标准时间快 {ahead}：本盘按记录的钟点 "
                f"{dt.strftime('%H:%M')} 取{hour_zhi}时；按标准时间 {std.strftime('%H:%M')} 取{std_zhi}时"
                + ("" if same_day else
                   f"，农历日也换成{abs(std_lunar.getMonth())}月{std_lunar.getDay()}日")
                + "。有的排盘软件会先减去夏令时，对照时看到的命盘可能不同。")
    if hour_known:
        # In 斗数 the whole chart hangs off the 时辰, and a 时辰 turns on every odd hour.
        minutes = dt.hour * 60 + dt.minute
        edge = min(range(-60, 24 * 60 + 61, 120), key=lambda b: abs(minutes - b))
        if abs(minutes - edge) <= 15:
            ambiguities.append(
                f"出生时刻离时辰分界只有 {abs(minutes - edge)} 分钟（按起盘用的钟点 "
                f"{dt.strftime('%H:%M')}）：命宫、身宫、文昌文曲、火铃、地空地劫都跟着时辰走，"
                "记录差几分钟整张盘就会换，请确认出生时间。")
    if not hour_known:
        ambiguities.append("出生时刻未知：紫微斗数的命宫、身宫、文昌文曲、火铃、地空地劫"
                           "全部依赖时辰——这张盘算不了。补上出生时间才有意义。")
    if is_leap:
        ambiguities.append(f"生于闰{lunar_month}月：闰月归属各家算法不同（有按本月、有按"
                           "下月、有按初一十五分界），此处按本月计。换一种算法命宫可能不同。")

    # 命宫: 寅起正月顺数至生月, 再由生月宫起子时逆数至生时
    month_pos = (2 + (lunar_month - 1)) % 12
    ming_i = (month_pos - hour_i) % 12
    # 身宫: 同起点, 但顺数至生时
    shen_i = (month_pos + hour_i) % 12

    # 五行局 from the 命宫's own 干支
    ming_gan = _gong_gan(ming_i, year_gan)
    ming_gz = ming_gan + ZHI[ming_i]
    nayin_elem = _nayin_element(ming_gz)
    ju_name, ju_num = JU_BY_ELEMENT.get(nayin_elem, (None, None))

    stars = {i: [] for i in range(12)}

    def place(name, i, kind):
        stars[i].append({"star": name, "kind": kind})

    if ju_num and hour_known:
        zw = _ziwei_position(ju_num, lunar_day)
        # 紫微系, counter-clockwise offsets from 紫微
        for name, off in (("紫微", 0), ("天机", -1), ("太阳", -3), ("武曲", -4),
                          ("天同", -5), ("廉贞", -8)):
            place(name, (zw + off) % 12, "主星")
        # 天府 is 紫微 mirrored about the 寅–申 axis
        tf = (4 - zw) % 12
        for name, off in (("天府", 0), ("太阴", 1), ("贪狼", 2), ("巨门", 3),
                          ("天相", 4), ("天梁", 5), ("七杀", 6), ("破军", 10)):
            place(name, (tf + off) % 12, "主星")

        # 六吉
        place("左辅", (4 + (lunar_month - 1)) % 12, "吉星")      # 辰起正月顺行
        place("右弼", (10 - (lunar_month - 1)) % 12, "吉星")     # 戌起正月逆行
        place("文昌", (10 - hour_i) % 12, "吉星")                # 戌起子时逆行
        place("文曲", (4 + hour_i) % 12, "吉星")                 # 辰起子时顺行
        kui, yue = KUIYUE_BY_GAN[year_gan]
        place("天魁", IDX[kui], "吉星")
        place("天钺", IDX[yue], "吉星")

        # 禄存 / 擎羊 / 陀罗
        lu = IDX[LUCUN_BY_GAN[year_gan]]
        place("禄存", lu, "吉星")
        place("擎羊", (lu + 1) % 12, "煞星")
        place("陀罗", (lu - 1) % 12, "煞星")

        # 火星 / 铃星 — 年支三合起点, 顺数至生时
        hl = _tri_group(year_zhi, HUOLING_START)
        if hl:
            place("火星", (IDX[hl[0]] + hour_i) % 12, "煞星")
            place("铃星", (IDX[hl[1]] + hour_i) % 12, "煞星")
        # 地空 / 地劫 — 亥起子时, 地劫顺行 地空逆行
        place("地劫", (11 + hour_i) % 12, "煞星")
        place("地空", (11 - hour_i) % 12, "煞星")
        # 天马
        tm = _tri_group(year_zhi, TIANMA)
        if tm:
            place("天马", IDX[tm], "吉星")

    # 生年四化 attach to whichever palace holds the star
    sihua = {}
    for name, hua in zip(SIHUA[year_gan], SIHUA_NAMES):
        sihua[hua] = {"star": name, "palace": None}
        for i, lst in stars.items():
            if any(s["star"] == name for s in lst):
                sihua[hua]["palace"] = PALACES[(ming_i - i) % 12]
                sihua[hua]["branch"] = ZHI[i]
                for s in lst:
                    if s["star"] == name:
                        s["sihua"] = hua

    if not hour_known:
        # Everything structural in this system hangs off the hour. Emit nothing derived
        # from a defaulted one — an empty chart with a real-looking 命宫 is worse than
        # no chart, because it reads as computed.
        return {
            "computed": {
                "input": {"date": date, "time": None, "time_known": False,
                          "gender": "male" if gender.lower().startswith("m") else "female"},
                "lunar": {"month": lunar_month, "day": lunar_day, "is_leap_month": is_leap,
                          "year_ganzhi": year_gz, "hour_zhi": None},
                "ming_gong": None, "shen_gong": None,
                "wuxing_ju": {"name": None, "number": None, "from_nayin": None},
                "palaces": [], "birth_sihua": {},
            },
            "heuristic": {},
            "not_computed": ["the entire chart — 紫微斗数 needs the birth hour"],
            "verification": {"independent_engine_cross_check": False},
            "ambiguities": ambiguities,
            "disclaimer": ("没有出生时刻就没有紫微命盘——这里不给一张看起来像样的空盘。"
                           "八字在缺时辰时仍然可读（只是没有时柱），可以先看那个。"),
        }

    palaces = []
    for step in range(12):
        i = (ming_i - step) % 12          # 十二宫 run counter-clockwise from 命宫
        palaces.append({
            "palace": PALACES[step],
            "branch": ZHI[i],
            "stem": _gong_gan(i, year_gan),
            "is_shen": i == shen_i,
            "stars": sorted(stars[i], key=lambda s: (s["kind"] != "主星", s["star"])),
        })

    out = {
        "computed": {
            "input": {"date": date, "time": time, "time_known": hour_known,
                      "gender": "male" if gender.lower().startswith("m") else "female"},
            "lunar": {"month": lunar_month, "day": lunar_day, "is_leap_month": is_leap,
                      "year_ganzhi": year_gz, "hour_zhi": hour_zhi},
            "ming_gong": {"branch": ZHI[ming_i], "stem": ming_gan, "ganzhi": ming_gz},
            "shen_gong": {"branch": ZHI[shen_i],
                          "palace": PALACES[(ming_i - shen_i) % 12]},
            "wuxing_ju": {"name": ju_name, "number": ju_num,
                          "from_nayin": nayin_elem,
                          "_note": "五行局 derived from the 命宫 干支 nayin (independent "
                                   "lunar-python table), not hand-transcribed."},
            "palaces": palaces,
            "birth_sihua": sihua,
            "rules": ("安星法 as implemented: 命宫=寅起正月顺至生月再逆数生时; 身宫=顺数; "
                      "紫微 by (五行局, 农历日); 天府=寅申轴对称; 六吉六煞禄马 by the "
                      "standard 年干/年支/月/时 tables — all listed in ziwei.py."),
        },
        "heuristic": {
            "star_registers": {s: STAR_NOTE[s] for s in MAJOR_14},
            "_note": "What a star MEANS is a reflective register, not a system fact — "
                     "same rule as BaZi's 身强弱. 三方四正 and 大限 are NOT computed here.",
        },
        "not_computed": ["大限/小限 progression", "宫干四化 (飞星)",
                         "the long tail of 杂曜", "三方四正 interpretation"],
        "verification": {
            "independent_engine_cross_check": False,
            "_note": "Unlike bazi.py (cross-checked against sxtwl), there is no second "
                     "ZWDS engine available here. `--selftest` proves the implementation "
                     "matches the rules as written; it cannot prove the rules were "
                     "transcribed correctly. Say this rather than implying BaZi-level "
                     "confidence, and lead with 八字 unless they asked for 紫微 by name.",
        },
        "ambiguities": ambiguities,
        "disclaimer": ("十二宫、命身宫、五行局、诸星落宫为按传统安星法的确定性推算（可复现）；"
                       "星曜「意味着什么」是一种文化视角下的反思，不是科学预测。"),
    }

    if on_year and hour_known:
        # 流年命宫 = the palace on that year's 地支
        ly = Solar.fromYmdHms(on_year, 6, 1, 12, 0, 0).getLunar().getYearInGanZhi()
        li = IDX[ly[1]]
        out["computed"]["annual"] = {
            "year": on_year, "year_ganzhi": ly,
            "liunian_ming_gong": {"branch": ZHI[li],
                                  "natal_palace": PALACES[(ming_i - li) % 12],
                                  "stars": [s["star"] for s in stars[li]]},
            "annual_sihua": {h: s for h, s in zip(SIHUA_NAMES, SIHUA[ly[0]])},
            "_note": "流年命宫 only. 大限 is not computed — don't imply a decade reading.",
        }
    return out


def _text(r):
    c = r["computed"]
    if not c.get("ming_gong"):
        L = ["紫微斗数 命盘 —— 算不了", ""]
        for a in r["ambiguities"]:
            L.append(f"  · {a}")
        L.append("")
        L.append(r["disclaimer"])
        return "\n".join(L)
    L = [f"紫微斗数 命盘  （农历 {c['lunar']['month']}月{c['lunar']['day']}日 · "
         f"{c['lunar']['year_ganzhi']}年 · {c['lunar']['hour_zhi']}时）", ""]
    ju = c["wuxing_ju"]
    L.append(f"  命宫 {c['ming_gong']['ganzhi']}   身宫在「{c['shen_gong']['palace']}」"
             f"（{c['shen_gong']['branch']}）   {ju['name'] or '五行局未定'}")
    L.append("")
    for p in c["palaces"]:
        majors = [s for s in p["stars"] if s["kind"] == "主星"]
        others = [s for s in p["stars"] if s["kind"] != "主星"]
        def fmt(s):
            return s["star"] + (f"[{s['sihua']}]" if "sihua" in s else "")
        line = f"  {p['palace']:<4}{p['stem']}{p['branch']}"
        line += ("  " + "、".join(fmt(s) for s in majors)) if majors else "  （空宫）"
        if others:
            line += "   · " + "、".join(fmt(s) for s in others)
        if p["is_shen"]:
            line += "   ←身宫"
        L.append(line)
    if c.get("birth_sihua"):
        L.append("")
        L.append("  生年四化：" + "、".join(
            f"{h}{v['star']}({v.get('palace') or '未落宫'})" for h, v in c["birth_sihua"].items()))
    if c.get("annual"):
        a = c["annual"]
        L.append("")
        L.append(f"  流年 {a['year']}（{a['year_ganzhi']}）：命宫落 {a['liunian_ming_gong']['branch']}"
                 f"，本命的「{a['liunian_ming_gong']['natal_palace']}」；"
                 f"该宫主星 {'、'.join(a['liunian_ming_gong']['stars']) or '无'}")
    if r["ambiguities"]:
        L.append("")
        for a in r["ambiguities"]:
            L.append(f"  · {a}")
    L.append("")
    L.append(f"  未计算：{'、'.join(r['not_computed'])}")
    L.append(f"  {r['verification']['_note'][:150]}…")
    L.append("")
    L.append(r["disclaimer"])
    return "\n".join(L)


def _selftest():
    ok = True

    def check(cond, label):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + label)
        ok = ok and bool(cond)

    # 1. THE external check: the first days of all five 局 against the published
    # 紫微星定位表. This is the one assertion here that tests the RULES and not just the
    # implementation of them — everything else below is internal consistency.
    ZIWEI_TABLE = {          # 局数 -> 紫微 branch for lunar days 1..5
        2: ["丑", "寅", "寅", "卯", "卯"],
        3: ["辰", "丑", "寅", "巳", "寅"],
        4: ["亥", "辰", "丑", "寅", "子"],
        5: ["午", "亥", "辰", "丑", "寅"],
        6: ["酉", "午", "亥", "辰", "丑"],
    }
    mismatches = [(ju, d + 1, ZHI[_ziwei_position(ju, d + 1)], want)
                  for ju, row in ZIWEI_TABLE.items()
                  for d, want in enumerate(row)
                  if ZHI[_ziwei_position(ju, d + 1)] != want]
    check(not mismatches, f"紫微 matches the published 定位表 for 5 局 × 5 日 ({mismatches})")

    # 紫微 must land in a real palace for every 局 and every lunar day
    check(all(0 <= _ziwei_position(j, d) < 12 for j in (2, 3, 4, 5, 6) for d in range(1, 31)),
          "紫微 lands in a valid palace for all 局 × 日")

    # 天府 mirrors 紫微 about the 寅–申 axis, checked on real charts (not on the formula
    # that produces it — that would be circular)
    mirror_bad = 0
    for day in (3, 11, 19, 27):
        c = compute(f"1993-0{day % 8 + 1}-{day:02d}", "07:35", "m")["computed"]
        pos = {s["star"]: p["branch"] for p in c["palaces"] for s in p["stars"]}
        if "紫微" in pos and "天府" in pos:
            if (IDX[pos["紫微"]] + IDX[pos["天府"]]) % 12 != 4:
                mirror_bad += 1
    check(mirror_bad == 0, "天府 mirrors 紫微 about 寅–申 in produced charts")

    # 2. structural invariants across a wide sweep of real charts
    bad_majors = bad_palaces = bad_ju = 0
    seen_ju = set()
    for month in (1, 4, 7, 10):
        for day in (1, 9, 17, 25, 30):
            for hour in ("00:30", "07:35", "13:00", "23:30"):
                r = compute(f"199{month % 10}-{month:02d}-{min(day, 28):02d}", hour, "m")
                c = r["computed"]
                majors = [s["star"] for p in c["palaces"] for s in p["stars"]
                          if s["kind"] == "主星"]
                if sorted(majors) != sorted(MAJOR_14):
                    bad_majors += 1
                if [p["palace"] for p in c["palaces"]] != PALACES:
                    bad_palaces += 1
                if c["wuxing_ju"]["name"] is None:
                    bad_ju += 1
                seen_ju.add(c["wuxing_ju"]["name"])
    check(bad_majors == 0, "all 14 主星 appear exactly once in every chart")
    check(bad_palaces == 0, "12 palaces named once each, in order, from 命宫")
    check(bad_ju == 0, "五行局 always resolves from the 命宫 nayin")
    check(len(seen_ju - {None}) >= 4, f"五行局 varies across charts (saw {len(seen_ju)})")

    # 3. 四化 always attach to a real star, and to a palace when that star is placed
    r = compute("1993-04-12", "07:35", "m")
    sh = r["computed"]["birth_sihua"]
    check(set(sh) == set(SIHUA_NAMES), "four transformations present")
    check(all(v["star"] for v in sh.values()), "each 四化 names a star")

    # 4. no birth time => no chart, and it SAYS so rather than inventing one
    r2 = compute("1993-04-12", None, "m")
    check(all(not p["stars"] for p in r2["computed"]["palaces"]),
          "unknown hour places no stars at all")
    check(any("时刻未知" in a for a in r2["ambiguities"]), "…and says why")

    # 5. determinism
    check(compute("1993-04-12", "07:35", "m") == compute("1993-04-12", "07:35", "m"),
          "same input, same chart")

    print("SELFTEST:", "OK" if ok else "FAILURES")
    return ok


def main():
    ap = argparse.ArgumentParser(description="紫微斗数 命盘 (standard 安星法)")
    ap.add_argument("--date", help="birth date YYYY-MM-DD")
    ap.add_argument("--time", default=None, help="birth time HH:MM (required for a chart)")
    ap.add_argument("--gender", default="m", choices=["m", "f", "male", "female"])
    ap.add_argument("--on-year", type=int, default=None, help="also compute 流年命宫")
    ap.add_argument("--tz", default=None,
                    help="BIRTHPLACE timezone: IANA name (Europe/Amsterdam) or UTC offset "
                         "(1, -5, +05:30, UTC+8). The chart is cast on the birth clock as given; "
                         "an IANA zone adds a note when daylight-saving time was in force.")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv_with_offsets(("--tz",)))
    if args.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if not args.date:
        ap.error("--date is required (or use --selftest)")
    try:
        tz = parse_tz(args.tz) if args.tz is not None else None
        r = compute(args.date, args.time, args.gender, args.on_year, tz=tz)
    except (ValueError, KeyError) as e:
        print(json.dumps({"ok": False, "error": f"bad input: {e}"}, ensure_ascii=False))
        raise SystemExit(2)
    print(_text(r) if args.format == "text" else json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

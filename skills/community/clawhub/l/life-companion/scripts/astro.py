#!/usr/bin/env python3
"""
astro.py — REAL Western-astrology positions for a daily reading.

Honesty note: this computes ACTUAL astronomical positions (Swiss Ephemeris via
pyswisseph, offline Moshier mode — no data files, no network). The positions,
signs, retrogrades and aspect geometry it returns are *facts of the sky*; what any
of it "means" is a reflective/cultural lens, labeled as such by the reading — never
a scientific prediction. It fabricates nothing: if birth time is unknown, it omits
the Moon/rising rather than guessing.

Usage:
  python3 astro.py --date 1993-04-12 [--time 07:35] --on-date today --format json
  python3 astro.py --date 1993-04-12 --on-date 2026-07-18 --format text
"""
import argparse
import datetime
import json
import sys


import os
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deps import ensure as _ensure  # noqa: E402

swe = _ensure("pyswisseph", "swisseph")

SIGNS = ["白羊", "金牛", "双子", "巨蟹", "狮子", "处女",
         "天秤", "天蝎", "射手", "摩羯", "水瓶", "双鱼"]
SIGN_EN = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
           "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGN_ELEMENT = {  # 星座四元素 (reflective flavor)
    "白羊": "火", "狮子": "火", "射手": "火", "金牛": "土", "处女": "土", "摩羯": "土",
    "双子": "风", "天秤": "风", "水瓶": "风", "巨蟹": "水", "天蝎": "水", "双鱼": "水",
}
PLANETS = [("太阳", swe.SUN), ("月亮", swe.MOON), ("水星", swe.MERCURY),
           ("金星", swe.VENUS), ("火星", swe.MARS), ("木星", swe.JUPITER),
           ("土星", swe.SATURN)]
# Full natal set = the daily 7 + the outer 3 + the lunar nodes (reflective layer).
NATAL_PLANETS = PLANETS + [("天王星", swe.URANUS), ("海王星", swe.NEPTUNE),
                           ("冥王星", swe.PLUTO), ("北交点", swe.TRUE_NODE)]
ASPECTS = [(0, "合", 7), (60, "六合(和谐)", 5), (90, "刑(张力)", 6),
           (120, "拱(顺遂)", 6), (180, "冲(对立)", 7)]


def _sign(lon):
    return SIGNS[int(lon // 30) % 12]


def _jd(dt):
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)


def _lon_speed(jd, planet):
    r = swe.calc_ut(jd, planet)[0]
    return r[0] % 360.0, r[3]  # longitude, daily speed (neg = retrograde)


def _angle(a, b):
    d = abs((a - b) % 360.0)
    return min(d, 360 - d)


def compute(birth_date, birth_time, on_date, tz=None):
    """Daily reading. `tz` is the BIRTHPLACE zone (IANA name or offset hours).

    This used to take the birth wall clock as if it were UT while natal() correctly
    subtracted the offset, so the same profile could be told two different Sun signs
    by the two modes — 金牛 from the daily card and 白羊 from the natal chart. The
    daily entry point also accepted --tz and then ignored it.
    """
    by, bm, bd = (int(x) for x in birth_date.split("-"))
    hh, mm = ((int(x) for x in birth_time.split(":")) if birth_time else (12, 0))
    time_known = birth_time is not None
    caveats = []

    tz_offset, tz_note = _resolve_tz(tz, birth_date, birth_time)
    if tz_note:
        caveats.append(tz_note)
    if tz_offset is None:
        tz_offset = 0.0
        caveats.append("未提供出生地时区：出生钟点按 UT 处理，本命太阳/月亮的度数会有偏差"
                       "（最多约一个星座）。传 --tz（如 Asia/Shanghai）即可对齐。")
    natal_jd = swe.julday(by, bm, bd, hh + mm / 60.0 - float(tz_offset))
    sun_natal = _lon_speed(natal_jd, swe.SUN)[0]
    moon_natal = _lon_speed(natal_jd, swe.MOON)[0] if time_known else None
    if not time_known:
        caveats.append("出生时刻未知：本命月亮按当日 12:00 估算，月亮每天走 12–15°，"
                       "星座可能不对——本命月亮相关的解读请当作存疑。")

    # "Today" is a moment, not a day. The snapshot used to be a bare 12:00 UT with no
    # epoch stated, while the card said 「今日月亮在X座」 — the Moon crosses a sign
    # roughly every 2.5 days, so on a crossing day that label is a coin flip. Take the
    # snapshot at local noon for the person's own zone and SAY which instant it is.
    snap_hour = 12.0 - float(tz_offset)
    tjd = _jd(datetime.datetime(on_date.year, on_date.month, on_date.day, 12, 0)) \
        - 12.0 / 24.0 + snap_hour / 24.0
    today = {}
    for name, pl in PLANETS:
        lon, spd = _lon_speed(tjd, pl)
        today[name] = {"sign": _sign(lon), "lon": round(lon, 2),
                       "retrograde": spd < 0}

    # transits from fast movers to the natal Sun (and Moon if known)
    transits = []
    targets = [("本命太阳", sun_natal)]
    if moon_natal is not None:
        targets.append(("本命月亮", moon_natal))
    for tname, tlon in targets:
        for pname, pl in [("太阳", swe.SUN), ("月亮", swe.MOON), ("水星", swe.MERCURY),
                          ("金星", swe.VENUS), ("火星", swe.MARS)]:
            plon = _lon_speed(tjd, pl)[0]
            ang = _angle(plon, tlon)
            for deg, label, orb in ASPECTS:
                if abs(ang - deg) <= orb:
                    transits.append({"from": f"流{pname}", "to": tname,
                                     "aspect": label, "orb": round(abs(ang - deg), 1)})
                    break

    retros = [n for n in ("水星", "金星", "火星", "木星", "土星") if today[n]["retrograde"]]

    # Is the Moon near a sign boundary at the snapshot instant? Then "today's moon
    # sign" depends on the hour and must not be stated flatly.
    moon_lon = today["月亮"]["lon"]
    deg_in_sign = moon_lon % 30.0
    if deg_in_sign < 1.6 or deg_in_sign > 28.4:
        caveats.append(f"今日月亮在 {today['月亮']['sign']}座 {deg_in_sign:.1f}° —— 贴近换座边界，"
                       f"月亮一天走 12–15°，今天早晚可能不是同一个星座。别把它说死。")

    return {
        "system": "Western astrology (real ephemeris, Swiss/Moshier)",
        "date": on_date.isoformat(),
        "snapshot_at": (f"{on_date.isoformat()} 12:00 local (UT"
                        f"{-snap_hour + 12:+g}h offset applied)"),
        "tz": tz,
        "caveats": caveats,
        "sun_sign": _sign(sun_natal),
        "sun_sign_en": SIGN_EN[int(sun_natal // 30) % 12],
        "sun_element": SIGN_ELEMENT[_sign(sun_natal)],
        "moon_sign_natal": (_sign(moon_natal) if moon_natal is not None else None),
        "time_known": time_known,
        "today_moon_sign": today["月亮"]["sign"],
        "today_planets": today,
        "retrogrades": retros,
        "transits_to_natal": transits,
        "disclaimer": ("以上为真实天文位置(可复现的事实);星座/相位的『意义』是文化性的"
                       "反思视角,非科学预测。"),
    }


def _parse_tz(s):
    """Accept either a UTC offset in hours or an IANA zone name.

    The profile stores `birth.tz_at_birth`, and the natural thing to store there is a
    zone name ("Asia/Shanghai") — but this script used to take only a float, so the
    two halves of the skill disagreed and a natal chart just failed. Worse, asking for
    a raw offset pushes the *historical* DST question onto the model ("was Europe on
    summer time in July 1993?"), which is a guess dressed as a fact. A zone name lets
    zoneinfo answer it exactly, for the birth moment.
    """
    from _tz import parse_tz    # the one parser every chart script shares
    try:
        return parse_tz(s)      # validate now so the error is about --tz, not about JSON
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def _resolve_tz(tz, date_str, time_str):
    """Turn a zone name into the offset ACTUALLY in force at that birth moment.

    Returns (offset_hours, note) — the note records how it was resolved so the reply
    can be honest about it, e.g. a summer birth in Amsterdam being +2, not +1.
    """
    if tz is None or isinstance(tz, (int, float)):
        return (None if tz is None else float(tz)), None
    from zoneinfo import ZoneInfo
    y, m, d = (int(x) for x in date_str.split("-"))
    hh, mm = (int(x) for x in (time_str or "12:00").split(":"))
    zone = ZoneInfo(tz)
    naive = datetime.datetime(y, m, d, hh, mm)
    local = naive.replace(tzinfo=zone)
    off = local.utcoffset().total_seconds() / 3600.0

    # A wall clock is not a guarantee that the moment existed. On the spring-forward
    # night the clocks jump and an hour is simply skipped; on the autumn night an hour
    # runs twice. zoneinfo resolves both silently, so the chart used to be built on a
    # time that never happened — or on the wrong one of two — with no complaint.
    extra = None
    round_trip = local.astimezone(datetime.timezone.utc).astimezone(zone)
    if round_trip.replace(tzinfo=None) != naive:
        extra = (f"{date_str} {time_str} 在 {tz} 并不存在——那晚夏令时向前跳，这个钟点被"
                 f"跳过了。已按 UTC{off:+g} 处理，但出生时间本身需要向本人确认。")
    else:
        alt = naive.replace(tzinfo=zone, fold=1).utcoffset().total_seconds() / 3600.0
        if abs(alt - off) > 1e-9:
            extra = (f"{date_str} {time_str} 在 {tz} 出现了两次——那晚时钟回拨，同一个钟点"
                     f"走了两遍（UTC{off:+g} 与 UTC{alt:+g}）。已取前一次；差一小时会移动"
                     f"上升约 15°，请与本人确认是拨钟前还是拨钟后。")
    note = (f"tz {tz} resolved to UTC{off:+g} for {date_str} "
            f"{time_str or '(time unknown, assumed 12:00)'} — historical DST/zone "
            f"changes applied by zoneinfo, not guessed.")
    if extra:
        note += " " + extra
    if y < 1970:
        # Many platforms ship a "slim"/truncated tzdata that drops pre-1970 transitions
        # and answers with the modern rule instead. Don't present that as exact — an
        # hour of error moves the Ascendant by ~15°, i.e. often a whole sign.
        note += (" NOTE: this is a pre-1970 birth, and some systems' timezone database "
                 "omits transitions that old — treat the offset as likely-but-unverified "
                 "and say so; an hour of error shifts the Ascendant by roughly a sign.")
    return off, note


def natal(birth_date, birth_time=None, lat=None, lon=None, tz_offset=None):
    """Compute a REAL natal chart: planets-in-signs + natal aspects, and the
    Ascendant/houses ONLY when birth time + place + timezone are all known.

    Everything returned is astronomical fact; meaning is a reflective lens (labeled
    by the caller). It fabricates nothing — it omits, with a stated reason, any part
    that the person's birth data can't support:
      * `time_known=False`  -> no Ascendant/houses; the Moon is flagged approximate
        (it moves ~12-15°/day, so its sign can be wrong without a birth time).
      * `tz_offset` unknown -> birth time is treated as UT and flagged; fine for the
        slow planets' signs, unreliable for the Ascendant (which we then omit).
      * `lat`/`lon` unknown -> no houses/Ascendant (they are place-specific).

    tz_offset is hours east of UTC (e.g. +8 for China, +1 for NL winter). Returns a
    dict; `caveats` lists every honest limitation so the reading can state them.
    """
    by, bm, bd = (int(x) for x in birth_date.split("-"))
    time_known = birth_time is not None
    hh, mm = ((int(x) for x in birth_time.split(":")) if time_known else (12, 0))
    caveats = []
    # Local -> UT. Without tz we treat the clock time as UT (flagged below, after
    # `planets` exists — the Moon moves too fast to trust the sign without a real UT).
    no_tz_with_time = tz_offset is None and time_known
    if tz_offset is None:
        ut_hour = hh + mm / 60.0
    else:
        ut_hour = hh + mm / 60.0 - float(tz_offset)
    jd = swe.julday(by, bm, bd, ut_hour)

    planets = {}
    for name, pl in NATAL_PLANETS:
        lonp, spd = _lon_speed(jd, pl)
        entry = {"sign": _sign(lonp), "sign_en": SIGN_EN[int(lonp // 30) % 12],
                 "deg_in_sign": round(lonp % 30, 2), "lon": round(lonp, 2)}
        if name != "北交点":  # the node is always ~retrograde by nature; not a flag
            entry["retrograde"] = spd < 0
        planets[name] = entry
    if not time_known:
        planets["月亮"]["approximate"] = True
        caveats.append("未提供出生时间:月亮星座按当日正午估算,可能跨座;上升/宫位无法计算。"
                       "太阳及慢速行星星座一般不受影响。")
    elif no_tz_with_time:
        planets["月亮"]["approximate"] = True
        caveats.append("未提供出生地时区,出生时间按 UT 处理:太阳及慢速行星星座可靠,"
                       "但月亮(移动快)可能差一个星座、且上升/宫位不可靠(已省略)。"
                       "给出时区可修正。")

    # natal planet-planet aspects (major only), each pair once
    names = [n for n, _ in NATAL_PLANETS if n != "北交点"]
    aspects = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = planets[names[i]]["lon"], planets[names[j]]["lon"]
            ang = _angle(a, b)
            for deg, label, orb in ASPECTS:
                if abs(ang - deg) <= orb:
                    aspects.append({"a": names[i], "b": names[j], "aspect": label,
                                    "orb": round(abs(ang - deg), 1)})
                    break

    # Ascendant / houses: need time + place + a real UT (tz). Else omit honestly.
    ascendant = houses = midheaven = None
    if time_known and lat is not None and lon is not None and tz_offset is not None:
        try:
            cusps, ascmc = swe.houses(jd, float(lat), float(lon), b"P")  # Placidus
            asc_lon, mc_lon = ascmc[0] % 360.0, ascmc[1] % 360.0
            ascendant = {"sign": _sign(asc_lon), "sign_en": SIGN_EN[int(asc_lon // 30) % 12],
                         "deg_in_sign": round(asc_lon % 30, 2)}
            midheaven = {"sign": _sign(mc_lon), "deg_in_sign": round(mc_lon % 30, 2)}
            houses = [{"house": k + 1, "sign": _sign(c % 360.0),
                       "deg_in_sign": round((c % 360.0) % 30, 2)}
                      for k, c in enumerate(list(cusps)[:12])]
        except Exception as e:  # high-latitude Placidus failure etc. — omit, don't fake
            caveats.append(f"宫位计算失败({e});已省略上升/宫位,行星星座与相位不受影响。")
    elif time_known and (lat is None or lon is None):
        caveats.append("已知出生时间但缺出生地经纬度:上升/中天/宫位与地点相关,无法计算,已省略。")

    return {
        "system": "Western natal chart (real ephemeris, Swiss/Moshier)",
        "birth_date": birth_date,
        "birth_time": birth_time,
        "time_known": time_known,
        "tz_offset": tz_offset,
        "sun_sign": planets["太阳"]["sign"],
        "sun_sign_en": planets["太阳"]["sign_en"],
        "sun_element": SIGN_ELEMENT[planets["太阳"]["sign"]],
        "moon_sign": planets["月亮"]["sign"],
        "planets": planets,
        "aspects": aspects,
        "ascendant": ascendant,
        "midheaven": midheaven,
        "houses": houses,
        "caveats": caveats,
        "disclaimer": ("以上行星经度/星座/相位为真实天文事实(可复现);其『意义』是文化性的"
                       "反思视角,非科学预测,也非命运判定。"),
    }


def _natal_text(r):
    L = [f"本命盘 ({r['birth_date']}{' ' + r['birth_time'] if r['birth_time'] else ' 时间未知'})",
         f"  太阳 {r['sun_sign']}座 ({r['sun_element']}象) · 月亮 {r['moon_sign']}座"
         + ("(近似)" if r["planets"]["月亮"].get("approximate") else "")]
    if r["ascendant"]:
        L.append(f"  上升 {r['ascendant']['sign']}座 · 中天 {r['midheaven']['sign']}座")
    L.append("  行星落座:")
    for name in [n for n, _ in NATAL_PLANETS]:
        p = r["planets"][name]
        rx = "逆" if p.get("retrograde") else ""
        L.append(f"    {name}: {p['sign']}座 {p['deg_in_sign']}°{rx}")
    if r["aspects"]:
        L.append("  主要相位:")
        for a in r["aspects"][:8]:
            L.append(f"    {a['a']} {a['aspect']} {a['b']} (orb {a['orb']}°)")
    for c in r["caveats"]:
        L.append("  ⚠ " + c)
    L.append("\n" + r["disclaimer"])
    return "\n".join(L)


def _text(r):
    L = [f"星座: {r['sun_sign']}座 ({r['sun_sign_en']}, {r['sun_element']}象)"]
    L.append(f"今日({r['date']})月亮在 {r['today_moon_sign']}座")
    if r["retrogrades"]:
        L.append("逆行中: " + "、".join(x + "逆" for x in r["retrogrades"]))
    if r["transits_to_natal"]:
        L.append("今日对你本命的相位:")
        for t in r["transits_to_natal"][:5]:
            L.append(f"  {t['from']} {t['aspect']} {t['to']} (orb {t['orb']}°)")
    L.append("\n" + r["disclaimer"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="birth date YYYY-MM-DD")
    ap.add_argument("--time", default=None, help="birth time HH:MM (omit if unknown)")
    ap.add_argument("--on-date", default="today", help="daily mode: YYYY-MM-DD or 'today'")
    ap.add_argument("--natal", action="store_true",
                    help="compute the full natal chart instead of the daily reading")
    ap.add_argument("--lat", type=float, default=None, help="natal: birth latitude (for houses/ascendant)")
    ap.add_argument("--lon", type=float, default=None, help="natal: birth longitude (for houses/ascendant)")
    ap.add_argument("--tz", type=_parse_tz, default=None,
                    help="natal: birth-place timezone — either an IANA name (Asia/Shanghai, "
                         "Europe/Amsterdam; PREFERRED, historical DST resolved for you) or a "
                         "plain UTC offset in hours (8, 1, -5). Needed for the ascendant/houses.")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    from _tz import argv_with_offsets
    args = ap.parse_args(argv_with_offsets(("--tz",)))
    try:
        if args.natal:
            tz_hours, tz_note = _resolve_tz(args.tz, args.date, args.time)
            r = natal(args.date, args.time, lat=args.lat, lon=args.lon, tz_offset=tz_hours)
            if tz_note:
                r.setdefault("caveats", []).append(tz_note)
            print(_natal_text(r) if args.format == "text"
                  else json.dumps(r, ensure_ascii=False, indent=2))
            return
        on_date = (datetime.date.today() if args.on_date == "today"
                   else datetime.date.fromisoformat(args.on_date))
        # daily mode used to accept --tz and silently drop it
        r = compute(args.date, args.time, on_date, tz=args.tz)
    except (ValueError, TypeError) as e:
        print(json.dumps({"ok": False, "error": f"bad input: {e}"}, ensure_ascii=False))
        sys.exit(2)
    print(_text(r) if args.format == "text" else json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

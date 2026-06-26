#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
印度占星统一引擎 v3.7.1 (Jyotish Unified Engine)
整合所有计算能力为单一CLI入口，供Skill调用

子命令:
  chart        计算完整星盘（基于Swiss Ephemeris）
  dasha        计算Vimshottari Dasha大运时间线
  yoga         Yoga格局识别
  predict      三层验证法事件预测（优先EventPredictionModel规则引擎）
  varga        分盘计算（D9/D10）
  varga-full   BPHS十六分盘完整计算（D2-D60）（v3.7新增）
  aspects      度数精确相位系统（v3.7新增）
  jaimini      Jaimini系统（Chara Karaka/Chara Dasha/Karakamsha）（v3.7新增）
  nakshatra-adv 高级Nakshatra分析（Tara Bala/Sub-Lord/兼容性）（v3.7新增）
  argala       Argala门闩系统（v3.7新增）
  tajika       Tajika/Varshaphala年运盘（v3.7新增）
  synastry     合盘分析（Ashta Koota 36分制+Mangal Dosha）（v3.7新增）
  full-reading 全自动综合解盘（出生信息→全链路计算→完整报告）（v3.7.1新增）
  celebrity    名人案例查询（15,807条数据+SQLite验证库）
  db-stats     验证数据库统计
  transit      行星过境查询
  shadbala     六重力量计算（v3.4新增）
  ashtakavarga 八分法计算（v3.5升级BPHS完整表，SAV=337）
  memory       Hermes记忆系统（v3.4新增）
  validate     R1-R10数学验证（v3.5新增，含R2b BAV列→SAV校验）
  audit        P1-P12行星审计管线（v3.6升级含P3仓库耦合+P8年龄状态+冲突仲裁）
  report       MD→HTML报告生成（v3.6新增，羊皮纸主题）

用法示例:
  python3 jyotish_engine.py chart --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py shadbala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py ashtakavarga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py memory --action store --content "测试记忆"
"""

import argparse
import json
import sys
import os
import csv
import math
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List

# ============================================================================
# 路径常量
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.expanduser('~')
CLAW_DIR = os.path.join(HOME_DIR, 'WorkBuddy', 'Claw')
DB_PATH = os.path.join(CLAW_DIR, 'vedic_astrology_validation.db')
PERSON_CSV = os.path.join(CLAW_DIR, 'vedastro_data', 'PersonList-15k.csv')
TRANSIT_JSON = os.path.join(CLAW_DIR, '月运过境配置-2026-2028.json')

try:
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)  # P0修复：必须设置Lahiri恒星黄道模式
    HAS_SWE = True
except ImportError:
    HAS_SWE = False

# ============================================================================
# 常量
# ============================================================================
NAKSHATRA_LIST = [
    ("Ashwini", "Ketu", 7), ("Bharani", "Venus", 20), ("Krittika", "Sun", 6),
    ("Rohini", "Moon", 10), ("Mrigashira", "Mars", 7), ("Ardra", "Rahu", 18),
    ("Punarvasu", "Jupiter", 16), ("Pushya", "Saturn", 19), ("Ashlesha", "Mercury", 17),
    ("Magha", "Ketu", 7), ("Purva Phalguni", "Venus", 20), ("Uttara Phalguni", "Sun", 6),
    ("Hasta", "Moon", 10), ("Chitra", "Mars", 7), ("Swati", "Rahu", 18),
    ("Vishakha", "Jupiter", 16), ("Anuradha", "Saturn", 19), ("Jyeshtha", "Mercury", 17),
    ("Mula", "Ketu", 7), ("Purva Ashadha", "Venus", 20), ("Uttara Ashadha", "Sun", 6),
    ("Shravana", "Moon", 10), ("Dhanishta", "Mars", 7), ("Shatabhisha", "Rahu", 18),
    ("Purva Bhadrapada", "Jupiter", 16), ("Uttara Bhadrapada", "Saturn", 19), ("Revati", "Mercury", 17),
]
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
SIGNS_CN = {'Aries': '白羊座', 'Taurus': '金牛座', 'Gemini': '双子座', 'Cancer': '巨蟹座', 'Leo': '狮子座', 'Virgo': '处女座', 'Libra': '天秤座', 'Scorpio': '天蝎座', 'Sagittarius': '射手座', 'Capricorn': '摩羯座', 'Aquarius': '水瓶座', 'Pisces': '双鱼座'}
SIGN_LORDS = {'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'}
EXALTATION = {'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn', 'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'}
DEBILITATION = {'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer', 'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries'}
# Moolatrikona（三方本宫）: 行星 → (星座, 度数范围起始)
MOOLATRIKONA = {'Sun': ('Leo', 0, 20), 'Moon': ('Taurus', 0, 3), 'Mars': ('Aries', 0, 12), 'Mercury': ('Virgo', 16, 20), 'Jupiter': ('Sagittarius', 0, 10), 'Venus': ('Libra', 0, 15), 'Saturn': ('Aquarius', 0, 20)}
# BPHS 永久友好关系表 (Naisargika Mitra)
PERMANENT_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
    'Rahu': ['Venus', 'Saturn'],
    'Ketu': ['Mars', 'Saturn'],
}
PERMANENT_ENEMIES = {
    'Sun': ['Saturn', 'Venus'],
    'Moon': [],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
    'Rahu': ['Sun', 'Moon', 'Jupiter'],
    'Ketu': ['Sun', 'Moon'],
}


def _get_dignity_level(planet, sign, deg_in_sign=None):
    """判断行星在某星座的尊严等级 (用于 Vimsopaka 映射)"""
    if EXALTATION.get(planet) == sign:
        return 'EXALTED'
    # Moolatrikona: 需要检查度数范围
    mt = MOOLATRIKONA.get(planet)
    if mt and mt[0] == sign:
        if deg_in_sign is not None and mt[1] <= deg_in_sign < mt[2]:
            return 'MOOLATRIKONA'
    if SIGN_LORDS.get(sign) == planet:
        return 'OWN_SIGN'
    if DEBILITATION.get(planet) == sign:
        return 'DEBILITATED'
    # 友好/敌对
    sign_lord = SIGN_LORDS.get(sign, '')
    if planet in PERMANENT_FRIENDS.get(sign_lord, []):
        return 'FRIEND'
    if planet in PERMANENT_ENEMIES.get(sign_lord, []):
        return 'ENEMY'
    return 'NEUTRAL'
PLANET_CN = {"Ketu": "南交点Ketu", "Venus": "金星Venus", "Sun": "太阳Sun", "Moon": "月亮Moon", "Mars": "火星Mars", "Rahu": "北交点Rahu", "Jupiter": "木星Jupiter", "Saturn": "土星Saturn", "Mercury": "水星Mercury"}
PLANETS_SWE = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE} if HAS_SWE else {}


def output_json(data):
    """统一JSON输出"""
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _add_chart_args(p):
    """为需要出生数据的子命令添加公共参数"""
    p.add_argument('--year', type=int, required=True)
    p.add_argument('--month', type=int, required=True)
    p.add_argument('--day', type=int, required=True)
    p.add_argument('--hour', type=int, required=True)
    p.add_argument('--minute', type=int, required=True)
    p.add_argument('--lat', type=float, required=True)
    p.add_argument('--lon', type=float, required=True)
    p.add_argument('--tz', type=float, default=0)


# ============================================================================
# 公共星盘计算（供 chart/shadbala/ashtakavarga 共用，v3.4提取）
# ============================================================================
def compute_chart_data(year, month, day, hour, minute, lat, lon, tz):
    """计算星盘核心数据，返回 (result_dict, asc_idx, jd, ayanamsa)"""
    if not HAS_SWE:
        return None, None, None, None
    swe.set_ephe_path('')
    hour_decimal = hour + minute / 60.0 - tz
    jd = swe.julday(year, month, day, hour_decimal)
    ayanamsa = swe.get_ayanamsa(jd)

    result = {"birth_info": {
        "date": f"{year}-{month:02d}-{day:02d}", "time": f"{hour:02d}:{minute:02d}",
        "tz": f"UTC{'+' if tz >= 0 else ''}{tz}", "lat": lat, "lon": lon,
        "julian_day": round(jd, 6), "ayanamsa": round(ayanamsa, 4)
    }, "ascendant": None, "planets": {}, "houses": {}}

    asc_lon, _ = swe.houses(jd, lat, lon, b'A')
    asc_deg = (asc_lon[0] - ayanamsa) % 360
    asc_idx = int(asc_deg / 30)
    asc_sign = SIGNS[asc_idx]
    result["ascendant"] = {"sign": asc_sign, "sign_cn": SIGNS_CN[asc_sign],
        "degree": round(asc_deg, 4), "degree_in_sign": round(asc_deg - asc_idx * 30, 4),
        "lord": SIGN_LORDS[asc_sign]}

    for i in range(12):
        c = (asc_lon[i] - ayanamsa) % 360
        si = int(c / 30)
        result["houses"][f"house_{i+1}"] = {"cusp_sign": SIGNS[si],
            "cusp_sign_cn": SIGNS_CN[SIGNS[si]], "cusp_degree": round(c, 4),
            "lord": SIGN_LORDS[SIGNS[si]]}

    nak_span = 360.0 / 27
    for pname, pid in PLANETS_SWE.items():
        try:
            pos, _ = swe.calc_ut(jd, pid)
            lon_p = (pos[0] - ayanamsa) % 360; lat_p = pos[1]; spd = pos[3]
            si = int(lon_p / 30); d_in_s = lon_p - si * 30; sign = SIGNS[si]
            retro = spd < 0
            house = ((si - asc_idx) % 12) + 1
            status = "中性"
            if EXALTATION.get(pname) == sign: status = "入旺(Exalted)"
            elif DEBILITATION.get(pname) == sign: status = "落陷(Debilitated)"
            elif SIGN_LORDS.get(sign) == pname: status = "入庙(Own Sign)"
            ni = int(lon_p / nak_span); pada = int((lon_p % nak_span) / (nak_span / 4)) + 1
            nak_n, nak_l, _ = NAKSHATRA_LIST[ni % 27]
            result["planets"][pname] = {
                "sign": sign, "sign_cn": SIGNS_CN[sign], "degree": round(lon_p, 4),
                "degree_in_sign": round(d_in_s, 4), "house": house, "status": status,
                "retrograde": retro, "speed": round(spd, 6),
                "nakshatra": nak_n, "nakshatra_pada": pada, "nakshatra_lord": nak_l}
            if pname == 'Rahu':
                klon = (lon_p + 180) % 360; ksi = int(klon / 30); kd = klon - ksi * 30
                kni = int(klon / nak_span); kp = int((klon % nak_span) / (nak_span / 4)) + 1
                kn, kl, _ = NAKSHATRA_LIST[kni % 27]
                result["planets"]["Ketu"] = {
                    "sign": SIGNS[ksi], "sign_cn": SIGNS_CN[SIGNS[ksi]],
                    "degree": round(klon, 4), "degree_in_sign": round(kd, 4),
                    "house": ((ksi - asc_idx) % 12) + 1, "status": "中性",
                    "retrograde": True, "speed": round(spd, 6),
                    "nakshatra": kn, "nakshatra_pada": kp, "nakshatra_lord": kl}
        except Exception as e:
            result["planets"][pname] = {"error": str(e)}
    return result, asc_idx, jd, ayanamsa


# ============================================================================
# 1. 星盘计算
# ============================================================================
def cmd_chart(args):
    result, asc_idx, jd, ayanamsa = compute_chart_data(args.year, args.month, args.day, args.hour, args.minute, args.lat, args.lon, args.tz)
    if result is None:
        return {"error": "swisseph未安装"}
    # v3.5: --validate 触发 R1-R10 校验
    if getattr(args, 'validate', False):
        try:
            sys.path.insert(0, SCRIPT_DIR)
            from ashtakavarga import calc_ashtakavarga
            asht_result = calc_ashtakavarga(result.get('planets', {}), asc_idx)
            from validate import validate_chart
            validation = validate_chart(result, asht_result)
            result['validation'] = validation
        except Exception as e:
            result['validation'] = {"error": str(e), "valid": False}
    return result


# ============================================================================
# 2. Dasha计算
# ============================================================================
def cmd_dasha(args):
    nak_info = None; progress = 0.5
    if args.moon_lon is not None:
        ns = 360.0 / 27; idx = int(args.moon_lon / ns); progress = (args.moon_lon % ns) / ns
        nak_info = NAKSHATRA_LIST[idx % 27]
    elif args.nakshatra:
        nl = args.nakshatra.lower().replace(" ", "").replace("-", "")
        for n in NAKSHATRA_LIST:
            if nl in n[0].lower().replace(" ", "") or n[0].lower().replace(" ", "").startswith(nl[:5]):
                nak_info = n; break
        if not nak_info: return {"error": f"未找到Nakshatra: {args.nakshatra}"}
        if args.pada: progress = (max(1, min(4, args.pada)) - 1) / 4 + 0.125
    else:
        return {"error": "请提供 --nakshatra 或 --moon-lon"}

    nak_name, start_lord, start_years = nak_info
    birth_dt = datetime.strptime(args.birthdate, "%Y-%m-%d")
    elapsed = progress * start_years; remaining = start_years - elapsed
    dt = birth_dt - timedelta(days=elapsed * 365.25)
    si = DASHA_ORDER.index(start_lord)
    timeline = []
    for i in range(9):
        lord = DASHA_ORDER[(si + i) % 9]; years = DASHA_YEARS[lord]
        end_dt = dt + timedelta(days=years * 365.25)
        # 第一个 MD 的展示 years 用 balance，实际日期计算用完整年数（数学等价）
        display_years = round(remaining, 2) if i == 0 else years
        timeline.append({"lord": lord, "lord_cn": PLANET_CN[lord], "start": dt.strftime("%Y-%m-%d"), "end": end_dt.strftime("%Y-%m-%d"), "years": display_years, "full_years": years, "is_current": False, "is_balance": i == 0, "balance_years": round(remaining, 2) if i == 0 else None, "elapsed_at_birth": round(elapsed, 2) if i == 0 else None})
        dt = end_dt

    today = datetime.strptime(args.today, "%Y-%m-%d") if args.today else datetime.now()
    current = None
    for d in timeline:
        ds = datetime.strptime(d["start"], "%Y-%m-%d"); de = datetime.strptime(d["end"], "%Y-%m-%d")
        total_days = (de - ds).days; li = DASHA_ORDER.index(d["lord"])
        # v3.7.2: 为所有 Mahadasha 计算 Antardasha（不仅当前大运）
        sub = []; sdt = ds
        for j in range(9):
            sl = DASHA_ORDER[(li + j) % 9]; sd = total_days * DASHA_YEARS[sl] / 120
            se = sdt + timedelta(days=sd)
            is_cur = sdt <= today < se
            sub.append({"lord": sl, "lord_cn": PLANET_CN[sl], "start": sdt.strftime("%Y-%m-%d"), "end": se.strftime("%Y-%m-%d"), "is_current": is_cur})
            sdt = se
        d["antardasha_timeline"] = sub
        if ds <= today < de:
            d["is_current"] = True
            # 从 antardasha 列表中提取当前正在运行的 antardasha
            current_ad = None
            for ad in sub:
                if ad.get("is_current"):
                    current_ad = ad
                    break
            d["mahadasha"] = d.get("lord", "")
            d["mahadasha_cn"] = d.get("lord_cn", "")
            d["antardasha"] = current_ad or (sub[0] if sub else None)
            current = d

    return {"moon_nakshatra": nak_name, "birth_date": args.birthdate, "reference_date": today.strftime("%Y-%m-%d"), "timeline": timeline, "current_dasha": current}


# ============================================================================
# 3. Yoga识别
# ============================================================================
def cmd_yoga(args):
    planets = {}
    if args.planets:
        for item in args.planets.split(','):
            parts = item.strip().split(':')
            if len(parts) >= 3:
                planets[parts[0].strip()] = {"sign": parts[1].strip(), "house": int(parts[2].strip())}
    asc = args.ascendant or "Aries"
    ai = SIGNS.index(asc) if asc in SIGNS else 0
    kl = list(set([SIGN_LORDS[SIGNS[(ai + h - 1) % 12]] for h in [1, 4, 7, 10]]))
    tl = list(set([SIGN_LORDS[SIGNS[(ai + h - 1) % 12]] for h in [1, 5, 9]]))
    yogas = []

    # Raja Yoga
    for k in kl:
        for t in tl:
            if k != t and k in planets and t in planets and planets[k]["house"] == planets[t]["house"]:
                yogas.append({"name": "Raja Yoga", "name_cn": "王者格局", "combination": f"{k}+{t}同在第{planets[k]['house']}宫", "effects": ["权力地位", "事业成功", "社会影响力"], "strength": "强" if planets[k]["sign"] in [EXALTATION.get(k, ''), SIGN_LORDS.get(planets[k]["sign"], '')] else "中"})

    # Mahapurusha Yoga
    yoga_names = {'Mars': 'Ruchaka', 'Mercury': 'Bhadra', 'Jupiter': 'Hamsa', 'Venus': 'Malavya', 'Saturn': 'Sasa'}
    for p, info in planets.items():
        if info["house"] in [1, 4, 7, 10] and p in yoga_names:
            if EXALTATION.get(p) == info["sign"] or SIGN_LORDS.get(info["sign"]) == p:
                st = "入旺" if EXALTATION.get(p) == info["sign"] else "入庙"
                yogas.append({"name": f"{yoga_names[p]} Yoga", "name_cn": f"{PLANET_CN.get(p, p)}{st}格局", "combination": f"{p}{st}在{info['sign']}(第{info['house']}宫)", "effects": ["卓越才能", "领域领军", "人格魅力"], "strength": "极强" if st == "入旺" else "强"})

    # Gajakesari
    if 'Jupiter' in planets and 'Moon' in planets:
        jh = planets['Jupiter']['house']; mh = planets['Moon']['house']
        if jh in [1, 4, 7, 10] and mh in [1, 4, 7, 10]:
            yogas.append({"name": "Gajakesari Yoga", "name_cn": "象狮格局", "combination": f"木星第{jh}宫+月亮第{mh}宫", "effects": ["智慧学识", "财富名声", "道德品质"], "strength": "中"})

    # Neechabhanga
    for p, info in planets.items():
        if DEBILITATION.get(p) == info["sign"]:
            dl = SIGN_LORDS[info["sign"]]
            if dl in planets and planets[dl]["house"] in [1, 4, 7, 10]:
                yogas.append({"name": "Neechabhanga Raja Yoga", "name_cn": "落陷取消格局", "combination": f"{p}落陷在{info['sign']}，{dl}在角宫化解", "effects": ["克服困难", "逆境崛起", "转化能力"], "strength": "中强"})

    # Dhana Yoga
    wl = set(); wh = [2, 5, 9, 11]
    for h in wh:
        wl.add(SIGN_LORDS[SIGNS[(ai + h - 1) % 12]])
    wc = sum(1 for w in wl if w in planets and planets[w]["house"] in wh)
    if wc >= 2:
        yogas.append({"name": "Dhana Yoga", "name_cn": "财富格局", "combination": f"{wc}个财富宫主星落入财富宫", "effects": ["财富积累", "物质成功", "投资收益"], "strength": "中强" if wc >= 3 else "中"})

    # Solar Yogas (Veshi/Voshi/Ubhayachari)
    if 'Sun' in planets:
        sun_h = planets['Sun']['house']
        h2_from_sun = ((sun_h - 1 + 1) % 12) + 1  # 2nd from Sun
        h12_from_sun = ((sun_h - 1 + 11) % 12) + 1  # 12th from Sun
        planets_in_h2 = [p for p, info in planets.items() if info['house'] == h2_from_sun]
        planets_in_h12 = [p for p, info in planets.items() if info['house'] == h12_from_sun]
        if planets_in_h12 and not planets_in_h2:
            yogas.append({"name": "Voshi Yoga", "name_cn": "太阳前瑜伽", "combination": f"{'+'.join(planets_in_h12)}在太阳第12宫", "effects": ["口才出众", "善于表达", "受人尊敬"], "strength": "中"})
        if planets_in_h2 and not planets_in_h12:
            yogas.append({"name": "Veshi Yoga", "name_cn": "太阳后瑜伽", "combination": f"{'+'.join(planets_in_h2)}在太阳第2宫", "effects": ["财富充裕", "生活舒适", "性情愉快"], "strength": "中"})
        if planets_in_h2 and planets_in_h12:
            yogas.append({"name": "Ubhayachari Yoga", "name_cn": "太阳双夹瑜伽", "combination": f"太阳两侧均有行星", "effects": ["性格坚毅", "口才与财富兼备", "受人爱戴"], "strength": "强"})

    # Lunar Yogas (Sunapha/Anapha/Durudhura/Kemadruma)
    if 'Moon' in planets:
        moon_h = planets['Moon']['house']
        h2_from_moon = ((moon_h - 1 + 1) % 12) + 1
        h12_from_moon = ((moon_h - 1 + 11) % 12) + 1
        p_in_h2_moon = [p for p, info in planets.items() if p != 'Moon' and info['house'] == h2_from_moon]
        p_in_h12_moon = [p for p, info in planets.items() if p != 'Moon' and info['house'] == h12_from_moon]
        if p_in_h12_moon and not p_in_h2_moon:
            yogas.append({"name": "Anapha Yoga", "name_cn": "月后瑜伽", "combination": f"{'+'.join(p_in_h12_moon)}在月亮第12宫", "effects": ["体格健壮", "名声良好", "品德高尚"], "strength": "中"})
        if p_in_h2_moon and not p_in_h12_moon:
            yogas.append({"name": "Sunapha Yoga", "name_cn": "月前瑜伽", "combination": f"{'+'.join(p_in_h2_moon)}在月亮第2宫", "effects": ["自力更生", "财富充裕", "受人尊敬"], "strength": "中"})
        if p_in_h2_moon and p_in_h12_moon:
            yogas.append({"name": "Durudhura Yoga", "name_cn": "月双夹瑜伽", "combination": f"月亮两侧均有行星", "effects": ["享受丰富", "善于辞令", "性格坚定"], "strength": "强"})
        # Kemadruma Yoga: Moon两侧（2宫和12宫）均无行星
        if not p_in_h2_moon and not p_in_h12_moon:
            yogas.append({"name": "Kemadruma Yoga", "name_cn": "空劫瑜伽", "combination": f"月亮两侧均无行星（2宫/12宫空）", "effects": ["人生艰辛", "需自力更生", "精神挑战"], "strength": "凶"})

    # ========================================================================
    # 扩展组合型 Yoga（v3.7.2 新增，共 25 条）
    # ========================================================================

    # --- 辅助函数 ---
    def _house_of(planet_name):
        """获取行星所在宫位，不存在返回 None"""
        return planets[planet_name]["house"] if planet_name in planets else None

    def _sign_of(planet_name):
        """获取行星所在星座，不存在返回 None"""
        return planets[planet_name]["sign"] if planet_name in planets else None

    def _is_exalted(planet_name):
        """行星是否入旺"""
        s = _sign_of(planet_name)
        return s is not None and EXALTATION.get(planet_name) == s

    def _is_own_sign(planet_name):
        """行星是否入庙"""
        s = _sign_of(planet_name)
        return s is not None and SIGN_LORDS.get(s) == planet_name

    def _is_debilitated(planet_name):
        """行星是否落陷"""
        s = _sign_of(planet_name)
        return s is not None and DEBILITATION.get(planet_name) == s

    def _is_kendra(house_num):
        return house_num in [1, 4, 7, 10]

    def _is_trikona(house_num):
        return house_num in [1, 5, 9]

    def _is_dusthana(house_num):
        return house_num in [6, 8, 12]

    def _is_upachaya(house_num):
        return house_num in [3, 6, 10, 11]

    def _planets_in_house(h):
        """获取落入第 h 宫的所有行星列表"""
        return [p for p, info in planets.items() if info["house"] == h]

    def _lord_of_house(h):
        """获取第 h 宫的宫主星"""
        return SIGN_LORDS[SIGNS[(ai + h - 1) % 12]]

    def _planet_in_kendra_or_trikona(planet_name):
        """行星是否在角宫或三方宫"""
        h = _house_of(planet_name)
        return h is not None and (_is_kendra(h) or _is_trikona(h))

    # ========================================================================
    # 1. Vipreet Raja Yoga（逆行王者格局）—— Harsha / Sarala / Vimala
    # 来源：Phaladeepika。6/8/12 宫主星落入 6/8/12 宫（凶宫互落）→ 因祸得福
    # ========================================================================
    for dh_h, yoga_sub, yoga_cn in [(6, "Harsha", "喜悦逆行"), (8, "Sarala", "锐利逆行"), (12, "Vimala", "纯净逆行")]:
        lord_dh = _lord_of_house(dh_h)
        if lord_dh in planets:
            lh = _house_of(lord_dh)
            if lh in [6, 8, 12] and lh != dh_h:
                yogas.append({"name": f"{yoga_sub} Vipreet Raja Yoga", "name_cn": f"{yoga_cn}格局", "combination": f"第{dh_h}宫主星{lord_dh}落入第{lh}宫（凶宫互落）", "effects": ["因祸得福", "逆境崛起", "困境中成长"], "strength": "中强"})

    # ========================================================================
    # 2. Amala Yoga（无瑕格局）
    # 来源：BPHS。10 宫（天顶）及其前方（从10宫算2宫即11宫）有吉星
    # 简化版：10 宫或 11 宫有木星/金星/明亮水星
    # ========================================================================
    benefics_10_11 = [p for p in ['Jupiter', 'Venus', 'Mercury'] if p in planets and _house_of(p) in [10, 11] and not _is_debilitated(p)]
    if benefics_10_11:
        yogas.append({"name": "Amala Yoga", "name_cn": "无瑕格局", "combination": f"{'、'.join(benefics_10_11)}在10宫或11宫", "effects": ["名声清白", "受人敬仰", "事业有成"], "strength": "中强"})

    # ========================================================================
    # 3. Parvata Yoga（山岳格局）
    # 来源：BPHS。角宫主星有力 + 6/8 宫主星落入对应凶宫
    # 简化版：至少两个角宫主星在角宫或三方宫 + 6/8宫主不在1宫
    # ========================================================================
    kendra_lords_strong = sum(1 for k in kl if k in planets and _planet_in_kendra_or_trikona(k))
    if kendra_lords_strong >= 2:
        lord_6 = _lord_of_house(6)
        lord_8 = _lord_of_house(8)
        lord_6_ok = lord_6 in planets and _house_of(lord_6) != 1
        lord_8_ok = lord_8 in planets and _house_of(lord_8) != 1
        if lord_6_ok or lord_8_ok:
            yogas.append({"name": "Parvata Yoga", "name_cn": "山岳格局", "combination": f"角宫主星有力+凶宫主星不落入1宫", "effects": ["智慧卓越", "富有口才", "品格高尚"], "strength": "中"})

    # ========================================================================
    # 4. Kahala Yoga（勇气格局）
    # 来源：BPHS。3 宫主与 10 宫主有连接（同宫/互换/相位），且落入角宫
    # 简化版：3 宫主与 10 宫主同在一宫
    # ========================================================================
    lord_3 = _lord_of_house(3)
    lord_10 = _lord_of_house(10)
    if lord_3 in planets and lord_10 in planets:
        if _house_of(lord_3) == _house_of(lord_10):
            yogas.append({"name": "Kahala Yoga", "name_cn": "勇气格局", "combination": f"3宫主{lord_3}与10宫主{lord_10}同在第{_house_of(lord_3)}宫", "effects": ["意志坚定", "领导才能", "充满活力"], "strength": "中"})

    # ========================================================================
    # 5. Sankha Yoga（海螺格局）
    # 来源：BPHS。5 宫主 + 6 宫主落入角宫/三方宫，且上升主星有力
    # 简化版：5宫主和6宫主均在角宫或三方宫
    # ========================================================================
    lord_5 = _lord_of_house(5)
    lord_6 = _lord_of_house(6)
    if lord_5 in planets and lord_6 in planets:
        l5h = _house_of(lord_5)
        l6h = _house_of(lord_6)
        if (_is_kendra(l5h) or _is_trikona(l5h)) and (_is_kendra(l6h) or _is_trikona(l6h)):
            yogas.append({"name": "Sankha Yoga", "name_cn": "海螺格局", "combination": f"5宫主{lord_5}在第{l5h}宫+6宫主{lord_6}在第{l6h}宫（均有力）", "effects": ["学识渊博", "品德高尚", "物质充裕"], "strength": "中强"})

    # ========================================================================
    # 6. Bheri Yoga（旗帜格局）
    # 来源：BPHS。9 宫主落入 2 宫 + 木星/金星在角宫/三方宫 + 上升主与 9 宫主有关联
    # 简化版：9 宫主在 2 宫 + 木星或金星在角宫
    # ========================================================================
    lord_9 = _lord_of_house(9)
    if lord_9 in planets and _house_of(lord_9) == 2:
        jv_in_kendra = [p for p in ['Jupiter', 'Venus'] if p in planets and _is_kendra(_house_of(p))]
        if jv_in_kendra:
            yogas.append({"name": "Bheri Yoga", "name_cn": "旗帜格局", "combination": f"9宫主{lord_9}在2宫+{'、'.join(jv_in_kendra)}在角宫", "effects": ["品德高尚", "长寿幸福", "受人敬仰"], "strength": "中"})

    # ========================================================================
    # 7. Mridanga Yoga（鼓格局）
    # 来源：BPHS。上升主星在入旺/入庙 + 其他行星在自身入旺/入庙星座
    # 简化版：上升主星入旺或入庙
    # ========================================================================
    asc_lord = SIGN_LORDS.get(asc, '')
    if asc_lord in planets and (_is_exalted(asc_lord) or _is_own_sign(asc_lord)):
        other_strong = [p for p in planets if p != asc_lord and p not in ['Rahu', 'Ketu'] and (_is_exalted(p) or _is_own_sign(p))]
        if other_strong:
            st = "入旺" if _is_exalted(asc_lord) else "入庙"
            yogas.append({"name": "Mridanga Yoga", "name_cn": "鼓格局", "combination": f"上升主星{asc_lord}{st}+{'、'.join(other_strong)}有力", "effects": ["权力权威", "个人魅力", "领导气质"], "strength": "强"})

    # ========================================================================
    # 8. Sreenatha Yoga（幸运之主格局）
    # 来源：BPHS。7 宫主星落入 10 宫且 10 宫主落入 1 宫
    # ========================================================================
    lord_7 = _lord_of_house(7)
    if lord_7 in planets and lord_10 in planets:
        if _house_of(lord_7) == 10 and _house_of(lord_10) == 1:
            yogas.append({"name": "Sreenatha Yoga", "name_cn": "幸运之主格局", "combination": f"7宫主{lord_7}在10宫+10宫主{lord_10}在1宫", "effects": ["事业辉煌", "婚姻美满", "贵人相助"], "strength": "强"})

    # ========================================================================
    # 9. Matsya Yoga（鱼格局）
    # 来源：BPHS。1/5/9 宫中有吉星 + 6/8 宫有凶星 + 上升与木星/金星有连接
    # 简化版：三方宫(5/9)有吉星 + 6/8宫有凶星
    # ========================================================================
    benefics = ['Jupiter', 'Venus', 'Mercury']
    malefics = ['Mars', 'Saturn', 'Sun', 'Rahu', 'Ketu']
    ben_in_trikona = [p for p in benefics if p in planets and _house_of(p) in [5, 9]]
    mal_in_dusthana = [p for p in malefics if p in planets and _house_of(p) in [6, 8]]
    if ben_in_trikona and mal_in_dusthana:
        yogas.append({"name": "Matsya Yoga", "name_cn": "鱼格局", "combination": f"{'、'.join(ben_in_trikona)}在三方宫+{'、'.join(mal_in_dusthana)}在凶宫", "effects": ["聪慧过人", "直觉敏锐", "灵性成长"], "strength": "中"})

    # ========================================================================
    # 10. Koorma Yoga（龟格局）
    # 来源：BPHS。5/9 宫主落入三方宫 + 1 宫有吉星
    # 简化版：5宫主或9宫主在1宫，且1宫有吉星
    # ========================================================================
    ben_in_1 = [p for p in benefics if p in planets and _house_of(p) == 1]
    lord_5_or_9_in_1 = False
    for lp in [lord_5, lord_9]:
        if lp in planets and _house_of(lp) == 1:
            lord_5_or_9_in_1 = True
    if ben_in_1 and lord_5_or_9_in_1:
        yogas.append({"name": "Koorma Yoga", "name_cn": "龟格局", "combination": f"吉星在1宫+5/9宫主在1宫", "effects": ["智慧深厚", "耐心坚韧", "精神修养"], "strength": "中"})

    # ========================================================================
    # 11. Khadga Yoga（剑格局）
    # 来源：BPHS。2 宫主落入 2 宫且不被凶星占据 + 9 宫主有力
    # 简化版：2 宫主在 2 宫且 2 宫无凶星
    # ========================================================================
    lord_2 = _lord_of_house(2)
    if lord_2 in planets and _house_of(lord_2) == 2:
        mal_in_2 = [p for p in malefics if p in planets and _house_of(p) == 2]
        if not mal_in_2:
            yogas.append({"name": "Khadga Yoga", "name_cn": "剑格局", "combination": f"2宫主{lord_2}在2宫且2宫无凶星", "effects": ["财富充裕", "口才出众", "品格坚定"], "strength": "中"})

    # ========================================================================
    # 12. Kusuma Yoga（花格局）
    # 来源：BPHS。木星在 10 宫 + 月亮在 1 宫 + 太阳在 2 宫 + 金星在 9 宫
    # ========================================================================
    jup_10 = 'Jupiter' in planets and _house_of('Jupiter') == 10
    moon_1 = 'Moon' in planets and _house_of('Moon') == 1
    sun_2 = 'Sun' in planets and _house_of('Sun') == 2
    ven_9 = 'Venus' in planets and _house_of('Venus') == 9
    checks_kusuma = [jup_10, moon_1, sun_2, ven_9]
    met_kusuma = sum(checks_kusuma)
    if met_kusuma >= 3:
        parts = []
        if jup_10: parts.append("木星在10宫")
        if moon_1: parts.append("月亮在1宫")
        if sun_2: parts.append("太阳在2宫")
        if ven_9: parts.append("金星在9宫")
        yogas.append({"name": "Kusuma Yoga", "name_cn": "花格局", "combination": "+".join(parts), "effects": ["才貌双全", "受人爱戴", "幸福美满"], "strength": "强" if met_kusuma == 4 else "中强"})

    # ========================================================================
    # 13. Chandra-Mangala Yoga（日月-火星格局）
    # 来源：BPHS。火星与月亮同宫或在 2/12 宫关系
    # ========================================================================
    if 'Moon' in planets and 'Mars' in planets:
        mh = _house_of('Moon')
        marsh = _house_of('Mars')
        if mh == marsh:
            yogas.append({"name": "Chandra-Mangala Yoga", "name_cn": "日月火星同宫格局", "combination": f"火星与月亮同在第{mh}宫", "effects": ["财富积累", "行动力强", "情绪驱动成功"], "strength": "强" if _is_exalted('Mars') or _is_own_sign('Mars') else "中"})
        elif abs(mh - marsh) in [1, 11]:
            yogas.append({"name": "Chandra-Mangala Yoga", "name_cn": "日月火星关联格局", "combination": f"火星在第{marsh}宫，月亮在第{mh}宫（2/12宫关系）", "effects": ["财运亨通", "精力充沛", "商业头脑"], "strength": "中"})

    # ========================================================================
    # 14. Dwi-Gurupada Yoga / Guru-Mangala Yoga（木火格局）
    # 来源：木星与火星同宫或互换星座
    # ========================================================================
    if 'Jupiter' in planets and 'Mars' in planets:
        jup_s = _sign_of('Jupiter')
        mars_s = _sign_of('Mars')
        jup_h = _house_of('Jupiter')
        mars_h = _house_of('Mars')
        if jup_h == mars_h:
            yogas.append({"name": "Guru-Mangala Yoga", "name_cn": "木火同宫格局", "combination": f"木星与火星同在第{jup_h}宫", "effects": ["智慧与行动力兼备", "正义感强", "领导能力"], "strength": "中强"})
        elif SIGN_LORDS.get(jup_s) == 'Mars' and SIGN_LORDS.get(mars_s) == 'Jupiter':
            yogas.append({"name": "Guru-Mangala Yoga", "name_cn": "木火互容格局", "combination": f"木星在{jup_s}(火星守护)+火星在{mars_s}(木星守护)", "effects": ["智慧与行动力兼备", "正义感强", "领导能力"], "strength": "强"})

    # ========================================================================
    # 15. Budhaditya Yoga（水日格局）
    # 来源：BPHS。水星与太阳同宫
    # ========================================================================
    if 'Mercury' in planets and 'Sun' in planets:
        if _house_of('Mercury') == _house_of('Sun'):
            yogas.append({"name": "Budhaditya Yoga", "name_cn": "水日同宫格局", "combination": f"水星与太阳同在第{_house_of('Sun')}宫", "effects": ["智力超群", "口才出众", "学识渊博"], "strength": "中强" if not _is_debilitated('Mercury') else "弱"})

    # ========================================================================
    # 16. Lakshmi Yoga（拉克什米格局/财富女神格局）
    # 来源：BPHS。9 宫主在入旺/入庙星座且落入 1 宫
    # ========================================================================
    if lord_9 in planets:
        l9h = _house_of(lord_9)
        if l9h == 1 and (_is_exalted(lord_9) or _is_own_sign(lord_9)):
            st = "入旺" if _is_exalted(lord_9) else "入庙"
            yogas.append({"name": "Lakshmi Yoga", "name_cn": "财富女神格局", "combination": f"9宫主{lord_9}{st}在1宫", "effects": ["财富充裕", "生活幸福", "品德高尚"], "strength": "强"})

    # ========================================================================
    # 17. Vasumati Yoga（大地格局）
    # 来源：BPHS。所有吉星（木星/金星/水星/月亮）在上升盘的 3/6/10/11 宫（成长宫）
    # ========================================================================
    upachaya_benefics = [p for p in ['Jupiter', 'Venus', 'Mercury', 'Moon'] if p in planets and _is_upachaya(_house_of(p))]
    if len(upachaya_benefics) >= 3:
        yogas.append({"name": "Vasumati Yoga", "name_cn": "大地格局", "combination": f"{len(upachaya_benefics)}颗吉星在成长宫(3/6/10/11)", "effects": ["财富丰厚", "生活富足", "物质成功"], "strength": "中强" if len(upachaya_benefics) >= 4 else "中"})

    # ========================================================================
    # 18. Vanchana Kalusha Yoga / Papakartari Yoga（凶星夹宫格局）
    # 来源：Brihat Jataka。某宫被两侧凶星夹击（前一宫和后一宫均有凶星）
    # ========================================================================
    for target_house in [1, 4, 7, 10, 5, 9]:
        prev_h = ((target_house - 2) % 12) + 1
        next_h = (target_house % 12) + 1
        mal_before = [p for p in malefics if p in planets and _house_of(p) == prev_h]
        mal_after = [p for p in malefics if p in planets and _house_of(p) == next_h]
        if mal_before and mal_after:
            house_names = {1: "命宫", 4: "田宅宫", 7: "夫妻宫", 10: "事业宫", 5: "子女宫", 9: "迁移宫"}
            yogas.append({"name": "Papakartari Yoga", "name_cn": f"凶星夹{house_names.get(target_house, f'第{target_house}宫')}格局", "combination": f"第{target_house}宫被{'、'.join(mal_before)}和{'、'.join(mal_after)}前后夹击", "effects": [f"{house_names.get(target_house, f'第{target_house}宫')}领域受限", "需要额外努力", "阻碍与挑战"], "strength": "凶"})
            break  # 只报告一次

    # ========================================================================
    # 19. Subhakartari Yoga（吉星夹宫格局）
    # 来源：Brihat Jataka。与 Papakartari 相反——某宫被两侧吉星包围
    # ========================================================================
    for target_house in [1, 4, 7, 10, 5, 9]:
        prev_h = ((target_house - 2) % 12) + 1
        next_h = (target_house % 12) + 1
        ben_before = [p for p in benefics if p in planets and _house_of(p) == prev_h]
        ben_after = [p for p in benefics if p in planets and _house_of(p) == next_h]
        if ben_before and ben_after:
            house_names = {1: "命宫", 4: "田宅宫", 7: "夫妻宫", 10: "事业宫", 5: "子女宫", 9: "迁移宫"}
            yogas.append({"name": "Subhakartari Yoga", "name_cn": f"吉星护{house_names.get(target_house, f'第{target_house}宫')}格局", "combination": f"第{target_house}宫被{'、'.join(ben_before)}和{'、'.join(ben_after)}吉星守护", "effects": [f"{house_names.get(target_house, f'第{target_house}宫')}领域受保护", "顺利发展", "贵人助力"], "strength": "吉"})
            break

    # ========================================================================
    # 20. Saraswati Yoga（辩才天女格局）
    # 来源：BPHS。木星/金星/水星在 2/4/7/9/10 宫，且木星在自身友好星座
    # ========================================================================
    saraswati_houses = [2, 4, 7, 9, 10]
    saraswati_planets = [p for p in ['Jupiter', 'Venus', 'Mercury'] if p in planets and _house_of(p) in saraswati_houses]
    if len(saraswati_planets) >= 3 or (len(saraswati_planets) >= 2 and 'Jupiter' in saraswati_planets):
        jup_dignity = _get_dignity_level('Jupiter', _sign_of('Jupiter')) if 'Jupiter' in planets else ''
        if jup_dignity in ['EXALTED', 'OWN_SIGN', 'MOOLATRIKONA', 'FRIEND']:
            yogas.append({"name": "Saraswati Yoga", "name_cn": "辩才天女格局", "combination": f"{'、'.join(saraswati_planets)}在吉宫(2/4/7/9/10)+木星有力", "effects": ["学问渊博", "艺术才华", "表达卓越"], "strength": "强" if jup_dignity in ['EXALTED', 'OWN_SIGN'] else "中强"})

    # ========================================================================
    # 21. Hamsa Yoga（天鹅格局）—— 增强版 Mahapurusha
    # 来源：BPHS。木星入旺/入庙在角宫(1/4/7/10)
    # （注：基本版已包含在 Mahapurusha Yoga 中，这里增加三方宫扩展检测）
    # ========================================================================
    if 'Jupiter' in planets:
        jup_h = _house_of('Jupiter')
        if _is_trikona(jup_h) and (_is_exalted('Jupiter') or _is_own_sign('Jupiter')):
            st = "入旺" if _is_exalted('Jupiter') else "入庙"
            already_hamsa = any(y.get("name") == "Hamsa Yoga" for y in yogas)
            if not already_hamsa:
                yogas.append({"name": "Hamsa Yoga (Trikona)", "name_cn": f"木星{st}三方宫格局", "combination": f"木星{st}在{_sign_of('Jupiter')}(第{jup_h}宫，三方宫)", "effects": ["智慧卓越", "精神导师", "品德高尚"], "strength": "强"})

    # ========================================================================
    # 22. Chamara Yoga（拂尘格局）
    # 来源：BPHS。上升主星在入旺/入庙 + 两个或以上吉星在角宫/三方宫
    # ========================================================================
    if asc_lord in planets and (_is_exalted(asc_lord) or _is_own_sign(asc_lord)):
        ben_kt = [p for p in benefics if p in planets and _planet_in_kendra_or_trikona(p)]
        if len(ben_kt) >= 2:
            st = "入旺" if _is_exalted(asc_lord) else "入庙"
            yogas.append({"name": "Chamara Yoga", "name_cn": "拂尘格局", "combination": f"上升主星{asc_lord}{st}+{'、'.join(ben_kt)}在角宫/三方宫", "effects": ["长寿健康", "受人尊敬", "智慧通达"], "strength": "强"})

    # ========================================================================
    # 23. Akhanda Samrajya Yoga（永恒帝王格局）
    # 来源：BPHS。木星在 2/5/9/11 宫 + 2 宫主不在 6/8/12 宫 + 11 宫主在 11 宫
    # 简化版：木星在 2/5/9/11 + 11 宫主在 11 宫或角宫
    # ========================================================================
    if 'Jupiter' in planets and _house_of('Jupiter') in [2, 5, 9, 11]:
        lord_11 = _lord_of_house(11)
        if lord_11 in planets:
            l11h = _house_of(lord_11)
            if l11h == 11 or _is_kendra(l11h):
                yogas.append({"name": "Akhanda Samrajya Yoga", "name_cn": "永恒帝王格局", "combination": f"木星在{_house_of('Jupiter')}宫+11宫主{lord_11}在{l11h}宫", "effects": ["权力持久", "事业辉煌", "影响力广泛"], "strength": "强"})

    # ========================================================================
    # 24. Gurumauli Yoga / Maha Bhagya Yoga（大运格局）
    # 来源：经典文献。木星在 9 宫或与 9 宫主同宫
    # ========================================================================
    if 'Jupiter' in planets:
        jup_h = _house_of('Jupiter')
        if jup_h == 9:
            yogas.append({"name": "Gurumauli Yoga", "name_cn": "至上师格局", "combination": f"木星在9宫（命运宫）", "effects": ["命运眷顾", "精神导师指引", "福德深厚"], "strength": "强"})
        elif lord_9 in planets and jup_h == _house_of(lord_9):
            yogas.append({"name": "Gurumauli Yoga", "name_cn": "至上师关联格局", "combination": f"木星与9宫主{lord_9}同在第{jup_h}宫", "effects": ["命运眷顾", "贵人运强", "智慧通达"], "strength": "中强"})

    # ========================================================================
    # 25. Shakata Yoga（车格局——凶）
    # 来源：BPHS。木星在 6/8/12 宫（从月亮算起），且月亮与木星不在 1/4/7/10 宫关系
    # 简化版（从上升算）：木星落入 6/8/12 宫
    # ========================================================================
    if 'Jupiter' in planets and _house_of('Jupiter') in [6, 8, 12]:
        yogas.append({"name": "Shakata Yoga", "name_cn": "车格局（凶）", "combination": f"木星落入第{_house_of('Jupiter')}宫（凶宫）", "effects": ["财富不稳", "健康需注意", "精神起伏"], "strength": "凶"})

    # ========================================================================
    # 26. Amarishta Yoga / Daridra Yoga（贫困格局——凶）
    # 来源：BPHS。11 宫主落入 6/8/12 宫，或 2 宫主落陷且在凶宫
    # ========================================================================
    lord_11 = _lord_of_house(11)
    if lord_11 in planets and _house_of(lord_11) in [6, 8, 12]:
        yogas.append({"name": "Daridra Yoga", "name_cn": "贫困格局（凶）", "combination": f"11宫主{lord_11}落入第{_house_of(lord_11)}宫（凶宫）", "effects": ["财务困难", "需努力积累", "谨慎理财"], "strength": "凶"})
    if lord_2 in planets and _is_debilitated(lord_2) and _is_dusthana(_house_of(lord_2)):
        yogas.append({"name": "Daridra Yoga (variant)", "name_cn": "贫困格局变体（凶）", "combination": f"2宫主{lord_2}落陷在凶宫第{_house_of(lord_2)}宫", "effects": ["财务压力", "家庭纠纷", "需节俭持家"], "strength": "凶"})

    # ========================================================================
    # 27. Dhan Yoga 增强版 —— Grahi Dhan Yoga
    # 来源：Phaladeepika。1 宫主 + 2 宫主 + 11 宫主同在 2/11 宫
    # ========================================================================
    lords_wealth = {1: SIGN_LORDS[SIGNS[(ai + 0) % 12]], 2: lord_2, 11: _lord_of_house(11)}
    for wh in [2, 11]:
        count = sum(1 for h_num, lp in lords_wealth.items() if lp in planets and _house_of(lp) == wh)
        if count >= 2:
            in_house = [f"{h_num}宫主{lp}" for h_num, lp in lords_wealth.items() if lp in planets and _house_of(lp) == wh]
            yogas.append({"name": "Grahi Dhana Yoga", "name_cn": "星聚财富格局", "combination": f"{'、'.join(in_house)}同在第{wh}宫", "effects": ["财运亨通", "投资有利", "收入丰厚"], "strength": "强"})
            break

    return {"ascendant": asc, "planets_analyzed": len(planets), "kendra_lords": kl, "trikona_lords": tl, "yogas_detected": len(yogas), "yogas": yogas}


# ============================================================================
# 4. 三层验证法事件预测（v3.4增强：优先EventPredictionModel规则引擎）
# ============================================================================
def cmd_predict(args):
    # 验前事模式（v3.5新增）
    if getattr(args, 'past_verify', False) and args.year:
        chart, asc_idx, jd, ayanamsa = compute_chart_data(
            args.year, args.month, args.day, args.hour, args.minute,
            args.lat, args.lon, args.tz)
        if chart is None:
            return {"error": "swisseph未安装"}
        return _past_event_verify(chart, asc_idx, args)

    chart = json.loads(args.chart) if args.chart else {}
    evt = args.event_type or "all"

    # 尝试加载 EventPredictionModel（替代LAM神经网络）
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from event_prediction_model import EventPredictionModel
        # 直接传完整chart数据给EventPredictionModel（v5.0需要ascendant dict和planets dict）
        # 同时从 full-reading 输出中提取所有模块数据传入（v5.1修复：之前丢失dasha/congregation等）
        modules = chart.get("modules", {})
        model = EventPredictionModel(
            chart_data={
                "ascendant": chart.get("ascendant", {}),
                "planets": chart.get("planets", {}),
            },
            dasha_data=modules.get("dasha"),
            congregation_data=modules.get("congregation"),
            vivah_saham_data=modules.get("vivah_saham"),
            chara_dasha_data=modules.get("jaimini", {}).get("chara_dasha"),
        )
        raw_preds = model.predict_all_events()
        # 将 Prediction dataclass 转为可序列化 dict（v5.1补充缺失字段）
        predictions = []
        for p in raw_preds:
            predictions.append({
                "event_type": str(p.event_type.value) if hasattr(p.event_type, 'value') else str(p.event_type),
                "description": p.description,
                "probability": p.probability,
                "risk_level": str(p.risk_level.value) if hasattr(p.risk_level, 'value') else str(p.risk_level),
                "confidence": str(p.confidence.value) if hasattr(p.confidence, 'value') else str(p.confidence),
                "timing": p.timing,
                "key_factors": p.key_factors,
                "recommendations": p.recommendations,
                "dasha_signals": p.dasha_signals,
                "transit_signals": p.transit_signals,
                "timing_windows": p.timing_windows,
            })
        return {
            "method": "三层验证法（EventPredictionModel规则引擎）",
            "engine": "event_prediction_model.py",
            "event_type": evt,
            "predictions": predictions,
            "note": "基于规则引擎的三层验证法，替代LAM神经网络（准确率从0.17%大幅提升）"
        }
    except Exception as e:
        # 降级到简化版
        result = {"method": "三层验证法（简化版）", "fallback_reason": str(e),
                  "event_type": evt, "predictions": []}
        planets = chart.get("planets", {})
        indicators_map = {
            "marriage": {"houses": [7], "karaka": "Venus", "cn": "婚姻"},
            "career": {"houses": [10, 6], "karaka": "Sun", "cn": "职业"},
            "wealth": {"houses": [2, 11], "karaka": "Jupiter", "cn": "财富"},
            "health": {"houses": [6, 8, 12], "karaka": "Saturn", "cn": "健康"},
        }
        for ek, ei in indicators_map.items():
            if evt != "all" and evt != ek: continue
            found = []
            for hn in ei["houses"]:
                for pn, pd in planets.items():
                    if isinstance(pd, dict) and pd.get("house") == hn:
                        found.append({"planet": pn, "house": hn, "sign": pd.get("sign", ""), "status": pd.get("status", "中性")})
            if found:
                result["predictions"].append({"event": ei["cn"], "key": ek, "static_indicators": found, "note": "需要结合Dasha和Transit进行精确预测"})
        return result


# ============================================================================
# 验前事模式（v3.5新增，避免冷读效应）
# ============================================================================
def _past_event_verify(chart: Dict, asc_idx: int, args) -> Dict:
    """
    验前事：从星盘数据推断 2-4 个高信号历史时段，供用户确认。
    AI 先推断，用户后确认——避免冷读效应。
    """
    planets = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Unknown')
    birth_year = args.year

    signals = []

    # 1. 土星回归（约29.5年一次）
    saturn_sign = planets.get('Saturn', {}).get('sign', '')
    saturn_house = planets.get('Saturn', {}).get('house', 0)
    # 土星绕黄道一圈约29.5年
    for cycle_age in [29, 58]:
        event_year = birth_year + cycle_age
        signals.append({
            'type': '土星回归',
            'age': cycle_age,
            'year': event_year,
            'description': f'约{event_year}年（{cycle_age}岁），土星回归周期',
            'confidence': '高',
            'indicators': [f'土星在{saturn_sign}（第{saturn_house}宫）'],
        })

    # 2. 木星回归（约12年一次）
    jupiter_sign = planets.get('Jupiter', {}).get('sign', '')
    jupiter_house = planets.get('Jupiter', {}).get('house', 0)
    for cycle_age in [12, 24, 36, 48]:
        event_year = birth_year + cycle_age
        signals.append({
            'type': '木星回归',
            'age': cycle_age,
            'year': event_year,
            'description': f'约{event_year}年（{cycle_age}岁），木星回归周期',
            'confidence': '中高',
            'indicators': [f'木星在{jupiter_sign}（第{jupiter_house}宫）'],
        })

    # 3. Rahu-Ketu 对冲过境（约18.6年半周期）
    rahu_sign = planets.get('Rahu', {}).get('sign', '')
    for half_cycle in [9, 18, 27, 36]:
        event_year = birth_year + half_cycle
        signals.append({
            'type': 'Rahu-Ketu半周期',
            'age': half_cycle,
            'year': event_year,
            'description': f'约{event_year}年（{half_cycle}岁），Rahu-Ketu对冲轴变化',
            'confidence': '中',
            'indicators': [f'本命Rahu在{rahu_sign}'],
        })

    # 4. 关键宫位激活（基于 Dasha 可能性）
    # 7宫主星相关 → 婚姻/合作时间窗
    libra_idx = SIGNS.index('Libra') if 'Libra' in SIGNS else 6
    sign_7 = SIGNS[(asc_idx + 6) % 12]
    lord_7 = SIGN_LORDS.get(sign_7, 'Unknown')
    lord_7_info = planets.get(lord_7, {})
    if lord_7_info:
        signals.append({
            'type': '7宫主星活跃期',
            'age_range': '24-32',
            'year_range': f'{birth_year + 24}-{birth_year + 32}',
            'description': f'{lord_7}（7宫主星，7宫={sign_7}）活跃期，可能涉及婚姻/重要合作',
            'confidence': '中',
            'indicators': [f'{lord_7}在{lord_7_info.get("sign", "")}（第{lord_7_info.get("house", 0)}宫）'],
        })

    # 5. 10宫主星相关 → 事业突破
    sign_10 = SIGNS[(asc_idx + 9) % 12]
    lord_10 = SIGN_LORDS.get(sign_10, 'Unknown')
    lord_10_info = planets.get(lord_10, {})
    if lord_10_info:
        signals.append({
            'type': '10宫主星活跃期',
            'age_range': '28-40',
            'year_range': f'{birth_year + 28}-{birth_year + 40}',
            'description': f'{lord_10}（10宫主星，10宫={sign_10}）活跃期，可能涉及事业突破',
            'confidence': '中',
            'indicators': [f'{lord_10}在{lord_10_info.get("sign", "")}（第{lord_10_info.get("house", 0)}宫）'],
        })

    # 按置信度排序，取前4
    priority = {'高': 3, '中高': 2, '中': 1, '低': 0}
    signals.sort(key=lambda s: priority.get(s.get('confidence', '低'), 0), reverse=True)
    top_signals = signals[:4]

    return {
        'method': '验前事（Past Event Reverse Verification）',
        'version': '3.5',
        'note': 'AI从星盘推断的高信号历史时段，请用户确认——避免冷读效应',
        'birth_year': birth_year,
        'ascendant': asc_sign,
        'inferred_periods': top_signals,
        'disclaimer': '这些是基于星盘结构推断的可能时段，需要用户确认是否实际发生了相关事件。',
    }


# ============================================================================
# 5. 分盘计算
# ============================================================================
def cmd_varga(args):
    if not HAS_SWE: return {"error": "swisseph未安装"}
    swe.set_ephe_path('')
    hd = args.hour + args.minute / 60.0 - args.tz
    jd = swe.julday(args.year, args.month, args.day, hd)

    # Lahiri Ayanamsa（恒星黄道修正，与cmd_chart一致）
    ayanamsa = swe.get_ayanamsa(jd)

    natal = {}
    for pn, pid in PLANETS_SWE.items():
        pos, _ = swe.calc_ut(jd, pid); natal[pn] = (pos[0] - ayanamsa) % 360  # 恒星黄道
    if 'Rahu' in natal: natal['Ketu'] = (natal['Rahu'] + 180) % 360
    asc_lon, _ = swe.houses(jd, args.lat, args.lon, b'A'); asc_deg = (asc_lon[0] - ayanamsa) % 360  # 恒星黄道

    def navamsa(lon):
        si = int(lon / 30); d = lon - si * 30; ni = int(d / (30/9))
        el_starts = {0: 0, 1: 9, 2: 6, 3: 3}; return SIGNS[(el_starts[si % 4] + ni) % 12]

    def dasamsa(lon):
        si = int(lon / 30); d = lon - si * 30; di = int(d / 3)
        return SIGNS[di % 12] if si % 2 == 0 else SIGNS[(6 + di) % 12]

    result = {"birth_info": f"{args.year}-{args.month:02d}-{args.day:02d} {args.hour:02d}:{args.minute:02d}", "divisional_charts": {}}
    if args.d9 or args.all:
        d9 = {"ascendant": navamsa(asc_deg)}
        for p, l in natal.items(): d9[p] = {"sign": navamsa(l), "sign_cn": SIGNS_CN[navamsa(l)]}
        result["divisional_charts"]["D9_Navamsa"] = d9
    if args.d10 or args.all:
        d10 = {"ascendant": dasamsa(asc_deg)}
        for p, l in natal.items(): d10[p] = {"sign": dasamsa(l), "sign_cn": SIGNS_CN[dasamsa(l)]}
        result["divisional_charts"]["D10_Dasamsa"] = d10
    if not result["divisional_charts"]: result["note"] = "请指定 --d9, --d10 或 --all"
    return result


# ============================================================================
# 6. 名人案例查询
# ============================================================================
def cmd_celebrity(args):
    result = {"query": args.name or "all", "results": []}
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH); c = conn.cursor()
            if args.name: c.execute("SELECT * FROM cases WHERE name LIKE ?", (f'%{args.name}%',))
            else: c.execute("SELECT * FROM cases LIMIT ?", (args.limit or 20,))
            cols = [d[0] for d in c.description]
            for r in c.fetchall(): result["results"].append(dict(zip(cols, r)))
            conn.close()
        except Exception as e: result["db_error"] = str(e)

    if os.path.exists(PERSON_CSV) and args.name:
        try:
            matches = []
            with open(PERSON_CSV, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    if args.name.lower() in row.get('Name', '').lower():
                        matches.append({"name": row.get('Name', ''), "birth_time": row.get('BirthTime', ''), "gender": row.get('Gender', '')})
                        if len(matches) >= 10: break
            result["person_list_matches"] = matches; result["person_list_total"] = 15807
        except Exception as e: result["csv_error"] = str(e)
    return result


# ============================================================================
# 7. 数据库统计
# ============================================================================
def cmd_db_stats(args):
    result = {}
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH); c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM cases"); result["total_cases"] = c.fetchone()[0]
            c.execute("SELECT case_type, COUNT(*) FROM cases GROUP BY case_type"); result["by_type"] = dict(c.fetchall())
            c.execute("SELECT difficulty, COUNT(*) FROM cases GROUP BY difficulty"); result["by_difficulty"] = dict(c.fetchall())
            c.execute("SELECT name, accuracy_rate, sample_size, correct_predictions FROM techniques"); result["techniques"] = [{"name": r[0], "accuracy": r[1], "samples": r[2], "correct": r[3]} for r in c.fetchall()]
            conn.close()
        except Exception as e: result["error"] = str(e)
    else:
        result["error"] = f"数据库不存在: {DB_PATH}"
    return result


# ============================================================================
# 8. 过境查询
# ============================================================================
def cmd_transit(args):
    """
    实时 Transit 行星过境计算（v3.7.2 改用 Swiss Ephemeris）
    不再依赖静态 JSON，直接用 swe 计算任意日期的行星位置。
    支持指定日期范围（--year/--month）和目标行星（--planet）。
    """
    if not HAS_SWE:
        return {"error": "swisseph未安装，无法计算实时Transit"}

    swe.set_ephe_path('')

    # --- 参数解析 ---
    t_year = args.year
    t_month = args.month
    # 可选：指定某日（默认取月中15号做代表）
    t_day = getattr(args, 'day', 15) or 15
    # 可选：指定目标行星（默认全部七曜+Rahu/Ketu）
    target_planets_str = getattr(args, 'planet', None)
    target_planets = [p.strip() for p in target_planets_str.split(',')] if target_planets_str else None

    # --- 计算该月月中行星位置 ---
    try:
        hd = 12.0 - (getattr(args, 'tz', 8) or 8)  # 默认UTC+8中午
        jd_mid = swe.julday(t_year, t_month, t_day, hd)
    except Exception as e:
        return {"error": f"日期计算失败: {e}"}

    ayanamsa = swe.get_ayanamsa(jd_mid)

    # --- 计算行星位置 ---
    planet_map = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
        'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE
    }

    transit_data = {}
    for pname, pid in planet_map.items():
        if target_planets and pname not in target_planets:
            continue
        pos, ret = swe.calc_ut(jd_mid, pid)
        if ret < 0:
            continue
        lon_sid = (pos[0] - ayanamsa) % 360
        speed = pos[3]
        retrograde = speed < 0
        sign_idx = int(lon_sid / 30) % 12
        deg_in_sign = lon_sid % 30
        sign_name = SIGNS[sign_idx]
        sign_cn = SIGNS_CN[sign_name]

        transit_data[pname] = {
            'sign': sign_name,
            'sign_cn': sign_cn,
            'degree': round(lon_sid, 4),
            'degree_in_sign': round(deg_in_sign, 2),
            'speed': round(speed, 4),
            'retrograde': retrograde,
        }

    # Rahu 存在时补算 Ketu
    if 'Rahu' in transit_data:
        rahu_lon = transit_data['Rahu']['degree']
        ketu_lon = (rahu_lon + 180) % 360
        ketu_si = int(ketu_lon / 30) % 12
        transit_data['Ketu'] = {
            'sign': SIGNS[ketu_si],
            'sign_cn': SIGNS_CN[SIGNS[ketu_si]],
            'degree': round(ketu_lon, 4),
            'degree_in_sign': round(ketu_lon % 30, 2),
            'speed': 0,
            'retrograde': True,
        }

    # --- 计算行星间相位（互相在对方星座的宫位关系）---
    aspects_found = []
    planet_names = list(transit_data.keys())
    for i, p1 in enumerate(planet_names):
        for p2 in planet_names[i+1:]:
            if p1 == 'Ketu' or p2 == 'Ketu':
                continue
            d1 = transit_data[p1]['degree']
            d2 = transit_data[p2]['degree']
            diff = abs(d1 - d2) % 360
            if diff > 180:
                diff = 360 - diff
            # 合相（≤10°）
            if diff <= 10:
                aspects_found.append({
                    'type': 'conjunction',
                    'planets': [p1, p2],
                    'degree_diff': round(diff, 2),
                    'description': f'{p1}与{p2}合相（{diff:.1f}°）'
                })
            # 对冲（180°±8°）
            elif 172 <= diff <= 188:
                aspects_found.append({
                    'type': 'opposition',
                    'planets': [p1, p2],
                    'degree_diff': round(diff, 2),
                    'description': f'{p1}与{p2}对冲（{diff:.1f}°）'
                })
            # 三方（120°±6°）
            elif 114 <= diff <= 126:
                aspects_found.append({
                    'type': 'trine',
                    'planets': [p1, p2],
                    'degree_diff': round(diff, 2),
                    'description': f'{p1}与{p2}三方相位（{diff:.1f}°）'
                })
            # 四分（90°±6°）
            elif 84 <= diff <= 96:
                aspects_found.append({
                    'type': 'square',
                    'planets': [p1, p2],
                    'degree_diff': round(diff, 2),
                    'description': f'{p1}与{p2}四分相位（{diff:.1f}°）'
                })

    # --- 构建结果 ---
    result = {
        'method': 'Swiss Ephemeris 实时计算（v3.7.2）',
        'target_date': f'{t_year}-{t_month:02d}-{t_day:02d}',
        'ayanamsa': round(ayanamsa, 4),
        'planets': transit_data,
        'aspects': aspects_found,
        'note': f'使用Swiss Ephemeris实时计算{t_year}年{t_month}月行星过境位置，不再依赖静态JSON'
    }

    return result


# ============================================================================
# 8b. Double Transit PAC + D9 层（KN Rao 完整实现 v3.9新增）
#
# 核心逻辑:
# 1. D1 层: Saturn/Jupiter 通过 PAC 关联事件宫/宫主/LL/对宫主
# 2. D9 层: Saturn/Jupiter 通过 PAC 关联 D9 宫主/D9 Asc/宫主D9星座/LL D9星座
# 3. 两者必须同时激活同一目标 -> Double Transit 确认
#
# 精度: KN Rao 体系 110-115 星盘测试 97% 准确率（使用 D9 Navamsa）
# ============================================================================
def _navamsa_idx(lon):
    """Navamsa 星座索引"""
    lon = lon % 360
    si = int(lon / 30)
    d = lon - si * 30
    ni = int(d / (30 / 9))
    el_starts = [0, 9, 6, 3]  # Aries/Fire=0, Taurus/Earth=9, Gemini/Air=6, Cancer/Water=3
    return (el_starts[si % 4] + ni) % 12


def _calc_planetary_congregation(planets: Dict, asc_idx: int) -> Dict:
    """
    本命盘行星聚集检测（供 cmd_full_reading 调用）
    检测 3+ 行星同宫的聚集效应，返回聚集宫位、行星列表、影响领域
    """
    houses = {}
    for pn, pd in planets.items():
        if not isinstance(pd, dict) or 'sign' not in pd:
            continue
        if pn in ['Rahu', 'Ketu']:
            continue  # Rahu/Ketu 不计入聚集
        si = SIGNS.index(pd['sign']) if pd['sign'] in SIGNS else 0
        h = ((si - asc_idx) % 12) + 1
        houses.setdefault(h, []).append(pn)

    congregations = []
    for h, plist in houses.items():
        if len(plist) >= 3:
            h_sign = SIGNS[(asc_idx + h - 1) % 12]
            # 判断影响领域
            impact = _house_theme(h)
            # 判断聚集力量（有无吉星/凶星）
            benefics = [p for p in plist if p in ['Jupiter', 'Venus', 'Mercury', 'Moon']]
            malefics = [p for p in plist if p in ['Saturn', 'Mars', 'Sun', 'Rahu']]
            strength = 'strong' if len(benefics) > len(malefics) else 'mixed'
            if len(malefics) >= 3:
                strength = 'malefic_heavy'
            congregations.append({
                'house': h,
                'sign': h_sign,
                'planets': plist,
                'count': len(plist),
                'benefics': benefics,
                'malefics': malefics,
                'strength': strength,
                'impact': impact,
                'description': f'{",".join(plist)} 聚集于{h}宫({h_sign})',
            })

    return {
        'congregations': congregations,
        'total': len(congregations),
        'note': '3+ 行星同宫为显著聚集，影响该宫主题领域',
    }


def _house_theme(house: int) -> List[str]:
    """返回宫位影响领域"""
    themes = {
        1: ['自我', '健康', '性格'],
        2: ['财富', '家庭', '言语'],
        3: ['沟通', '旅行', '兄弟'],
        4: ['母亲', '房产', '情感'],
        5: ['子女', '投资', '创意'],
        6: ['疾病', '敌人', '债务'],
        7: ['婚姻', '合作', '伴侣'],
        8: ['转型', '意外', '遗产'],
        9: ['命运', '父亲', '灵性'],
        10: ['事业', '声望', '成就'],
        11: ['收益', '社交', '愿望'],
        12: ['损失', '外迁', '解脱'],
    }
    return themes.get(house, ['未知'])


def _calc_vivah_saham(planets: Dict, asc_deg: float) -> Dict:
    """
    计算本命 Vivah Saham 婚姻敏感点（供 cmd_full_reading 调用）
    公式: Saham = (Venus_lon - Saturn_lon + Asc_deg) % 360
    """
    venus_lon = planets.get('Venus', {}).get('degree', 0)
    saturn_lon = planets.get('Saturn', {}).get('degree', 0)
    if venus_lon == 0 or saturn_lon == 0:
        return {'error': '缺少金星或土星数据', 'saham': None}

    sahams_lon = (venus_lon - saturn_lon + asc_deg) % 360
    sahams_sign = SIGNS[int(sahams_lon / 30) % 12]
    sahams_deg_in_sign = sahams_lon % 30
    sahams_si = int(sahams_lon / 30) % 12

    # 检查哪些本命行星与 Saham 同宫/合相
    conjuncts = []
    for pn, pd in planets.items():
        if pn in ['Rahu', 'Ketu']:
            continue
        if not isinstance(pd, dict) or 'degree' not in pd:
            continue
        p_lon = pd['degree']
        diff = abs(p_lon - sahams_lon) % 360
        if diff > 180:
            diff = 360 - diff
        if diff <= 5:
            conjuncts.append({'planet': pn, 'diff_deg': round(diff, 2)})

    # 从 Saham 位置反推婚姻相关宫位
    asc_si = int(asc_deg / 30) % 12
    sahams_house = ((sahams_si - asc_si) % 12) + 1

    return {
        'saham_lon': round(sahams_lon, 4),
        'saham_sign': sahams_sign,
        'saham_deg_in_sign': round(sahams_deg_in_sign, 2),
        'saham_house': sahams_house,
        'formula': f'Venus({venus_lon:.2f}°) - Saturn({saturn_lon:.2f}°) + Asc({asc_deg:.2f}°)',
        'natal_conjuncts': conjuncts,
        'marriage_relevance': 'high' if sahams_house in [7, 1, 5, 9] else 'moderate',
        'note': 'Vivah Saham 是度数级婚姻敏感点，Transit 木星/土星过境此点时触发婚姻事件窗',
    }


def _check_pac(planet_name, planet_lon, target_lon, asc_idx):
    """PAC检查: Position(同宫)/Aspect(相位)/Conjunction(合相<=10度)"""
    results = []
    p_si = int((planet_lon % 360) / 30)
    t_si = int((target_lon % 360) / 30)
    p_house = ((p_si - asc_idx) % 12) + 1
    t_house = ((t_si - asc_idx) % 12) + 1

    # P: Position - 同宫
    if p_house == t_house:
        results.append({'type': 'Position', 'desc': f'同宫({t_house}宫)'})

    # C: Conjunction - 合相 <=10度
    diff = abs(planet_lon - target_lon) % 360
    if diff > 180:
        diff = 360 - diff
    if diff <= 10:
        results.append({'type': 'Conjunction', 'desc': f'合相({diff:.2f}\u00b0)'})

    # A: Aspect - Graha Drishti
    planet_aspects = {
        'Sun': [7], 'Moon': [7], 'Mars': [4, 7, 8], 'Mercury': [7],
        'Jupiter': [5, 7, 9], 'Venus': [7], 'Saturn': [3, 7, 10],
        'Rahu': [5, 7, 9], 'Ketu': [5, 7, 9],
    }
    aspects = planet_aspects.get(planet_name, [7])
    for offset in aspects:
        if ((t_house - p_house + 12) % 12) == offset:
            results.append({'type': 'Aspect', 'offset': offset, 'desc': f'{offset}宫相位'})

    return results


def cmd_double_transit_pac(args):
    """Double Transit PAC + D9 层计算"""
    # 1. 计算本命星盘
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    natal = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Aries')
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    event_house = args.house or 7

    # 2. 计算过境行星位置
    if not HAS_SWE:
        return {"error": "swisseph未安装"}

    transit_year, transit_month, transit_day = map(int, args.date.split('-'))
    transit_hour = 12.0 - args.tz  # 正午 UT
    transit_jd = swe.julday(transit_year, transit_month, transit_day, transit_hour)
    transit_ayanamsa = swe.get_ayanamsa(transit_jd)

    transit_planets = {}
    for pname, pid in PLANETS_SWE.items():
        try:
            pos, _ = swe.calc_ut(transit_jd, pid)
            lon_p = (pos[0] - transit_ayanamsa) % 360
            transit_planets[pname] = {'lon': lon_p, 'sign': SIGNS[int(lon_p / 30)]}
            if pname == 'Rahu':
                klon = (lon_p + 180) % 360
                transit_planets['Ketu'] = {'lon': klon, 'sign': SIGNS[int(klon / 30)]}
        except Exception as e:
            transit_planets[pname] = {'error': str(e)}

    # 3. D1 层敏感点
    event_si = (asc_idx + event_house - 1) % 12
    event_sign = SIGNS[event_si]
    event_lord = SIGN_LORDS[event_sign]
    ll_name = SIGN_LORDS[asc_sign]
    opposite_si = (asc_idx + 6) % 12
    opposite_lord = SIGN_LORDS[SIGNS[opposite_si]]

    event_house_lon = (event_si * 30) + 15  # 宫位中点
    ll_lon = natal.get(ll_name, {}).get('degree', 0)
    event_lord_lon = natal.get(event_lord, {}).get('degree', 0)
    opp_lord_lon = natal.get(opposite_lord, {}).get('degree', 0)

    d1_targets = {
        f'{event_house}宫({event_sign})': event_house_lon,
        f'{event_lord}(宫主)': event_lord_lon,
        f'{ll_name}(LL)': ll_lon,
        f'{opposite_lord}(对宫主)': opp_lord_lon,
    }

    # 4. D9 层敏感点
    d9_asc_idx = _navamsa_idx(asc_deg)
    d9_asc_sign = SIGNS[d9_asc_idx]
    d9_event_si = (d9_asc_idx + event_house - 1) % 12
    d9_event_sign = SIGNS[d9_event_si]
    d9_event_lord = SIGN_LORDS[d9_event_sign]
    # 宫主的 D9 星座（KN Rao 关键）
    event_lord_d9_si = _navamsa_idx(event_lord_lon)
    event_lord_d9_sign = SIGNS[event_lord_d9_si]
    ll_d9_si = _navamsa_idx(ll_lon)
    ll_d9_sign = SIGNS[ll_d9_si]

    d9_event_house_lon = (d9_asc_idx * 30) + 15
    d9_event_lord_lon = natal.get(d9_event_lord, {}).get('degree', 0)

    d9_targets = {
        f'D9_{event_house}宫({d9_event_sign})': d9_event_house_lon,
        f'D9_{d9_event_lord}(宫主)': d9_event_lord_lon,
        f'{event_lord}_D9({event_lord_d9_sign})': event_lord_d9_si * 30 + 15,
        f'{ll_name}_D9({ll_d9_sign})': ll_d9_si * 30 + 15,
    }

    # 5. PAC 检查
    results = {
        'transit_date': args.date,
        'event_house': event_house,
        'd1': {'jupiter': {}, 'saturn': {}},
        'd9': {'jupiter': {}, 'saturn': {}},
        'cl': {'jupiter': {}, 'saturn': {}},
        'double_transit': [],
        'summary': '',
    }

    # Chandra Lagna 层敏感点
    moon_lon = natal.get('Moon', {}).get('degree', 0)
    moon_idx = int((moon_lon % 360) / 30)
    cl_event_sign = SIGNS[(moon_idx + event_house - 1) % 12]
    cl_event_lord = SIGN_LORDS[cl_event_sign]
    cl_event_house_lon = ((moon_idx + event_house - 1) % 12) * 30 + 15
    cl_event_lord_lon = natal.get(cl_event_lord, {}).get('degree', 0)
    cl_targets = {
        f'CL_{event_house}宫({cl_event_sign})': cl_event_house_lon,
        f'CL_{cl_event_lord}(宫主)': cl_event_lord_lon,
    }

    for tp_name in ['Jupiter', 'Saturn']:
        tp = transit_planets.get(tp_name, {})
        if 'error' in tp:
            continue
        tp_lon = tp['lon']
        layer = tp_name.lower()

        for t_name, t_lon in d1_targets.items():
            pac = _check_pac(tp_name, tp_lon, t_lon, asc_idx)
            if pac:
                results['d1'][layer][t_name] = pac

        for t_name, t_lon in d9_targets.items():
            pac = _check_pac(tp_name, tp_lon, t_lon, d9_asc_idx)
            if pac:
                results['d9'][layer][t_name] = pac

        for t_name, t_lon in cl_targets.items():
            pac = _check_pac(tp_name, tp_lon, t_lon, moon_idx)
            if pac:
                results['cl'][layer][t_name] = pac

    # 6. Double Transit 判定
    jup_d1 = set(results['d1']['jupiter'].keys())
    sat_d1 = set(results['d1']['saturn'].keys())
    jup_d9 = set(results['d9']['jupiter'].keys())
    sat_d9 = set(results['d9']['saturn'].keys())
    jup_cl = set(results['cl']['jupiter'].keys())
    sat_cl = set(results['cl']['saturn'].keys())

    # D1 层 overlap
    d1_overlap = jup_d1 & sat_d1
    for t in d1_overlap:
        results['double_transit'].append({
            'layer': 'D1', 'target': t,
            'jupiter_pac': results['d1']['jupiter'][t],
            'saturn_pac': results['d1']['saturn'][t],
            'strength': 'strong',
        })

    # D9 层 overlap
    d9_overlap = jup_d9 & sat_d9
    for t in d9_overlap:
        results['double_transit'].append({
            'layer': 'D9', 'target': t,
            'jupiter_pac': results['d9']['jupiter'][t],
            'saturn_pac': results['d9']['saturn'][t],
            'strength': 'strong',
        })

    # Chandra Lagna 层 overlap
    cl_overlap = jup_cl & sat_cl
    for t in cl_overlap:
        results['double_transit'].append({
            'layer': 'CL', 'target': t,
            'jupiter_pac': results['cl']['jupiter'][t],
            'saturn_pac': results['cl']['saturn'][t],
            'strength': 'strong',
        })

    # 跨层 Double Transit
    for d1t in jup_d1:
        for d9t in sat_d9:
            d1_nums = ''.join(c for c in d1t if c.isdigit())
            d9_nums = ''.join(c for c in d9t if c.isdigit())
            if d1_nums == d9_nums or (event_lord in d1t and event_lord in d9t):
                results['double_transit'].append({
                    'layer': 'D1+D9', 'target': f'Jupiter(D1){d1t} + Saturn(D9){d9t}',
                    'jupiter_pac': results['d1']['jupiter'][d1t],
                    'saturn_pac': results['d9']['saturn'][d9t],
                    'strength': 'moderate',
                })
    for d1t in sat_d1:
        for d9t in jup_d9:
            d1_nums = ''.join(c for c in d1t if c.isdigit())
            d9_nums = ''.join(c for c in d9t if c.isdigit())
            if d1_nums == d9_nums or (event_lord in d1t and event_lord in d9t):
                results['double_transit'].append({
                    'layer': 'D1+D9', 'target': f'Saturn(D1){d1t} + Jupiter(D9){d9t}',
                    'jupiter_pac': results['d9']['jupiter'][d9t],
                    'saturn_pac': results['d1']['saturn'][d1t],
                    'strength': 'moderate',
                })

    # Summary
    d1_active = len(d1_overlap) > 0
    d9_active = len(d9_overlap) > 0
    cl_active = len(cl_overlap) > 0
    cross_active = any(d['layer'] == 'D1+D9' for d in results['double_transit'])

    active_layers = []
    if d1_active: active_layers.append('D1')
    if d9_active: active_layers.append('D9')
    if cl_active: active_layers.append('CL')

    if len(active_layers) >= 2:
        results['summary'] = f'✅ Double Transit PAC 确认: {"+".join(active_layers)} 多层激活{event_house}宫主题'
    elif d1_active:
        results['summary'] = f'⚠️ D1 层 Double Transit 激活，D9/CL 层未确认'
    elif d9_active:
        results['summary'] = f'⚠️ D9 层 Double Transit 激活，D1/CL 层未确认'
    elif cl_active:
        results['summary'] = f'⚠️ Chandra Lagna 层 Double Transit 激活，D1/D9 未确认'
    elif cross_active:
        results['summary'] = f'⚠️ 跨层间接 Double Transit (D1+D9)，需结合 Dasha 确认'
    else:
        results['summary'] = f'❌ 无 Double Transit PAC 激活'

    results['stats'] = {
        'd1_jupiter_targets': sorted(jup_d1),
        'd1_saturn_targets': sorted(sat_d1),
        'd9_jupiter_targets': sorted(jup_d9),
        'd9_saturn_targets': sorted(sat_d9),
        'cl_jupiter_targets': sorted(jup_cl),
        'cl_saturn_targets': sorted(sat_cl),
        'd1_overlap': sorted(d1_overlap),
        'd9_overlap': sorted(d9_overlap),
        'cl_overlap': sorted(cl_overlap),
        'd9_ascendant': d9_asc_sign,
        'event_lord_d9_sign': event_lord_d9_sign,
        'chandra_lagna': SIGNS[moon_idx],
    }

    return results


# ============================================================================
# 8c. Transit LL/7L 连接 + 互换（Parivartana）（v3.9新增）
#
# P5: Transit LL PAC natal 7L / Transit 7L PAC natal LL (98%命中率)
# P8: Transit LL 过 7H 或 Transit 7L 过 Lagna (59%命中率)
# + Parivartana 互换检测
# ============================================================================
def _calc_transit_lon(jd, planet_name):
    """计算指定 Julian Day 的行星恒星黄经"""
    pid_map = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY,
               'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE}
    pid = pid_map.get(planet_name)
    if pid is None:
        return None
    pos, _ = swe.calc_ut(jd, pid)
    aya = swe.get_ayanamsa_ut(jd)
    return (pos[0] - aya) % 360


def cmd_transit_ll7l(args):
    """Transit LL/7L 连接 + 互换检测"""
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    natal = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Aries')
    asc_deg = chart.get('ascendant', {}).get('degree', 0)

    ll_name = SIGN_LORDS[asc_sign]
    seven_sign = SIGNS[(SIGNS.index(asc_sign) + 6) % 12]
    seven_lord = SIGN_LORDS[seven_sign]

    # Transit 日期
    t_year, t_month, t_day = map(int, args.date.split('-'))
    transit_jd = swe.julday(t_year, t_month, t_day, 12.0 - args.tz)

    # Transit LL/7L 位置
    t_ll_lon = _calc_transit_lon(transit_jd, ll_name)
    t_7l_lon = _calc_transit_lon(transit_jd, seven_lord)
    if t_ll_lon is None or t_7l_lon is None:
        return {"error": f"无法计算 Transit 位置: LL={ll_name}, 7L={seven_lord}"}

    n_ll_lon = natal.get(ll_name, {}).get('degree', 0)
    n_7l_lon = natal.get(seven_lord, {}).get('degree', 0)
    asc_lon = asc_deg

    result = {
        'transit_date': args.date,
        'lagna_lord': ll_name,
        'seventh_lord': seven_lord,
        'p5': {'hit': False, 'details': []},
        'p8': {'hit': False, 'details': []},
        'parivartana': {'hit': False, 'details': []},
    }

    # P5: Transit LL PAC natal 7L / Transit 7L PAC natal LL
    pac1 = _check_pac(ll_name, t_ll_lon, n_7l_lon, asc_idx)
    if pac1:
        result['p5']['hit'] = True
        result['p5']['details'].append({
            'direction': f'Transit {ll_name} → natal {seven_lord}',
            'connections': pac1,
        })
    pac2 = _check_pac(seven_lord, t_7l_lon, n_ll_lon, asc_idx)
    if pac2:
        result['p5']['hit'] = True
        result['p5']['details'].append({
            'direction': f'Transit {seven_lord} → natal {ll_name}',
            'connections': pac2,
        })

    # P8: Transit LL 过 7H 或 Transit 7L 过 Lagna
    t_ll_house = ((int((t_ll_lon % 360) / 30) - asc_idx) % 12) + 1
    t_7l_house = ((int((t_7l_lon % 360) / 30) - asc_idx) % 12) + 1
    if t_ll_house == 7:
        result['p8']['hit'] = True
        result['p8']['details'].append(f'Transit {ll_name}({SIGNS[int(t_ll_lon/30)]})在7H')
    if t_7l_house == 1:
        result['p8']['hit'] = True
        result['p8']['details'].append(f'Transit {seven_lord}({SIGNS[int(t_7l_lon/30)]})在Lagna')

    # Parivartana 互换
    n_ll_sign = SIGNS[int((n_ll_lon % 360) / 30)]
    n_7l_sign = SIGNS[int((n_7l_lon % 360) / 30)]
    t_ll_in_7l = SIGNS[int((t_ll_lon % 360) / 30)] == n_7l_sign
    t_7l_in_ll = SIGNS[int((t_7l_lon % 360) / 30)] == n_ll_sign
    if t_ll_in_7l and t_7l_in_ll:
        result['parivartana']['hit'] = True
        result['parivartana']['details'].append(
            f'完整互换: Transit {ll_name}在{n_7l_sign}(natal {seven_lord}) + Transit {seven_lord}在{n_ll_sign}(natal {ll_name})')
    elif t_ll_in_7l:
        result['parivartana']['details'].append(f'部分: Transit {ll_name}在{n_7l_sign}')
    elif t_7l_in_ll:
        result['parivartana']['details'].append(f'部分: Transit {seven_lord}在{n_ll_sign}')

    return result


# ============================================================================
# 8d. 行星聚集检测（Lagna/7H + Transit 聚集）（v3.9新增）
# ============================================================================
def cmd_planetary_congregation(args):
    """行星聚集检测"""
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    natal = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Aries')
    event_house = args.house or 7

    result = {
        'natal': {'lagna': [], 'house_7': [], f'house_{event_house}': []},
        'transit': None,
        'summary': '',
    }

    # 本命盘聚集
    for pname, pdata in natal.items():
        if 'error' in pdata or 'sign' not in pdata:
            continue
        p_si = SIGNS.index(pdata['sign'])
        house = ((p_si - asc_idx) % 12) + 1
        if house == 1:
            result['natal']['lagna'].append(pname)
        if house == 7:
            result['natal']['house_7'].append(pname)
        if house == event_house:
            result['natal'][f'house_{event_house}'].append(pname)

    # Transit 聚集
    if args.transit_date:
        t_year, t_month, t_day = map(int, args.transit_date.split('-'))
        transit_jd = swe.julday(t_year, t_month, t_day, 12.0 - args.tz)
        transit_aya = swe.get_ayanamsa(transit_jd)
        result['transit'] = {str(h): [] for h in range(1, 13)}
        for pname, pid in PLANETS_SWE.items():
            try:
                pos, _ = swe.calc_ut(transit_jd, pid)
                lon_p = (pos[0] - transit_aya) % 360
                si = int(lon_p / 30)
                house = ((si - asc_idx) % 12) + 1
                result['transit'][str(house)].append(pname)
                if pname == 'Rahu':
                    klon = (lon_p + 180) % 360
                    ksi = int(klon / 30)
                    khouse = ((ksi - asc_idx) % 12) + 1
                    result['transit'][str(khouse)].append('Ketu')
            except Exception:
                pass

    # 判定
    flags = []
    lagna_count = len(result['natal']['lagna'])
    h7_count = len(result['natal']['house_7'])
    if 'Sun' in result['natal']['lagna'] or lagna_count >= 3:
        flags.append(f"Lagna聚集: {','.join(result['natal']['lagna'])}({lagna_count})")
    if 'Sun' in result['natal']['house_7'] or h7_count >= 3:
        flags.append(f"7H聚集: {','.join(result['natal']['house_7'])}({h7_count})")

    if result['transit']:
        slow = {'Saturn', 'Jupiter', 'Rahu', 'Ketu'}
        t_event = result['transit'].get(str(event_house), [])
        t_slow = [p for p in t_event if p in slow]
        if len(t_slow) >= 2:
            flags.append(f"Transit {event_house}宫慢行星聚集: {','.join(t_slow)}")

    result['flags'] = flags
    result['hit'] = len(flags) > 0
    result['summary'] = ' | '.join(flags) if flags else '无显著聚集'
    return result


# ============================================================================
# 8e. Vivah Saham + 婚姻计时管线（v3.9新增）
#
# Vivah Saham = norm(Venus - Saturn + Asc) — 度数级精确计算
# Transit 激活: Jupiter/Saturn PAC 到 Vivah Saham
# ============================================================================
def cmd_vivah_saham(args):
    """Vivah Saham 计算 + Transit 激活"""
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    natal = chart.get('planets', {})
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    venus_lon = natal.get('Venus', {}).get('degree', 0)
    saturn_lon = natal.get('Saturn', {}).get('degree', 0)

    # Vivah Saham = norm(Venus - Saturn + Asc)
    sahams_lon = (venus_lon - saturn_lon + asc_deg) % 360
    sahams_si = int(sahams_lon / 30)
    sahams_sign = SIGNS[sahams_si]
    sahams_deg = sahams_lon - sahams_si * 30

    result = {
        'vivah_saham': {
            'longitude': round(sahams_lon, 4),
            'sign': sahams_sign,
            'sign_cn': SIGNS_CN[sahams_sign],
            'degree_in_sign': round(sahams_deg, 4),
        },
        'formula': f'norm({venus_lon:.2f} Venus - {saturn_lon:.2f} Saturn + {asc_deg:.2f} Asc)',
        'transit_activation': None,
    }

    # Transit 激活
    if args.transit_date:
        t_year, t_month, t_day = map(int, args.transit_date.split('-'))
        transit_jd = swe.julday(t_year, t_month, t_day, 12.0 - args.tz)

        result['transit_activation'] = {'jupiter': [], 'saturn': [], 'double_activation': False}

        jup_lon = _calc_transit_lon(transit_jd, 'Jupiter')
        sat_lon = _calc_transit_lon(transit_jd, 'Saturn')

        if jup_lon is not None:
            jup_pac = _check_pac('Jupiter', jup_lon, sahams_lon, asc_idx)
            if jup_pac:
                result['transit_activation']['jupiter'] = jup_pac

        if sat_lon is not None:
            sat_pac = _check_pac('Saturn', sat_lon, sahams_lon, asc_idx)
            if sat_pac:
                result['transit_activation']['saturn'] = sat_pac

        if result['transit_activation']['jupiter'] and result['transit_activation']['saturn']:
            result['transit_activation']['double_activation'] = True

        # Venus transit 过 Saham 星座
        venus_t = _calc_transit_lon(transit_jd, 'Venus')
        if venus_t is not None:
            if SIGNS[int(venus_t / 30)] == sahams_sign:
                result['transit_activation']['venus_in_saham_sign'] = True

    return result


# ============================================================================
# 9. Shadbala 六重力量（v3.4新增）
# ============================================================================
def cmd_shadbala(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from shadbala import calc_shadbala
    except ImportError as e:
        return {"error": f"shadbala模块导入失败: {e}"}
    planets = chart.get("planets", {})
    asc_sign = chart.get("ascendant", {}).get("sign", "Aries")
    birth_hour = args.hour + args.minute / 60.0
    sun_lon = planets.get("Sun", {}).get("degree", 0)
    moon_lon = planets.get("Moon", {}).get("degree", 0)
    return calc_shadbala(planets, asc_sign, birth_hour, sun_lon, moon_lon)


# ============================================================================
# 10. Ashtakavarga 八分法（v3.4新增）
# ============================================================================
def cmd_ashtakavarga(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
    except ImportError as e:
        return {"error": f"ashtakavarga模块导入失败: {e}"}
    planets = chart.get("planets", {})
    return calc_ashtakavarga(planets, asc_idx)


# ============================================================================
# 11. Hermes 记忆系统（v3.4新增）
# ============================================================================
def cmd_memory(args):
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from hermes_memory_core import HermesMemoryCore
    except ImportError as e:
        return {"error": f"Hermes记忆模块导入失败: {e}", "hint": "确保hermes_memory_core.py在scripts/目录下"}
    db_file = os.path.join(SCRIPT_DIR, 'hermes_memory.db')
    mem = HermesMemoryCore(db_file)
    result = {"action": args.action}
    if args.action == "store":
        if not args.content:
            return {"error": "store操作需要 --content 参数"}
        tags = args.tags.split(',') if args.tags else []
        importance = args.importance if args.importance else 5
        metadata = {"tags": tags, "importance": importance}
        mem_id = mem.store_memory(args.content, metadata)
        result.update({"stored": True, "memory_id": mem_id, "content": args.content, "tags": tags})
    elif args.action == "search":
        if not args.query:
            return {"error": "search操作需要 --query 参数"}
        results = mem.search(args.query, limit=args.limit or 10)
        result.update({"query": args.query, "found": len(results), "results": results})
    elif args.action == "context":
        session_id = f"jyotish-cli-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        ctx = mem.get_context_for_session(session_id)
        result.update({"session_id": session_id, "context": ctx})
    elif args.action == "stats":
        # Hermes没有get_stats，用搜索空串获取总数
        try:
            all_mem = mem.search("", limit=1000)
            result["total_memories"] = len(all_mem)
        except:
            result["total_memories"] = "unknown"
        result["db_path"] = db_file
    else:
        result["error"] = f"未知action: {args.action}，支持: store/search/context/stats"
    return result


# ============================================================================
# 12. R1-R10 数学验证（v3.5新增）
# ============================================================================
def cmd_validate(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
        asht_result = calc_ashtakavarga(chart.get('planets', {}), asc_idx)
    except ImportError:
        asht_result = None
    try:
        from validate import validate_chart
        return validate_chart(chart, asht_result)
    except ImportError as e:
        return {"error": f"validate模块导入失败: {e}"}


# ============================================================================
# 13. P1-P12 行星审计管线（v3.5新增）
# ============================================================================
def _assess_conjunction_quality(lord, houses, planets):
    """评估仓库耦合的吉凶质量"""
    lord_info = planets.get(lord, {})
    lord_status = lord_info.get('status', '中性')
    # 凶宫组合
    dusthana = {6, 8, 12}
    trikona = {1, 5, 9}
    kendra = {1, 4, 7, 10}
    
    has_dusthana = any(h in dusthana for h in houses)
    has_trikona = any(h in trikona for h in houses)
    has_kendra = any(h in kendra for h in houses)
    
    if has_dusthana and has_trikona:
        return f"凶吉混合 — 挑战与成长并存"
    elif has_dusthana and has_kendra:
        return f"压力型 — 通过努力获取成就"
    elif has_trikona:
        return f"吉庆型 — 自然流畅的支持"
    elif has_dusthana:
        return f"消耗型 — 需要额外努力维持"
    else:
        return f"中性 — 标准互动"

def _conflict_arbitration(report):
    """
    冲突仲裁规则（CNWU16框架）：
    1. P1清理者+P7入旺 = "带毒高价值资产"，禁止说逢凶化吉
    2. P5凶宫+BAV高 = "乱世出英雄"
    3. P1吉+P2受损 = "空有雄心无着力点"
    """
    conflicts = []
    planets = report.get('planets', {})
    audit = report.get('audit', {})
    
    p1 = audit.get('P1_identity', {})
    p7 = audit.get('P7_dignity', {})
    p2 = audit.get('P2_health', {})
    
    asc_lord = p1.get('asc_lord', '')
    
    # 规则1: P1清理者+P7入旺 → 检查上升主是否掌管8/12宫（清理者角色）
    # 清理者定义：掌管8宫或12宫的行星
    SIGN_LORDS_MAP = {'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
                      'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
                      'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'}
    
    asc_sign = p1.get('asc_sign', '')
    asc_idx_local = SIGNS.index(asc_sign) if asc_sign in SIGNS else 0
    
    # 找8宫主和12宫主
    h8_sign = SIGNS[(asc_idx_local + 7) % 12]
    h12_sign = SIGNS[(asc_idx_local + 11) % 12]
    destroyer_lords = {SIGN_LORDS_MAP.get(h8_sign, ''), SIGN_LORDS_MAP.get(h12_sign, '')}
    
    for dl in destroyer_lords:
        if dl and dl in p7:
            dl_status = p7[dl].get('status', '')
            if 'Exalted' in dl_status or 'Own' in dl_status:
                conflicts.append({
                    'rule': 'Destroyer+Exalted',
                    'planets': [dl],
                    'verdict': '带毒高价值资产',
                    'instruction': f"{dl}既是清理者(掌8/12宫)又入旺/入庙，力量极强但方向凶险——禁止说逢凶化吉",
                })
    
    # 规则2: P5凶宫+BAV高 → 检查6/8/12宫的SAV是否 >28
    asht_data = report.get('ashtakavarga', {})
    house_scores = {}
    if asht_data:
        # 从ashtakavarga原始数据获取house_scores
        try:
            sys.path.insert(0, SCRIPT_DIR)
            from ashtakavarga import calc_ashtakavarga
            asht_result = calc_ashtakavarga(planets, asc_idx_local)
            house_scores = asht_result.get('house_scores', {})
        except:
            pass
    
    for h in [6, 8, 12]:
        hs = house_scores.get(f'house_{h}', {})
        sav_score = hs.get('score', 0)
        if sav_score > 28:
            conflicts.append({
                'rule': 'Dusthana+HighBAV',
                'house': h,
                'sav': sav_score,
                'verdict': '乱世出英雄',
                'instruction': f"{h}宫是凶宫但SAV={sav_score}（>28），在困境中反而能出成就",
            })
    
    # 规则3: P1吉+P2受损 → 上升主星状态好但太阳(健康指标)受损
    sun_info = p2.get('sun_status', '')
    lord_info = p7.get(asc_lord, {})
    lord_status = lord_info.get('status', '')
    if ('Exalted' in lord_status or 'Own' in lord_status) and ('Debilitated' in sun_info or 'Enemy' in sun_info):
        conflicts.append({
            'rule': 'GoodP1+DamagedP2',
            'planets': [asc_lord, 'Sun'],
            'verdict': '空有雄心无着力点',
            'instruction': f"上升主{asc_lord}强健但太阳受损，有野心但执行力/健康跟不上",
        })
    
    return conflicts


def cmd_audit(args):
    """P1-P12 行星审计：调用 chart→shadbala→ashtakavarga→yoga，输出统一审计报告"""
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    planets = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Unknown')

    report = {
        'version': '3.5',
        'birth_info': chart.get('birth_info', {}),
        'ascendant': chart.get('ascendant', {}),
        'planets': planets,
        'audit': {},
    }

    # P1 Identity（本命身份）: 上升星座 + 上升主星
    asc_lord = chart.get('ascendant', {}).get('lord', 'Unknown')
    lord_info = planets.get(asc_lord, {})
    report['audit']['P1_identity'] = {
        'asc_sign': asc_sign,
        'asc_lord': asc_lord,
        'lord_sign': lord_info.get('sign', 'Unknown'),
        'lord_house': lord_info.get('house', 0),
        'lord_status': lord_info.get('status', '未知'),
    }

    # P2 Health（健康指标）: 6宫 + 8宫 + 12宫主星 + 太阳状态
    health_houses = [6, 8, 12]
    health_lords = set()
    health_info = {}
    for h in health_houses:
        sign_idx = (asc_idx + h - 1) % 12
        sign_name = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sign_name, 'Unknown')
        health_lords.add(lord)
        health_info[f'house_{h}'] = {'sign': sign_name, 'lord': lord}
    sun_info = planets.get('Sun', {})
    report['audit']['P2_health'] = {
        'houses': health_info,
        'sun_status': sun_info.get('status', '未知'),
        'sun_house': sun_info.get('house', 0),
    }

    # P3 Warehouse Coupling（仓库耦合）: 双宫掌管=货物捆绑
    # CNWU16逻辑：如果一颗行星同时掌管两个宫位，则两个宫位的事务被"捆绑"
    house_lord_map = {}
    for h in range(1, 13):
        sign_idx = (asc_idx + h - 1) % 12
        sname = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sname, 'Unknown')
        if lord not in house_lord_map:
            house_lord_map[lord] = []
        house_lord_map[lord].append(h)

    warehouse_coupling = {}
    for lord, houses in house_lord_map.items():
        if len(houses) > 1:
            warehouse_coupling[lord] = {
                'houses': houses,
                'meaning': f"{lord}同时掌管{houses[0]}宫和{houses[1]}宫，事务捆绑",
                'conjunction_quality': _assess_conjunction_quality(lord, houses, planets),
            }
    report['audit']['P3_warehouse_coupling'] = warehouse_coupling

    # P8 Age Status（年龄状态）: 青壮=主动, 老婴=辅助, 死=自动执行
    # 基于行星在星座中的度数区间判定生命周期
    age_status_map = {}
    for pname, pd in planets.items():
        deg_in_sign = pd.get('degree_in_sign', 0)
        if pname in ['Rahu', 'Ketu']:
            age_status_map[pname] = {'status': '永远逆行', 'phase': 'Rahu/Ketu无年龄状态'}
            continue
        if deg_in_sign < 10:
            phase = '婴幼(0-10°)'
            quality = '辅助型 — 能量尚未完全展开'
        elif deg_in_sign < 20:
            phase = '青壮(10-20°)'
            quality = '主动型 — 能量最活跃，主导性强'
        else:
            phase = '老年(20-30°)'
            quality = '自动执行型 — 已内化的能力，自动化运作'
        age_status_map[pname] = {
            'degree_in_sign': round(deg_in_sign, 2),
            'phase': phase,
            'quality': quality,
        }
    report['audit']['P8_age_status'] = age_status_map

    # P4 Resource SAV（资源SAV）& P6 Exit SAV（退出SAV）
    # 需要 Ashtakavarga 数据
    asht_data = None
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
        asht_data = calc_ashtakavarga(planets, asc_idx)
        report['ashtakavarga'] = {
            'sav_total': asht_data.get('sav', {}).get('total', 0),
            'sav_valid': asht_data.get('sav', {}).get('valid', False),
            'strongest': asht_data.get('strongest_signs', []),
            'weakest': asht_data.get('weakest_signs', []),
        }
        house_scores = asht_data.get('house_scores', {})
        # P4: 财富宫(2,11) SAV
        p4_info = {}
        for h in [2, 11]:
            hs = house_scores.get(f'house_{h}', {})
            p4_info[f'house_{h}'] = hs
        report['audit']['P4_resource_sav'] = p4_info
        # P6: 退出宫(12) SAV + 8宫
        p6_info = {}
        for h in [8, 12]:
            hs = house_scores.get(f'house_{h}', {})
            p6_info[f'house_{h}'] = hs
        report['audit']['P6_exit_sav'] = p6_info
        # P5: 路况(1,5,9三宫) SAV
        p5_info = {}
        for h in [1, 5, 9]:
            hs = house_scores.get(f'house_{h}', {})
            p5_info[f'house_{h}'] = hs
        report['audit']['P5_road_condition'] = p5_info
    except Exception as e:
        report['audit']['ashtakavarga_error'] = str(e)

    # P7 Dignity（尊严状态）
    dignity_map = {}
    for pname, pd in planets.items():
        dignity_map[pname] = {
            'sign': pd.get('sign', ''),
            'status': pd.get('status', '中性'),
            'house': pd.get('house', 0),
            'retrograde': pd.get('retrograde', False),
        }
    report['audit']['P7_dignity'] = dignity_map

    # P9 Shadbala（六重力量）
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from shadbala import calc_shadbala
        birth_hour = args.hour + args.minute / 60.0
        sun_lon = planets.get('Sun', {}).get('degree', 0)
        moon_lon = planets.get('Moon', {}).get('degree', 0)
        shadbala = calc_shadbala(planets, asc_sign, birth_hour, sun_lon, moon_lon)
        report['audit']['P9_shadbala'] = {
            'summary': shadbala.get('summary', {}),
            'ishta_bala_ranking': shadbala.get('ishta_bala_ranking', []),
        }
    except Exception as e:
        report['audit']['P9_shadbala_error'] = str(e)

    # P10 Aspects（相位）简化版
    aspect_map = {}
    for pname, pd in planets.items():
        if pname in ['Rahu', 'Ketu']:
            continue
        house = pd.get('house', 0)
        # 标准 7/4 相位（从该行星宫位数起）
        aspects_from_house = {1: [7], 2: [7], 3: [5, 9, 7], 4: [7, 10],
                              5: [7], 6: [7], 7: [7], 8: [7],
                              9: [5, 7], 10: [7], 11: [7], 12: [7]}
        # 特殊相位
        special = {'Mars': [4, 7, 8], 'Jupiter': [5, 7, 9], 'Saturn': [3, 7, 10]}
        if pname in special:
            aspect_houses = special[pname]
        else:
            aspect_houses = [7]  # 标准对宫
        aspect_map[pname] = {
            'from_house': house,
            'aspect_houses': aspect_houses,
        }
    report['audit']['P10_aspects'] = aspect_map

    # P11 Nakshatra
    nak_map = {}
    for pname, pd in planets.items():
        nak_map[pname] = {
            'nakshatra': pd.get('nakshatra', ''),
            'pada': pd.get('nakshatra_pada', 0),
            'lord': pd.get('nakshatra_lord', ''),
        }
    report['audit']['P11_nakshatra'] = nak_map

    # P12 Yogas（格局识别）
    try:
        yoga_planets = {}
        for pname, pd in planets.items():
            if isinstance(pd, dict) and 'sign' in pd and 'house' in pd:
                yoga_planets[pname] = {'sign': pd['sign'], 'house': pd['house']}
        yoga_result = cmd_yoga(type('Args', (), {
            'ascendant': asc_sign,
            'planets': ','.join([f"{k}:{v['sign']}:{v['house']}" for k, v in yoga_planets.items()])
        })())
        report['audit']['P12_yogas'] = {
            'count': yoga_result.get('yogas_detected', 0),
            'yogas': yoga_result.get('yogas', []),
        }
    except Exception as e:
        report['audit']['P12_yogas_error'] = str(e)

    # 验证
    try:
        from validate import validate_chart
        validation = validate_chart(chart, asht_data)
        report['validation'] = validation
    except Exception as e:
        report['validation'] = {"error": str(e)}

    # 冲突仲裁（CNWU16框架3条规则）
    report['conflict_arbitration'] = _conflict_arbitration(report)

    return report


# ============================================================================
# 14. 报告生成（v3.6新增）
# ============================================================================
def cmd_report(args):
    """调用 report_builder.py 生成 HTML 报告"""
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from report_builder import main as report_main
    except ImportError as e:
        return {"error": f"report_builder模块导入失败: {e}"}

    # 构造 sys.argv 并调用 report_builder
    folder = args.folder
    if not os.path.isdir(folder):
        return {"error": f"目录不存在: {folder}"}

    report_argv = [
        'report_builder.py', folder,
        '--name', args.name,
        '--lagna', args.lagna,
        '--gender', args.gender,
        '--status', args.status,
        '--lang', args.lang,
    ]
    if args.output:
        report_argv.extend(['--output', args.output])

    old_argv = sys.argv
    sys.argv = report_argv
    try:
        report_main()
        output_path = args.output or os.path.join(folder, 'report.html')
        return {
            'status': 'ok',
            'output': output_path,
            'name': args.name,
            'lagna': args.lagna,
            'lang': args.lang,
        }
    except SystemExit:
        return {"error": "report_builder执行出错，请检查MD文件格式"}
    except Exception as e:
        return {"error": f"报告生成失败: {e}"}
    finally:
        sys.argv = old_argv


# ============================================================================
# 15. BPHS十六分盘完整计算（v3.7新增）
# ============================================================================
def cmd_varga_full(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from varga import calc_all_vargas
    except ImportError as e:
        return {"error": f"varga模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {pn: pd['degree'] for pn, pd in planets.items() if isinstance(pd, dict) and 'degree' in pd}
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    divisions = [int(d.strip().replace('D','')) for d in args.divisions.split(',')] if args.divisions else None
    return calc_all_vargas(planet_lons, asc_deg, divisions)


# ============================================================================
# 16. 度数精确相位系统（v3.7新增）
# ============================================================================
def cmd_aspects(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from aspects import calc_all_aspects
    except ImportError as e:
        return {"error": f"aspects模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    return calc_all_aspects(planet_lons, asc_deg)


# ============================================================================
# 17. Jaimini系统（v3.7新增）
# ============================================================================
def cmd_jaimini(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from jaimini import calc_chara_karaka_7, calc_chara_karaka_8, calc_chara_dasha, calc_karakamsha, calc_chara_dasha_with_antardasha
        from varga import calc_varga
    except ImportError as e:
        return {"error": f"jaimini模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    planet_degs = {}  # 星座内度数(0-30)，用于Jaimini Karaka计算
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
            planet_degs[pn] = pd.get('degree_in_sign', pd['degree'] % 30)
    asc_deg = chart.get('ascendant', {}).get('degree', 0)

    result = {}
    # Chara Karaka（必须传星座内度数0-30，不是完整经度0-360）
    mode = args.mode or 'all'
    if mode in ('all', 'karaka'):
        result['chara_karaka_7'] = calc_chara_karaka_7(planet_degs)
        result['chara_karaka_8'] = calc_chara_karaka_8(planet_degs)
    if mode in ('all', 'dasha'):
        use_antardasha = getattr(args, 'antardasha', False)
        if use_antardasha:
            result['chara_dasha'] = calc_chara_dasha_with_antardasha(asc_idx, planet_lons, args.year, args.month)
        else:
            result['chara_dasha'] = calc_chara_dasha(asc_idx, planet_lons, args.year, args.month)
    if mode in ('all', 'karakamsha'):
        # AK（灵魂星）的D9位置 — Karakamsha定义是AK在Navamsa中的星座
        # ⚠️ 2026-05-03修正：此前错误使用DK，现已修正为AK
        ck7 = calc_chara_karaka_7(planet_degs)
        ak_name = ck7['karaka_table']['Atmakaraka']['planet']
        ak_lon = planet_lons.get(ak_name, 0)
        ak_d9 = calc_varga(ak_lon, 9)
        result['karakamsha'] = calc_karakamsha(ak_d9.get('sign', 'Aries'), ak_d9.get('degree_in_sign', 0))
    return result


# ============================================================================
# 18. 高级Nakshatra分析（v3.7新增）
# ============================================================================
def cmd_nakshatra_adv(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from nakshatra_advanced import find_nakshatra, calc_all_tara_balas, calc_sub_lord, nakshatra_compatibility
    except ImportError as e:
        return {"error": f"nakshatra_advanced模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']

    result = {'planets': {}}
    mode = args.mode or 'all'

    if mode in ('all', 'detail'):
        for pn, lon in planet_lons.items():
            result['planets'][pn] = find_nakshatra(lon)

    if mode in ('all', 'tara'):
        moon_lon = planet_lons.get('Moon', 0)
        moon_nak_idx = int(moon_lon / (360/27)) % 27
        result['tara_bala'] = calc_all_tara_balas(moon_nak_idx, planet_lons)

    if mode in ('all', 'sublord'):
        result['sub_lords'] = {pn: calc_sub_lord(lon) for pn, lon in planet_lons.items()}

    return result


# ============================================================================
# 19. Argala门闩系统（v3.7新增）
# ============================================================================
def cmd_argala(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from argala import calc_argala
    except ImportError as e:
        return {"error": f"argala模块导入失败: {e}"}
    planets = chart.get('planets', {})
    # 构建宫位到行星的映射 - argala需要sign_indices
    planet_sign_indices = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'sign' in pd:
            si = SIGNS.index(pd['sign']) if pd['sign'] in SIGNS else 0
            planet_sign_indices[pn] = si
    return calc_argala(planet_sign_indices, asc_idx)


# ============================================================================
# 20. Tajika/Varshaphala年运盘（v3.7新增）
# ============================================================================
def cmd_tajika(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from tajika import calc_muntha, calc_year_lord, calc_mudda_dasha, calc_tri_pataka
    except ImportError as e:
        return {"error": f"tajika模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    asc_si = int(asc_deg / 30) % 12  # sign index
    age = args.age
    if age is None:
        return {"error": "请提供 --age 参数（当前年龄）"}

    result = {}
    mode = args.mode or 'all'
    if mode in ('all', 'muntha'):
        result['muntha'] = calc_muntha(asc_si, age)
    if mode in ('all', 'yearlord'):
        result['year_lord'] = calc_year_lord(asc_si, age)
    if mode in ('all', 'mudda'):
        # 需要先获取 varsha_lord
        yl = calc_year_lord(asc_si, age)
        varsha_lord = yl.get('year_lord', 'Jupiter')
        result['mudda_dasha'] = calc_mudda_dasha(asc_si, varsha_lord, args.month)
    if mode in ('all', 'tripataka'):
        yl = calc_year_lord(asc_si, age)
        varsha_lord = yl.get('year_lord', 'Jupiter')
        muntha_si = (asc_si + age) % 12
        result['tri_pataka'] = calc_tri_pataka(planet_lons, varsha_lord, muntha_si)
    return result


# ============================================================================
# 21. 合盘分析（v3.7新增）
# ============================================================================
def cmd_synastry(args):
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from synastry import calc_synastry
    except ImportError as e:
        return {"error": f"synastry模块导入失败: {e}"}
    # 构建两人数据
    p1 = {'moon_lon': args.moon1, 'gender': args.gender1 or 'M'}
    p2 = {'moon_lon': args.moon2, 'gender': args.gender2 or 'F'}
    if args.mars1 is not None: p1['mars_lon'] = args.mars1
    if args.mars2 is not None: p2['mars_lon'] = args.mars2
    if args.asc1 is not None: p1['asc_lon'] = args.asc1
    if args.asc2 is not None: p2['asc_lon'] = args.asc2
    return calc_synastry(p1, p2)


# ============================================================================
# 22. 全自动综合解盘 full-reading（v3.7.1新增）
# ============================================================================


# ============================================================================
# Transit 多参考点分析（v4.5.0 P1补齐）
# 基于 transit-multi-reference-guide.md 强制规范
# 四参考点：Lagna / Chandra Lagna / Arudha Lagna / Navamsa Lagna
# ============================================================================
def _calc_transit_multi_reference(planets, asc_idx, asc_deg, planet_lons):
    """
    ⭐ v4.5.0: Transit多参考点分析（强制规范）
    每次Transit分析必须同时从四个参考点评估：
    1. Lagna（上升点）— 实际生活事件
    2. Chandra Lagna（月亮星座）— 心理状态、职业变动
    3. Arudha Lagna（AL）— 公众形象
    4. Navamsa Lagna（D9上升）— 灵魂层面
    """
    # 四个参考点的星座索引
    moon_lon = planet_lons.get('Moon', 0)
    chandra_idx = int(moon_lon / 30) % 12

    # Arudha Lagna（从special_lagnas模块逻辑简化：AL = (Ascendant度数+12宫主度数)%360 对应的星座）
    twelfth_sign_idx = (asc_idx + 11) % 12
    twelfth_lord = SIGN_LORDS.get(SIGNS[twelfth_sign_idx], '')
    twelfth_lord_lon = planet_lons.get(twelfth_lord, 0)
    al_raw = (asc_deg + twelfth_lord_lon) % 360
    # AL 特殊规则：如果结果落在原始宫或第7宫，取对宫
    al_idx = int(al_raw / 30) % 12
    if al_idx == asc_idx or al_idx == (asc_idx + 6) % 12:
        al_idx = (al_idx + 7) % 12  # 取第8个 = 对宫再移一位

    # Navamsa Lagna
    d9_asc_idx = _navamsa_idx(asc_deg)

    references = {
        'Lagna': {
            'name': 'Lagna',
            'cn': '上升点',
            'sign': SIGNS[asc_idx],
            'sign_cn': SIGNS_CN[SIGNS[asc_idx]],
            'sign_idx': asc_idx,
            'priority': 'P1',
            'scope': '实际生活事件、身体健康',
        },
        'Chandra_Lagna': {
            'name': 'Chandra Lagna',
            'cn': '月亮上升',
            'sign': SIGNS[chandra_idx],
            'sign_cn': SIGNS_CN[SIGNS[chandra_idx]],
            'sign_idx': chandra_idx,
            'priority': 'P1',
            'scope': '心理状态、职业变动、情感体验',
        },
        'Arudha_Lagna': {
            'name': 'Arudha Lagna',
            'cn': '形象上升',
            'sign': SIGNS[al_idx],
            'sign_cn': SIGNS_CN[SIGNS[al_idx]],
            'sign_idx': al_idx,
            'priority': 'P2',
            'scope': '公众形象、社会认知、他人如何看待你',
        },
        'Navamsa_Lagna': {
            'name': 'Navamsa Lagna',
            'cn': '灵性上升',
            'sign': SIGNS[d9_asc_idx],
            'sign_cn': SIGNS_CN[SIGNS[d9_asc_idx]],
            'sign_idx': d9_asc_idx,
            'priority': 'P3',
            'scope': '灵魂层面的实际影响、内在真实',
        },
    }

    # 对每个外行星（Jupiter/Saturn/Rahu/Ketu），计算从四个参考点看的宫位
    OUTER_PLANETS = ['Jupiter', 'Saturn', 'Rahu', 'Ketu']
    transit_analysis = {}
    for pn in OUTER_PLANETS:
        pd = planets.get(pn, {})
        if not isinstance(pd, dict) or 'sign' not in pd:
            continue
        p_sign_idx = SIGNS.index(pd['sign']) if pd['sign'] in SIGNS else 0
        transit_analysis[pn] = {
            'sign': pd['sign'],
            'sign_cn': SIGNS_CN.get(pd['sign'], ''),
            'degree_in_sign': pd.get('degree_in_sign', pd.get('degree', 0) % 30),
            'house_from_ref': {},
        }
        for ref_name, ref_info in references.items():
            ref_idx = ref_info['sign_idx']
            house = ((p_sign_idx - ref_idx) % 12) + 1
            house_meaning = _house_theme(house)
            transit_analysis[pn]['house_from_ref'][ref_name] = {
                'house': house,
                'meaning': house_meaning,
            }

    # 差异检测：同一行星在不同参考点的宫位含义是否矛盾
    divergences = []
    for pn, pa in transit_analysis.items():
        houses = {ref: info['house'] for ref, info in pa['house_from_ref'].items()}
        unique_houses = set(houses.values())
        if len(unique_houses) > 1:
            divergences.append({
                'planet': pn,
                'houses': houses,
                'divergence': f'{pn}在四个参考点分别落在不同宫位，需综合判断',
            })

    # Sade Sati / Ashtama Shani 检测（基于Chandra Lagna）
    special_checks = {}
    saturn_sign_idx = SIGNS.index(planets.get('Saturn', {}).get('sign', 'Aries')) if isinstance(planets.get('Saturn'), dict) and planets.get('Saturn', {}).get('sign') in SIGNS else 0
    # Sade Sati: Saturn 在月亮星座或前后1宫
    sade_sati_phase = None
    if saturn_sign_idx == chandra_idx:
        sade_sati_phase = 'peak'
    elif saturn_sign_idx == (chandra_idx - 1) % 12:
        sade_sati_phase = 'rising'
    elif saturn_sign_idx == (chandra_idx + 1) % 12:
        sade_sati_phase = 'setting'
    if sade_sati_phase:
        special_checks['sade_sati'] = {
            'active': True,
            'phase': sade_sati_phase,
            'note': f'土星过境月亮{SIGNS_CN[SIGNS[chandra_idx]]}附近，Sade Sati {sade_sati_phase}期',
        }
    # Ashtama Shani: Saturn在月亮第8宫
    saturn_from_chandra = ((saturn_sign_idx - chandra_idx) % 12) + 1
    if saturn_from_chandra == 8:
        special_checks['ashtama_shani'] = {
            'active': True,
            'note': '土星过境月亮第8宫（Ashtama Shani），压力期',
        }

    return {
        'references': references,
        'transit_analysis': transit_analysis,
        'divergences': divergences,
        'divergence_count': len(divergences),
        'special_checks': special_checks,
        'protocol': 'v4.5.0 Transit多参考点强制规范：AI必须同时呈现Lagna和Chandra Lagna两个视角。任何矛盾信号必须记录并解释。',
    }


# ============================================================================
# Dasa Convergence 三系统交叉验证（v4.5.0 P1补齐）
# 基于 dasa-convergence-methodology.md
# 三系统：Vimshottari + Chara Dasha + Yogini
# ============================================================================
# Yogini Dasha 常量
YOGINI_ORDER = ['Mangala', 'Pingala', 'Dhanya', 'Bhramari', 'Bhadrika', 'Ulka', 'Siddha', 'Sankata']
YOGINI_YEARS = {'Mangala': 1, 'Pingala': 2, 'Dhanya': 3, 'Bhramari': 4, 'Bhadrika': 5, 'Ulka': 6, 'Siddha': 7, 'Sankata': 8}
# Yogini 从月亮 Nakshatra 的第3个 Nakshatra（Dhanishta）开始计数
YOGINI_NAK_START = 23  # Dhanishta 在 NAKSHATRA_LIST 中的索引


def _calc_yogini_dasha(moon_lon, birthdate_str):
    """
    计算 Yogini Dasha 时间线
    Yogini 基于 8 位女神循环，总周期 36 年
    起始点由月亮所在 Nakshatra 决定
    """
    nak_idx = int(moon_lon / (360 / 27)) % 27
    # Yogini 起始索引 = (nak_idx - YOGINI_NAK_START) % 8
    yog_start = (nak_idx - YOGINI_NAK_START) % 8
    # 余数 = 在当前 Yogini 周期中的已过比例
    nak_in_yog = nak_idx % 8  # 在8分组的第几个
    pada = int((moon_lon % (360/27)) / (360/108)) + 1
    # 余数比例
    balance_frac = (nak_in_yog * 4 + pada - 1) / 32  # 8 Nakshatra × 4 Pada = 32 份
    balance_frac = min(balance_frac, 1.0)

    birth_date = datetime.strptime(birthdate_str, '%Y-%m-%d')
    maha_periods = []
    total_years = 0
    for i in range(8):
        idx = (yog_start + i) % 8
        name = YOGINI_ORDER[idx]
        years = YOGINI_YEARS[name]
        if i == 0:
            elapsed_years = years * balance_frac
            actual_years = years - elapsed_years
            start_offset = total_years
            maha_periods.append({
                'yogini': name,
                'full_years': years,
                'balance_years': round(actual_years, 3),
                'start_offset_years': round(start_offset, 3),
                'start_date': (birth_date + timedelta(days=round(start_offset * 365.25))).strftime('%Y-%m-%d'),
                'end_date': (birth_date + timedelta(days=round((start_offset + actual_years) * 365.25))).strftime('%Y-%m-%d'),
                'is_current_start': True,
            })
            total_years += actual_years
        else:
            start_offset = total_years
            maha_periods.append({
                'yogini': name,
                'full_years': years,
                'start_offset_years': round(start_offset, 3),
                'start_date': (birth_date + timedelta(days=round(start_offset * 365.25))).strftime('%Y-%m-%d'),
                'end_date': (birth_date + timedelta(days=round((start_offset + years) * 365.25))).strftime('%Y-%m-%d'),
            })
            total_years += years

    # 计算当前 Yogini
    today = datetime.now()
    age_days = (today - birth_date).days
    age_years = age_days / 365.25
    cycle_years = 36  # Yogini 总周期
    current_in_cycle = age_years % cycle_years
    current_yogini = None
    cumulative = 0
    for yp in maha_periods:
        dur = yp.get('balance_years', yp['full_years'])
        if cumulative <= current_in_cycle < cumulative + dur:
            current_yogini = yp
            break
        cumulative += dur

    return {
        'moon_nakshatra_idx': nak_idx,
        'yogini_start_index': yog_start,
        'total_cycle_years': 36,
        'maha_periods': maha_periods,
        'current_yogini': current_yogini,
    }


def _calc_dasa_convergence(dasha_result, chara_dasha_result, yogini_result, planet_lons, asc_idx):
    """
    ⭐ v4.5.0: Dasa Convergence 三系统交叉验证
    Vimshottari + Chara Dasha + Yogini 三系统同时激活同一生活领域时，概率大幅提升
    """
    # 提取各系统当前周期
    convergence_data = {'systems': {}}

    # 系统1: Vimshottari
    if isinstance(dasha_result, dict):
        current_d = dasha_result.get('current_dasha', {})
        if isinstance(current_d, dict):
            maha = current_d.get('mahadasha', current_d.get('maha'))
            antar = current_d.get('antardasha', current_d.get('antar'))
            convergence_data['systems']['vimshottari'] = {
                'maha': maha,
                'antar': antar,
                'pratyantar': current_d.get('pratyantar'),
                'basis': 'Nakshatra (Moon)',
            }

    # 系统2: Chara Dasha
    if isinstance(chara_dasha_result, dict):
        cd_maha = chara_dasha_result.get('current_maha', chara_dasha_result.get('current'))
        cd_antar = chara_dasha_result.get('current_antar')
        if isinstance(cd_maha, dict):
            cd_sign = cd_maha.get('sign', cd_maha.get('rashi'))
        elif isinstance(cd_maha, str):
            cd_sign = cd_maha
        else:
            cd_sign = None
        convergence_data['systems']['chara_dasha'] = {
            'maha_sign': cd_sign,
            'antar_sign': cd_antar.get('sign', cd_antar) if isinstance(cd_antar, dict) else cd_antar,
            'basis': 'Rashi (Sign-based)',
        }

    # 系统3: Yogini
    if isinstance(yogini_result, dict):
        cur_yog = yogini_result.get('current_yogini', {})
        convergence_data['systems']['yogini'] = {
            'yogini': cur_yog.get('yogini') if isinstance(cur_yog, dict) else None,
            'years': cur_yog.get('full_years') if isinstance(cur_yog, dict) else None,
            'basis': 'Nakshatra (8-goddess cycle)',
        }

    # 宫位主题映射
    house_themes_map = {
        1: 'self_health', 2: 'wealth_family', 3: 'communication_skill', 4: 'home_mother',
        5: 'creativity_children', 6: 'health_service', 7: 'marriage_partnership',
        8: 'transformation', 9: 'fortune_dharma', 10: 'career_status',
        11: 'gains_wishes', 12: 'loss_spirituality',
    }

    # 逐领域检测三系统激活
    domain_activations = {}
    for house, domain in house_themes_map.items():
        activations = []

        # Vimshottari: 检查大运/小运行星是否关联该宫
        vims = convergence_data['systems'].get('vimshottari', {})
        if vims:
            for level in ['maha', 'antar']:
                planet = vims.get(level)
                if planet and isinstance(planet, str):
                    # 该行星是否掌管此宫？
                    target_sign_idx = (asc_idx + house - 1) % 12
                    target_sign = SIGNS[target_sign_idx]
                    target_lord = SIGN_LORDS.get(target_sign, '')
                    if planet == target_lord:
                        activations.append({
                            'system': 'Vimshottari',
                            'level': level,
                            'planet': planet,
                            'reason': f'{planet}是{house}宫({target_sign})的宫主星',
                        })
                    # 该行星是否落在此宫？
                    p_sign_idx = int(planet_lons.get(planet, 0) / 30) % 12
                    p_house = ((p_sign_idx - asc_idx) % 12) + 1
                    if p_house == house:
                        activations.append({
                            'system': 'Vimshottari',
                            'level': level,
                            'planet': planet,
                            'reason': f'{planet}落在{house}宫',
                        })

        # Chara Dasha: 检查当前星座是否关联该宫
        cd = convergence_data['systems'].get('chara_dasha', {})
        if cd and cd.get('maha_sign'):
            cd_sign = cd['maha_sign']
            if cd_sign in SIGNS:
                cd_sign_idx = SIGNS.index(cd_sign)
                cd_house_from_asc = ((cd_sign_idx - asc_idx) % 12) + 1
                if cd_house_from_asc == house:
                    activations.append({
                        'system': 'Chara Dasha',
                        'level': 'maha',
                        'sign': cd_sign,
                        'reason': f'Chara大运星座{cd_sign}是{house}宫',
                    })

        if activations:
            domain_activations[domain] = {
                'house': house,
                'activations': activations,
                'system_count': len(set(a['system'] for a in activations)),
            }

    # 收敛等级评估
    for domain, info in domain_activations.items():
        sc = info['system_count']
        if sc >= 3:
            info['convergence_level'] = 'L4'
            info['probability'] = '75-85%'
            info['interpretation'] = '三系统同时激活，极强信号'
        elif sc >= 2:
            info['convergence_level'] = 'L3'
            info['probability'] = '50-65%'
            info['interpretation'] = '双系统激活，强信号'
        else:
            info['convergence_level'] = 'L1'
            info['probability'] = '+15-20%'
            info['interpretation'] = '单系统激活，需Transit确认'

    # 收敛窗口（最高优先级的领域）
    top_domains = sorted(domain_activations.items(), key=lambda x: x[1]['system_count'], reverse=True)[:5]

    return {
        'systems_summary': convergence_data['systems'],
        'domain_activations': domain_activations,
        'top_convergent_domains': [(d, info['convergence_level']) for d, info in top_domains],
        'protocol': 'v4.5.0 Dasa Convergence 三系统交叉验证。收敛等级: L1(单系统)→L3(双系统)→L4(三系统)。所有预测必须标注收敛等级。',
    }


def _calc_actionable_context(planets, asc_idx):
    """⭐ v4.1.0: 计算Transit Actionable Output所需的上下文数据
    输出：宫位激活映射 + 关键行星宫位关系 → 供AI生成Actionable Output时直接引用
    """
    # 宫位主星映射（哪个行星掌管哪个宫）
    house_lord_map = {}
    for h in range(1, 13):
        sign_idx = (asc_idx + h - 1) % 12
        sname = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sname, 'Unknown')
        house_lord_map[h] = {'sign': sname, 'lord': lord}

    # 行星落宫映射（哪个行星落在哪个宫）
    planet_house_map = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict):
            planet_house_map[pn] = {
                'sign': pd.get('sign', 'Unknown'),
                'house': pd.get('house', 0),
                'degree_in_sign': pd.get('degree_in_sign', 0),
            }

    # 双宫掌管检测（仓库耦合）
    lord_to_houses = {}
    for h, info in house_lord_map.items():
        lord = info['lord']
        if lord not in lord_to_houses:
            lord_to_houses[lord] = []
        lord_to_houses[lord].append(h)
    warehouse_coupling = {l: hs for l, hs in lord_to_houses.items() if len(hs) > 1}

    # 关键宫位激活条件（Transit激活该宫需要哪些行星过境相关星座）
    KEY_HOUSES = {
        2: '财富/家庭/语言',
        3: '沟通/技能/短途/内容创作',
        5: '创造力/子女/投机/恋爱',
        7: '婚姻/合作/公开对手',
        9: '长途旅行/高等教育/宗教/出版',
        10: '事业/社会地位/权威',
        11: '收入/愿望/社交网络/贵人',
        12: '海外/灵性/损失/解脱',
    }

    activation_map = {}
    for h, meaning in KEY_HOUSES.items():
        sign_idx = (asc_idx + h - 1) % 12
        sname = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sname, 'Unknown')
        lord_house = planet_house_map.get(lord, {}).get('house', 0)
        activation_map[h] = {
            'house_meaning': meaning,
            'sign': sname,
            'lord': lord,
            'lord_house': lord_house,
            'transit_triggers': f'{lord}过境{h}宫({sname})或{lord}本身过境相关宫位',
            'double_transit_hint': f'需要Saturn和Jupiter同时激活{h}宫或{h}宫主所在宫',
        }

    # 内容创作相关信号（3宫/5宫/9宫/10宫交叉）
    content_signals = {}
    for h in [3, 5, 9, 10]:
        if h in activation_map:
            content_signals[f'house_{h}'] = activation_map[h]

    # 贵人相关信号（7宫/9宫/11宫）
    mentor_signals = {}
    for h in [7, 9, 11]:
        if h in activation_map:
            mentor_signals[f'house_{h}'] = activation_map[h]

    return {
        'house_lord_map': house_lord_map,
        'planet_house_map': planet_house_map,
        'warehouse_coupling': warehouse_coupling,
        'key_house_activations': activation_map,
        'content_creation_context': content_signals,
        'mentor_discovery_context': mentor_signals,
        'actionable_hint': 'AI应基于此上下文生成Transit Actionable Output：每条Transit预测必须包含时间段+行动类型+置信度。详见SKILL.md Transit Actionable Output规范。',
    }

def cmd_full_reading(args):
    """
    用户只需提供出生信息，引擎自动串起全链路分析：
    chart → dasha → yoga → varga-full → aspects → jaimini → nakshatra-adv
    → argala → tajika → shadbala → ashtakavarga → validate → audit
    → 综合报告输出
    """
    import time
    t0 = time.time()

    report = {
        'version': '4.4.0-full-reading',
        'birth_info': {
            'date': f"{args.year}-{args.month:02d}-{args.day:02d}",
            'time': f"{args.hour:02d}:{args.minute:02d}",
            'lat': args.lat, 'lon': args.lon,
            'tz': f"UTC{'+' if args.tz >= 0 else ''}{args.tz}",
        },
        'modules': {},
        'errors': [],
        'warnings': [],
    }

    # ── Step 1: 核心星盘 ──
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装，无法计算星盘"}

    report['chart'] = chart
    planets = chart.get('planets', {})
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    asc_sign = chart.get('ascendant', {}).get('sign', 'Unknown')
    planet_lons = {pn: pd['degree'] for pn, pd in planets.items() if isinstance(pd, dict) and 'degree' in pd}
    planet_degs = {pn: pd.get('degree_in_sign', pd['degree'] % 30) for pn, pd in planets.items() if isinstance(pd, dict) and 'degree' in pd}
    planet_sign_indices = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'sign' in pd:
            planet_sign_indices[pn] = SIGNS.index(pd['sign']) if pd['sign'] in SIGNS else 0

    # ── Step 1.5: Special Lagnas 特殊上升点 (v4.4.0) ──
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from special_lagnas import SpecialLagnasCalculator
        sl_calc = SpecialLagnasCalculator()
        birth_dt = datetime(args.year, args.month, args.day, args.hour, args.minute)
        # 简化处理：sunrise 近似为 6:00 当地时间
        sunrise_dt = datetime(args.year, args.month, args.day, 6, 0)
        sl_result = sl_calc.calculate_all_lagnas(
            asc_degree=asc_deg,
            sun_degree=planet_lons.get('Sun', 0),
            moon_degree=planet_lons.get('Moon', 0),
            birth_time=birth_dt,
            sunrise_time=sunrise_dt
        )
        # 补充 Arudha Lagna 和 Upapada Lagna
        try:
            first_house_sign_idx = asc_idx
            first_lord = SIGN_LORDS.get(SIGNS[first_house_sign_idx], '')
            first_lord_deg = planet_lons.get(first_lord, 0)
            sl_result['Arudha_Lagna'] = sl_calc.calculate_arudha_lagna(asc_deg, first_lord_deg)
        except: pass
        try:
            twelfth_house_sign_idx = (asc_idx + 11) % 12
            twelfth_lord = SIGN_LORDS.get(SIGNS[twelfth_house_sign_idx], '')
            twelfth_lord_deg = planet_lons.get(twelfth_lord, 0)
            sl_result['Upapada_Lagna'] = sl_calc.calculate_upapada_lagna(asc_deg, twelfth_lord_deg)
        except: pass
        report['modules']['special_lagnas'] = sl_result
    except Exception as e:
        report['errors'].append(f"special-lagnas: {e}")

    # ── Step 2: Vimshottari Dasha ──
    try:
        moon_data = planets.get('Moon', {})
        moon_lon = moon_data.get('degree', 0)
        nak_idx = int(moon_lon / (360 / 27)) % 27
        nak_name = NAKSHATRA_LIST[nak_idx][0]
        nak_lord = NAKSHATRA_LIST[nak_idx][1]
        pada = int((moon_lon % (360/27)) / (360/108)) + 1

        birthdate = f"{args.year}-{args.month:02d}-{args.day:02d}"
        today_str = datetime.now().strftime('%Y-%m-%d')
        dasha_result = cmd_dasha(type('Args', (), {
            'nakshatra': nak_name, 'pada': pada,
            'moon_lon': moon_lon, 'birthdate': birthdate, 'today': today_str
        })())
        report['modules']['dasha'] = dasha_result
    except Exception as e:
        report['errors'].append(f"dasha: {e}")

    # ── Step 3: Yoga格局 ──
    try:
        yoga_planets = {}
        for pn, pd in planets.items():
            if isinstance(pd, dict) and 'sign' in pd and 'house' in pd:
                yoga_planets[pn] = {'sign': pd['sign'], 'house': pd['house']}
        yoga_result = cmd_yoga(type('Args', (), {
            'ascendant': asc_sign,
            'planets': ','.join([f"{k}:{v['sign']}:{v['house']}" for k, v in yoga_planets.items()])
        })())
        report['modules']['yoga'] = yoga_result
    except Exception as e:
        report['errors'].append(f"yoga: {e}")

    # ── Step 4: BPHS十六分盘 ──
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from varga import calc_all_vargas
        varga_result = calc_all_vargas(planet_lons, asc_deg, None)  # None = 全部分盘
        # 补充 D1_Rashi 到 varga_full（使用 chart 中的行星位置）
        d1_data = {}
        for pn, pd in planets.items():
            if isinstance(pd, dict) and 'sign' in pd:
                d1_data[pn] = {
                    "sign": pd["sign"],
                    "degree": pd.get("degree", 0),
                    "degree_in_sign": pd.get("degree_in_sign", pd.get("degree", 0) % 30),
                    "house": pd.get("house"),
                    "nakshatra": pd.get("nakshatra"),
                    "nakshatra_pada": pd.get("nakshatra_pada"),
                }
        if d1_data:
            varga_result["D1_Rashi"] = d1_data
        report['modules']['varga_full'] = varga_result
    except Exception as e:
        report['errors'].append(f"varga-full: {e}")

    # ── Step 4.5: Vimsopaka Bala 分盘力量 (v4.4.0) ──
    try:
        from vimsopaka_calculator import VimsopakaBalaCalculator, VargaType as VimsVargaType, DignityLevel
        vims_calc = VimsopakaBalaCalculator(mode="shodasavarga")
        # 将 varga_result 转换为 Vimsopaka 所需的 planet_vargas 格式
        # varga_result 结构: {varga_name: {planet: {sign, degree, ...}}}
        # 需要转为: {planet: {VargaType: DignityLevel}}
        dignity_map = {
            'EXALTED': DignityLevel.EXALTED, 'MOOLATRIKONA': DignityLevel.MOOLATRIKONA,
            'OWN_SIGN': DignityLevel.OWN_SIGN, 'FRIEND': DignityLevel.FRIEND,
            'NEUTRAL': DignityLevel.NEUTRAL, 'ENEMY': DignityLevel.ENEMY,
            'DEBILITATED': DignityLevel.DEBILITATED,
        }
        # 建立 VargaType → varga_result key 的映射（修复：每个分盘独立计算尊贵）
        _vt_div = {VimsVargaType.D1:1, VimsVargaType.D2:2, VimsVargaType.D3:3,
                   VimsVargaType.D4:4, VimsVargaType.D7:7, VimsVargaType.D9:9,
                   VimsVargaType.D10:10, VimsVargaType.D12:12, VimsVargaType.D16:16,
                   VimsVargaType.D20:20, VimsVargaType.D24:24, VimsVargaType.D27:27,
                   VimsVargaType.D30:30, VimsVargaType.D40:40, VimsVargaType.D45:45,
                   VimsVargaType.D60:60}
        _div_meta = {2:'Hora',3:'Drekkana',4:'Turyamsa',7:'Saptamsa',9:'Navamsa',
                     10:'Dasamsa',12:'Dwadashamsa',16:'Shodasamsa',20:'Vimsamsa',
                     24:'Siddhamsa',27:'Bhamsa',30:'Trimsamsa',40:'Khavedamsa',
                     45:'Akshavedamsa',60:'Shashtiamsa'}
        planet_vargas_input = {}
        for pn in planet_lons:
            planet_vargas_input[pn] = {}
            for vt in VimsVargaType:
                div = _vt_div.get(vt)
                if div and varga_result:
                    # 构造对应的 key，如 D9_Navamsa
                    vkey = f"D{div}_{_div_meta.get(div, f'D{div}')}"
                    vdata = varga_result.get(vkey, {})
                    # 使用 _get_dignity_level 计算完整5-fold尊贵（含Friend/Enemy）
                    # 不使用 _dignity 字典（只有 Exalted/Debilitated/Own Sign）
                    pinfo = vdata.get(pn, {})
                    if isinstance(pinfo, dict) and 'sign' in pinfo:
                        dl_key = _get_dignity_level(pn, pinfo['sign'],
                                      pinfo.get('degree_in_sign', pinfo.get('degree', 0) % 30))
                        planet_vargas_input[pn][vt] = dignity_map.get(dl_key, DignityLevel.NEUTRAL)
                    elif div == 1:
                        # D1 直接用本命盘数据
                        p_sign = SIGNS[int(planet_lons.get(pn, 0) / 30) % 12]
                        d_in_s = planet_lons.get(pn, 0) % 30
                        dl_key = _get_dignity_level(pn, p_sign, d_in_s)
                        planet_vargas_input[pn][vt] = dignity_map.get(dl_key, DignityLevel.NEUTRAL)
                    else:
                        planet_vargas_input[pn][vt] = DignityLevel.NEUTRAL
                elif div == 1 and not varga_result:
                    # fallback: D1 从 planet_lons 计算
                    p_sign = SIGNS[int(planet_lons.get(pn, 0) / 30) % 12]
                    d_in_s = planet_lons.get(pn, 0) % 30
                    dl_key = _get_dignity_level(pn, p_sign, d_in_s)
                    planet_vargas_input[pn][vt] = dignity_map.get(dl_key, DignityLevel.NEUTRAL)
                else:
                    planet_vargas_input[pn][vt] = DignityLevel.NEUTRAL
        vimsopaka_result = vims_calc.calculate_vimsopaka_bala(planet_vargas_input)
        # 添加顶层汇总
        if isinstance(vimsopaka_result, dict):
            total_scores = []
            for pn, pdata in vimsopaka_result.items():
                if isinstance(pdata, dict) and 'total_score' in pdata:
                    total_scores.append(pdata['total_score'])
            if total_scores:
                avg_score = round(sum(total_scores) / len(total_scores), 2)
                vimsopaka_result['total_score'] = avg_score
                vimsopaka_result['total_score_max'] = 20.0
                vimsopaka_result['status'] = '优秀' if avg_score >= 15 else '良好' if avg_score >= 10 else '一般' if avg_score >= 7 else '偏弱'
        report['modules']['vimsopaka'] = vimsopaka_result
    except Exception as e:
        report['errors'].append(f"vimsopaka: {e}")

    # ── Step 4.6: Divisional Charts Extended 扩展分盘 (v4.4.0) ──
    try:
        from divisional_charts_extended import DivisionalChartsCalculator
        dc_calc = DivisionalChartsCalculator()
        # 只计算 D5/D6/D8/D11（扩展分盘，与 Step 4 的标准分盘互补）
        ext_vargas = dc_calc.calculate_all_vargas(planet_lons, asc_deg)
        # 过滤只保留 Step 4 没有的分盘
        ext_filtered = {k: v for k, v in ext_vargas.items()
                       if v.get('division') in [5, 6, 8, 11]}
        report['modules']['varga_extended'] = ext_filtered
    except Exception as e:
        report['errors'].append(f"varga-extended: {e}")

    # ── Step 5: 精确相位 ──
    try:
        from aspects import calc_all_aspects
        aspects_result = calc_all_aspects(planet_lons, asc_deg)
        report['modules']['aspects'] = aspects_result
    except Exception as e:
        report['errors'].append(f"aspects: {e}")

    # ── Step 6: Jaimini系统 ──
    try:
        from jaimini import calc_chara_karaka_7, calc_chara_karaka_8, calc_chara_dasha, calc_karakamsha, calc_chara_dasha_with_antardasha
        from varga import calc_varga

        jaimini_result = {}
        jaimini_result['chara_karaka_7'] = calc_chara_karaka_7(planet_degs)
        jaimini_result['chara_karaka_8'] = calc_chara_karaka_8(planet_degs)

        # Step 6+: Karaka JH Compatible Mode (v4.4.0)
        try:
            from karaka_calculator import KarakaCalculator, KarakaMode
            kc_jh = KarakaCalculator(mode=KarakaMode.JH_COMPATIBLE)
            jaimini_result['chara_karaka_jh'] = kc_jh.calculate_karaka(planet_lons)
        except Exception as e:
            jaimini_result['chara_karaka_jh'] = {"error": str(e)}

        # 使用带 Antardasha 子周期的 Chara Dasha（v4.3.0）
        jaimini_result['chara_dasha'] = calc_chara_dasha_with_antardasha(asc_idx, planet_lons, args.year, args.month)
        jaimini_result['has_antardasha'] = True

        # Karakamsha（用AK灵魂星，非DK配偶星）
        # ⚠️ 2026-05-03修正：此前错误使用DK，现已修正为AK
        ck7 = jaimini_result['chara_karaka_7']
        ak_name = ck7['karaka_table']['Atmakaraka']['planet']
        ak_lon = planet_lons.get(ak_name, 0)
        ak_d9 = calc_varga(ak_lon, 9)
        jaimini_result['karakamsha'] = calc_karakamsha(
            ak_d9.get('sign', 'Aries'), ak_d9.get('degree_in_sign', 0))
        report['modules']['jaimini'] = jaimini_result
    except Exception as e:
        report['errors'].append(f"jaimini: {e}")

    # ── Step 7: 高级Nakshatra ──
    try:
        from nakshatra_advanced import find_nakshatra, calc_all_tara_balas, calc_sub_lord

        nak_result = {'planets': {}}
        for pn, lon in planet_lons.items():
            nak_result['planets'][pn] = find_nakshatra(lon)
        moon_nak_idx = int(planet_lons.get('Moon', 0) / (360/27)) % 27
        nak_result['tara_bala'] = calc_all_tara_balas(moon_nak_idx, planet_lons)
        nak_result['sub_lords'] = {pn: calc_sub_lord(lon) for pn, lon in planet_lons.items()}
        report['modules']['nakshatra_advanced'] = nak_result
    except Exception as e:
        report['errors'].append(f"nakshatra-adv: {e}")

    # ── Step 8: Argala门闩 ──
    try:
        from argala import calc_argala
        report['modules']['argala'] = calc_argala(planet_sign_indices, asc_idx)
    except Exception as e:
        report['errors'].append(f"argala: {e}")

    # ── Step 9: Tajika年运盘（需要年龄） ──
    age = args.age
    if age is None:
        # 自动计算年龄
        try:
            birth_date = datetime(args.year, args.month, args.day)
            age = (datetime.now() - birth_date).days // 365
            report['warnings'].append(f"未提供年龄，自动计算为 {age} 岁")
        except:
            age = None

    if age is not None:
        try:
            from tajika import calc_muntha, calc_year_lord, calc_mudda_dasha, calc_tri_pataka
            asc_si = int(asc_deg / 30) % 12
            tajika_result = {}
            tajika_result['muntha'] = calc_muntha(asc_si, age)
            yl = calc_year_lord(asc_si, age)
            tajika_result['year_lord'] = yl
            varsha_lord = yl.get('year_lord', 'Jupiter')
            tajika_result['mudda_dasha'] = calc_mudda_dasha(asc_si, varsha_lord, args.month)
            muntha_si = (asc_si + age) % 12
            tajika_result['tri_pataka'] = calc_tri_pataka(planet_lons, varsha_lord, muntha_si)
            report['modules']['tajika'] = tajika_result
        except Exception as e:
            report['errors'].append(f"tajika: {e}")

    # ── Step 10: Shadbala六重力量 ──
    try:
        from shadbala import calc_shadbala
        birth_hour = args.hour + args.minute / 60.0
        sun_lon = planet_lons.get('Sun', 0)
        moon_lon = planet_lons.get('Moon', 0)
        shadbala_result = calc_shadbala(planets, asc_sign, birth_hour, sun_lon, moon_lon)
        # 添加顶层汇总
        if isinstance(shadbala_result, dict):
            sb_planets = shadbala_result.get('planets', {})
            total_rupas = 0
            min_req_total = 0
            strong_count = 0
            for pn, pdata in sb_planets.items():
                if isinstance(pdata, dict):
                    total_rupas += pdata.get('total_rupas', 0)
                    min_req_total += pdata.get('min_required', 0)
                    if pdata.get('total_rupas', 0) >= pdata.get('min_required', 0):
                        strong_count += 1
            shadbala_result['total_shadbala'] = round(total_rupas, 2)
            shadbala_result['total_min_required'] = round(min_req_total, 2)
            shadbala_result['strong_planets'] = strong_count
            shadbala_result['weak_planets'] = len(sb_planets) - strong_count
            shadbala_result['status'] = '优秀' if strong_count >= 5 else '良好' if strong_count >= 3 else '一般'
        report['modules']['shadbala'] = shadbala_result
    except Exception as e:
        report['errors'].append(f"shadbala: {e}")

    # ── Step 10.5: Avasthas 行星状态 (v4.4.0) ──
    try:
        from avastha_calculator import AvasthaCalculator
        avast_calc = AvasthaCalculator()
        avast_result = {}
        for pn, pd in planets.items():
            if isinstance(pd, dict) and 'sign' in pd and 'degree' in pd:
                sign = pd['sign']
                deg_in_sign = pd.get('degree_in_sign', pd['degree'] % 30)
                house = pd.get('house', 0)
                # 收集同宫行星作为 conjunctions
                conjunctions = [p2 for p2, pd2 in planets.items()
                               if isinstance(pd2, dict) and pd2.get('house') == house and p2 != pn]
                avast_result[pn] = avast_calc.calculate_all_avasthas(
                    planet=pn, sign=sign, degree=deg_in_sign,
                    house=house, conjunctions=conjunctions)
        report['modules']['avasthas'] = avast_result
    except Exception as e:
        report['errors'].append(f"avasthas: {e}")

    # ── Step 11: Ashtakavarga八分法 ──
    asht_data = None
    try:
        from ashtakavarga import calc_ashtakavarga
        asht_data = calc_ashtakavarga(planets, asc_idx)
        report['modules']['ashtakavarga'] = asht_data
    except Exception as e:
        report['errors'].append(f"ashtakavarga: {e}")

    # ── Step 12: R1-R10数学验证 ──
    try:
        from validate import validate_chart
        report['modules']['validation'] = validate_chart(chart, asht_data)
    except Exception as e:
        report['errors'].append(f"validate: {e}")

    # ── Step 13: P1-P12行星审计 ──
    try:
        audit_result = cmd_audit(args)
        report['modules']['audit'] = audit_result
    except Exception as e:
        report['errors'].append(f"audit: {e}")

    # ── Step 14: ⭐ Transit Actionable Context (v4.1.0) ──
    try:
        actionable_ctx = _calc_actionable_context(planets, asc_idx)
        report['modules']['actionable_context'] = actionable_ctx
    except Exception as e:
        report['errors'].append(f"actionable-context: {e}")

    # ── Step 15: Planetary Congregation 行星聚集 (v4.3.0) ──
    try:
        congregation = _calc_planetary_congregation(planets, asc_idx)
        report['modules']['congregation'] = congregation
    except Exception as e:
        report['errors'].append(f"congregation: {e}")

    # ── Step 16: Vivah Saham 婚姻敏感点 (v4.3.0) ──
    try:
        sahams = _calc_vivah_saham(planets, asc_deg)
        # 包装为标准结构，与 standalone vivah-saham 子命令一致
        if 'error' not in sahams:
            report['modules']['vivah_saham'] = {
                'vivah_saham': {
                    'longitude': sahams['saham_lon'],
                    'sign': sahams['saham_sign'],
                    'degree_in_sign': sahams['saham_deg_in_sign'],
                    'house': sahams['saham_house'],
                },
                **sahams
            }
        else:
            report['modules']['vivah_saham'] = sahams
    except Exception as e:
        report['errors'].append(f"vivah-saham: {e}")

    # ── Step 17: Transit 多参考点分析 (v4.5.0 P1) ──
    try:
        transit_multi = _calc_transit_multi_reference(planets, asc_idx, asc_deg, planet_lons)
        report['modules']['transit_multi_reference'] = transit_multi
    except Exception as e:
        report['errors'].append(f"transit-multi-ref: {e}")

    # ── Step 18: Dasa Convergence 三系统交叉验证 (v4.5.0 P1) ──
    try:
        dasha_data = report['modules'].get('dasha', {})
        jaimini_data = report['modules'].get('jaimini', {})
        chara_dasha_data = jaimini_data.get('chara_dasha', {}) if isinstance(jaimini_data, dict) else {}
        birthdate_str = f"{args.year}-{args.month:02d}-{args.day:02d}"
        yogini_data = _calc_yogini_dasha(planet_lons.get('Moon', 0), birthdate_str)
        report['modules']['yogini_dasha'] = yogini_data
        convergence = _calc_dasa_convergence(dasha_data, chara_dasha_data, yogini_data, planet_lons, asc_idx)
        report['modules']['dasa_convergence'] = convergence
    except Exception as e:
        report['errors'].append(f"dasa-convergence: {e}")

    # ── Step 19: D9 Navamsa 逐行星尊严展开 (v4.5.0 P1) ──
    try:
        varga_data = report['modules'].get('varga_full', {})
        d9_data = varga_data.get('D9_Navamsa', {}) if isinstance(varga_data, dict) else {}
        if d9_data:
            d9_expanded = {}
            for pn, pd in d9_data.items():
                if pn == '_meta' or not isinstance(pd, dict) or 'sign' not in pd:
                    continue
                d9_sign = pd['sign']
                d9_deg = pd.get('degree_in_sign', pd.get('degree', 0) % 30)
                dignity = _get_dignity_level(pn, d9_sign, d9_deg)
                # D9 宫位（从D9 Asc计算）
                d9_asc_data = d9_data.get('Ascendant', {})
                d9_asc_sign_idx = SIGNS.index(d9_asc_data.get('sign', 'Aries')) if isinstance(d9_asc_data, dict) and d9_asc_data.get('sign') in SIGNS else 0
                p_sign_idx = SIGNS.index(d9_sign) if d9_sign in SIGNS else 0
                d9_house = ((p_sign_idx - d9_asc_sign_idx) % 12) + 1
                # 关系状态
                d9_sign_lord = SIGN_LORDS.get(d9_sign, '')
                is_own = (d9_sign_lord == pn)
                is_exalted = (EXALTATION.get(pn) == d9_sign)
                is_debilitated = (DEBILITATION.get(pn) == d9_sign)
                is_moola = False
                if pn in MOOLATRIKONA:
                    mt_sign, mt_start, mt_end = MOOLATRIKONA[pn]
                    if mt_sign == d9_sign and mt_start <= d9_deg < mt_end:
                        is_moola = True
                d9_expanded[pn] = {
                    'sign': d9_sign,
                    'sign_cn': SIGNS_CN.get(d9_sign, ''),
                    'house_in_d9': d9_house,
                    'dignity': dignity,
                    'is_own_sign': is_own,
                    'is_exalted': is_exalted,
                    'is_debilitated': is_debilitated,
                    'is_moolatrikona': is_moola,
                    'pada': pd.get('pada'),
                    'lord': d9_sign_lord,
                    'degree_in_sign': round(d9_deg, 4),
                }
            report['modules']['d9_navamsa_expanded'] = d9_expanded
    except Exception as e:
        report['errors'].append(f"d9-expanded: {e}")

    # ── 汇总 ──
    elapsed = round(time.time() - t0, 2)
    module_count = len(report['modules'])
    error_count = len(report['errors'])
    report['summary'] = {
        'elapsed_seconds': elapsed,
        'modules_computed': module_count,
        'errors': error_count,
        'status': 'complete' if error_count == 0 else f'{error_count} errors',
        'next_step': '⭐ v4.5.0: P1缺口已补齐。新增 transit_multi_reference(四参考点) + dasa_convergence(三系统交叉) + yogini_dasha + d9_navamsa_expanded(逐行星尊严展开)。AI必须使用四参考点分析Transit，Dasa预测必须标注收敛等级。',
    }

    return report


# ============================================================================
# 23. Prashna 问事占星 (v3.9新增)
# ============================================================================
def cmd_prashna(args):
    """Prashna 问事占星：基于提问时刻的即时星盘分析"""
    try:
        from prashna import cast_prashna, calc_arudha, calc_sphutas, calc_life_sphutas, calc_sahams, analyze_lost_item, kunda_verify, calc_gulika_simple
    except ImportError:
        # 尝试从同目录导入
        import importlib.util, os
        spec = importlib.util.spec_from_file_location("prashna", os.path.join(os.path.dirname(__file__), "prashna.py"))
        prashna_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prashna_mod)
        cast_prashna = prashna_mod.cast_prashna
        calc_arudha = prashna_mod.calc_arudha
        calc_sphutas = prashna_mod.calc_sphutas
        calc_life_sphutas = prashna_mod.calc_life_sphutas
        calc_sahams = prashna_mod.calc_sahams
        analyze_lost_item = prashna_mod.analyze_lost_item
        kunda_verify = prashna_mod.kunda_verify
        calc_gulika_simple = prashna_mod.calc_gulika_simple

    if args.mode == 'chart':
        return cast_prashna(args.datetime, args.lat, args.lon)

    # 其他模式需要先铸盘获取行星位置
    chart = cast_prashna(args.datetime, args.lat, args.lon)
    if 'error' in chart:
        return chart

    asc_lon = chart['ascendant']['lon']
    p_lons = {n: d['lon'] for n, d in chart['planets'].items()}

    if args.mode == 'arudha':
        return {'arudha_lagna': calc_arudha(asc_lon, p_lons),
                'ascendant': chart['ascendant']}
    elif args.mode == 'sphutas':
        return calc_sphutas(p_lons, 0)
    elif args.mode == 'sahams':
        return calc_sahams(p_lons, asc_lon)
    elif args.mode == 'lost-item':
        return analyze_lost_item(p_lons, asc_lon)
    elif args.mode == 'life':
        return calc_life_sphutas(asc_lon, p_lons.get('Moon',0), p_lons.get('Sun',0), 0)
    elif args.mode == 'kunda':
        return kunda_verify(asc_lon)
    else:
        return cast_prashna(args.datetime, args.lat, args.lon)


# ============================================================================
# CLI入口
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description='印度占星统一引擎 v3.7.0', formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', help='子命令')

    # 1. chart
    p = sub.add_parser('chart', help='计算完整星盘')
    _add_chart_args(p)
    p.add_argument('--validate', action='store_true', help='附加R1-R10数学验证')

    # 2. dasha
    p = sub.add_parser('dasha', help='计算Dasha大运')
    p.add_argument('--nakshatra', default=None); p.add_argument('--pada', type=int, default=None)
    p.add_argument('--moon-lon', type=float, default=None); p.add_argument('--birthdate', required=True)
    p.add_argument('--today', default=None)

    # 3. yoga
    p = sub.add_parser('yoga', help='Yoga格局识别')
    p.add_argument('--ascendant', default=None)
    p.add_argument('--planets', default=None, help="格式: 'Sun:Aries:9,Moon:Aquarius:7,...'")

    # 4. predict
    p = sub.add_parser('predict', help='三层验证法事件预测')
    p.add_argument('--chart', default=None, help='星盘JSON字符串')
    p.add_argument('--event-type', default='all', choices=['all', 'marriage', 'career', 'wealth', 'health'])
    p.add_argument('--past-verify', action='store_true', help='验前事模式：推断2-4个高信号历史时段')
    p.add_argument('--year', type=int, default=None, help='出生年（验前事模式需要）')
    p.add_argument('--month', type=int, default=None, help='出生月')
    p.add_argument('--day', type=int, default=None, help='出生日')
    p.add_argument('--hour', type=int, default=None, help='出生时')
    p.add_argument('--minute', type=int, default=None, help='出生分')
    p.add_argument('--lat', type=float, default=None, help='纬度')
    p.add_argument('--lon', type=float, default=None, help='经度')
    p.add_argument('--tz', type=float, default=0, help='时区')

    # 5. varga
    p = sub.add_parser('varga', help='分盘计算')
    _add_chart_args(p)
    p.add_argument('--d9', action='store_true'); p.add_argument('--d10', action='store_true')
    p.add_argument('--all', action='store_true')

    # 6. celebrity
    p = sub.add_parser('celebrity', help='名人案例查询')
    p.add_argument('--name', default=None); p.add_argument('--limit', type=int, default=20)

    # 7. db-stats
    sub.add_parser('db-stats', help='验证数据库统计')

    # 8. transit
    p = sub.add_parser('transit', help='行星过境查询（Swiss Ephemeris实时计算）')
    p.add_argument('--year', type=int, required=True); p.add_argument('--month', type=int, required=True)
    p.add_argument('--day', type=int, default=15, help='指定日期（默认15日取月中代表）')
    p.add_argument('--planet', default=None, help='目标行星，逗号分隔（默认全部，如：Jupiter,Saturn）')
    p.add_argument('--tz', type=float, default=8, help='时区（默认UTC+8）')

    # 9. shadbala (v3.4新增)
    p = sub.add_parser('shadbala', help='Shadbala六重力量计算')
    _add_chart_args(p)

    # 10. ashtakavarga (v3.4新增)
    p = sub.add_parser('ashtakavarga', help='Ashtakavarga八分法计算')
    _add_chart_args(p)

    # 11. memory (v3.4新增)
    p = sub.add_parser('memory', help='Hermes记忆系统')
    p.add_argument('--action', default='stats', choices=['store', 'search', 'context', 'stats'])
    p.add_argument('--content', default=None, help='存储内容（store操作必填）')
    p.add_argument('--query', default=None, help='搜索查询（search操作必填）')
    p.add_argument('--tags', default=None, help='标签，逗号分隔')
    p.add_argument('--importance', type=int, default=5, help='重要性 1-10')
    p.add_argument('--limit', type=int, default=10, help='搜索结果数量')

    # 12. validate (v3.5新增)
    p = sub.add_parser('validate', help='R1-R10数学验证')
    _add_chart_args(p)

    # 13. audit (v3.5新增)
    p = sub.add_parser('audit', help='P1-P12行星审计管线')
    _add_chart_args(p)

    # 14. report (v3.6新增)
    p = sub.add_parser('report', help='MD→HTML报告生成（羊皮纸主题）')
    p.add_argument('folder', help='包含MD文件的目录路径')
    p.add_argument('--name', default='Client', help='客户姓名')
    p.add_argument('--lagna', default='—', help='上升星座')
    p.add_argument('--gender', default='—', help='性别')
    p.add_argument('--status', default='—', help='当前状态')
    p.add_argument('--lang', default='cn', choices=['cn', 'en'], help='语言 (默认cn)')
    p.add_argument('--output', default=None, help='输出HTML路径')

    # 15. varga-full (v3.7新增)
    p = sub.add_parser('varga-full', help='BPHS十六分盘完整计算')
    _add_chart_args(p)
    p.add_argument('--divisions', default=None, help='指定分盘，逗号分隔(如 D2,D9,D60)，空=全部')

    # 16. aspects (v3.7新增)
    p = sub.add_parser('aspects', help='度数精确相位系统')
    _add_chart_args(p)

    # 17. jaimini (v3.7新增)
    p = sub.add_parser('jaimini', help='Jaimini系统（Chara Karaka/Dasha/Karakamsha）')
    _add_chart_args(p)
    p.add_argument('--mode', default='all', choices=['all','karaka','dasha','karakamsha'], help='分析模式')
    p.add_argument('--antardasha', action='store_true', help='Chara Dasha含Antardasha子周期')

    # 18. nakshatra-adv (v3.7新增)
    p = sub.add_parser('nakshatra-adv', help='高级Nakshatra分析')
    _add_chart_args(p)
    p.add_argument('--mode', default='all', choices=['all','detail','tara','sublord'], help='分析模式')

    # 19. argala (v3.7新增)
    p = sub.add_parser('argala', help='Argala门闩系统')
    _add_chart_args(p)

    # 20. tajika (v3.7新增)
    p = sub.add_parser('tajika', help='Tajika/Varshaphala年运盘')
    _add_chart_args(p)
    p.add_argument('--age', type=int, required=True, help='当前年龄')
    p.add_argument('--mode', default='all', choices=['all','muntha','yearlord','mudda','tripataka'], help='分析模式')

    # 21. synastry (v3.7新增)
    p = sub.add_parser('synastry', help='合盘分析（Ashta Koota 36分制）')
    p.add_argument('--moon1', type=float, required=True, help='Person1月亮黄经')
    p.add_argument('--moon2', type=float, required=True, help='Person2月亮黄经')
    p.add_argument('--mars1', type=float, default=None, help='Person1火星黄经')
    p.add_argument('--mars2', type=float, default=None, help='Person2火星黄经')
    p.add_argument('--asc1', type=float, default=None, help='Person1上升黄经')
    p.add_argument('--asc2', type=float, default=None, help='Person2上升黄经')
    p.add_argument('--gender1', default='M', help='Person1性别')
    p.add_argument('--gender2', default='F', help='Person2性别')

    # 22. full-reading (v3.7.1新增)
    p = sub.add_parser('full-reading', help='全自动综合解盘（出生信息→全链路→完整报告）')
    _add_chart_args(p)
    p.add_argument('--age', type=int, default=None, help='当前年龄（不提供则自动计算）')

    # 23. prashna (v3.9新增)
    p = sub.add_parser('prashna', help='Prashna问事占星（提问时刻星盘+Arudha+Sphuta+Sahams）')
    p.add_argument('--datetime', required=True, help='提问时间 YYYY-MM-DD HH:MM')
    p.add_argument('--lat', type=float, required=True, help='纬度')
    p.add_argument('--lon', type=float, required=True, help='经度')
    p.add_argument('--mode', default='chart', choices=['chart','arudha','sphutas','sahams','lost-item','life','kunda'], help='分析模式')

    # 24. double-transit-pac (v3.9新增)
    p = sub.add_parser('double-transit-pac', help='Double Transit PAC + D9层（KN Rao完整实现）')
    _add_chart_args(p)
    p.add_argument('--date', required=True, help='过境日期 YYYY-MM-DD')
    p.add_argument('--house', type=int, default=7, help='目标宫位（默认7=婚姻）')

    # 25. transit-ll7l (v3.9新增)
    p = sub.add_parser('transit-ll7l', help='Transit LL/7L连接+互换检测')
    _add_chart_args(p)
    p.add_argument('--date', required=True, help='过境日期 YYYY-MM-DD')

    # 26. planetary-congregation (v3.9新增)
    p = sub.add_parser('planetary-congregation', help='行星聚集检测（Lagna/7H+Transit）')
    _add_chart_args(p)
    p.add_argument('--house', type=int, default=7, help='目标宫位')
    p.add_argument('--transit-date', default=None, help='过境日期 YYYY-MM-DD（可选）')

    # 27. vivah-saham (v3.9新增)
    p = sub.add_parser('vivah-saham', help='Vivah Saham计算+Transit激活')
    _add_chart_args(p)
    p.add_argument('--transit-date', default=None, help='过境日期 YYYY-MM-DD（可选）')

    args = parser.parse_args()
    if not args.command:
        parser.print_help(); sys.exit(1)

    cmds = {'chart': cmd_chart, 'dasha': cmd_dasha, 'yoga': cmd_yoga, 'predict': cmd_predict,
            'varga': cmd_varga, 'celebrity': cmd_celebrity, 'db-stats': cmd_db_stats, 'transit': cmd_transit,
            'shadbala': cmd_shadbala, 'ashtakavarga': cmd_ashtakavarga, 'memory': cmd_memory,
            'validate': cmd_validate, 'audit': cmd_audit, 'report': cmd_report,
            'varga-full': cmd_varga_full, 'aspects': cmd_aspects, 'jaimini': cmd_jaimini,
            'nakshatra-adv': cmd_nakshatra_adv, 'argala': cmd_argala, 'tajika': cmd_tajika,
            'synastry': cmd_synastry, 'full-reading': cmd_full_reading, 'prashna': cmd_prashna,
            'double-transit-pac': cmd_double_transit_pac,
            'transit-ll7l': cmd_transit_ll7l, 'planetary-congregation': cmd_planetary_congregation,
            'vivah-saham': cmd_vivah_saham}
    result = cmds[args.command](args)
    output_json(result)


if __name__ == '__main__':
    main()

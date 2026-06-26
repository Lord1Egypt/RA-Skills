#!/usr/bin/env python3
"""
Prashna Shastra（问事占星）计算引擎 v1.0
Jyotish Vedic Astrology Skill - Prashna Module
依赖: pyswisseph
"""

import math, json, argparse
from datetime import datetime, timedelta

SIGN_NAMES = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
              'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_CN = ['白羊座','金牛座','双子座','巨蟹座','狮子座','处女座',
           '天秤座','天蝎座','射手座','摩羯座','水瓶座','双鱼座']
SIGN_LORDS = ['Mars','Venus','Mercury','Moon','Sun','Mercury',
              'Venus','Mars','Jupiter','Saturn','Saturn','Jupiter']
PLANET_CN = {'Sun':'太阳','Moon':'月亮','Mars':'火星','Mercury':'水星',
             'Jupiter':'木星','Venus':'金星','Saturn':'土星','Rahu':'罗睺','Ketu':'计都'}

GULIKA_DAY = {'Sunday':26,'Monday':22,'Tuesday':18,'Wednesday':14,'Thursday':10,'Friday':6,'Saturday':2}
GULIKA_NIGHT = {'Sunday':10,'Monday':6,'Tuesday':2,'Wednesday':26,'Thursday':22,'Friday':18,'Saturday':14}

SAHAM_DEFS = {
    'Punya':('福德','Moon','Sun','Asc'), 'Vidya':('学业','Sun','Moon','Asc'),
    'Bhratru':('兄弟','Jupiter','Saturn','Asc'), 'Pitru':('父亲','Saturn','Sun','Asc'),
    'Putra':('子女','Jupiter','Moon','Asc'), 'Vivaha':('婚姻','Venus','Saturn','Asc'),
    'Karma':('职业','Mars','Mercury','Asc'), 'Roga':('疾病','Asc','Moon','Asc'),
    'Raja':('权力','Saturn','Sun','Asc'), 'Asha':('愿望','Saturn','Mars','Asc'),
    'Matru':('母亲','Moon','Venus','Asc'), 'Jeeva':('生计','Saturn','Jupiter','Asc'),
    'Kali':('冲突','Jupiter','Mars','Asc'), 'Satru':('敌人','Mars','Saturn','Asc'),
    'Paradesa':('出国','H9','H9Lord','Asc'), 'Mrityu':('死亡','H8','Moon','Asc'),
    'Vidya':('学业','Sun','Moon','Asc'), 'Artha':('财富','H2','H2Lord','Asc'),
    'Vyapara':('商业','Mars','Saturn','Asc'), 'Bandhana':('监禁','Punya','Saturn','Asc'),
}

def sign_of(lon): return int((lon % 360) / 30)
def norm(lon): return lon % 360
def lon_cn(lon):
    s, d = sign_of(lon), lon % 30
    return f"{SIGN_CN[s]} {int(d)}°{int((d%1)*60)}'"

# ── Arudha Lagna ──
def calc_arudha(asc_lon, planet_lons):
    asc_s = sign_of(asc_lon)
    lord = SIGN_LORDS[asc_s]
    lord_lon = planet_lons.get(lord, 0)
    lord_s = sign_of(lord_lon)
    count = ((lord_s - asc_s) % 12) or 12
    al_s = (lord_s + count) % 12
    if al_s == asc_s or al_s == (asc_s + 6) % 12:
        al_s = (al_s + 10) % 12
    al_lon = al_s * 30 + (asc_lon % 30)
    return {'longitude': norm(al_lon), 'sign_cn': SIGN_CN[al_s], 'lord': lord}

# ── Gulika ──
def calc_gulika_simple(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    dn = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][dt.weekday()]
    is_day = 6 <= dt.hour < 18
    gh = GULIKA_DAY.get(dn, 14) if is_day else GULIKA_NIGHT.get(dn, 14)
    return {'ghatika': gh, 'minutes': gh*24, 'day': dn, 'is_daytime': is_day}

# ── Sphuta 组合 ──
def calc_sphutas(planet_lons, gulika_lon=0):
    sun, moon = planet_lons.get('Sun',0), planet_lons.get('Moon',0)
    rahu = planet_lons.get('Rahu',0)
    tri = norm(sun + moon + gulika_lon)
    catu = norm(tri + sun)
    pancha = norm(catu + rahu)
    return {'trisphuta': {'lon': tri, 'cn': lon_cn(tri)},
            'catusphuta': {'lon': catu, 'cn': lon_cn(catu)},
            'pancasphuta': {'lon': pancha, 'cn': lon_cn(pancha)}}

# ── Prana/Deha/Mrityu ──
def calc_life_sphutas(asc_lon, moon_lon, sun_lon, gulika_lon):
    prana = norm(asc_lon * 5 + gulika_lon)
    deha = norm(moon_lon * 8 + gulika_lon)
    mrityu = norm(gulika_lon * 7 + sun_lon)
    danger = norm(prana + deha) < mrityu
    return {'prana_cn': lon_cn(prana), 'deha_cn': lon_cn(deha), 'mrityu_cn': lon_cn(mrityu),
            'judgment': '⚠️ 生命能量<死亡指标' if danger else '✅ 生命能量>死亡指标'}

# ── Sahams ──
def calc_sahams(planet_lons, asc_lon):
    asc_s = sign_of(asc_lon)
    vals = dict(planet_lons)
    vals['Asc'] = asc_lon
    vals['AscLord'] = planet_lons.get(SIGN_LORDS[asc_s], 0)
    vals['H2'] = (asc_s+1)%12*30+15; vals['H2Lord'] = planet_lons.get(SIGN_LORDS[(asc_s+1)%12], 0)
    vals['H8'] = (asc_s+7)%12*30+15; vals['H9'] = (asc_s+8)%12*30+15
    vals['H9Lord'] = planet_lons.get(SIGN_LORDS[(asc_s+8)%12], 0)

    results = {}
    for name, (cn, m, s, b) in SAHAM_DEFS.items():
        mv = vals.get(m, 0); sv = vals.get(s, 0); bv = vals.get(b, asc_lon)
        if name == 'Punya':
            pass  # Punya always computable
        elif isinstance(mv, str) or isinstance(sv, str):
            continue
        try:
            v = norm(mv - sv + bv)
            results[name] = {'cn': cn, 'longitude': round(v,4), 'sign_cn': SIGN_CN[sign_of(v)]}
        except: pass
    return results

# ── Kunda 验证 ──
def kunda_verify(asc_lon):
    mins = int(asc_lon * 60)
    idx = (mins * 81) % 12
    naks = ['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra',
            'Punarvasu','Pushya','Ashlesha','Magha','P.Phalguni','U.Phalguni']
    return {'derived_nakshatra': naks[idx] if idx < len(naks) else '?', 'index': idx}

# ── 失物分析 ──
def analyze_lost_item(planet_lons, asc_lon):
    asc_s = sign_of(asc_lon)
    h2_lord = SIGN_LORDS[(asc_s+1)%12]
    h7_lord = SIGN_LORDS[(asc_s+6)%12]
    h11_lord = SIGN_LORDS[(asc_s+10)%12]
    h2_lon = planet_lons.get(h2_lord, 0)
    h7_lon = planet_lons.get(h7_lord, 0)
    h2_elem = (asc_s+1) % 4
    dirs = {0:'东方(火象)', 1:'南方(土象)', 2:'西方(风象)', 3:'北方(水象)'}
    h7_house = (sign_of(h7_lon) - asc_s) % 12 + 1
    return {
        'item_lord': h2_lord, 'item_cn': PLANET_CN.get(h2_lord,''),
        'direction': dirs.get(h2_elem, '未知'),
        'thief_lord': h7_lord, 'thief_cn': PLANET_CN.get(h7_lord,''),
        'thief_in_house': h7_house,
        'thief_type': '已知/附近' if h7_house in [1,4,7,10] else '隐秘/远方' if h7_house in [6,8,12] else '待定',
        'recovery_lord': h11_lord, 'recovery_cn': PLANET_CN.get(h11_lord,'')
    }

# ── 完整 Prashna 星盘 ──
def cast_prashna(dt_str, lat, lon):
    try:
        import swisseph as swe
        swe.set_sid_mode(swe.SIDM_LAHIRI)
    except ImportError:
        return {'error': '需要 pip install pyswisseph'}

    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
    asc_lon = ascmc[0]

    p_lons = {}
    se_map = {0:'Sun',1:'Moon',2:'Mars',3:'Mercury',4:'Jupiter',5:'Venus',6:'Saturn'}
    for sid, name in se_map.items():
        r = swe.calc_ut(jd, sid, swe.FLG_SIDEREAL)
        p_lons[name] = r[0][0]
    rahu = swe.calc_ut(jd, 8, swe.FLG_SIDEREAL)[0][0]
    p_lons['Rahu'] = rahu; p_lons['Ketu'] = norm(rahu + 180)

    arudha = calc_arudha(asc_lon, p_lons)
    gulika = calc_gulika_simple(dt_str)
    sphutas = calc_sphutas(p_lons, 0)  # 简化无精确Gulika经度
    life = calc_life_sphutas(asc_lon, p_lons['Moon'], p_lons['Sun'], 0)
    sahams = calc_sahams(p_lons, asc_lon)
    kunda = kunda_verify(asc_lon)

    return {
        'time': dt_str, 'lat': lat, 'lon': lon,
        'ascendant': {'lon': round(asc_lon,4), 'cn': lon_cn(asc_lon),
                      'lord': SIGN_LORDS[sign_of(asc_lon)]},
        'planets': {n: {'lon': round(l,4), 'cn': lon_cn(l)} for n,l in p_lons.items()},
        'arudha_lagna': arudha,
        'sphutas': sphutas,
        'life_sphutas': life,
        'sahams': sahams,
        'kunda': kunda,
        'gulika_info': gulika
    }

# ── CLI ──
def main():
    p = argparse.ArgumentParser(description='Prashna Shastra Engine')
    sub = p.add_subparsers(dest='cmd')

    # chart
    ch = sub.add_parser('chart', help='铸造Prashna星盘')
    ch.add_argument('--datetime', required=True, help='提问时间 YYYY-MM-DD HH:MM')
    ch.add_argument('--lat', type=float, required=True)
    ch.add_argument('--lon', type=float, required=True)

    # arudha
    ar = sub.add_parser('arudha', help='计算Arudha Lagna')
    ar.add_argument('--asc-lon', type=float, required=True)
    ar.add_argument('--planet-lons', required=True, help='JSON: {"Sun":123.4,...}')

    # sphutas
    sp = sub.add_parser('sphutas', help='计算Sphuta组合')
    sp.add_argument('--planet-lons', required=True, help='JSON')
    sp.add_argument('--gulika-lon', type=float, default=0)

    # sahams
    sa = sub.add_parser('sahams', help='计算Sahams')
    sa.add_argument('--planet-lons', required=True, help='JSON')
    sa.add_argument('--asc-lon', type=float, required=True)

    # lost-item
    li = sub.add_parser('lost-item', help='失物查询')
    li.add_argument('--planet-lons', required=True, help='JSON')
    li.add_argument('--asc-lon', type=float, required=True)

    # life-sphutas
    ls = sub.add_parser('life', help='生命Sphuta')
    ls.add_argument('--asc-lon', type=float, required=True)
    ls.add_argument('--moon-lon', type=float, required=True)
    ls.add_argument('--sun-lon', type=float, required=True)
    ls.add_argument('--gulika-lon', type=float, required=True)

    args = p.parse_args()
    if args.cmd == 'chart':
        print(json.dumps(cast_prashna(args.datetime, args.lat, args.lon), ensure_ascii=False, indent=2))
    elif args.cmd == 'arudha':
        pl = json.loads(args.planet_lons)
        print(json.dumps(calc_arudha(args.asc_lon, pl), ensure_ascii=False, indent=2))
    elif args.cmd == 'sphutas':
        pl = json.loads(args.planet_lons)
        print(json.dumps(calc_sphutas(pl, args.gulika_lon), ensure_ascii=False, indent=2))
    elif args.cmd == 'sahams':
        pl = json.loads(args.planet_lons)
        print(json.dumps(calc_sahams(pl, args.asc_lon), ensure_ascii=False, indent=2))
    elif args.cmd == 'lost-item':
        pl = json.loads(args.planet_lons)
        print(json.dumps(analyze_lost_item(pl, args.asc_lon), ensure_ascii=False, indent=2))
    elif args.cmd == 'life':
        r = calc_life_sphutas(args.asc_lon, args.moon_lon, args.sun_lon, args.gulika_lon)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        p.print_help()

if __name__ == '__main__':
    main()

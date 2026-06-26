#!/usr/bin/env python3
"""
印度占星 Dasha 推算脚本
基于用户提供的星盘数据（月亮Nakshatra + 出生日期）推算大运/小运时间线

用法:
  python3 dasha_analyzer.py --nakshatra "Jyeshtha" --pada 3 --birthdate 1985-08-20
  python3 dasha_analyzer.py --moon-lon 226.5 --birthdate 1985-08-20
"""

import argparse
from datetime import datetime, timedelta

# Nakshatra 对应大运主星与年限
NAKSHATRA_LIST = [
    ("Ashwini",            "Ketu",    7),
    ("Bharani",            "Venus",   20),
    ("Krittika",           "Sun",     6),
    ("Rohini",             "Moon",    10),
    ("Mrigashira",         "Mars",    7),
    ("Ardra",              "Rahu",    18),
    ("Punarvasu",          "Jupiter", 16),
    ("Pushya",             "Saturn",  19),
    ("Ashlesha",           "Mercury", 17),
    ("Magha",              "Ketu",    7),
    ("Purva Phalguni",     "Venus",   20),
    ("Uttara Phalguni",    "Sun",     6),
    ("Hasta",              "Moon",    10),
    ("Chitra",             "Mars",    7),
    ("Swati",              "Rahu",    18),
    ("Vishakha",           "Jupiter", 16),
    ("Anuradha",           "Saturn",  19),
    ("Jyeshtha",           "Mercury", 17),
    ("Mula",               "Ketu",    7),
    ("Purva Ashadha",      "Venus",   20),
    ("Uttara Ashadha",     "Sun",     6),
    ("Shravana",           "Moon",    10),
    ("Dhanishtha",         "Mars",    7),
    ("Shatabhisha",        "Rahu",    18),
    ("Purva Bhadrapada",   "Jupiter", 16),
    ("Uttara Bhadrapada",  "Saturn",  19),
    ("Revati",             "Mercury", 17),
]

DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}

PLANET_CN = {
    "Ketu":"南交点 Ketu ☄️",
    "Venus":"金星 Venus ♀",
    "Sun":"太阳 Sun ☀️",
    "Moon":"月亮 Moon 🌙",
    "Mars":"火星 Mars ♂",
    "Rahu":"北交点 Rahu 🐉",
    "Jupiter":"木星 Jupiter ♃",
    "Saturn":"土星 Saturn ♄",
    "Mercury":"水星 Mercury ☿",
}

def fuzzy_match_nakshatra(name):
    """模糊匹配 Nakshatra 名称"""
    name_lower = name.lower().replace(" ", "").replace("-", "")
    for nak in NAKSHATRA_LIST:
        if name_lower in nak[0].lower().replace(" ", ""):
            return nak
        if nak[0].lower().replace(" ", "").startswith(name_lower[:5]):
            return nak
    return None

def lon_to_nakshatra(moon_lon):
    """月亮黄经（0-360）→ Nakshatra + Pada"""
    nak_span = 360 / 27
    pada_span = nak_span / 4
    idx = int(moon_lon / nak_span)
    progress = (moon_lon % nak_span) / nak_span
    pada = int((moon_lon % nak_span) / pada_span) + 1
    return NAKSHATRA_LIST[idx], progress, pada

def build_dasha_timeline(birth_date_str, nak_info, nak_progress):
    """构建完整大运时间线"""
    birth_dt = datetime.strptime(birth_date_str, "%Y-%m-%d")
    nak_name, start_lord, start_years = nak_info

    # 当前大运已经走了多少年
    elapsed = nak_progress * start_years
    remaining = start_years - elapsed

    # 当前大运的实际开始时间（往回推）
    current_dasha_start = birth_dt - timedelta(days=elapsed * 365.25)

    start_idx = DASHA_ORDER.index(start_lord)
    timeline = []
    dt = current_dasha_start

    for i in range(9):
        lord = DASHA_ORDER[(start_idx + i) % 9]
        years = DASHA_YEARS[lord]
        end_dt = dt + timedelta(days=years * 365.25)
        timeline.append({
            "lord": lord,
            "start": dt,
            "end": end_dt,
            "years": years,
        })
        dt = end_dt

    return timeline, round(elapsed, 2), round(remaining, 2), start_lord

def build_antardasha(mahadasha):
    """计算某个大运内的全部小运"""
    lord = mahadasha["lord"]
    total_days = (mahadasha["end"] - mahadasha["start"]).days
    start_idx = DASHA_ORDER.index(lord)
    sub_list = []
    dt = mahadasha["start"]

    for i in range(9):
        sub_lord = DASHA_ORDER[(start_idx + i) % 9]
        sub_years = DASHA_YEARS[sub_lord]
        # 小运时长 = 大运总年数 × 小运行星年占比 / 120
        sub_days = total_days * sub_years / 120
        end_dt = dt + timedelta(days=sub_days)
        sub_list.append({
            "lord": sub_lord,
            "start": dt,
            "end": end_dt,
        })
        dt = end_dt

    return sub_list

def find_current(timeline, today):
    """找到当前所处的大运"""
    for i, d in enumerate(timeline):
        if d["start"] <= today < d["end"]:
            return i, d
    return len(timeline) - 1, timeline[-1]

def find_current_sub(sub_list, today):
    """找到当前小运"""
    for d in sub_list:
        if d["start"] <= today < d["end"]:
            return d
    return sub_list[-1]

def print_timeline(timeline, today, show_sub=True):
    print(f"\n{'='*62}")
    print(f"  📅 Vimshottari Dasha 大运时间线")
    print(f"{'='*62}")
    print(f"  {'大运主星':<22} {'开始':<10}  {'结束':<10}  {'年限':>4}")
    print(f"  {'-'*58}")

    cur_idx, cur_dasha = find_current(timeline, today)

    for i, d in enumerate(timeline):
        marker = "  ◀ 当前" if i == cur_idx else ""
        print(f"  {PLANET_CN[d['lord']]:<20} {d['start'].strftime('%Y-%m'):<10}  {d['end'].strftime('%Y-%m'):<10}  {d['years']:>2}年{marker}")

    # 当前大运小运展开
    if show_sub:
        print(f"\n{'='*62}")
        print(f"  🔍 当前大运 [{PLANET_CN[cur_dasha['lord']]}] 小运展开")
        print(f"{'='*62}")
        sub_list = build_antardasha(cur_dasha)
        cur_sub = find_current_sub(sub_list, today)

        print(f"  {'小运主星':<22} {'开始':<10}  {'结束'}")
        print(f"  {'-'*50}")
        for s in sub_list:
            marker = "  ◀ 当前" if s == cur_sub else ""
            print(f"  {PLANET_CN[s['lord']]:<20} {s['start'].strftime('%Y-%m-%d'):<10}  {s['end'].strftime('%Y-%m-%d')}{marker}")

        # 当前小运剩余时间
        remaining_days = (cur_sub["end"] - today).days
        print(f"\n  当前小运 [{PLANET_CN[cur_sub['lord']]}] 将于 {cur_sub['end'].strftime('%Y年%m月%d日')} 结束")
        print(f"  剩余约 {remaining_days} 天（{round(remaining_days/30.44, 1)} 个月）")

def main():
    parser = argparse.ArgumentParser(description='印度占星 Dasha 推算器（基于已知星盘）')
    parser.add_argument('--nakshatra', help='月亮 Nakshatra 名称，如 "Jyeshtha"')
    parser.add_argument('--pada', type=int, default=None, help='Nakshatra Pada（1-4）')
    parser.add_argument('--moon-lon', type=float, help='月亮恒星黄经（0-360），与--nakshatra二选一')
    parser.add_argument('--birthdate', required=True, help='出生日期 YYYY-MM-DD')
    parser.add_argument('--today', default=None, help='计算基准日期 YYYY-MM-DD（默认今天）')
    args = parser.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d") if args.today else datetime.now()

    print(f"\n{'='*62}")
    print(f"  🌙 印度占星 Vimshottari Dasha 推算器")
    print(f"{'='*62}")
    print(f"  出生日期：{args.birthdate}")
    print(f"  计算基准：{today.strftime('%Y-%m-%d')}")

    if args.nakshatra:
        nak_info = fuzzy_match_nakshatra(args.nakshatra)
        if not nak_info:
            print(f"  ❌ 未找到 Nakshatra：{args.nakshatra}")
            print(f"  请检查拼写，或使用 --moon-lon 直接输入月亮黄经")
            return
        # 若提供了Pada，推算更精确的进度
        if args.pada:
            pada = max(1, min(4, args.pada))
            progress = (pada - 1) / 4 + 0.125  # 每Pada约25%，取中间值
        else:
            progress = 0.5  # 默认取中间
        print(f"  月亮星宿：{nak_info[0]}（大运主星：{nak_info[1]}，{nak_info[2]}年）")
        if args.pada:
            print(f"  Pada：第{args.pada}Pada")

    elif args.moon_lon is not None:
        nak_info, progress, pada = lon_to_nakshatra(args.moon_lon % 360)
        print(f"  月亮黄经：{args.moon_lon:.2f}°")
        print(f"  月亮星宿：{nak_info[0]}（第{pada}Pada，大运主星：{nak_info[1]}）")
    else:
        print("  ❌ 请提供 --nakshatra 或 --moon-lon")
        return

    timeline, elapsed, remaining, start_lord = build_dasha_timeline(args.birthdate, nak_info, progress)

    print(f"\n  出生时处于 [{PLANET_CN[start_lord]}] 大运")
    print(f"  出生时已历时约 {elapsed} 年，剩余约 {remaining} 年")

    print_timeline(timeline, today)

    print(f"\n{'='*62}\n")

if __name__ == '__main__':
    main()

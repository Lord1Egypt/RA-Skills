#!/usr/bin/env python3
"""
lunar_query.py — 农历/公历转换查询工具
用法：
  python3 lunar_query.py 2026-04-04
  python3 lunar_query.py 2026-04-04 2026-04-06
  python3 lunar_query.py --lunar 2026-1-1      # 农历查公历
  python3 lunar_query.py --range 2026-04-01 2026-04-07
  python3 lunar_query.py --moon-phase 2026-04-04  # 月相估算
"""
import sys
from datetime import datetime
from lunarcalendar import Converter, Solar, Lunar
from astronomy import julian_day, moon_phase, MOON_SYNODIC, NEW_MOON_JD

def solar_to_lunar_str(year, month, day):
    try:
        s = Solar(year, month, day)
        l = Converter.Solar2Lunar(s)
        return f"{year}-{month:02d}-{day:02d} = 农历{l.year}年{l.month:02d}月{l.day:02d}"
    except Exception as e:
        return f"错误: {e}"

def lunar_to_solar_str(year, month, day):
    try:
        l = Lunar(year, month, day, is_leap=False)
        s = Converter.Lunar2Solar(l)
        return f"农历{year}年{month}月{day} = 公历{s.year}-{s.month:02d}-{s.day:02d}"
    except Exception as e:
        try:
            l = Lunar(year, month, day, is_leap=True)
            s = Converter.Lunar2Solar(l)
            return f"农历{year}年(闰){month}月{day} = 公历{s.year}-{s.month:02d}-{s.day:02d}"
        except:
            return f"错误: {e}"

def moon_phase_desc(year, month, day):
    """估算月相（基于天文月龄与照明率近似）。"""
    try:
        jd = julian_day(datetime(year, month, day, 12, 0, 0))
        lunar_age = (jd - NEW_MOON_JD) % MOON_SYNODIC
        illumination, _ = moon_phase(jd)

        if lunar_age < 1.5:
            phase = "🌑 新月"
        elif lunar_age < 6.4:
            phase = "🌒 眉月"
        elif lunar_age < 8.9:
            phase = "🌓 上弦月"
        elif lunar_age < 13.8:
            phase = "🌔 盈凸月"
        elif lunar_age < 15.8:
            phase = "🌕 满月(望)"
        elif lunar_age < 20.7:
            phase = "🌖 亏凸月"
        elif lunar_age < 23.1:
            phase = "🌗 下弦月"
        elif lunar_age < 28.0:
            phase = "🌘 残月"
        else:
            phase = "🌘 晦月/新月前夕"

        return f"月相: {phase} (约{illumination * 100:.0f}%亮度) 月龄约{lunar_age:.1f}天"
    except Exception as e:
        return f"月相估算错误: {e}"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "--moon-phase" and len(sys.argv) >= 3:
        y, m, d = map(int, sys.argv[2].split('-'))
        print(moon_phase_desc(y, m, d))
    
    elif cmd == "--lunar" and len(sys.argv) >= 3:
        parts = list(map(int, sys.argv[2].split('-')))
        if len(parts) == 3:
            print(lunar_to_solar_str(parts[0], parts[1], parts[2]))
        else:
            print("格式: --lunar YYYY-M-D")
    
    elif cmd == "--range" and len(sys.argv) >= 4:
        from datetime import datetime, timedelta
        start = datetime.strptime(sys.argv[2], "%Y-%m-%d")
        end = datetime.strptime(sys.argv[3], "%Y-%m-%d")
        current = start
        while current <= end:
            print(solar_to_lunar_str(current.year, current.month, current.day))
            current += timedelta(days=1)
    
    elif cmd == "--help":
        print(__doc__)
    
    else:
        # 假设是日期列表
        for arg in sys.argv[1:]:
            if '-' in arg:
                parts = list(map(int, arg.split('-')))
                if len(parts) == 3:
                    print(solar_to_lunar_str(parts[0], parts[1], parts[2]))
                    print("  ", moon_phase_desc(parts[0], parts[1], parts[2]))

if __name__ == "__main__":
    main()

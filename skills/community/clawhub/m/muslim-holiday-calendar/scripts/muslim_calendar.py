#!/usr/bin/env python3
"""Muslim Holiday Calendar - Islamic holidays and Hijri calendar calculator"""
import sys, json
from datetime import date, timedelta

# Islamic holidays: approximate Gregorian dates (moon sighting varies by region)
# Format: year -> {holiday_name: gregorian_date}
ISLAMIC_HOLIDAYS = {
    2024: {
        "Eid al-Fitr": "2024-04-10",
        "Eid al-Adha": "2024-06-16",
        "Islamic New Year": "2024-07-07",
        "Mawlid al-Nabi": "2024-09-15",
        "Ramadan Start": "2024-03-11",
        "Arafat Day": "2024-06-15",
    },
    2025: {
        "Eid al-Fitr": "2025-03-30",
        "Eid al-Adha": "2025-06-06",
        "Islamic New Year": "2025-06-27",
        "Mawlid al-Nabi": "2025-09-04",
        "Ramadan Start": "2025-02-28",
        "Arafat Day": "2025-06-05",
    },
    2026: {
        "Eid al-Fitr": "2026-03-20",
        "Eid al-Adha": "2026-05-27",
        "Islamic New Year": "2026-06-16",
        "Mawlid al-Nabi": "2026-08-25",
        "Ramadan Start": "2026-02-18",
        "Arafat Day": "2026-05-26",
    },
    2027: {
        "Eid al-Fitr": "2027-03-09",
        "Eid al-Adha": "2027-05-16",
        "Islamic New Year": "2027-06-05",
        "Mawlid al-Nabi": "2027-08-14",
        "Ramadan Start": "2027-02-08",
        "Arafat Day": "2027-05-15",
    },
    2028: {
        "Eid al-Fitr": "2028-02-26",
        "Eid al-Adha": "2028-05-05",
        "Islamic New Year": "2028-05-25",
        "Mawlid al-Nabi": "2028-08-03",
        "Ramadan Start": "2028-01-28",
        "Arafat Day": "2028-05-04",
    },
    2029: {
        "Eid al-Fitr": "2029-02-15",
        "Eid al-Adha": "2029-04-25",
        "Islamic New Year": "2029-05-14",
        "Mawlid al-Nabi": "2029-07-24",
        "Ramadan Start": "2029-01-17",
        "Arafat Day": "2029-04-24",
    },
    2030: {
        "Eid al-Fitr": "2030-02-05",
        "Eid al-Adha": "2030-04-14",
        "Islamic New Year": "2030-05-04",
        "Mawlid al-Nabi": "2030-07-13",
        "Ramadan Start": "2030-01-07",
        "Arafat Day": "2030-04-13",
    },
}

HOLIDAY_INFO = {
    "Eid al-Fitr": {"ar": "عيد الفطر", "en": "Festival of Breaking Fast", "days": 3},
    "Eid al-Adha": {"ar": "عيد الأضحى", "en": "Festival of Sacrifice", "days": 4},
    "Ramadan Start": {"ar": "رمضان", "en": "Month of Fasting", "days": 30},
    "Islamic New Year": {"ar": "رأس السنة الهجرية", "en": "Hijri New Year", "days": 1},
    "Mawlid al-Nabi": {"ar": "المولد النبوي", "en": "Prophet's Birthday", "days": 1},
    "Arafat Day": {"ar": "يوم عرفة", "en": "Day of Arafat", "days": 1},
}

def parse_date(s):
    if not s: return None
    y, m, d = map(int, s.split('-'))
    return date(y, m, d)

def cmd_holidays(args):
    year = int(args[0]) if args else date.today().year
    if year not in ISLAMIC_HOLIDAYS:
        print(json.dumps({"error": f"No data for year {year}. Available: 2024-2030"}))
        return
    holidays = ISLAMIC_HOLIDAYS[year]
    result = {"year": year, "holidays": []}
    for name, dstr in sorted(holidays.items(), key=lambda x: x[1]):
        d = parse_date(dstr)
        info = HOLIDAY_INFO.get(name, {})
        result["holidays"].append({
            "name": name,
            "arabic": info.get("ar", ""),
            "meaning": info.get("en", ""),
            "date": dstr,
            "days": info.get("days", 1)
        })
    print(json.dumps(result, ensure_ascii=False, indent=2))

def cmd_next(args):
    today = date.today()
    all_holidays = []
    for year, holidays in ISLAMIC_HOLIDAYS.items():
        for name, dstr in holidays.items():
            d = parse_date(dstr)
            if d >= today:
                all_holidays.append((d, name, dstr))
    all_holidays.sort()
    if all_holidays:
        d, name, dstr = all_holidays[0]
        days_left = (d - today).days
        info = HOLIDAY_INFO.get(name, {})
        print(json.dumps({
            "holiday": name,
            "arabic": info.get("ar", ""),
            "meaning": info.get("en", ""),
            "date": dstr,
            "days_until": days_left,
            "is_upcoming": days_left <= 30
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "No upcoming holidays in database"}))

def cmd_countdown(args):
    target = args[0] if args else "Eid al-Fitr"
    today = date.today()
    for year, holidays in ISLAMIC_HOLIDAYS.items():
        if target in holidays:
            d = parse_date(holidays[target])
            if d >= today:
                days = (d - today).days
                print(json.dumps({
                    "holiday": target,
                    "date": holidays[target],
                    "days_remaining": days,
                    "weeks": days // 7
                }, indent=2))
                return
    print(json.dumps({"error": f"Holiday '{target}' not found"}))

def cmd_is_friday(args):
    d = parse_date(args[0]) if args else date.today()
    is_friday = d.weekday() == 4
    print(json.dumps({
        "date": str(d),
        "weekday": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][d.weekday()],
        "is_friday": is_friday,
        "note": "Friday is the holy day in Islam (Jumu'ah)" if is_friday else ""
    }, indent=2))

def cmd_info(args):
    name = args[0] if args else "Eid al-Fitr"
    info = HOLIDAY_INFO.get(name, {})
    print(json.dumps({
        "holiday": name,
        "arabic": info.get("ar", ""),
        "english": info.get("en", ""),
        "duration_days": info.get("days", 1)
    }, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) < 2:
        print("Usage: muslim_calendar.py <command> [args...]\nCommands: holidays, next-holiday, countdown, is-friday, info")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "holidays":
        cmd_holidays(args)
    elif cmd == "next-holiday":
        cmd_next(args)
    elif cmd == "countdown":
        cmd_countdown(args)
    elif cmd == "is-friday":
        cmd_is_friday(args)
    elif cmd == "info":
        cmd_info(args)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()

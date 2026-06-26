#!/usr/bin/env python3
"""kr-holiday-cli — Korean public holidays, business-day calculator, lunar↔solar converter.

Zero API key. Uses the `holidays` package for KR public holidays (including
substitute holidays / 대체공휴일) and `korean-lunar-calendar` for lunar↔solar
conversion.

Subcommands:
    is-holiday <date>
    list --year <y> [--month <m>]
    next-business-day <date> [--offset N]
    prev-business-day <date> [--offset N]
    add-business-days <date> --days <n>
    business-days --start <d> --end <d>
    solar-to-lunar <date>
    lunar-to-solar <date> [--leap]
    month <year> <month> [--format text|json]

Dates accept YYYYMMDD or YYYY-MM-DD.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import sys
from typing import Iterable


def _eprint(payload: dict, code: int = 1) -> int:
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
    return code


def _import_holidays():
    try:
        import holidays  # type: ignore
    except ImportError:
        _eprint({
            "error": "missing_dependency",
            "package": "holidays",
            "hint": "pip install -r scripts/requirements.txt",
        })
        sys.exit(4)
    return holidays


def _import_lunar():
    try:
        from korean_lunar_calendar import KoreanLunarCalendar  # type: ignore
    except ImportError:
        _eprint({
            "error": "missing_dependency",
            "package": "korean-lunar-calendar",
            "hint": "pip install -r scripts/requirements.txt",
        })
        sys.exit(4)
    return KoreanLunarCalendar


def parse_date(s: str) -> dt.date:
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise SystemExit(_eprint({"error": "bad_date", "input": s}, 2))


def kr_holidays(years: Iterable[int]):
    holidays = _import_holidays()
    return holidays.country_holidays("KR", years=list(years), language="ko")


def is_business_day(d: dt.date, kr) -> bool:
    return d.weekday() < 5 and d not in kr


def cmd_is_holiday(args) -> int:
    d = parse_date(args.date)
    kr = kr_holidays([d.year])
    names = []
    if d in kr:
        raw = kr.get(d)
        if raw:
            names = [n.strip() for n in str(raw).split(",") if n.strip()]
    payload = {
        "date": d.isoformat(),
        "weekday": d.strftime("%a"),
        "is_weekend": d.weekday() >= 5,
        "is_holiday": d in kr,
        "is_business_day": is_business_day(d, kr),
        "names": names,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def cmd_list(args) -> int:
    kr = kr_holidays([args.year])
    rows = []
    for d in sorted(kr):
        if args.month and d.month != args.month:
            continue
        raw = kr.get(d)
        names = [n.strip() for n in str(raw).split(",") if n.strip()] if raw else []
        rows.append({
            "date": d.isoformat(),
            "weekday": d.strftime("%a"),
            "names": names,
        })
    print(json.dumps(rows, ensure_ascii=False))
    return 0


def _shift_business(start: dt.date, step: int, count: int) -> dt.date:
    if count < 0:
        raise SystemExit(_eprint({"error": "bad_offset", "offset": count}, 2))
    years = {start.year, start.year + 1, start.year - 1}
    kr = kr_holidays(years)
    d = start
    moved = 0
    guard = 0
    while moved < count:
        d = d + dt.timedelta(days=step)
        guard += 1
        if guard > 3650:  # ~10 years of slack
            raise SystemExit(_eprint({"error": "shift_overflow"}, 3))
        if d.year not in years:
            years.add(d.year)
            kr = kr_holidays(years)
        if is_business_day(d, kr):
            moved += 1
    return d


def cmd_next_business(args) -> int:
    d = parse_date(args.date)
    n = max(1, args.offset)
    result = _shift_business(d, +1, n)
    print(json.dumps({"input": d.isoformat(), "offset": n, "result": result.isoformat()}, ensure_ascii=False))
    return 0


def cmd_prev_business(args) -> int:
    d = parse_date(args.date)
    n = max(1, args.offset)
    result = _shift_business(d, -1, n)
    print(json.dumps({"input": d.isoformat(), "offset": -n, "result": result.isoformat()}, ensure_ascii=False))
    return 0


def cmd_add_business(args) -> int:
    d = parse_date(args.date)
    days = args.days
    if days == 0:
        years = {d.year}
        kr = kr_holidays(years)
        result = d
        payload_days = 0
        if not is_business_day(d, kr):
            # snap forward to the next business day
            result = _shift_business(d, +1, 1)
            payload_days = 0
        print(json.dumps({"input": d.isoformat(), "days": payload_days, "result": result.isoformat()}, ensure_ascii=False))
        return 0
    step = 1 if days > 0 else -1
    result = _shift_business(d, step, abs(days))
    print(json.dumps({"input": d.isoformat(), "days": days, "result": result.isoformat()}, ensure_ascii=False))
    return 0


def cmd_business_days(args) -> int:
    start = parse_date(args.start)
    end = parse_date(args.end)
    if end < start:
        start, end = end, start
    years = set(range(start.year, end.year + 1))
    kr = kr_holidays(years)
    total = 0
    d = start
    while d <= end:
        if is_business_day(d, kr):
            total += 1
        d += dt.timedelta(days=1)
    print(json.dumps({
        "start": start.isoformat(),
        "end": end.isoformat(),
        "calendar_days": (end - start).days + 1,
        "business_days": total,
    }, ensure_ascii=False))
    return 0


def cmd_solar_to_lunar(args) -> int:
    KoreanLunarCalendar = _import_lunar()
    d = parse_date(args.date)
    c = KoreanLunarCalendar()
    ok = c.setSolarDate(d.year, d.month, d.day)
    if not ok:
        return _eprint({"error": "conversion_failed", "input": d.isoformat()}, 3)
    print(json.dumps({
        "solar": d.isoformat(),
        "lunar": f"{c.lunarYear:04d}-{c.lunarMonth:02d}-{c.lunarDay:02d}",
        "lunar_year": c.lunarYear,
        "lunar_month": c.lunarMonth,
        "lunar_day": c.lunarDay,
        "is_leap_month": c.isIntercalation,
        "gapja": c.getGapJaString(),
    }, ensure_ascii=False))
    return 0


def cmd_lunar_to_solar(args) -> int:
    KoreanLunarCalendar = _import_lunar()
    d = parse_date(args.date)
    c = KoreanLunarCalendar()
    ok = c.setLunarDate(d.year, d.month, d.day, bool(args.leap))
    if not ok:
        return _eprint({"error": "conversion_failed", "input": d.isoformat(), "leap": bool(args.leap)}, 3)
    print(json.dumps({
        "lunar": f"{d.year:04d}-{d.month:02d}-{d.day:02d}",
        "is_leap_month": bool(args.leap),
        "solar": f"{c.solarYear:04d}-{c.solarMonth:02d}-{c.solarDay:02d}",
        "gapja": c.getGapJaString(),
    }, ensure_ascii=False))
    return 0


def cmd_month(args) -> int:
    year, month = args.year, args.month
    if not (1 <= month <= 12):
        return _eprint({"error": "bad_month", "month": month}, 2)
    kr = kr_holidays([year])
    cal = calendar.Calendar(firstweekday=6)  # Sunday-first (Korean convention)
    weeks = cal.monthdatescalendar(year, month)

    if args.format == "json":
        grid = []
        for week in weeks:
            row = []
            for d in week:
                in_month = d.month == month
                names = []
                if in_month and d in kr:
                    raw = kr.get(d)
                    if raw:
                        names = [n.strip() for n in str(raw).split(",") if n.strip()]
                row.append({
                    "date": d.isoformat(),
                    "day": d.day,
                    "in_month": in_month,
                    "is_weekend": d.weekday() >= 5,
                    "is_holiday": in_month and d in kr,
                    "is_business_day": in_month and is_business_day(d, kr),
                    "names": names,
                })
            grid.append(row)
        print(json.dumps({
            "year": year,
            "month": month,
            "first_weekday": "Sunday",
            "weeks": grid,
        }, ensure_ascii=False))
        return 0

    # text format
    header = f"{year}-{month:02d}  Korean calendar (S M T W T F S)"
    print(header)
    print("-" * len(header))
    print(" 일  월  화  수  목  금  토")
    holiday_names = []
    for week in weeks:
        cells = []
        for d in week:
            if d.month != month:
                cells.append("   ")
                continue
            token = f"{d.day:2d}"
            is_hol = d in kr
            is_wknd = d.weekday() >= 5
            if is_hol:
                cells.append(f"*{token}")
                raw = kr.get(d)
                if raw:
                    holiday_names.append(f"  {d.isoformat()}  {raw}")
            elif is_wknd:
                cells.append(f" {token}")
            else:
                cells.append(f" {token}")
        print(" ".join(cells))
    if holiday_names:
        print()
        print("Holidays (* = public holiday):")
        for line in holiday_names:
            print(line)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kr-holiday", description="Korean public holidays & business-day calculator (CLI)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("is-holiday", help="Check if a date is a Korean public holiday")
    s.add_argument("date")
    s.set_defaults(func=cmd_is_holiday)

    s = sub.add_parser("list", help="List Korean public holidays in a year")
    s.add_argument("--year", type=int, required=True)
    s.add_argument("--month", type=int)
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("next-business-day", help="N-th next business day (weekend/holiday aware)")
    s.add_argument("date")
    s.add_argument("--offset", type=int, default=1)
    s.set_defaults(func=cmd_next_business)

    s = sub.add_parser("prev-business-day", help="N-th previous business day")
    s.add_argument("date")
    s.add_argument("--offset", type=int, default=1)
    s.set_defaults(func=cmd_prev_business)

    s = sub.add_parser("add-business-days", help="Add signed business-day offset to a date")
    s.add_argument("date")
    s.add_argument("--days", type=int, required=True)
    s.set_defaults(func=cmd_add_business)

    s = sub.add_parser("business-days", help="Count business days between two inclusive dates")
    s.add_argument("--start", required=True)
    s.add_argument("--end", required=True)
    s.set_defaults(func=cmd_business_days)

    s = sub.add_parser("solar-to-lunar", help="Convert solar date to Korean lunar date")
    s.add_argument("date")
    s.set_defaults(func=cmd_solar_to_lunar)

    s = sub.add_parser("lunar-to-solar", help="Convert Korean lunar date to solar date")
    s.add_argument("date")
    s.add_argument("--leap", action="store_true", help="Treat input month as leap (윤달)")
    s.set_defaults(func=cmd_lunar_to_solar)

    s = sub.add_parser("month", help="Render a monthly calendar with Korean holidays")
    s.add_argument("year", type=int)
    s.add_argument("month", type=int)
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.set_defaults(func=cmd_month)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SystemExit:
        raise
    except Exception as exc:  # last-resort guard
        return _eprint({"error": "internal_error", "message": str(exc)}, 3)


if __name__ == "__main__":
    sys.exit(main())

---
name: kr-holiday-cli
description: Korean public holidays, business-day calculator, and lunar↔solar converter (CLI). Check if a date is a Korean public holiday (including 대체공휴일), list holidays in a year/month, compute next/previous business days, count business days in a range, add signed business-day offsets, convert between Korean lunar and solar dates (including 윤달), render a monthly calendar. Use when a user asks about Korean holidays 공휴일, 설날, 추석, 대체공휴일, 평일 계산, 영업일, 음력 양력 변환, or scheduling that must skip Korean holidays. Zero API key.
license: MIT
---

# Korean Holiday & Business-Day CLI

Zero-config CLI for Korean public holidays, business-day math, and Korean lunar↔solar conversion. No API key. No network required at runtime.

- Public holidays powered by the [`holidays`](https://pypi.org/project/holidays/) package (Korean names, substitute holidays / 대체공휴일 included).
- Lunar↔solar powered by [`korean-lunar-calendar`](https://pypi.org/project/korean-lunar-calendar/) (KASI astronomical tables, supports 윤달).

## When to use

Trigger this skill for any of:

- Is a given date a Korean public holiday? ("2026-05-05 공휴일이야?")
- List Korean holidays for a year or month
- Compute next/previous business day, skipping weekends AND Korean holidays
- Add a signed business-day offset (e.g., invoice due in +10 business days from order date)
- Count business days between two dates (payroll, SLA, delivery ETA)
- Convert solar ↔ Korean lunar dates (음력 생일 lookup, 설날·추석 date lookup)
- Render a monthly calendar view with holidays marked

Do **not** use for:

- Regional / religious holidays that aren't recognized as national public holidays (예: 성탄절 제외 종교 행사)
- Company-specific working calendars (add your own per-company overrides outside this skill)
- Realtime election-day announcements (bundled rules reflect statutory holidays; ad-hoc presidential decree holidays may lag until the `holidays` package updates)

## Install

```bash
pip install -r scripts/requirements.txt
```

Dependencies: `holidays`, `korean-lunar-calendar`.

## Usage

All commands are sub-commands of `scripts/kr_holiday.py`. Output is JSON (UTF-8, Korean preserved). Dates accept `YYYY-MM-DD`, `YYYYMMDD`, `YYYY/MM/DD`, or `YYYY.MM.DD`.

### Check a date

```bash
python scripts/kr_holiday.py is-holiday 2026-05-05
# → {"date":"2026-05-05","weekday":"Tue","is_weekend":false,"is_holiday":true,"is_business_day":false,"names":["어린이날"]}
```

### List holidays in a year (optionally filter by month)

```bash
python scripts/kr_holiday.py list --year 2026
python scripts/kr_holiday.py list --year 2026 --month 5
```

### Next / previous business day

```bash
python scripts/kr_holiday.py next-business-day 2026-05-02                 # skip Sat → 2026-05-04 (Mon)
python scripts/kr_holiday.py next-business-day 2026-05-02 --offset 3      # 3rd next business day
python scripts/kr_holiday.py prev-business-day 2026-05-06 --offset 2
```

### Add a signed business-day offset

```bash
python scripts/kr_holiday.py add-business-days 2026-04-20 --days 10       # 2026-05-04
python scripts/kr_holiday.py add-business-days 2026-05-05 --days -3
```

### Count business days in a range (inclusive)

```bash
python scripts/kr_holiday.py business-days --start 2026-05-01 --end 2026-05-31
# → {"start":"2026-05-01","end":"2026-05-31","calendar_days":31,"business_days":19}
```

### Solar ↔ Korean lunar

```bash
python scripts/kr_holiday.py solar-to-lunar 2026-02-17
# → {"solar":"2026-02-17","lunar":"2026-01-01","is_leap_month":false,"gapja":"병오년 경인월 임술일"}

python scripts/kr_holiday.py lunar-to-solar 2026-08-15
python scripts/kr_holiday.py lunar-to-solar 2025-06-01 --leap              # pass --leap for 윤달
```

### Monthly calendar view

```bash
python scripts/kr_holiday.py month 2026 5                   # human-readable, Sunday-first
python scripts/kr_holiday.py month 2026 5 --format json     # weeks grid in JSON
```

## Output conventions

- JSON by default (no pretty-print; pipe through `python -m json.tool` if desired).
- `is_business_day = true` ⇔ Mon–Fri AND not a Korean public holiday.
- `names` is a list — a single calendar day can carry multiple labels (e.g., when holidays overlap).
- Substitute holidays (대체공휴일) appear as their own entries in `list` output.

## Error handling

- Unparseable date → exit `2`, stderr JSON `{"error":"bad_date","input":"…"}`.
- Out-of-range month, negative offset, conversion failure → exit `2` or `3`, stderr JSON.
- Missing dependency → exit `4`, stderr JSON with install hint.

## Notes on holiday accuracy

- 대체공휴일 rules: reflects the revised 2021/2023 rules (substitute applies when a national holiday falls on Sat/Sun, with the documented exceptions). Results match rulings published by 공공데이터포털 한국천문연구원 특일 정보 through 2030.
- Lunar holidays (설날, 추석, 부처님오신날) are computed from the lunar calendar bundled in the `holidays` package.
- Update `holidays` periodically to pick up legislative changes: `pip install -U holidays`.

## See also

- `krx-stock-cli` — KRX stock market data (KOSPI/KOSDAQ)
- `toss-payments-cli` — Toss Payments API
- `kakao-local-cli` — Kakao Local place & geocoding API

## License

MIT.

# kr-holiday-cli

Korean public holidays, business-day calculator, and lunar↔solar converter — CLI.

Zero API key. Zero network. Pure compute over bundled rules.

## What it does

- `is-holiday` — is a given date a Korean public holiday (including 대체공휴일)?
- `list` — all Korean public holidays in a year (optionally filtered by month).
- `next-business-day` / `prev-business-day` — skip weekends + Korean holidays.
- `add-business-days` — signed business-day offset from a given date.
- `business-days` — count business days between two inclusive dates.
- `solar-to-lunar` / `lunar-to-solar` — Korean lunar calendar conversion (with 윤달 support).
- `month` — rendered monthly calendar with holidays highlighted.

## Install

```bash
pip install -r scripts/requirements.txt
```

Dependencies:

- [`holidays`](https://pypi.org/project/holidays/) — Korean public holidays (with substitute holidays).
- [`korean-lunar-calendar`](https://pypi.org/project/korean-lunar-calendar/) — lunar↔solar conversion based on KASI tables.

## Quick start

```bash
python scripts/kr_holiday.py is-holiday 2026-05-05
python scripts/kr_holiday.py list --year 2026
python scripts/kr_holiday.py add-business-days 2026-04-20 --days 10
python scripts/kr_holiday.py solar-to-lunar 2026-02-17
python scripts/kr_holiday.py month 2026 5
```

See `SKILL.md` for complete usage and I/O conventions.

## Why

Every agent that touches Korean scheduling (payroll, delivery SLAs, billing cycles, appointment reminders, marketing sends) needs to answer "is this a public holiday?" or "when is the next business day?" For Korea that question is non-trivial: lunar holidays (설날, 추석, 부처님오신날) shift every year and 대체공휴일 rules changed in 2021 and 2023.

## License

MIT.

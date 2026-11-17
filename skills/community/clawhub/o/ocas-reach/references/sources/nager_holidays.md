# nager_holidays — public holidays by country

## What this source has

Nager.Date is a small open dataset of public holidays for ~110 countries. Coverage focuses on national-level public holidays (banks/government closed); regional or religious-only observances are partial. Each holiday has a date, local name, English name, country code, fixed/moveable flag, and a list of types (`Public`, `Bank`, `School`, `Authorities`, `Optional`, `Observance`).

Country code is ISO 3166-1 alpha-2 (e.g., `US`, `DE`, `JP`). The API also exposes "long weekend" calculations (when a public holiday combined with weekend or bridge day yields a 3+ day stretch).

Use Nager.Date for: "is X a holiday in country Y", "what are the holidays in country Y for year N", planning around long weekends. Pair with `worldtime` when also computing local time/DST.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no documented cap; data is small enough to cache the full year per country |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `public` | Public holidays in a year for a country | `year`, `country` |
| `next_public` | Upcoming public holidays for a country | `country` |
| `countries` | List supported countries | none |
| `long_weekend` | Long-weekend stretches in a year | `year`, `country` |

## Worked examples

```bash
# US holidays in 2026
python3 scripts/reach.py query nager_holidays public '{"year": 2026, "country": "US"}'

# Next holidays in Germany
python3 scripts/reach.py query nager_holidays next_public '{"country": "DE"}'

# All long weekends in Japan in 2026
python3 scripts/reach.py query nager_holidays long_weekend '{"year": 2026, "country": "JP"}'

# Supported countries list
python3 scripts/reach.py query nager_holidays countries '{}'
```

## Response shape

- `public` / `next_public`: list of `{date: "YYYY-MM-DD", localName, name, countryCode, fixed: bool, global: bool, counties: ["US-AL", ...] | null, launchYear: int | null, types: ["Public"]}`. `counties` is the subdivision list (when the holiday is regional only); `null` when the holiday applies nationwide.
- `countries`: list of `{countryCode, name}`.
- `long_weekend`: list of `{startDate, endDate, dayCount, needBridgeDay: bool}`. `needBridgeDay: true` means you'd take 1 PTO day to bridge.

## Pitfalls

- **Country code is ISO-3166-1 alpha-2**, not 3-letter: `US`, not `USA`. `GB` for the UK (not `UK`). The API rejects unknown codes with 404.
- **`global: false` means regional-only.** A holiday applying only to certain US states will have `global: false` and `counties` populated. If you want "everywhere", filter on `global: true`.
- **Coverage is uneven.** Some countries have 8-10 holidays listed (well-covered); others 3-4 (incomplete). Don't trust the dataset as authoritative for niche jurisdictions.
- **No religious-observance toggle.** Easter, Christmas, Eid where they're official public holidays are included; where they're cultural-only they aren't. Check `types`.
- **Date format `YYYY-MM-DD`**, no time component (holidays are full-day).
- **`next_public` returns the next ~12 months' worth.** Doesn't go far into the future; for year-N planning, use `public` with the explicit year.
- **No state/province granularity for most countries.** US has `counties: ["US-AL"]` syntax; many others don't break out subdivisions.

## Source links

- API docs: https://date.nager.at/swagger/index.html
- Project home: https://date.nager.at/
- Source: https://github.com/nager/Nager.Date

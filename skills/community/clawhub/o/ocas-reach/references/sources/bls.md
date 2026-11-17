# bls — US Bureau of Labor Statistics time series

## What this source has

The BLS Public Data API serves all BLS published time series: Consumer Price Index (CPI-U, CPI-W, C-CPI-U), Producer Price Index, Employment Situation (CES), unemployment (LAUS), Job Openings and Labor Turnover (JOLTS), occupational employment, work stoppages, productivity. ~600,000+ time series, identified by series ID (e.g., `CUUR0000SA0` = CPI-U, all items, all urban consumers, US city average; `LNS14000000` = unemployment rate, seasonally adjusted).

Series IDs encode their dataset and dimensions in fixed-position character codes — `CUUR` (CPI-U, all urban, NSA) + `0000` (US city average) + `SA0` (all items). The PDF "documentation" lists every code position per dataset.

FRED ingests most BLS series and is usually friendlier — use `bls` directly when you need a series FRED doesn't carry, or for fresh data immediately on release morning.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `BLS_KEY` |
| Account URL | https://data.bls.gov/registrationEngine/ |
| Plan tier | free (v2) |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. Without a key (v1 access) you're capped at 25 queries/day with reduced features; v2 with key gives 500/day.

## Limits

| | |
|---|---|
| Daily | 500 |
| Monthly | — |
| Rate | no per-second limit; daily cap is the constraint |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `timeseries` | Fetch values for one or more series IDs (POST) | `seriesid` (array) |
| `surveys` | List surveys / datasets | none |

## Worked examples

```bash
# CPI-U (all items) and unemployment rate, 2020-2026
python3 scripts/reach.py query bls timeseries '{
  "seriesid": ["CUUR0000SA0", "LNS14000000"],
  "startyear": "2020",
  "endyear": "2026"
}'

# Just the most recent unemployment rate
python3 scripts/reach.py query bls timeseries '{
  "seriesid": ["LNS14000000"],
  "latest": true
}'

# Multiple series with calculations (12-month % change)
python3 scripts/reach.py query bls timeseries '{
  "seriesid": ["CUUR0000SA0", "CUUR0000SA0L1E"],
  "startyear": "2024",
  "endyear": "2026",
  "calculations": true,
  "annualaverage": false
}'

# List BLS surveys
python3 scripts/reach.py query bls surveys '{}'
```

## Response shape

- `timeseries`: `{status: "REQUEST_SUCCEEDED", responseTime, message: [...], Results: {series: [{seriesID, data: [{year, period, periodName, value, footnotes: [{code, text}], calculations: {net_changes: {...}, pct_changes: {...}}}, ...]}]}}`. `value` is a **string** (numeric content). `period` is `M01`...`M12` for months, `Q01`-`Q04` for quarters, `A01` for annual.
- `surveys`: `{status, message, Results: {survey: [{survey_abbreviation, survey_name}, ...]}}`.

## Pitfalls

- **POST not GET.** v2 timeseries is POST with JSON body — the connector handles this. The key goes in the body (`registrationkey`) not as a query param.
- **`seriesid` is an array** even when fetching one series. `["CUUR0000SA0"]`, not `"CUUR0000SA0"`.
- **Up to 50 series IDs per call.** v2 with key allows 50; v1 only 25. Mix dataset families freely in one call.
- **Up to 20 years of data per call.** For longer ranges, page by year window.
- **`value` is a string.** Convert to float; some values are `"-"` or `"NA"` for unreleased / suppressed.
- **Period codes are dataset-specific.** Most monthly series use `M01`-`M12`; CES uses `M01`-`M13` where `M13` is annual average. JOLTS uses `M01`-`M12`.
- **`startyear`/`endyear` are 4-digit strings** in the request body. Numbers also accepted by most clients but strings are safest.
- **Some series have lag.** Annual data for year N is published months into year N+1.
- **Specific value-quirk: `EuiIA`.** Iowa LAUS values use the footnote code `EuiIA` to indicate "Iowa-published value differs from BLS estimate". Treat the footnote codes as caveats; check `footnotes` before drawing conclusions.

## Source links

- API docs: https://www.bls.gov/developers/
- v2 sign-up: https://data.bls.gov/registrationEngine/
- Series ID format guide: https://www.bls.gov/help/hlpforma.htm

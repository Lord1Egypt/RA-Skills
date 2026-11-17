# fred — Federal Reserve Economic Data

## What this source has

FRED is the St. Louis Fed's economic time-series library: ~800,000 series covering US and global macro indicators. GDP, CPI, unemployment, federal funds rate, M2, payrolls, industrial production, exchange rates, housing starts, mortgage rates, oil prices — and 800k more. Most series are updated within a day of release.

Each series has a stable string ID (`UNRATE`, `GDPC1`, `DFF`, `CPIAUCSL`) and metadata: source (e.g., BLS, BEA, Fed Board), frequency (daily / weekly / monthly / quarterly / annual), units (percent, billions of chained 2017 dollars, index), seasonal adjustment.

Use FRED for: any US macroeconomic question, central-bank rates worldwide, exchange rates, sector employment, inflation breakdowns. Pair with `bls` only when you need labor data not yet pulled into FRED (rare — FRED ingests BLS).

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `FRED_KEY` |
| Account URL | https://fred.stlouisfed.org/docs/api/api_key.html |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. The signup form asks for name + email + use case; "personal AI assistant; non-commercial" is sufficient. Key issued instantly by email.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 120 req/min per key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `series_observations` | Time series values | `series_id` |
| `series` | Metadata for a series | `series_id` |
| `series_search` | Find series by keyword | `search_text` |
| `category` | Series in a category | `category_id` |

## Worked examples

```bash
# US unemployment rate, last 24 months
python3 scripts/reach.py query fred series_observations '{
  "series_id": "UNRATE",
  "observation_start": "2024-01-01",
  "sort_order": "desc",
  "limit": 24
}'

# Real GDP, quarterly, last 5 years
python3 scripts/reach.py query fred series_observations '{
  "series_id": "GDPC1",
  "observation_start": "2021-01-01"
}'

# What's the metadata on the federal funds rate series?
python3 scripts/reach.py query fred series '{"series_id": "DFF"}'

# Find series mentioning "core inflation"
python3 scripts/reach.py query fred series_search '{"search_text": "core inflation", "limit": 10}'
```

## Response shape

- `series_observations`: `{realtime_start, realtime_end, observation_start, observation_end, units, output_type, file_type, order_by, sort_order, count, offset, limit, observations: [{realtime_start, realtime_end, date, value}, ...]}`. The `value` field is a string — convert to float; missing values come as `"."`.
- `series`: `{seriess: [{id, realtime_start, realtime_end, title, observation_start, observation_end, frequency, frequency_short, units, units_short, seasonal_adjustment, seasonal_adjustment_short, last_updated, popularity, notes}]}`. Note the typo — it's `seriess`, not `series`.
- `series_search`: same shape as `series` but the `seriess` array contains many matches.
- `category`: `{categories: [{id, name, parent_id}]}`.

## Pitfalls

- **Missing values.** `value` comes as the string `"."` for periods where data isn't yet released. Filter or convert to None before plotting.
- **`series_observations` defaults to descending order without dates.** Always set `sort_order` and `observation_start`/`observation_end` explicitly to avoid surprises.
- **Real-time vintages.** FRED supports requesting a series "as it was known" on a past date via `realtime_start`/`realtime_end`. Default is current. For revisions analysis, set both to the same historical date.
- **`seriess` typo.** The metadata response key really is `seriess` (double-s). Don't try to "fix" it.
- **Series ID case sensitivity.** Series IDs are upper-case (`UNRATE`, `GDPC1`). Lower-case may silently return empty or 404.
- **Frequency aliases.** The `frequency_short` field uses single letters: `D` daily, `W` weekly, `M` monthly, `Q` quarterly, `A` annual.

## Source links

- API docs: https://fred.stlouisfed.org/docs/api/fred/
- Series catalog: https://fred.stlouisfed.org/categories
- Terms: https://fred.stlouisfed.org/legal/

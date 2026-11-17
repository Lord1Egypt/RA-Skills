# world_bank — global development indicators (~1500 indicators × ~265 countries)

## What this source has

The World Bank Open Data API serves the WDI (World Development Indicators) plus dozens of allied datasets: GDP, GNI, life expectancy, literacy, poverty, climate, energy, governance. ~1500 indicators across ~265 country/region codes (countries plus aggregates like `WLD`, `EUU`, `LIC`). Annual time series, going back to 1960 for many indicators.

Indicator IDs are dotted strings: `NY.GDP.MKTP.CD` (GDP, current US$), `SP.POP.TOTL` (total population), `FP.CPI.TOTL.ZG` (inflation, consumer prices, annual %). Country codes are ISO-3 letter (`USA`, `DEU`, `JPN`) plus aggregates.

Use World Bank for: cross-country comparison, long-term development trends, "GDP per capita over 50 years", governance indicators (Worldwide Governance Indicators included). Pair with `fred` for higher-frequency US/global macro; pair with `rest_countries` for static metadata.

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
| Rate | no documented cap; the API is generous but slow under heavy load |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `indicator` | Time series for one indicator + country | `country`, `indicator` |
| `indicators` | Search/list indicators | none |
| `countries` | List countries / aggregates | none |

## Worked examples

```bash
# US GDP (current US$), all years available
python3 scripts/reach.py query world_bank indicator '{
  "country": "USA",
  "indicator": "NY.GDP.MKTP.CD",
  "per_page": 100
}'

# Compare GDP across multiple countries (semicolon-separated)
python3 scripts/reach.py query world_bank indicator '{
  "country": "USA;CHN;DEU;JPN",
  "indicator": "NY.GDP.MKTP.CD",
  "date": "2010:2024",
  "per_page": 200
}'

# Search for indicators about "renewable energy"
python3 scripts/reach.py query world_bank indicators '{
  "source": 2,
  "per_page": 50
}'

# All countries / regions
python3 scripts/reach.py query world_bank countries '{"per_page": 300}'
```

## Response shape

The World Bank wraps every response as a 2-element JSON array: `[<metadata>, <data>]`.

- `indicator` (with `format: json`): `[{page, pages, per_page, total, sourceid, lastupdated}, [{indicator: {id, value}, country: {id, value}, countryiso3code, date, value, unit, obs_status, decimal}, ...]]`. Element [1] is the time-series array.
- `indicators`: `[{...meta...}, [{id, name, unit, source: {id, value}, sourceNote, sourceOrganization, topics: [...]}, ...]]`.
- `countries`: `[{...meta...}, [{id, iso2Code, name, region: {id, iso2code, value}, adminregion, incomeLevel, lendingType, capitalCity, longitude, latitude}, ...]]`.

## Pitfalls

- **Response is `[meta, data]`**, not an object. Always destructure both. Forgetting this is the most common mistake.
- **`format: json` is mandatory** for JSON output (default is XML). The connector sets it via defaults.
- **`per_page` max is 32500** — high enough to fetch a full indicator history in one call. Default is 50, which truncates almost everything; raise it.
- **Country codes are ISO-3 letter** (`USA`), not alpha-2 (`US`). Multi-country: semicolon-separated (`USA;CHN`). Aggregates: `WLD` (world), `EUU` (EU), `LIC` (low income), etc.
- **`date` filter syntax.** Single year `2020`, range `2010:2020`. MRV (most recent value) shortcut: `mrv=1`.
- **`value: null` is common.** Many country-year pairs have no data. Filter on non-null before charting.
- **Indicator naming changes.** The Bank deprecates and renames indicators occasionally. `SP.DYN.LE00.IN` (life expectancy) has been stable; smaller indicators less so.
- **Sources are numbered.** `source: 2` is WDI; full list at the `/sources` endpoint. Filtering by source narrows the indicator universe.
- **Aggregates are arithmetic, not surveys.** "World" GDP is summed from country values where available, so partial coverage skews aggregates.

## Source links

- API docs: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
- Indicator catalog: https://data.worldbank.org/indicator
- Country/aggregate codes: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519

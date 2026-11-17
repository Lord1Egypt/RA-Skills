# census — US Census Bureau Data API

## What this source has

The US Census Bureau's API provides access to 100+ datasets covering demographics, economics, housing, and geography. Key datasets include:

- **American Community Survey (ACS)** — 1-year and 5-year estimates for social, economic, housing, and demographic characteristics. Updated annually.
- **Decennial Census** — Full population count every 10 years (2020 most recent).
- **Population Estimates Program (PEP)** — Annual population estimates between censuses.
- **Economic Census** — Business counts by NAICS, geography, and size. Every 5 years.
- **County Business Patterns** — Annual business establishment data.

Use Census for: population counts, median income, poverty rates, housing statistics, business density, demographic breakdowns, and geographic-level data (state, county, tract, block group, ZIP code).

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

No API key required. Rate limit is generous (500/day recommended polite default, no hard cap documented).

## Limits

| | |
|---|---|
| Daily | — (no hard cap; 500/day polite) |
| Monthly | — |
| Rate | no published cap |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `acs` | American Community Survey data | `year`, `get` (variable names), `for` (geography) |
| `decennial` | Decennial Census data | `year`, `get`, `for` |
| `population` | Population estimates | `year`, `get`, `for` |

## Worked examples

```bash
# Get total population for all US states (ACS 2021 1-year)
python3 scripts/reach.py query census acs '{"year": "2021", "get": "NAME,B01001_001E", "for": "state:*"}'

# Get median household income for California counties (ACS 5-year)
python3 scripts/reach.py query census acs '{"year": "2021", "get": "NAME,B19013_001E", "for": "county:*", "in": "state:06"}'

# Get 2020 Decennial Census population for the US
python3 scripts/reach.py query census decennial '{"year": "2020", "get": "NAME,P1_001N", "for": "us:1"}'

# Get population estimates for all counties
python3 scripts/reach.py query census population '{"year": "2022", "get": "POP_2022,NAME", "for": "county:*"}'
```

## Response shape

All actions return a JSON array of arrays. The first row is the header (variable names), subsequent rows are data values:

```json
[["NAME", "B01001_001E", "state"],
 ["Alabama", "5024279", "01"],
 ["Alaska", "733391", "02"]]
```

Variable codes (like `B01001_001E`) are documented in the Census Bureau's variable index. Use the `/variables.json` endpoint for a dataset to discover available variables.

## Pitfalls

- **Variable codes are dataset-specific.** `B01001_001E` in ACS means "total population" but the same code in a different dataset may not exist. Always check the variable list for the specific dataset/year.
- **Geography hierarchy matters.** The `for` parameter must match valid geographic entities. `state:*` works; `state:all` does not. Use `*` as wildcard.
- **5-year vs 1-year ACS.** 1-year ACS covers areas with population ≥65,000. 5-year ACS covers all geographies. Use 5-year for small areas.
- **API version paths.** The URL pattern is `/data/{year}/dataset_name`. Year must be a string.
- **Rate limiting is soft.** No hard cap, but aggressive polling may get throttled. Cache results locally when possible.

## Source links

- API docs: https://www.census.gov/data/developers/data-sets.html
- Variable index: https://api.census.gov/data/2021/acs/acs1/variables.html
- Geography reference: https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

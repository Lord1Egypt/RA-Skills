# rest_countries — country metadata (codes, capitals, currencies, languages)

## What this source has

REST Countries serves a single, hand-curated dataset: 250 countries (sovereign states + dependencies), each with name (common, official, native), ISO codes (alpha-2, alpha-3, numeric), capital(s), region/subregion, population, area, languages, currencies (ISO 4217), borders (alpha-3 codes of land neighbors), timezones, top-level domain, calling code, flag (SVG + emoji), coat of arms, lat/lng, and translations of the country name into ~25 languages.

The data is not real-time — it's a static curated snapshot updated occasionally. Population numbers may be a year or two stale.

Use REST Countries for: country code lookup, capital/currency/language quick reference, listing all countries in a region. Pair with `world_bank` for time-varying indicators (GDP, life expectancy); pair with `geonames` for richer admin/place data.

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
| Rate | no documented cap; the full dataset is small enough to cache locally |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `all` | All countries | none |
| `name` | Lookup by name (fuzzy) | `name` |
| `code` | Lookup by ISO alpha-2 or alpha-3 | `code` |
| `currency` | Countries using a given currency | `currency` (ISO 4217 like `USD`) |

## Worked examples

```bash
# All countries (full dump — slow, large)
python3 scripts/reach.py query rest_countries all '{"fields": "name,cca2,cca3,capital,population"}'

# Fuzzy name search
python3 scripts/reach.py query rest_countries name '{"name": "germany"}'

# Exact code lookup
python3 scripts/reach.py query rest_countries code '{"code": "JP"}'

# All countries using the euro
python3 scripts/reach.py query rest_countries currency '{"currency": "EUR"}'
```

## Response shape

All actions return arrays (even single-result lookups). Each country object:

```json
{
  "name": {"common": "Japan", "official": "Japan", "nativeName": {"jpn": {"official": "日本", "common": "日本"}}},
  "cca2": "JP", "cca3": "JPN", "ccn3": "392",
  "capital": ["Tokyo"], "region": "Asia", "subregion": "Eastern Asia",
  "languages": {"jpn": "Japanese"},
  "currencies": {"JPY": {"name": "Japanese yen", "symbol": "¥"}},
  "borders": [],
  "area": 377930, "population": 125836021,
  "timezones": ["UTC+09:00"], "continents": ["Asia"],
  "tld": [".jp"], "idd": {"root": "+8", "suffixes": ["1"]},
  "latlng": [36, 138],
  "flags": {"png": "...", "svg": "...", "alt": "..."},
  "translations": {"deu": {"common": "Japan"}, ...}
}
```

## Pitfalls

- **Even single-country lookups return a list.** `code` for `JP` returns `[{...one country...}]`. Index `[0]` defensively.
- **`name` is fuzzy by default.** "georgia" returns both Georgia (the country) and South Georgia. Pass `fullText=true` to require exact match.
- **`capital` is an array.** Some countries have multiple capitals (South Africa: Cape Town, Pretoria, Bloemfontein). Don't assume `[0]` is "the" one.
- **`languages` and `currencies` are dict-keyed** by ISO 639-3 / ISO 4217 codes, not arrays. Iterate keys, not values.
- **Dependencies vs sovereign states.** The dataset includes 250 entries; ~193 are UN members. Don't confuse "countries" counts.
- **`borders` is alpha-3 only.** Translate via `cca3` if you need to match against `cca2` lookups.
- **`fields` parameter trims response.** For list operations, pass `fields=name,cca2,population` to keep payloads small. Otherwise each country dump is ~3KB.
- **Population/area are static-ish.** For up-to-date demographics, use `world_bank`.

## Source links

- API docs: https://restcountries.com/
- Source code: https://gitlab.com/restcountries/restcountries
- License: Mozilla Public License 2.0

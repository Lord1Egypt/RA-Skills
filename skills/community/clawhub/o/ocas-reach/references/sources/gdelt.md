# gdelt — global news + TV events with sentiment

## What this source has

GDELT 2.0 is a planetary-scale event database built from open news media in 100+ languages, machine-translated to English in near-real-time. The Document API surfaces individual articles; the TV API queries the Internet Archive's TV news captions; the Geo API returns spatially-aggregated counts. Coverage is continuous from 2015 onward (Document 2.0); GDELT 1.0 events go back to 1979 but aren't exposed by this connector.

Each article comes annotated with tone (-100 to +100), themes (CAMEO/GKG taxonomies like `ECON_TAXATION` or `WB_2024_BANKING_FINANCE`), named entities, and geocoded mentions. There's no canonical document ID — articles are identified by their source URL.

Use GDELT for: "what is the world saying about X right now", sentiment trend over time, geographic clustering of coverage, finding obscure local-language coverage of a story. Pair with `federal_register` or `gov info` when the underlying event is a US government action; pair with `wikipedia` for the canonical encyclopedia entry on a story.

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
| Rate | no published cap; throttle yourself to <1 req/sec to avoid 429s |

A single Document API query returns at most 250 articles. Pagination is via `startdatetime`/`enddatetime` windows, not offsets.

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `doc_search` | Article search with tone/theme filters | `query` |
| `tv_search` | Search captioned US TV news (Internet Archive) | `query` |
| `geo` | Spatially-aggregated mentions | `query` |

## Worked examples

```bash
# Top articles about lithium mining, last 7 days, with tone metadata
python3 scripts/reach.py query gdelt doc_search '{
  "query": "lithium mining",
  "mode": "ArtList",
  "format": "json",
  "maxrecords": 50,
  "timespan": "7d"
}'

# Tone time-series for "central bank" coverage over 30 days
python3 scripts/reach.py query gdelt doc_search '{
  "query": "central bank",
  "mode": "TimelineTone",
  "format": "json",
  "timespan": "30d"
}'

# US TV mentions of "AI safety", last 24 hours
python3 scripts/reach.py query gdelt tv_search '{
  "query": "AI safety",
  "mode": "TimelineVol",
  "format": "json",
  "timespan": "1d"
}'

# Geographic heatmap of "wildfire" mentions
python3 scripts/reach.py query gdelt geo '{
  "query": "wildfire",
  "format": "GeoJSON",
  "timespan": "3d"
}'
```

## Response shape

`mode` controls the entire output schema:

- `ArtList` (default): `{articles: [{url, url_mobile, title, seendate, socialimage, domain, language, sourcecountry, ...}]}`. `seendate` is `YYYYMMDDTHHMMSSZ`.
- `TimelineTone` / `TimelineVol`: `{timeline: [{series, data: [{date, value}, ...]}]}`. Date format is `YYYYMMDDHHMMSS`.
- `TimelineLang` / `TimelineSourceCountry`: stacked time series keyed by language or country code.
- `geo` mode: GeoJSON `FeatureCollection` with point features per article cluster.

## Pitfalls

- **Date parsing is strict.** GDELT timestamps are `YYYYMMDDHHMMSS` with no separators — neither RFC-3339 nor Unix epochs work. Convert before comparing.
- **`timespan` vs `startdatetime`.** Pick one; if both are passed, GDELT silently uses `startdatetime` and ignores `timespan`. Valid `timespan`: `30min`, `4h`, `7d`, `1m`, `1y`.
- **`maxrecords` caps at 250.** Asking for more silently truncates. Window with `startdatetime`/`enddatetime` to page.
- **Mode determines schema, not just content.** Switching from `ArtList` to `TimelineTone` returns a completely different JSON skeleton. Always branch on `mode` in your post-processing.
- **Tone is per-article, computed at index time.** It's a scalar (-100 to +100), not a probability — treat as ordinal.
- **Some queries return HTML errors with 200.** GDELT's edge sometimes returns `<html>` even on success when the query language is malformed. Always check that the response parses as JSON.

## Source links

- Doc API docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- API guide: https://www.gdeltproject.org/data.html#documentation
- Terms: https://www.gdeltproject.org/about.html#termsofuse

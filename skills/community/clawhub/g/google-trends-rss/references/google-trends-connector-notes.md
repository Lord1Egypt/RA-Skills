# Google Trends Connector Notes

This skill mirrors the core behavior in `wsjwong/google-trends-connector`:

- Source endpoint (current): `https://trends.google.com/trending/rss?geo=<CODE>`
- Legacy endpoint (older connector): `https://trends.google.com/trends/trendingsearches/daily/rss?geo=<CODE>`
- Parse RSS `<item>` records plus `ht:` namespace fields:
  - `approx_traffic`
  - `picture`
  - `news_item` (title/snippet/url/source)
- Keep output tabular so it can be pasted into Sheets.

## Important Limits

- This is **daily trending searches** feed, not full historical keyword index.
- Coverage/latency is controlled by Google Trends.
- Geo input uses Google Trends country/region codes (e.g., `HK`, `US`, `JP`).
- Feed schema may change; keep parsing defensive.

## Suggested Output Columns

- title
- approx_traffic
- link
- pub_date
- picture
- news_1_title / news_1_snippet / news_1_url / news_1_source
- news_2_title / news_2_snippet / news_2_url / news_2_source

## Quick Validation

```bash
python scripts/google_trends_rss.py daily --geo HK --limit 5 --format table
python scripts/google_trends_rss.py daily --geo US --limit 10 --format json
python scripts/google_trends_rss.py daily --geo JP --out /tmp/jp-trends.csv
```

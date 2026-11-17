---
name: housing-market-research
description: Compare US housing markets through Crawlora's historical housing dataset and Redfin tools. Use for city, metro, county, or ZIP-code comparisons of prices, inventory, sales activity, time on market, and explicitly qualified affordability trends.
---

# Housing market research

Compare defined markets over comparable periods. Keep market aggregates separate
from individual property valuations and personalized financing decisions.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
dataset discovery/history and optional live Redfin context.

## Build a comparable market panel

1. Define geography level, candidate places, property type, period, and decision.
   Dataset `region_type` accepts `national`, `metro`, `county`, `city`, or `zip`.
   Use `/datasets/housing-markets/facets` and `/search` under the same prefix to
   resolve exact regions and `table_id`; names and ZIP codes are not table IDs.
2. Start with `latest=true`, a single region level, and a single property type.
   Latest is per series, so compare returned `period_begin` AND `period_end`.
   Select a common period if series differ. A monthly observation can summarize
   a longer rolling window; do not call every row one month's transactions.
3. Retrieve `/datasets/housing-markets/items/{region_type}/{table_id}` with
   `history=true` and the same `property_type` for the stored chronological
   series. Keep gaps, window lengths, and revisions visible. Use matched periods
   for YoY comparisons; overlapping windows are not independent observations.
4. Compare median sale/list prices, inventory, homes sold, and median days on
   market where populated. MoM/YoY fields are fractions: `0.05` means +5%.
   Preserve nulls; a thin market or unmatched metric is not a measured zero.
5. Treat affordability as a modeled comparison. Retain `income_vintage`,
   `income_geo_id`, and `mortgage_rate_pct`. Check the income geography actually
   matches the intended comparison; unavailable or broader-area income cannot
   establish precise neighborhood affordability. The dataset's salary estimate
   assumes 20% down, a 30-year fixed mortgage, 1.5% annual taxes/insurance, and a
   28% payment-to-income ratio. Disclose these assumptions and the income lag.
6. If requested, supplement with `/redfin/search?location=...` or live regional
   trends. These use numeric `region_type` and `region_id` values resolved by
   the live search response; dataset string types/table IDs are not a drop-in
   substitute. Live listings and historical market aggregates have different
   populations and dates; do not blend them into a single unlabeled statistic.
   Live trends can be display strings such as `$1.2M` or `+5%`; they are not the
   dataset's numeric dollars and fractional change fields.

```sh
scripts/crawlora.sh /datasets/housing-markets/search \
  region_type=city state_code=TX latest=true \
  'property_type=Single Family Residential' page_size=5
# Resolve table_id before requesting history for the same region/property type.
```

## Deliverable and interpretation

Return a comparison table and, when helpful, time-series charts with region,
property type, full measurement window, units, sample/activity counts, source,
collection time, and missing-data notes. Explain tradeoffs against the user's
criteria. Link the [Redfin source and methodology](https://www.redfin.com/news/data-center/)
alongside record provenance.

- Do not average ZIP/city medians to obtain a metro median, sum overlapping
  geographies, or sum overlapping rolling-window sales counts.
- A change in median price can reflect the mix of homes sold. It is not the
  appreciation rate of a fixed property. Low transaction counts weaken comparisons.
- Median-income affordability is not an individual's mortgage qualification or
  monthly budget. Keep custom scenarios and assumptions separate from returned data.
- Bound dataset pagination to `page_size<=100` and 10,000 results. A `404` item
  can mean an absent region/period/property-type combination. Back off on `429`,
  retry transient `5xx` once, stop on `401`/`403`, and check application `code`.

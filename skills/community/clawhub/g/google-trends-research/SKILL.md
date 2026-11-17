---
name: google-trends-research
description: Compare search interest, regional patterns, seasonality, and rising queries through Crawlora's Google Trends endpoints. Use for topic-demand briefs, keyword comparisons, and trending-topic research with correctly interpreted relative indices.
---

# Google Trends research

Produce a search-interest comparison with explicit terms, geography, time range,
and search property. Trends measures relative search interest, not sales,
population opinion, or absolute search volume.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1` and prints JSON.
Keep the key in the environment. Read [reference/endpoints.md](reference/endpoints.md)
for all eleven Trends tools.

## Choose the right query

1. Specify the terms, geography, time range, and purpose. Discover supported
   values with `/google/trends/enums`, `/locations`, and `/categories`. Explore
   categories and Trending Now categories are different accepted sets; use the
   relevant discovery response instead of transferring IDs between them.
2. For a comparison, POST to `/google/trends/explore/interest-over-time` with
   **flat** fields: `keywords` (1–5 strings), `geo`, `time_range`, and `type`.
   Do not nest them inside the catalog's `request` body label. Prefer `type`
   (`web`, `image`, `news`, `youtube`, `shopping`) over the legacy `property`.
3. Compare the terms in the same request. Hold geography, period, category,
   property, locale, and timezone constant. Use returned keyword labels to
   align values rather than assuming array positions across responses.
4. For a broader brief, `/google/trends/explore` combines the timeline with
   optional region/query/topic widgets. Use the specific `/interest-by-region`,
   `/top-queries`, `/rising-queries`, or `/related-topics` endpoint when only one
   component is needed. Omitted optional widgets in Explore are unavailable,
   not zero demand. A regional query can legitimately return an empty array.
5. For current events, GET `/google/trends/trending` with `geo`, `window`
   (`4h`, `24h`, `48h`, `7d`), and `limit` (max 100). Then POST a returned term
   as `query` to `/google/trends/trending/detail`. Explore uses different time
   strings, such as `today 12-m` or `now 7-d`; discover rather than mixing them.

```sh
scripts/crawlora.sh /google/trends/enums
scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time \
  '{"keywords":["coffee","tea"],"geo":"US","time_range":"today 12-m","type":"web"}'
```

## Interpret and report

- Interest scores are normalized 0–100 within the query context. Scores from
  independently scaled requests are not directly comparable. For more than five
  terms, present separate labeled panels or use an explicit shared-anchor method
  and describe its sampling/rounding limitations; never simply concatenate scores.
- A zero or `has_data=false` can reflect insufficient data. Preserve missing
  flags and partial periods when supplied instead of substituting zeros or
  declaring demand absent. Equal regional scores do not imply equal search counts.
- Distinguish a literal keyword from a related-topic entity. Do not silently
  replace one with the other. Preserve `Breakout` labels instead of inventing
  a precise growth percentage.
- Use a sufficiently long series before claiming seasonality. A single spike
  cannot establish a recurring pattern or its cause. Describe correlations and
  possible explanations separately from measured observations.

Return a chart/table or brief as requested, with terms, filters, collection time,
query/source URL where available, interpretation, and missing components. Label
the axis as a relative index. See [Google's data FAQ](https://support.google.com/trends/answer/4365533?hl=en)
for normalization and sampling context.

The service already retries throttled widgets. On `503`/`429`, honor
`Retry-After` when available and use a bounded retry; avoid rapid repeated calls
or concurrent widget fan-out. Stop on `401`/`403` and check application `code`.
Report missing results rather than fabricating a completed comparison.

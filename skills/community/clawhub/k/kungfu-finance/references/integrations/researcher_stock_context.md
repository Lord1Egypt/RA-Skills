# Researcher Integration Notes

This project should only use one researcher route:

- `/researcher/stock`

Nothing else from the researcher module should be integrated into `kungfu_finance` for now.

## Scope Decision

The skill remains:

- single-instrument first
- deterministic
- low-fanout
- analysis-oriented, not explorer-oriented

So the researcher module is only used for:

- single-stock forecast context
- single-stock covered-researcher context

It is not used for:

- report drill-down
- report links
- report original text
- global researcher ranking
- industry browsing
- concept browsing
- author-to-stock exploration

## The Only Route To Use

### `/researcher/stock`

Source:
- `serverless-tianshan-api/src/api/researcher_routes.py#L184`

Backed by:
- `serverless-tianshan-api/src/handlers/researcher/score_calculator.py#L864`
- `serverless-tianshan-api/src/handlers/researcher/score_calculator.py#L257`

Why this is enough:

- It is already single-stock scoped.
- It returns the two pieces of researcher information this project actually needs:
  - forecast summary
  - covered researcher ranking
- The current route no longer returns `latest_report`, and this project should not assume it does.

Recommended use in this project:

- as a data product for `deep_research`
- as optional enrichment for stock analysis
- not as a standalone browse flow

## Routes Not To Use

These routes should stay out of this project:

- `/researcher/rank`
- `/researcher/industries`
- `/researcher/industry/rank`
- `/researcher/concepts`
- `/researcher/concept/rank`
- `/researcher/detail`
- `/researcher/reports`
- `/researcher/stocks/by-authors`

Reason:

- they add browse/explorer behavior
- they increase fanout
- they push the skill away from single-stock deterministic analysis

## What Output Matters

Only the output contract of `/researcher/stock` matters for this project.

Expected shape:

```json
{
  "forecast": {
    "instrument_id": "600519",
    "security_name": "贵州茅台",
    "exchange_id": "SSE",
    "rating_org_num": 12,
    "rating_buy_num": 8,
    "rating_add_num": 3,
    "eps_current": 55.2,
    "eps_next": 61.8,
    "aim_price_max": 2100.0,
    "aim_price_min": 1850.0,
    "current_price": 1788.0,
    "actual_eps": 52.6
  },
  "researchers": [
    {
      "author_id": "xxx",
      "name": "张三",
      "org_name": "某证券",
      "total_score": 73.5,
      "report_count": 18,
      "stock_count": 11,
      "win_rate_1m": 66.7,
      "win_rate_3m": 61.1,
      "win_rate_6m": 58.8,
      "win_rate_1y": 54.5,
      "win_1m": 12,
      "win_3m": 11,
      "win_6m": 10,
      "win_1y": 9,
      "valid_1m": 18,
      "valid_3m": 18,
      "valid_6m": 17,
      "valid_1y": 16
    }
  ],
  "rank_by": "total"
}
```

## What Tests Should Check

If another AI writes the tests, it only needs to validate `/researcher/stock`.

Required checks:

- response contains `forecast`, `researchers`, `rank_by`
- `forecast` may be `null`
- `researchers` is always a list
- every researcher item contains:
  - `author_id`
  - `name`
  - `org_name`
  - `total_score`
- `rank_by` echoes the requested ranking period
- `instrument_id` is scoped to a single stock request
- no report list, report link, or report content fields are expected here

## Integration Rule For The Skill

The skill should treat `/researcher/stock` as a compact enrichment source.

It should not:

- branch into researcher detail pages
- fetch report cards
- fetch report links
- fetch report original text

One route is enough here.

# Recipe — Citation / Publication Trends (group_by year)

## Goal

Show how research volume (or another distribution) changes over time or across categories, using aggregation — no row fetching.

## When

The user asks "how has research on X grown", "publications per year", "OA share over time", or "which institutions publish most on X".

## Inputs

- A population to aggregate: topic, author, institution, OA status, year window.
- A `group_by` field (commonly `publication_year`).

## Steps

1. **Resolve any entity IDs** needed for the filter (topic/author/institution) via `openalex_search` / `autocomplete`.
2. **Group by year over a filtered population:**
   ```json
   {
     "tool": "openalex_group_by",
     "arguments": {
       "entity": "works",
       "group_by": "publication_year",
       "filter": "primary_topic.id:T11689,is_oa:true"
     }
   }
   ```
3. **Read `group_by`** — `[{key, key_display_name, count}]`. `results` is empty by design; `meta.count` is the total population.
4. **Optional second cut:** group by `open_access.oa_status` or `authorships.institutions.id` for share/leaderboard views.
5. **Present** as a table or simple chart, citing the filter used.

## Output

A year-by-year count table (and optionally OA share or top institutions), with the total `meta.count` and the exact filter stated.

## Example

```json
{
  "meta": { "count": 6470, "page": 1, "per_page": 200 },
  "results": [],
  "group_by": [
    { "key": "2022", "key_display_name": "2022", "count": 1840 },
    { "key": "2023", "key_display_name": "2023", "count": 2510 },
    { "key": "2024", "key_display_name": "2024", "count": 2120 }
  ]
}
```

> Open-access works on topic T11689: 2022: 1,840 · 2023: 2,510 · 2024: 2,120 (total 6,470). Filter: `primary_topic.id:T11689,is_oa:true`.

## Edge cases

- **Empty `group_by`** → the filter matched nothing; broaden it.
- **`400` on group_by field** → that field isn't groupable; pick a supported one.
- **Partial current year** → note that the latest year is still accruing.

## Production notes

- group_by is cheap (no row fetch) — prefer it for trends over scanning works.
- Always state the filter so the trend is reproducible.
- Set `OPENALEX_MAILTO`; cache aggregates with a medium TTL.

> Verification needed: confirm groupable fields with <https://docs.openalex.org>.

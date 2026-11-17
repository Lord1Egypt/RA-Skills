# Filters and Sorts — Getting the Right Rows

The query language is small and unforgiving: a filter whose type does not match the property type matches nothing and does not error. That silence is the defining failure of this file.

**Contents:** [The Type-Matching Rule](#the-type-matching-rule) · [Filter Conditions by Type](#filter-conditions-by-type) · [Compound Filters](#compound-filters) · [Timestamp and Relative Dates](#timestamp-and-relative-dates) · [Formula and Rollup Filters](#formula-and-rollup-filters) · [Sorts](#sorts) · [What the API Cannot Filter](#what-the-api-cannot-filter) · [Debugging an Empty Result](#debugging-an-empty-result)

**Before writing a non-trivial filter**, open `schemas/<data-source>.md` if `## Boxes` names one, and check for a saved payload in `artifacts/query-*.md`. Half the filters in a workspace have already been derived once.

## The Type-Matching Rule

The filter key must be the property's **type**, not what the value looks like:

```json
{"filter": {"property": "Status", "status": {"equals": "Done"}}}
```

If `Status` is a `select` property, that same filter returns `[]` — a `select` property needs `{"select": {"equals": "Done"}}`. Both are valid JSON, both return 200, one is always empty. The schema box is what tells them apart.

## Filter Conditions by Type

| Type | Conditions |
|---|---|
| rich_text, title, url, email, phone_number | `equals`, `does_not_equal`, `contains`, `does_not_contain`, `starts_with`, `ends_with`, `is_empty`, `is_not_empty` |
| number | `equals`, `does_not_equal`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to`, `is_empty`, `is_not_empty` |
| checkbox | `equals`, `does_not_equal` — takes `true`/`false`, and there is no empty state |
| select, status | `equals`, `does_not_equal`, `is_empty`, `is_not_empty` |
| multi_select | `contains`, `does_not_contain`, `is_empty`, `is_not_empty` — never `equals` |
| date, created_time, last_edited_time | `equals`, `before`, `after`, `on_or_before`, `on_or_after`, `is_empty`, `is_not_empty`, plus the relative set below |
| people, created_by, last_edited_by | `contains` (a user id), `does_not_contain`, `is_empty`, `is_not_empty` |
| relation | `contains` (a page id), `does_not_contain`, `is_empty`, `is_not_empty` |
| files | `is_empty`, `is_not_empty` only |
| formula | Nested by result type: `{"formula": {"string": {...}}}`, or `number`, `checkbox`, `date` |
| rollup | Nested by aggregation: `{"rollup": {"any": {...}}}`, `every`, `none`, or `number`/`date` for numeric rollups |
| unique_id | `equals`, `greater_than`, `less_than` — on the numeric part, not the prefix |

Examples:

```json
{"filter": {"property": "Tags", "multi_select": {"contains": "urgent"}}}
{"filter": {"property": "Assignee", "people": {"contains": "USER_ID"}}}
{"filter": {"property": "Company", "relation": {"contains": "PAGE_ID"}}}
{"filter": {"property": "external_id", "rich_text": {"equals": "recAbc123"}}}
```

The last one is the idempotency check every import runs before creating a row (SKILL.md Rule 6).

## Compound Filters

```json
{"filter": {"and": [
  {"property": "Status", "status": {"does_not_equal": "Done"}},
  {"or": [
    {"property": "Due", "date": {"on_or_before": "2026-08-31"}},
    {"property": "Priority", "select": {"equals": "P0"}}
  ]}
]}}
```

- `and` / `or` take arrays and can nest, but nesting is depth-limited and the error when you exceed it does not say so.
- Keep the server-side filter to what the API expresses well and finish in code. A filter nobody can read is re-derived from scratch in six months — save the one that works to `artifacts/`.
- `does_not_equal` and `does_not_contain` **exclude empty values too** on some types: a row with no Status is not returned by `{"status": {"does_not_equal": "Done"}}` in the way most people expect. Add an explicit `is_empty` branch in an `or` when unset rows must be included.

## Timestamp and Relative Dates

```json
{"filter": {"timestamp": "last_edited_time", "last_edited_time": {"after": "2026-07-01T00:00:00Z"}}}
```

- `timestamp` filters address `created_time` and `last_edited_time` without a property existing for them. This is the backbone of polling-based sync (`sync.md`).
- Relative conditions: `past_week`, `past_month`, `past_year`, `this_week`, `next_week`, `next_month`, `next_year`, each taking `{}`. They are evaluated in the workspace's frame, not yours — for reproducible jobs, compute the absolute timestamp yourself.
- A date-only property compared against a datetime matches on the date part; mixing the two in one query is how "yesterday's rows" go missing.

## Formula and Rollup Filters

- The nesting must match the formula's **result** type, which the schema reports. A formula returning a string filtered as a number returns `[]`.
- Rollup filters: `any`/`every`/`none` wrap a condition on the rolled-up property's type; numeric aggregations filter directly with `number`.
- Both are computed server-side and can lag a write to their inputs — never filter on a formula you set milliseconds ago in the same loop.

## Sorts

```json
{"sorts": [
  {"property": "Priority", "direction": "descending"},
  {"property": "Due", "direction": "ascending"}
]}
{"sorts": [{"timestamp": "last_edited_time", "direction": "ascending"}]}
```

- Sorts are applied in array order.
- Sorting by `select` or `status` uses the option order defined in the schema, not alphabetical — reordering options in the UI silently reorders every API result.
- **A paginated job must sort deterministically.** Rows edited during a long export move under an unstable sort and get skipped or duplicated; sort ascending by `created_time` for stable full scans (`pagination.md`).

## What the API Cannot Filter

Know these before promising a query:

- **Page content.** Blocks are not searchable or filterable; only property values are.
- **Search does not look at property values** at all (`search.md`).
- Case-insensitive matching is not selectable; `contains` behaves case-insensitively for text but `equals` is exact.
- Cross-source joins. A filter addresses one data source; combining two is code.
- Rollups of rollups, and conditions the rollup functions do not offer.
- Sorting by a relation, or by anything other than a property or a timestamp.

## Debugging an Empty Result

In this order — each step is one request and rules out a whole class:

1. Query with **no filter**, `page_size: 1`. Empty means the source is empty or unreachable, not the filter.
2. Compare the filter key against the property `type` in the schema box. This is the answer most of the time.
3. Compare the value against the option list in the schema, character for character — a renamed option matches nothing (`## Gotchas`).
4. Drop the compound to a single condition, then add conditions back one at a time.
5. Check whether the rows are archived: archived pages are excluded by default.
6. If it now works, **save the payload to `artifacts/query-<what>.md`** before moving on.

**When a filter finally returns the right rows**, write it to `~/Clawic/data/notion-api-integration/artifacts/query-<what>.md` — the endpoint, the payload, why it is shaped that way, the row count and the request count — and add its `## Boxes` line in the same turn. Deriving a compound filter is the most repeated wasted hour in this domain.

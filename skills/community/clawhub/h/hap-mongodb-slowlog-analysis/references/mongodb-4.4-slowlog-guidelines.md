# MongoDB 4.4 Slowlog Guidelines

## What to Extract

For each slow query event, try to extract:

- Namespace: `ns`
- Operation family: `find`, `aggregate`, `count`, `update`, `remove`
- `planSummary`
- `keysExamined`
- `docsExamined`
- `nreturned`
- `durationMillis`
- `hasSortStage`
- Filter fields
- Sort fields
- Projection fields
- Limit or batch size

## How to Read the Main Signals

- `COLLSCAN` in `planSummary` usually means a missing or unusable index.
- Very high `docsExamined` compared with low `nreturned` usually means poor selectivity or poor index shape.
- High `keysExamined` and high `docsExamined` together often mean the query uses an index but still scans too broadly.
- A sort paired with broad scans may indicate the index order does not support both filtering and sorting.
- Low `nreturned` with high `durationMillis` often means the server spent time scanning or sorting rather than returning rows.

## Heuristic for Compound Indexes

Prefer this ordering unless evidence suggests otherwise:

1. Equality filter fields
2. Sort fields
3. Range fields

Do not blindly include every filter field. Exclude low-value fields and fields the project has declared out of scope.

## Non-Index-Friendly Predicates

Strictly follow the project slow-query rules for predicates that do not use ordinary indexes well:

- Negative predicates such as `$ne`, `$nin`, `$not`, "not contains", and "does not start with" should not drive normal index recommendations.
- Mixed empty checks such as `null`, `""`, missing field, and `$size: 0` should not be treated as a strong indexable equality shape.
- Plain contains regex and case-insensitive regex usually have poor ordinary B-tree index benefit.
- Nested `$or` branches with empty checks often need query rewrite before index design.

Preferred rewrite:

- Keep the original field key.
- Normalize writes so empty or missing business values are stored as one canonical default value.
- Query that default value with exact equality, for example `{ "field": "__EMPTY__" }` or another business-approved enum/default.
- Keep the field type consistent; do not mix `null`, `""`, `[]`, scalar defaults, and array values for the same logical predicate.
- Normalize historical data before relying on the rewritten query shape.

Only suggest a new helper/derived field when the user explicitly says the original field value cannot be normalized but adding fields is allowed.

## Project-Specific Constraints

These constraints are mandatory for this skill:

- HAP worksheet collections whose collection names start with `ws` have these default single-field indexes:
  - `{ "_id": 1 }`
  - `{ "utime": 1 }`
  - `{ "rowid": 1 }`
  - `{ "ctime": 1 }`
- Never recommend recreating those single-field indexes for `ws*` collections.
- If `_id`, `utime`, `rowid`, or `ctime` appears in a recommendation, make clear whether it is already a default single-field index or is being considered only as part of a compound index.
- `status` has only two values: `1` and `9`.
- `1` means active/in-use.
- Never include `status` in a recommended index definition because it is low-cardinality and not useful enough for index design here.

When either field appears in the query:

- Mention `_id`, `utime`, `rowid`, and `ctime` as default indexed fields for `ws*` collections when it matters to the explanation.
- Mention `status` as a business filter that should not drive index design.

## Advice Patterns

### If `planSummary` is `COLLSCAN`

- Look for equality filters with meaningful selectivity.
- Propose a compound index using those equality fields and any supported sort fields.
- If the only visible fields are `ctime` and `status`, explicitly avoid recommending a new index from that evidence alone.

### If an Index Exists but the Scan Is Still Large

- Compare the filter shape with the likely current index order.
- Suggest reordering a compound index to match equality predicates first.
- Point out when a sort field probably belongs before a trailing range field.

### If the Query Uses Sort

- Say whether the sort likely benefits from index support.
- Recommend matching sort direction when it matters.
- Avoid recommending a sort-supporting index if the visible filter is too weak or dominated by excluded fields.
- Treat `_id` as already indexed by default.
- Never recommend creating a single-field `_id` index.
- For `ws*` collections, also never recommend creating single-field `utime`, `rowid`, or `ctime` indexes.
- When `sort: { _id: 1/-1 }` appears with business filters, explain that `_id` may only be serving sort order.
- Only include `_id` as the trailing key of a compound index when planner evidence shows `_id` sort order is still a bottleneck after query predicates are index-friendly.
- For incomplete command payloads without `planSummary`, do not include `_id` in post-rewrite candidate indexes by default; mention it as something to re-evaluate after `explain("executionStats")`.

### If the Query Returns Too Many Fields

- Suggest narrowing the projection if the log or command payload shows broad document fetch.

### If Pagination Looks Expensive

- Suggest seek-based pagination or tighter predicates instead of deep skip patterns when applicable.

## Confidence Language

Use:

- `High confidence` when filter, sort, and planner evidence are all visible.
- `Medium confidence` when some fields are missing but the planner evidence is still strong.
- `Low confidence` when the snippet is incomplete and only provisional guidance is possible.

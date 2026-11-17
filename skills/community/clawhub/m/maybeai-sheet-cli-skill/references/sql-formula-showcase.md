# `=SQL(...)` Formula Showcase

## Contents

1. When to use this
2. When to use `=SQL(...)`
3. Assumed worksheet layout
4. Showcase formula
5. `excel-worksheet range set-formula` example
6. Saved state and recalculation
7. Verification flow
8. Notes

## 1. When to use this

Use this document when you want to showcase live SQL capability in MaybeAI Sheet instead of writing a one-time static result table.

This document assumes the current routed online runtime model:

- new examples no longer assume SQLite-only behavior
- examples are written as PG-backed worksheet SQL
- validate non-trivial SQL by calculating the corresponding `=SQL(...)` formula on a disposable target when needed

This is appropriate when you want to:

- anchor a spilling SQL result block at `A1` in a report sheet
- keep a result block live as source worksheets change
- demonstrate `join`, `group by`, `order by`, and `limit` with a single formula

## 2. When to use `=SQL(...)`

Priority:

- For a live workbook formula, use `mbs excel-worksheet range set-formula` with `=SQL("...")`
- For a one-time static result table, use a first-class command only if current `mbs --help` exposes one; otherwise prefer a live `=SQL(...)` formula

Difference:

- `=SQL(...)` stores a formula in the workbook
- a static result write would store ordinary cell values for that execution result
- If the source data will change later and you want the report logic to stay live, prefer `=SQL(...)`
- `mbs excel-worksheet range set-formula` saves the `=SQL(...)` formula automatically when the command succeeds; no separate save step is required

## 3. Assumed worksheet layout

Assume the workbook has three worksheets:

- `Orders`
  - `Order ID`
  - `Region`
  - `SKU`
  - `Revenue`
- `Products`
  - `SKU`
  - `Category`
- `Report`
  - used to hold the SQL formula result

This example writes a formula into `Report!A1` that returns a Top 20 revenue summary by category and region.

## 4. Showcase formula

Recommended for `Report!A1`:

```text
=SQL("select p.""Category"" as ""Category"", o.""Region"" as ""Region"", count(*) as ""Orders"", round(sum(cast(o.""Revenue"" as real)), 2) as ""Revenue"", round(avg(cast(o.""Revenue"" as real)), 2) as ""Avg Revenue"" from ""Orders"" o left join ""Products"" p on o.""SKU"" = p.""SKU"" where trim(coalesce(o.""Region"", '')) <> '' group by p.""Category"", o.""Region"" order by ""Revenue"" desc limit 20")
```

This example demonstrates:

- cross-worksheet `left join`
- `count(*)`
- `sum(...)`
- `avg(...)`
- `round(...)`
- `group by`
- `order by`
- `limit`

Raw SQL before converting to the Excel formula string:

```sql
select
  p."Category" as "Category",
  o."Region" as "Region",
  count(*) as "Orders",
  round(sum(cast(o."Revenue" as real)), 2) as "Revenue",
  round(avg(cast(o."Revenue" as real)), 2) as "Avg Revenue"
from "Orders" o
left join "Products" p on o."SKU" = p."SKU"
where trim(coalesce(o."Region", '')) <> ''
group by p."Category", o."Region"
order by "Revenue" desc
limit 20
```

## 5. `excel-worksheet range set-formula` example

CLI:

```bash
FORMULA=$(cat <<'EOF'
=SQL("select p.""Category"" as ""Category"", o.""Region"" as ""Region"", count(*) as ""Orders"", round(sum(cast(o.""Revenue"" as real)), 2) as ""Revenue"", round(avg(cast(o.""Revenue"" as real)), 2) as ""Avg Revenue"" from ""Orders"" o left join ""Products"" p on o.""SKU"" = p.""SKU"" where trim(coalesce(o.""Region"", '')) <> '' group by p.""Category"", o.""Region"" order by ""Revenue"" desc limit 20")
EOF
)

mbs excel-worksheet range set-formula \
  --doc-id <DOC_ID> \
  --worksheet-name Report \
  --cell A1 \
  --formula "$FORMULA"
```

Request shape:

```json
{
  "uri": "https://www.maybe.ai/docs/spreadsheets/d/<document_id>",
  "worksheet_name": "Report",
  "cell": "A1",
  "formula": "=SQL(\"select p.\"\"Category\"\" as \"\"Category\"\", o.\"\"Region\"\" as \"\"Region\"\", count(*) as \"\"Orders\"\", round(sum(cast(o.\"\"Revenue\"\" as real)), 2) as \"\"Revenue\"\", round(avg(cast(o.\"\"Revenue\"\" as real)), 2) as \"\"Avg Revenue\"\" from \"\"Orders\"\" o left join \"\"Products\"\" p on o.\"\"SKU\"\" = p.\"\"SKU\"\" where trim(coalesce(o.\"\"Region\"\", '')) <> '' group by p.\"\"Category\"\", o.\"\"Region\"\" order by \"\"Revenue\"\" desc limit 20\")",
  "skip_recalculation": false
}
```

## 6. Saved state and recalculation

`mbs excel-worksheet range set-formula` has two effects by default:

1. It saves the formula into the target cell.
2. It recalculates the formula immediately, so the SQL result should spill into the surrounding cells.

`skip_recalculation` changes only the second effect:

| Setting | Saved formula | SQL spill result |
|---------|---------------|------------------|
| default / `skip_recalculation=false` | Saved automatically on success | Refreshed immediately |
| `--skip-recalculation` / `skip_recalculation=true` | Saved automatically on success | May remain stale or absent until calculate runs |

After `--skip-recalculation`, refresh explicitly:

```bash
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name Report
# or, if downstream sheets depend on the result:
mbs workbook calculate --doc-id <DOC_ID>
```

## 7. Verification flow

Suggested flow:

1. `mbs workbook list-worksheets`
2. `mbs excel-table schema` or `mbs db-table schema` to confirm column names in `Orders` and `Products`
3. Optionally validate the SQL by calculating the corresponding `=SQL(...)` formula on a disposable target
4. Confirm the spill area around `Report!A1` can be overwritten
5. Call `mbs excel-worksheet range set-formula` with `=SQL(...)`
6. Optionally call `mbs formula read --doc-id <DOC_ID> --worksheet-name Report --range A1:A1` to confirm the formula was saved
7. By default, that request calculates the SQL formula and materializes the spill result
8. `mbs excel-worksheet range read` to verify `Report`

If you intentionally set `skip_recalculation=true`, the formula is still saved,
but the visible result may not be refreshed. Call `mbs excel-worksheet calculate`
or `mbs workbook calculate` afterwards.

## 8. Notes

- The SQL text inside `=SQL(...)` lives inside an Excel string literal, so internal double quotes must be written as `""`
- Static SQL result writes are not currently documented as a supported CLI workflow unless a first-class command appears in `mbs --help`
- The spill result will overwrite the anchor cell area and adjacent cells, so do not anchor it where existing content must be preserved
- For non-trivial SQL, validate with a disposable formula calculation before writing into the final report location
- The examples assume PG-backed worksheet SQL, but a conservative SQL subset is still the safest default
- If a worksheet name contains spaces, continue to use double quotes, for example `"Sales Data"`

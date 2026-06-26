# `=SQL(...)` Formula Showcase

## Contents

1. When to use this
2. When to use `=SQL(...)`
3. Assumed worksheet layout
4. Showcase formula
5. `formula/set` example
6. Verification flow
7. Notes

## 1. When to use this

Use this document when you want to showcase live SQL capability in MaybeAI Sheet instead of writing a one-time static result table.

This document assumes the current routed online runtime model:

- new examples no longer assume SQLite-only behavior
- examples are written as PG-backed worksheet SQL
- you should still validate the SQL with `sql/compile` first

This is appropriate when you want to:

- anchor a spilling SQL result block at `A1` in a report sheet
- keep a result block live as source worksheets change
- demonstrate `join`, `group by`, `order by`, and `limit` with a single formula

## 2. When to use `=SQL(...)`

Priority:

- For a live workbook formula, use `POST /api/v1/excel/formula/set` with `=SQL("...")`
- For a one-time static result table, use `sql/compile` + `sql/write_result`

Difference:

- `=SQL(...)` stores a formula in the workbook
- `sql/write_result` writes ordinary cell values for that execution result
- If the source data will change later and you want the report logic to stay live, prefer `=SQL(...)`

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

If you want to validate the raw SQL first with `sql/compile`, use:

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

## 5. `formula/set` example

```json
{
  "uri": "https://www.maybe.ai/docs/spreadsheets/d/<document_id>",
  "worksheet_name": "Report",
  "cell": "A1",
  "formula": "=SQL(\"select p.\"\"Category\"\" as \"\"Category\"\", o.\"\"Region\"\" as \"\"Region\"\", count(*) as \"\"Orders\"\", round(sum(cast(o.\"\"Revenue\"\" as real)), 2) as \"\"Revenue\"\", round(avg(cast(o.\"\"Revenue\"\" as real)), 2) as \"\"Avg Revenue\"\" from \"\"Orders\"\" o left join \"\"Products\"\" p on o.\"\"SKU\"\" = p.\"\"SKU\"\" where trim(coalesce(o.\"\"Region\"\", '')) <> '' group by p.\"\"Category\"\", o.\"\"Region\"\" order by \"\"Revenue\"\" desc limit 20\")",
  "skip_recalculation": false
}
```

## 6. Verification flow

Suggested flow:

1. `list_worksheets`
2. `read_headers` to confirm the column names in `Orders` and `Products`
3. Validate the raw SQL with `sql/compile`
4. Confirm the spill area around `Report!A1` can be overwritten
5. Call `formula/set` with `=SQL(...)`
6. By default, that request calculates the SQL formula and materializes the spill result
7. `read_sheet` to verify `Report`

If you intentionally set `skip_recalculation=true`, or if other formulas depend on this spill result, call `recalculate_formulas` afterwards.

## 7. Notes

- The SQL text inside `=SQL(...)` lives inside an Excel string literal, so internal double quotes must be written as `""`
- `sql/compile` and `sql/write_result` use raw SQL, not Excel formula strings
- The spill result will overwrite the anchor cell area and adjacent cells, so do not anchor it where existing content must be preserved
- For non-trivial SQL, always compile first
- The examples assume PG-backed worksheet SQL, but a conservative SQL subset is still the safest default
- If a worksheet name contains spaces, continue to use double quotes, for example `"Sales Data"`

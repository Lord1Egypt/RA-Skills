# Formulas and SQL Reference

## Contents

1. When to use this
2. Formula endpoints
3. SQL result-table flow
4. SQL authoring rules
5. Common workflows

## 1. When to use this

Read this document when the task involves writing formulas, recalculating formulas, building SQL pivots or result tables, or verifying result sheets.

## 2. Formula endpoints

```text
POST /api/v1/excel/formula/batch_set
POST /api/v1/excel/formula/set
POST /api/v1/excel/calc-formula
POST /api/v1/excel/calc_formulas
POST /api/v1/excel/recalculate_formulas
```

Guidance:

- Use `formula/batch_set` when you need to persist a report block or many formulas in one workbook
- Use `formula/set` when you want to persist one cell or a sparse one-off fix
- Use `calc-formula` or `calc_formulas` for temporary preview or debugging
- Use `recalculate_formulas` when you need a broader refresh after data changes
- `formula/set` calculates the target formula as part of that request
- For batch report builds, prefer `formula/batch_set` with rectangular `operations[]` and one final `recalculate_mode`
- Phase 1 `formula/batch_set` is for ordinary workbook formulas only; do not use it for `=SQL(...)` or pivot formulas
- If you explicitly pass `skip_recalculation=true`, or you also need to refresh downstream formulas or report logic, call `recalculate_formulas` afterwards

Script: `scripts/06-formulas.sh`

## 3. SQL result-table flow

Default flow:

1. `list_worksheets`
2. `read_headers`
3. Optionally `read_sheet` for a sample
4. `sql/compile`
5. `sql/write_result`
6. `read_sheet` to verify the result sheet

Core endpoints:

```text
POST /api/v1/excel/sql/compile
POST /api/v1/excel/sql/write_result
```

Do not skip `compile`.

## 4. SQL authoring rules

Prefer PostgreSQL-compatible worksheet SQL, but stay within a conservative subset.

Recommended default subset:

- `select`
- `with`
- `where`
- `group by`
- `having`
- `order by`
- `limit`
- `left join`
- `inner join`
- `coalesce`
- `round`
- `cast`
- `case when`
- `nullif`
- `count` / `sum` / `avg` / `min` / `max`

Practical assumption for this skill:

- The online SQL path is PostgreSQL-backed
- Agents should still prefer worksheet SQL that is easy to compile, portable, and easy to rewrite

Hard boundaries:

- only `SELECT` or `WITH ... SELECT`
- no multiple statements
- no `INSERT` / `UPDATE` / `DELETE` / DDL
- no `SELECT INTO`
- no row-locking clauses such as `FOR UPDATE`
- do not reference `pg_catalog`, `information_schema`, `public`, or internal worksheet metadata tables

Not recommended:

- MySQL backticks
- SQL Server `TOP`
- BigQuery-only structures
- heavy PostgreSQL-specific features that have not been validated with `sql/compile`

Notes:

- `ILIKE` is no longer treated as automatically forbidden
- whether it works in practice still depends on `sql/compile`
- in many cases, `lower(...) like ...` is a safer default than depending on a more specific dialect feature

Table naming rules:

- Prefer worksheet names directly
- If a worksheet name contains spaces, wrap it in double quotes, for example `"Sales Data"`
- If a historical workflow already uses `gid_*`, that is still acceptable, but new examples should prefer worksheet names

Extra rules for `=SQL("...")`:

- the SQL text lives inside an Excel string literal
- internal double quotes must be doubled as `""`
- for example, raw SQL `"Revenue"` becomes `""Revenue""` inside the formula

If `WITH` is rejected by the backend, rewrite it as an inline subquery and compile again.

## 5. Common workflows

### Build a regional revenue result table

1. `read_headers`
2. Write PostgreSQL-compatible worksheet SQL:

```sql
select "Region", sum("Revenue") as "Revenue"
from "Orders"
group by "Region"
order by "Revenue" desc
```

3. `sql/compile`
4. `sql/write_result`
5. `read_sheet` to verify `Pivot_RegionRevenue`

### Recalculate after syncing business data

1. `update_range_by_lookup`
2. `recalculate_formulas`
3. `read_sheet`

### Write formulas into a new report worksheet

1. `write_new_worksheet`
2. Group derived cells into rectangular blocks
3. Use `formula/batch_set`
4. Prefer `recalculate_mode=workbook` if downstream sheets reference these blocks
5. `read_sheet`

Example payload:

```json
{
  "uri": "https://www.maybe.ai/docs/spreadsheets/d/<doc_id>",
  "skip_recalculation": true,
  "recalculate_mode": "workbook",
  "operations": [
    {
      "worksheet_name": "利润分析",
      "range_address": "B2:F3",
      "formulas": [
        ["='利润表-2025Q1'!D4/10000", "='利润表-2025Q2'!D4/10000", "='利润表-2025Q3'!D4/10000", "='利润表-2025Q4'!D4/10000", "=SUM(B2:E2)"],
        ["='利润表-2025Q1'!D5/10000", "='利润表-2025Q2'!D5/10000", "='利润表-2025Q3'!D5/10000", "='利润表-2025Q4'!D5/10000", "=SUM(B3:E3)"]
      ]
    }
  ]
}
```

### Write a live SQL formula into a report worksheet

1. `write_new_worksheet`
2. Write the raw SQL and validate it with `sql/compile`
3. Use `formula/set` to write `=SQL("...")`

Raw SQL for `sql/compile`:

```sql
select "Region", sum("Revenue") as "Revenue"
from "Orders"
group by "Region"
order by "Revenue" desc
```

Formula text for `formula/set`:

```text
=SQL("select ""Region"", sum(""Revenue"") as ""Revenue"" from ""Orders"" group by ""Region"" order by ""Revenue"" desc")
```

4. By default, that request calculates and writes the target formula result
5. If you explicitly skipped recalculation, or if other formulas depend on this result block, call `recalculate_formulas`
6. `read_sheet`

Reference:

- `references/sql-formula-showcase.md`

# Formulas and SQL Reference

## Contents

1. When to use this
2. Formula commands
3. Persistence and recalculation state
4. SQL formula flow
5. SQL authoring rules
6. Common workflows

## 1. When to use this

Read this document when the task involves writing formulas, recalculating formulas, building SQL result tables, or verifying result sheets. For persisted pivot tables, use `mbs pivot` instead of formula authoring.

## 2. Formula commands

Guidance:

- Use `mbs excel-worksheet range set-formula` when you need to persist one worksheet formula or a batch of worksheet formulas.
- Use `mbs formula batch-set` when you need the workbook-level batch alias for many formulas across worksheets.
- Treat `mbs formula set` as a compatibility alias for single worksheet formula writes; prefer the `excel-worksheet range` form in new examples.
- Use `mbs db-table range set-formula` when the target is a PG/SheetTable-backed table.
- Use `mbs excel-worksheet range calculate` for temporary preview or debugging.
- Use `mbs excel-worksheet calculate` for one-sheet refresh after data changes.
- Use `mbs workbook calculate` when downstream formulas span worksheets.
- Use `mbs excel-worksheet check-error` after writes or recalculation when the result worksheet must be free of worksheet errors.
- For batch report builds, prefer rectangular `operations[]` and one final `recalculate_mode`.
- Batch formula setting is for ordinary workbook formulas; do not use it for `=SQL(...)` or pivot formulas. For persisted pivots, use `mbs pivot preview` / `mbs pivot upsert`.
- `mbs excel-worksheet range set-formula` is a saved workbook write. If the command succeeds, the target cell contains the formula; there is no separate save command.
- If you explicitly pass `--skip-recalculation`, the formula is still saved, but the displayed value or SQL spill output may not refresh until you call `mbs excel-worksheet calculate` or `mbs workbook calculate`.

CLI:

```bash
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name <SHEET> --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --operations ops.json --recalculate-mode worksheet
mbs formula batch-set --doc-id <DOC_ID> --operations ops.json --recalculate-mode worksheet
mbs db-table range set-formula --doc-id <DOC_ID> --name Orders --cell G2 --formula '=SQL("select * from Orders limit 10")'
mbs workbook calculate --doc-id <DOC_ID>
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs formula read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:E20
mbs excel-worksheet range calculate --doc-id <DOC_ID> --worksheet-name <SHEET> --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs formula lineage --doc-id <DOC_ID> --worksheet-name <SHEET> --cell E2 --format tree
```

For SQL-over-sheet work, choose the persistence model deliberately:

- Use live `=SQL(...)` formulas through `excel-worksheet range set-formula` or
  `db-table range set-formula` when the workbook should recalculate from source
  tables later.
- Use `db-table create-from-query` when the result should become a reusable
  PG/SheetTable handoff table. Current CLI versions still try to keep the
  source `=SQL(...)` formula in the final table cell, defaulting to `A1`, and
  report that attempt in `context.formula_trace`.
- For user-facing silver handoffs such as `OrderDetailsStructureInput`, treat
  `A1 =SQL(...)` as a **pass gate**. If `formula_trace` is not `persisted`, or
  A1 only shows a materialized header (for example `period`), run
  `mbs db-table range set-formula --cell A1 --formula '=SQL("...")'` and
  re-check with `mbs formula read --range A1`. Do not use
  `--no-preserve-formula` on those tables.
- For native pivot-table aggregation, do not hand-build `MAYBE_PIVOT(...)` or
  call pivot APIs through `raw post`. Author a JSON pivot config and run
  `mbs pivot preview` before `mbs pivot upsert --target-worksheet-name ... --anchor-cell ...`.

## 3. Persistence and recalculation state

`mbs excel-worksheet range set-formula` and the `formula set` alias change workbook state.
Treat them like writing a formula into a cell in Excel or Google Sheets.

| Action | Saved formula state | Displayed result state |
|--------|---------------------|------------------------|
| `mbs excel-worksheet range set-formula ... --formula '=SQL(...)'` succeeds | Formula is saved in the target cell | Recalculated immediately by default |
| Same command with `--skip-recalculation` | Formula is still saved in the target cell | Existing displayed value may remain stale until a calculate command runs |
| Source worksheet data changes later | Formula remains saved | SQL spill result may need `mbs excel-worksheet calculate` or `mbs workbook calculate` |
| `mbs excel-worksheet range calculate` | Does not document a persistent save workflow | Useful for preview/debugging a formula result |

Verification should check both layers when precision matters:

```bash
# Confirm the saved formula text.
mbs formula read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:A1

# Confirm the visible/spilled result values.
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:E20 --output table

# Scan the worksheet for formula-style errors or missing cached results.
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name <SHEET>
```

## 4. SQL formula flow

Default flow:

1. `mbs workbook metadata`
2. `mbs workbook list-worksheets`
3. `mbs excel-table schema` or `mbs db-table schema`
4. Optionally read a sample with `excel-table sample`, `db-table sample`, or `excel-worksheet range read`
5. Convert the SQL into a `=SQL("...")` formula, doubling internal double quotes
6. Use `mbs excel-worksheet range set-formula` on the target cell; on success, the formula is saved automatically
7. Verify the saved formula with `formula read` if needed
8. Verify the spill result with `excel-worksheet range read`, `excel-table sample`, or `workbook list-worksheets`
9. Run `excel-worksheet check-error` on the worksheet before claiming the report is healthy

For reusable PG/SheetTable handoff tables, replace steps 6-9 with
`mbs db-table create-from-query --sql-file ... --verify`, then inspect
`context.formula_trace` in JSON output and sample the created table. If
`formula_trace.persisted` is false, report the traceability limitation instead
of implying the created table still contains the source formula in `A1`.

For temporary validation, use `mbs excel-worksheet range calculate` with the
`=SQL(...)` formula on a disposable target cell or worksheet.

## 5. SQL authoring rules

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
- heavy PostgreSQL-specific features unless you have validated them against the current formula runtime

Notes:

- `ILIKE` is no longer treated as automatically forbidden
- whether it works in practice still depends on the current backend SQL formula runtime
- in many cases, `lower(...) like ...` is a safer default than depending on a more specific dialect feature

Table naming rules:

- Prefer worksheet names directly
- If a worksheet name contains spaces, wrap it in double quotes, for example `"Sales Data"`
- If a historical workflow already uses `gid_*`, that is still acceptable, but new examples should prefer worksheet names

Extra rules for `=SQL("...")`:

- the SQL text lives inside an Excel string literal
- internal double quotes must be doubled as `""`
- for example, raw SQL `"Revenue"` becomes `""Revenue""` inside the formula

If `WITH` is rejected by the backend, rewrite it as an inline subquery and recalculate again.

## 6. Common workflows

### Build a regional revenue result table

1. `mbs excel-table schema` or `mbs db-table schema`
2. Write PostgreSQL-compatible worksheet SQL:

```sql
select "Region", sum("Revenue") as "Revenue"
from "Orders"
group by "Region"
order by "Revenue" desc
```

3. Write it as `=SQL("...")` in the report worksheet with `mbs excel-worksheet range set-formula`
4. The formula is saved automatically if the command succeeds
5. `mbs excel-worksheet range read` to verify `Pivot_RegionRevenue`
6. `mbs excel-worksheet check-error` on the output worksheet

### Recalculate after syncing business data

1. `mbs sheet upsert --verify` or table insert plus sample verification
2. `mbs excel-worksheet calculate` or `mbs workbook calculate`
3. `mbs excel-worksheet range read`
4. `mbs excel-worksheet check-error` when downstream formulas are expected to be stable

If JSON output includes `result.source_info.degraded_success=true`, recalculation completed with available dependencies while skipping stale or missing PG-backed worksheet sources. Inspect `result.source_info.warnings` for `pg_sources[n]`, `gid`, worksheet, and skipped cell details before deciding whether source repair is needed.

### Write formulas into a new report worksheet

1. `mbs excel-worksheet create`
2. Group derived cells into rectangular blocks
3. Use `mbs excel-worksheet range set-formula --operations formulas.json`
4. Prefer `recalculate_mode=workbook` if downstream sheets reference these blocks
5. `mbs excel-worksheet range read`
6. `mbs excel-worksheet check-error`

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

1. `mbs excel-worksheet create`
2. Write the SQL and validate it by calculating the corresponding `=SQL(...)` formula on a disposable target if needed
3. Use `mbs excel-worksheet range set-formula` to write `=SQL("...")`

Raw SQL before converting to the Excel formula string:

```sql
select "Region", sum("Revenue") as "Revenue"
from "Orders"
group by "Region"
order by "Revenue" desc
```

Formula text for `excel-worksheet range set-formula`:

```text
=SQL("select ""Region"", sum(""Revenue"") as ""Revenue"" from ""Orders"" group by ""Region"" order by ""Revenue"" desc")
```

4. If the command succeeds, the formula is saved automatically in the target cell
5. By default, that request also recalculates and materializes the SQL spill result
6. If you pass `--skip-recalculation`, the formula is still saved, but the visible result may remain stale until you call `mbs excel-worksheet calculate` or `mbs workbook calculate`
7. `mbs formula read` can confirm the saved formula text
8. `mbs excel-worksheet range read` can confirm the visible result values
9. `mbs excel-worksheet check-error` can catch `#VALUE!`, `#REF!`, and empty cached formula results across the worksheet

Reference:

- `references/sql-formula-showcase.md`

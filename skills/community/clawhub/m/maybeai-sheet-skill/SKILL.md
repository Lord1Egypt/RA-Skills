---
name: maybeai-sheet
description: "Manages MaybeAI spreadsheets across upload, workbook profiling, read/write, worksheet operations, formulas, formula lineage tracing, formatting, and SQL result-table workflows. Use when working on Excel or spreadsheet tasks in MaybeAI, including file import, large row-count or large cell-count table imports that should route to SheetTable/PG, workbook semantic overview, worksheet inspection, cell or range updates, row or column changes, formula execution, cell dependency tracing, readable report sheets, sharing, or export. Use sheet-dashboard instead for chart-authoring or dashboard-first workflows."
metadata:
  openclaw:
    requires:
      env:
        - MAYBEAI_API_TOKEN
    primaryEnv: MAYBEAI_API_TOKEN
    emoji: "📊"
    homepage: https://github.com/OmniMCP-AI/maybeai-uni
---

# MaybeAI Sheet

Use this skill for MaybeAI spreadsheet lifecycle work: upload or import files, profile workbook contents, inspect worksheets, read and write data, manage worksheets, run formulas, trace formula lineage, build SQL result sheets, apply lightweight formatting, share, and export.

Do not use this skill as the primary workflow for chart authoring or dashboard composition. For dashboard-first work, use `sheet-dashboard`.

## Quick Start

Required environment:

- `MAYBEAI_API_TOKEN`

Common script prerequisites:

- `curl`
- `jq`

Base URL:

```text
https://play-be.omnimcp.ai
```

Authorization header:

```text
Authorization: Bearer <MAYBEAI_API_TOKEN>
```

Ready-to-run examples live in `scripts/`:

```bash
bash scripts/01-file-management.sh
bash scripts/02-read-data.sh
bash scripts/03-write-data.sh
bash scripts/04-rows-columns.sh
bash scripts/05-worksheets.sh
bash scripts/06-formulas.sh
bash scripts/07-charts-pictures.sh
bash scripts/08-formatting.sh
bash scripts/09-end-to-end.sh
bash scripts/10-workbook-profile.sh
bash scripts/11-lineage-trace.sh
```

## When To Use Which Path

| User intent | Recommended path |
|---|---|
| Upload or import Excel files | `references/file-management.md` |
| Understand what a workbook contains before deciding what to read or analyze | `references/workbook-profile.md` |
| Inspect worksheets, read headers, sample data | `references/read-write.md` |
| Replace table data while keeping headers or formulas | `references/read-write.md` |
| Update or append rows by business key | `references/read-write.md` |
| Insert, delete, or move rows and columns; manage worksheets | `references/read-write.md` |
| Write formulas, batch-persist report blocks, recalculate, build SQL result tables, or create live `=SQL(...)` reports | `references/formulas-sql.md` / `references/sql-formula-showcase.md` |
| Explain where a formula cell, computed column, or SQL formula result comes from | `references/lineage-trace.md` |
| Render confirmed Maybe Sheet cells, ranges, or worksheets as clickable references in final answers | `references/clickable-refs.md` |
| Apply lightweight styling, freeze panes, or add autofilter | `references/charts-formatting.md` |
| Troubleshoot auth, wrong-sheet writes, ignored styles, or SQL compile errors | `references/errors-recovery.md` |
| Build chart-heavy pages or dashboards | Switch to `sheet-dashboard`; this skill only covers low-level spreadsheet and chart APIs |

## Core Rules

### 1. Choose the worksheet before you read or write

Do not rely on defaults for non-first worksheets.

- Prefer `worksheet_name` when the endpoint supports it
- Some endpoints require `?gid=<index>` in `uri`
- If you pass neither, many calls will land on the first worksheet, which causes classic “wrote to the wrong sheet” failures

See `references/read-write.md` for details.

### 2. Choose the right engine before importing large files

MaybeAI Sheet routes `/api/v1/excel/*` through Playground, then into either `excelize-mcp` or SheetTable. Engine choice is a Playground routing decision.

- Use SheetTable/PG for table-like workbooks when any worksheet has more than 10,000 rows, the workbook has more than 100,000 populated cells, the data is mostly flat records, or the workflow is SQL-heavy / append-upsert-heavy.
- Use Excelize for workbook-style files where preserving Excel layout, styles, formulas, merged cells, and workbook semantics matters more than table scale.
- For large table-like `.xlsx` uploads, prefer `POST /api/v1/excel/import` with multipart `engine=postgres`; avoid `/api/v1/excel/upload` for those large-data cases.
- After import, verify `list_worksheets` reports `engine: "pg"` or worksheet `data_engine: "pg"`.

See `references/file-management.md` for the exact request.

### 3. Prefer high-level write APIs before raw A1 writes

Priority order:

1. `update_data_keep_headers`
2. `update_range_by_lookup`
3. `append_rows`
4. `update_range`

Meaning:

- Use `update_data_keep_headers` for full-table replacement while preserving headers and column order
- Use `update_range_by_lookup` for key-based updates with automatic append of new rows
- Use `append_rows` for simple object-row appends
- Use `update_range` only when you must target an exact A1 range or non-tabular cells

`update_range` defaults to `RAW`: numeric-looking strings such as `"5.53%"` and `"9,007,000"` remain strings. Use `value_input_option=USER_ENTERED` only when the user intentionally wants Excel-like parsing of formulas, dates, numbers, and percentages. Check the write response `message`: `parse_result=NOT_REQUESTED` means RAW kept strings as text and lists them in `preserved_values`; `parse_result=PASS` means USER_ENTERED parsed values listed in `parsed_values`; `parse_result=PARTIAL` means values listed in `parsed_values` parsed, while `preserved_text_values` may stay text unless target cells are numeric-formatted.

### 4. Separate data writes from style writes

Do not assume `write_new_worksheet`, `update_range`, or `sql/write_result` will automatically apply formatting.

If the user wants a readable report or manager-facing table:

1. Write the data first
2. Call `freeze_panes`
3. Call `batch_set_cell_style`
4. Optionally set column widths, row heights, and autofilter

See `references/charts-formatting.md` for the style playbook.

### 5. Compile SQL before writing a result sheet

Default SQL result-table flow:

1. `read_headers`
2. Optionally `read_sheet` for sampling
3. `sql/compile`
4. `sql/write_result`
5. `read_sheet` to verify the result

Do not skip `sql/compile`.

### 6. Always read back after writing

Do at least one of the following:

- `read_sheet`
- `list_worksheets`
- `read_headers`
- Export the file and inspect it manually

Verification is especially required after:

- SQL result-table writes
- Writes to non-first worksheets
- Overwrite flows that preserve formulas or styles
- Chart, image, or style changes

### 7. Use workbook profile for broad workbook understanding

Use `POST /api/v1/excel/workbook_profile` when the user asks what a workbook contains, which sheets are relevant, or where to start an analysis.

- It returns a cached LLM-generated workbook summary plus worksheet sample rows
- It is read-only and requires viewer access
- Use it before manual `read_sheet` calls for unfamiliar multi-sheet workbooks
- Use `force_refresh: true` after worksheet structure changes or when cached semantics may be stale

See `references/workbook-profile.md` for request and response details.

### 8. Use lineage trace to explain computed cell dependencies

Use `POST /api/v1/excel/lineage/trace` when the user asks where a formula result comes from, why a computed value is wrong, or which source columns feed a target cell.

- It is read-only and requires viewer access
- It traces ordinary Excel formulas, cross-sheet references, column-like formulas, and supported `=SQL(...)` formula outputs
- Prefer `format: "tree"` when explaining to a user
- Prefer `format: "node"` when a UI or downstream tool needs graph nodes and edges

See `references/lineage-trace.md` for request and response details.

### 9. Use clickable references only for confirmed workbook locations

When the final answer references real cells, ranges, or worksheets from the current Maybe Sheet workbook, follow `references/clickable-refs.md` so the frontend can make those references clickable.

- Use clickable references only for confirmed current-workbook locations
- Include the current workbook document ID in the `docId` attribute
- Include the target worksheet gid in the `gid` attribute
- Do not use clickable references for examples, guesses, inferred locations, or uncertain references
- When referencing workbook cells, ranges, or table names, always use `<sheet-ref kind="..." docId="..." gid="..." sheet="..." range="...">...</sheet-ref>` tags. Do not use conversational location descriptions such as "above", "the cell above", "D column row fourteen", or "D 列第十四行".
- Always use paired `sheet-ref` tags with visible text, never self-closing tags. Use `<sheet-ref kind="cell" docId="DOCUMENT_ID" gid="WORKSHEET_GID" sheet="Sheet1" range="A1">Sheet1!A1</sheet-ref>`, not `<sheet-ref .../>`.
- Do not place clickable references inside code blocks, formulas, SQL, JSON, or shell examples

### 10. Use the share API family for visibility changes

When the user asks to make a Maybe Sheet public or private, use:

- `POST /api/v1/share/sheet/visibility`

Do not use:

- `/api/v1/excel/spreadsheets/d/{id}/share`

That spreadsheet-path share route is the wrong endpoint for MaybeAI Sheet visibility changes and returns 404. Use the `share/sheet/*` API family for visibility, permission updates, access removal, and share listing.

## Agent-Safe Playbooks

### Upload and inspect a file

1. Upload or import the file
2. Capture `document_id` and `uri`
3. `list_worksheets`
4. `read_headers`
5. Optionally `read_sheet` for a small sample

References:

- `references/file-management.md`
- `references/read-write.md`
- `scripts/01-file-management.sh`
- `scripts/02-read-data.sh`

### Profile a workbook before analysis

1. Capture `document_id` or `uri`
2. Call `workbook_profile`
3. Use `profile.summary` to explain the workbook at a high level
4. Use `profile.worksheets[].sample_rows` to choose targeted `read_headers` or `read_sheet` calls
5. If the workbook changed materially, call again with `force_refresh: true`

References:

- `references/workbook-profile.md`
- `scripts/10-workbook-profile.sh`

### Refresh a table while keeping headers and formulas

1. Identify the target worksheet
2. Use `update_data_keep_headers`
3. If the sheet has computed columns, set `preserve_formulas: true`
4. `read_sheet` to verify

References:

- `references/read-write.md`
- `scripts/03-write-data.sh`

### Sync business records by key

1. Identify the key column, such as `Order ID` or `SKU`
2. Use `update_range_by_lookup`
3. If you need workbook-wide downstream recalculation, call `recalculate_formulas`
4. `read_sheet` to verify

References:

- `references/read-write.md`
- `references/formulas-sql.md`

### Build an SQL result sheet

1. Identify the worksheet name or gid
2. `read_headers`
3. Write PostgreSQL-compatible worksheet SQL
4. `sql/compile`
5. `sql/write_result`
6. `read_sheet` to verify the output

References:

- `references/formulas-sql.md`
- `scripts/06-formulas.sh`

### Persist many report formulas efficiently

1. Scaffold the destination worksheet first
2. Group derived cells into rectangular blocks
3. Use `formula/batch_set` for those blocks
4. Prefer `recalculate_mode=workbook` when later blocks depend on earlier blocks
5. Use `formula/set` only for sparse one-off fixes
6. `read_sheet` to verify representative cells

References:

- `references/formulas-sql.md`
- `scripts/06-formulas.sh`

### Trace formula lineage for a cell

1. Capture `document_id` or `uri`
2. Identify the target worksheet by `worksheet_name` or `gid`
3. Call `lineage/trace` with the exact A1 target cell
4. Use `tree` output to explain the dependency chain, or `node` output to render a graph
5. If lineage is incomplete, read the referenced sheets and headers to verify unsupported or unresolved references

References:

- `references/lineage-trace.md`
- `scripts/11-lineage-trace.sh`

### Produce a readable report worksheet

1. Create the table with `write_new_worksheet` or a data-write API
2. `freeze_panes`
3. `batch_set_cell_style`
4. Optionally set widths, heights, and autofilter
5. If the response includes `source_info.styles_ignored=true`, explicitly tell the user the engine did not apply styles

References:

- `references/charts-formatting.md`
- `references/errors-recovery.md`
- `scripts/08-formatting.sh`

## Reference Map

- `references/file-management.md`
  Best for upload, import, search, copy, sharing, export, and file-entry issues.
- `references/workbook-profile.md`
  Best for workbook semantic overview, sheet discovery before analysis, cached profile behavior, and `workbook_profile` request/response details.
- `references/read-write.md`
  Best for reading sheets, worksheet targeting, choosing the right write API, row and column operations, and worksheet management.
- `references/formulas-sql.md`
  Best for formulas, recalculation, SQL compile, and SQL result tables.
- `references/sql-formula-showcase.md`
  Best when you need a single live `=SQL(...)` formula that demonstrates joins, aggregation, Top N, and spill behavior.
- `references/lineage-trace.md`
  Best for tracing a target cell's formula dependencies, explaining source columns behind computed values, or producing lineage graph nodes and edges.
- `references/charts-formatting.md`
  Best for low-level chart APIs, pictures, freezing panes, styles, autofilter, and conditional formatting.
- `references/errors-recovery.md`
  Best for troubleshooting, limitations, and recovery paths.

## What This Skill Intentionally Excludes

- It does not handle full dashboard composition, chart layout strategy, or infographic design; use `sheet-dashboard` for those.
- It does not turn the main `SKILL.md` into a full API manual; long request bodies and examples belong in `references/` and `scripts/`.
- It does not default to large visual redesign or chart rearrangement unless the user explicitly asks for that.

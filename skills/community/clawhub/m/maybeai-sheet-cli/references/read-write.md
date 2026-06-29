# Read/Write Reference

## Contents

1. When to use this
2. Worksheet targeting rules
3. Read endpoints
4. How to choose a write API
5. Row and column operations
6. Worksheet management
7. Post-write verification

## 1. When to use this

Read this document when the task involves reading sheets, sampling data, reading headers, updating cells, replacing full tables, updating by key, appending rows, inserting or deleting rows and columns, or creating and renaming worksheets.

## 2. Worksheet targeting rules

This is the most important operational rule.

Default workflow:

1. `workbook manifest`
2. choose `worksheet_name` or `gid`
3. call `read_sheet`, `read_headers`, or a write API

- Prefer `worksheet_name`
- Some endpoints only respect `uri?gid=<index>`
- If you pass neither, the backend often defaults to the first worksheet

Typical rules:

- `read_sheet` / `update_range` / `clear_range` / `update_data_keep_headers`
  Prefer `worksheet_name`
- `read_headers` / `append_rows` / `update_range_by_lookup`
  Commonly use `uri?gid=<index>`

If the user says “update the second sheet” or “append to Summary”, identify the sheet first, then execute the write.

## 3. Read endpoints

### CLI (preferred)

```bash
# Full sheet with headers + rows (human-friendly)
maybeai-sheet sheet read --doc-id <DOC_ID> --gid <GID> --output table

# Full sheet (JSON for parsing)
maybeai-sheet sheet read --doc-id <DOC_ID> --worksheet-name <SHEET>

# Specific range
maybeai-sheet sheet read-range --doc-id <DOC_ID> --gid <GID> --range A1:G20 --output table

# Headers only
maybeai-sheet sheet headers --doc-id <DOC_ID> --gid <GID> --output table

# Worksheet list
maybeai-sheet sheet worksheets --doc-id <DOC_ID> --output table

# Workbook manifest / capabilities
maybeai-sheet workbook manifest --doc-id <DOC_ID>
maybeai-sheet workbook capabilities --doc-id <DOC_ID>
```

Targeting flags (`--doc-id`, `--url`, `--uri`, `--gid`, `--worksheet-name`) and output flags (`--output`, `--verbose`, `--timeout`) work at the root, on `sheet` / `workbook`, or on the leaf command. You must always pass a leaf subcommand such as `read`, `headers`, or `worksheets`.

With `--output table`, read responses render as an aligned column grid from `result.data` or `result.values` + `headers`. Metadata such as `styles`, `fonts`, and `formulas` is omitted from the table view.

### Read workbook manifest first

```text
POST /api/v3/excel/workbook/manifest
POST /api/v3/excel/worksheet/list
```

Use these to:

- inspect worksheet names and gid values
- confirm engine capabilities before choosing a write path
- avoid guessing the target sheet

### Read a full sheet or a range

```text
POST /api/v3/excel/range/read
POST /api/v3/excel/range/read_many
POST /api/v3/excel/table/read
POST /api/v3/excel/named_range/read
```

Common parameters:

- `worksheet_name`
- `range_address`
- `value_render_option`
- `filter_tokens`
- `auto_filter`

Use it to:

- inspect data
- sample and verify
- read chart or formatting metadata

Use `range/read_many` when:

- you need several disjoint ranges from one workbook
- you want one manifest-derived context and one aggregated response
- you want to reduce repeated chat turns

Use `table/read` when:

- the target is conceptually a rectangular report block or table region
- you want the response to stay in the table domain rather than a generic range read

Use `named_range/read` when:

- the workbook already exposes a stable business name for the target block
- you want to avoid leaking worksheet coordinates into the prompt
- you are reading a finance or reporting region that should survive layout shifts

### Read headers

```text
POST /api/v3/excel/table/headers
```

Use it to:

- get the schema quickly
- confirm column names before writing SQL

### List worksheets and versions

```text
POST /api/v3/excel/workbook/versions
POST /api/v1/excel/read_version
POST /api/v1/excel/list_worksheets_version
```

## 4. How to choose a write API

### `update_data_keep_headers`

Best when:

- headers are already correct
- you need to replace the entire data region
- you want to preserve column order
- you want to preserve formula columns

Advantages:

- input can be list-of-dict
- safer for agents

### `update_range_by_lookup`

Best when:

- syncing business records by key
- updating existing rows
- appending missing rows automatically

Common keys:

- `Order ID`
- `SKU`
- `ID`

### `append_rows`

Best when:

- you want a blind append of object rows
- the target sheet and headers are already known

### `update_range`

Best when:

- you need to update an exact A1 range
- the target is non-tabular
- you are making a small manual cell edit

### `clear_range`

Best when:

- you need to clear a specific range
- you want a local reset before a write

## 5. Row and column operations

Related endpoints:

```text
POST /api/v3/excel/worksheet/rows/insert
POST /api/v3/excel/worksheet/rows/delete
POST /api/v3/excel/worksheet/rows/move
POST /api/v1/excel/move_row
POST /api/v1/excel/undo_delete_rows
POST /api/v3/excel/worksheet/columns/insert
POST /api/v3/excel/worksheet/columns/delete
POST /api/v3/excel/worksheet/columns/move
POST /api/v1/excel/move_column
POST /api/v1/excel/undo_delete_columns
POST /api/v1/excel/add_header_columns
POST /api/v1/excel/set_columns_width
POST /api/v1/excel/set_rows_height
```

Notes:

- row numbers are 1-based
- columns typically use Excel letters such as `A` and `B`

## 6. Worksheet management

Related endpoints:

```text
POST /api/v3/excel/worksheet/create
POST /api/v3/excel/worksheet/delete
POST /api/v3/excel/worksheet/rename
POST /api/v3/excel/worksheet/move
POST /api/v3/excel/worksheet/copy
POST /api/v3/excel/workbook/copy
```

Guidance:

- When creating a new report sheet, write data first and style it separately
- Before deleting a worksheet, confirm the `gid` or sheet name to avoid deleting the wrong sheet

## 7. Post-write verification

Do at least one of the following:

- `read_sheet`
- `read_headers`
- `list_worksheets`
- `range/read_many`

Strongly recommended after:

- `sheet upsert` / `sheet append` / `sheet write-range`
- writes to non-first worksheets
- `raw post` SQL or formatting operations

See `references/cli-commands.md` for verification commands.

## 8. Workbook-scope batch

Use this when one workbook task naturally contains several ordered operations:

```text
POST /api/v3/excel/batch
```

Good fits:

- read several ranges, then write one summary range
- clear a staging block, append rows, then recalculate formulas
- create a worksheet and then write its starter block

Current behavior:

- the backend executes supported v3 operations sequentially
- this is not a cross-engine transaction
- prefer `continue_on_error=false` unless the workflow explicitly tolerates partial progress

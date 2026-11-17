# Read/Write Reference

## Contents

1. When to use this
2. Worksheet targeting rules
3. Read commands
4. How to choose a write API
5. Row and column operations
6. Worksheet management
7. Post-write verification

## 1. When to use this

Read this document when the task involves reading sheets, sampling data, reading headers, updating cells, replacing full tables, updating by key, appending rows, inserting or deleting rows and columns, or creating and renaming worksheets.

## 2. Worksheet targeting rules

This is the most important operational rule.

Default workflow:

1. `mbs workbook metadata` or `mbs workbook list-worksheets`
2. choose `worksheet_name`, `table_id`, `db-table --name`, or `gid`
3. call `range`, `excel-table`, `db-table`, or `worksheet` command

- Prefer `worksheet_name` for current object commands
- Use `gid` mainly for legacy `sheet` aliases and gid-only backend routes
- If you pass neither, the backend often defaults to the first worksheet

Typical rules:

- `excel-worksheet read`, `excel-worksheet range write/clear/search`, `excel-worksheet` lifecycle, `formula`, and `style`: prefer `--worksheet-name`
- `excel-table`: use `--worksheet-name` plus `--table-id`
- `db-table`: use `--name` or `--backend-id`
- `sheet update-data-keep-headers` and legacy `sheet append/upsert/headers`: commonly use `--gid`

If the user says “update the second sheet” or “append to Summary”, identify the sheet first, then execute the write.

## 3. Read commands

### CLI (preferred)

```bash
# Full sheet with headers + rows (human-friendly)
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name <SHEET> --output table

# Specific range
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:G20 --output table

# Scan a worksheet for formula-style errors from worksheet readback
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name <SHEET>

# Worksheet-backed table
mbs excel-table sample --doc-id <DOC_ID> --worksheet-name Orders --table-id 1 --limit 50

# PG/SheetTable-backed table
mbs db-table sample --doc-id <DOC_ID> --name orders_large --limit 50

# Workbook worksheet list
mbs workbook list-worksheets --doc-id <DOC_ID> --output table

# Workbook metadata / capabilities
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook capabilities --doc-id <DOC_ID>
```

Targeting flags (`--doc-id`, `--url`, `--uri`, `--gid`, `--worksheet-name`) and output flags (`--output`, `--verbose`, `--timeout`) work at the root, on many groups, or on the leaf command. You must always pass a leaf subcommand such as `read`, `metadata`, `sample`, or `list`.

With `--output table`, read responses render as an aligned column grid from `result.data` or `result.values` + `headers`. Metadata such as `styles`, `fonts`, and `formulas` is omitted from the table view.
`excel-worksheet check-error` is the readback-oriented verification companion for
formula or SQL result worksheets: it reports formula-style error values and
warns when formula cells have no cached/display result yet. Use worksheet-wide
checks by default; add `--range` only when narrowing down one block.

### Read workbook metadata first

```bash
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook list-worksheets --doc-id <DOC_ID>
```

Use these to:

- inspect worksheet names and gid values
- confirm engine capabilities before choosing a write path
- avoid guessing the target sheet

### Read a full sheet, range, or table

Use the CLI commands above to:

- inspect data
- sample and verify
- read chart or formatting metadata

Prefer `excel-table schema` or `db-table schema` when you need headers before SQL or row-object writes.

Use named ranges only when a current first-class command exposes them and the workbook already has a stable business name for the target block.

### List worksheets and versions

Use `mbs workbook list-worksheets`, `mbs history list`, and `mbs history read`.

## 4. How to choose a write API

### `sheet update-data-keep-headers`

The preferred unified CLI entry point is:

```bash
mbs worksheet import ./rows.json --strategy replace --doc-id <DOC_ID> --worksheet-name Students --verify
```

It routes to the same `update_data_keep_headers` backend behavior documented
below. Keep the `sheet update-data-keep-headers` form only for compatibility.

Best when:

- row 1 already contains the canonical worksheet headers
- all data rows from `start_row` onward should be replaced, not appended or merged
- existing header order and cell styles must remain in place
- formula columns omitted from the input should be filled from the row 2 formula template

Input must be a non-empty JSON array of objects. Every object key must exactly
match an existing header; matching is case-sensitive. The CLI calls
`/api/v1/excel/read_headers` before mutation and rejects unknown keys, empty
arrays, empty objects, mixed item types, and `start_row < 2`.

```json
[
  {"Name": "Alice", "Score": 88},
  {"Name": "Bob", "Score": 92}
]
```

Run a preflight before the real write:

```bash
mbs sheet update-data-keep-headers \
  --doc-id <DOC_ID> \
  --worksheet-name Students \
  --data students.json \
  --dry-run

mbs sheet update-data-keep-headers \
  --doc-id <DOC_ID> \
  --worksheet-name Students \
  --data students.json \
  --verify
```

Defaults are intentionally safe:

- `--start-row 2`: row 1 is never replaced
- `--preserve-formulas`: columns omitted from the first input object can reuse a row 2 formula template
- recalculation enabled: the backend rebuilds the workbook calculation chain
- `--verify`: opt-in bounded readback from row 1 through one row after the new dataset

Use `--no-preserve-formulas` only when input JSON should own formula columns.
Use `--skip-recalculation` only when a later explicit calculate step is planned.
`--dry-run` and `--verify` are mutually exclusive.

Replacement semantics matter: the backend clears existing values from
`start_row` through the previous last row before writing the new objects. A
shorter input therefore clears stale trailing rows. Missing known keys and
`null` leave cells blank. Unknown keys never reach the update endpoint because
the CLI rejects them after header preflight.

Numeric-looking strings follow this backend's USER_ENTERED-style parsing. A
value such as `"46215.95520833333"` can read back as `"46215.95521"`. Use
`excel-worksheet range write` for exact RAW text preservation instead of this
full-refresh command.

### `excel-table insert` / `db-table insert`

Best when:

- appending row objects to a known worksheet-backed table or PG table
- the target table metadata is already known
- you can verify with `excel-table sample` or `db-table sample`

### `db-table create`

Best when:

- creating a new PG/SheetTable-backed logical table inside an existing workbook
- you have row-object JSON data and want the backend to materialize it as a DB table
- the table should be addressed later by `mbs db-table ... --name <TABLE_NAME>`

CLI:

```bash
mbs db-table create --doc-id <DOC_ID> --name Orders --rows orders.json
mbs db-table create --doc-id <DOC_ID> --name Orders --columns columns.json --rows rows.json --if-exists adopt --verify
mbs db-table metadata --doc-id <DOC_ID> --name Orders
mbs db-table metadata --doc-id <DOC_ID> --name Orders --include-headers --output json
mbs db-table sample --doc-id <DOC_ID> --name Orders --limit 20 --output table
```

Use `db-table metadata --include-headers` when the next step needs exact header
text. The command is still a single-table lookup and requires `--name` or
`--backend-id`; use `workbook list-worksheets` first if the table name is
unknown.

`orders.json` must contain a JSON array of row objects. The CLI infers column
names and simple logical types (`text`, `number`, `boolean`) from the rows.
Pass `--columns columns.json` to provide an explicit schema, especially when
`rows.json` is empty or when the column order and logical types must be stable.
Use `--if-exists adopt` or `--adopt-existing` only for idempotent setup flows
where a matching PG table may already exist; pair it with `--verify` so the CLI
confirms the registry adopted a PG-backed worksheet. Use `db-table create` only
for table-shaped data; use `excel-worksheet create` or `excel-worksheet range
write` for workbook-layout reports. `db-table update` and `db-table delete` are
currently planned stubs, not supported mutation commands.

### `db-table field metadata` / `field batch-update`

Use these commands when the user wants PG/SheetTable column display metadata,
not row data mutation:

- formatter such as `$#,##0.00`, `0.00%`, `yyyy-mm-dd`
- data-cell text color or background color
- column width
- beautified header style metadata

```bash
mbs db-table field metadata --doc-id <DOC_ID> --name Orders --output json
mbs db-table field batch-update --doc-id <DOC_ID> --name Orders --updates field-updates.json --verify --output json
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name Orders --range A1:Z3 --output json
```

`field-updates.json` must be a JSON array. Prefer one batch update over many
single-column calls. After updating, confirm persisted state from
`excel-worksheet read` fields such as `formatting.frozen_rows`,
`formatting.auto_filter`, and `db_table.fields[*].property`.

### `db-table create-from-range`

Best when:

- a source worksheet lives in one document and the target PG/SheetTable raw
  surface must land in another document
- you need a raw `R_*` surface from a bounded worksheet range without writing
  per-run Python import drivers
- merged-title sheets need a semantic header row inside the readback matrix

CLI:

```bash
mbs db-table create-from-range \
  --doc-id <TARGET_DOC_ID> \
  --name R_OrderLines_Store1 \
  --source-doc-id <SOURCE_DOC_ID> \
  --worksheet-name "1店" \
  --range A2:AR423 \
  --header-row 0 \
  --use-header-names \
  --if-exists adopt \
  --verify \
  --output json

mbs db-table schema --doc-id <TARGET_DOC_ID> --name R_OrderLines_Store1
mbs db-table sample --doc-id <TARGET_DOC_ID> --name R_OrderLines_Store1 --limit 20 --output table
```

The command is CLI-composed: it reads the source range through
`/api/v1/excel/read_sheet`, reshapes the values matrix, then creates the named
PG table on the target workbook through `/api/v1/excel/db_table/create`.
`--header-row` is a 0-based index inside the returned `values` matrix, not an
Excel row number. For Shein-style merged titles, start `--range` at the
semantic header row (`A2:...`) and keep `--header-row 0`. Use
`--use-header-names` for semantic column names (blank header cells become
`col_NNN`); omit it for positional `raw_col_NNN` columns. Entirely blank rows
are dropped. JSON output includes source doc/sheet/range plus row/column
counts in `context`.

### `db-table create-from-query`

Best when:

- a SQL template should materialize a reusable PG/SheetTable handoff table
- the source tables already exist in MaybeSheet
- the output should be addressed later by `mbs db-table ... --name <TABLE_NAME>`
- an ETL skill needs an auditable `--sql-file` command instead of Python-side planning

CLI:

```bash
mbs db-table create-from-query \
  --doc-id <DOC_ID> \
  --worksheet-name B_FxSettlement \
  --name S1_RevenueStructureInput \
  --sql-file s1_revenue_structure_input.sql \
  --if-exists adopt \
  --verify

mbs db-table schema --doc-id <DOC_ID> --name S1_RevenueStructureInput
mbs db-table sample --doc-id <DOC_ID> --name S1_RevenueStructureInput --limit 20 --output table
mbs db-table read --doc-id <DOC_ID> --name S1_RevenueStructureInput --limit 100 --output table
```

The command is CLI-composed. It sends the SQL as a `=SQL(...)` calculation to
`/api/v1/excel/calc-formula`, reads the table-shaped result from `values` or
`range_values`, then creates the named PG table through
`/api/v1/excel/db_table/create`. After create, current CLI versions try to
write the same `=SQL(...)` formula into the final table cell, defaulting to
`A1`, and return `context.formula_trace` in JSON output. Treat
`formula_trace.persisted=true` as evidence that the formula was kept in the
created table. If it is `failed` or `skipped`, the table may still be valid,
but you must report that formula-cell traceability was not preserved and include
the recorded reason. Use `--no-preserve-formula` only for workflows that
explicitly do not want the extra formula write. If the hosted `calc-formula`
route cannot resolve source columns, do not work around it by hand-writing JSON
rows unless the user explicitly changes the workflow; fix or redeploy the
backend route.

### Formula writes through range commands

Use these when the workflow is already operating on the object-specific range
surface:

```bash
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name <SHEET> --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --operations formulas.json --recalculate-mode worksheet
mbs db-table range set-formula --doc-id <DOC_ID> --name Orders --cell G2 --formula '=SQL("select * from Orders limit 10")'
```

Use `excel-worksheet range set-formula` for worksheet formula writes and
`db-table range set-formula` for PG/SheetTable-backed formula writes. Use
`formula read`, `formula batch-set`, and `formula lineage` when working from the
formula-focused playbook.

### Legacy `sheet upsert`

Best when:

- syncing business records by key
- updating existing rows
- appending missing rows automatically
- you have confirmed the gid and key column

Common keys include `Order ID`, `SKU`, and `ID`.

### `update_range`

Best when:

- you need to update an exact A1 range
- the target is non-tabular
- you are making a small manual cell edit

CLI:

```bash
mbs excel-worksheet range write --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:C3 --values values.json --verify
mbs excel-worksheet range clear --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:C3
```

Value handling:

- `excel-worksheet range write` defaults to `RAW`; numeric-looking strings such as `"5.53%"` and `"9,007,000"` stay strings.
- Use `value_input_option=USER_ENTERED` only when you want Excel-like parsing of formulas, dates, numbers, and percentages.
- Read the response `message` after writes:
  - `parse_result=NOT_REQUESTED` means `RAW` kept numeric-looking strings as text; inspect `preserved_values`.
  - `parse_result=PASS` means `USER_ENTERED` parsed the submitted numeric-looking strings; inspect `parsed_values`.
  - `parse_result=PARTIAL` means values in `parsed_values` parsed, while values in `preserved_text_values` may stay text unless the target cells are numeric-formatted.

### `clear_range`

Best when:

- you need to clear a specific range
- you want a local reset before a write

## 5. Row and column operations

CLI:

```bash
mbs row insert --doc-id <DOC_ID> --worksheet-name <SHEET> --row 10 --count 2
mbs row delete --doc-id <DOC_ID> --worksheet-name <SHEET> --row 10 --count 2 --yes
mbs row move --doc-id <DOC_ID> --worksheet-name <SHEET> --row 10 --count 2 --destination-row 20

mbs column insert --doc-id <DOC_ID> --worksheet-name <SHEET> --column B --count 2
mbs column delete --doc-id <DOC_ID> --worksheet-name <SHEET> --column B --count 2 --yes
mbs column move --doc-id <DOC_ID> --worksheet-name <SHEET> --column B --count 2 --destination-column D
mbs column width --doc-id <DOC_ID> --worksheet-name <SHEET> --start-column B --end-column D --width 120
```

Notes:

- row numbers are 1-based
- columns typically use Excel letters such as `A` and `B`

## 6. Worksheet management

CLI:

```bash
mbs excel-worksheet create --doc-id <DOC_ID> --name Summary --values values.json
mbs excel-worksheet rename --doc-id <DOC_ID> --worksheet-name Old --new-name New
mbs excel-worksheet delete --doc-id <DOC_ID> --worksheet-name Temp --dry-run
mbs excel-worksheet delete --doc-id <DOC_ID> --worksheet-name Temp --yes
mbs excel-worksheet copy --doc-id <DOC_ID> --worksheet-name Sheet1 --new-name Copy
mbs excel-worksheet move --doc-id <DOC_ID> --worksheet-name Summary --index 0
```

Guidance:

- When creating a new report sheet, write data first and style it separately
- Before deleting a worksheet, confirm the `gid` or sheet name to avoid deleting the wrong sheet
- The `excel-worksheet copy` CLI command remains a same-document command.
  For cross-document native copy, use `mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name <SHEET>`;
  it routes the cross-document `/api/v1/excel/copy_worksheet` contract and
  preserves the source worksheet engine. Use the default values mode or
  `db-table create-from-range` when the target should instead be a raw PG
  `R_*` surface.

## 7. Post-write verification

Do at least one of the following:

- a targeted read
- `mbs excel-worksheet check-error` on formula/result worksheets
- a schema/header command
- workbook list-worksheets
- `mbs excel-worksheet range read --output table`
- `mbs excel-table sample`
- `mbs db-table sample`
- `mbs workbook list-worksheets`

Strongly recommended after:

- `excel-worksheet range write`, `excel-table insert`, `db-table create`, `db-table insert`, or legacy `sheet upsert`
- writes to non-first worksheets
- formula, chart, image, dashboard, or style operations
- formula writes, recalculation, or SQL spill/report worksheets that should be free of `#VALUE!`, `#REF!`, and similar worksheet errors

See `references/cli-commands.md` for verification commands.

## 8. Workbook-scope batches

Do not assume batch behavior from this skill. Prefer explicit ordered `mbs`
commands unless a first-class batch command is documented in current `mbs --help`.

# CLI Command Reference

Use this as the primary execution catalog. Use first-class `mbs` commands.

Install: `pip install maybeai-sheet-cli`

Required env: `MAYBEAI_API_TOKEN`

## Shared Options

These flags work at the root, on most command groups, or on the leaf command:

| Flag | Purpose |
|------|---------|
| `--token` | API token; defaults to `MAYBEAI_API_TOKEN` |
| `--base-url` | API base; default `https://a-play-be.maybeai.cn`; env var `MAYBEAI_BASE_URL` |
| `--doc-id` | Workbook document ID |
| `--url` | MaybeAI workbook URL; parses doc id and gid when possible |
| `--uri` | Fully resolved workbook URI |
| `--gid` | Worksheet gid |
| `--worksheet-name` | Worksheet name |
| `--output` | `json` default, `table`, or `yaml` |
| `--verbose` | Include extra command metadata |
| `--timeout` | HTTP timeout seconds |

Always pass a leaf subcommand. `mbs workbook --doc-id <id>` alone is invalid.

## Workbook And Files

```bash
mbs workbook create --title "Board Pack"
mbs workbook create --title "Board Pack" --sheet-name Summary --data rows.json

# Default Excelize/workbook-fidelity import. No engine field is sent.
mbs workbook import ./report.xlsx
mbs workbook create-from-file ./report.xlsx

# Backend-selected per-worksheet engines for mixed workbooks.
mbs workbook import ./mixed-workbook.xlsx --engine auto

# Explicit per-worksheet engines by worksheet index.
mbs workbook import ./mixed-workbook.xlsx --engine "postgres,excel,excel,postgres"

# SheetTable/PG import for large flat table-like files.
mbs workbook import ./large-table.xlsx --engine postgres
mbs workbook create-from-file ./large-table.xlsx --engine pg

# Remote HTTPS Excel URL into a new workbook via /api/v1/excel/import_by_url.
mbs workbook import "https://static.example.com/imports/report.xlsx" --engine auto
mbs workbook import "https://static.example.com/download?id=123" --source-type xlsx --filename report.xlsx --engine excelize

# CSV/TSV/Google Sheet import-source flow into a new workbook.
mbs workbook import ./orders.csv --engine postgres
mbs workbook import ./orders.tsv --engine excelize
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --engine postgres
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --source-worksheet-name "1店" --worksheet-name "Store 1" --engine excelize
mbs workbook import ./orders.csv --preview-only --output json

# Import source worksheets/tabs into an existing workbook.
# Omit --source-worksheet-name to import all previewed worksheets/tabs.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --engine postgres
mbs worksheet import --strategy create ./orders.csv --doc-id <TARGET_DOC_ID> --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --engine excelize

# Pass one --source-worksheet-name to import one source worksheet/tab, optionally renamed.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine postgres
mbs worksheet import --strategy create ./orders.csv --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --target-worksheet-name Orders --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --target-worksheet-name "Store 1" --engine excelize

# Repeat --source-worksheet-name to import multiple selected source worksheets/tabs.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --source-worksheet-name "订单" --engine postgres
mbs worksheet import --strategy create ./orders.tsv --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --source-worksheet-name refunds --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --engine excelize

# Cross-workbook worksheet -> raw PG/db-table surface import.
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --verify
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --verify

# Native cross-workbook import. Do not pass --engine; source metadata selects it.
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "工作表3" --source-worksheet-name "工作簿1" --verify
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --verify

# Replace data rows in one existing worksheet from a JSON object array.
mbs worksheet import ./rows.json --strategy replace --doc-id <TARGET_DOC_ID> --worksheet-name Students --verify

mbs workbook metadata --doc-id <DOC_ID>
mbs workbook manifest --doc-id <DOC_ID>        # compatibility alias
mbs workbook capabilities --doc-id <DOC_ID>
mbs workbook list-user-workbooks --limit 20
mbs workbook list-worksheets --doc-id <DOC_ID>
mbs workbook list --limit 20
mbs workbook search --query "q2 forecast" --limit 20
mbs workbook --doc-id <DOC_ID> copy --title "Copy of Workbook"

mbs file export --doc-id <DOC_ID> --out workbook.xlsx
mbs file list --limit 20
mbs file search --query "q2 forecast" --limit 20
```

Accepted import engine values are omitted/`excelize` for the default Excelize
route, `pg`/`postgres`/`postgresql` for SheetTable, `auto` for backend
per-worksheet detection, or a comma-separated per-worksheet list such as
`postgres,excel,excel,postgres`. `auto` and comma-separated engines apply to
whole local Excel workbook imports. Remote Excel URL imports accept one of
`excelize`, `postgres`, or `auto`; comma-separated engines are rejected. Local Excel worksheet append into an
existing workbook supports `excelize` or `postgres`/`pg`. CSV/TSV/Google Sheet
import-source selections support `excelize`, `postgres`/`pg`, or `auto`.
SheetTable owns DB-import preprocessing; the CLI only forwards the requested
engine intent.

Import routing:

- `.xls` / `.xlsx` / `.xlsm` without a target workbook: `/api/v1/excel/import`.
- Remote HTTPS `.xls` / `.xlsx` / `.xlsm` URL without a target workbook: `/api/v1/excel/import_by_url`. `--filename` is optional; the CLI uses the explicit value, then the decoded URL path basename, then `upload.xlsx`. For a download URL without an Excel suffix, pass `--source-type xlsx`. This mode rejects target workbook flags, worksheet selection flags, `--preview-only`, and comma-separated engines.
- `worksheet import` for `.xls` / `.xlsx` / `.xlsm` with `--doc-id` / `--url` / `--uri`: `/api/v1/excel/import_worksheet_preview` then `/api/v1/excel/import_worksheet_data`. Omit `--source-worksheet-name` to import all previewed worksheets, or repeat it to select worksheets.
- `.csv` / `.tsv` / public Google Sheet URL without a target workbook: `/api/v1/excel/import_sources/preview` then commit with `target.mode = new_workbook`. With no explicit selection, the backend imports all previewed worksheets/tabs.
- `.csv` / `.tsv` / public Google Sheet URL with `--doc-id` / `--url` / `--uri`: same preview route then commit with `target.mode = existing_workbook`; the CLI sends non-empty `selections`. Omit `--worksheet-name` to select all previewed worksheets/tabs, or repeat `--worksheet-name` to select specific worksheet/tab names. Missing requested names fail before commit and return the available worksheet names.
- No local/URL source plus `--source-doc-id` / `--source-url` and `--transfer-mode values`: CLI-composed cross-workbook raw PG/db-table surface import.
- No local/URL source plus `--source-doc-id` / `--source-url` and `--transfer-mode native`: metadata-driven native worksheet import. Do not pass `--engine`.
- Both Maybe Sheet source modes accept repeated `--source-worksheet-name`; omitting it selects all metadata worksheets.

For existing-workbook imports, `--target-worksheet-name` is only valid when
exactly one source worksheet/tab is selected.

For JSON replace, `--worksheet-name` identifies the existing target worksheet.
The command keeps row 1 and calls `/api/v1/excel/update_data_keep_headers`.
The JSON file must be a non-empty object array with keys matching existing
headers. Do not pass `--engine`, `--transfer-mode`, or source worksheet options.

For import-source existing-workbook commits that return exactly one worksheet,
the CLI top-level `target` should include `gid` and `worksheet_name` from
`result.worksheets[0]`. For multi-worksheet commits, treat top-level `target`
as workbook-level and inspect `result.worksheets`.

For cross-workbook raw-surface imports, successful `worksheet import` stdout plus
`--verify` is the creation evidence; do not follow it with per-table
`db-table schema`, `db-table sample`, or `db-table read` loops. If shape
confirmation is needed, do at most one representative `mbs db-table sample --limit 2`
per family.

## Inspect And Target

```bash
mbs workbook list-worksheets --doc-id <DOC_ID> --output table
mbs excel-worksheet metadata --doc-id <DOC_ID> --worksheet-name Sheet1
mbs excel-worksheet list-table --doc-id <DOC_ID> --output json
mbs excel-worksheet list-table --doc-id <DOC_ID> --gid <GID> --output json
```

Prefer `workbook metadata` or `workbook list-worksheets` before writes on unfamiliar
workbooks. Use `--worksheet-name` for worksheet/range/formula work, `--table-id`
for `excel-table`, and `--name` or `--backend-id` for `db-table`.
Use `excel-worksheet list-table --gid <GID>` to detect multiple content-backed
tables inside a visual Excel worksheet.

## Ranges And Worksheets

```bash
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name Sheet1 --output table
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:D20 --output table
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name Model
mbs excel-worksheet range write --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:C3 --values values.json --verify
mbs excel-worksheet range clear --doc-id <DOC_ID> --worksheet-name Sheet1 --range D1:F10
mbs excel-worksheet range search --doc-id <DOC_ID> --worksheet-name Sheet1 --query revenue --max-results 20
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name Sheet1 --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --operations formulas.json --recalculate-mode worksheet

mbs excel-worksheet create --doc-id <DOC_ID> --name Summary --values values.json
mbs excel-worksheet rename --doc-id <DOC_ID> --worksheet-name Old --new-name New
mbs excel-worksheet delete --doc-id <DOC_ID> --worksheet-name Temp --dry-run
mbs excel-worksheet delete --doc-id <DOC_ID> --worksheet-name Temp --yes
mbs excel-worksheet copy --doc-id <DOC_ID> --worksheet-name Sheet1 --new-name Copy
mbs excel-worksheet copy --doc-id <SOURCE_DOC_ID> --worksheet-name Sheet1 --target-doc-id <TARGET_DOC_ID> --new-name Copy  # fails fast; use db-table create-from-range
mbs excel-worksheet move --doc-id <DOC_ID> --worksheet-name Summary --index 0
```

`excel-worksheet range write` defaults to RAW value handling through the backend. Numeric-looking
strings stay text unless a future command explicitly exposes USER_ENTERED.
`excel-worksheet check-error` reuses worksheet readback and returns formula-style
errors such as `#VALUE!` / `#REF!`, plus warnings when a formula cell has no
cached or display result in the response. Default to worksheet-wide scans; add
`--range` only for targeted debugging or when a large worksheet makes a bounded
check more practical.

## Excel Tables

Use `excel-table` for worksheet-backed Excelize table/range views. The
`--table-id` comes from workbook/table metadata and defaults to `1` only when the
worksheet target is unambiguous.

```bash
mbs excel-table metadata --doc-id <DOC_ID> --worksheet-name Orders --table-id 1
mbs excel-table schema --doc-id <DOC_ID> --worksheet-name Orders --table-id 1
mbs excel-table sample --doc-id <DOC_ID> --worksheet-name Orders --table-id 1 --limit 50
mbs excel-table read --doc-id <DOC_ID> --worksheet-name Orders --table-id 1 --limit 100 --output table
mbs excel-table insert --doc-id <DOC_ID> --worksheet-name Orders --table-id 1 --rows rows.json
```

Use `--range A1:D100` only as an advanced override when metadata lacks the table
range.

## DB Tables

Use `db-table` for PG/SheetTable-backed worksheets created through PG import or
`db-table create`.
Prefer human-readable `--name`; use `--backend-id` only when metadata requires
it.

```bash
mbs db-table metadata --doc-id <DOC_ID> --name orders_large
mbs db-table metadata --doc-id <DOC_ID> --name orders_large --include-headers --output json
mbs db-table schema --doc-id <DOC_ID> --name orders_large
mbs db-table sample --doc-id <DOC_ID> --name orders_large --limit 50
mbs db-table read --doc-id <DOC_ID> --name orders_large --limit 100 --output table
mbs db-table insert --doc-id <DOC_ID> --name orders_large --rows rows.json
mbs db-table create --doc-id <DOC_ID> --name Orders --rows orders.json
mbs db-table create --doc-id <DOC_ID> --name Orders --columns columns.json --rows rows.json --if-exists adopt --verify
mbs db-table create --doc-id <DOC_ID> --name Orders --columns columns.json --rows rows.json --adopt-existing --verify
mbs db-table create-from-range --doc-id <TARGET_DOC_ID> --name R_OrderLines_Store1 --source-doc-id <SOURCE_DOC_ID> --worksheet-name "1店" --range A2:AR423 --header-row 0 --use-header-names --if-exists adopt --verify
mbs db-table create-from-query --doc-id <DOC_ID> --worksheet-name Orders --name OrderSummary --sql-file order_summary.sql --if-exists adopt --verify
mbs db-table create-from-query --doc-id <DOC_ID> --worksheet-name B_FxSettlement --name S1_RevenueStructureInput --sql-file s1_revenue_structure_input.sql --if-exists adopt --verify
mbs db-table create-from-query --doc-id <DOC_ID> --name OrderDetailsStructureInput --sql-file order_details_structure.sql --no-preserve-formula
mbs db-table range set-formula --doc-id <DOC_ID> --name orders_large --cell G2 --formula '=SQL("select * from orders_large limit 10")'
mbs db-table field metadata --doc-id <DOC_ID> --name orders_large --output json
mbs db-table field update --doc-id <DOC_ID> --name orders_large --field revenue --logical-type number --formatter "$#,##0.00" --width 144 --verify
mbs db-table field batch-update --doc-id <DOC_ID> --name orders_large --updates field-updates.json --verify
```

`db-table metadata` targets one PG/SheetTable-backed worksheet. Pass `--name`
or `--backend-id`; calling it with only `--doc-id` is invalid. Add
`--include-headers` when exact header text is needed. The CLI resolves the
table through `/api/v1/excel/worksheet/metadata`, then merges targeted
`/api/v1/excel/worksheet/dimensions`; with headers enabled, JSON output may
include `headers`, `header_names`, `header_count`, `headers_source`, and
`headers_exact`. Use `workbook list-worksheets` first when the table name is
unknown.

`orders.json` for `db-table create` must be a JSON array of row objects. The
CLI infers column names and logical types from those rows, then calls
`/api/v1/excel/db_table/create`. Pass `--columns columns.json` when rows are
empty or when the schema must be explicit. `--if-exists adopt` and
`--adopt-existing` adopt a matching existing PG table after a 409 response; use
`--verify` to confirm the workbook registry reports a PG/SheetTable-backed
worksheet. `db-table create-from-range` is for cross-document raw `R_*`
surfaces: it reads a source worksheet range, treats `--header-row` as a
0-based index inside the returned values matrix, optionally uses header text
via `--use-header-names` (otherwise `raw_col_NNN`), drops blank rows, and
creates the named PG table on the target `--doc-id`. Prefer it over
hand-written import Python. For merged-title sheets, start `--range` at the
semantic header row. `db-table create-from-query` is for SQL-materialized PG
handoff tables. It wraps the SQL text as `=SQL(...)`, calls
`/api/v1/excel/calc-formula`, parses table-shaped `values` / `range_values`,
then creates the named PG table through `/api/v1/excel/db_table/create`.
Current CLI versions then try to persist that same `=SQL(...)` formula into
the final table cell, defaulting to `A1`, and report the result in
`context.formula_trace`. Use `--worksheet-name` as the SQL evaluation context
and `--sql-file` for auditable ETL templates. Keep default formula
preservation when traceability matters; use `--no-preserve-formula` only when
the extra formula write should be skipped. After create, inspect JSON output
for `context.formula_trace.persisted`, then verify with `db-table metadata`,
`db-table sample`, or `workbook list-worksheets`. `db-table update` and
`db-table delete` are still planned stubs in the current CLI.

Use `db-table field metadata` / `update` / `batch-update` for PG/SheetTable
field display metadata. `property.formatter` controls the column display
format, `property.style` controls data-cell text/background/width, and
`property.headerStyle` controls header appearance. For multiple columns,
generate one JSON array and use `batch-update --verify`:

```json
[
  {
    "name": "revenue",
    "logical_type": "number",
    "property": {
      "formatter": "$#,##0.00",
      "style": {"color": "#0F172A", "backgroundColor": "#F8FAFC", "width": 144},
      "headerStyle": {"backgroundColor": "#173E56", "color": "#FFFFFF", "bold": true}
    }
  },
  {
    "name": "margin_rate",
    "logical_type": "number",
    "property": {
      "formatter": "0.00%",
      "style": {"color": "#166534", "width": 120},
      "headerStyle": {"backgroundColor": "#173E56", "color": "#FFFFFF", "bold": true}
    }
  }
]
```

After PG field style updates, read the worksheet with `excel-worksheet read
--output json` and confirm `formatting.frozen_rows`,
`formatting.auto_filter`, and `db_table.fields[*].property`. PG/db-table
header freeze/filter should come from backend readback. Header dark background
is a beautify or explicit `headerStyle` result, not a frontend default.

For the newer `workbook import` raw-surface path, prefer that command family
over teaching a post-import verification loop. When `workbook import ... --verify`
succeeds, use that stdout as the existence proof. Only run one representative
`db-table sample --limit 2` per family when a human needs quick shape
confirmation.

## Rows, Columns, Formulas, Styles

```bash
mbs excel-worksheet row insert --doc-id <DOC_ID> --worksheet-name Sheet1 --row 10 --count 2
mbs excel-worksheet row delete --doc-id <DOC_ID> --worksheet-name Sheet1 --row 10 --count 2 --yes
mbs excel-worksheet row move --doc-id <DOC_ID> --worksheet-name Sheet1 --row 10 --count 2 --destination-row 20

mbs excel-worksheet column insert --doc-id <DOC_ID> --worksheet-name Sheet1 --column B --count 2
mbs excel-worksheet column delete --doc-id <DOC_ID> --worksheet-name Sheet1 --column B --count 2 --yes
mbs excel-worksheet column move --doc-id <DOC_ID> --worksheet-name Sheet1 --column B --count 2 --destination-column D
mbs excel-worksheet column width --doc-id <DOC_ID> --worksheet-name Sheet1 --start-column B --end-column D --width 120

mbs formula read --doc-id <DOC_ID> --worksheet-name Model --range A1:E20
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name Model --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --operations ops.json --recalculate-mode worksheet
mbs formula batch-set --doc-id <DOC_ID> --operations ops.json --recalculate-mode worksheet
mbs workbook calculate --doc-id <DOC_ID>
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name Model
mbs excel-worksheet range calculate --doc-id <DOC_ID> --worksheet-name Model --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name Model
mbs formula lineage --doc-id <DOC_ID> --worksheet-name Model --cell E2 --format tree

mbs excel-worksheet style freeze-panes --doc-id <DOC_ID> --worksheet-name Sheet1 --cell B2
mbs excel-worksheet style cell batch-set --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:G1 --style header_style.json
mbs excel-worksheet style auto-filter set --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:G100
mbs excel-worksheet style auto-filter remove --doc-id <DOC_ID> --worksheet-name Sheet1
mbs excel-worksheet style gridlines toggle --doc-id <DOC_ID> --worksheet-name Sheet1 --show-gridlines false
mbs excel-worksheet style filter-values --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:G100 --column 2 --filters-active true --already-checked APAC --already-checked EMEA
mbs excel-worksheet style conditional-formats set --doc-id <DOC_ID> --worksheet-name Sheet1 --spec conditional_formats.json
mbs excel-worksheet style columns-width --doc-id <DOC_ID> --worksheet-name Sheet1 --start-column B --end-column D --width 120
mbs excel-worksheet style rows-height --doc-id <DOC_ID> --worksheet-name Sheet1 --start-row 1 --end-row 1 --height 28
mbs excel-worksheet style worksheet plan --doc-id <DOC_ID> --worksheet-name Sheet1 --mode auto_detect --spec worksheet_style.json
mbs excel-worksheet style worksheet apply --doc-id <DOC_ID> --worksheet-name Sheet1 --mode auto_detect --spec worksheet_style.json
mbs style beautify --doc-id <DOC_ID> --worksheet-name Sheet1 --dry-run --output json
mbs style beautify --doc-id <DOC_ID> --worksheet-name Sheet1 --output json
```

Run `mbs <group> <command> --help` for exact row/column JSON shapes before
structural edits.

`mbs style beautify` is the recommended one-command report/table polish path.
It inspects metadata first, classifies columns from Chinese/English headers and
sample values, applies header freeze/filter and semantic styles for Excelize,
and applies PG/SheetTable formatter/style/header metadata through batched field
updates when possible. Use `--dry-run --output json` to inspect each column's
category, formatter, confidence, and reasons before mutation.

## Charts, Images, And Dashboards

```bash
mbs workbook list-worksheets --doc-id <DOC_ID> --output json
mbs excel-worksheet chart list --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet chart get --doc-id <DOC_ID> --worksheet-name Dashboard --cell J2
mbs excel-worksheet chart create-config --doc-id <DOC_ID> --worksheet-name Dashboard --cell J2 --spec chart.json
mbs excel-worksheet chart create-config --doc-id <DOC_ID> --worksheet-name Dashboard --spec chart-with-cell.json
mbs excel-worksheet chart update --doc-id <DOC_ID> --worksheet-name Dashboard --cell J2 --chart-id rId1 --spec chart.json
mbs excel-worksheet chart delete --doc-id <DOC_ID> --worksheet-name Dashboard --chart-id rId1

# recommendation:
# author `chart.json` with top-level `"type": "json"` and renderer code in `html`
# do not default to authoring chart specs as top-level `"type": "line"` / `"bar"` / `"pie"`

mbs excel-worksheet image list --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet image read --doc-id <DOC_ID> --worksheet-name Dashboard --cell A1 --out logo.png
mbs excel-worksheet image insert --doc-id <DOC_ID> --worksheet-name Dashboard --cell B3 --file logo.png --alt-text "Company logo" --format picture-format.json
mbs excel-worksheet image set --doc-id <DOC_ID> --worksheet-name Dashboard --old-cell B3 --cell B3 --format picture-format.json --width 120 --height 91
mbs excel-worksheet image replace --doc-id <DOC_ID> --worksheet-name Dashboard --cell B3 --file logo_v2.png --format picture-format.json
mbs excel-worksheet image delete --doc-id <DOC_ID> --worksheet-name Dashboard --cell A1
mbs excel-worksheet media check --doc-id <DOC_ID> --worksheet-name Dashboard

mbs excel-worksheet dashboard validate --spec dashboard.json
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run
mbs excel-worksheet dashboard manifest --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet dashboard create-config --doc-id <DOC_ID> --spec dashboard.json --create-worksheet
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
```

`picture-format.json` uses the same anchor model as chart layout:

```json
{
  "from": {"col": 1, "row": 2, "col_off": 0, "row_off": 0},
  "to": {"col": 4, "row": 10, "col_off": 0, "row_off": 0}
}
```

Use zero-based `row` / `col` indexes in the format JSON. Keep the outer
`--cell` aligned with `format.from` when possible.

Notes:

- For dashboard authoring, prefer: `sheet-dashboard` generates `dashboard.json`, then `mbs excel-worksheet dashboard validate/refresh/manifest` executes and verifies it.
- If `dashboard_style_pack` is present in `dashboard.json`, also include the matching `industry_style` and `dashboard_story`; `dashboard validate` now checks this style linkage explicitly.
- Author `chart.json` with top-level `"type": "json"` and renderer code in `html`.
- `chart-with-cell.json` may be either flat `{cell,type,sql,html,...}` or `{cell,chart:{type,sql,html,...}}`.
- Do not default to authoring chart specs as top-level `"type": "line"`, `"bar"`, or `"pie"`.
- `chart get` resolves one chart by `--cell` or `--chart-id` after reading the worksheet chart inventory.
- Images are floating worksheet objects like charts, not values inserted inside cells.
- Images require an Excelize worksheet. Check `workbook list-worksheets --output json` first; PG-only worksheets do not support `add_picture`, and `excel-worksheet create` in a PG workbook may create a PG-only sheet. For a new image canvas, import a small blank `.xlsx` with `--engine excelize`.
- `image list` extracts picture metadata from worksheet formatting; use returned URL/media fields, anchor cell, picture id, and chart-compatible format/position fields for display and later updates.
- `image read` reads one concrete picture by `--cell` or `--picture-id`.
- `image insert` and `image set` should include `--format picture-format.json` when layout matters; `cell` alone is only an anchor and is not enough to preserve drag/resize position.
- `image replace` is an `mbs` orchestration: read existing picture, delete it, then insert the replacement at the resolved cell.
- `media check` quickly verifies whether the worksheet contains image objects and chart objects after `add_picture`, image insert/set, chart create, or dashboard refresh.
- `dashboard validate` is local-only. `dashboard create-config`, `manifest`, and `refresh` are worksheet-level `mbs` orchestrations over existing routed endpoints.
- If dashboard batch refresh/create-config fails with a server-side batch error, retry with per-chart `chart create-config --cell <CELL> --spec <single_chart.json>`.
- `dashboard manifest` and `chart list` verify persisted chart metadata, not browser canvas rendering.

## Pivot Tables

Use `mbs pivot` for persisted pivot tables. Do not use `mbs raw post` for
`/api/v1/excel/pivot_table/*`, `/api/v1/excel/read_pivot_table`, or legacy
`/api/pivot_table/*` when these commands are available.

```bash
mbs pivot read --doc-id <DOC_ID> --worksheet-name SourceData --spec pivot-config.json --output json
mbs pivot preview --doc-id <DOC_ID> --worksheet-name SourceData --spec pivot-config.json --output json
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json --dry-run
mbs pivot delete --doc-id <DOC_ID> --worksheet-name PivotResult --anchor-cell A1 --dry-run
mbs pivot delete --doc-id <DOC_ID> --worksheet-name PivotResult --anchor-cell A1 --yes
```

`pivot-config.json` for `preview` and the usual `upsert` path is the pivot
config object. A reusable copy lives at [../artifacts/pivot-config.json](../artifacts/pivot-config.json).

```json
{
  "worksheet_name": "SourceData",
  "range_address": "A1:E1001",
  "row_fields": ["period", "dimension_type"],
  "column_fields": [],
  "metrics": [
    {
      "aggregate": "sum",
      "value_field": "settled_amount_reporting",
      "label": "settled_revenue_reporting"
    }
  ],
  "row_sort": {"by": "label", "order": "asc"},
  "show_row_totals": false,
  "show_column_totals": false
}
```

`pivot read` uses the older read shape and supports one metric. If the spec
contains a single `metrics[]` item, the CLI converts it to `aggregate` and
`value_field`; for multi-metric output use `pivot preview`.

`pivot upsert` writes the pivot through the semantic pivot endpoint and requires
an explicit `--anchor-cell`. The target worksheet can be created by the backend
semantic path; do not pre-create it just to call pivot upsert. `preview` is the
right command before mutation when comparing output shape or sort behavior.

See [pivot-tables.md](pivot-tables.md) for field rules, common spec patterns,
and verification commands.

## History And Sharing

```bash
mbs history list --doc-id <DOC_ID> --limit 10
mbs history read --doc-id <DOC_ID> --version <VERSION_ID>

mbs share permission --doc-id <DOC_ID>
mbs share visibility --doc-id <DOC_ID> --visibility public --public-permission viewer
mbs share visibility --doc-id <DOC_ID> --visibility private
mbs share grant --doc-id <DOC_ID> --email user@example.com --permission viewer
mbs share grant --doc-id <DOC_ID> --email user@example.com --permission editor
mbs share remove --doc-id <DOC_ID> --email user@example.com
mbs share list --doc-id <DOC_ID>
```

Only owners can change visibility, grant access, remove access, or list shares.

## Raw API Escape Hatch

Use first-class commands first. When an uncovered endpoint is required:

```bash
mbs raw post /api/v1/excel/sql/compile --body body.json
mbs raw post /api/v1/excel/sql/write_result --body body.json
mbs raw post /api/v1/excel/get_charts --json '{"document_id":"<DOC_ID>","worksheet_name":"Dashboard"}'
mbs raw post /api/v1/excel/get_charts --body get_charts_body.json
```

`--json` takes an inline JSON object. `--body` takes a path to a JSON file. Do not pass inline JSON to `--body`.

If a workflow is not exposed through a first-class command, check `mbs --help`
and pause for a supported command or backend route.

## Legacy Aliases

The `sheet` group remains for compatibility:

```bash
mbs sheet read --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:D20
mbs sheet worksheets --doc-id <DOC_ID>
mbs sheet update-data-keep-headers --doc-id <DOC_ID> --worksheet-name Sheet1 --data rows.json --dry-run
mbs sheet update-data-keep-headers --doc-id <DOC_ID> --worksheet-name Sheet1 --data rows.json --verify
mbs sheet update-data-keep-headers --doc-id <DOC_ID> --gid 1 --data rows.json --start-row 2 --no-preserve-formulas --skip-recalculation
mbs sheet append --doc-id <DOC_ID> --gid 0 --rows rows.json --verify
mbs sheet upsert --doc-id <DOC_ID> --gid 0 --key order_id --rows rows.json --verify
```

`update-data-keep-headers` is the supported full-refresh command even though it
lives under `sheet`. It accepts only a non-empty JSON object array, performs a
header preflight, rejects unknown keys, preserves formulas and recalculates by
default, and clears stale rows after the replacement dataset. Run `--dry-run`
before the first write and `--verify` on execution. The two flags cannot be
combined. Prefer the object-specific groups above for other new workflows.

## Help Discovery

```bash
mbs --help
mbs workbook import --help
mbs excel-worksheet read --help
mbs excel-table read --help
mbs db-table read --help
```

---
name: maybeai-sheet-cli
version: 0.16.2
description: Use when the user works with MaybeAI spreadsheets through the mbs CLI for workbook inspection, local or remote-URL file import, native cross-workbook import/export, worksheet/range/table writes, full worksheet data refreshes that keep headers, formulas, worksheet styling, chart/image CRUD, dashboard validate/refresh flows, or sharing. Route dashboard design and chart composition to `sheet-dashboard`.
metadata:
  openclaw:
    requires:
      env:
        - MAYBEAI_API_TOKEN
    primaryEnv: MAYBEAI_API_TOKEN
    emoji: "📊"
    homepage: https://github.com/OmniMCP-AI/maybeai-uni
---

# MaybeAI Sheet CLI

Execute spreadsheet work through `mbs`, the console script from
`maybeai-sheet-cli`. Use first-class object commands.

For local `.xls` / `.xlsx` imports, choose the engine per worksheet when a
workbook mixes large table-like sheets and Excel-layout sheets. The workbook
import commands support `--engine auto`, `--engine postgres`, and
comma-separated worksheet engine lists. CSV/TSV files and public Google Sheet
URLs use the import-source preview flow and can import as a new workbook or
append all or selected worksheets/tabs to an existing workbook. Remote HTTPS
Excel URLs create a new workbook through `/api/v1/excel/import_by_url`.

**Prerequisites:** `MAYBEAI_API_TOKEN`, `mbs` (`pip install maybeai-sheet-cli`)

## Quick start

```bash
# Inspect before writing
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook list-worksheets --doc-id <DOC_ID> --output table

# Read and write cells/ranges
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name Sheet1 --output table
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:D20 --output table
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name Model
mbs excel-worksheet range write --doc-id <DOC_ID> --worksheet-name Sheet1 --range A1:C3 --values values.json --verify
mbs sheet update-data-keep-headers --doc-id <DOC_ID> --worksheet-name Sheet1 --data rows.json --verify

# Work with table-shaped data
mbs excel-worksheet list-table --doc-id <DOC_ID> --gid <GID> --output json
mbs excel-table sample --doc-id <DOC_ID> --worksheet-name Orders --table-id 1 --limit 20 --output table
mbs db-table sample --doc-id <DOC_ID> --name orders_large --limit 20 --output table
mbs db-table metadata --doc-id <DOC_ID> --name orders_large --include-headers --output json
mbs db-table create --doc-id <DOC_ID> --name Orders --rows orders.json
mbs db-table create --doc-id <DOC_ID> --name Orders --columns columns.json --rows rows.json --if-exists adopt --verify
mbs db-table create-from-range --doc-id <TARGET_DOC_ID> --name R_OrderLines_Store1 --source-doc-id <SOURCE_DOC_ID> --worksheet-name "1店" --range A2:AR423 --header-row 0 --use-header-names --if-exists adopt --verify
mbs db-table create-from-query --doc-id <DOC_ID> --worksheet-name Orders --name OrderSummary --sql-file order_summary.sql --if-exists adopt --verify
mbs db-table insert --doc-id <DOC_ID> --name Orders --rows new_orders.json
mbs db-table field metadata --doc-id <DOC_ID> --name orders_large --output json
mbs db-table field batch-update --doc-id <DOC_ID> --name orders_large --updates field-updates.json --verify

# Import files
mbs workbook import-plan ./mixed-workbook.xlsx --engine auto --output table
mbs workbook import ./report.xlsx
mbs workbook import ./mixed-workbook.xlsx --engine auto
mbs workbook import ./mixed-workbook.xlsx --engine "postgres,excel,excel,postgres"
mbs workbook import ./large-table.xlsx --engine postgres
mbs workbook import "https://static.example.com/imports/report.xlsx" --engine auto
mbs workbook import "https://static.example.com/download?id=123" --source-type xlsx --filename report.xlsx --engine excelize
mbs workbook import ./orders.csv --engine postgres
mbs workbook import ./orders.tsv --engine excelize
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --engine postgres
mbs worksheet import ./report.xlsx --strategy create --doc-id <TARGET_DOC_ID> --engine postgres --verify
mbs worksheet import ./report.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine postgres --verify
mbs worksheet import ./report.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --source-worksheet-name "订单" --engine postgres --verify
mbs worksheet import ./orders.csv --strategy create --doc-id <TARGET_DOC_ID> --engine postgres --verify
mbs worksheet import ./orders.csv --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --target-worksheet-name Orders --engine postgres --verify
mbs worksheet import ./orders.csv --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --source-worksheet-name refunds --engine postgres --verify
mbs worksheet import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --strategy create --doc-id <TARGET_DOC_ID> --engine excelize --verify
mbs worksheet import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --target-worksheet-name "Store 1" --engine excelize --verify
mbs worksheet import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --engine excelize --verify
mbs worksheet import ./rows.json --strategy replace --doc-id <TARGET_DOC_ID> --worksheet-name Students --verify
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --verify
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --verify
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "工作表3" --source-worksheet-name "工作簿1" --verify
mbs workbook --doc-id <DOC_ID> copy --title "Copy of Workbook"

# Formulas and sharing
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name Model --cell E2 --formula '=SUM(B2:D2)'
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --operations formulas.json --recalculate-mode worksheet
mbs db-table range set-formula --doc-id <DOC_ID> --name orders_large --cell G2 --formula '=SQL("select * from orders_large limit 10")'
mbs workbook calculate --doc-id <DOC_ID>
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name Model
mbs excel-worksheet range calculate --doc-id <DOC_ID> --worksheet-name Model --cell E2 --formula '=SUM(B2:D2)'
mbs share permission --doc-id <DOC_ID>
mbs excel-worksheet chart list --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet image list --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet image set --doc-id <DOC_ID> --worksheet-name Dashboard --old-cell B3 --cell B3 --format picture-format.json --width 120 --height 91
mbs excel-worksheet media check --doc-id <DOC_ID> --worksheet-name Dashboard
mbs style beautify --doc-id <DOC_ID> --worksheet-name Sheet1 --dry-run --output json
mbs style beautify --doc-id <DOC_ID> --worksheet-name Sheet1 --output json
mbs pivot preview --doc-id <DOC_ID> --worksheet-name SourceData --spec artifacts/pivot-config.json
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json
mbs excel-worksheet dashboard validate --spec dashboard.json
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
mbs excel-worksheet dashboard manifest --doc-id <DOC_ID> --worksheet-name Dashboard
```

- `--output table` for human inspection; `json` (default) for automation
- Use `--base-url http://localhost:7011` or `MAYBEAI_BASE_URL=http://localhost:7011` for the local `play-be` router; `localhost:3003` is the chat frontend, not the spreadsheet API backend
- Targeting flags (`--doc-id`, `--gid`, `--worksheet-name`, `--output`) work at root, group, or command level
- Always pass a leaf subcommand (`read`, `metadata`, `insert`, etc.)

Command catalog: [references/cli-commands.md](references/cli-commands.md)

## Execution order

1. Run `mbs --version` and `mbs --help` once at the start of a session; trust the local CLI over remembered examples.
2. `mbs <group> <command> --help` when flags are unclear.
3. [references/cli-commands.md](references/cli-commands.md) for command lookup.
4. Topic reference below for semantics, edge cases, and uncovered CLI gaps.

## Critical rules

**Worksheet targeting.** Non-first worksheets MUST be named explicitly. Prefer `--worksheet-name` for current object commands; use `--gid` mainly for legacy `sheet` aliases. Without either, calls often hit the first worksheet. Details: [references/read-write.md](references/read-write.md)

**Metadata-first.** Before reads or writes on an unfamiliar workbook: `workbook metadata` or `workbook list-worksheets`, then pick worksheet/gid/table.

**Worksheet table detection.** Use `excel-worksheet list-table --gid <GID>` when a visual Excel worksheet can contain multiple separated tables. The routed local path is `play-be` on port `7011`, and Excelize-backed worksheets should return content-backed table ranges such as `A4:I16` and `A20:I27` instead of one whole-sheet range.

**Import engine choice.** Use `mbs workbook import-plan ./file.xlsx --engine auto` before creating a new workbook from an unfamiliar local Excel file. Use `mbs workbook import` only to create a new workbook. To import into an existing workbook, use `mbs worksheet import --strategy create`; omit `--source-worksheet-name` to import all source worksheets/tabs, repeat it to select multiple sources, and use `--target-worksheet-name` only for one selected source. Use `--engine postgres` only for known flat tables and `--engine excelize` for reports, formulas, merged cells, styles, or multiple separated tables. For Maybe Sheet-to-Maybe Sheet imports, use `--transfer-mode values` for PG raw surfaces and `--transfer-mode native` to preserve registered engines and supported fidelity. Native transfer rejects `--engine`. Details: [references/file-management.md](references/file-management.md)

**Dashboard imports.** For chart-heavy dashboards, plan the workbook before upload. Data source worksheets that will be queried by chart SQL should be PG-compatible flat tables and usually use `postgres`; cover, summary, and dashboard canvas worksheets should usually use `excelize`. Use the worksheet-index engine list only after `import-plan` confirms sheet order.

**Object model.** Use `excel-worksheet read` for full worksheet reads and bounded `--range` reads. Use `excel-worksheet check-error` to scan worksheet readback for formula-style error values and empty cached formula results. Use `excel-worksheet range` for coordinate writes, clears, searches, formula persistence, and one-off formula calculation; `excel-table` for worksheet-backed Excelize tables; `db-table` for PG/SheetTable-backed tables; `db-table range` for PG-backed formula writes; `formula` for formula reads, workbook-level batch writes, and lineage; `workbook calculate` or `excel-worksheet calculate` for recalculation; and `share` for access.

**Write priority.** `db-table create-from-range` for cross-document raw `R_*` surfaces from a source worksheet range; `db-table create-from-query` for SQL-materialized PG/SheetTable handoff tables; `db-table create` for a new PG/SheetTable-backed table from JSON row objects; `excel-table insert` or `db-table insert` for appending rows to existing tables; `sheet update-data-keep-headers` for replacing all data rows while preserving row 1, header order, styles, and formula columns; `excel-worksheet range write` for exact cells; legacy `sheet append/upsert` only when you need the compatibility path.

**Full worksheet data refresh.** Prefer the unified entry point: `mbs worksheet import ./rows.json --strategy replace --doc-id <DOC_ID> --worksheet-name <SHEET> --verify`. It uses the same `/api/v1/excel/update_data_keep_headers` contract as `mbs sheet update-data-keep-headers`. The JSON file must be a non-empty array of objects whose keys match existing headers. The command keeps row 1 and column order, rejects unknown keys, preserves formula columns and recalculates by default, and rejects `--dry-run --verify`. Use `--dry-run` first for unfamiliar data. Details: [references/read-write.md](references/read-write.md)

**Range value mode.** `excel-worksheet range write` uses backend RAW value handling: numeric-looking strings such as `"5.53%"` and `"9,007,000"` remain strings. Treat USER_ENTERED parsing as unavailable unless a specific command exposes it.

**Verify after every write.** Use `--verify` where available, then `excel-worksheet read --output table`, `excel-table sample`, `db-table sample`, or `workbook list-worksheets`. After formula writes, recalculation, or SQL/report-sheet updates, also run `excel-worksheet check-error` on the worksheet before claiming success. For `worksheet import` into raw PG/db-table surfaces, successful stdout plus `--verify` is already the existence proof; do not loop over every created table.

**DB table metadata and headers.** `db-table metadata` is a single-table lookup; pass `--name` or `--backend-id`. Add `--include-headers` when the agent needs header text in the final JSON. Current CLI versions resolve the table through `/api/v1/excel/worksheet/metadata`, merge targeted `/api/v1/excel/worksheet/dimensions`, and return `headers`, `header_names`, and header metadata when available. Do not expect `workbook metadata` to include exact table headers.

**DB table field style.** For PG/SheetTable column formatter, color, background, width, or beautified header style, prefer `mbs db-table field batch-update --updates field-updates.json --verify` over per-column loops. Use `mbs db-table field metadata` before explicit updates and `mbs excel-worksheet read --output json` after updates to confirm `formatting.frozen_rows`, `formatting.auto_filter`, and `db_table.fields[*].property`. Plain PG/db-table reads should get freeze/filter config from the backend; frontend defaults are not the source of truth.

**DB table lifecycle.** `db-table create-from-range` is API-backed and CLI-composed for raw-surface import. `db-table create-from-query` materializes SQL results and records formula trace status. Use `--if-exists adopt` only with `--verify`. For supported cross-document worksheet copies, use `mbs worksheet import --strategy create --transfer-mode native`; do not use the legacy workbook-import native entry point.

**Styles.** Use `mbs style beautify` for agent-friendly report/table polish. It reads metadata first, classifies columns from Chinese/English headers plus sample values, applies Excelize worksheet styles, and writes PG/SheetTable field style metadata through the batch route when possible. Use first-class `excel-worksheet style` commands for explicit freeze panes, filters, widths, heights, cell style batches, gridlines, filter values, conditional formats, and worksheet style planning/apply. See [references/charts-formatting.md](references/charts-formatting.md).

**Images.** Worksheet images are floating objects like charts, not cell values. Before `image insert`, confirm the target worksheet is Excelize-backed with `workbook list-worksheets`; PG-only worksheets do not support `add_picture`. Use `image insert` / `image set` with chart-compatible picture `format` JSON for position and size (`from`, `to`, and pixel offsets), then verify with `image list` and `media check`. Do not treat the returned `cell` as enough to preserve layout after drag/resize. To create a new image canvas in an existing PG workbook, import a small blank `.xlsx` with `--engine excelize` instead of `excel-worksheet create`.

**SQL.** For reusable PG/SheetTable handoff tables, prefer `mbs db-table create-from-query --sql-file ... --verify`; it materializes the SQL result as a named DB table. For live workbook formulas, use `mbs excel-worksheet range set-formula` or `mbs db-table range set-formula`. User-facing silver sheets such as `OrderDetailsStructureInput` must expose the generating query as `A1 =SQL(...)` — materialized rows alone are not enough. See [references/formulas-sql.md](references/formulas-sql.md).

**Pivot tables.** Use first-class `mbs pivot read`, `mbs pivot preview`, `mbs pivot upsert`, and `mbs pivot delete`. Do not call `/api/v1/excel/pivot_table/*`, `/api/v1/excel/read_pivot_table`, legacy `/api/pivot_table/*`, or hand-build `MAYBE_PIVOT` formulas through `raw post` / `formula set` unless the local `mbs pivot --help` proves the command is unavailable. `pivot upsert` requires an explicit target anchor cell; if the user says `A1`, keep `--anchor-cell A1`. Details and spec examples: [references/pivot-tables.md](references/pivot-tables.md).

```bash
mbs excel-worksheet dashboard validate --spec dashboard.json
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
mbs excel-worksheet dashboard manifest --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet chart list --doc-id <DOC_ID> --worksheet-name Dashboard
```

Use `dashboard create-config` when the worksheet should be created from the spec in one run.

For dashboard specs with `chart.type: "html"`, the chart object must include non-empty `chart.html`, `chart.sql`, `chart.format.from/to`, and `chart.dimension`. Named sources must be direct SQL strings such as `"data_sources": {"mgmt_summary": "SELECT * FROM \"gid_2\""}`; never emit `"mgmt_summary": {"sql": "..."}`. For large renderer dependencies, reference approved CDN packages with `<script src>` such as jsdelivr/unpkg/cdnjs/d3js; do not inline full ECharts/D3 bundles into `chart.html`.


```bash
mbs excel-worksheet dashboard validate --spec dashboard.json
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
mbs excel-worksheet dashboard manifest --doc-id <DOC_ID> --worksheet-name Dashboard
mbs excel-worksheet chart list --doc-id <DOC_ID> --worksheet-name Dashboard
```

Use `dashboard create-config` when the worksheet should be created from the spec in one run.


## Task routing

| Task | Start here |
|------|------------|
| Command flags and examples | [references/cli-commands.md](references/cli-commands.md) |
| Read/write targeting and API choice | [references/read-write.md](references/read-write.md) |
| Upload, export, sharing | [references/file-management.md](references/file-management.md) |
| Workbook semantic overview | [references/workbook-profile.md](references/workbook-profile.md) |
| Sharing and permissions | [references/permission-sharing.md](references/permission-sharing.md) |
| Formulas and SQL result sheets | [references/formulas-sql.md](references/formulas-sql.md) |
| Pivot tables and pivot config specs | [references/pivot-tables.md](references/pivot-tables.md) |
| Formula dependency tracing | [references/lineage-trace.md](references/lineage-trace.md) |
| Charts, images, dashboards, worksheet styling | [references/charts-formatting.md](references/charts-formatting.md) |
| Sharing and permissions | [references/permission-sharing.md](references/permission-sharing.md) |
| Failures and recovery | [references/errors-recovery.md](references/errors-recovery.md) |
| Clickable cell refs in answers | [references/clickable-refs.md](references/clickable-refs.md) |
| Live `=SQL(...)` showcase | [references/sql-formula-showcase.md](references/sql-formula-showcase.md) |

## Workflows

### Inspect a workbook

```
- [ ] workbook metadata or workbook list-worksheets
- [ ] identify worksheet name, table id, or db-table name
- [ ] read sample with --output table
```

```bash
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook list-worksheets --doc-id <DOC_ID> --output table
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name <SHEET> --output table
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:D20 --output table
```

### Upload and inspect

```
- [ ] workbook import
- [ ] capture document_id from JSON output
- [ ] use import stdout plus `--verify` as creation evidence
- [ ] if needed, do one representative `db-table sample --limit 2` per family
```

```bash
# Small workbook-style files
mbs workbook import-plan ./file.xlsx --engine auto --output table
mbs workbook import ./file.xlsx --verify
mbs workbook import ./orders.csv --engine postgres
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --engine excelize
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook list-worksheets --doc-id <DOC_ID> --output table

# Large table-like files
mbs workbook import ./file.xlsx --engine postgres --verify
mbs db-table sample --doc-id <DOC_ID> --name <REPRESENTATIVE_TABLE_NAME> --limit 2 --output table

# Cross-workbook worksheet -> raw PG/db-table surface import
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --verify
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --verify

# Replace existing worksheet rows from JSON while keeping headers
mbs worksheet import ./rows.json --strategy replace --doc-id <TARGET_DOC_ID> --worksheet-name Students --verify

# Native Maybe Sheet worksheet import; engine is detected per worksheet
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "工作表3" --source-worksheet-name "工作簿1" --verify
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --verify

# Append source worksheets/tabs into an existing workbook
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --engine excelize --verify
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine excelize --verify
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --source-worksheet-name "订单" --engine postgres --verify
mbs worksheet import ./orders.csv --strategy create --doc-id <TARGET_DOC_ID> --engine postgres --verify
mbs worksheet import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --target-worksheet-name "Store 1" --engine excelize --verify
```

Do not follow successful raw-surface imports with per-table `schema` / `sample` / `read` loops. See [references/file-management.md](references/file-management.md) for engine choice and PG verification.

### Dashboard execution

```
- [ ] `mbs --version` and relevant `--help`
- [ ] `mbs workbook import-plan ./file.xlsx --engine auto --output table`
- [ ] import with `--engine auto` or an explicit worksheet-index engine list
- [ ] `workbook list-worksheets` verifies Data_* PG and Dashboard/summary Excelize where intended
- [ ] `dashboard validate --spec dashboard.json`
- [ ] `dashboard refresh --dry-run` checks payload shape before mutation
- [ ] execute `dashboard refresh`; if batch errors persist, use per-chart `chart create-config`
- [ ] `dashboard manifest` and `chart list` verify persisted metadata
- [ ] read source Data_* sheets and run browser/vision verification when logged-in canvas access exists
```

See [references/charts-formatting.md](references/charts-formatting.md) for chart spec shapes, fallback, and verification limits.

### Sync rows by key

```
- [ ] confirm key column name
- [ ] use legacy sheet upsert when key-based merge is required
- [ ] recalculate if downstream formulas exist
- [ ] read back target range
```

```bash
mbs sheet upsert --doc-id <DOC_ID> --gid <GID> --key order_id --rows rows.json --verify
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name <SHEET>
```

### SQL result sheet

```
- [ ] headers + read sample on source sheet
- [ ] write a live =SQL(...) formula
- [ ] read result sheet
- [ ] scan the worksheet with `excel-worksheet check-error`
```

See [references/formulas-sql.md](references/formulas-sql.md).

### Pivot table

```
- [ ] inspect source worksheet headers
- [ ] author `pivot-config.json`
- [ ] preview pivot output
- [ ] upsert with explicit target worksheet and anchor cell
- [ ] read target range to verify
```

```bash
mbs pivot preview --doc-id <DOC_ID> --worksheet-name <SOURCE_SHEET> --spec pivot-config.json --output table
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name PivotResult --range A1:H30 --output table
```

See [references/pivot-tables.md](references/pivot-tables.md).

### Trace formula lineage

```bash
mbs formula lineage --doc-id <DOC_ID> --worksheet-name <SHEET> --cell E2 --format tree --output yaml
```

See [references/lineage-trace.md](references/lineage-trace.md) for response interpretation.

### Share or check access

```bash
mbs share permission --doc-id <DOC_ID>
mbs share visibility --doc-id <DOC_ID> --visibility public --public-permission viewer
# Share read-only access with a MaybeAI user email
mbs share grant --doc-id <DOC_ID> --email user@example.com --permission viewer
# Share write/edit access with a MaybeAI user email
mbs share grant --doc-id <DOC_ID> --email user@example.com --permission editor
mbs share list --doc-id <DOC_ID>
```

See [references/permission-sharing.md](references/permission-sharing.md) for owner requirements and access rules.

## Boundaries

- **Dashboard/chart layout** -> use `sheet-dashboard`, not this skill
- **Uncovered CLI gaps** -> check current `mbs --help` for a supported command
- **Clickable refs** -> only confirmed locations; see [references/clickable-refs.md](references/clickable-refs.md)

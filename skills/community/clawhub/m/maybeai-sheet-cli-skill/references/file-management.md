# File Management Reference

## Contents

1. When to use this
2. Basic conventions
3. Engine selection
4. Core file commands
5. Sharing and permissions
6. Recommended flows

## 1. When to use this

Read this document when the task involves uploading, importing, searching, copying, renaming, deleting, sharing, or exporting MaybeAI spreadsheets.

## 2. Basic conventions

- Base URL defaults to `https://a-play-be.maybeai.cn`
- Auth comes from `MAYBEAI_API_TOKEN`
- Most follow-up commands use `--doc-id <document_id>` or `--url <sheet_url>`
- `mbs workbook import` creates a new workbook from a local file or remote source; `mbs worksheet import --strategy create` imports worksheets into an existing workbook

- After import succeeds, record:
  - `document_id`
  - `uri`

## 3. Engine selection

MaybeAI Sheet routes worksheets through either Excelize or SheetTable:

- `excelize` is the workbook-style runtime for Excel layout, styles, formulas, merged cells, and workbook semantics.
- `postgres` / `pg` is the SheetTable runtime for large table-like data, SQL, large row counts, large cell counts, append/upsert, and PG-native reads/writes.

Best practice:

- Choose engine per worksheet for mixed workbooks; do not force the whole workbook to Postgres just because one sheet is large.
- Inspect unfamiliar files before creating a workbook: `mbs workbook import-plan ./file.xlsx --engine auto --output table`.
- Use `mbs workbook import ./file.xlsx --engine auto` when the backend should detect engines per worksheet.
- Use `mbs workbook import "https://static.example.com/file.xlsx" --engine auto` to create a workbook from a remote Excel URL. This routes through `/api/v1/excel/import_by_url`; it does not append into an existing workbook.
- Use comma-separated engines by worksheet index when the target is known, for example `--engine "postgres,excel,excel,postgres"`.
- Use `mbs workbook import ./orders.csv --engine postgres` or a public Google Sheet URL with `--engine ...` for import-source flows.
- Use `mbs worksheet import <source> --strategy create --doc-id <TARGET_DOC_ID>` for an existing workbook. Omit `--source-worksheet-name` to import all previewed worksheets/tabs, repeat it to select multiple sources, and use `--target-worksheet-name` only for one selected source.
- Prefer Postgres for a worksheet when it has more than 5,000 rows and is one flat table whose data columns each have one datatype except the header and missing values. The older high-cell-count preference still applies when the data is one homogeneous table.
- If the task depends on Excel-specific workbook fidelity, use `excel`/`excelize` for those worksheets.
- Use Excelize for reports, summaries, dashboards, formulas, merged cells, styled workbooks, or worksheets with multiple separated tables. For example, `L1_广州瑞鹏_详细` in the LLM cost analysis workbook has two tables in one worksheet and should use Excelize.
- A small single table such as `L1_客户集中度_帕累托` can use PG or Excelize; auto may choose Excelize because the sheet is not large.
- For chart-heavy dashboards, small flat `Data_*` worksheets may still need PG because chart SQL will query them. Use `import-plan` to confirm sheet order, then choose `postgres` for SQL source sheets and `excelize` for dashboard/cover/summary sheets.
- Explicit `--engine postgres` is strict. If the worksheet is not PG-compatible, expect `PG_IMPORT_UNSUPPORTED_LAYOUT`. Use `--engine auto` when fallback to Excelize is acceptable.
- Do not push large table data through row-object JSON writes; import the file with `engine=postgres` instead.
- SheetTable owns datatype normalization during import. The CLI should only pass intent through `--engine`; parsing to same datatype should be enabled by backend default.
- After import, verify the response top-level `engine`, plus per-worksheet `worksheet_engines` entries such as `worksheet_name`, `index`, `requested_engine`, `selected_engine`, `final_engine`, `fallback_reason`, `reason`, and datatype warnings/errors.
- For import-source appends into existing workbooks, single-worksheet commits should expose `target.gid` and `target.worksheet_name`; multi-worksheet commits keep top-level `target` workbook-scoped, so inspect `result.worksheets`.
- For raw PG/db-table surface imports, target table names default to `R_{sanitized_worksheet_name}`. Omit `--source-worksheet-name` to import all source worksheets, or repeat it to select worksheets. Successful `worksheet import` stdout plus `--verify` is the creation evidence.
- If shape confirmation is needed after a batch raw-surface import, do at most one representative `mbs db-table sample --limit 2` per family.
- For Maybe Sheet-to-Maybe Sheet imports, use `--transfer-mode values` for PG raw surfaces or `--transfer-mode native` to preserve each source worksheet's registered engine and supported fidelity. Native transfer does not accept `--engine`.

### SheetTable preprocess contract

Do not implement datatype detection or conversion inside `maybeai-sheet-cli`.
For DB-backed imports, `SheetTable` should preprocess worksheet columns before
materializing them into PostgreSQL:

- infer one target datatype per column from non-header values
- allow empty cells and common missing-value markers such as `n/a`
- coerce values that can safely convert to the inferred datatype
- keep or report values that cannot convert instead of silently corrupting data
- prefer Postgres when a worksheet has more than 10,000 rows and the columns can be normalized

When changing this behavior, update and test the source in
`/Users/dengwei/work/ai/maybeai-uni/mcp/SheetTable`, then verify through the
local routed runtime described in
`/Users/dengwei/work/ai/maybeai-uni/docs/maybeai_sheet/debugging-runtime.md`:

```bash
cd /Users/dengwei/work/ai/maybeai-uni/mcp/SheetTable
just run

cd /Users/dengwei/work/ai/maybeai-uni/mcp/maybeai-sheet-cli
uv run mbs --base-url http://localhost:7011 workbook import ./mixed-workbook.xlsx --engine auto
uv run mbs --base-url http://localhost:7011 workbook list-worksheets --doc-id <DOC_ID> --output json
```

The verification target is the routed path `mbs -> play-be -> SheetTable`, not
a direct CLI-only unit test. Also use SheetTable tests such as `go test -v ./...`
and the composite router test asset referenced by `debugging-runtime.md` when
the change affects engine selection or registry routing.

## 4. Core file commands

### Import a mixed workbook with engine autodetect

Use autodetect first when the workbook has both table-like and Excel-layout worksheets:

```bash
mbs workbook import-plan /absolute/path/to/file.xlsx --engine auto --output table
mbs workbook import /absolute/path/to/file.xlsx --engine auto
```

Expected response should include the selected engine for each worksheet. If that
field is missing, call `mbs workbook list-worksheets --doc-id <DOC_ID> --output json`
and verify `engine` or `data_engine` per worksheet.

### Import a remote Excel URL into a new workbook

Pass a public HTTPS Excel URL as the positional source:

```bash
mbs workbook import "https://static.example.com/imports/report.xlsx" --engine auto
mbs workbook import "https://static.example.com/imports/report.xlsx" --filename "Board Pack.xlsx" --engine excelize
mbs workbook import "https://static.example.com/download?id=123" --source-type xlsx --filename report.xlsx --engine postgres
```

This path calls `POST /api/v1/excel/import_by_url` with `file_url`, the resolved
`filename`, and `engine`. `--filename` is optional. Resolution order is the
explicit option, the decoded URL path basename, then `upload.xlsx`.

Remote Excel URL import only creates a new workbook. Do not combine it with
`--doc-id`, `--url`, `--uri`, worksheet selection flags, `--preview-only`, or
`--transfer-mode native`. Use exactly one of `excelize`, `postgres`, or `auto`; the remote
route does not support comma-separated per-worksheet engines. Explicit
`excelize` forwards the URL directly to the Excelize import service. `auto` and
`postgres` first download the workbook for worksheet planning before routing it
to the selected engine, so their request cost includes that planning download.

### Import CSV, TSV, or Google Sheet into a new workbook

CSV/TSV uploads and public Google Sheet URLs use the import-source preview +
commit flow:

```bash
mbs workbook import ./orders.csv --engine postgres
mbs workbook import ./orders.tsv --engine excelize
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --engine postgres
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --source-worksheet-name "1店" --worksheet-name "Store 1" --engine excelize
mbs workbook import ./orders.csv --preview-only --output json
```

When no explicit source worksheet/tab is selected for a new workbook, the CLI
sends `selections: []` and lets the backend import all previewed worksheets/tabs.
When selecting one Google tab, prefer `--source-worksheet-name`; use
`--candidate-id` only to disambiguate duplicate backend candidate ids.

### Import local files or Google Sheet tabs into an existing workbook

Use this when the target should gain a normal worksheet, not a raw `R_*`
PG/db-table surface:

```bash
# Omit --source-worksheet-name to import all previewed worksheets/tabs.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --engine excelize
mbs worksheet import --strategy create ./orders.csv --doc-id <TARGET_DOC_ID> --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --engine excelize

# Pass one --source-worksheet-name to import one source worksheet/tab, optionally renamed.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine excelize
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine postgres
mbs worksheet import --strategy create ./orders.csv --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --target-worksheet-name Orders --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --target-worksheet-name "Store 1" --engine excelize

# Repeat --source-worksheet-name to import multiple selected source worksheets/tabs.
mbs worksheet import --strategy create ./report.xlsx --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --source-worksheet-name "订单" --engine postgres
mbs worksheet import --strategy create ./orders.tsv --doc-id <TARGET_DOC_ID> --source-worksheet-name orders --source-worksheet-name refunds --engine postgres
mbs worksheet import --strategy create "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --engine excelize
```

For Excel files, `--source-worksheet-name` is the source worksheet returned by
`import_worksheet_preview`. For CSV/TSV/Google import sources, `--source-worksheet-name`
selects the source worksheet/tab name from preview when importing into an
existing workbook. If any requested worksheet/tab does not exist, the CLI fails
before commit/data import and prints the available worksheet names.
`--target-worksheet-name` controls the new worksheet name in the target workbook
and is only valid when exactly one source worksheet/tab is selected. If omitted,
the backend/CLI uses the source worksheet/tab's suggested worksheet name.

### Replace data rows from JSON while keeping headers

Use the unified worksheet import entry point for a full data refresh of one
existing worksheet:

```bash
mbs worksheet import ./rows.json \
  --strategy replace \
  --doc-id <TARGET_DOC_ID> \
  --worksheet-name Students \
  --verify
```

The JSON file must be a non-empty array of objects whose keys match the target
worksheet headers. This strategy calls `/api/v1/excel/update_data_keep_headers`,
keeps row 1 and column order, preserves formula columns by default, and clears
stale data rows. Use `--dry-run` for preflight validation; it cannot be combined
with `--verify`. JSON replace does not accept `--engine`, `--transfer-mode`, or
source worksheet selection options.

### Natively import worksheets from another Maybe Sheet workbook

Use this when the target should receive real worksheet copies rather than
value-materialized `R_*` tables:

```bash
# Copy selected worksheets. Mixed PG and Excelize selections are supported.
mbs worksheet import \
  --strategy create \
  --transfer-mode native \
  --doc-id <TARGET_DOC_ID> \
  --source-doc-id <SOURCE_DOC_ID> \
  --source-worksheet-name "工作表3" \
  --source-worksheet-name "工作簿1" \
  --verify \
  --output json

# Copy every source worksheet.
mbs worksheet import \
  --strategy create \
  --transfer-mode native \
  --doc-id <TARGET_DOC_ID> \
  --source-doc-id <SOURCE_DOC_ID> \
  --verify \
  --output json
```

Native flow:

1. Read source `/api/v1/excel_v2/worksheet/metadata` once.
2. Validate repeated `--source-worksheet-name` values, or select all metadata items.
3. Derive `pg` or `excelize` from each worksheet's `data_engine`/source metadata.
4. Call `/api/v1/excel/copy_worksheet` once per worksheet.
5. With `--verify`, read target worksheet metadata once and verify final name,
   gid, and engine.

Do not pass `--engine`; it is selected internally per worksheet. Use
`--target-worksheet-name` only for one selected worksheet. The backend may
rename a conflict to `Name (2)`, and the CLI reports that final name. Empty
worksheets are valid native copies. This mode supports PG -> PG and Excelize ->
Excelize only; a mixed logical workbook is allowed, but no worksheet is
converted between engines.

Native copy uses the CLI HTTP timeout, which defaults to 30 seconds. For large
worksheets, pass `--timeout 600`. If a timeout names a worksheet, do not rerun
the full batch immediately: the backend may still complete after the client
disconnects. Inspect target worksheet metadata/listing first, then retry only
the unconfirmed worksheet with explicit `--worksheet-name`. Use `--verbose` to
print the active worksheet index and engine before each copy.

### Import source worksheets into raw PG/db-table surfaces in another workbook

Use `worksheet import --strategy create --transfer-mode values` for cross-workbook worksheet -> raw surface creation when
the target should become an `R_*`-style PG/db-table backing table:

```bash
mbs worksheet import --strategy create --transfer-mode values --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --verify
mbs worksheet import --strategy create --transfer-mode values --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --verify
mbs worksheet import --strategy create --transfer-mode values --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --verify
```

Target table names default to `R_{sanitized_worksheet_name}`. If
`--source-worksheet-name` is omitted, the CLI calls `/api/v1/excel_v2/worksheet/metadata`
for the source workbook and imports all returned worksheets. If multiple
`--source-worksheet-name` values are provided, the CLI validates them against source
metadata before importing, so missing names fail before partial creation and
print the available worksheet names.

`values` is the compatibility default, so existing commands may omit it. This
path only accepts omitted/`--engine postgres|pg`, reads source
`FORMATTED_VALUE`, and does not preserve formulas or Excelize formatting.

Treat successful stdout plus `--verify` as the creation proof. Do not follow
that with `db-table schema`, `db-table read`, or repeated `db-table sample`
calls for every created table. If the workflow needs a quick shape check, sample
one representative table per family:

```bash
mbs db-table sample --doc-id <TARGET_DOC_ID> --name R_OrderLines_Store1 --limit 2 --output table
```

### Import with explicit per-worksheet engines

The comma-separated list matches worksheet index order:

```bash
mbs workbook import /absolute/path/to/file.xlsx --engine "postgres,excel,excel,postgres"
```

Use this when worksheet 1 and 4 are table-like but worksheet 2 and 3 require
Excel workbook fidelity.

For dashboards, a common pattern is:

```text
Cover, Dashboard -> excelize
Data_KPI, Data_Trend, Data_Platform, Data_Quarter -> postgres when flat and SQL queried
```

Do not guess this list from memory. Run `import-plan --engine auto --output table`
and map engines by returned worksheet index.

### Import a large table-like file into SheetTable/PG

Use the CLI first:

```bash
mbs workbook import /absolute/path/to/file.xlsx --engine postgres
```

If an older installed CLI does not expose `--engine`, upgrade the CLI before importing large table files.

Expected success shape:

```json
{
  "success": true,
  "documentId": "<document_id>",
  "fileUri": "https://www.maybe.ai/docs/spreadsheets/d/<document_id>",
  "sheets": ["Sheet1"]
}
```

Then verify routing with the CLI:

```bash
mbs workbook list-worksheets --doc-id <DOC_ID> --output json
```

Confirm the response top-level `engine` and per-worksheet `worksheet_engines`, or that `workbook list-worksheets` reports `engine: "pg"` or worksheet `data_engine: "pg"` for Postgres-backed worksheets.

### Import a workbook-style file

CLI:

```bash
mbs workbook import ./report.xlsx
```

Use this for Excelize/workbook-style imports where layout, styles, formulas,
merged cells, or workbook fidelity matter more than table scale.

### List or search files

Use search when you need to find historical files by keyword.

CLI:

```bash
mbs file list --limit 20
mbs file search --query "q2 forecast" --limit 20
```

### Export

Guidance:

- Prefer `export` when you want the `.xlsx` file directly
- Use `download` when you already have a `uri`

CLI:

```bash
mbs file export --doc-id <DOC_ID> --out workbook.xlsx
```

### Copy a workbook

Use workbook copy when you need a new editable document based on an existing
workbook. The backend should preserve worksheet engine topology when possible,
so verify the copied workbook with `workbook list-worksheets` before continuing.

```bash
mbs workbook --doc-id <DOC_ID> copy --title "Copy of Workbook"
mbs workbook list-worksheets --doc-id <NEW_DOC_ID> --output table
```

## 5. Sharing and permissions

Use the `mbs share ...` commands in [permission-sharing.md](permission-sharing.md).

## 6. Recommended flows

### Bring a new file into the system

1. Inspect approximate row count and workbook intent
2. Run `mbs workbook import-plan ./file.xlsx --engine auto --output table`
3. If sheets are mixed, use `mbs workbook import ./file.xlsx --engine auto`
4. If all sheets are table-like and rows > 10,000, use `mbs workbook import ./file.xlsx --engine postgres`
5. If worksheet engines are known, use `mbs workbook import ./file.xlsx --engine "postgres,excel,excel"`
6. Otherwise use `mbs workbook import ./file.xlsx`
7. Record `document_id` from JSON output
8. `mbs workbook list-worksheets --doc-id <DOC_ID>`
9. Sample only when needed for shape confirmation; prefer one representative `excel-table sample` or `db-table sample --limit 2`, not a per-table loop

### Bring in a chart-heavy dashboard workbook

1. `mbs workbook import-plan ./dashboard.xlsx --engine auto --output table`
2. Identify SQL source worksheets, usually flat `Data_*` tabs.
3. Identify canvas/layout worksheets, usually `Dashboard`, cover, and summaries.
4. Import with `--engine auto` only if the plan chooses the intended engines.
5. Otherwise import with an explicit worksheet-index list such as `--engine "excel,postgres,postgres,excel"`.
6. `mbs workbook list-worksheets --doc-id <DOC_ID> --output table`
7. Verify source `Data_*` sheets report PG when chart SQL will query them.

### Bring a large table-like file into the system

1. Use `mbs workbook import ./file.xlsx --engine postgres`
2. Record `documentId` and `fileUri`
3. `mbs workbook list-worksheets --doc-id <DOC_ID> --output json`
4. Confirm response top-level `engine` and per-worksheet `worksheet_engines`, or `engine: "pg"` / `data_engine: "pg"` in list output
5. If needed, `mbs db-table sample --doc-id <DOC_ID> --name <REPRESENTATIVE_TABLE_NAME> --limit 2 --output table`

### Batch raw-surface import with probe budget

1. Prepare the family-level import plan or source list.
2. Run `mbs workbook import ... --verify`.
3. Treat successful stdout plus `--verify` as the creation evidence.
4. Do not loop over each created table with `db-table schema`, `db-table sample`, or `db-table read`.
5. If shape confirmation is needed, run at most one representative `db-table sample --limit 2` per family.

### Export before delivery

1. Finish all writes
2. `mbs excel-worksheet range read --output table` or `mbs excel-table sample` on key ranges
3. `mbs file export --doc-id <DOC_ID> --out workbook.xlsx`

### Reuse a historical file

1. `mbs file search --query "<keyword>"`
2. If copying is needed, use `mbs workbook --doc-id <DOC_ID> copy --title "<NEW_NAME>"`
3. Edit the selected workbook

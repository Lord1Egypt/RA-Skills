---
version: v0.21.8
name: maybeai-sheet-cli
description: Use when the user works with MaybeAI spreadsheets through the mbs CLI for workbook inspection, local or remote-URL file import, native cross-workbook import/export, worksheet/range/table writes, worksheet calculation and error scans, complete table/SQL reads with frame export, SQL-to-Base materialization, full worksheet data refreshes that keep headers, formulas, worksheet styling, chart/image CRUD, dashboard validate/refresh/export-template flows, or sharing. Route dashboard design and chart composition to `sheet-dashboard`.
metadata:
  cli_version: "0.28.4"
  openclaw:
    requires:
      env:
        - MAYBEAI_API_TOKEN
    primaryEnv: MAYBEAI_API_TOKEN
    emoji: "📊"
    homepage: https://github.com/OmniMCP-AI/maybeai-uni
required_environment_variables:
  - name: MAYBEAI_API_TOKEN
---

# MaybeAI Sheet CLI

Execute spreadsheet work through `mbs`, the console script from
`maybeai-sheet-cli`. Use first-class object commands.

## Target model gate

Before choosing a command, inspect the installed CLI rather than relying on a
documented command map:

```bash
mbs --help
mbs workbook --help
mbs worksheet --help
mbs <PUBLIC_GROUP> <PUBLIC_COMMAND> --help
```

Use `mbs workbook inspect` to inspect the workbook and `mbs worksheet list` to
discover worksheet identities. A worksheet name or `gid` is only a locator; it
does not prove the target supports cells, ranges, or stable table records.

| Target model | Required identity | Use | Do not use |
|---|---|---|---|
| Sheet grid | `worksheet_name` or `gid` | A1 ranges, cell formulas, worksheet calculation, row/column layout, cell notes | Base record/field selectors |
| Sheet table | worksheet locator plus persistent `table_id` when multiple tables exist | table read/insert/update and table/row/column views | treating a scan-order table number as a stable ID |
| Base table | `table_id` (or `table_name` for resolution), then `field_id`/`record_id` | typed records, Base field/column operations, Base Formula | A1/range writes, cell formulas, keep-headers refresh |
| Worksheet SQL Config | SQL-config worksheet identity plus raw SQL | `mbs sql config`, preview, and materialization | a legacy SQL cell wrapper or cell Formula |

## Canonical operation layer

Use the public canonical groups (`workbook`, `worksheet`, `table`, `range`, `row`,
`column`, and `formula`) for new work. They emit `contract_version: "1.0"` JSON with `ok`, `operation`,
`target`, and either `result` or `error`; `--output table|yaml` only changes
rendering. Mutations default to `--verify`; use `--dry-run` before a destructive
or unfamiliar request and pass `--expected-revision`/`--idempotency-key` when
the workflow needs concurrency protection.

Canonical target URIs are stable, redacted MaybeAI URLs:

```text
Sheet worksheet: https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>
Sheet table:     https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>&tid=<TABLE_ID>
Base table:      https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>
Base by name:    https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?table=<TABLE_NAME>
```

`--target` is accepted by canonical object operations and mutations. Use the
runtime help output as the sole command-discovery contract; do not maintain or
infer a static command map from this skill.

For `sql query` and `sql preview`, a workbook target may include the worksheet
selector `?table=<WORKSHEET_NAME>`. The CLI resolves that selector first and
then sends the SQL request against the workbook target, so SQL still requires
a workbook URL rather than a Base-table `tid` target. Preserve the selector
when the query is intended for one worksheet:

```bash
mbs sql query \
  --target "$WORKBOOK?table=Sheet6" \
  --sql-file result.sql \
  --all \
  --frame-out /tmp/query.parquet
```

### Runtime command discovery and compatibility policy

Run `mbs --help` before selecting a top-level group, then run
`mbs <group> --help` before selecting its operation. The parent help lists the
public command surface that agents may generate. Consult the selected command's
`--help` for required selectors and mutation flags.

A command that remains directly callable but is absent from its parent help is a
hidden compatibility command. Do **not** probe for, suggest, or generate it in
new workflows. If an existing integration explicitly names one, explain that it
is compatibility-only and first look for a public workflow in the current help.
If no public command preserves the requested semantics, report the capability
gap instead of silently composing a lossy substitute.

`worksheet style` is public. When the user explicitly requests worksheet
styling, discover its supported nested operations with `mbs worksheet style
--help`; do not duplicate a nested operation list in this skill.

### Resource style commands and config aliases

The current public style operations are `worksheet style`, `table style`,
`range style`, `row style`, and `column style`. Public resource-local config
commands are `worksheet config`, `table config`, `row config`, and `column
config`. Use `range style` for a range; `range config` is compatibility-only and
must not be generated.

```bash
mbs worksheet config --target "$SHEET" --spec worksheet-config.json --verify
mbs table config --target "$SHEET_TABLE" --section header --spec table-style.json --verify
mbs range style --target "$SHEET" --range B2:D4 --spec range-style.json --verify
mbs row config --target "$SHEET" --rows 2:4 --spec row-style.json --verify
```

Use `--scope entire-grid` only with `--yes` or `--dry-run`. `worksheet config`
keeps behavior separate from `--style-spec`; the style spec cannot be combined
with `--spec` or the worksheet behavior flags (`--freeze-*`, `--gridlines`, or
`--zoom`). The `--zoom` flag is retained by the CLI but is currently rejected
by the HTTP adapters as unsupported; do not rely on it for remote writes. Table
styles may target `all`, `header`, `body`, or `totals`. For
column styles, pass exactly one of `--columns` (Sheet) or `--field` (Base).

For `worksheet config --spec`, prefer the canonical nested schema:

```json
{
  "layout": {
    "freeze": {"rows": 1, "columns": 0},
    "gridlines": {"visible": false},
    "zoom": 110
  },
  "filter": {
    "enabled": true,
    "range": "A1:H100",
    "conditions": [{"field_id": "col_status", "op": "in", "value": ["open"]}]
  },
  "view": {
    "id": "optional-view-id",
    "fields": {"order": ["col_status"], "hidden": ["col_internal"]},
    "sorts": [{"field_id": "col_status", "direction": "asc"}]
  }
}
```

The CLI accepts legacy keys for compatibility but normalizes output to this
shape. `layout.*` and `filter.range` are Sheet-only in the canonical model,
but the current HTTP Sheet adapters only implement `layout.freeze`,
`layout.gridlines`, `filter.enabled`, and `filter.range`; `layout.headings` and
`layout.zoom` are rejected as unsupported. `filter.conditions` and `view.*`
are Base-only. For Base view configuration, use `--doc-id` plus `--table-id`
(or a Base target URI), not a `gid`; a view ID is optional when saving a new
view. Unsupported engine properties fail before mutation.

### Column rename and resource style (`column.rename`, `column.style`)

`column rename` changes one Sheet header or Base field name. Provide exactly one
of `--column`, `--field`, or `--field-id`, plus required `--new-name`.

```bash
# Sheet/SheetTable: one A1 column; header row is 1-based and defaults to 1.
mbs column rename --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=0" \
  --column B --new-name "Net Revenue" --verify

# Base: resolve a human-readable field or use its stable ID.
mbs column rename --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" \
  --field-id <FIELD_ID> --new-name "Net Amount" --verify
```

In the current CLI, `column config` is a command-name alias for
`column style`, not a typed field-metadata editor. It requires `--spec` and
exactly one style selector: `--columns` for a Sheet target or `--field` for a
Base target. The alias still emits the `column.style` operation; it does not
accept the older `--field-type`, `--required`, `--unique`, `--default`, or
`--options` flags.

```bash
mbs column style --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=0" \
  --columns B:D --spec column-style.json --verify
mbs column config --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" \
  --field amount --spec column-style.json --verify
```

For Base schema changes, use only the public commands shown by `mbs column
--help`, such as `column insert` and `column rename`. `column config` is a style
operation, not a typed field-metadata editor. If a requested Base field property
is not exposed by a public command, report a capability gap; do not generate a
hidden compatibility command.

To convert an existing Base Formula field to an ordinary field type, use the
public `column batch-update` command with an update object that explicitly
requests materialization:

```json
[
  {
    "field_id": "col_formula",
    "logical_type": "text",
    "formula_conversion": "materialize"
  }
]
```

```bash
mbs column batch-update \
  --target "$BASE_TABLE" \
  --updates formula-to-text.json \
  --dry-run

mbs column batch-update \
  --target "$BASE_TABLE" \
  --updates formula-to-text.json \
  --verify
```

`--updates` accepts an array of JSON objects, so `formula_conversion` belongs
on the individual field update and is passed through unchanged. Use
`formula_conversion: "materialize"` only when the current field is Formula and
the requested `logical_type` is an ordinary type. Materialization preserves the
current formula results as field values and removes Formula metadata; it is a
destructive schema/data-semantic change and must not be inferred for ordinary
type, name, or style updates. The conversion instruction is not a persisted
field property, so verification should check the resulting `logical_type` and
values rather than expect `formula_conversion` in the readback.

Use `formula set`, `formula validate`, `formula calculate`, and `formula
recalculate` according to their runtime help. Do not generate the hidden
`formula compile` or `formula batch-set` compatibility commands.

Do not infer the model from a worksheet's name, a compatibility alias, or its
visual appearance. If inspection does not return an engine and Base identity,
stop before a mutation and obtain the required target details through the public inspection/list workflow. The public Base surface is
`mbs table`, `row`, `column`, and `formula` with a Base target. Do not
substitute an A1/range or keep-headers command for a Base record write.

For local `.xls` / `.xlsx` imports, choose the engine per worksheet when a
workbook mixes large table-like sheets and Excel-layout sheets. The workbook
import commands support `--engine auto`, `--engine base`, and
comma-separated worksheet engine lists. CSV/TSV files and public Google Sheet
URLs use the import-source preview flow and can import as a new workbook or
append all or selected worksheets/tabs to an existing workbook. Remote HTTPS
Excel URLs create a new workbook through `/api/v1/excel/import_by_url`.
To migrate one existing Sheet-backed worksheet to Base, use the guarded
`worksheet convert-to-base` workflow below; it is a one-way data migration,
not an import-engine setting.

**Prerequisites:** `MAYBEAI_API_TOKEN`, `mbs` (`pip install maybeai-sheet-cli`)

**Delegated subagent rule.** For a delegated MaybeAI task, use `terminal` first:
`mbs --version` and `test -n "$MAYBEAI_API_TOKEN"`. Do not infer missing mbs,
terminal, or token from old files, logs, or JSON artifacts. Only report a
missing token when that command actually shows it is absent.

**CLI 0.28 compatibility boundaries.** Generate only the public command
surface for new workflows:

- Use `mbs worksheet …`, never `mbs excel_worksheet …`; the underscore
  alias was removed.
- Use `mbs range lineage --target <SHEET_TARGET> --range <A1_CELL_OR_RANGE>`;
  `range lineage --cell` was removed.
- Use `mbs worksheet beautify`, `mbs worksheet config`, or resource-local
  `range`, `row`, `column`, and `table` style commands for styling.
- `mbs worksheet beautify` defaults to `--layout auto`: it keeps ordinary
  column tables on the field-by-column path, including date columns. It selects
  a pivot/report only after finding at least two concrete horizontal members
  (for example, `1店`/`2店`, `Store A`/`Store B`, or `Q1`/`Q2`); generic names
  such as `日期` or `门店`, and a lone `合计`/`Total`, are not pivot evidence.
  For a pivot/report, the first column of the target range is treated as row
  labels (text or numeric codes) and each value row is formatted from its
  label: `毛利率` is percent while `毛利-CNY` is currency. Use dry-run before
  applying, and pass `--layout table` or `--layout pivot` only when an explicit
  override is needed.
- Use `mbs range note read|set|clear`, not the removed nested
  `mbs cell note read|set|clear` commands. `read` accepts an A1 range; `set`
  and `clear` currently require one A1 cell.

## Quick start

```bash
# Discover the installed public surface and target identity first.
mbs --help
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output json
mbs table list --doc-id <DOC_ID> --output json

# Read a bounded preview. Omitting --limit requests 1000 rows.
mbs range read --target "$SHEET" --range A1:D20 --output table
mbs table read --target "$BASE_TABLE" --limit 100 --output table

# Export every page to one local frame; use backend ordering when available.
mbs table read --target "$BASE_TABLE" --all --order-by order_id --frame-out /tmp/orders.parquet

# Public writes use explicit frames/keys and verification.
mbs table insert --target "$BASE_TABLE" --frame-in rows.json --verify
mbs table update --target "$BASE_TABLE" --frame-in corrected_rows.json --key order_id --verify
mbs formula set --target "$SHEET" --cell E2 --expression '=SUM(B2:D2)' --verify
mbs range note set --target "$SHEET" --range B2 --text "Reviewed" --verify

# Current public worksheet and SQL operations.
mbs worksheet calculate --target "$SHEET" --verify
mbs worksheet check-error --target "$SHEET" --range A1:Z100
mbs sql query --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --all --frame-out /tmp/query.parquet
mbs sql materialize --target "$BASE_TABLE" --sql-file result.sql --mode create --schema schema.json --verify
```

All public `table create` source variants use the canonical operation
`table.create`, including frame, SQL-query, and worksheet-range creation.
Adapters must not expect `table.create-from-query` or
`table.create-from-range` in the response envelope.

Whole-table replacement does not have an automatic public-command substitute.
Do not rewrite it as a sequence of destructive calls without confirming the
changed semantics. For an in-place batch update of existing Base field schema,
use public `mbs column batch-update` only after inspecting its installed help;
it is not a substitute for a whole-schema replacement, field deletion, or data
migration.

## Execution order

1. Run `mbs --version` and `mbs --help` once at the start of a session; trust the local CLI over remembered examples.
2. `mbs <group> <command> --help` when flags are unclear.
3. [references/cli-commands.md](references/cli-commands.md) for runtime-help-first operational guidance.
4. Topic reference below for semantics, edge cases, and uncovered CLI gaps.

## Critical rules

- **Runtime help is authoritative.** Use the public groups and commands listed
  by `mbs --help` and the relevant parent `--help`; do not hard-code a full
  command map here.
- **Model before mutation.** Inspect the workbook and list worksheets before
  choosing Sheet-range, table-record, Base-field, or SQL workflows.
- **No hidden compatibility generation.** Never generate an operation absent
  from parent help for a new workflow, including old `excel-*`, `base-table`,
  `db-table`, `sheet`, top-level `style`, `worksheet image`, and nested
  `cell note` entry points.
- **Formula and notes.** Use `formula set` for formula writes and `range note
  read|set|clear` for Sheet notes. `range lineage` takes `--range`, not `--cell`.
- **Workbook deletion lifecycle.** When the user asks to delete a workbook but
  does not explicitly request a recoverable deletion, use
  `mbs workbook delete --yes`; the CLI defaults to physical `purge`. Run the
  corresponding `--dry-run` first. Use
  `--mode mark --yes` only when the user explicitly asks for mark deletion,
  recovery, or 7-day retention. Both modes use the workbook lifecycle API;
  never use the legacy file-delete route.
- **Clear versus replace.** Use public `table clear --target "$BASE_TABLE" --yes --verify`
  to remove all Base records while preserving fields/schema; use `--dry-run`
  before destructive execution. `table insert` and `table update` do not
  provide atomic whole-table replacement semantics. Use
  `column batch-update` for a supported in-place batch update of existing Base
  field metadata; resource style config alone does not imply that capability.
- **Verification.** Use `--dry-run` before destructive or unfamiliar writes;
  preserve `--expected-revision`/`--idempotency-key` when required; use
  `--verify` and target-appropriate readback after mutation.
- **Base inspection.** `table inspect` addresses one Base table by `tid` or
  `table` name. Its canonical result may include matched worksheet dimensions;
  use `table schema` and `table read` for fields and records.
- **Complete table reads.** `table read` defaults to 1000 rows (maximum
  5000), so a command without `--all` is only a bounded read. Use `--all`
  with `--frame-out` for a complete export. The CLI follows a cursor or, when
  the backend returns `has_more: true` without one, advances by the page's
  actual record count. A full page with no cursor, `has_more`, total, or
  completion proof is a `backend.pagination_contract` error, not a completed
  export. See [references/cli-commands.md](references/cli-commands.md).
- **Images and SQL.** Use `mbs image` for public image operations. Use `sql
  materialize` for public Base-table materialization and `sql config` /
  `sql overwrite` only when their runtime help matches the requested target.

## Task routing

| Task | Start here |
|------|------------|
| Command flags and examples | [references/cli-commands.md](references/cli-commands.md) |
| Read/write targeting and API choice | [references/read-write.md](references/read-write.md) |
| Base record/field/formula verification | [references/base-mode-verification.md](references/base-mode-verification.md) |
| Upload, export, sharing | [references/file-management.md](references/file-management.md) |
| Workbook semantic overview | [references/workbook-profile.md](references/workbook-profile.md) |
| Sharing and permissions | [references/permission-sharing.md](references/permission-sharing.md) |
| Formulas and SQL result sheets | [references/formulas-sql.md](references/formulas-sql.md) |
| Pivot tables and pivot config specs | [references/pivot-tables.md](references/pivot-tables.md) |
| Formula dependency tracing | [references/lineage-trace.md](references/lineage-trace.md) |
| Charts, images, dashboards, worksheet styling | [references/charts-formatting.md](references/charts-formatting.md) |
| Merge/unmerge cells, cell notes, Base record notes | [references/charts-formatting.md](references/charts-formatting.md) |
| Sharing and permissions | [references/permission-sharing.md](references/permission-sharing.md) |
| Failures and recovery | [references/errors-recovery.md](references/errors-recovery.md) |
| Clickable cell refs in answers | [references/clickable-refs.md](references/clickable-refs.md) |
| Legacy SQL formula migration/showcase | [references/sql-formula-showcase.md](references/sql-formula-showcase.md) |

## Workflows

### Inspect a workbook

```
- [ ] `mbs workbook inspect` and `mbs worksheet list`
- [ ] identify worksheet name, table id, or Base table name
- [ ] read sample with --output table
```

```bash
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output table
mbs range read --doc-id <DOC_ID> --worksheet-name <SHEET> --output table
mbs range read --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:D20 --output table
```

### Delete a workbook

The `mbs` command defaults to physical `purge`, reclaiming the workbook's
storage unless the user explicitly requests recoverability. Inspect the target
and preview the physical deletion before sending it:

```bash
mbs workbook inspect --target "$WORKBOOK"
mbs workbook delete --target "$WORKBOOK" --dry-run
mbs workbook delete --target "$WORKBOOK" --yes
```

Use a mark deletion only when the user explicitly wants the 7-day recovery
window:

```bash
mbs workbook delete --target "$WORKBOOK" --mode mark --yes
```

### Upload and inspect

```
- [ ] workbook import
- [ ] capture document_id from JSON output
- [ ] use import stdout plus `--verify` as creation evidence
- [ ] if needed, resolve and sample one representative Base table per family
```

```bash
# Small workbook-style files
mbs workbook import ./file.xlsx --verify
mbs workbook import ./orders.csv --engine base
mbs workbook import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --engine sheet
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output table

# Large table-like files
mbs workbook import ./file.xlsx --engine base --verify
mbs table inspect --doc-id <DOC_ID> --table-name <REPRESENTATIVE_TABLE_NAME> --output json
mbs table sample --doc-id <DOC_ID> --table-id <TABLE_ID> --limit 2 --output table

# Cross-workbook worksheet -> raw Base-backed surface import
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --verify
mbs worksheet import --strategy create --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "1店" --source-worksheet-name "2店" --verify

# Sheet only: replace existing worksheet rows from JSON while keeping headers.
# For Base records, use public `mbs table insert` / `mbs table update` after checking their help.
mbs worksheet import ./rows.json --strategy replace --doc-id <TARGET_DOC_ID> --worksheet-name Students --verify

# Native Maybe Sheet worksheet import; engine is detected per worksheet
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --source-worksheet-name "工作表3" --source-worksheet-name "工作簿1" --verify
mbs worksheet import --strategy create --transfer-mode native --doc-id <TARGET_DOC_ID> --source-doc-id <SOURCE_DOC_ID> --verify

# Append source worksheets/tabs into an existing workbook
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --engine sheet --verify
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --target-worksheet-name "联盟导入" --engine sheet --verify
mbs worksheet import ./file.xlsx --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "联盟" --source-worksheet-name "订单" --engine base --verify
mbs worksheet import ./orders.csv --strategy create --doc-id <TARGET_DOC_ID> --engine base --verify
mbs worksheet import "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=0" --strategy create --doc-id <TARGET_DOC_ID> --source-worksheet-name "1店" --target-worksheet-name "Store 1" --engine sheet --verify
```

Do not follow successful raw-surface imports with per-table `schema` / `sample` / `read` loops. See [references/file-management.md](references/file-management.md) for engine choice and Base Mode verification.

### Convert a worksheet to Base

```
- [ ] inspect `worksheet list` and select exactly one Sheet-backed worksheet
- [ ] run `convert-to-base --dry-run` with `--gid` or `--worksheet-name`
- [ ] execute the reviewed conversion with `--yes --verify`
- [ ] retain old Sheet-engine source cells only when explicitly requested
```

```bash
# The workbook URL can provide both document ID and gid.
mbs worksheet convert-to-base \
  --url "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>" \
  --dry-run

# Execute after reviewing the dry run. Source cells are scrubbed by default.
mbs worksheet convert-to-base \
  --doc-id <DOC_ID> \
  --worksheet-name Orders \
  --yes \
  --verify

# Keep the prior Sheet-engine cell content only when required.
mbs worksheet convert-to-base \
  --doc-id <DOC_ID> \
  --gid <GID> \
  --keep-sheet-source \
  --yes \
  --verify
```

Use `--recalculate` when the converted Base worksheet should recalculate
immediately. Do not combine `--dry-run` with `--verify`. The command checks
metadata during `--verify` and succeeds only when the selected worksheet
reports `data_engine: base`.

### Dashboard execution

```
- [ ] `mbs --version` and relevant `--help`
- [ ] import with `--engine auto` or an explicit worksheet-index engine list
- [ ] `worksheet list` verifies Data_* Base Mode and Dashboard/summary Sheet mode where intended
- [ ] `dashboard validate --spec dashboard.json`
- [ ] `dashboard refresh --dry-run` checks payload shape before mutation
- [ ] execute `dashboard refresh`; if batch errors persist, use per-chart `chart create-config`
- [ ] `dashboard manifest` and `chart list` verify persisted metadata
- [ ] read source Data_* sheets and run browser/vision verification when logged-in canvas access exists
```

See [references/charts-formatting.md](references/charts-formatting.md) for chart spec shapes, fallback, and verification limits.

### Dashboard template export

Use this only when the user wants to promote an existing Maybe Sheet HTML dashboard worksheet into a reusable template package. The dashboard canvas must be a `sheet` worksheet, and the worksheet should contain exactly one persisted `chart.type=html` dashboard chart unless `--chart-id` or `--cell` is provided.

```bash
mbs dashboard export-template \
  --doc-id <DOC_ID> \
  --worksheet-name <DASHBOARD_WORKSHEET> \
  --template-id <template-id> \
  --out-dir <analysis-style-system-skill-dir>/dashboard-templates/<template-id> \
  --force
```

The command writes `template.json`, `html/dashboard.template.html`, and `html/runtime-payload.schema.json`. After export, switch to `analysis-style-system` and run `node scripts/validate_dashboard_html_template.mjs --template-dir dashboard-templates/<template-id>` before using or publishing the template skill.

### Sync rows by key

Choose the model first. For a Base table, use public `table update` with a
stable key and an explicit input frame. The public command surface has no
generic Sheet key-merge primitive: reconcile the data before a `range write`,
or report the capability gap rather than invoking a hidden Sheet upsert alias.

```
- [ ] inspect workbook and worksheet identities
- [ ] confirm the stable Base record key, or explicitly approve Sheet overwrite semantics
- [ ] use `table update --key ...` only for a Base/table target
- [ ] recalculate Sheet formulas if downstream formulas exist
- [ ] read back the target
```

```bash
mbs formula recalculate --doc-id <DOC_ID> --worksheet-name <SHEET>
```

### SQL result sheet

```
- [ ] headers + read sample on source sheet
- [ ] save raw SQL with `mbs sql config set`
- [ ] use `mbs sql materialize` for a public Base-table materialization, or `mbs sql overwrite` only when the target is a SQL-config worksheet
- [ ] read the materialized target
- [ ] scan the worksheet with `range inspect`
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
mbs range read --doc-id <DOC_ID> --worksheet-name PivotResult --range A1:H30 --output table
```

See [references/pivot-tables.md](references/pivot-tables.md).

### Trace formula lineage

```bash
mbs formula lineage --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>" --cell E2 --format tree --output yaml
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

If `mbs share visibility` returns 403 with an owner-only message, classify it as `owner_permission_required` / `permission_skipped`. If `workbook inspect` already shows the requested public/editor or public/viewer visibility, report it as a share warning rather than a dashboard failure; otherwise ask the owner or service account to update visibility. See [references/permission-sharing.md](references/permission-sharing.md) for owner requirements and access rules.

## Boundaries

- **Dashboard/chart layout** -> use `sheet-dashboard`, not this skill
- **Uncovered CLI gaps** -> check current `mbs --help` for a supported command
- **Clickable refs** -> only confirmed locations; see [references/clickable-refs.md](references/clickable-refs.md)

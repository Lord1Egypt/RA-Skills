# Charts and Formatting Reference

## Contents

1. When to use this
2. Scope boundary
3. First-class mbs coverage
4. Styling and freezing
5. Minimal report-polish flow

## 1. When to use this

Read this document when the task involves charts, pictures, frozen panes, cell styles, autofilter, or conditional formatting.

## 2. Scope boundary

This skill only covers worksheet-level `mbs` execution and media/styling operations.

Switch to `sheet-dashboard` when:

- chart composition is the main task
- dashboard layout and storytelling are the main task
- you need chart layout systems, visual systems, or dashboard workflows
- you need an agent to generate or swap a dashboard spec before execution

If you only need to:

- inspect existing chart metadata
- call low-level chart/image CRUD APIs
- bind a chart to an existing sheet

then this skill is sufficient.

Chart and picture editing is first-class in `mbs` for common worksheet
workflows. Use `mbs raw post` only when you already have a task-specific
payload for an uncovered operation.

## 3. First-class mbs coverage

CLI:

```bash
mbs chart list --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs chart get --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2
mbs chart create-config --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2 --spec chart.json
# Current CLI also accepts top-level `cell` in chart.json when --cell is omitted.
mbs chart update --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2 --chart-id rId1 --spec chart.json
mbs chart delete --doc-id <DOC_ID> --worksheet-name <SHEET> --chart-id rId1
```

Recommended authored `chart.json` shape:

```json
{
  "type": "json",
  "sql": "select Month, Revenue from Sheet1",
  "title": "Monthly Revenue",
  "hide_title": true,
  "legend": "bottom",
  "html": "{ library: 'echarts', handler: (data) => ({ xAxis: { type: 'category', data: data.map(r => r.Month) }, yAxis: { type: 'value' }, series: [{ type: 'line', data: data.map(r => Number(r.Revenue) || 0) }] }) }",
  "spec": {
    "style": {
      "title": "Monthly Revenue",
      "showContainerTitle": false
    }
  }
}
```

Alternate single-chart item shape accepted by recent CLI versions:

```json
{
  "cell": "B2",
  "chart": {
    "type": "json",
    "sql": "select Month, Revenue from Sheet1",
    "title": "Monthly Revenue",
    "html": "{ library: 'echarts', handler: (data) => ({ series: [{ type: 'line', data: data.map(r => Number(String(r.Revenue || '').replace(/,/g, '')) || 0) }] }) }"
  }
}
```

Important chart authoring rule:

- Prefer top-level `chart.type = "json"` for authored `mbs` specs.
- Put the actual ECharts or Highcharts renderer logic in `chart.html`.
- For `chart create-config`, the backend request is `{cell, chart}`. If you include `cell` in the spec, keep it top-level; do not nest a second `chart.chart`.
- Do not push `chart.type = "line"`, `"bar"`, or `"pie"` as the default authored pattern in `mbs` docs or skills.
- Treat those simple aliases as low-level backend-supported forms, not the primary recommendation.
- If the chart should keep metadata `title` but hide the visible container title, prefer `hide_title: true` or explicit `spec.style.showContainerTitle: false`.
- Do not rely on `title: ""` as the primary authored pattern for non-filter charts. Keep `chart.title` for metadata and hide the container title instead.
- If `chart.html` already draws its own visible title/header, also set `spec.style.showContainerTitle: false` to avoid duplicate titles.

Images:

```bash
mbs workbook inspect --doc-id <DOC_ID> --output json
mbs worksheet list --doc-id <DOC_ID> --output json
mbs image list --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs image read --doc-id <DOC_ID> --worksheet-name <SHEET> --cell A1 --out logo.png
mbs image insert --doc-id <DOC_ID> --worksheet-name <SHEET> --cell B3 --file logo.png --format picture-format.json
mbs image set --doc-id <DOC_ID> --worksheet-name <SHEET> --old-cell B3 --cell B3 --format picture-format.json --width 120 --height 91
mbs image replace --doc-id <DOC_ID> --worksheet-name <SHEET> --cell B3 --file logo_v2.png --format picture-format.json
mbs image delete --doc-id <DOC_ID> --worksheet-name <SHEET> --cell A1
mbs media check --doc-id <DOC_ID> --worksheet-name <SHEET>
```

Picture format uses the chart-compatible floating-object anchor model:

```json
{
  "from": {"col": 1, "row": 2, "col_off": 0, "row_off": 0},
  "to": {"col": 4, "row": 10, "col_off": 0, "row_off": 0}
}
```

Use zero-based row/column indexes in `from` and `to`. The `--cell` value is the
anchor used by the command, but persisted layout depends on picture `format`
and dimensions. Do not model worksheet images as cell values.

Engine preflight:

- Run `workbook inspect` and `worksheet list` before inserting images.
- The target worksheet should be Sheet-backed, usually
  `data_engine=sheet` and `style_engine=sheet`.
- Base-only worksheets do not support `add_picture`. In a Base Mode workbook,
  `worksheet create` can create a Base-only empty worksheet, which image
  insert may later report as `sheet <name> does not exist`.
- If the user wants a new image canvas in an existing Base Mode workbook, create a
  small local blank `.xlsx` with the desired sheet name and import it:

```bash
mbs worksheet import --strategy create ./blank.xlsx --doc-id <DOC_ID> --engine sheet --source-worksheet-name <SHEET> --target-worksheet-name <SHEET> --verify
```

- If a Base-only placeholder was created only for the image task and cannot be
  used, delete that placeholder before importing the Excel worksheet.

Dashboard worksheet orchestration:

```bash
mbs dashboard validate --spec dashboard.json
mbs dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run
mbs dashboard manifest --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs dashboard create-config --doc-id <DOC_ID> --spec dashboard.json --create-worksheet
mbs dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
mbs dashboard export-template --doc-id <DOC_ID> --worksheet-name <SHEET> --template-id <template-id> --out-dir <analysis-style-system-skill-dir>/dashboard-templates/<template-id> --force
```

Guidance:

- when a dashboard is being designed from scratch, let `sheet-dashboard` generate `dashboard.json` first, then use the commands above to validate and write it
- when an existing HTML dashboard should become a reusable template, use `dashboard export-template`; the source worksheet must be a `sheet` worksheet, and the output package belongs under `analysis-style-system/dashboard-templates/<template-id>`
- if a dashboard spec uses `dashboard_style_pack`, keep `industry_style` and `dashboard_story` alongside it so `dashboard validate` can prove the style contract is complete
- `dashboard refresh --dry-run` is a hard step before mutation; inspect that each operation has `charts: [{cell, chart}]`, not `chart.chart`.
- Use `chart list` or `image list` first to inspect current worksheet inventory.
- Before editing an existing chart, confirm `chart_id`, the anchor cell, and the worksheet.
- `chart get` requires `--cell` or `--chart-id` and resolves locally from the listed chart inventory.
- When documenting or generating dashboard chart specs, prefer `type: "json"` entries there as well.
- For non-filter charts, keep `chart.title` in metadata and hide duplicate visible titles with `spec.style.showContainerTitle: false`.
- Dashboard chart specs should keep charts inside columns `B:N`.
- Dashboard chart specs should include `chart.format.from` and `chart.format.to`, and the outer `cell` should match `chart.format.from`.
- For vertically stacked dashboard charts that share horizontal space, leave at least 1 empty worksheet row between them.
- Images are floating objects like charts. For insert, move, resize, or replace workflows, include `--format picture-format.json` so x/y position, anchors, and size survive readback and frontend drag/resize.
- Images require an Sheet-backed worksheet. Do not insert pictures into Base-only
  worksheets; use an existing Excel sheet or import a blank `.xlsx` with
  `--engine sheet` to create one.
- `image list` should return enough metadata for frontend display and later updates: URL/media reference when available, anchor cell, picture id, extension, alt text, size, and chart-compatible position/format fields.
- `image set` updates an existing picture's anchor, position, size, alt text, scale, hyperlink, or format. Use it after a frontend drag/resize operation instead of reinserting the image.
- `image replace` inherits prior `alt_text` when `--alt-text` is omitted.
- `media check` verifies worksheet-level image/chart object presence after `add_picture`, image commands, chart commands, or dashboard refresh.
- `dashboard refresh` is upsert-only: matching charts are updated, missing charts are created, and unrelated existing charts are not deleted.
- If batch dashboard refresh/create-config returns a server-side or unsupported-route error, retry as per-chart calls:
  `mbs chart create-config --doc-id <DOC_ID> --worksheet-name Dashboard --cell <CELL> --spec <single_chart.json>`.
- `dashboard manifest`, `chart list`, `image list`, `media check`, and returned ids prove metadata persistence only. They do not prove the web canvas rendered successfully.
- For delivery, also verify source data reads for every chart SQL source. If logged-in browser access to the MaybeSheet canvas is available, use a screenshot/vision check for true render validation. Public unauthenticated viewer access may show a login wall instead of charts. For HTML dashboards, use `mbs dashboard render-probe --screenshot` when possible and read the output in tiers: `local_probe_passed` proves local runtime/data binding, `screenshot_verified` proves PNG capture, and `environment_blocked` with `playwright_unavailable` / `chromium_unavailable` means the environment needs `npm i -D playwright` and `npx playwright install chromium` before final visual proof.
- After `dashboard export-template`, switch to `analysis-style-system` and run `node scripts/validate_dashboard_html_template.mjs --template-dir dashboard-templates/<template-id>` before reusing or publishing the template.
- For KPI or chart handlers that consume formatted numeric strings, coerce defensively:
  `Number(String(value || '').replace(/,/g, '')) || 0`.

## 4. Styling and freezing

Prefer the resource-local canonical style layer for new work. The current CLI
registers `worksheet.style`, `table.style`, `range.style`, `row.style`, and
`column.style`; `table`, `row`, and `column` also expose public `config`
operations for resource-local configuration. `worksheet config` remains the behavior/view
command, while `worksheet config --style-spec` is the appearance alias and
cannot be combined with view options.

```bash
mbs worksheet style --target "$SHEET" --scope used-region --spec worksheet-style.json --verify
mbs worksheet config --target "$SHEET" --style-spec worksheet-style.json --verify
mbs table style --target "$SHEET_TABLE" --section header --spec table-style.json --verify
mbs range style --target "$SHEET" --range A1:G1 --spec header-style.json --verify
mbs row config --target "$SHEET" --rows 2:4 --spec row-style.json --verify
mbs column config --target "$SHEET" --columns B:D --spec column-style.json --verify
mbs column config --target "$BASE_TABLE" --field amount --spec column-style.json --verify
```

Selector and safety rules:

- `worksheet style --scope` accepts `used-region` or `entire-grid`; the latter
  requires `--yes` or `--dry-run`.
- `table style/config --section` accepts `all`, `header`, `body`, or `totals`.
- `range style` requires a bounded A1 `--range`; `row style/config` requires
  `--rows`.
- `column style/config` requires exactly one of `--columns` (Sheet) or
  `--field` (Base). It is a style operation, not a typed field-metadata
  editor. For Base schema work, inspect `mbs column --help`; use public
  `column batch-update --updates` for supported in-place updates to existing
  field metadata, and use individual public column operations for structural
  changes not covered by that update contract.

For advanced worksheet styling (for example conditional formats, filters, or
explicit dimensions), do not retain a static nested command list in this skill.
Inspect the installed public surface first:

```bash
mbs worksheet style --help
mbs worksheet style <PUBLIC_STYLE_OPERATION> --help
```

Generate only an operation shown by that parent help. Use `mbs worksheet
beautify --help` when the task is an agent-driven polish workflow rather than a
specific, user-defined style operation.

Important rules:

- Use `mbs worksheet beautify` for the default agent-friendly polish workflow. It
  inspects metadata first, applies Excel worksheet styling where appropriate,
  and applies Base-backed field formatter/style/header metadata through the
  native field update path when possible.
- For column names and schema, use only the public operations shown by
  `mbs column --help`, including `mbs column rename`, `mbs column insert
  --field-type`, and `mbs column batch-update --updates` for supported
  in-place batch changes to existing Base field metadata. For resource
  appearance, use `mbs column style` or public `mbs column config --spec`.
  Do not treat batch update as a whole-schema replacement or compose destructive
  delete/recreate sequences without an explicit migration decision.
- Base-backed table default freeze/filter/header config should be returned by the
  backend. Do not instruct the frontend to synthesize auto-filter or dark
  header backgrounds.
- `filter-values --column` takes a zero-based absolute column index. In `--range A1:G100`, `--column 2` targets column C.
- Even a single range should use `range_addresses: ["A1:G1"]`
- Keep style payloads small and explicit
- Prefer high-level style keys:
  - `format`
  - `bold`
  - `bg_color`
  - `font_color`
  - `font_size`
  - `font_family`
  - `horizontal`
  - `wrap_text`


Example `header_style.json` payload for `batch-set --style`:

```json
{
  "bold": true,
  "font_color": "#FFFFFF",
  "bg_color": "#173E56",
  "font_size": 12,
  "font_family": "Arial",
  "horizontal": "center",
  "wrap_text": true
}
```

## 5. Minimal report-polish flow

Use this when the user asks for something like “make it look more like a management report”, “improve readability”, or “style the header row”.

1. Write the data first.
2. For a general polish request, inspect `mbs worksheet beautify --help`.
3. For a specific worksheet-level style request, inspect `mbs worksheet style
   --help` and then the selected public child command's `--help`.
4. Use resource-local `range style`, `row style`, or `column style` when they
   preserve the requested scope.
5. Read the affected range to verify.

If the response includes:

```text
source_info.styles_ignored=true
```

you must explicitly tell the user that the current worksheet engine did not apply the styles. Do not claim the styling work is complete.

Use canonical resource-local style/config commands for the common appearance
path. Use `mbs worksheet style --help` only when the requested operation is
worksheet-level and not covered by those resource-local commands.
Use `mbs chart`, `image`, and `dashboard` for the first-class
worksheet media and orchestration workflows above.
Use `mbs raw post` only for uncovered chart/picture/style operations. Verify
with `mbs range read --output table`, `chart list`, or
`image list`.

## 6. Merge cells and cell notes / record notes

Use these when the user asks to merge/unmerge cells, attach a cell note (Excel
comment) on a Sheet worksheet, or add notes on Base table records.

### Merge / unmerge cells (Sheet worksheets)

```bash
mbs range merge --doc-id <doc_id> --worksheet-name Sheet1 --range A1:D1
mbs range unmerge --doc-id <doc_id> --worksheet-name Sheet1 --range A1:D1
```

Rules:

- `--range` must be a range (contains `:`); merge requires at least two cells.
- Unmerging a sub-range removes the whole containing merged region
  (Excel-compatible).
- Merged ranges are returned by `mbs range read` under
  `formatting.merged_cells`; do not manually compute display values for merged
  titles.

### Range notes (Excel comments, Sheet worksheets)

Use the canonical target-based `range note` commands with a Sheet target
containing worksheet identity (`gid` or an equivalent canonical target).

```bash
# Read notes from one cell or an A1 range
mbs range note read --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=0" --range B2:D4

# Set one note
mbs range note set --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=0" --range B2 --text "review this" --verify

# Clear one note
mbs range note clear --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=0" --range B2 --verify
```

Rules:

- `read` accepts one A1 cell or an A1 range.
- `set` and `clear` currently require a single A1 cell such as `B2`. The
  CLI `--text` interface emits a 1×1 matrix; do not claim that a multi-cell
  write is supported until it has a matching matrix input contract.
- `set`/`clear` are versioned worksheet writes, so preserve the returned
  revision and use `--expected-revision` when coordinating concurrent edits.
- Notes are stored as Excel comments inside the workbook and follow workbook
  version history.
- The historical flat `mbs cell note-get`, `mbs cell note-set`, and
  `mbs cell note-clear` forms may remain compatibility aliases. The nested
  `mbs cell note read|set|clear` forms were removed; do not generate either
  legacy form for new instructions.

### Base table record notes

Use canonical row-note commands with a Base table target:

```bash
mbs row note add --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" --record-id <RECORD_ID> --text "记得核对一下" --verify
mbs row note list --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" --record-id <RECORD_ID>
mbs row note update --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" --record-id <RECORD_ID> --note-id <NOTE_ID> --text "updated" --verify
mbs row note delete --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?tid=<TABLE_ID>" --record-id <RECORD_ID> --note-id <NOTE_ID> --yes --verify
```

Rules:

- Record notes are collaboration metadata on Base tables; they do **not**
  participate in version history / rollback.
- **Owner-only edit/delete**: only the note author (the API user's email/user id)
  can update or delete a note. When creating via CLI, omit `--author` (or pass
  your own email) so you remain the owner; a custom `--author` name is not the
  API user and cannot be edited/deleted through the API.
- The historical `mbs row note|note-list|note-update|note-delete`
  commands may remain available as compatibility aliases. Prefer canonical
  `mbs row note ...` commands in new workflows.

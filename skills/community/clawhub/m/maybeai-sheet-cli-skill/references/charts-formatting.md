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
mbs excel-worksheet chart list --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs excel-worksheet chart get --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2
mbs excel-worksheet chart create-config --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2 --spec chart.json
# Current CLI also accepts top-level `cell` in chart.json when --cell is omitted.
mbs excel-worksheet chart update --doc-id <DOC_ID> --worksheet-name <SHEET> --cell J2 --chart-id rId1 --spec chart.json
mbs excel-worksheet chart delete --doc-id <DOC_ID> --worksheet-name <SHEET> --chart-id rId1
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
mbs workbook list-worksheets --doc-id <DOC_ID> --output json
mbs excel-worksheet image list --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs excel-worksheet image read --doc-id <DOC_ID> --worksheet-name <SHEET> --cell A1 --out logo.png
mbs excel-worksheet image insert --doc-id <DOC_ID> --worksheet-name <SHEET> --cell B3 --file logo.png --format picture-format.json
mbs excel-worksheet image set --doc-id <DOC_ID> --worksheet-name <SHEET> --old-cell B3 --cell B3 --format picture-format.json --width 120 --height 91
mbs excel-worksheet image replace --doc-id <DOC_ID> --worksheet-name <SHEET> --cell B3 --file logo_v2.png --format picture-format.json
mbs excel-worksheet image delete --doc-id <DOC_ID> --worksheet-name <SHEET> --cell A1
mbs excel-worksheet media check --doc-id <DOC_ID> --worksheet-name <SHEET>
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

- Check `workbook list-worksheets --output json` before inserting images.
- The target worksheet should be Excelize-backed, usually
  `data_engine=excelize` and `style_engine=excelize`.
- PG-only worksheets do not support `add_picture`. In a PG workbook,
  `excel-worksheet create` can create a PG-only empty worksheet, which image
  insert may later report as `sheet <name> does not exist`.
- If the user wants a new image canvas in an existing PG workbook, create a
  small local blank `.xlsx` with the desired sheet name and import it:

```bash
mbs worksheet import --strategy create ./blank.xlsx --doc-id <DOC_ID> --engine excelize --source-worksheet-name <SHEET> --target-worksheet-name <SHEET> --verify
```

- If a PG-only placeholder was created only for the image task and cannot be
  used, delete that placeholder before importing the Excelize worksheet.

Dashboard worksheet orchestration:

```bash
mbs excel-worksheet dashboard validate --spec dashboard.json
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run
mbs excel-worksheet dashboard manifest --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs excel-worksheet dashboard create-config --doc-id <DOC_ID> --spec dashboard.json --create-worksheet
mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json
```

Guidance:

- when a dashboard is being designed from scratch, let `sheet-dashboard` generate `dashboard.json` first, then use the commands above to validate and write it
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
- Images require an Excelize worksheet. Do not insert pictures into PG-only
  worksheets; use an existing Excelize sheet or import a blank `.xlsx` with
  `--engine excelize` to create one.
- `image list` should return enough metadata for frontend display and later updates: URL/media reference when available, anchor cell, picture id, extension, alt text, size, and chart-compatible position/format fields.
- `image set` updates an existing picture's anchor, position, size, alt text, scale, hyperlink, or format. Use it after a frontend drag/resize operation instead of reinserting the image.
- `image replace` inherits prior `alt_text` when `--alt-text` is omitted.
- `media check` verifies worksheet-level image/chart object presence after `add_picture`, image commands, chart commands, or dashboard refresh.
- `dashboard refresh` is upsert-only: matching charts are updated, missing charts are created, and unrelated existing charts are not deleted.
- If batch dashboard refresh/create-config returns a server-side or unsupported-route error, retry as per-chart calls:
  `mbs excel-worksheet chart create-config --doc-id <DOC_ID> --worksheet-name Dashboard --cell <CELL> --spec <single_chart.json>`.
- `dashboard manifest`, `chart list`, `image list`, `media check`, and returned ids prove metadata persistence only. They do not prove the web canvas rendered successfully.
- For delivery, also verify source data reads for every chart SQL source. If logged-in browser access to the MaybeSheet canvas is available, use a screenshot/vision check for true render validation. Public unauthenticated viewer access may show a login wall instead of charts.
- For KPI or chart handlers that consume formatted numeric strings, coerce defensively:
  `Number(String(value || '').replace(/,/g, '')) || 0`.

## 4. Styling and freezing

CLI:

```bash
mbs excel-worksheet style freeze-panes --doc-id <DOC_ID> --worksheet-name <SHEET> --cell B2
mbs excel-worksheet style cell batch-set --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:G1 --style header_style.json
mbs excel-worksheet style auto-filter set --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:G100
mbs excel-worksheet style auto-filter remove --doc-id <DOC_ID> --worksheet-name <SHEET>
mbs excel-worksheet style gridlines toggle --doc-id <DOC_ID> --worksheet-name <SHEET> --show-gridlines false
mbs excel-worksheet style filter-values --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:G100 --column 2 --already-checked Closed
mbs excel-worksheet style conditional-formats set --doc-id <DOC_ID> --worksheet-name <SHEET> --spec conditional_formats.json
mbs excel-worksheet style columns-width --doc-id <DOC_ID> --worksheet-name <SHEET> --start-column B --end-column D --width 120
mbs excel-worksheet style rows-height --doc-id <DOC_ID> --worksheet-name <SHEET> --start-row 1 --end-row 1 --height 28
mbs excel-worksheet style worksheet plan --doc-id <DOC_ID> --worksheet-name <SHEET> --mode auto_detect --spec worksheet_style.json
mbs excel-worksheet style worksheet apply --doc-id <DOC_ID> --worksheet-name <SHEET> --mode auto_detect --spec worksheet_style.json
mbs style beautify --doc-id <DOC_ID> --worksheet-name <SHEET> --dry-run --output json
mbs style beautify --doc-id <DOC_ID> --worksheet-name <SHEET> --output json
mbs db-table field batch-update --doc-id <DOC_ID> --name <PG_TABLE_NAME> --updates field-updates.json --verify
```

Important rules:

- Use `mbs style beautify` for the default agent-friendly polish workflow. It
  inspects metadata first, applies Excelize worksheet styling where appropriate,
  and applies PG/SheetTable field formatter/style/header metadata through the
  batch field update path when possible.
- For explicit PG/SheetTable field styles, use `db-table field batch-update`
  with a JSON array. Verify with `excel-worksheet read --output json` and look
  for `formatting.frozen_rows`, `formatting.auto_filter`, and
  `db_table.fields[*].property`.
- PG/db-table default freeze/filter/header config should be returned by the
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
  - `horizontal`
  - `wrap_text`

## 5. Minimal report-polish flow

Use this when the user asks for something like “make it look more like a management report”, “improve readability”, or “style the header row”.

1. Write the data first
2. `mbs excel-worksheet style freeze-panes`
3. `mbs excel-worksheet style cell batch-set` for header styling
4. `mbs excel-worksheet style cell batch-set` for highlighted rows or totals
5. `mbs excel-worksheet style columns-width` / `mbs excel-worksheet style rows-height`
6. Optionally `mbs excel-worksheet style auto-filter set`
7. `mbs excel-worksheet range read` to verify

If the response includes:

```text
source_info.styles_ignored=true
```

you must explicitly tell the user that the current worksheet engine did not apply the styles. Do not claim the styling work is complete.

Use `mbs excel-worksheet style` for worksheet styling.
Use `mbs excel-worksheet chart`, `image`, and `dashboard` for the first-class
worksheet media and orchestration workflows above.
Use `mbs raw post` only for uncovered chart/picture/style operations. Verify
with `mbs excel-worksheet range read --output table`, `chart list`, or
`image list`.

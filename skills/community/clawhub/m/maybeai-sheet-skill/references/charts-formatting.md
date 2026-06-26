# Charts and Formatting Reference

## Contents

1. When to use this
2. Chart scope
3. Low-level chart and picture APIs
4. Styling and freezing
5. Minimal report-polish flow

## 1. When to use this

Read this document when the task involves low-level chart APIs, pictures, frozen panes, cell styles, autofilter, or conditional formatting.

## 2. Chart scope

This skill only covers low-level spreadsheet capabilities and low-level chart APIs.

Switch to `sheet-dashboard` when:

- chart composition is the main task
- dashboard layout and storytelling are the main task
- you need chart layout systems, visual systems, or dashboard workflows

If you only need to:

- inspect existing chart metadata
- call low-level add/set/delete chart APIs
- bind a chart to an existing sheet

then this skill is sufficient.

Script: `scripts/07-charts-pictures.sh`

## 3. Low-level chart and picture APIs

Related endpoints:

```text
POST /api/v1/excel/add_chart
POST /api/v1/excel/set_chart
POST /api/v1/excel/delete_chart
POST /api/v1/excel/add_picture
POST /api/v1/excel/read_picture
POST /api/v1/excel/delete_picture
```

Guidance:

- Use `read_sheet` first to inspect `formatting.charts` and `formatting.pictures`
- Before editing an existing chart, confirm `chart_id`, the anchor cell, and the worksheet

## 4. Styling and freezing

Core endpoints:

```text
POST /api/v1/excel/freeze_panes
POST /api/v1/excel/batch_set_cell_style
POST /api/v1/excel/set_auto_filter
POST /api/v1/excel/remove_auto_filter
POST /api/v1/excel/set_conditional_formats
POST /api/v1/excel/set_columns_width
POST /api/v1/excel/set_rows_height
```

Important rules:

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
2. `freeze_panes`
3. `batch_set_cell_style` for header styling
4. `batch_set_cell_style` for highlighted rows or totals
5. `set_columns_width` / `set_rows_height`
6. Optionally `set_auto_filter`
7. `read_sheet` to verify

If the response includes:

```text
source_info.styles_ignored=true
```

you must explicitly tell the user that the current worksheet engine did not apply the styles. Do not claim the styling work is complete.

Scripts:

- `scripts/07-charts-pictures.sh`
- `scripts/08-formatting.sh`

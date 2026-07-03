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

### Read a full sheet or a range

```text
POST /api/v1/excel/read_sheet
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

### Read headers

```text
POST /api/v1/excel/read_headers
```

Use it to:

- get the schema quickly
- confirm column names before writing SQL

### List worksheets and versions

```text
POST /api/v1/excel/list_worksheets
POST /api/v1/excel/list_worksheets_version
POST /api/v1/excel/list_versions
POST /api/v1/excel/read_version
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

Value handling:

- `update_range` defaults to `RAW`; numeric-looking strings such as `"5.53%"` and `"9,007,000"` stay strings.
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

Related endpoints:

```text
POST /api/v1/excel/insert_rows
POST /api/v1/excel/delete_rows
POST /api/v1/excel/move_row
POST /api/v1/excel/move_rows
POST /api/v1/excel/undo_delete_rows
POST /api/v1/excel/insert_columns
POST /api/v1/excel/delete_columns
POST /api/v1/excel/move_column
POST /api/v1/excel/move_columns
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
POST /api/v1/excel/write_new_worksheet
POST /api/v1/excel/delete_worksheet
POST /api/v1/excel/rename_worksheet
POST /api/v1/excel/move_worksheet
POST /api/v1/excel/copy_worksheet
```

Guidance:

- When creating a new report sheet, write data first and style it separately
- Before deleting a worksheet, confirm the `gid` or sheet name to avoid deleting the wrong sheet

## 7. Post-write verification

Do at least one of the following:

- `read_sheet`
- `read_headers`
- `list_worksheets`

Strongly recommended after:

- `update_data_keep_headers`
- `update_range_by_lookup`
- writes to non-first worksheets
- `write_new_worksheet`

Related scripts:

- `scripts/02-read-data.sh`
- `scripts/03-write-data.sh`
- `scripts/04-rows-columns.sh`
- `scripts/05-worksheets.sh`

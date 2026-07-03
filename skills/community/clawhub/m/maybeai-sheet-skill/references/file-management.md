# File Management Reference

## Contents

1. When to use this
2. Basic conventions
3. Engine selection
4. Core endpoints
5. Sharing and permissions
6. Recommended flows

## 1. When to use this

Read this document when the task involves uploading, importing, searching, copying, renaming, deleting, sharing, or exporting MaybeAI spreadsheets.

## 2. Basic conventions

- Base URL: `https://play-be.omnimcp.ai`
- Auth header: `Authorization: Bearer <MAYBEAI_API_TOKEN>`
- Most follow-up requests use:

```text
https://www.maybe.ai/docs/spreadsheets/d/<document_id>
```

- After upload succeeds, record:
  - `document_id`
  - `uri`

## 3. Engine selection

MaybeAI Sheet uses Playground as the product-level router. It can create workbooks in different engines:

- `excelize`: workbook-style runtime for Excel layout, styles, formulas, merged cells, and workbook semantics.
- `postgres` / `pg`: SheetTable runtime for table-like data, SQL, large row counts, large cell counts, append/upsert, and PG-native reads/writes.

Best practice:

- If any worksheet has more than 10,000 rows, the workbook has more than 100,000 populated cells, or the file is mostly flat table data, import with `engine=postgres`.
- If the task depends on Excel-specific workbook fidelity, use the Excelize upload path and keep the dataset size modest.
- Avoid sending large table data through row-object JSON writes or `/api/v1/excel/upload`; that path can fail when the server expands the workbook into large in-memory payloads.
- After importing a large table file, call `list_worksheets` and confirm `engine: "pg"` or `data_engine: "pg"`.

## 4. Core endpoints

### Import a large table-like file into SheetTable/PG

```text
POST /api/v1/excel/import
```

Use this for large table-like `.xlsx` files: more than 10,000 rows in any worksheet, more than 100,000 populated cells across the workbook, or data shaped primarily as records.

```bash
curl -sS -X POST "$BASE_URL/api/v1/excel/import" \
  -H "Authorization: Bearer $MAYBEAI_API_TOKEN" \
  -F "engine=postgres" \
  -F "file=@/absolute/path/to/file.xlsx"
```

Expected success shape:

```json
{
  "success": true,
  "documentId": "<document_id>",
  "fileUri": "https://www.maybe.ai/docs/spreadsheets/d/<document_id>",
  "sheets": ["Sheet1"]
}
```

Verification:

```bash
curl -sS -X POST "$BASE_URL/api/v1/excel/list_worksheets" \
  -H "Authorization: Bearer $MAYBEAI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uri":"https://www.maybe.ai/docs/spreadsheets/d/<document_id>"}'
```

Confirm the response reports `engine: "pg"` or worksheet `data_engine: "pg"`.

### Upload a file

```text
POST /api/v1/excel/upload
```

Notes:

- `multipart/form-data`
- `file` is required
- `user_id` is optional and exists only as a compatibility field
- Use this for Excelize/workbook-style imports where layout, styles, formulas, merged cells, or workbook fidelity matter more than table scale

Script: `scripts/01-file-management.sh`

### Import from URL

```text
POST /api/v1/excel/import_by_url
```

Use this when you already have a public downloadable `.xlsx` URL.

### List or search files

```text
POST /api/v1/excel/list_files
POST /api/v1/excel/search_files
```

Use search when you need to find historical files by keyword.

### Rename, delete, or copy

```text
POST /api/v1/excel/rename_file
POST /api/v1/excel/delete_file
POST /api/v1/excel/copy_excel
```

These endpoints all operate on the same `uri`.

### Export

```text
GET /api/v1/excel/export/{document_id}
POST /api/v1/excel/download
```

Guidance:

- Prefer `export` when you want the `.xlsx` file directly
- Use `download` when you already have a `uri`

## 5. Sharing and permissions

### Visibility

```text
POST /api/v1/share/sheet/visibility
```

### Share with a specific user

```text
POST /api/v1/share/sheet/update-permission
```

### Inspect permissions

```text
POST /api/v1/share/sheet/list
POST /api/v1/share/sheet/permission
```

## 6. Recommended flows

### Bring a new file into the system

1. Inspect approximate row count and workbook intent
2. If table-like and rows > 10,000 or populated cells > 100,000, use `/api/v1/excel/import` with `engine=postgres`
3. Otherwise use `upload` or `import_by_url`
4. Record `document_id` and `uri`
5. `list_worksheets`
6. `read_headers` or a small `read_sheet`

### Bring a large table-like file into the system

1. `POST /api/v1/excel/import` with multipart `engine=postgres`
2. Record `document_id` and `uri`
3. `list_worksheets`
4. Confirm `engine: "pg"` or worksheet `data_engine: "pg"`
5. `read_headers` or a small `read_sheet`

### Export before delivery

1. Finish all writes
2. Read back the key ranges with `read_sheet`
3. `export` the final file

### Reuse a historical file

1. `search_files`
2. `copy_excel`
3. Edit the copy instead of the original

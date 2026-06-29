# File Management Reference

## Contents

1. When to use this
2. Basic conventions
3. Core endpoints
4. Sharing and permissions
5. Recommended flows

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

## 3. Core endpoints

### Upload a file

```text
POST /api/v1/excel/upload
```

Notes:

- `multipart/form-data`
- `file` is required
- `user_id` is optional and exists only as a compatibility field

CLI:

```bash
maybeai-sheet workbook create-from-file ./report.xlsx
```

For endpoints without a first-class command (import by URL, search, export, sharing), use `maybeai-sheet raw post <path> --body body.json`. See `references/cli-commands.md`.

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

## 4. Sharing and permissions

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

## 5. Recommended flows

### Bring a new file into the system

1. `maybeai-sheet workbook create-from-file ./file.xlsx`
2. Record `document_id` from JSON output
3. `maybeai-sheet sheet worksheets --doc-id <DOC_ID>`
4. `maybeai-sheet sheet headers` or `sheet read --output table`

### Export before delivery

1. Finish all writes
2. `maybeai-sheet sheet read --output table` on key ranges
3. `maybeai-sheet raw post /api/v1/excel/download --body export.json` or export endpoint

### Reuse a historical file

1. `raw post /api/v1/excel/search_files`
2. `raw post /api/v1/excel/copy_excel`
3. Edit the copy

# Workbook Profile Reference

## Contents

1. When to use this
2. What the endpoint does
3. Request
4. Response
5. Recommended workflows
6. Limitations and recovery

## 1. When to use this

Read this document when the task involves understanding an unfamiliar workbook, deciding which worksheets to inspect, summarizing workbook contents, or preparing a plan before detailed analysis.

Use this endpoint when the user asks:

- what a workbook contains
- which sheets are relevant
- where to start analyzing a multi-sheet workbook
- for a high-level workbook summary
- for a quick profile before writing SQL, formulas, or reports

Do not use this as a substitute for exact data extraction. After the profile identifies relevant worksheets, use `read_headers` and `read_sheet` for precise values.

## 2. What the endpoint does

```text
POST /api/v1/excel/workbook_profile
```

`workbook_profile` is a read-only workbook understanding endpoint.

It:

- accepts a `document_id` or MaybeAI spreadsheet `uri`
- works through the Excel V2 compatibility route at `/api/v1/excel/workbook_profile`
- supports Excel V2 registry workbooks and legacy Excelize fallback on the `/excel` compatibility path
- lists workbook worksheets internally
- reads non-empty sample rows from each worksheet
- sends compact worksheet samples to an LLM to generate a Chinese natural-language workbook summary
- caches the result in `excel_v2_workbook_profiles`
- returns the cached profile when the worksheet signature has not changed

The generated profile is useful for orientation, routing, and analysis planning. It should not be treated as a complete audit of every row.

## 3. Request

Headers:

```text
Authorization: Bearer <MAYBEAI_API_TOKEN>
Content-Type: application/json
```

Body:

```json
{
  "document_id": "<document_id>",
  "force_refresh": false
}
```

Alternative body:

```json
{
  "uri": "https://www.maybe.ai/docs/spreadsheets/d/<document_id>",
  "force_refresh": false
}
```

Fields:

- `document_id`: workbook document id. Required unless `uri` is provided.
- `uri`: MaybeAI spreadsheet URL or document id string. Required unless `document_id` is provided.
- `force_refresh`: optional boolean. Use `true` to rebuild the profile even when cache exists.
- `model`: optional model override. Leave unset by default; the service default is used.

Prefer `/api/v1/excel/workbook_profile` for skill usage because it includes legacy Excelize fallback. `/api/v1/excel_v2/workbook_profile` exists, but it does not use the same legacy fallback behavior.

## 4. Response

Typical shape:

```json
{
  "success": true,
  "document_id": "<document_id>",
  "cache_status": "hit",
  "profile": {
    "summary": "这个工作簿...",
    "worksheets": [
      {
        "gid": 0,
        "sheet_name": "订单",
        "data_engine": "pg",
        "sample_rows": [
          ["日期", "订单号"],
          ["2026-06-01", "SO-1"]
        ]
      }
    ],
    "worksheet_signature": [
      {
        "gid": 0,
        "sheet_name": "订单"
      }
    ],
    "generated_at": "2026-06-17T00:00:00+00:00"
  }
}
```

Important fields:

- `cache_status`: `hit`, `miss`, `stale`, or `refreshed`
- `profile.summary`: LLM-generated Chinese summary of workbook purpose, likely business scenario, key data objects, and metrics
- `profile.worksheets`: per-worksheet metadata and up to five sample non-empty rows returned to the caller
- `profile.worksheet_signature`: sheet identity used for cache freshness checks
- `profile.generated_at`: profile generation or refresh time

Cache behavior:

- `hit`: existing profile reused
- `miss`: no cached profile existed
- `stale`: worksheet signature changed, so the profile was rebuilt
- `refreshed`: caller forced a rebuild with `force_refresh: true`

## 5. Recommended workflows

### Understand an unfamiliar workbook

1. Call `workbook_profile`
2. Read `profile.summary`
3. Use `profile.worksheets[].sheet_name`, `gid`, and `sample_rows` to identify likely source sheets
4. Call `read_headers` or targeted `read_sheet` on the relevant worksheets
5. Continue with SQL, formulas, or report-building only after exact schema checks

### Plan a SQL result sheet

1. Call `workbook_profile` to understand sheet roles
2. Call `read_headers` on likely source worksheets
3. Optionally call `read_sheet` for representative rows
4. Draft SQL
5. `sql/compile`
6. `sql/write_result`

### Refresh profile after workbook changes

Use:

```json
{
  "document_id": "<document_id>",
  "force_refresh": true
}
```

Use this after:

- adding, deleting, or renaming worksheets
- materially changing worksheet schemas
- importing a new workbook over an existing document
- receiving a profile that appears stale

## 6. Limitations and recovery

Limitations:

- The summary is based on worksheet names and sample non-empty rows, not a full workbook scan
- Returned `sample_rows` are limited and intended for orientation
- Very wide rows are truncated internally before summarization
- The summary is generated in Chinese by the service prompt
- It requires viewer permission on the sheet

Recovery:

- `400 document_id or uri is required`: pass `document_id` or `uri`
- `403`: confirm `MAYBEAI_API_TOKEN` and sheet access
- profile seems stale: retry with `force_refresh: true`
- worksheet sample read errors: inspect the affected worksheet with `read_sheet`
- need exact values: use `read_headers` and `read_sheet`; do not rely only on `profile.summary`

Related script:

- `scripts/10-workbook-profile.sh`

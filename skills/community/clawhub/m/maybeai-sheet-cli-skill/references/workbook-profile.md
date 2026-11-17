# Workbook Profile Reference

## Contents

1. When to use this
2. What workbook metadata does
3. Request
4. Response
5. Recommended workflows
6. Limitations and recovery

## 1. When to use this

Read this document when the task involves understanding an unfamiliar workbook, deciding which worksheets to inspect, summarizing workbook contents, or preparing a plan before detailed analysis.

Use workbook metadata when the user asks:

- what a workbook contains
- which sheets are relevant
- where to start analyzing a multi-sheet workbook
- for a high-level workbook summary
- for a quick profile before writing SQL, formulas, or reports

Do not use this as a substitute for exact data extraction. After the profile identifies relevant worksheets, use `mbs excel-worksheet range read`, `mbs excel-table sample`, or `mbs db-table sample` for precise values.

## 2. What workbook metadata does

`mbs workbook metadata` is read-only workbook understanding.

It:

- accepts a `document_id` or MaybeAI spreadsheet `uri`
- lists workbook worksheets internally
- reads non-empty sample rows from each worksheet
- sends compact worksheet samples to an LLM to generate a Chinese natural-language workbook summary
- caches the result in `excel_v2_workbook_profiles`
- returns the cached profile when the worksheet signature has not changed

The generated profile is useful for orientation, routing, and analysis planning. It should not be treated as a complete audit of every row.

## 3. Request

Use:

```bash
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook metadata --url <MAYBE_SHEET_URL>
```

Fields:

- `document_id`: workbook document id. Required unless `uri` is provided.
- `uri`: MaybeAI spreadsheet URL or document id string. Required unless `document_id` is provided.
- Use `--url` when you already have a Maybe Sheet URL.
- Use `--doc-id` when you only have the workbook document id.

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

1. Call `mbs workbook metadata`
2. Read `profile.summary`
3. Use `profile.worksheets[].sheet_name`, `gid`, and `sample_rows` to identify likely source sheets
4. Call `mbs excel-worksheet range read`, `mbs excel-table schema`, or `mbs db-table schema` on the relevant targets
5. Continue with SQL, formulas, or report-building only after exact schema checks

### Plan a SQL result sheet

1. Call `mbs workbook metadata` to understand sheet roles
2. Call `mbs excel-table schema` or `mbs db-table schema` on likely source tables
3. Optionally call `mbs excel-worksheet range read`, `mbs excel-table sample`, or `mbs db-table sample` for representative rows
4. Draft SQL
5. Convert the SQL into a `=SQL("...")` formula
6. Use `mbs excel-worksheet range set-formula` on the report worksheet
7. Verify the spill result with `mbs excel-worksheet range read`

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
- profile seems stale: rerun `mbs workbook metadata`; if it remains stale, inspect exact sheets directly
- worksheet sample read errors: inspect the affected worksheet with `mbs excel-worksheet range read`
- need exact values: use `mbs excel-worksheet range read`, `mbs excel-table sample`, or `mbs db-table sample`; do not rely only on `profile.summary`

Related CLI:

```bash
mbs workbook metadata --doc-id <DOC_ID>
mbs workbook capabilities --doc-id <DOC_ID>
```

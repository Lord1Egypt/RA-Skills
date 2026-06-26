# ADP CLI Response Schema Reference

> This document defines the output structure of each command so that Agent can reliably parse results.

## Output Modes

The CLI has two output modes controlled by `--json` flag:
- **Human-readable** (default in TTY): colored text with formatting
- **JSON mode** (`--json` or non-TTY/pipe): structured JSON to stdout, errors to stderr

**Agent should always use `--json` flag** or pipe output to ensure machine-readable JSON.

---

## config get

```json
{
  "configured": true,
  "api_key_masked": "9ce0...ab4f",
  "api_base_url": "https://adp.laiye.com/"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `configured` | boolean | Whether API Key is configured |
| `api_key_masked` | string | Masked API Key (first 4 + last 4 chars) |
| `api_base_url` | string | Current API Base URL |

---

## app-id list

```json
[
  {
    "app_id": "61ac******bd21",
    "app_name": "Overseas Invoices/Receipts",
    "app_label": ["Invoice", "Receipt", "Bill"],
    "app_type": 1
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `app_id` | string | Application ID (use this for `--app-id`) |
| `app_name` | string | Application display name |
| `app_label` | string[] | Labels for matching user intent |
| `app_type` | int | 0:Out-of-the-box application(Pre-set);1:Custom application|

---

## credit

```json
{
  "credit_balance": 95.5
}
```

---

## parse (single file, sync)

Top-level response:

```json
{
  "code": "success",
  "message": "",
  "tips": null,
  "data": {
    "task_id": "",
    "file_url": "",
    "status": 4,
    "message": "",
    "doc_recognize_result": [...]
  }
}
```

### doc_recognize_result item

```json
{
  "page_num": 1,
  "document_content": "Full text content of this page...",
  "document_details": [
    {
      "type": "Text | Picture | Table",
      "text": "content or image URL",
      "position": [{"points": [{"x": 311, "y": 50}, ...]}],
      "ocr_confidence": {
        "ocr_mean_confidence": 0.999,
        "ocr_min_confidence": 0.998,
        "is_overall_confidence": 1
      }
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `page_num` | integer | Page number (1-indexed) |
| `document_content` | string | Full text of the page in reading order |
| `document_details` | array | Element-level details with position and confidence |
| `document_details[].type` | string | Element type: `Text`, `Picture`, or `Table` |
| `document_details[].text` | string | Text content, or image URL for Picture type |
| `document_details[].position` | array | Bounding box coordinates (4 corner points) |
| `document_details[].ocr_confidence.ocr_mean_confidence` | float | Average OCR confidence (0-1) |
| `document_details[].ocr_confidence.ocr_min_confidence` | float | Minimum OCR confidence (0-1) |

---

## extract (single file, sync)

Returns an array of extracted fields:

```json
[
  {
    "field_key": "invoice_number",
    "field_name": "Invoice Number",
    "field_values": [
      {
        "field_value": "24VLT0591617",
        "field_confidence": 1.0,
        "references": []
      }
    ]
  },
  {
    "field_key": "line_items",
    "field_name": "Product Details Table",
    "references": [],
    "field_confidence": 1.0,
    "table_values": [
      [
        {
          "field_name": "Description",
          "field_key": "line_items_description",
          "field_values": [
            {
              "field_value": "TESLA MODEL 3",
              "field_confidence": 1.0,
              "references": "Description: TESLA MODEL 3"
            }
          ]
        }
      ]
    ]
  }
]
```

### Field types

**Regular field** (no `table_values`):

| Field | Type | Description |
|-------|------|-------------|
| `field_key` | string | Machine-readable field identifier |
| `field_name` | string | Human-readable field name |
| `field_values` | array | Extracted values |
| `field_values[].field_value` | string | The extracted value |
| `field_values[].field_confidence` | float | Confidence score (0-1) |

**Table field** (has `table_values`):

| Field | Type | Description |
|-------|------|-------------|
| `field_key` | string | Table identifier (e.g., `line_items`) |
| `field_name` | string | Table name |
| `table_values` | array[array] | 2D array: rows of cells, each cell has `field_name`, `field_key`, `field_values` |

### How to distinguish field types

- If the field object contains `table_values` → it is a table field, read from `table_values`
- If the field object contains `field_values` without `table_values` → it is a regular field

---

## Async task submission (--async)

When using `--async` without `--no-wait`, the CLI polls until completion and returns the same response as sync mode.

When using `--async --no-wait`, the CLI returns immediately:

```json
{
  "task_id": "dffe****427d",
  "status": "PROCESSING"
}
```

---

## Async query (parse query / extract query)

```json
{
  "task_id": "dffe****427d",
  "status": "SUCCESS"
}
```

| Status | Meaning |
|--------|---------|
| `SUCCESS` | Task completed, result data included |
| `PROCESSING` | Still processing, query again later |
| `FAILED` | Task failed |

When status is `SUCCESS`, the full parse/extract result is included in the response.

---

## Batch Processing Output

### Sync batch (multiple files)

**stdout** outputs a summary JSON:

```json
{
  "total": 5,
  "success": 4,
  "failed": 1,
  "output_dir": "/absolute/path/to/adp_results_20260417_143025",
  "files": [
    {"input": "invoice1.pdf", "output": "invoice1.pdf.json", "status": "success"},
    {"input": "invoice2.pdf", "output": "invoice2.pdf.json", "status": "success"},
    {"input": "bad.pdf", "output": "bad.pdf.error.json", "status": "failed", "error": "..."}
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total` | integer | Total number of files processed |
| `success` | integer | Number of successful files |
| `failed` | integer | Number of failed files |
| `output_dir` | string | **Absolute path** to the output directory — Agent must read files from here |
| `files` | array | Per-file status and output filename |
| `files[].input` | string | Original input filename |
| `files[].output` | string | Output filename in `output_dir` |
| `files[].status` | string | `success` or `failed` |
| `files[].error` | string | Error message (only when failed) |

### Output directory structure

```
adp_results_20260417_143025/     (or --export specified path)
  ├── invoice1.pdf.json          # Successful result (same schema as single-file response)
  ├── invoice2.pdf.json
  ├── bad.pdf.error.json         # Failed result: {"input": "...", "status": "failed", "error": "..."}
  └── _summary.json              # Same content as stdout summary
```

**Agent workflow for batch results:**
1. Parse the stdout summary JSON
2. Read `output_dir` path from summary
3. For each file in `files` array where `status` is `success`:
   - Read `{output_dir}/{files[].output}` to get the individual result
   - The JSON structure inside each file is identical to the single-file parse/extract response
4. For failed files, the error reason is in both the summary and the `.error.json` file

### Default output directory

- If `--export` is specified: uses that path
- If `--export` is not specified: auto-creates `adp_results_{YYYYMMDD_HHMMSS}/` in current directory

### Async batch (--async --no-wait)

Returns a JSON array of task IDs:

```json
[
  {"path": "invoice1.pdf", "task_id": "abc123"},
  {"path": "invoice2.pdf", "task_id": "def456"},
  {"path": "bad.pdf", "error": "file too large"}
]
```

**Agent workflow for async batch:**
1. Save the output to a file (using `--export tasks.json`)
2. Later, query all tasks: `adp parse query --file tasks.json --watch`
3. The `--file` flag reads the JSON array and queries all task IDs

---

## custom-app create

```json
{
  "code": "success",
  "message": "",
  "tips": null,
  "data": {
    "app_id": "ed5195882cd311f19359627c0509427d",
    "app_name": "Custom Application Name",
    "app_label": ["Custom Label 1"],
    "config_version": "v1"
  }
}
```

---

## custom-app ai-generate

Returns AI-recommended extraction fields based on the sample document. The Agent can use these recommendations to populate `--extract-fields` when calling `custom-app create`.

---

## Error Response Format

When `--json` flag is used, errors are output to **stderr** as:

```json
{
  "type": "AUTH_ERROR",
  "message": "Authentication error: invalid API key",
  "fix": "Check your API key is correct and has not expired.",
  "retryable": false,
  "details": {"context": "extract"}
}
```

See [error-handling.md](error-handling.md) for the complete error type reference.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Parameter error |
| 3 | Resource not found |
| 4 | Permission denied |
| 5 | Conflict |
| 6 | Partial failure (batch: some succeeded, some failed) |

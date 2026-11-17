---
name: jsonl-validator
description: Validate JSONL files for broken lines, summarize counts, time ranges, and key distributions. Use when checking evolution logs, memory graph exports, or any line-delimited JSON data.
---

# JSONL Validator

Validate one JSONL file and report:
- valid/invalid line counts
- time range from `ts` fields, if present
- top JSON keys by frequency
- up to 5 invalid line examples

## Usage

```bash
node skills/jsonl-validator/scripts/validate-jsonl.js <path/to/file.jsonl>
```

Exit codes:
- `0` — all non-empty lines are valid JSON
- `2` — invalid JSON lines found
- `1` — usage or missing file error

## Notes

- This skill is read-only; it does not modify files.
- Large files are read fully into memory; for very large JSONL, prefer a streaming approach.

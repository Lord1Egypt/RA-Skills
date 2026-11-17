# Input contract

file: relative UTF-8 HTML path. table: zero-based index, default0. sourceUrl: optional provenance URL. Exports table.csv.

## Operational scope

Capture the page with an available browser first. This parser handles outer HTML tables, not nested-table fidelity, JavaScript grids or infinite scrolling. Do not claim the whole site was crawled.

## Fictional example

```json
{
  "file": "samples/table.html",
  "table": 0,
  "sourceUrl": "https://example.com/demo"
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

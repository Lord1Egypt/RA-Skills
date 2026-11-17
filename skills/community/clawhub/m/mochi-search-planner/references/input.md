# Input contract

query: nonempty string. sites: optional host-name list. exact: optional exact phrase. Returns raw and URL-encoded queries.

## Operational scope

Use the available search tool for actual results; the helper only plans queries. Verify current claims against original sources. Do not put private documents or credentials into public searches.

## Fictional example

```json
{
  "query": "Ubuntu runtime requirements",
  "sites": [
    "docs.openclaw.ai"
  ],
  "exact": "Node.js"
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

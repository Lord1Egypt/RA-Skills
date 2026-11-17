# Input contract

cases: unique id, actual string, and at least one of nonempty mustContain/mustNotContain or exact. Returns per-case results.

## Operational scope

These are deterministic assertions on supplied replies, not a semantic intelligence score. Generate realistic cases, keep held-out cases separate, and report model execution separately. Do not automatically rewrite agent instructions.

## Fictional example

```json
{
  "cases": [
    {
      "id": "timezone",
      "actual": "09:00 UTC",
      "mustContain": [
        "UTC"
      ],
      "mustNotContain": [
        "API_KEY"
      ]
    },
    {
      "id": "exact",
      "actual": "done",
      "exact": "done"
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

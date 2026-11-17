# Input contract

asOf: timezone-aware ISO timestamp. maxAgeDays: nonnegative integer. sources: id, url, publishedAt or updatedAt, optional eventDate.

## Operational scope

Publication dates and event dates differ. The helper evaluates provided dates, not factual truth or website changes. Browse the original source when a stale claim affects the answer.

## Fictional example

```json
{
  "asOf": "2026-10-27T00:00:00Z",
  "maxAgeDays": 30,
  "sources": [
    {
      "id": "a",
      "url": "https://example.com/a",
      "publishedAt": "2026-08-01T00:00:00Z"
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

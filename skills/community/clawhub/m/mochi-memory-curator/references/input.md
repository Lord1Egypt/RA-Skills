# Input contract

asOf: aware ISO timestamp. facts: key, value, source, optional expiresAt. Conflicts are not resolved automatically.

## Operational scope

Only include facts the user asked to retain. No chat sweeping, hooks or silent memory writes. Contradictory sources stay visible rather than being resolved by recency alone.

## Fictional example

```json
{
  "asOf": "2026-10-27T00:00:00Z",
  "facts": [
    {
      "key": "city",
      "value": "A",
      "source": "user note1"
    },
    {
      "key": "city",
      "value": "B",
      "source": "user note2"
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

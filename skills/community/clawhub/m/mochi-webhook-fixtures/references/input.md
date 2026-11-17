# Input contract

events: list of id and payload. First occurrence of an ID is retained. Exports fixtures.jsonl.

## Operational scope

Fixture deduplication is not a production idempotency store. Remove secrets and personal payloads before sharing fixtures. Real delivery requires a separately authorized destination and replay strategy.

## Fictional example

```json
{
  "events": [
    {
      "id": "one",
      "payload": {
        "n": 1
      }
    },
    {
      "id": "one",
      "payload": {
        "n": 1
      }
    },
    {
      "id": "two",
      "payload": {
        "n": 2
      }
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

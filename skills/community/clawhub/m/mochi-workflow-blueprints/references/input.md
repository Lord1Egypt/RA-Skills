# Input contract

steps: unique id, optional needs list and mutates boolean. Returns a topological execution order.

## Operational scope

A validated graph is not a running automation. Map each step to available tools, test with fixtures, and create schedules or external actions only when requested. Define retry limits and idempotency before repeated writes.

## Fictional example

```json
{
  "steps": [
    {
      "id": "collect"
    },
    {
      "id": "summarize",
      "needs": [
        "collect"
      ]
    },
    {
      "id": "send",
      "needs": [
        "summarize"
      ],
      "mutates": true
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

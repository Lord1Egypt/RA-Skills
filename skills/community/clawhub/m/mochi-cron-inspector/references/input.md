# Input contract

expression: five fields; supports numbers, ranges, lists, star and steps. timezone: IANA name. after: aware ISO time. count:1..20. Search bounded to366days.

## Operational scope

This is a preview, not a scheduler. Named months/weekdays, macros and seconds are unsupported. Day-of-month and weekday use POSIX OR semantics when both are restricted. Native schedulers can differ; verify the actual scheduler before activation.

## Fictional example

```json
{
  "expression": "0 9 * * 1-5",
  "timezone": "UTC",
  "after": "2026-10-26T08:59:00Z",
  "count": 2
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.

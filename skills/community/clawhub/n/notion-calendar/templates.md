# Reusable Payload Templates

Use templates only after the target schema is verified.

## Scheduled Item

```json
{
  "Name": {
    "title": [
      {"text": {"content": "Launch review"}}
    ]
  },
  "Date": {
    "date": {"start": "2026-03-15T09:00:00+01:00"}
  },
  "Status": {
    "status": {"name": "Scheduled"}
  }
}
```

## All-Day Item

```json
{
  "Name": {
    "title": [
      {"text": {"content": "Publishing freeze"}}
    ]
  },
  "Date": {
    "date": {"start": "2026-03-22", "end": "2026-03-23"}
  }
}
```

## Rule

Rename properties to match the live schema before sending any payload.

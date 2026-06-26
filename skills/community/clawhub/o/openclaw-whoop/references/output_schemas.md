# Normalized output schema (stable contract)

`scripts/whoop_normalize.py` converts raw WHOOP API responses into a stable JSON shape so downstream prompts and integrations don’t break when WHOOP adds fields.

## Top-level

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "profile": {
    "name": "string|null",
    "email": "string|null"
  },
  "recovery": {
    "score": "number|null",
    "hrv_ms": "number|null",
    "rhr_bpm": "number|null"
  },
  "sleep": {
    "duration_minutes": "number|null",
    "performance_percent": "number|null"
  },
  "cycle": {
    "strain": "number|null",
    "avg_hr_bpm": "number|null"
  },
  "workout": {
    "count": "number",
    "top_strain": "number|null"
  },
  "source": {
    "whoop": {
      "api_base": "string",
      "raw_files": ["string"]
    }
  }
}
```

Notes:
- Fields may be `null` if missing, unavailable, or scope not granted.
- Keep this schema conservative; add fields only when stable and widely useful.

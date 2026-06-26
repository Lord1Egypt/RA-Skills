# Output schema (for Wellness hub)

`fitbit_normalize_daily.py` outputs:

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "sleep": {
    "duration_minutes": "number|null",
    "score": "number|null",
    "source": "fitbit"
  },
  "activity": {
    "steps": "number|null",
    "distance_km": "number|null",
    "source": "fitbit"
  },
  "sources_present": ["fitbit"],
  "source": {"raw_files": ["string"]}
}
```

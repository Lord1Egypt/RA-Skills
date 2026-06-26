# Output schema (for Wellness hub)

`oura_normalize_daily.py` outputs:

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "sleep": {
    "duration_minutes": "number|null",
    "efficiency": "number|null",
    "score": "number|null",
    "source": "oura"
  },
  "recovery": {
    "score": "number|null",
    "source": "oura"
  },
  "activity": {
    "steps": "number|null",
    "active_calories_kcal": "number|null",
    "source": "oura"
  },
  "sources_present": ["oura"],
  "source": {"raw_files": ["string"]}
}
```

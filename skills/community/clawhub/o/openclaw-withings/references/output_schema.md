# Output schema (for Wellness hub)

`withings_normalize_daily.py` outputs:

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "sleep": {
    "duration_minutes": "number|null",
    "score": "number|null",
    "source": "withings"
  },
  "body": {
    "weight_kg": "number|null",
    "body_fat_percent": "number|null",
    "source": "withings"
  },
  "vitals": {
    "bp_systolic": "number|null",
    "bp_diastolic": "number|null",
    "resting_hr_bpm": "number|null",
    "source": "withings"
  },
  "sources_present": ["withings"],
  "source": {"raw_files": ["string"]}
}
```

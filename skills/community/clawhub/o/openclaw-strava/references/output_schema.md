# Output schema (for Wellness hub)

`strava_normalize_daily.py` outputs:

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "training": {
    "workouts": [
      {
        "start": "ISO-8601|null",
        "end": "ISO-8601|null",
        "type": "string",
        "duration_minutes": "number|null",
        "distance_km": "number|null",
        "calories_kcal": "number|null",
        "avg_hr_bpm": "number|null",
        "max_hr_bpm": "number|null",
        "source": "strava"
      }
    ],
    "source": "strava"
  },
  "sources_present": ["strava"],
  "source": {"raw_files": ["string"]}
}
```

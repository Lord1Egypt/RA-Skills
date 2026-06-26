# Weekly Summary Schema (v0.2)

`weekly_report.py` writes:

- `data/weekly-summary.json`
- `data/weekly-summary.txt`

## JSON shape

```json
{
  "generated_at": "ISO-8601",
  "subject_count": 2,
  "subjects": [
    {
      "subject": "data-structures",
      "level": "intermediate",
      "ema_score": 68.4,
      "last_score": 72.0,
      "confidence": 54.0,
      "attempts": 5,
      "trend": "up|flat|down|insufficient-data",
      "weak_areas": ["recurrence"],
      "next_focus": ["trees", "graphs"],
      "updated_at": "ISO-8601"
    }
  ]
}
```

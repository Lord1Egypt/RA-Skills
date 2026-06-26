# Daily Log Format

> Storage: `~/.parent-skill/children/[name]/daily-log.jsonl`

## Entry Format

```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "type": "feed|sleep|diaper|play|cry|milestone|note",
  "details": "Description of what happened",
  "what_worked": "What resolved the situation (if applicable)",
  "caregiver": "Who was with baby"
}
```

## Examples

```json
{"date":"2025-03-15","time":"03:47","type":"feed","details":"Bottle 4oz, took 15 min","caregiver":"Mom"}
{"date":"2025-03-15","time":"06:30","type":"sleep","details":"Woke up, slept 5.5hrs straight","caregiver":"Mom"}
{"date":"2025-03-15","time":"14:00","type":"milestone","details":"Rolled over for the first time trying to reach the cat","caregiver":"Dad"}
{"date":"2025-03-15","time":"17:15","type":"cry","details":"Fussy period, 30min","what_worked":"Yoga ball bouncing","caregiver":"Grandma"}
```

*Log entries are cumulative. Earlier entries are preserved alongside newer ones.*

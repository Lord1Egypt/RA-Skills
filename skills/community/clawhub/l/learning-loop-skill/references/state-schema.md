# state.json Schema

## Full Schema

```json
{
  "topic": "Machine Learning",
  "topicSlug": "machine-learning",
  "phase": 1,
  "curriculum": ["linear-regression", "gradient-descent", "neural-networks"],
  "currentSubtopicIndex": 0,
  "currentDay": 1,
  "currentSession": "S1",
  "status": "in_progress",
  "sessionTiming": {
    "dailyStartHour": 9,
    "s1ToS2Hours": 4,
    "s2ToS3Hours": 4,
    "s3ToS4Hours": 4
  },
  "notifications": {
    "deliver": true,
    "channel": "telegram",
    "to": null
  },
  "history": [
    {
      "subtopic": "linear-regression",
      "day": 1,
      "s2Score": 62,
      "s4Score": 85,
      "improvement": 23,
      "mastered": true
    }
  ],
  "createdAt": "2026-03-12T03:00:00Z",
  "updatedAt": "2026-03-12T03:00:00Z"
}
```

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `topic` | string | Human-readable topic name |
| `topicSlug` | string | URL-safe slug used in paths |
| `phase` | number | Curriculum phase (starts at 1, increments on expansion) |
| `curriculum` | string[] | Ordered list of subtopic slugs |
| `currentSubtopicIndex` | number | Index into curriculum array (0-based) |
| `currentDay` | number | Learning day counter (1-based) |
| `currentSession` | string | Next session to execute: "S1", "S2", "S3", "S4", "S5" |
| `status` | string | Pipeline status (see below) |
| `sessionTiming` | object | Schedule config: `dailyStartHour` (0-23, default 9) and hours between sessions |
| `notifications` | object | How to notify the user |
| `history` | array | One entry per day with scores |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

## Status Values

| Status | Meaning |
|--------|---------|
| `in_progress` | Learning is active, sessions executing |
| `needs_intervention` | S4 score < 50%, waiting for user |
| `paused` | User requested pause |
| `curriculum_complete` | All subtopics mastered |
| `expanding` | Curriculum expansion in progress |

## History Entry

Each day produces one history entry:

```json
{
  "subtopic": "gradient-descent",
  "day": 3,
  "s2Score": 58,
  "s4Score": 82,
  "improvement": 24,
  "mastered": false,
  "focusAreas": ["convergence criteria", "learning rate selection"]
}
```

- `mastered`: true if s4Score >= 85
- `focusAreas`: populated when score 50-84%, guides next day's S1

## Notifications Object

```json
{
  "deliver": true,
  "channel": "telegram",
  "to": "839346179"
}
```

If `deliver` is false or notifications object is absent, cron agents should skip notification steps. When `deliver` is true, agents use the message/delivery tool with the specified channel and recipient.

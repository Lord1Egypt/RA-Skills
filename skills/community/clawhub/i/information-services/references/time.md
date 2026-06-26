# Time Service — Detailed Specifications

> Part of information-services skill.

---

## 1. Trigger Scenarios

| Scenario | Example Phrase |
|----------|----------------|
| Current time | "What time is it?" |
| Time check | "Report current time with confidence" |
| Timezone conversion | "What time is it in London?" |
| Precise time | "Accurate time via NTP" |

## 2. Multi-Source Time Fusion

### Source Priority

| Priority | Source | Accuracy | Latency |
|----------|--------|----------|---------|
| 1 | System clock | OS-dependent | Instant |
| 2 | NTP | ±10ms | 50-200ms |
| 3 | Web API (worldtimeapi, etc.) | ±500ms | 100-500ms |

### Workflow

1. Query system clock (instant, baseline)
2. If precision needed, query NTP server
3. If NTP fails, query web time API
4. Combine with confidence scoring
5. Return unified result

### Confidence Scoring

| Source | Base Confidence | Notes |
|--------|----------------|-------|
| System clock | 0.85 | OS-synced, may drift |
| NTP | 0.98 | Stratum-synchronized |
| Web API | 0.92 | Server-dependent |

### Output Format

```json
{
  "datetime": "2026-04-26T22:47:00+08:00",
  "timestamp": 1743084420,
  "timezone": "Asia/Hong_Kong",
  "sources": ["system", "ntp"],
  "confidence": 0.96,
  "accuracy_ms": 15
}
```

## 3. Voice Output (Optional)

When TTS is available and requested, optionally announce time in natural language:
- "It's 10:47 PM, Saturday, April 26th."
- Timezone-aware natural speech formatting
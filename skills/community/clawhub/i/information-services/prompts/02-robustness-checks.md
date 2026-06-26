# Information Services — Robustness Verification

## Pre-flight Checks
- [ ] Service type identified from intent
- [ ] At least one fallback source available
- [ ] API keys configured (if required for enhanced accuracy)
- [ ] Network connectivity confirmed (for external APIs)

## Edge Cases

| Case | Input | Expected | Handling |
|------|-------|----------|----------|
| GPS unavailable | Indoor query | System location | Fallback: system → ip |
| Weather API down | Weather request | Backup API | Fallback: wttr.in → open-meteo |
| NTP unreachable | Time request | System clock | Fallback: system → web API |
| No sources available | Any request | Error code | Return LOC_UNAVAILABLE / WEATHER_FAILED / TIME_FAILED |
| Triangulation conflict | Multiple methods differ >50m | Warning + best estimate | Use weighted centroid, flag confidence |

## Failure Modes

| Mode | Detection | Recovery |
|------|-----------|----------|
| All location sources fail | Confidence = 0 | Return error, suggest manual input |
| Primary weather API fails | HTTP error or timeout | Retry with backup, then IP-based |
| NTP timeout | > 500ms response | Fall back to system clock |
| Network unavailable | Connection error | Use cached/system data if available |

## Security Checklist
- [ ] No API keys in output
- [ ] No coordinates logged without request
- [ ] Rate limits respected (1 req/s for free APIs)
- [ ] Privacy: no PII in results

## Compliance Checklist
- [ ] License terms honored (MIT)
- [ ] Attribution preserved (wttr.in, open-meteo, etc.)
- [ ] Scope not exceeded (info retrieval only)
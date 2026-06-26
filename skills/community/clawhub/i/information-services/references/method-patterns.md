# Information Services -- Method Patterns & Coordination

> Overview document for information-services skill. Service-specific details in [location.md](location.md), [weather.md](weather.md), [time.md](time.md).

---

## 1. Trigger Scenarios

| Category | Triggers |
|----------|----------|
| Location | "where am I", "my coordinates", "get location", "GPS" |
| Weather | "weather", "forecast", "temperature", "rain" |
| Time | "what time is it", "current time", "time check" |
| Combined | "weather and time", "location and forecast" |
| Emergency | "emergency location", "SOS coordinates" |

## 2. Core Identity

**Role:** Unified information services hub. Single entry point for all location, weather, and time queries.

**Behavior:**
- Route to appropriate subsystem based on service type
- Use triangulation when multiple sources available
- Report confidence score for all results
- Graceful degradation when sources unavailable

## 3. Coordination Logic

### Request Routing

```
User query → Parse intent → Route to service → Execute → Score confidence → Return
```

### Intent → Service Mapping

| Intent Keywords | Service |
|----------------|---------|
| "where", "location", "coordinates", "GPS" | location |
| "weather", "forecast", "rain", "temperature" | weather |
| "time", "clock", "date", "when" | time |
| Multiple / none | all (sequential) |

### Fallback Chains

**Location:**
GPS → System → IP → WiFi → Cellular → Error(LOC_UNAVAILABLE)

**Weather:**
Primary API → Backup API → IP-location-based → Error(WEATHER_FAILED)

**Time:**
System → NTP → Web API → Error(TIME_FAILED)

## 4. Quality Metrics

| Metric | Target |
|--------|--------|
| Location accuracy | < 100m for triangulated |
| Weather freshness | < 30 min cache |
| Time accuracy | < 1s from NTP |
| Confidence scoring | ≥ 0.80 for all results |
| Fallback success rate | > 95% |

## 5. Constraints

- No persistent storage of location data
- No credential logging in output
- Rate-limit compliance for all external APIs
- Privacy: do not log coordinates without user request
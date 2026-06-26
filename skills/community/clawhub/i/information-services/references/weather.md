# Weather Service — Detailed Specifications

> Part of information-services skill.

---

## 1. Trigger Scenarios

| Scenario | Example Phrase |
|----------|----------------|
| Current location weather | "What's the weather here?" |
| Fixed-point forecast | "Weather in Shanghai tomorrow" |
| Manual coordinates | "Weather at 39.9N, 116.4E" |
| Time-aware location | "Weather this evening" |

## 2. Workflow

1. **Geolocation** — Use location service to get coordinates (GPS → system → IP → WiFi → cellular)
2. **Weather lookup** — Query weather API with coordinates
3. **Multi-source fusion** — Combine multiple weather sources with confidence weighting
4. **Output** — Return structured weather data with confidence score

## 3. Supported Weather Data

| Data Point | Description |
|------------|-------------|
| Temperature | Current temp in Celsius |
| Conditions | sunny, cloudy, rainy, etc. |
| Humidity | Percentage |
| Wind | Speed and direction |
| Forecast | 3-7 day outlook |
| UV Index | UV radiation level |
| AQI | Air quality index |

## 4. Sources

- wttr.in (no API key required)
- Open-Meteo (no API key required)
- Custom weather API (if configured)

## 5. Error Handling

| Error | Action |
|-------|--------|
| No location available | Fall back to IP-based location |
| Weather API timeout | Retry with alternate source |
| All sources failed | Return error with partial data |

## 6. Output Format

```json
{
  "location": {"lat": 39.9042, "lon": 116.4074},
  "current": {
    "temp_c": 18,
    "conditions": "partly cloudy",
    "humidity": 65,
    "wind_kmh": 12
  },
  "forecast": [...],
  "confidence": 0.88,
  "source": "wttr.in"
}
```
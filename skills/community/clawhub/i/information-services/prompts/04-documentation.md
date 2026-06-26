# Information Services — Documentation

## Overview
Unified information services hub combining location, weather, and time capabilities into a single skill.

## Services

### Location Service
Multi-source geolocation combining GPS, System, IP, WiFi, and Cellular methods with triangulated confidence scoring.

**Methods:**
- `GPS`: 3-10m accuracy, outdoor only
- `System`: 10m-1km, OS-managed, always available
- `IP`: 1-50km, city-level, internet required
- `WiFi`: 10-100m, indoor environments
- `Cellular`: 100m-3km, rural fallback
- `Triangulated`: Weighted centroid of multiple methods

### Weather Service
Fixed-point weather forecasts with multi-source data fusion.

**Data:** Current conditions, temperature, humidity, wind, 3-7 day forecast, AQI, UV index

**Sources:** wttr.in (default), Open-Meteo (backup)

### Time Service
Multi-source time with system/NTP/web API fusion and confidence scoring.

**Precision:** ±15ms (NTP), ±500ms (web API), OS-dependent (system)

## Usage Examples

```
# Get current location weather
service=weather, method=all

# Get precise time
service=time, precision=high

# Get coordinates
service=location, method=gps
```

## Configuration
No required API keys for basic operation. Optional keys for enhanced accuracy:
- `GOOGLE_GEOLOCATION_API_KEY` (WiFi/Cellular accuracy)
- `MLS_API_KEY` (Mozilla Location Service)
- `UNWIRED_API_KEY` (Unwired Labs)
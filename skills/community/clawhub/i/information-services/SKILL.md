---
name: "Information Services"
slug: "information-services"
version: "1.0.0"
language: en
description: |
  Unified information services hub combining location, weather, and time capabilities.
  Multi-source geolocation (GPS/IP/WiFi), fixed-point weather forecasts, and multi-source
  time reporting with confidence scoring. Single entry point for all location-aware services.
license: MIT
triggers:
  - location
  - weather
  - time
  - GPS coordinates
  - forecast
  - current time
  - where am i
  - what time is it
  - weather forecast
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        service:
          type: string
          enum: [location, weather, time, all]
          description: Which service to query
        location:
          type: string
          description: City name or coordinates (lat,lon)
        method:
          type: string
          description: Specific method (gps, system, ip, wifi, cellular)
  outputs:
    type: object
    schema:
      type: object
      properties:
        service_type:
          type: string
          description: location | weather | time
        data:
          type: object
          description: Service-specific result data
        confidence:
          type: number
          description: Confidence score 0-1
  errors:
    - code: LOC_UNAVAILABLE
      message: No location source available
    - code: WEATHER_FAILED
      message: Weather API request failed
    - code: TIME_FAILED
      message: Time source unavailable
    - code: NO_CREDENTIALS
      message: Required API credentials missing
quality:
  idempotent: true
metadata:
  category: information
  standardized: true
---

# Information Services v1.0.0

> Index & Quick Reference. Full specifications in [references/](references/).

## Quick Reference

### Role
Unified hub for location, weather, and time services. Routes requests to the appropriate subsystem based on service type.

### Department
Information

## Section Index

- [Location Service](references/location.md)
- [Weather Service](references/weather.md)
- [Time Service](references/time.md)
- [Coordination Logic](references/method-patterns.md#coordination)

## Services

| Service | Capabilities | Source Skills |
|---------|-------------|---------------|
| **Location** | GPS, system, IP, WiFi, cellular triangulation | multi-source-locate |
| **Weather** | Current conditions, forecast, multi-source fusion | locate-weather |
| **Time** | System clock, NTP, web API, confidence scoring | multi-source-time |

## Prompts

- [01-implement-method.md](prompts/01-implement-method.md)
- [02-robustness-checks.md](prompts/02-robustness-checks.md)
- [03-test-cases.md](prompts/03-test-cases.md)
- [04-documentation.md](prompts/04-documentation.md)
- [05-workflow-execution.md](prompts/05-workflow-execution.md)

---

*See [references/](references/) for detailed service specifications.*
---
name: openweathermap
description: Get current weather data, forecasts, and weather information from OpenWeatherMap API. Use when the user asks about weather, temperature, forecasts, or any weather-related queries for any location. Supports both metric (Celsius, m/s, hPa) and imperial (Fahrenheit, mph, inHg) units. Requires an OpenWeatherMap API key from https://home.openweathermap.org/api_keys
metadata:
  openclaw:
    requires:
      env:
        - OPENWEATHERMAP_API_KEY
      files:
        - ~/.openweathermap
    primaryEnv: OPENWEATHERMAP_API_KEY
---

# OpenWeatherMap Weather Skill

## Setup

Get your free API key from: https://home.openweathermap.org/api_keys

Store your API key securely (the skill checks these in order):
1. Environment variable `$OPENWEATHERMAP_API_KEY`
2. File `~/.openweathermap` (should contain just the API key, one line)
3. Ask the user for their API key

## Current Weather API

### By City Name
```
GET https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={API_KEY}&units={units}
```

### By Coordinates
```
GET https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}
```

### Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `appid` | Yes | Your OpenWeatherMap API key |
| `q` | Yes* | City name, state code, country code (e.g., "London,UK" or "Stamford,CT,US") |
| `lat` | Yes* | Latitude |
| `lon` | Yes* | Longitude |
| `units` | No | `metric`, `imperial`, or `standard`. Default: standard |
| `lang` | No | Language code for description (e.g., `en`, `es`, `fr`, `de`) |

**Units:**
- `metric` = Celsius, m/s, hPa
- `imperial` = Fahrenheit, mph, hPa (use for US locations)
- `standard` = Kelvin, m/s, hPa

**Location Tips for US:**
- Use state abbreviation: `Stamford,CT,US` or full name `Stamford,Connecticut,US`
- The API often requires country code for US cities

## Example API Calls

### London (Metric - Celsius)
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London,UK&appid=YOUR_API_KEY&units=metric"
```

### Stamford CT (Imperial - Fahrenheit)
```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Stamford,CT,US&appid=YOUR_API_KEY&units=imperial"
```

### By Coordinates
```bash
curl "https://api.openweathermap.org/data/2.5/weather?lat=41.05&lon=-73.54&appid=YOUR_API_KEY&units=imperial"
```

## Response Fields
- `main.temp` - Temperature (Celsius/Fahrenheit/Kelvin based on units)
- `main.feels_like` - Perceived temperature
- `main.humidity` - Humidity %
- `main.pressure` - Atmospheric pressure (hPa)
- `wind.speed` - Wind speed (m/s or mph based on units)
- `wind.deg` - Wind direction (degrees)
- `wind.gust` - Wind gusts (if available)
- `clouds.all` - Cloudiness %
- `weather[0].main` - Weather condition (Rain, Snow, Clouds, Clear, etc.)
- `weather[0].description` - Detailed description
- `visibility` - Visibility in meters
- `sys.sunrise` / `sys.sunset` - Unix timestamps
- `name` - Location name
- `timezone` - Shift from UTC in seconds

## Displaying Weather to User

**Use imperial units (Fahrenheit, mph) for US users:**
- Fahrenheit reads naturally to Americans
- Wind speed in mph is the US standard
- Convert pressure from hPa to inHg: `1 inHg = 33.86 hPa`

**24-hour time:** Convert Unix timestamps to 24-hour format (e.g., 18:45 instead of 6:45 PM)

**Example formatting:**
```
🌡️ Temp: 45°F (feels like 40°F)
💧 Humidity: 65%
💨 Wind: 12 mph NW
🌅 Sunrise: 06:32
🌇 Sunset: 18:45
```

## Forecast API (5 Day / 3 Hour)

```
GET https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial
```

Returns forecast data in 3-hour intervals for 5 days.

## API Limits

- Free tier: 60 calls/minute, 1,000,000 calls/month
- One Call API 3.0 (hourly/daily/minutely forecasts + alerts): requires paid subscription
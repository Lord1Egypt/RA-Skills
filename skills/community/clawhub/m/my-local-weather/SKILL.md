# My Local Weather Skill

## Description
A robust, local-first weather information skill for OpenClaw. This skill provides real-time weather forecasts, current conditions, and alerts by querying reliable meteorological APIs. It is designed to be fast, privacy-conscious, and highly configurable.

## Capabilities
- **Current Weather**: Retrieve temperature, humidity, wind speed, pressure, and visibility for any location.
- **Forecasts**: Get hourly forecasts for the next 24 hours and daily forecasts for up to 7 days.
- **Weather Alerts**: Fetch active severe weather warnings (storms, heatwaves, floods) for specific regions.
- **Historical Data**: Access past weather data for analysis (optional, depending on API key).
- **Unit Conversion**: Automatically handle conversions between Metric (Celsius, km/h) and Imperial (Fahrenheit, mph) units based on user preference or location.

## Usage Examples
- "What's the weather like in Tokyo right now?"
- "Will it rain in London tomorrow morning?"
- "Give me a 3-day forecast for New York City."
- "Are there any storm warnings in Florida?"
- "What is the humidity and wind speed in Berlin?"

## Configuration
This skill requires an API key for the weather provider (e.g., OpenWeatherMap, WeatherAPI).
1. Obtain an API key from your preferred provider.
2. Set the environment variable WEATHER_API_KEY or configure it in your .env file within the skill directory.
3. Optionally set WEATHER_UNITS to 'metric' or 'imperial'.

## Technical Details
- **Runtime**: Node.js
- **Dependencies**: Axios (for HTTP requests), dotenv (for config)
- **Privacy**: No user data is stored; all requests are proxied directly from the user's machine to the weather API.

## Troubleshooting
- If you see "API Key Missing", ensure WEATHER_API_KEY is set correctly.
- If location lookup fails, try using city names instead of coordinates, or vice versa.

---
name: open-meteo-daily-weather
description: Get today's high, low, and maximum rain chance for a user-selected public location.
---

Run `node forecast.mjs "City, Region"` from this skill folder for the user's public location, or set `WEATHER_LOCATION` and run `node forecast.mjs`. The script needs Node.js 20 or newer and HTTPS access to Open-Meteo's geocoding and forecast APIs. It needs no API key and reads no private account data.

Report the returned date, location, Fahrenheit high and low, maximum rain chance, and Open-Meteo source. If lookup or forecast fails, say weather is unavailable; do not invent a forecast. Ask for a more specific city or postal code when the location is ambiguous.

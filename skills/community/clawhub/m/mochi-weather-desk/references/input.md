# Action contract

import: file, an Open-Meteo JSON response containing aligned daily arrays time, temperature_2m_max, temperature_2m_min, precipitation_probability_max, wind_speed_10m_max. fetch: latitude (-90..90), longitude (-180..180), days (1..7, default 3), network:true. Only api.open-meteo.com/v1/forecast is called; coordinates are sent to that provider. Import is offline. API access depends on provider terms and quotas.

## Request example

```json
{
  "action": "import",
  "file": "samples/forecast.json"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Use a user-selected city or coordinates; do not discover the device location automatically. Explain that a live request sends coordinates to Open-Meteo. Preserve attribution and check service usage terms, including commercial use. Forecasts are not official emergency alerts.

# Open-Meteo Forecast API — Variable Catalog

Complete variable lists for `https://api.open-meteo.com/v1/forecast`.
All names below were verified against the live API. Pass them comma-separated
to the `current`, `hourly`, or `daily` query parameters.

## Contents

- [Current variables](#current-variables)
- [Hourly variables](#hourly-variables)
- [Daily variables](#daily-variables)
- [Units and settings parameters](#units-and-settings-parameters)
- [Weather models](#weather-models)
- [Full WMO weather code table](#full-wmo-weather-code-table)

## Current variables

| Variable | Unit | Notes |
|---|---|---|
| `temperature_2m` | °C | Air temperature at 2 m |
| `relative_humidity_2m` | % | |
| `apparent_temperature` | °C | "Feels like" (wind chill + humidity + radiation) |
| `is_day` | 0/1 | 1 = daylight — use to pick day/night icons |
| `precipitation` | mm | Total of rain + showers + snow (preceding interval) |
| `rain` | mm | |
| `showers` | mm | |
| `snowfall` | cm | |
| `weather_code` | WMO code | See table below |
| `cloud_cover` | % | |
| `pressure_msl` | hPa | Sea-level pressure |
| `surface_pressure` | hPa | |
| `wind_speed_10m` | km/h | |
| `wind_direction_10m` | ° | Meteorological (direction wind comes FROM) |
| `wind_gusts_10m` | km/h | |

The `current` block also returns `time` and `interval` (data refresh interval
in seconds, typically 900).

## Hourly variables

### Temperature and humidity

| Variable | Unit |
|---|---|
| `temperature_2m` | °C |
| `relative_humidity_2m` | % |
| `dew_point_2m` | °C |
| `apparent_temperature` | °C |
| `temperature_80m`, `temperature_120m`, `temperature_180m` | °C |

### Precipitation

| Variable | Unit | Notes |
|---|---|---|
| `precipitation_probability` | % | Chance of precipitation in the hour |
| `precipitation` | mm | Sum of rain + showers + snowfall |
| `rain` | mm | Large-scale rain |
| `showers` | mm | Convective showers |
| `snowfall` | cm | |
| `snow_depth` | m | Snow on ground |

### Sky, wind, pressure

| Variable | Unit | Notes |
|---|---|---|
| `weather_code` | WMO code | |
| `cloud_cover` | % | Total |
| `cloud_cover_low` / `cloud_cover_mid` / `cloud_cover_high` | % | 0–2 km / 2–6 km / >6 km |
| `visibility` | m | |
| `pressure_msl`, `surface_pressure` | hPa | |
| `wind_speed_10m`, `wind_speed_80m`, `wind_speed_120m`, `wind_speed_180m` | km/h | |
| `wind_direction_10m` (also `_80m`, `_120m`, `_180m`) | ° | |
| `wind_gusts_10m` | km/h | |

### Radiation, sun, agriculture

| Variable | Unit | Notes |
|---|---|---|
| `uv_index`, `uv_index_clear_sky` | index | |
| `is_day` | 0/1 | |
| `shortwave_radiation` | W/m² | Global horizontal irradiance |
| `direct_radiation`, `diffuse_radiation` | W/m² | |
| `direct_normal_irradiance` | W/m² | For solar panel modeling |
| `sunshine_duration` | s | Per hour |
| `et0_fao_evapotranspiration` | mm | FAO-56 reference evapotranspiration |
| `vapour_pressure_deficit` | kPa | |
| `soil_temperature_0cm`, `_6cm`, `_18cm`, `_54cm` | °C | |
| `soil_moisture_0_to_1cm`, `_1_to_3cm`, `_3_to_9cm`, `_9_to_27cm`, `_27_to_81cm` | m³/m³ | |

### Severe weather / aviation

| Variable | Unit | Notes |
|---|---|---|
| `cape` | J/kg | Convective available potential energy |
| `freezing_level_height` | m | Altitude of the 0 °C isotherm |

## Daily variables

Daily aggregation **requires the `timezone` parameter** (use `timezone=auto`).

| Variable | Unit | Notes |
|---|---|---|
| `weather_code` | WMO code | Most severe code of the day |
| `temperature_2m_max`, `temperature_2m_min` | °C | |
| `apparent_temperature_max`, `apparent_temperature_min` | °C | |
| `precipitation_sum` | mm | |
| `rain_sum`, `showers_sum` | mm | |
| `snowfall_sum` | cm | |
| `precipitation_hours` | h | Hours with precipitation |
| `precipitation_probability_max` | % | |
| `sunrise`, `sunset` | ISO 8601 | Local time when `timezone=auto` |
| `daylight_duration`, `sunshine_duration` | s | |
| `uv_index_max`, `uv_index_clear_sky_max` | index | |
| `wind_speed_10m_max`, `wind_gusts_10m_max` | km/h | |
| `wind_direction_10m_dominant` | ° | |
| `shortwave_radiation_sum` | MJ/m² | |
| `et0_fao_evapotranspiration` | mm | |

## Units and settings parameters

| Parameter | Values | Default |
|---|---|---|
| `temperature_unit` | `celsius`, `fahrenheit` | celsius |
| `wind_speed_unit` | `kmh`, `ms`, `mph`, `kn` | kmh |
| `precipitation_unit` | `mm`, `inch` | mm |
| `timeformat` | `iso8601`, `unixtime` | iso8601 (unixtime is always UTC) |
| `timezone` | `auto` or IANA name | GMT |
| `forecast_days` | 0–16 | 7 |
| `past_days` | 0–92 | 0 |
| `start_date` / `end_date` | `YYYY-MM-DD` | — |
| `cell_selection` | `land`, `sea`, `nearest` | land |
| `elevation` | meters | downscaling from a 90 m DEM; pass explicitly to override |

## Weather models

By default (`models=auto`) Open-Meteo picks the best model per location. To
force a specific model, pass e.g. `models=gfs_seamless`. Common options:
`best_match` (default), `ecmwf_ifs025`, `gfs_seamless` (NOAA),
`icon_seamless` (DWD), `meteofrance_seamless`, `jma_seamless`, `gem_seamless`,
`ukmo_seamless`. Multiple models can be requested at once
(`models=gfs_seamless,icon_seamless`) — variables are then suffixed with the
model name in the response.

## Full WMO weather code table

| Code | Description | Day/night icon hint |
|---|---|---|
| 0 | Clear sky | sun / moon |
| 1 | Mainly clear | sun / moon |
| 2 | Partly cloudy | sun+cloud |
| 3 | Overcast | cloud |
| 45 | Fog | fog |
| 48 | Depositing rime fog | fog |
| 51 | Light drizzle | drizzle |
| 53 | Moderate drizzle | drizzle |
| 55 | Dense drizzle | drizzle |
| 56 | Light freezing drizzle | sleet |
| 57 | Dense freezing drizzle | sleet |
| 61 | Slight rain | rain |
| 63 | Moderate rain | rain |
| 65 | Heavy rain | rain |
| 66 | Light freezing rain | sleet |
| 67 | Heavy freezing rain | sleet |
| 71 | Slight snowfall | snow |
| 73 | Moderate snowfall | snow |
| 75 | Heavy snowfall | snow |
| 77 | Snow grains | snow |
| 80 | Slight rain showers | showers |
| 81 | Moderate rain showers | showers |
| 82 | Violent rain showers | showers |
| 85 | Slight snow showers | snow |
| 86 | Heavy snow showers | snow |
| 95 | Thunderstorm | storm |
| 96 | Thunderstorm with slight hail | storm+hail |
| 99 | Thunderstorm with heavy hail | storm+hail |

Codes 96/99 are only produced by models that forecast hail; most locations see
95 for any thunderstorm.

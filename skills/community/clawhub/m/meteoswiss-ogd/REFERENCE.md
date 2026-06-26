<!-- Canonical source: packages/meteoswiss-mcp/src/support/weather-icons.ts and src/schemas/ogd-shared.ts -->
<!-- If MeteoSwiss updates parameters or icons, update both this file and the MCP server source. -->

# MeteoSwiss OGD — Parameter Reference

Full reference tables for MeteoSwiss Open Government Data parameters, weather icons, and STAC collections.

## Table of Contents

- [Current Weather Parameters (VQHA80.csv)](#current-weather-parameters)
- [Forecast Parameters — Daily (Stations)](#forecast-parameters--daily)
- [Forecast Parameters — Hourly (Postal Codes, Mountains)](#forecast-parameters--hourly)
- [Weather Icon Codes — Day](#weather-icon-codes--day)
- [Weather Icon Codes — Night](#weather-icon-codes--night)
- [Pollen Types](#pollen-types)
- [Pollen Stations](#pollen-stations)
- [STAC Collections](#stac-collections)

## Current Weather Parameters

Parameters in the `VQHA80.csv` real-time measurements file. All values from the most recent 10-minute observation.

| Parameter | Description | Unit |
|-----------|------------|------|
| `tre200s0` | Air temperature 2m above ground | °C |
| `ure200s0` | Relative humidity 2m above ground | % |
| `tde200s0` | Dew point temperature 2m | °C |
| `rre150z0` | Precipitation, 10-minute total | mm |
| `fu3010z0` | Mean wind speed 10min | km/h |
| `fu3010z1` | Wind gust peak (max) | km/h |
| `dkl010z0` | Wind direction | ° (0-360) |
| `sre000z0` | Sunshine duration, 10-minute total | min |
| `gre000z0` | Global radiation | W/m² |
| `prestas0` | Atmospheric pressure at station level | hPa |
| `pp0qffs0` | Pressure reduced to sea level (QFF) | hPa |
| `htoauts0` | Total snow depth | cm |

## Forecast Parameters — Daily

Available for stations (`point_type_id=1`). One value per day.

| Parameter | Description | Unit |
|-----------|------------|------|
| `tre200dx` | Daily maximum temperature 2m | °C |
| `tre200dn` | Daily minimum temperature 2m | °C |
| `rka150d0` | Daily precipitation total | mm |
| `jp2000d0` | Weather pictogram code (daytime, see icon tables) | — |

## Forecast Parameters — Hourly

Available for all point types (stations, postal codes, mountains). One value per hour.

| Parameter | Description | Unit |
|-----------|------------|------|
| `tre200h0` | Hourly temperature 2m | °C |
| `rre150h0` | Hourly precipitation | mm |
| `jww003i0` | 3-hourly weather pictogram code | — |

## Weather Icon Codes — Day

Codes used in `jp2000d0` (daily) and `jww003i0` (3-hourly) parameters.

| Code | Description |
|------|------------|
| 1 | Sunny |
| 2 | Mostly sunny, some clouds |
| 3 | Partly sunny, thick passing clouds |
| 4 | Overcast |
| 5 | Very cloudy |
| 6 | Sunny intervals, isolated showers |
| 7 | Sunny intervals, isolated sleet |
| 8 | Sunny intervals, snow showers |
| 9 | Overcast, some rain showers |
| 10 | Overcast, some sleet |
| 11 | Overcast, some snow showers |
| 12 | Sunny intervals, chance of thunderstorms |
| 13 | Sunny intervals, possible thunderstorms |
| 14 | Very cloudy, light rain |
| 15 | Very cloudy, light sleet |
| 16 | Very cloudy, light snow showers |
| 17 | Very cloudy, intermittent rain |
| 18 | Very cloudy, intermittent sleet |
| 19 | Very cloudy, intermittent snow |
| 20 | Very overcast with rain |
| 21 | Very overcast with frequent sleet |
| 22 | Very overcast with heavy snow |
| 23 | Very overcast, slight chance of storms |
| 24 | Very overcast with storms |
| 25 | Very cloudy, very stormy |
| 26 | High clouds |
| 27 | Stratus |
| 28 | Fog |
| 29 | Sunny intervals, scattered showers |
| 30 | Sunny intervals, scattered snow showers |
| 31 | Sunny intervals, scattered sleet |
| 32 | Sunny intervals, some showers |
| 33 | Short sunny intervals, frequent rain |
| 34 | Short sunny intervals, frequent snowfall |
| 35 | Overcast and dry |

SVG icons: `https://www.meteoschweiz.admin.ch/static/resources/weather-symbols/{CODE}.svg`

## Weather Icon Codes — Night

Night codes are day code + 100. Used in `jww003i0` for nighttime hours.

| Code | Description |
|------|------------|
| 101 | Clear |
| 102 | Slightly overcast |
| 103 | Heavy cloud formations |
| 104 | Overcast |
| 105 | Very cloudy |
| 106 | Overcast, scattered showers |
| 107 | Overcast, scattered rain and snow showers |
| 108 | Overcast, snow showers |
| 109 | Overcast, some showers |
| 110 | Overcast, some rain and snow showers |
| 111 | Overcast, some snow showers |
| 112 | Slightly stormy |
| 113 | Storms |
| 114 | Very cloudy, light rain |
| 115 | Very cloudy, light rain and snow showers |
| 116 | Very cloudy, light snowfall |
| 117 | Very cloudy, intermittent rain |
| 118 | Very cloudy, intermittent mixed rain and snowfall |
| 119 | Very cloudy, intermittent snowfall |
| 120 | Very cloudy, constant rain |
| 121 | Very cloudy, frequent rain and snowfall |
| 122 | Very cloudy, heavy snowfall |
| 123 | Very cloudy, slightly stormy |
| 124 | Very cloudy, stormy |
| 125 | Very cloudy, storms |
| 126 | High cloud |
| 127 | Stratus |
| 128 | Fog |
| 129 | Slightly overcast, scattered showers |
| 130 | Slightly overcast, scattered snowfall |
| 131 | Slightly overcast, rain and snow showers |
| 132 | Slightly overcast, some showers |
| 133 | Overcast, frequent rain showers |
| 134 | Overcast, frequent snow showers |
| 135 | Overcast and dry |
| 136 | Slightly overcast, slightly stormy |
| 137 | Slightly overcast, stormy snow showers |
| 138 | Overcast, thundery showers |
| 139 | Overcast, thundery snow showers |
| 140 | Very cloudy, slightly stormy |
| 141 | Overcast, slightly stormy |
| 142 | Very cloudy, thundery snow showers |

## Pollen Types

Common pollen parameter codes in daily pollen CSVs.

| Code | Pollen type (English) |
|------|----------------------|
| `ALN` | Alder |
| `AMB` | Ragweed |
| `BET` | Birch |
| `BIR` | Birch (alternate) |
| `COR` | Hazel |
| `FRA` | Ash |
| `GRA` | Grass |
| `HIE` | Plantain |
| `OLE` | Olive |
| `PAR` | Pellitory |
| `PLA` | Plane |
| `POA` | Grass (Poaceae) |
| `RUM` | Sorrel |
| `TAX` | Yew/Cypress |
| `URT` | Nettle |

Values are in particles/m³. Not all pollen types are measured at every station.

## Pollen Stations

| Abbreviation | Station name |
|-------------|-------------|
| BAS | Basel |
| BER | Bern |
| BUC | Buchs (SG) |
| DAV | Davos |
| GEN | Genève |
| LAU | Lausanne |
| LOG | Locarno |
| LUG | Lugano |
| LUZ | Luzern |
| MUN | Münsterlingen |
| NEU | Neuchâtel |
| VIS | Visp |
| ZUE | Zürich |

URL pattern (lowercase abbreviation): `https://data.geo.admin.ch/ch.meteoschweiz.ogd-pollen/{abbr}/ogd-pollen_{abbr}_d_now.csv`

## STAC Collections

All collections available under `https://data.geo.admin.ch/api/stac/v1/collections/{ID}`.

| Collection ID | Description |
|---------------|-------------|
| `ch.meteoschweiz.ogd-smn` | SwissMetNet automatic stations — real-time measurements |
| `ch.meteoschweiz.ogd-local-forecasting` | Local forecasts for ~6000 Swiss locations |
| `ch.meteoschweiz.ogd-pollen` | Pollen concentration monitoring |
| `ch.meteoschweiz.ogd-smn-precip` | Precipitation measurements |
| `ch.meteoschweiz.ogd-smn-tower` | Tower measurements |
| `ch.meteoschweiz.ogd-nbcn` | Swiss NBCN climate stations |
| `ch.meteoschweiz.ogd-radiosounding` | Radiosounding data |

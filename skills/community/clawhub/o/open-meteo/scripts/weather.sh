#!/usr/bin/env bash
# Open-Meteo weather fetcher
# Usage: weather.sh <latitude> <longitude> [hourly|daily|current] [days] [units]
# units: fahrenheit (default) or celsius

set -euo pipefail

LAT="${1:?Usage: weather.sh <lat> <lon> [hourly|daily|current] [days] [units]}"
LON="${2:?}"
MODE="${3:-current}"
DAYS="${4:-3}"
UNITS="${5:-fahrenheit}"

BASE="https://api.open-meteo.com/v1/forecast"

if [ "$UNITS" = "fahrenheit" ]; then
  TEMP_UNIT="&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
else
  TEMP_UNIT=""
fi

case "$MODE" in
  current)
    curl -sf "${BASE}?latitude=${LAT}&longitude=${LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,sunrise,sunset,uv_index_max,wind_speed_10m_max&forecast_days=${DAYS}&timezone=auto${TEMP_UNIT}"
    ;;
  hourly)
    curl -sf "${BASE}?latitude=${LAT}&longitude=${LON}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m,uv_index,is_day&forecast_days=${DAYS}&timezone=auto${TEMP_UNIT}"
    ;;
  daily)
    curl -sf "${BASE}?latitude=${LAT}&longitude=${LON}&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant&forecast_days=${DAYS}&timezone=auto${TEMP_UNIT}"
    ;;
  *)
    echo "Unknown mode: $MODE (use current, hourly, or daily)" >&2
    exit 1
    ;;
esac

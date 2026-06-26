#!/usr/bin/env bash
# name: weather
# description: 查询全球城市天气（当前天气、多日预报），数据来源 wttr.in / WorldWeatherOnline
# tags: 天气,气温,预报,weather

set -euo pipefail

CITY="" DAYS="0" DETAIL="false" FORMAT="json"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --city) CITY="$2"; shift 2;;
    --days) DAYS="$2"; shift 2;;
    --detail) DETAIL="true"; shift;;
    --format) FORMAT="$2"; shift 2;;
    *) shift;;
  esac
done

if [[ -z "$CITY" ]]; then
  echo '{"status":"error","error_type":"missing_parameter","missing":"city","suggestion":"请指定城市名，例如 --city 北京","example":"bash scripts/run.sh call weather --city 北京"}' >&2
  exit 1
fi

# URL 编码城市名
ENCODED_CITY=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$CITY")

# 请求天气数据，带超时控制
RESP=$(curl -sf --max-time 10 "https://wttr.in/${ENCODED_CITY}?format=j1&m" 2>/dev/null) || {
  echo '{"status":"error","error_type":"api_unavailable","service":"wttr.in","suggestion":"天气服务暂时不可用，请稍后重试。如持续失败，可尝试使用英文城市名。"}' >&2
  exit 1
}

# 通过环境变量传 JSON，sys.argv 传参数，避免 stdin 冲突和 shell 注入
export _WEATHER_JSON="$RESP"

if [[ "$FORMAT" == "table" ]]; then
  python3 -c "
import json, os, sys

data = json.loads(os.environ['_WEATHER_JSON'])
city = sys.argv[1]
days = int(sys.argv[2])

cur = data.get('current_condition', [{}])[0]
weather_list = data.get('weather', [])

# 当前天气
desc = cur.get('weatherDesc', [{}])[0].get('value', '')
temp = cur.get('temp_C', '')
feels = cur.get('FeelsLikeC', '')
humidity = cur.get('humidity', '')
wind_speed = cur.get('windspeedKmph', '')
wind_dir = cur.get('winddir16Point', '')
uv = cur.get('uvIndex', '')
precip = cur.get('precipMM', '')

print(f'{city} 天气')
print(f'当前: {desc}, {temp}°C (体感 {feels}°C)')
print(f'湿度: {humidity}%  风: {wind_dir} {wind_speed}km/h  UV: {uv}  降水: {precip}mm')

# 多日预报
forecasts = weather_list[:max(days, 1)] if days > 0 else []
if forecasts:
    print()
    header = f'{\"日期\":<12} {\"最高\":>5} {\"最低\":>5} {\"天气\":<16} {\"降雨概率\":>8}'
    print(header)
    print('─' * 56)
    for day in forecasts:
        date = day.get('date', '')
        maxt = day.get('maxtempC', '')
        mint = day.get('mintempC', '')
        hourly = day.get('hourly', [])
        mid = hourly[4] if len(hourly) > 4 else {}
        ddesc = mid.get('weatherDesc', [{}])[0].get('value', '')
        rain = mid.get('chanceofrain', '0')
        print(f'{date:<12} {maxt:>4}°C {mint:>4}°C {ddesc:<16} {rain:>7}%')

# 日出日落
if weather_list:
    astro = weather_list[0].get('astronomy', [{}])[0]
    sunrise = astro.get('sunrise', '')
    sunset = astro.get('sunset', '')
    print(f'\n日出: {sunrise}  日落: {sunset}')
" "$CITY" "$DAYS"
else
  python3 -c "
import json, os, sys

data = json.loads(os.environ['_WEATHER_JSON'])
city = sys.argv[1]
days = int(sys.argv[2])
detail = sys.argv[3] == 'true'

cur = data.get('current_condition', [{}])[0]
weather_list = data.get('weather', [])

result = {
    'city': city,
    'current': {
        'temp_C': cur.get('temp_C', ''),
        'feels_like_C': cur.get('FeelsLikeC', ''),
        'desc': cur.get('weatherDesc', [{}])[0].get('value', ''),
        'humidity': cur.get('humidity', ''),
        'wind_kmph': cur.get('windspeedKmph', ''),
        'wind_dir': cur.get('winddir16Point', ''),
        'precip_mm': cur.get('precipMM', ''),
        'uv_index': cur.get('uvIndex', ''),
        'pressure_hPa': cur.get('pressure', ''),
        'visibility_km': cur.get('visibility', ''),
    }
}

# 日出日落
if weather_list:
    astro = weather_list[0].get('astronomy', [{}])[0]
    result['current']['sunrise'] = astro.get('sunrise', '')
    result['current']['sunset'] = astro.get('sunset', '')

# 预报
forecasts = weather_list[:max(days, 1)] if days > 0 else []
if forecasts:
    result['forecast'] = []
    for day in forecasts:
        entry = {
            'date': day.get('date', ''),
            'max_C': day.get('maxtempC', ''),
            'min_C': day.get('mintempC', ''),
            'uv_index': day.get('uvIndex', ''),
            'sun_hour': day.get('sunHour', ''),
        }
        hourly = day.get('hourly', [])
        mid = hourly[4] if len(hourly) > 4 else {}
        entry['desc'] = mid.get('weatherDesc', [{}])[0].get('value', '')
        entry['chance_of_rain'] = mid.get('chanceofrain', '')
        entry['chance_of_snow'] = mid.get('chanceofsnow', '')
        if detail and hourly:
            entry['hourly'] = []
            for h in hourly:
                entry['hourly'].append({
                    'time': h.get('time', ''),
                    'temp_C': h.get('tempC', ''),
                    'desc': h.get('weatherDesc', [{}])[0].get('value', ''),
                    'chance_of_rain': h.get('chanceofrain', ''),
                    'wind_kmph': h.get('windspeedKmph', ''),
                })
        result['forecast'].append(entry)

print(json.dumps(result, ensure_ascii=False, indent=2))
" "$CITY" "$DAYS" "$DETAIL"
fi

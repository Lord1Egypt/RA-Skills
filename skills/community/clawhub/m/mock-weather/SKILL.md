---
name: mock-weather
description: "模拟天气查询，为任意城市生成仿真天气数据（当前天气 + 多日预报）。Use when: (1) 用户查询某城市天气，(2) 用户询问天气预报，(3) 需要演示天气功能但无真实API时。支持中英文城市名，支持1-7天预报。注意：数据为模拟生成，非真实气象数据。"
---

# Mock Weather Skill

Generate simulated weather data for any city. Useful for demos, testing, or when no real weather API is available.

## Usage

Run the script directly:

```bash
# Current weather (today)
python3 scripts/mock_weather.py <city>

# Multi-day forecast (1-7 days)
python3 scripts/mock_weather.py <city> --forecast <days>
```

Examples:

```bash
python3 scripts/mock_weather.py 北京
python3 scripts/mock_weather.py Shanghai --forecast 5
python3 scripts/mock_weather.py 深圳 --forecast 7
```

## Output Fields

| Field | Description |
|-------|-------------|
| 天气 | Weather condition (晴/多云/雨/雪 etc.) |
| 气温 | Low ~ High temperature (°C) |
| 湿度 | Humidity (%) |
| 风力 | Wind direction + level |

## Notes

- Data is deterministically generated from city name + current date (same city = consistent results within a day)
- Supports any city name (Chinese or English)
- Always clarify to users that this is **simulated data**, not real weather

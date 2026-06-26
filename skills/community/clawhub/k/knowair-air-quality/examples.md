# Examples — knowair-forecast

## 7-day forecast for Beijing

**User:** What's the weekly forecast for Beijing?

**Command:**
```bash
python3 scripts/query_forecast.py --lng 116.3176 --lat 39.9760 --type daily --days 7
```

**Response style:** Present a day-by-day summary with high/low temps, weather, and precipitation probability.

## Hourly forecast for the next 24 hours

**User:** Show me the hourly weather for Shanghai today.

**Command:**
```bash
python3 scripts/query_forecast.py --lng 121.4737 --lat 31.2304 --type hourly --hours 24
```

**Response style:** Highlight temperature trend, when weather changes, and any precipitation windows.

## 15-day extended forecast

**User:** 成都未来15天天气怎么样？

**Command:**
```bash
python3 scripts/query_forecast.py --lng 104.0665 --lat 30.5728 --type daily --days 15 --lang zh
```

**Response style:** 按天展示高低温、天气状况和降水概率，重点提示天气变化日期。

## Detailed hourly forecast (every 3 hours)

**User:** Give me the weather every 3 hours for the next 3 days in Hangzhou.

**Command:**
```bash
python3 scripts/query_forecast.py --lng 120.1551 --lat 30.2741 --type hourly --hours 72 --detail-level 3
```

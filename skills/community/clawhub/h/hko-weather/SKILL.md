# HKO Weather Skill (Traditional Chinese / Cantonese)

從香港天文台 (HKO) 開放數據 API 獲取天氣預報及警告信號。

## Description

從香港天文台獲取實時天氣狀況、9 日預報及天氣警告信號。返回格式化的 Markdown，適合 Discord 發佈。

**數據來源：香港天文台 (https://www.hko.gov.hk)**

**語言：繁體中文 (Traditional Chinese)**

**Features:**
- 實時天氣（溫度、濕度、紫外線指數）
- 9 日天氣預報
- 天氣警告及信號（颱風、暴雨、寒冷等）

## License Compliance Notes

**HKO Data Terms:**
- Data is provided by the Hong Kong Observatory under non-commercial terms
- Attribution required: "資料來源：香港天文台 (https://www.hko.gov.hk)"
- All outputs must include the HKO disclaimer (see below)
- Non-commercial use only - no sale or commercial exploitation without written permission

**Required Disclaimer for Outputs:**

All skill outputs must include or reference the HKO disclaimer:

> 香港天文台所提供的天氣預報及氣候預測僅供參考，天文台不就該等天氣預報及氣候預測的準確性或完整性作出任何明示或暗示的保證。在任何情況下，天文台亦不就因使用該等天氣預報及氣候預測而引致或有關的任何損失、損害或費用承擔任何法律責任。
>
> The weather forecasts and climate predictions provided by the Hong Kong Observatory are for reference only. The Observatory does not warrant the accuracy or completeness of such weather forecasts and climate predictions.

## Trigger Keywords

- "HK weather"
- "Hong Kong weather"
- "HKO weather"
- "weather report HK"
- "Hong Kong forecast"
- "HK temperature"
- "Hong Kong Observatory weather"
- "香港天氣"
- "天氣報告"
- "香港預報"

## API Endpoints

No API key required. All endpoints are from HKO's open data platform.

### Current Weather (Traditional Chinese)
```
https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc
```

Returns:
- Temperature readings from multiple stations (溫度)
- Humidity (濕度)
- UV index (紫外線指數)
- Rainfall data (雨量)
- Weather icon (天氣圖標)

### 9-Day Forecast (Traditional Chinese)
```
https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc
```

Returns:
- Daily forecasts (min/max temp, humidity, wind, weather description)
- General weather situation summary (天氣概況)
- Sea and soil temperatures (海溫/土溫)

### Weather Warning Information (Traditional Chinese)
```
https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=tc
```

Returns:
- Warning_Summary: Array of active warnings (typhoon, rainstorm, cold weather, etc.)
- Signal numbers for tropical cyclone and rainstorm warnings
- Issue times and warning descriptions
- Special_Warning: Additional special weather tips (if any)
- Reminder_Warning: Reminder messages (if any)

**Warning Types:**
- `TCWS` - Tropical Cyclone Warning Signal (熱帶氣旋警告信號) 🌀
- `RAINSTORM` - Rainstorm Warning Signal (暴雨警告信號) 🌧️
- `COLD` - Cold Weather Advice (寒冷天氣提示) ❄️
- `STRONGWIND` - Strong Wind Signal (強風信號) 💨
- `LIGHTNING` - Lightning Warning (雷暴警告) ⚡
- `FIRESHRISK` - Fire Risk Warning (火災危險警告) 🔥
- `FLOOD` - Flood Warning (水淹警告) 🌊
- `LANDSLIP` - Landslip Warning (山泥傾瀉警告) 🏔️

## Usage

### Fetch Current Weather Only
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
```

### Fetch 9-Day Forecast Only
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
```

### Fetch Weather Warnings Only
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=tc"
```

### Fetch All (Recommended)
```bash
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=tc"
```

## Output Format

The skill returns markdown formatted for Discord (bullet points, no tables):

**When warnings are active:**
```markdown
## ⚠️ 天氣警告及信號

- 🌀 **八號烈風或暴風信號 8 號**
  - 發出時間：14:00 HKT

## 🌤️ 香港天氣

**現時天氣** (更新時間：HH:MM HKT)
- 🌡️ 溫度：XX°C (京士柏)
- 💧 濕度：XX%
- ☀️ 紫外線指數：X (程度)
...
```

**When no warnings are active:**
```markdown
## ⚠️ 天氣警告及信號

目前沒有生效警告

## 🌤️ 香港天氣
...
```

## Error Handling

### Rate Limiting
- HKO API does not enforce strict rate limits
- Recommended: Cache responses for 10-15 minutes
- If API fails, wait 5 seconds and retry once

### API Failures
- If current weather fails: Return forecast only with error notice
- If forecast fails: Return current weather only with error notice
- If both fail: Return friendly error message suggesting retry

### Timeout
- Set timeout to 10 seconds per request
- HKO servers are generally reliable but can be slow during peak times

## Scripts

See `scripts/fetch-weather.sh` for a ready-to-use fetcher with Traditional Chinese output.

## References

- [HKO Open Data Portal](https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm)
- [HKO API Documentation (PDF)](https://www.hko.gov.hk/tc/weatherAPI/doc/files/HKO_Open_Data_API_Documentation.pdf)
- [DATA.GOV.HK HKO Datasets](https://data.gov.hk/tc-datasets/provider/hk-hko)

## Example Response Structure

### Current Weather (rhrread) - Traditional Chinese
```json
{
  "temperature": {
    "data": [
      {"place": "京士柏", "value": 27, "unit": "C"},
      {"place": "香港天文台", "value": 27, "unit": "C"}
    ],
    "recordTime": "2026-03-26T14:00:00+08:00"
  },
  "humidity": {
    "data": [{"place": "香港天文台", "value": 67, "unit": "percent"}],
    "recordTime": "2026-03-26T14:00:00+08:00"
  },
  "uvindex": {
    "data": [{"place": "京士柏", "value": 6, "desc": "高"}]
  }
}
```

### Forecast (fnd) - Traditional Chinese
```json
{
  "generalSituation": "較潮濕的偏東氣流會在未來一兩日影響廣東東部沿岸...",
  "weatherForecast": [
    {
      "forecastDate": "20260327",
      "week": "星期五",
      "forecastWeather": "大致多雲。早上沿岸有薄霧，日間部分時間有陽光。",
      "forecastMaxtemp": {"value": 28, "unit": "C"},
      "forecastMintemp": {"value": 23, "unit": "C"},
      "forecastWind": "東至東南風 2 至 3 級。"
    }
  ],
  "updateTime": "2026-03-26T11:30:00+08:00"
}
```

### Weather Warning Info (warningInfo) - Traditional Chinese
```json
{
  "Warning_Summary": [
    {
      "WarningType": {
        "Code": "TCWS",
        "Name": {
          "en": "Tropical Cyclone Warning Signal",
          "tc": "熱帶氣旋警告信號",
          "sc": "热带气旋警告信号"
        }
      },
      "Signal": {
        "Code": "8",
        "Value": "8",
        "Name": {
          "en": "Strong Winds from Southeast",
          "tc": "烈風或暴風從東南方吹襲",
          "sc": "烈风或暴风从东南方吹袭"
        }
      },
      "IssueTime": "2026-03-26T14:00:00+08:00"
    }
  ],
  "Special_Warning": [],
  "Reminder_Warning": []
}
```

**No warnings active:**
```json
{}
```

## Notes

- All times are in Hong Kong Time (HKT, UTC+8)
- Temperature in Celsius (攝氏度)
- Wind speeds in Hong Kong Observatory force scale
- PSR (Probability of Significant Rain) values: 低，中低，中，高
- Forecast updates twice daily (around 09:00 and 16:30 HKT)
- Current weather updates every 10 minutes
- **Language**: All output in Traditional Chinese (繁體中文)

## Cron Job Configuration

To schedule regular weather updates with Traditional Chinese output:

```bash
# Example cron job (runs at 8 AM and 6 PM HKT daily)
0 0,10 * * * /app/skills/hko-weather/scripts/fetch-weather.sh --format markdown --lang tc
```

The `--lang tc` parameter ensures Traditional Chinese output.

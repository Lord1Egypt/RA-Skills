# API 參考文檔 (已更新 2026)

## 官方資源

- **API 基址**: https://data.weather.gov.hk/weatherAPI/opendata/weather.php
- **完整文檔 (PDF)**: https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf
- **開放數據介紹**: https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm
- **data.gov.hk 入口**: https://data.gov.hk/tc-datasets/provider/hk-hko

## 正確 dataType 參數

| dataType | 說明 | 更新頻率 |
|----------|------|----------|
| `rhrread` | 當前天氣報告 (含分區氣溫、雨量) | 每小時 |
| `flw` | 本地天氣預報 | 每小時 |
| `fnd` | 九天天氣預報 | 每日 2 次 |
| `warnsum` | 天氣警告摘要 | 即時 |
| `warningInfo` | 詳細天氣警告資訊 | 即時 |
| `swt` | 特別天氣提示 | 即時 |

⚠️ **重要**: 以下為錯誤/過時的 dataType，請勿使用：
- ❌ `CurrentWeatherReport` (應使用 `rhrread`)
- ❌ `RegionalWeather` (分區數據在 `rhrread` 內)
- ❌ `NineDayWeatherForecast` (應使用 `fnd`)
- ❌ `WarningSummary` (應使用 `warnsum`)

## 請求格式

```
https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={dataType}&lang={lang}
```

**參數**:
- `dataType`: 必填，見上表
- `lang`: 選填，`en` (英文), `tc` (繁體中文), `sc` (簡體中文)

## 回應結構示例

### rhrread (當前天氣報告)

```json
{
  "updateTime": "2026-03-11T20:02:00+08:00",
  "temperature": {
    "data": [
      {"place": "香港天文台", "value": 19, "unit": "C"},
      {"place": "沙田", "value": 17, "unit": "C"}
    ],
    "recordTime": "2026-03-11T20:00:00+08:00"
  },
  "humidity": {
    "data": [
      {"place": "香港天文台", "value": 75, "unit": "percent"}
    ],
    "recordTime": "2026-03-11T20:00:00+08:00"
  },
  "rainfall": {
    "data": [
      {"place": "中西區", "max": 0, "unit": "mm"}
    ]
  },
  "uvindex": "",
  "icon": [77]
}
```

### fnd (九天天氣預報)

```json
{
  "updateTime": "2026-03-11T16:30:00+08:00",
  "weatherForecast": [
    {
      "forecastDate": "2026-03-11",
      "forecastMinTemp": 18,
      "forecastMaxTemp": 23,
      "forecastMinRH": 60,
      "forecastMaxRH": 85
    }
  ]
}
```

### warnsum (天氣警告摘要)

```json
{
  "updateTime": "2026-03-11T10:30:00+08:00",
  "warningSummary": [
    {
      "warningType": "RAINSTM",
      "name": {"tc": "暴雨警告", "en": "Rainstorm Warning"},
      "status": "ISSUED",
      "effectiveTime": "2026-03-11T10:30:00+08:00"
    }
  ]
}
```

## 常見警告類型

| 代碼 | 中文名稱 | 英文名稱 |
|------|----------|----------|
| `RAINSTM` / `RS` | 暴雨警告 | Rainstorm Warning |
| `TYHOON` / `TC` | 颱風警告 | Tropical Cyclone Warning |
| `HEAT` | 高溫天氣 | Very Hot Weather |
| `COLD` | 寒冷天氣 | Cold Weather |
| `FIRE` | 火災危險警告 | Fire Danger Warning |
| `LANDSLP` | 山泥傾瀉警告 | Landslip Warning |
| `FLOOD` | 山洪暴發警告 | Flooding in Northern New Territories |
| `WIND` | 強烈季候風信號 | Strong Monsoon Signal |
| `TSTORM` | 雷暴提示 | Thunderstorm |
| `UV` | 紫外線指數 | UV Index |

## curl 使用示例

```bash
# 當前天氣
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc" | jq

# 九天預報
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc" | jq

# 本地天氣預報
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc" | jq

# 天氣警告
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=tc" | jq
```

## 使用條款（重要）

- 使用者必須遵守香港天文台／香港特別行政區政府對「天文台網站資料」的使用條件（尤其商業用途）。
  - 知識產權公告／免責聲明：https://www.hko.gov.hk/tc/readme/readme.htm
  - 非商業用途使用條件：https://www.hko.gov.hk/tc/appweb/applink.htm
  - 商業用途使用條件：https://www.hko.gov.hk/tc/appweb/commercial.htm
- 一般展示／轉載建議：最少保留「資料來源：香港天文台」及相關免責聲明（詳見 `references/terms-and-attribution.md`）。
- ❌ 不建議用於航空、航海或其他安全關鍵應用。
- ❌ 不可誤導用戶認為本項目與香港天文台有任何合作或關聯。

## 錯誤處理

| HTTP 狀態碼 | 說明 | 建議處理 |
|-------------|------|----------|
| 200 | 成功 | 正常處理 JSON |
| 400 | 錯誤請求 | 檢查 dataType 參數 |
| 404 | 資源不存在 | 確認 dataType 正確 |
| 500 | 伺服器錯誤 | 稍後重試 |
| 503 | 服務不可用 | 稍後重試 |

## 相關數據集

除 API 外，data.gov.hk 亦提供：
- 每日總降雨量
- 每日最高/最低氣溫
- 熱帶氣旋路徑資訊
- 預測潮汐資料
- 日出日落時間

詳見：https://data.gov.hk/tc-datasets/provider/hk-hko

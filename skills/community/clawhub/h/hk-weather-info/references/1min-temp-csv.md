# HKO 1-Minute Temperature CSV — Reference

## CSV URLs

| Language | URL |
|---|---|
| `en` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv` |
| `tc` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_uc.csv` |
| `sc` | `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature_sc.csv` |

## Column Names (actual, verified 2026-06-05)

### TC CSV
First column has UTF-8 BOM prefix. Actual headers:
- `日期時間` (datetime)
- `自動氣象站` (station name)
- `氣溫（攝氏）` (temperature in Celsius)

### EN CSV
- `Date time`
- `Automatic Weather Station`
- `Air Temperature(degree Celsius)`

### SC CSV
Similar Chinese column names to TC but with Simplified Chinese characters.

## Sample Data (TC)
```
日期時間,自動氣象站,氣溫（攝氏）
202606051420,赤鱲角,34.4
202606051420,荃灣可觀,32.5
202606051420,荃灣城門谷,34.6
202606051420,京士柏,34.0
```

~39 stations total.

## English → Chinese Alias Mapping

When user provides an English region name, map to Chinese station name fragments:

| English | Chinese fragments |
|---|---|
| Tsuen Wan | 荃灣, 荃 |
| Yuen Long | 元朗 |
| Tuen Mun | 屯門 |
| Central | 中環 |
| Wan Chai | 灣仔 |
| Kowloon | 九龍 |
| Sha Tin | 沙田 |
| Tai Po | 大埔 |
| Tsing Yi | 青衣 |
| Kwun Tong | 觀塘 |
| Mong Kok | 旺角 |
| Aberdeen | 香港仔 |
| Kennedy Town | 堅尼地城 |
| Sheung Wan | 上環 |
| Causeway Bay | 銅鑼灣 |
| Tin Shui Wai | 天水圍 |
| Fanling | 粉嶺 |
| Sheung Shui | 上水 |
| Lau Fau Shan | 流浮山 |

## Gotchas

1. **BOM**: Always strip `\ufeff` from CSV content before parsing.
2. **Station names ≠ district names**: The CSV uses specific automatic weather station names, not district names. E.g. "Tsuen Wan" matches `荃灣可觀` or `荃灣城門谷`, not a station literally called "Tsuen Wan".
3. **Multiple stations per district**: Some districts have multiple stations (e.g. Tsuen Wan has both `荃灣可觀` and `荃灣城門谷`). Return the first match.
4. **No match → average**: If no station matches the requested region, fall back to HK-wide average of all stations.
5. **Cache TTL**: 60 seconds for CSV (fresh data matters more than for JSON API which caches 10 min).

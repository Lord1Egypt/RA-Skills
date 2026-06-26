# 腳本使用說明

本技能提供兩個 Python 腳本用於查詢香港天氣。

## 環境要求

- Python 3.6+
- 無需額外套件 (使用標準庫)

## 腳本列表

### 1. fetch_weather.py - 主要查詢腳本

獲取並解析香港天氣數據。

**用法**:
```bash
python3 scripts/fetch_weather.py --type <類型> [選項]
```

**參數**:

| 參數 | 必填 | 說明 |
|------|------|------|
| `--type` | ✓ | 數據類型：`current` (即時), `forecast` (九天), `hourly` (本地預報), `warnings` (警告) |
| `--days` | 否 | 預報天數 (默认 9，僅 forecast 使用) |
| `--lang` | 否 | 語言：`en` 或 `tc` (默认 tc) |
| `--json` | 否 | 輸出原始 JSON |

**示例**:

```bash
# 全港即時天氣 (含分區氣溫)
python3 scripts/fetch_weather.py --type current

# 九天預報
python3 scripts/fetch_weather.py --type forecast --days 9

# 3 天預報
python3 scripts/fetch_weather.py --type forecast --days 3

# 本地天氣預報 (概況)
python3 scripts/fetch_weather.py --type hourly

# 輸出原始 JSON
python3 scripts/fetch_weather.py --type current --json
```

**輸出範例** (即時天氣):
```
🌡️ 香港即時天氣
   溫度：19°C
   濕度：75%

📍 分區氣溫:
   京士柏：18°C
   香港天文台：19°C
   黃竹坑：19°C
   沙田：17°C
   屯門：19°C
```

**輸出範例** (九天預報):
```
📅 九天天氣預報
   2026-03-12
      天氣：天晴。日間乾燥。
      風：東北風 4 級，晚上漸轉東風 5 級。
      溫度：18-24°C
      濕度：50-80%
```

### 2. check_warnings.py - 警告檢查腳本

快速檢查生效中的天氣警告。

**用法**:
```bash
python3 scripts/check_warnings.py [選項]
```

**參數**:

| 參數 | 說明 |
|------|------|
| `--json` | 輸出原始 JSON |
| `--critical` | 僅顯示關鍵警告 (暴雨/颱風/山泥傾瀉/山洪) |

**示例**:

```bash
# 檢查所有警告
python3 scripts/check_warnings.py

# 僅檢查關鍵警告
python3 scripts/check_warnings.py --critical

# 輸出原始 JSON
python3 scripts/check_warnings.py --json
```

**輸出範例** (無警告):
```
✅ 目前無生效中天氣警告
```

**輸出範例** (有警告):
```
⚠️ 生效中天氣警告
   暴雨警告
      🟢 生效中
      生效時間：2026-03-11 10:30:00
```

## 集成到其他腳本

可以將 API 調用邏輯導入到其他 Python 腳本中使用：

```python
from urllib.request import urlopen, Request
import json

def get_weather_data(data_type, lang="tc"):
    """獲取 HKO 天氣數據"""
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType={data_type}&lang={lang}"
    req = Request(url, headers={"User-Agent": "HKO-Weather-Skill/1.0"})
    with urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))

# 使用示例
data = get_weather_data("rhrread")  # 當前天氣
temp_data = data["temperature"]["data"]
for station in temp_data[:5]:
    print(f"{station['place']}: {station['value']}°C")
```

## 自動化使用

可將腳本加入 cron 定時任務：

```bash
# 每小時檢查天氣
0 * * * * python3 /path/to/fetch_weather.py --type current >> /var/log/hko_weather.log

# 每 10 分鐘檢查警告
*/10 * * * * python3 /path/to/check_warnings.py >> /var/log/hko_warnings.log
```

## 故障排查

**問題**: 腳本返回網絡錯誤

**解決**:
1. 確認網絡連接正常
2. 確認 API 基址正確：`https://data.weather.gov.hk/weatherAPI/opendata/weather.php`
3. 確認 dataType 參數正確：`rhrread`, `fnd`, `flw`, `warnsum`

**問題**: 返回空數據或 N/A

**說明**: 
- API 可能返回空對象 (`{}`) 表示無數據 (如無天氣警告)
- 部分字段可能為空字符串 (如 `uvindex`)
- 檢查 API 回應的實際結構

**問題**: JSON 解析錯誤

**解決**:
1. 使用 `--json` 參數查看原始回應
2. 確認 API 返回有效 JSON
3. 檢查網絡連接是否穩定

## API dataType 速查

| 需求 | dataType |
|------|----------|
| 當前天氣 | `rhrread` |
| 九天預報 | `fnd` |
| 本地預報 | `flw` |
| 天氣警告 | `warnsum` |

⚠️ **注意**: 以下為錯誤/過時的 dataType，請勿使用：
- ❌ `CurrentWeatherReport` (應使用 `rhrread`)
- ❌ `NineDayWeatherForecast` (應使用 `fnd`)
- ❌ `WarningSummary` (應使用 `warnsum`)

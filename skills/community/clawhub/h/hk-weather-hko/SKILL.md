---
name: hk-weather-hko
description: 香港天文台 (HKO) 開放數據 API 查詢技能。用於獲取香港天氣數據，包括：(1) 全港即時天氣，(2) 分區天氣 (港島/九龍/新界/離島)，(3) 天氣預報 (每小時/九天)，(4) 天氣警告 (暴雨/颱風/高溫等)。當用戶查詢香港天氣、請求天氣預報、或需要了解生效中天氣警告時使用此技能。
---

# 香港天氣查詢技能

本技能提供調用香港天文台 (HKO) 開放數據 API 的完整指導，無需 API Key，完全免費。

## API 基礎資訊

- **基址**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php`
- **認證**: 無需 API Key
- **回應格式**: JSON
- **語言參數**: `lang=en` (英文) 或 `lang=tc` (繁體中文)
- **官方文檔**: 見 `references/api-docs.md`

## 核心端點速查

| 需求 | dataType | 說明 | 更新頻率 |
|------|----------|------|----------|
| 全港即時天氣 | `rhrread` | 當前天氣報告 (含分區數據) | 每小時 |
| **分區天氣** | `rhrread` | **指定地區氣溫** (例如：沙田、銅鑼灣) | 每小時 |
| 本地天氣預報 | `flw` | 本地天氣預報 | 每小時 |
| 九天預報 | `fnd` | 九天天氣預報 | 每日 2 次 |
| 天氣警告摘要 | `warnsum` | 天氣警告摘要 | 即時 |
| 天氣警告詳情 | `warningInfo` | 詳細天氣警告資訊 | 即時 |
| 特別天氣提示 | `swt` | 特別天氣提示 | 即時 |

⚠️ **注意**: 分區天氣數據包含在 `rhrread` 回應中，為臨時數據，僅經有限度驗證。

## 標準調用流程

### 步驟 1: 確定用戶需求

詢問或確認用戶需要：
- 當前天氣還是預報？
- 全港還是特定分區？
- 是否需要天氣警告資訊？

### 步驟 2: 調用腳本獲取天氣數據 ⭐

**優先使用腳本**，而非直接調用 API。腳本已處理 API 請求、JSON parsing 同錯誤處理。

**標準命令**：

```bash
# 全港即時天氣 (含分區氣溫)
python3 {baseDir}/scripts/fetch_weather.py --type current

# 指定地區天氣 (例如：沙田)
python3 {baseDir}/scripts/fetch_weather.py --type regional --location 沙田

# 九天預報
python3 {baseDir}/scripts/fetch_weather.py --type forecast --days 9

# 3 天預報
python3 {baseDir}/scripts/fetch_weather.py --type forecast --days 3

# 本地天氣預報 (概況)
python3 {baseDir}/scripts/fetch_weather.py --type hourly

# 檢查天氣警告
python3 {baseDir}/scripts/check_warnings.py

# 僅檢查關鍵警告 (暴雨/颱風等)
python3 {baseDir}/scripts/check_warnings.py --critical
```

### 步驟 3: 呈現結果

以清晰格式向用戶展示天氣資訊，包括：
- 溫度、濕度
- 風向、風速
- 預報趨勢 (如適用)
- 生效中警告 (如適用)

**註**: 除非腳本 unavailable，否則避免直接用 `web_fetch` 調用 API。

## 使用腳本

本技能提供以下腳本：

| 腳本 | 用途 |
|------|------|
| `scripts/fetch_weather.py` | 獲取並解析天氣數據 |
| `scripts/check_warnings.py` | 檢查生效中天氣警告 |

**使用示例**:

```bash
# 全港即時天氣 (含分區氣溫)
python3 {baseDir}/scripts/fetch_weather.py --type current

# 指定地區天氣 (例如：沙田)
python3 {baseDir}/scripts/fetch_weather.py --type regional --location 沙田

# 指定地區天氣 (例如：香港天文台)
python3 {baseDir}/scripts/fetch_weather.py --type regional --location 香港天文台

# 顯示所有分區氣溫
python3 {baseDir}/scripts/fetch_weather.py --type regional

# 九天預報
python3 {baseDir}/scripts/fetch_weather.py --type forecast --days 9

# 3 天預報
python3 {baseDir}/scripts/fetch_weather.py --type forecast --days 3

# 本地天氣預報 (概況)
python3 {baseDir}/scripts/fetch_weather.py --type hourly

# 降雨資訊 (過去一小時分區降雨量)
python3 {baseDir}/scripts/fetch_weather.py --type rainfall

# 降雨預報 (未來幾日會唔會落雨)
python3 {baseDir}/scripts/fetch_weather.py --type rainfall-forecast --days 9

# 降雨預報 (未來 3 日)
python3 {baseDir}/scripts/fetch_weather.py --type rainfall-forecast --days 3

# 檢查天氣警告
python3 {baseDir}/scripts/check_warnings.py

# 僅檢查關鍵警告 (暴雨/颱風等)
python3 {baseDir}/scripts/check_warnings.py --critical

# 輸出原始 JSON
python3 {baseDir}/scripts/fetch_weather.py --type current --json
```

詳細腳本文檔見 `references/scripts.md`。

## 參考資料

- **API 完整文檔**: `references/api-docs.md`
- **腳本使用說明**: `references/scripts.md`
- **分區代碼對照表**: `references/regions.md`
- **天氣警告類型說明**: `references/warnings.md`

## 注意事項

1. **使用條款**:
   - 本專案代碼（Code）以 MIT 等開源授權釋出；資料使用受香港天文台使用條款約束，商業用途可能需要天文台書面授權（見 references/api-docs.md）。
   - 請於輸出中清楚註明資料來源為「香港天文台」，並必要時展示免責聲明（見 references/terms-and-attribution.md）。
   - 不可用於航空、航海等安全關鍵應用。
   - 不可誤導用戶認為本專案與香港天文台有正式合作或背後授權。

2. **錯誤處理**:
   - API 可能返回 404 或其他 HTTP 錯誤
   - 建議加入重試機制
   - 檢查 JSON 回應中的 error 欄位

3. **數據限制**:
   - 分區天氣為臨時數據
   - 預報數據可能隨更新調整
   - 警告資訊以天文台官方發布為準

## 觸發場景

當用戶提出以下類型的請求時，應使用本技能：

- 「香港今日天氣點？」
- 「聽日落唔落雨？」
- 「有冇暴雨警告？」
- 「九龍區而家幾度？」
- 「未來幾日天氣點？」
- 「有冇颱風警告？」

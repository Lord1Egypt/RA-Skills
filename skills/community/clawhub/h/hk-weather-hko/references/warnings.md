# 天氣警告（warnsum / warningInfo）

> 資料來源：香港天文台（HKO）開放數據 API

本 skill 目前主要使用：
- `dataType=warnsum`：天氣警告摘要（最常用、最適合聊天回覆）

另有：
- `dataType=warningInfo`：部分警告提供更詳細資訊（如需要可再擴展）

## warnsum 回應重點

常見欄位（實際以 HKO 回應為準）：
- `warningSummary[]`
  - `warningType`
  - `name`（可能係物件：`{ tc, en }`）
  - `status`（例如 `ISSUED`）
  - `effectiveTime`

## 常見警告類型（示例）

實際 `warningType` 會因應 HKO 定義而變更；建議程式對未知 code 以原樣顯示。

- 暴雨警告（Rainstorm）
- 熱帶氣旋 / 颱風警告（Tropical Cyclone）
- 山泥傾瀉警告
- 山洪暴發警告
- 寒冷 / 酷熱天氣警告
- 火災危險警告

## 建議顯示策略

- 無警告：回覆「✅ 目前無生效中天氣警告」
- 有警告：
  - 顯示中文名稱（tc）
  - 顯示 status + 生效時間（如有）
  - 如要「critical mode」：聚焦暴雨 / 颱風 / 山泥傾瀉 / 山洪等高風險項

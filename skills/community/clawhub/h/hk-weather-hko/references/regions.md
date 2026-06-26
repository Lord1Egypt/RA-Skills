# 分區 / 監測站（rhrread temperature.data）

> 資料來源：香港天文台（HKO）開放數據 API：`dataType=rhrread`

`rhrread` 回應包含 `temperature.data[]`（以及 `rainfall.data[]` 等），每個元素都有 `place` 欄位（監測站/地點名稱）。

## 如何取得最新列表

建議用腳本直接列出：

```bash
python3 {baseDir}/scripts/fetch_weather.py --type regional --json
```

然後檢查：
- `temperature.data[].place`
- `rainfall.data[].place`

## 例子（常見地點）

以下係常見監測站（實際以 API 回應為準，可能增減/改名）：

- 香港天文台
- 京士柏
- 黃竹坑
- 打鼓嶺
- 流浮山
- 大埔
- 沙田
- 屯門
- 元朗
- 荃灣
- 赤鱲角
- 迪士尼樂園
- 中環
- 灣仔
- 銅鑼灣
- 維多利亞公園
- 尖沙咀
- 九龍城
- 赤柱

## 建議（用戶輸入地點處理）

- 先做「包含/模糊匹配」
- 找唔到時：回覆 Top N 候選（例如 10 個），提示用戶改寫
- 避免將用戶輸入拼入 shell 指令

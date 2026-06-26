---
name: 台灣即時停車查詢
description: 傳送定位點或 Google Maps 網址，查詢附近台灣停車場即時空位，附 Apple Maps / Google Maps 一鍵導航連結。支援 Telegram、LINE、iMessage。
---

# parking_query

透過 Telegram 或 iMessage 傳送定位點或 Google Maps 網址，即可查詢附近台灣停車場的即時空位，並附上一鍵導航連結。

## 功能

- **即時查詢**：顯示附近有空位的停車場 + 即時格位數 + Apple Maps / Google Maps 導航連結
- **未來查詢**（訊息含「明天」、「下午」等時間詞）：顯示附近停車場位置 + 導航連結
- 搜尋半徑：500 公尺，無結果自動擴展至 1 公里
- 最多回傳 5 筆，依距離排序
- 覆蓋範圍：全台主要縣市（TDX 有提供資料者）

## 使用情境

```
用戶傳送：[定位點]
回覆：
🅿️ 附近 500 公尺 有空位的停車場（Taipei）

1. 信義廣場地下停車場
   空位：41 個　距離：103 公尺
   信義路5段11號地下
   🍎 Apple Maps → https://maps.apple.com/?daddr=...
   🗺 Google Maps → https://www.google.com/maps/dir/...
```

適用頻道：Telegram、LINE、iMessage（BlueBubbles）、及其他 OpenClaw 支援的頻道

支援輸入格式：
- Telegram / LINE 定位點（直接取座標）
- Google Maps 短網址：`maps.app.goo.gl/xxx`
- Google Maps 完整網址：`google.com/maps/@lat,lon,...`

## 前置需求

### 1. 申請 TDX 帳號（免費）

前往 [https://tdx.transportdata.tw](https://tdx.transportdata.tw) 註冊，取得：
- `Client ID`
- `Client Secret`

> 免費方案每月有 API 呼叫次數限制，一般個人使用綽綽有餘。

### 2. 設定環境變數

在 OpenClaw 的 `openclaw.json` 中加入：

```json
{
  "env": {
    "vars": {
      "TDX_CLIENT_ID": "your-client-id",
      "TDX_CLIENT_SECRET": "your-client-secret"
    }
  }
}
```

### 3. 安裝 Python 套件

```bash
pip3 install requests
```

## 安裝

```bash
# 複製到 OpenClaw skills 目錄
cp -r parking_query ~/.openclaw/skills/

# 重啟 gateway 讓 skill 生效
openclaw restart
```

## 使用方式

Agent 會自動判斷模式並呼叫此 skill。也可直接執行：

```bash
# 即時查詢（現在要停車）
python3 ~/.openclaw/skills/parking_query/parking_query.py \
  --lat 25.033 --lon 121.565 --mode realtime

# 未來查詢（明天要去的地點）
python3 ~/.openclaw/skills/parking_query/parking_query.py \
  --lat 25.033 --lon 121.565 --mode future

# Google Maps 短網址
python3 ~/.openclaw/skills/parking_query/parking_query.py \
  --url "https://maps.app.goo.gl/xxx" --mode realtime
```

## 資料來源

| 用途 | API | Tier |
|---|---|---|
| 停車場位置（靜態） | TDX `/api/advanced/v1/Parking/OffStreet/CarPark/NearBy` | Advanced |
| 即時空位（動態） | TDX `/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/{City}` | Basic |

快取策略：停車場靜態資料快取 24 小時（減少 API 呼叫），即時空位每次查詢都打 API。

## 覆蓋縣市

基隆、台北、新北、桃園、新竹市、新竹縣、苗栗、台中、彰化、南投、雲林、嘉義市、嘉義縣、台南、高雄、屏東、宜蘭、花蓮、台東

> 實際空位資料以 TDX 各縣市介接狀況為準，部分縣市可能無即時資料。

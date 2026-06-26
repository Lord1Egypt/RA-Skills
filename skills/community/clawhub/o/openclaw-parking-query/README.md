# 🅿️ openclaw-parking-query

全台即時停車查詢 OpenClaw Skill，透過 Telegram、LINE 或 iMessage 傳送定位點或 Google Maps 網址，即可查詢附近有空位的停車場並附上一鍵導航連結。

## 功能示範

```
你：[傳送定位點]

助理：
🅿️ 附近 500 公尺 有空位的停車場（Taipei）

1. 信義廣場地下停車場
   空位：41 個　距離：103 公尺
   信義路5段11號地下
   🍎 Apple Maps → https://maps.apple.com/?daddr=25.033,121.566&dirflg=d
   🗺 Google Maps → https://www.google.com/maps/dir/?api=1&destination=25.033,121.566&travelmode=driving

2. 三張里地下停車場
   空位：60 個　距離：301 公尺
   ...
```

## 特色

- **雙模式自動判斷**：訊息含時間詞（「明天」、「下午」等）→ 未來模式，只列停車場位置；純定位 → 即時模式，顯示空位數
- **三種輸入格式**：Telegram / LINE 定位點、Google Maps 短網址（`maps.app.goo.gl/xxx`）、完整 Google Maps URL
- **智慧搜尋半徑**：先搜 500 公尺，若無結果自動擴展至 1 公里
- **一鍵導航**：每筆結果附 Apple Maps 與 Google Maps 導航連結
- **全台覆蓋**：基隆、台北、新北、桃園、新竹、台中、台南、高雄等主要縣市
- **適用頻道**：Telegram、LINE、iMessage（BlueBubbles）及其他 OpenClaw 支援頻道

## 前置需求

### 1. OpenClaw

請先安裝並設定 [OpenClaw](https://github.com/openclaw/openclaw)。

### 2. TDX API 金鑰（免費）

前往 [tdx.transportdata.tw](https://tdx.transportdata.tw) 註冊帳號，取得：
- `Client ID`
- `Client Secret`

> 交通部官方開放資料平台，免費方案已足夠個人使用。

### 3. Python 套件

```bash
pip3 install requests
```

## 安裝

```bash
# 1. clone 到 OpenClaw skills 目錄
git clone https://github.com/Harperbot/openclaw-parking-query.git \
  ~/.openclaw/skills/parking_query

# 2. 設定 TDX 金鑰（加入 openclaw.json 的 env.vars）
#    TDX_CLIENT_ID: "your-client-id"
#    TDX_CLIENT_SECRET: "your-client-secret"

# 3. 重啟 gateway
openclaw restart
```

## 設定 TDX 金鑰

在 `~/.openclaw/openclaw.json` 的 `env.vars` 區塊加入：

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

## 直接執行（測試用）

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

## 更新

```bash
bash ~/.openclaw/skills/parking_query/update.sh
```

或手動：

```bash
cd ~/.openclaw/skills/parking_query && git pull
```

## 資料來源

| 用途 | 來源 |
|---|---|
| 停車場位置（靜態） | [TDX](https://tdx.transportdata.tw) `/api/advanced/v1/Parking/OffStreet/CarPark/NearBy` |
| 即時空位（動態） | [TDX](https://tdx.transportdata.tw) `/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/{City}` |

靜態資料快取 24 小時，即時空位每次查詢即時取得。

## License

MIT

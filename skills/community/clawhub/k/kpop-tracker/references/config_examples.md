# Config Examples (V2.1.0)

## 新架構說明

V2.1.0 引入新的 config 架構：
- 新增 `chinese_members` 欄位：中國成員微博監控
- `fan_accounts` 改為 `taiwan_fan_sources`：台灣粉絲團來源
- 3階段搜尋：官方 → 媒體 → 台灣粉絲團

## Single Artist with Chinese Member

```json
{
  "artists": [
    {
      "name": "I-DLE",
      "group": "I-DLE",
      "keywords": ["I-DLE", "아이들", "idle", "IDLE", "여자아이들"],
      "chinese_members": [
        {
          "name": "雨琦",
          "weibo": "@Song_Yuqi"
        }
      ],
      "sources": {
        "instagram": "https://www.instagram.com/i_dle_official/",
        "x": "https://x.com/official_i_dle",
        "youtube": "https://www.youtube.com/@G_I_DLE",
        "weverse": "",
        "berriz": "https://berriz.in/i-dle",
        "taiwan_fan_sources": []
      }
    }
  ],
  "last_check": null,
  "check_history_file": "kpop-tracker/check_history.json"
}
```

## Multiple Artists (Mixed)

```json
{
  "artists": [
    {
      "name": "I-DLE",
      "group": "I-DLE", 
      "keywords": ["I-DLE", "아이들", "idle"],
      "chinese_members": [
        {
          "name": "雨琦",
          "weibo": "@Song_Yuqi"
        }
      ],
      "sources": {
        "instagram": "https://www.instagram.com/i_dle_official/",
        "x": "https://x.com/official_i_dle",
        "youtube": "https://www.youtube.com/@G_I_DLE",
        "weverse": "",
        "berriz": "https://berriz.in/i-dle",
        "taiwan_fan_sources": []
      }
    },
    {
      "name": "BLACKPINK",
      "group": "BLACKPINK",
      "keywords": ["BLACKPINK", "블랙핑크", "blackpink"],
      "chinese_members": [],
      "sources": {
        "instagram": "https://www.instagram.com/blackpinkofficial/",
        "x": "https://x.com/BLACKPINK",
        "youtube": "https://www.youtube.com/@BLACKPINK",
        "weverse": "https://weverse.io/blackpink/feed",
        "berriz": "",
        "taiwan_fan_sources": [
          "台灣 BLACKPINK 粉絲團"
        ]
      }
    }
  ],
  "last_check": null,
  "check_history_file": "kpop-tracker/check_history.json"
}
```

## 官方帳號對照表 (Updated 2026.04.13)

| Group/Artist | Instagram | X | YouTube | Berriz | 中國成員微博 |
|-------------|-----------|---|---------|---------|-------------|
| **I-DLE** | @i_dle_official | @official_i_dle | @G_I_DLE | berriz.in/i-dle | 雨琦: @Song_Yuqi |
| **BLACKPINK** | @blackpinkofficial | @BLACKPINK | @BLACKPINK | - | - |
| **IVE** | @ivestarship | @IVEstarship | @ivestarship | berriz.in/ive | - |
| **Rosé** | @roses_are_rosie | @THEBLACKLABEL | @ROSE | - | - |
| **Jennie** | @jennierubyjane | @ODDATELIER | @jennierubyjane | - | - |
| **Lisa** | @lalalalisa_m | @wearelloud | @lalaborntodance | - | - |
| **Jisoo** | @sooyaaa__ | @officialBLISSOO | @officialBLISSOO | - | - |
| **薇娟 (Miyeon)** | @noodle.zip | - | - | - | - |
| **雨琦 (Yuqi)** | @yuqisong_ | - | @yuqisong | - | @Song_Yuqi |
| **米妮 (Minnie)** | @min.nicha | - | - | - | - |

## 新功能說明

### 🇺🇳 中國成員微博監控
- 自動檢查團體中國成員的微博動態
- 需要在 `chinese_members` 欄位設定微博帳號
- 支援多位中國成員

### 🇹🇼 台灣粉絲團來源
- 取代原先的 `fan_accounts`
- 專注於台灣地區的粉絲社群和媒體
- 支援購買資訊、演唱會消息等在地化內容

### 📊 3階段搜尋架構
1. **官方帳號檢查**：IG、Berriz/Weverse、X、YouTube、微博
2. **新聞媒體搜尋**：韓國媒體、訪談節目、國際媒體
3. **台灣粉絲團消息**：台灣社群、購買資訊

### 🏷️ 來源標註系統
- 🏢 官方帳號
- 📰 新聞媒體
- 🇺🇳 微博 (中國成員)
- 🇹🇼 台灣粉絲團/媒體
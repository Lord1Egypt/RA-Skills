---
name: daily-observatory-lite
description: Daily automated health check + mood tracking + proactive alerts for OpenClaw agents
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔭"
    homepage: https://github.com/lalawgwg99/daily-observatory-lite
    license: MIT-0
---

# Daily-Observatory Lite 🔭

## 概述

Daily-Observatory Lite 是一個**無感自動**的每日觀察站，幫你掌握 OpenClaw agent 的整體狀態：

- **系統健康**：Gateway、記憶結構、技能狀態
- **情緒溫度**：從 EMOJI-JOURNAL.md 分析趨勢
- **待辦預警**：P0-P1 卡住任務主動提醒
- **主動推播**：每天 08:00 / 23:00 自動推送到 Telegram

## 核心價值

**不是記錄，是預警**  
**不是單日，是趨勢**  
**不是被動，是主動**

## 安裝

```bash
clawhub install daily-observatory-lite
```

## 使用方式

### 自動執行（推薦）
skill 會自動在設定時間執行，並推送到 Telegram：

```bash
# 修正 crontab（如果沒有自動設定）
crontab -e
# 加入：
# 0 8 * * * openclaw agent --agent daily-observatory-lite --message "run" --deliver
# 0 23 * * * openclaw agent --agent daily-observatory-lite --message "run" --deliver
```

### 手動執行
```bash
openclaw agent --agent daily-observatory-lite --message "run" --deliver
```

## 輸出範例

### 🌅 早上 08:00 日誌
```
🔭 Daily-Observatory Lite · 2026-03-25 08:00

✅ 系統健康
├─ Gateway: 正常 (v1.2.3)
├─ 記憶結構: 完整
└─ 技能狀態: 24 個正常

😐 情緒溫度
├─ 今日: 0.65 (😌)
├─ 昨日: 0.45 (😐)
└─ 趨勢: ↗ +0.20

⚠️ 待辦預警
├─ P0 卡住: 1 個 (重構 authentication · 5 天)
└─ P1 卡住: 2 個

💡 建議: 注意 P0 阻塞任務
```

### 🌙 晚上 23:00 日誌
```
🔭 Daily-Observatory Lite · 2026-03-25 23:00

✅ 系統健康
├─ Gateway: 正常 (v1.2.3)
├─ 記憶結構: 完整
└─ 技能狀態: 24 個正常

😌 情緒溫度
├─ 今日: 0.60 (穩定)
└─ 趨勢: → 平穩

⚠️ 待辦預警
├─ P0 卡住: 0 個
└─ P1 卡住: 1 個

💡 建議: 今日完成率 80%，保持節奏
```

## 設定

### 檔案：`daily-observatory-lite/config.json`
```json
{
  "schedule": {
    "morning": "08:00",
    "evening": "23:00"
  },
  "channels": {
    "telegram": true,
    "telegram_chat_id": "YOUR_CHAT_ID"
  },
  "modules": {
    "system_health": true,
    "emotion_tracking": true,
    "todo_alerts": true
  }
}
```

## 差異化亮點

| 現有 skill | Daily-Observatory Lite |
|------------|----------------------|
| 只記錄 | **記錄 + 預警** |
| 被動查詢 | **主動推播** |
| 單日視角 | **趨勢分析** |
| 沒系統檢測 | **三合一健康檢查** |

## 授權

MIT-0

---


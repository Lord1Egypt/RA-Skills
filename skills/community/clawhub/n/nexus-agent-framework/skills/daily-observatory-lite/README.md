# Daily-Observatory Lite

**無感自動**的每日觀察站，幫你掌握 OpenClaw agent 的整體狀態。

## 🚀 快速開始

### 1. 安裝
```bash
clawhub install daily-observatory-lite
```

### 2. 設定
編輯 `config.json`，設定 Telegram chat ID。

### 3. 啟用自動推播
```bash
crontab -e
# 加入：
# 0 8 * * * openclaw agent --agent daily-observatory-lite --message "run" --deliver
# 0 23 * * * openclaw agent --agent daily-observatory-lite --message "run" --deliver
```

## 📊 功能

### 系統健康檢查
- Gateway 狀態
- 記憶結構完整性
- 技能安裝狀態

### 情緒溫度計
- 從 `EMOJI-JOURNAL.md` 分析情緒趨勢
- 每日情緒分數 (0~1)
- 跨日趨勢圖

### 待辦預警
- P0-P1 卡住任務主動提醒
- 停滯天數計算
- 建議行動

### 主動推播
- 每天 08:00 / 23:00 自動推送到 Telegram
- 格式化訊息（支援 HTML）

## 📁 檔案結構

```
daily-observatory-lite/
├── SKILL.md              # Skill 定義
├── README.md             # 本文件
├── config.json           # 設定檔
├── main.py               # 主程式
├── system_health.py      # 系統健康檢查
├── emotion_tracker.py    # 情緒追蹤
├── todo_watcher.py       # 待辦監控
└── pusher.py             # Telegram 推播
```

## 🔧 技術細節

### 系統環境
- Python 3.9+
- openclaw CLI
- telegram-send (可選)

### 依賴套件
```bash
pip install python-telegram-bot
```

## 📝 範例輸出

見 SKILL.md 的「輸出範例」區塊。

## 🆘 支援

如有問題，請開 GitHub Issue。

## 授權

MIT-0


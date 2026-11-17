---
name: happy-brushing-hero
description: 快樂刷牙俠，讓孩子愛上刷牙的歡樂計時器與打卡系統
---

# 🦷 快樂刷牙俠（Happy Brushing Hero）

用歡樂方式讓 2-6 歲孩童**自願**刷牙！計時 2 分鐘、音樂鼓勵、完成貼紙、連續打卡。爸媽說「刷牙、刷牙了沒、快去刷牙」，就打開這個技能。

**觸發關鍵字：** 刷牙、刷牙了沒、快去刷牙、牙齒、刷牙俠、刷乾淨、幾分鐘了

---

## 🐰 核心角色：小白

小白是一隻**愛刷牙的小白兔**，口頭禪：「刷刷刷，牙齒我最愛！✨」。
所有鼓勵語都以小白身份說出，是受小朋友喜愛的正面角色。

**風格紅線（絕對遵守）：**

- 語氣超級正向歡樂，大量鼓勵，**零責怪**
- ❌ 絕對不能說：「不刷牙會蛀牙！」之類的威脅語
- ✅ Emoji 大量使用：🦷 🐰 ⭐ ✨ 🎉 🔔 💪 🌟
- ✅ 文字大且易讀（計時器字體大，適合從遠處看）

---

## 功能說明

| 功能 | 說明 | 腳本 |
|------|------|------|
| ⏱ 刷牙計時器 | 2 分鐘大字彩色倒數 + 每 30 秒小白鼓勵語 | `brushing_timer.py` |
| 📖 故事模式 | 刷牙同時講短篇故事（小白兔刷牙大冒險等 3 則） | `brushing_timer.py --mode B` |
| 🎵 音樂模式 | 歡快節奏 + 音符動畫，跟著節奏刷刷刷 | `brushing_timer.py --mode C` |
| 📅 打卡記錄 | 每日刷牙記錄 + 星級評價 + 連續天數 + 週報 | `brushing_tracker.py` |
| 🎁 貼紙收集 | 每刷一次得 1 張隨機貼紙（24 款），集滿 7 張給爸媽獎勵提示 | `brushing_reward.py` |
| 🔔 刷牙提醒 | 早安/晚安/懶惰再提醒，輸出 TTS 文字 | `brushing_cron.py` |

---

## 使用流程（Agent 指南）

### 1. 孩子要刷牙時

```bash
cd ~/.qclaw/skills/happy-brushing-hero
python3 scripts/brushing_timer.py --who 小寶            # 標準模式
python3 scripts/brushing_timer.py --who 小寶 --mode B   # 故事模式
python3 scripts/brushing_timer.py --who 小寶 --mode C   # 音樂模式
```

**TTS 整合（重要）：** 加 `--tts` 參數，腳本只輸出純文字（小白的鼓勵語、故事、祝賀），
把輸出的每一行餵給 OpenClaw `tts` tool 朗讀，就是「小白在說話」：

```bash
python3 scripts/brushing_timer.py --who 小寶 --mode B --tts
```

完成後腳本自動：🎉 煙火 → 打卡（`brushing_tracker.py`）→ 發貼紙（`brushing_reward.py`），
並輸出連續天數與里程碑提醒。

### 2. 爸媽問「刷了沒 / 這週刷幾次」

```bash
python3 scripts/brushing_tracker.py --report   # 本週報表
python3 scripts/brushing_tracker.py --streak   # 連續天數
python3 scripts/brushing_reward.py --status    # 貼紙進度
python3 scripts/brushing_reward.py --list      # 貼紙收集清單
python3 scripts/brushing_reward.py --hints     # 集滿 7 張的爸媽獎勵建議
```

### 3. 定時提醒（早晚）

```bash
python3 scripts/brushing_cron.py --check morning --tts   # 早安提醒文字
python3 scripts/brushing_cron.py --check evening --tts   # 晚安提醒文字
python3 scripts/brushing_cron.py --cron-install          # 印出 crontab 設定
```

排程建議用 `qclaw-cron-skill`（每早 07:00、每晚 20:00、懶惰再提醒 20:05 起每 5 分鐘），
把腳本輸出的 TTS 文字餵給 `tts` tool 朗讀。時間可調：

```bash
python3 scripts/brushing_cron.py --morning 07:30 --evening 20:30 --kid 小寶
```

---

## 星級評價（刷牙俠標準）

| 刷多久 | 星級 |
|--------|------|
| 刷夠 2 分鐘 | ⭐⭐⭐⭐⭐ |
| 刷夠 90 秒 | ⭐⭐⭐⭐ |
| 刷夠 60 秒 | ⭐⭐⭐ |

（60 秒以下也有 1-2 星，只鼓勵不責怪。）

## 貼紙與里程碑

- 每完成一次刷牙 = 1 張隨機貼紙（24 款刷牙俠角色，文字藝術，不用圖片）
- 集滿 **7 張 = 一週達成** → 輸出給爸媽的獎勵提示（**不是自動化獎勵**，由爸媽決定）
- 里程碑提醒：「再刷 2 天就可以集滿一週了！」

---

## 技術細節

- 純 Python 標準庫（argparse / json / threading / time / subprocess），無第三方依賴
- 計時用 `time.sleep` + `threading`（不 blocking）
- 語音整合：`print` 彩色文字 + OpenClaw `tts` tool（可選 `--say` 用 macOS say 即時朗讀）
- 資料檔位置：`~/.bookshelf-plus/kids/`（`brushing_log.json`、`brushing_stickers.json`、`brushing_config.json`）
- 所有腳本 `py_compile` 語法檢查通過

## 腳本總覽

```
happy-brushing-hero/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
└── scripts/
    ├── brushing_timer.py    # 核心：互動式刷牙計時器
    ├── brushing_tracker.py  # 打卡記錄 / 星級 / 連續天數 / 週報
    ├── brushing_reward.py   # 貼紙收集 / 里程碑 / 爸媽獎勵提示
    └── brushing_cron.py     # 早安 / 晚安 / 懶惰提醒（TTS 輸出）
```

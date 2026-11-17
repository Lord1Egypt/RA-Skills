# 🦷 快樂刷牙俠（Happy Brushing Hero）

> 用歡樂方式讓 2-6 歲孩童**自願**刷牙！計時 2 分鐘、音樂鼓勵、完成貼紙、連續打卡。

**觸發關鍵字：** 刷牙、刷牙了沒、快去刷牙、牙齒、刷牙俠、刷乾淨、幾分鐘了

## 🐰 小白是誰？

小白是一隻**愛刷牙的小白兔**，口頭禪：「刷刷刷，牙齒我最愛！✨」。
他是小朋友的好朋友，負責在刷牙時間加油打氣、講故事、發貼紙。

**我們的原則：** 超級正向歡樂、大量鼓勵、**零責怪**。絕不說「不刷牙會蛀牙！」這種威脅語。

## ✨ 功能

- **⏱ 刷牙計時器** — 2 分鐘大字彩色倒數，每 30 秒輪播一句小白的鼓勵語
- **📖 故事模式** — 刷牙同時聽短篇故事（小白兔刷牙大冒險、太空牙刷任務、小恐龍的亮晶晶牙齒）
- **🎵 音樂模式** — 歡快節奏音符動畫，跟著節奏刷刷刷
- **📅 打卡系統** — 每日記錄、星級評價、連續天數、週報表
- **🎁 貼紙收集** — 每刷一次得 1 張隨機刷牙俠貼紙（24 款），集滿 7 張給爸媽獎勵提示
- **🔔 刷牙提醒** — 早安 / 晚安 / 懶惰再提醒（輸出 TTS 語音文字）

## 🚀 快速開始

```bash
cd ~/.qclaw/skills/happy-brushing-hero

# 標準模式：刷 2 分鐘
python3 scripts/brushing_timer.py --who 小寶

# 故事模式（刷牙聽故事）
python3 scripts/brushing_timer.py --who 小寶 --mode B

# 音樂模式
python3 scripts/brushing_timer.py --who 小寶 --mode C

# TTS 模式：只輸出小白的話（餵給語音朗讀）
python3 scripts/brushing_timer.py --who 小寶 --mode B --tts
```

完成後自動：🎉 煙火慶祝 → 打卡 → 發貼紙 → 顯示連續天數與里程碑。

## 📊 查詢

```bash
python3 scripts/brushing_tracker.py --report   # 本週報表
python3 scripts/brushing_tracker.py --streak   # 連續刷牙天數
python3 scripts/brushing_reward.py --status    # 貼紙進度與里程碑
python3 scripts/brushing_reward.py --list      # 貼紙收集清單
python3 scripts/brushing_reward.py --hints     # 集滿 7 張的獎勵建議（給爸媽）
```

## 🔔 定時提醒

```bash
python3 scripts/brushing_cron.py --check morning --tts   # 早安提醒
python3 scripts/brushing_cron.py --check evening --tts   # 晚安提醒
python3 scripts/brushing_cron.py --cron-install          # 印出 crontab 設定
python3 scripts/brushing_cron.py --morning 07:30 --evening 20:30   # 調整時間
```

預設：早安 07:00-08:00、晚安 20:00-21:00。過了時間還沒刷，5 分鐘後會溫柔再提醒一次（有冷卻，不會吵人）。

## ⭐ 星級評價

| 刷多久 | 星級 |
|--------|------|
| 刷夠 2 分鐘 | ⭐⭐⭐⭐⭐ |
| 刷夠 90 秒 | ⭐⭐⭐⭐ |
| 刷夠 60 秒 | ⭐⭐⭐ |

## 🗂 資料檔

所有資料存在 `~/.bookshelf-plus/kids/`：

| 檔案 | 內容 |
|------|------|
| `brushing_log.json` | 每日刷牙記錄（日期、時間、誰、上下午、秒數、星級） |
| `brushing_stickers.json` | 貼紙收集紀錄 |
| `brushing_config.json` | 提醒時間與小朋友名字設定 |
| `brushing_reminder_state.json` | 懶惰提醒冷卻狀態 |

## 🛠 技術

- 純 Python 標準庫（無第三方依賴）
- 計時用 `time.sleep` + `threading`（不 blocking）
- 語音：`print` 彩色文字 + OpenClaw `tts` tool；可選 `--say` 用 macOS `say` 即時朗讀

## 📄 License

MIT License，詳見 [LICENSE](LICENSE)。

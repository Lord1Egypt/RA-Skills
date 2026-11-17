---
name: Idle Ping — Proactive Outreach System
slug: idle-ping
version: 1.0.0
description: Install a complete proactive outreach system — idle detection, randomized dice delivery, topic-driven crawler, share queue, and persona-based messages. Use when the user wants the agent to proactively reach out with interesting content during idle time.
metadata:
  clawdbot:
    emoji: 🎲
    requires:
      bins: [bash, python3]
    os: [linux, darwin]
---

# Idle Ping — 主動出擊系統

一套完整嘅「AI 主動出擊」系統：用戶 idle 一段時間後，agent 用骰仔機制隨機主動搵用戶傾偈，內容由每日 crawler 探索入倉（share-queue），再以 persona 語氣送出。

## When to Use

用戶要求：
- 「你 idle 嗰陣主動搵我傾偈」
- 「自動探索有趣內容然後隨機分享俾我」
- 「set up proactive outreach / idle ping」
- 任何「AI 主動搵人」「唔好等指令先郁」嘅需求

## Core Rules

1. **安裝**：`bash install.sh`——需要 `TELEGRAM_ID` 環境變數指定 delivery target；可選 `MODEL`、`IDLE_PING_WS` 等（見 `scripts/idle-ping.env.example`）
2. **安裝後**：install.sh 自動建立全部 cron jobs——gate（每分鐘擲骰）、crawler（每小時探索）、topic-factory（每晚補主題）、deep-explore（凌晨深度探索）、send/pause（gate 觸發）
3. **驗證**：`bash ci-local.sh` 跑本地檢查；`tests/` 有 bats 測試（gate 邏輯、監控）
4. **私隱**：runtime data（sessions.json、share-queue.db、state.json、cache/）一律唔 commit；路徑全部用 `$HOME`/`~` 或佔位符（`{{WORKSPACE}}`/`{{SESSIONS_JSON}}`），安裝時先替換
5. **Persona**：send/pause prompt 會嘗試讀 `SOUL.md`/`IDENTITY.md` 等 persona 文件——有就用人格語氣，冇就用預設語氣；系統本身 persona-agnostic
6. **機制**：探索（crawler/深度探索）同出貨（idle-ping）完全分開——出貨時機由骰仔決定，唔係固定時間表；用戶一覆 message 就 reset 計時

## 檔案結構

- `install.sh` — 一鍵安裝（建立 cron jobs + 複製 scripts + 設定 env）
- `scripts/` — `idle-ping-gate.sh`（骰仔門神）、`semantic-patrol.py`（主題探索）、`share-queue.py`（倉）、`topic-factory.py`（主題工廠）、`system-log.sh`、`watchdog.sh`
- `templates/` — 各 cron job 嘅 prompt（佔位符版，install 時替換成用戶環境）
- `tests/` — bats 測試
- `README.md` / `流程圖.md` — 完整文檔

## 組件

| 組件 | 時機 | 職責 |
|------|------|------|
| `idle-ping-gate` | 每分鐘 | 靜音窗口檢查 → idle ≥N 分鐘 → 擲骰 1/N → streak 管理 → 觸發 send |
| `idle-ping-crawler` | 每小時 | 主題驅動探索（news/arxiv/reddit/wiki/onthisday/misconceptions）→ 入倉 |
| `idle-ping-topic-factory` | 每晚 | 補齊 30 條探索主題 list |
| `idle-ping-deep-explore` | 凌晨 | 自主深度探索 → 4 條入倉（channel=deep） |
| `idle-ping-send` | gate 觸發 | DB-first 出貨：查倉 → 揀最正 → persona 語氣 send |
| `idle-ping-pause-notice` | gate 觸發 | 連續冇回應 → 「知你忙」通知 + 暫停骰仔 |

## 安裝後檢查清單

- [ ] `openclaw cron list` 見到全部 idle-ping jobs
- [ ] `curl -s localhost:11434/api/tags`（如果用 Ollama）有模型
- [ ] 靜音窗口（預設 23:00–08:00）內唔會觸發
- [ ] 用戶覆 message → `pingStreak` reset 0（自動重開）

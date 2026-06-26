# MEMORY.md — UUZero 長期記憶

> 跨 session 需要記住的重要事項。subagent 不會載入此檔。

## 系統配置

- 2026-03-18: 初始部署
- 2026-03-19: 優化 .md 檔案，建立 subagent 分派協議
- 2026-03-20: 重裝 openclaw，重新配置 providers（VectorEngine + OpenRouter）
- 2026-03-22: 精簡為 3 代理架構（frontdesk/architect/engineer），移除 buddy/freebie

## 當前架構（2026-03-24 更新）

- 🤖 UUZero: meta-llama/llama-3.3-70b-instruct:free → fallback mimo-v2-flash → stepfun:free
- 🏗️ Architect: meta-llama/llama-3.3-70b-instruct:free → fallback minimax-m2.5:free
- ⚙️ Engineer: deepseek-v3.2（寫碼專用）
- 原則：免費優先（llama）、必要才用付費、刀刃留給寫碼
- 語音 TTS：xiaomi mimo-v2-tts，台灣腔女聲，inbound 模式（語音入才語音出）
- 注意：stepfun 工具呼叫有問題（read tool 不帶 path 參數），只留做最後 fallback

## 使用者偏好

- Telegram ack 用 👀、thinking 用 🦄、其他不顯示
- 一律繁體中文
- 簡潔直接，不要廢話
- 修改設定檔要謹慎，改一項測一項
- Jazz 說「不是啦」= 你搞錯了，別急著辯解

## Nexus 框架整合（2026-03-24）

整合 Jazz 開發的 Nexus Agent Framework：
- `NEXUS.md`：四層記憶架構（L1 working → L2 daily → L3 長期 → L4 archive）+ 知識網路
- `EMOJI-JOURNAL.md`：情緒溫度計，讀 Jazz 狀態自動調整回應風格
- `WAL.md`：操作日誌規範，P0 破壞性操作記 `memory/wal.md`
- `memory/ideas.md`：跨 session 靈感紀錄
- 啟動時新增讀取：`EMOJI-JOURNAL.md` + `NEXUS.md`
- AGENTS.md 加入 P0-P4 優先級系統 + 5 層安全審計

## 重要決策

- 省錢策略：路由免費、日常免費優先付費兜底、只有寫碼用付費模型
- tools.profile 用 minimal + 明確 allow（group:sessions, group:runtime, group:memory, group:web, read, write）
- vectorengine provider 已移除，全部走 openrouter
- statusReactions：🤔thinking / 🔥tool / 👨‍💻coding / ⚡web / 👍done / 😱error / 🥱stallSoft / 😨stallHard / ✍compacting（Telegram 限制只能用特定 emoji）

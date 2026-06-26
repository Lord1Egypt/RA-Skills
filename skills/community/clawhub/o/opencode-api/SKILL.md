---
name: opencode-api
description: >
  透過 HTTP API 呼叫 OpenCode Server 進行 code review、程式碼分析與編碼任務。
  涵蓋：Agents（4種模式+自訂代理）、Custom Tools（TypeScript）、Formatters（ruff/biome）、
  Skills（載入技能）、SDK（完整 API，含結構化輸出/noReply/事件監聽）、Plugins（事件鉤子）、
  Config（完整 schema）、Permissions（細粒度規則）、Commands（自訂指令）、Providers（MCP/LM Studio/Ollama）、
  MCP（Model Context Protocol）、LSP（語言伺服器整合）、Server（HTTP 部署）。
  適用於 OpenClaw 派工給 OpenCode 執行的場景。
version: "3.0.0"
author: james53882
license: MIT
clawhub: https://clawhub.com/opencode-api
tags:
  - opencode
  - code-review
  - http-api
  - agents
  - custom-tools
  - formatters
  - skills
  - sdk
  - plugins
  - config
  - permissions
  - commands
  - providers
  - mcp
  - lsp
category: workflow
department: coding
languages:
  - zh
  - en
models:
  recommended:
    - minimax-portal/MiniMax-M2.7
  compatible:
    - minimax-portal/MiniMax-M2.5
    - minimax-portal/MiniMax-M2.7-highspeed
    - openai-codex/gpt-5.4
---

# OpenCode API Skill（完整版 v3.0）

透過 HTTP API 呼叫已啟動的 OpenCode Server，讓 OpenClaw 可以派工給 OpenCode 處理 code review、程式碼分析、編碼任務。

---

## 📚 目錄索引

需要哪個主題的詳細內容，請讀對應的 reference 檔案：

| 主題 | 檔案 | 說明 |
|------|------|------|
| 快速開始 | — | 直接看下方第 1 節 |
| Agents 系統 | `references/agents.md` | 四種內建代理 + 自訂代理 + 溫度/max_steps |
| SDK 完整 API | `references/sdk.md` | 端點表 + Python 對照 + 結構化輸出/事件監聽 |
| Custom Tools | `references/sdk.md` → 見上方 | TypeScript 工具定義 |
| Formatters + Keybinds + Share | `references/formatters.md` | 格式化器設定 + 快捷鍵 + 分享 |
| Config 完整設定 | `references/config.md` | 所有 schema 欄位 + 變數替換 |
| Permissions 權限 | `references/permissions.md` | 細粒度規則 + 預設值 |
| Commands 自訂指令 | `references/commands.md` | Markdown/JSON 格式 + 參數/Shell 輸出 |
| Tools 內建工具 | `references/tools.md` | 14 種工具一覽 + question 工具用法 |
| MCP 伺服器 | `references/mcp.md` | 本地/遠端 + OAuth + 常見設定範例 |
| LSP 整合 | `references/lsp.md` | 內建 LSP + 設定方式 |
| Providers 設定 | `references/providers.md` | LM Studio / Ollama / 自訂 Provider |
| Server 部署 | `references/server.md` | HTTP Server + 認證 + API 端點 |
| 派工範本 | 直接看下方第 5 節 | Minecraft-translate 專用 prompt |
| **強化 Code Review Checklist** | `references/review-checklist.md` | **必讀** — 每次 review 都要問的 6 大問題（Schema 對應實作、Pattern 邊界、常數清理、改動範圍、Error logging、向後相容）|

---

## 1. 快速開始

### Sub-agent import（推薦）

```python
import sys
sys.path.insert(0, "C:/Users/admin/.openclaw/workspace/skills/opencode-api/scripts")
from opencode_task import run_opencode_task, OpenCodeAPI

# 單次任務
result = run_opencode_task(
    prompt="請用繁體中文對以下程式碼進行 code review：\ndef foo(): pass",
    model="minimax/MiniMax-M2.7",
    reasoning="high",
)
print(result.text)
print(result.session_id)
print(result.ok)

# 多輪對話
client = OpenCodeAPI(auto_start=True)
sid = client.create_session(title="PR Review")
r1 = client.send_message("請 review...", session_id=sid, model="minimax/MiniMax-M2.7")
r2 = client.send_message("第三點再詳細點", session_id=sid)
```

### CLI

```bash
python scripts/opencode_task.py --prompt "請幫我分析這個函數" --model minimax/MiniMax-M2.7 --reasoning high
```

---

## 2. Scripts 總覽

| 檔案 | 用途 | 推薦場景 |
|------|------|----------|
| `opencode_task.py` | 乾淨的任務封裝（推薦）| 單次/多輪對話、sub-agent import |
| `opencode_client.py` | 完整 HTTP client | 需精細控制 API 底層，含 SDK 進階功能 |
| `opencode_review.py` | PR Review 專用 wrapper | 直接 review GitHub PR |

---

## 3. 模型速查

| 模型 ID | 名稱 | 思考支援 | 適合場景 |
|---------|------|----------|----------|
| `minimax/MiniMax-M2.7` | MiniMax M2.7 | ✅ | 性價比 coding（預設）|
| `minimax/MiniMax-M2.5` | MiniMax M2.5 | ✅ | 中等複雜度任務 |
| `minimax/MiniMax-M2.7-highspeed` | MiniMax M2.7 高速 | ✅ | 快速響應 |
| `big-pickle:high` | Big Pickle High | ✅ 16K tokens | 深度分析（免費）|
| `big-pickle:max` | Big Pickle Max | ✅ 32K tokens | 極深度推理（免費）|

查詢可用模型：`client.get_providers()`

---

## 4. 思考深度（reasoning）

| 值 | 說明 |
|----|------|
| `none` | 關閉 |
| `minimal` / `low` | 輕量思考 |
| `medium` | 標準（預設）|
| `high` | 深度分析 |
| `xhigh` | 極深度推理 |

---

## 5. 派工上下文範本（Minecraft-translate 專用）

當派工給 OpenCode 時，**必須**在 prompt 裡附上：

### 專案基本資訊

| 項目 | 內容 |
|------|------|
| 工作目錄 | `C:\Users\admin\Desktop\minecraft_translator_flet` |
| 主要語言 | Python 3.12 + Flet 0.82.x |
| 測試框架 | pytest（需用 `.venv\Scripts\python.exe`） |
| Git | `gh` 已認證，可存取 `jlin53882/Minecraft-translate` |

### 重要資料夾對照

```
minecraft_translator_flet/
├── app/                          # Flet UI 主程式
│   ├── views/                    # View 元件
│   ├── icon_reader.py            # ZIP icon reader（含 LRU cache）
│   └── icon_index.py             # Icon 索引建立
├── translation_tool/             # 核心 CLI 工具
│   ├── core/                     # 翻譯引擎（lm_translator, kubejs, ftb...）
│   ├── plugins/                  # 插件（ftbquests, kubejs, md...）
│   └── utils/                    # 共用工具（jar_browser.py, cache_shards.py...）
├── tests/                        # pytest 測試（需 venv）
├── docs/                          # 開發文件（SOP、AI_WORKFLOW_MANUAL...）
├── .icon_cache/                  # JAR icon 快取
└── .venv/                        # Python 虛擬環境（依賴在此）
```

### 禁止假設

| ❌ 錯誤假設 | ✅ 正確做法 |
|------------|------------|
| 「pytest 直接跑」 | 必須先 `cd` 進專案目錄，用 `.venv\Scripts\python.exe -m pytest` |
| 「全域 Python 有套件」 | 專案依賴（`ftb_snbt_lib`、`pandas`）只在 `.venv` 裡 |
| 「直接用 `python`」 | 明確指定 `.venv\Scripts\python.exe` |
| 「桌面是工作目錄」 | 工作目錄是 `minecraft_translator_flet` |
| 「PowerShell redirect 寫中文」 | 會變成 UTF-16 截斷；改用 Python script 或 `write` tool |

### 典型派工 prompt 範例

```
你是一個專業的 Python 開發者，幫我對以下 PR 進行 code review。

## 專案背景
- 工作目錄：`C:\Users\admin\Desktop\minecraft_translator_flet`
- 主要語言：Python 3.12 + Flet 0.82.x
- 測試：`cd` 進專案目錄後，用 `.venv\Scripts\python.exe -m pytest` 執行

## 任務
請用繁體中文 review 這個 PR 的變更：
[這裡貼 PR 內容或 diff]

## 審查重點
1. 是否有破壞性變更未告知
2. 測試覆蓋是否足夠
3. 錯誤處理是否完整
4. 程式碼風格是否一致（建議使用 ruff formatter）
5. 是否有安全疑慮
6. **Schema 新增欄位 → 確認有對應實作讀取**（見 `references/review-checklist.md`）
7. **Pattern matching 函式 → 提供邊界條件測試**（見 `references/review-checklist.md`）
8. **常數/函式定義 → 確認沒有被取代後遺留**（見 `references/review-checklist.md`）
9. **改動範圍 → 只涵蓋需要修改的範圍，無關程式碼不受影響**

## 輸出格式
最後列出：
- ✅ 建議保留的優點
- ⚠️ 需要修改的問題（附檔案:行號）
- 💡 改進建議

請用繁體中文回覆，並在結尾列出你修改了哪些檔案。
```

---

## 6. 觸發關鍵字對照

| 關鍵字 | 對應行為 |
|--------|----------|
| `用 OpenCode review PR#xxx` | CLI: `opencode_task.py --prompt "review PR#xxx"` |
| `用 OpenCode 分析這個檔案` | `client.analyze_file()` |
| `用 OpenCode 多輪對話` | import `OpenCodeAPI` + 多輪 |
| `OpenCode 用高思考` | `--reasoning high` |
| `用 OpenCode 探索專案` | `agent="explore"` |
| `用 OpenCode 做規劃` | `agent="plan"` |
| `用 OpenCode 結構化輸出` | `outputFormat=json_schema` |
| `用 OpenCode 中止任務` | `client.abort_session(id)` |

---

## 依賴

```bash
# opencode_task.py：無外部依賴（標準函式庫）
# opencode_client.py：pip install requests
# SDK 進階功能（如 event subscribe）：pip install requests sseclient
```

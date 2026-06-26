# OpenCode Agents 系統

> 本文件說明 OpenCode 的代理（Agent）架構，包括內建代理、自訂代理、參數設定與使用方式。

---

## 1. 四種內建代理

OpenCode 預設提供四種內建代理，各自肩負不同職責，適用於不同場景。

| 代理 | 模式 | 工具權限 | 用途 |
|------|------|----------|------|
| `build` | primary | 全部 | 全工具開發工作（預設）|
| `plan` | primary | 唯讀 | 規劃分析，不改檔案 |
| `general` | subagent | 全部（除 todo）| 複雜研究、多步驟任務 |
| `explore` | subagent | 唯讀 | 快速探索程式碼庫 |

### 各代理適用情境

- **`build`**：日常開發、實作新功能、修改程式碼等需要寫入檔案的任務。
- **`plan`**：收到複雜需求時，先用 plan 代理分析問題、列出實作步驟，再切換 build 執行。
- **`general`**：當任務涉及多個階段（例如先搜尋、再分析、最後寫入）且估計會消耗大量 context 時使用。
- **`explore`**：快速掃描不熟悉的程式碼庫、查找特定函式或符號、統計程式碼結構。

### 模式差異說明

- **primary**：主代理，佔用主要對話上下文，與使用者直接互動。
- **subagent**：子代理，擁有獨立上下文，適合將複雜任務分流出去執行，不會污染主對話的 context。

---

## 2. 切換代理

### SDK 呼叫方式

透過 `agent` 參數指定欲使用的代理：

```python
# 使用 plan 代理進行唯讀分析（不改任何檔案）
client.send_message(prompt, session_id=sid, agent="plan")

# 使用 explore 代理快速探索程式碼庫
client.send_message(prompt, session_id=sid, agent="explore")

# 使用 general 代理處理複雜多步驟任務
client.send_message(prompt, session_id=sid, agent="general")

# 預設使用 build 代理（所有工具全開）
client.send_message(prompt, session_id=sid, agent="build")
```

### 互動式切換

在 OpenCode 的互動模式中，可以使用快捷鍵快速切換代理：

| 按鍵 | 動作 |
|------|------|
| `Tab` | 切換內建代理（build / plan / general / explore 輪流切換）|
| `Ctrl+X, Up/Down` | 切換到子工作階段（subagent session）|
| `Ctrl+X, Up` | 回到父工作階段（parent session）|

> **提示**：在規劃大型任務時，建議先 `Tab` 切到 `plan` 確認實作方向，再切回 `build` 執行。

---

## 3. 自訂代理

除了四種內建代理，使用者可以根據專案需求定義自己的代理。自訂代理支援兩種格式：**JSON 格式**（直接寫入設定檔）和 **Markdown 格式**（使用 YAML frontmatter 宣告式定義）。

### 3.1 JSON 格式

適合需要精細控制工具權限、模型、描述的場景。設定檔路徑：

- **全域**：`~/.config/opencode/opencode.json`
- **專案層級**：`專案根目錄/.opencode/opencode.json`

```json
{
  "agent": {
    "code-reviewer": {
      "description": "專門做 code review 的代理",
      "mode": "subagent",
      "model": "minimax/MiniMax-M2.7",
      "permission": {
        "edit": "deny",
        "bash": {
          "git diff": "allow",
          "grep *": "allow",
          "*": "ask"
        }
      }
    },
    "readonly-explorer": {
      "description": "快速唯讀探索",
      "mode": "subagent",
      "tools": {
        "write": false,
        "edit": false,
        "bash": false
      }
    }
  }
}
```

#### JSON 格式欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `description` | 字串 | 代理的用途描述（供 agentlens 或 UI 顯示）|
| `mode` | 字串 | 代理模式：`primary` 或 `subagent` |
| `model` | 字串 | 模型識別碼，格式：`provider/model-id`（例如 `minimax/MiniMax-M2.7`）|
| `tools` | 物件 | 工具開關，設定 `true`（開）或 `false`（關）|
| `permission` | 物件 | 細粒度權限控制，定義哪些操作需要詢問或直接允許/拒絕 |
| `temperature` | 浮點數 | 控制回應隨機性（範圍 0.0–1.0），見下方章節說明 |

### 3.2 Markdown 格式

使用 YAML frontmatter 宣告代理屬性，更適合需要自然語言描述代理行為的場景。檔案放置路徑：

- **全域**：`~/.config/opencode/agents/代理名稱.md`
- **專案層級**：`專案根目錄/.opencode/agents/代理名稱.md`

```markdown
---
description: Minecraft-translate 專用 code review 代理
mode: subagent
model: minimax/MiniMax-M2.7
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash:
    "git diff*": allow
    "grep *": allow
---

你是 Minecraft-translate 專案的 code reviewer。
只分析不修改，用繁體中文回覆。
重點檢查：安全性、效能、測試覆蓋。
```

#### Markdown 格式結構說明

1. **YAML frontmatter（前題）**：以 `---` 包圍的宣告式設定，定義代理的技術屬性。
2. **系統提示詞（System Prompt）**：frontmatter 之後的純文字內容，作為代理的角色定義與行為指引。

> **建議**：若代理需要扮演特定角色（例如「某專案的 code reviewer」），使用 Markdown 格式能讓系統提示詞更自然、易讀。

---

## 4. 溫度（temperature）

`temperature` 參數控制模型輸出的隨機性。OpenCode 的溫度範圍為 **0.0 至 1.0**。

| 範圍 | 特性 | 適用場景 |
|------|------|----------|
| 0.0–0.2 | 集中、確定性 | 程式碼分析、規劃、路線圖撰寫 |
| 0.3–0.5 | 平衡 | 一般開發任務、日常實作 |
| 0.6–1.0 | 有創意、多樣 | 腦力激盪、架構探索、生成多樣化名稱 |

### 設定建議

- **分析/規劃任務**：建議 `temperature: 0.1`–`0.2`，確保邏輯嚴謹、回覆一致。
- **一般實作任務**：預設 `0.3`–`0.4` 即可。
- **創意發想**：使用 `0.6`–`0.8`，但避免在需要確定性的場景使用高溫度。

---

## 5. max_steps（最大迭代次數）

`max_steps` 限制代理在單一回合中的最大迭代次數。用於控制成本、避免代理陷入無限迴圈，或確保長時間任務能分階段完成。

```python
# 限制為最多 5 次迭代
client.send_message(prompt, session_id=sid, max_steps=5)
```

### 使用時機

- **探索任務**：设低 `max_steps`（如 3–5）避免過度深入。
- **實作任務**：可以設高（如 10–20）或保持預設（不限）。
- **CI/自動化環境**：強制設定 `max_steps` 防止資源過度消耗。

---

## 6. default_agent（預設代理設定）

可以在設定檔中指定開啟新工作階段時的預設代理，取代預設的 `build`：

```json
{
  "default_agent": "plan"
}
```

此設定同樣支援寫入 `opencode.json` 的 `agent` 區塊。設定完成後，每次新工作階段將自動使用 `plan` 代理，適合希望先規劃再實作的工作流程。

---

## 7. 工具權限與 permission 設定

### 工具開關（tools）

適用只想快速開關整類工具的場合：

```json
{
  "tools": {
    "write": false,
    "edit": false,
    "bash": false
  }
}
```

### 細粒度權限（permission）

適用需要對特定操作做細節控制的場合：

```json
{
  "permission": {
    "edit": "deny",
    "bash": {
      "git diff": "allow",
      "git push": "deny",
      "*": "ask"
    }
  }
}
```

權限值說明：

| 值 | 行為 |
|------|------|
| `"allow"` | 直接執行，不詢問 |
| `"deny"` | 直接拒絕 |
| `"ask"` | 執行前詢問使用者確認（預設行為）|

---

## 8. subagent 與 primary 的差別

理解這兩種模式的差異，有助於決定何時該新建代理而非在當前代理中繼續執行。

| 維度 | primary | subagent |
|------|---------|----------|
| 對話上下文 | 與主對話共享，會佔用 parent context | 獨立上下文，不影響 parent context |
| 適用情境 | 日常單一任務、連貫性高的實作 | 多工分流、獨立探索、長期研究 |
| 建立方式 | 預設即為 primary | SDK 中傳入 `agent="general"` 等 subagent 名稱 |
| 回應方式 | 直接回覆給使用者 | 結果自動回傳給 parent session |

### 使用 subagent 的時機

- 預估任務需要超過 5 個來回（來回膨脹 context）時。
- 需要對同一個程式碼庫進行多個獨立探索時。
- 任務有明確邊界，可以並行執行時（各自建立 subagent）。

### 使用 primary 的時機

- 任務邏輯連貫，需要前後文參照。
- 只需要偶爾查閱其他檔案，不需要長期佔用獨立 context。

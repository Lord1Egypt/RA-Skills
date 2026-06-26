# OpenCode × OpenClaw 整合案例

## 案例一：PR Code Review

```python
import sys
sys.path.insert(0, "C:/Users/admin/.openclaw/workspace/skills/opencode-api/scripts")
from opencode_task import run_opencode_task

result = run_opencode_task(
    prompt="""請用繁體中文對以下 Git diff 進行 code review：

```diff
+def translate(items):
+    for item in items:
+        print(item)
```

分析：1) Bug  2) 安全性  3) 風格  4) 改進建議""",
    model="minimax/MiniMax-M2.7",
    reasoning="high",
)
print(result.text)
```

## 案例二：多輪對話

```python
from opencode_task import OpenCodeAPI

client = OpenCodeAPI(auto_start=True)
sid = client.create_session(title="PR Review #374")

r1 = client.send_message(
    "請 review 這個函數：\ndef translate(items): pass",
    session_id=sid,
    model="minimax/MiniMax-M2.7"
)
print(client.extract_text(r1))

r2 = client.send_message(
    "可以針對第三點給更具體的修改範例嗎？",
    session_id=sid,
)
print(client.extract_text(r2))
```

## 案例三：使用 Plan 代理（唯讀分析）

```python
from opencode_task import OpenCodeAPI

client = OpenCodeAPI()
sid = client.create_session(title="架構分析")
r = client.send_message(
    "分析 translation_tool/core/ 的模組設計，並提出重構建議。只分析不修改。",
    session_id=sid,
    agent="plan",  # 唯讀代理
    model="minimax/MiniMax-M2.7"
)
print(client.extract_text(r))
```

## 案例四：批次多檔分析

```python
from pathlib import Path
from opencode_task import OpenCodeAPI

client = OpenCodeAPI()
files = {
    "core/translator.py": Path("core/translator.py").read_text(encoding="utf-8"),
    "core/parser.py": Path("core/parser.py").read_text(encoding="utf-8"),
}

parts = [{"type": "text", "text": "請用繁體中文分析以下所有檔案的架構："}]
for fname, content in files.items():
    parts.append({"type": "text", "text": f"\n=== {fname} ===\n{content[:2000]}"})

sid = client.create_session(title="Batch Analyze")
response = client.send_message("", parts=parts, session_id=sid, model="minimax/MiniMax-M2.7")
print(client.extract_text(response))
```

## 案例五：結構化輸出（JSON Schema）

```python
from opencode_task import OpenCodeAPI

client = OpenCodeAPI()
sid = client.create_session(title="結構化 Review")

schema = {
    "type": "object",
    "properties": {
        "score": {"type": "number", "description": "程式碼評分 0-10"},
        "issues": {
            "type": "array",
            "items": {"type": "string"},
            "description": "發現的問題清單"
        },
        "suggestions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "改進建議清單"
        }
    },
    "required": ["score", "issues"]
}

result = client.structured_output(
    session_id=sid,
    prompt="請 review 以下程式碼並以結構化格式回傳：\ndef bad_func(): pass",
    schema=schema,
    model="minimax/MiniMax-M2.7",
)
print(result)  # {"score": 3, "issues": [...], "suggestions": [...]}
```

## 案例六：中止與還原

```python
from opencode_task import OpenCodeAPI
import time

client = OpenCodeAPI()
sid = client.create_session()

# 開始一個長時間任務
client.send_message("幫我重構整個翻譯引擎...", session_id=sid)

# 2 秒後中止
time.sleep(2)
client.abort_session(sid)

# 還原到上一個訊息
client.revert_session(sid, count=1)
```

## 案例七：探索代理（快速找程式碼）

```python
from opencode_task import OpenCodeAPI

client = OpenCodeAPI()
sid = client.create_session(title="快速探索")

r = client.send_message(
    "找出所有翻譯相關的函數，列出檔案路徑與行號",
    session_id=sid,
    agent="explore",  # 快速唯讀探索
    model="minimax/MiniMax-M2.7"
)
print(client.extract_text(r))
```

## 案例八：使用自訂工具（Custom Tool）

假設建立了 `.opencode/tools/github.ts`：

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "查詢 GitHub PR 狀態",
  args: {
    owner: tool.schema.string(),
    repo: tool.schema.string(),
    pr: tool.schema.number(),
  },
  async execute(args) {
    // 呼叫 GitHub API
  },
})
```

在 OpenCode 中使用：`查詢 jlin53882/Minecraft-translate 的 PR 狀態`

## 案例九：使用 MCP 伺服器

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

在 OpenCode prompt 中：`使用 context7 搜尋 Flet 0.82 的文件`

## 案例十：使用 Formatters（自動格式化）

設定 `opencode.json`：
```json
{
  "formatter": {
    "ruff": {
      "command": [".venv/Scripts/ruff", "format", "$FILE"],
      "extensions": [".py", ".pyi"]
    }
  }
}
```

OpenCode 寫入 `.py` 檔案後自動執行 `ruff format`。

## 與 Codex 比較

| 面向 | Codex CLI | OpenCode HTTP API |
|------|-----------|-------------------|
| 部署 | 獨立程序 | HTTP Server |
| 延遲 | 較高 | 低（keep-alive）|
| 多工 | 困難 | 原生 multi-session |
| OpenClaw 整合 | PTY 模式 | HTTP REST |
| 適用場景 | 即時互動 | 自動化派工 |
| Agents 系統 | 無 | 四種內建代理 |
| 工具權限 | 無 | 細粒度 permission |
| 結構化輸出 | 無 | JSON Schema |
| MCP 整合 | 無 | 原生支援 |

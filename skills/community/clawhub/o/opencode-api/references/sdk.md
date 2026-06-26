# SDK 完整 API

## 端點總覽

| 類別 | 方法 | 路徑 | 說明 |
|------|------|------|------|
| 全域 | GET | `/global/health` | 健康檢查 |
| 全域 | GET | `/global/event` | 全域 SSE 事件串流 |
| 工作階段 | GET | `/session` | 列出所有 session |
| 工作階段 | POST | `/session` | 建立 session |
| 工作階段 | GET | `/session/:id` | 取得單一 session |
| 工作階段 | DELETE | `/session/:id` | 刪除 session |
| 工作階段 | PATCH | `/session/:id` | 更新 session 屬性 |
| 工作階段 | GET | `/session/:id/children` | 列出子 session |
| 工作階段 | POST | `/session/:id/message` | 傳送訊息 |
| 工作階段 | POST | `/session/:id/prompt_async` | 非同步傳送（204 No Content）|
| 工作階段 | GET | `/session/:id/messages` | 列出訊息 |
| 工作階段 | POST | `/session/:id/abort` | 中止執行 |
| 工作階段 | POST | `/session/:id/share` | 分享 session |
| 工作階段 | DELETE | `/session/:id/share` | 取消分享 |
| 工作階段 | GET | `/session/:id/diff` | 取得變更差異 |
| 工作階段 | POST | `/session/:id/revert` | 還原訊息 |
| 工作階段 | POST | `/session/:id/unrevert` | 取消還原 |
| 工作階段 | POST | `/session/:id/fork` | 分岔 session |
| 工作階段 | POST | `/session/:id/init` | 分析專案建立 AGENTS.md |
| 工作階段 | POST | `/session/:id/summarize` | 摘要 session |
| 工作階段 | GET | `/session/:id/todo` | 取得待辦清單 |
| 工作階段 | GET | `/session/status` | 所有 session 狀態 |
| 設定 | GET | `/config` | 取得設定資訊 |
| 設定 | PATCH | `/config` | 更新設定 |
| 設定 | GET | `/config/providers` | 列出 provider 與模型 |
| 專案 | GET | `/project` | 列出所有專案 |
| 專案 | GET | `/project/current` | 取得當前專案 |
| 路徑 | GET | `/path` | 取得當前路徑 |
| VCS | GET | `/vcs` | 取得 VCS 資訊 |
| 檔案 | GET | `/find?pattern=` | 搜尋文字 |
| 檔案 | GET | `/find/file?query=` | 依名稱找檔案 |
| 檔案 | GET | `/find/symbol?query=` | 尋找工作區符號 |
| 檔案 | GET | `/file?path=` | 列出目錄內容 |
| 檔案 | GET | `/file/content?path=` | 讀取檔案內容 |
| 檔案 | GET | `/file/status` | 取得 git 狀態 |
| TUI | POST | `/tui/append-prompt` | 向 prompt 附加文字 |
| TUI | POST | `/tui/submit-prompt` | 送出 prompt |
| TUI | POST | `/tui/clear-prompt` | 清除 prompt |
| TUI | POST | `/tui/show-toast` | 顯示 toast |
| TUI | POST | `/tui/open-help` | 開啟幫助 |
| TUI | POST | `/tui/open-sessions` | 開啟 session 選擇器 |
| TUI | POST | `/tui/open-models` | 開啟模型選擇器 |
| TUI | GET | `/tui/control/next` | 等待控制請求 |
| 工具 | GET | `/experimental/tool/ids` | 列出所有工具 ID |
| 工具 | GET | `/experimental/tool` | 列出工具 schema |
| 代理 | GET | `/agent` | 列出所有代理 |
| 指令 | GET | `/command` | 列出所有指令 |
| MCP | GET | `/mcp` | 取得 MCP 狀態 |
| MCP | POST | `/mcp` | 動態新增 MCP |
| LSP | GET | `/lsp` | 取得 LSP 狀態 |
| 格式化 | GET | `/formatter` | 取得格式化器狀態 |
| 日誌 | POST | `/log` | 寫入日誌 |
| 認證 | PUT | `/auth/:id` | 設定認證憑證 |

## Python 對照表

| OpenCode SDK (TS) | Python 對應方法 |
|-------------------|----------------|
| `client.global.health()` | `client.health()` |
| `client.session.create()` | `client.create_session()` |
| `client.session.list()` | `client.list_sessions()` |
| `client.session.get()` | `client.get_session(id)` |
| `client.session.prompt()` | `client.send_message()` |
| `client.session.prompt({noReply:true})` | `client.send_message(no_reply=True)` |
| `client.session.prompt_async()` | 直接 POST `/session/:id/prompt_async` |
| `client.session.abort()` | `client.abort_session(id)` |
| `client.session.share()` | `client.share_session(id)` |
| `client.session.revert()` | `client.revert_session(id, count)` |
| `client.session.unrevert()` | `client.unrevert_session(id)` |
| `client.session.fork()` | 直接 POST `/session/:id/fork` |
| `client.session.init()` | 直接 POST `/session/:id/init` |
| `client.session.summarize()` | 直接 POST `/session/:id/summarize` |
| `client.session.messages()` | `client.list_messages(id)` |
| `client.session.children()` | 直接 GET `/session/:id/children` |
| `client.session.diff()` | 直接 GET `/session/:id/diff` |
| `client.session.todo()` | 直接 GET `/session/:id/todo` |
| `client.config.get()` | `client.get_config()` |
| `client.config.providers()` | `client.get_providers()` |
| `client.config.patch()` | 直接 PATCH `/config` |
| `client.find.text()` | `client.search_text(pattern)` |
| `client.find.files()` | `client.find_files(query, type)` |
| `client.find.symbols()` | 直接 GET `/find/symbol` |
| `client.file.read()` | `client.read_file(path)` |
| `client.file.status()` | `client.file_status()` |
| `client.tui.showToast()` | `client.show_toast(message, variant)` |
| `client.tui.appendPrompt()` | `client.append_prompt(text)` |
| `client.tui.submitPrompt()` | `client.submit_prompt()` |
| `client.tui.clearPrompt()` | `client.clear_prompt()` |
| `client.event.subscribe()` | `client.subscribe_events(session_id)` |

## 結構化輸出（JSON Schema）

要求模型回傳結構化 JSON：

```python
body = {
    "parts": [{"type": "text", "text": prompt}],
    "outputFormat": {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "issue_type": {"type": "string", "description": "問題類型"},
                "severity": {"type": "string", "description": "嚴重程度：critical/high/medium/low"},
                "location": {"type": "string", "description": "檔案與行號"},
                "description": {"type": "string", "description": "問題描述"}
            },
            "required": ["issue_type", "severity"]
        },
        "retryCount": 3
    }
}
response = client.post(f"/session/{sid}/message", body)
```

Python 捷徑（`opencode_task.py`）：
```python
result = client.structured_output(
    session_id=sid,
    prompt="...",
    schema={"type": "object", "properties": {...}},
    model="minimax/MiniMax-M2.7",
)
```

## noReply 模式

注入上下文不回覆（對 plugin 自動化很有用）：

```python
client.send_message(
    prompt="你現在是 Minecraft-translate reviewer。",
    session_id=sid,
    no_reply=True  # 只注入，不等待回覆
)
```

## session.abort()（中止執行）

```python
client.abort_session(sid)
```

## session.share()（分享連結）

```python
result = client.share_session(sid)
share_url = result.get("url")
```

## session.revert()（還原訊息）

```python
client.revert_session(sid, count=1)  # 還原上一個訊息
```

## session.fork()（分岔）

在特定訊息處分岔出新 session：
```python
result = client.post(f"/session/{sid}/fork", {"messageID": "msg_xxx"})
forked_sid = result["id"]
```

## session.init()（分析專案）

```python
client.post(f"/session/{sid}/init", {
    "messageID": None,
    "providerID": "minimax-portal",
    "modelID": "MiniMax-M2.7"
})
```

## session.summarize()（摘要）

```python
client.post(f"/session/{sid}/summarize", {
    "providerID": "minimax-portal",
    "modelID": "MiniMax-M2.7"
})
```

## 查可用模型

```python
providers = client.get_providers()
# 回傳格式：
# {
#   "providers": [{"id": "minimax-portal", "models": [...]}],
#   "default": {"minimax-portal": "MiniMax-M2.7"}
# }
```

## 即時事件監聽（SSE）

```python
stream = client.subscribe_events(session_id=sid)
for event in stream.stream:
    print(f"[EVENT] {event.type}: {event.data}")
```

## TUI Toast

```python
client.show_toast("任務完成！", variant="success")
# variant: info / success / warning / error
```

## 實用程式碼範例

### 基本使用

```python
import sys
sys.path.insert(0, "C:/Users/admin/.openclaw/workspace/skills/opencode-api/scripts")
from opencode_task import run_opencode_task

result = run_opencode_task(
    prompt="請用繁體中文 review 這個函數",
    model="minimax/MiniMax-M2.7",
    reasoning="high",
)
print(result.text)
```

### 批次分析

```python
from opencode_task import OpenCodeAPI
from pathlib import Path

client = OpenCodeAPI()
files = {
    "core/translator.py": Path("core/translator.py").read_text(encoding="utf-8")[:2000],
}

parts = [{"type": "text", "text": "請分析以下檔案："}]
for fname, content in files.items():
    parts.append({"type": "text", "text": f"\n=== {fname} ===\n{content}"})

sid = client.create_session(title="Batch Analyze")
response = client.send_message("", parts=parts, session_id=sid)
print(client.extract_text(response))
```

### 設定權限（細粒度）

```python
# 使用 config patch 動態更新權限
client.patch("/config", {
    "permission": {
        "bash": {"*": "ask", "git *": "allow", "rm *": "deny"},
        "edit": "deny"
    }
})
```

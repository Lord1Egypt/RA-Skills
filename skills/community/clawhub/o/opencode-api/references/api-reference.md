# OpenCode HTTP API 完整參考

## 基礎資訊

- **Base URL**: `http://127.0.0.1:4096`
- **格式**: JSON / UTF-8
- **OpenAPI 規範**: `http://localhost:4096/doc`

## 全域端點

| Method | Path | 說明 |
|--------|------|------|
| GET | `/global/health` | 健康檢查與版本 |
| GET | `/global/event` | 全域 SSE 事件串流 |

```python
import requests
r = requests.get("http://127.0.0.1:4096/global/health")
print(r.json())  # {"healthy": true, "version": "1.x.x"}
```

## 工作階段（Session）API

### 建立 Session

```python
r = requests.post("http://127.0.0.1:4096/session", json={"title": "PR Review"})
sid = r.json()["id"]
```

### 傳送訊息（核心）

```python
body = {
    "parts": [{"type": "text", "text": "請用繁體中文 review 這個函數"}],
    "model": {
        "providerID": "minimax-portal",
        "modelID": "MiniMax-M2.7",
        "reasoningEffort": "high"
    }
}
r = requests.post(f"http://127.0.0.1:4096/session/{sid}/message", json=body)
response = r.json()
text = "\n".join(p["text"].strip() for p in response.get("parts", []) if p.get("type") == "text" and p.get("text"))
```

### 結構化輸出（JSON Schema）

```python
body = {
    "parts": [{"type": "text", "text": prompt}],
    "outputFormat": {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "score": {"type": "number", "description": "程式碼評分 0-10"},
                "issues": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "發現的問題清單"
                }
            },
            "required": ["score"]
        },
        "retryCount": 3
    }
}
```

### Session 管理

| Method | Path | 說明 |
|--------|------|------|
| GET | `/session` | 列出所有 session |
| POST | `/session` | 建立新 session |
| GET | `/session/:id` | 取得 session |
| DELETE | `/session/:id` | 刪除 session |
| PATCH | `/session/:id` | 更新屬性（title）|
| GET | `/session/:id/messages` | 列出訊息 |
| POST | `/session/:id/message` | 傳送訊息 |
| POST | `/session/:id/prompt_async` | 非同步傳送（204）|
| POST | `/session/:id/abort` | 中止執行 |
| POST | `/session/:id/share` | 分享 session |
| DELETE | `/session/:id/share` | 取消分享 |
| POST | `/session/:id/revert` | 還原訊息 |
| POST | `/session/:id/unrevert` | 取消還原 |
| POST | `/session/:id/fork` | 分岔 session |
| POST | `/session/:id/init` | 分析專案 |
| POST | `/session/:id/summarize` | 摘要 session |
| GET | `/session/:id/diff` | 取得變更 |
| GET | `/session/:id/children` | 列出子 session |

### 回應 Parts 類型

| type | 說明 |
|------|------|
| `text` | 文字回覆 |
| `tool` | 工具呼叫（含狀態）|
| `reasoning` | 思考過程 |
| `step-start` | 步驟開始 |
| `step-finish` | 步驟完成 |

## 檔案工具

| Method | Path | 說明 |
|--------|------|------|
| GET | `/find?pattern=` | 搜尋文字（正規表示式）|
| GET | `/find/file?query=` | 依名稱找檔案 |
| GET | `/find/symbol?query=` | 尋找工作區符號 |
| GET | `/file?path=` | 列出目錄內容 |
| GET | `/file/content?path=` | 讀取檔案內容 |
| GET | `/file/status` | 取得 git 狀態 |

```python
# 搜尋文字
r = requests.get("http://127.0.0.1:4096/find", params={"pattern": "def translate"})
print(r.json())  # [{"path": "...", "lines": [...], "line_number": 42}]

# 依名稱找檔案
r = requests.get("http://127.0.0.1:4096/find/file", params={"query": "translator", "type": "file"})
print(r.json())  # ["path/to/translator.py", ...]
```

## 設定 API

| Method | Path | 說明 |
|--------|------|------|
| GET | `/config` | 取得設定 |
| PATCH | `/config` | 更新設定 |
| GET | `/config/providers` | 列出 provider 與模型 |

## TUI 控制

| Method | Path | 說明 |
|--------|------|------|
| POST | `/tui/append-prompt` | 向 prompt 附加文字 |
| POST | `/tui/submit-prompt` | 送出 prompt |
| POST | `/tui/clear-prompt` | 清除 prompt |
| POST | `/tui/show-toast` | 顯示 toast |
| POST | `/tui/open-sessions` | 開啟 session 選擇器 |
| POST | `/tui/open-models` | 開啟模型選擇器 |

```python
requests.post("http://127.0.0.1:4096/tui/show-toast",
    json={"message": "任務完成！", "variant": "success"})
```

## 工具與代理

| Method | Path | 說明 |
|--------|------|------|
| GET | `/agent` | 列出所有代理 |
| GET | `/command` | 列出所有指令 |
| GET | `/experimental/tool/ids` | 列出所有工具 ID |
| GET | `/experimental/tool` | 工具 schema |

## MCP / LSP / 格式化器

| Method | Path | 說明 |
|--------|------|------|
| GET | `/mcp` | MCP 狀態 |
| POST | `/mcp` | 動態新增 MCP |
| GET | `/lsp` | LSP 狀態 |
| GET | `/formatter` | 格式化器狀態 |

## 日誌

| Method | Path | 說明 |
|--------|------|------|
| POST | `/log` | 寫入日誌 |

```python
requests.post("http://127.0.0.1:4096/log", json={
    "service": "my-app",
    "level": "info",
    "message": "Task completed",
    "extra": {"task_id": "123"}
})
```

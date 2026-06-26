# Server 部署

## 啟動 Server

```bash
# 基本（預設 127.0.0.1:4096）
opencode serve

# 自訂連接埠
opencode serve --port 4096 --hostname 127.0.0.1

# 允許外部連線
opencode serve --port 4096 --hostname 0.0.0.0

# 多個 CORS 來源
opencode serve --cors http://localhost:5173 --cors https://app.example.com

# 啟用 mDNS 探索
opencode serve --mdns --mdns-domain opencode.local
```

## HTTP 基本認證

```bash
OPENCODE_SERVER_PASSWORD=your-password opencode serve
OPENCODE_SERVER_USERNAME=admin opencode serve
```

## 健康檢查

```python
import requests
r = requests.get("http://127.0.0.1:4096/global/health")
print(r.json())  # {"healthy": true, "version": "1.x.x"}
```

## 架構說明

- OpenCode TUI 啟動時自動啟動 HTTP Server
- TUI 本身就是 Server 的客戶端
- HTTP API 暴露所有功能，可用於外部整合
- OpenAPI 3.1 規範：`http://localhost:4096/doc`

## 設定檔中的 Server 設定

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "mdnsDomain": "opencode.local",
    "cors": ["http://localhost:5173"]
  }
}
```

## 重要 API 端點速查

| 端點 | 用途 |
|------|------|
| `GET /global/health` | 健康檢查 |
| `POST /session` | 建立工作階段 |
| `POST /session/:id/message` | 傳送訊息 |
| `POST /session/:id/abort` | 中止執行 |
| `GET /config/providers` | 列出可用模型 |
| `POST /tui/show-toast` | TUI 顯示通知 |
| `GET /doc` | OpenAPI 規範文件 |

## Python SDK

使用 `opencode_client.py`：

```python
import sys
sys.path.insert(0, "C:/Users/admin/.openclaw/workspace/skills/opencode-api/scripts")
from opencode_client import OpenCodeClient

client = OpenCodeClient(
    base_url="http://127.0.0.1:4096",
    auto_start=True  # 自動啟動 server（如果未運行）
)
```

## 環境變數

| 環境變數 | 說明 |
|----------|------|
| `OPENCODE_CONFIG` | 自訂設定檔路徑 |
| `OPENCODE_CONFIG_DIR` | 自訂設定目錄 |
| `OPENCODE_CONFIG_CONTENT` | 內嵌 JSON 設定 |
| `OPENCODE_SERVER_PASSWORD` | HTTP Basic 認證密碼 |
| `OPENCODE_SERVER_USERNAME` | HTTP Basic 認證帳號 |
| `OPENCODE_TUI_CONFIG` | 自訂 TUI 設定檔 |

## 連接到現有 Server

啟動 TUI 時自動分配連接埠。若已有一個 Server 運行，可指定連接：

```bash
opencode --port 4096 --hostname 127.0.0.1
```

## 認證儲存

`/connect` 指令設定的 API Key 儲存在：
- `~/.local/share/opencode/auth.json`

## 多個 OpenCode 實例

使用 `mdns` + `mdnsDomain` 在同一網路區分多個實例：

```bash
opencode serve --mdns --mdns-domain project-a.local
opencode serve --mdns --mdns-domain project-b.local
```

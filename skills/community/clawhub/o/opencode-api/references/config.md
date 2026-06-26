## Config 完整設定

### 設定檔位置（優先順序）

1. 遠端設定（`.well-known/opencode`）— 組織預設值
2. 全域設定（`~/.config/opencode/opencode.json`）— 使用者偏好
3. 自訂設定（`OPENCODE_CONFIG` 環境變數）
4. 專案設定（`opencode.json`）— 專案特定
5. `.opencode/` 目錄
6. 內嵌設定（`OPENCODE_CONFIG_CONTENT` 環境變數）

### 變數替換

```json
{
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

從檔案讀取：
```json
{
  "instructions": ["./custom-instructions.md"],
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{file:~/.secrets/openai-key}"
      }
    }
  }
}
```

### 主要設定項目速查

| 設定 | 說明 |
|------|------|
| `model` | 主模型 |
| `small_model` | 輕量任務用模型（如標題生成）|
| `autoupdate` | 自動更新（true/false/"notify"）|
| `server.port` | HTTP Server 連接埠 |
| `server.hostname` | 監聽位址 |
| `server.mdns` | 啟用 mDNS 探索 |
| `server.cors` | CORS 允許的來源 |
| `tui.scroll_speed` | 捲動速度倍率 |
| `tui.diff_style` | 差異呈現方式（auto/stacked）|
| `formatter` | 程式碼格式化器設定 |
| `permission` | 權限規則 |
| `compaction` | 上下文壓縮設定 |
| `watcher.ignore` | 檔案監看忽略模式 |
| `mcp` | MCP 伺服器設定 |
| `plugin` | 外掛程式設定 |
| `instructions` | 指示檔案 |
| `default_agent` | 預設代理 |
| `share` | 分享模式（manual/auto/disabled）|

### compaction 設定

```json
{
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  }
}
```

### 檔案監看器

```json
{
  "watcher": {
    "ignore": ["node_modules/**", "dist/**", ".git/**"]
  }
}
```

### 環境變數參考

| 環境變數 | 用途 |
|----------|------|
| `OPENCODE_CONFIG` | 自訂設定檔路徑 |
| `OPENCODE_CONFIG_DIR` | 自訂設定目錄 |
| `OPENCODE_CONFIG_CONTENT` | 內嵌 JSON 設定 |
| `OPENCODE_SERVER_PASSWORD` | HTTP 基本認證密碼 |
| `OPENCODE_SERVER_USERNAME` | HTTP 基本認證帳號 |
| `OPENCODE_TUI_CONFIG` | 自訂 TUI 設定檔 |

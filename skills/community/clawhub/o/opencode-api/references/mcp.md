## MCP 伺服器（Model Context Protocol）

### 放置位置

在 `opencode.json` 的 `mcp` 欄位設定。

### 本地 MCP

```json
{
  "mcp": {
    "my-local-server": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
      "enabled": true
    }
  }
}
```

### 遠端 MCP

```json
{
  "mcp": {
    "my-remote": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer {env:MY_API_KEY}"
      }
    }
  }
}
```

### OAuth 認證

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

手動觸發認證：
```bash
opencode mcp auth sentry
opencode mcp list        # 列出狀態
opencode mcp debug <name> # 偵錯
```

### MCP 管理

全域停用：
```json
{ "tools": { "mcp_*": false } }
```

按代理啟用：
```json
{
  "tools": { "mcp_*": false },
  "agent": {
    "my-agent": {
      "tools": { "mcp_*": true }
    }
  }
}
```

### 常見 MCP 設定範例

**Sentry（錯誤追蹤）**：
```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

**Context7（文件搜尋）**：
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

**GitHub Grep（程式碼搜尋）**：
```json
{
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app"
    }
  }
}
```

### 注意事項

- MCP 工具會佔用上下文空間，大量工具會快速消耗 Token
- 某些 MCP（如 GitHub MCP）容易超出上下文限制
- 建議按需啟用，而非全部啟用

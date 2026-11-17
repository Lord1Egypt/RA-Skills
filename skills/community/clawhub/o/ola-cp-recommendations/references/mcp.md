# MCP Server 接入

根据用户的偏好和历史选择，为您推荐最适合的邮轮产品，确保您找到理想的航行体验。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/a1f27563-e74b-4840-9e18-c3c884eae9ce
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/ola-cp-recommendations",
  "description": "根据用户的偏好和历史选择，为您推荐最适合的邮轮产品，确保您找到理想的航行体验。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/a1f27563-e74b-4840-9e18-c3c884eae9ce"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。

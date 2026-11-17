# MCP Server 接入

提供关于邮轮旅行的实用建议，包括行前准备、最佳出发时间及目的地推荐，帮助您规划完美的邮轮之旅。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/b70d3b5f-505c-4dfa-a699-587178feec21
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/ola-cp-travel-advice",
  "description": "提供关于邮轮旅行的实用建议，包括行前准备、最佳出发时间及目的地推荐，帮助您规划完美的邮轮之旅。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/b70d3b5f-505c-4dfa-a699-587178feec21"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。

# MCP Server 接入

Explore cruise products specifically tailored for beach vacation enthusiasts. Perfect for sun seekers and relaxation lovers.

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/a6060d76-a93a-43af-aca2-e3051a9d47c7
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/ola-cruise-beach",
  "description": "Explore cruise products specifically tailored for beach vacation enthusiasts. Perfect for sun seekers and relaxation lovers.",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/a6060d76-a93a-43af-aca2-e3051a9d47c7"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。

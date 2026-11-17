# MCP Server 接入

在选择邮轮时，您可以比较不同邮轮产品的价格、行程和品牌，以帮助您做出更明智的决策。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/607dada7-85a0-4d70-b7df-bddcdec3009f
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/ola-cp-comparison",
  "description": "在选择邮轮时，您可以比较不同邮轮产品的价格、行程和品牌，以帮助您做出更明智的决策。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/607dada7-85a0-4d70-b7df-bddcdec3009f"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。

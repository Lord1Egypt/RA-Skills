---
name: my-test-skill
description: 使用 Calculator Server MCP 进行加减法运算。当用户需要进行加法或减法计算时使用此 skill。Server 地址：http://192.168.71.7:8000/mcp，支持 add（加法）和 subtract（减法）两个工具。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["XINIUDATA_MCP_TOKEN"] },
        "primaryEnv": "XINIUDATA_MCP_TOKEN"
      }
  }
---

# MCP Calculator

Calculator Server 🔢 v3.1.0 - 数学运算 MCP 服务。

## 配置

在技能管理后台设置环境变量：
- `XINIUDATA_MCP_TOKEN` - MCP server 访问 token

## 可用工具

| 工具 | 功能 | 参数 |
|------|------|------|
| `add` | 加法：计算 a + b | `a`, `b` (number) |
| `subtract` | 减法：计算 a - b | `a`, `b` (number) |

## 使用（curl）

```bash
# 1. 初始化 session，获取 session ID
SESSION_ID=$(curl -s -D - -X POST http://192.168.71.7:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $XINIUDATA_MCP_TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "mcp-calculator", "version": "1.0.0"}
    },
    "id": 1
  }' | grep -i "mcp-session-id" | awk '{print $2}' | tr -d '\r')

# 2. 发送 initialized 通知
curl -s -X POST http://192.168.71.7:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $XINIUDATA_MCP_TOKEN" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3. 调用 add 工具
curl -s -X POST http://192.168.71.7:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $XINIUDATA_MCP_TOKEN" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {"name": "add", "arguments": {"a": 123, "b": 456}},
    "id": 2
  }'

# 或者调用 subtract 工具
curl -s -X POST http://192.168.71.7:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $XINIUDATA_MCP_TOKEN" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {"name": "subtract", "arguments": {"a": 100, "b": 30}},
    "id": 3
  }'
```

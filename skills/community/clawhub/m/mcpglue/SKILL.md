---
name: mcpglue
description: "OpenClaw MCP 桥接框架。受 Claude Code MCPTool 启发重新设计的 OpenClaw 原生 MCP 连接器。通过标准化的 stdio/SSE 协议连接外部服务，支持动态工具注册、资源读取、流式响应。零泄露代码，纯原创实现，使用 @modelcontextprotocol/sdk 标准库。"
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: [node]
---

# OpenClaw MCP 🔌

> 灵感来自 Claude Code 的 MCP 架构，但实现完全原创。
> 使用 Anthropic 官方开源的 `@modelcontextprotocol/sdk`，不涉及任何泄露代码。

## 安装

```bash
npm install @modelcontextprotocol/sdk
```

## 使用方式

### 列出 MCP Server 的工具
```bash
python3 {{SKILL_DIR}}/scripts/mcp_client.py tools --server node --args "server.js"
```

### 调用 MCP 工具
```bash
python3 {{SKILL_DIR}}/scripts/mcp_client.py call --server node --args "server.js" --tool tool_name --params '{"key":"value"}'
```

### Python 脚本方式
```python
# mcp_client.py 已提供完整实现
from mcp_client import list_tools, call_tool
await list_tools("node", ["server.js"])
await call_tool("node", ["server.js"], "tool_name", {"key": "value"})
```

## 适用场景

| 场景 | 说明 |
|------|------|
| 数据库查询 | 通过 MCP 连接 PostgreSQL/SQLite |
| GitHub API | 通过 MCP 操作 PR、Issue |
| 文件系统 | 通过 MCP 安全地读写文件 |
| 自定义 API | 将任意 API 封装为 MCP Server |

## 参考

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

# Kiro MCP 服务器参考

## 概述

Model Context Protocol (MCP) 允许 Kiro 连接到外部工具、API 和数据源，扩展 agent 的能力。

## 配置文件

`.kiro/mcp.json`

## 内置 MCP 服务器

### GitHub

访问 GitHub API，管理 issues、PRs、仓库等。

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**能力**：
- 创建/更新 issues
- 管理 PRs
- 读取仓库文件
- 搜索代码

### 文件系统

安全访问本地文件系统。

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "options": {
        "allowedPaths": ["/Users/mac/.openclaw/workspace"]
      }
    }
  }
}
```

**能力**：
- 读取/写入文件
- 列出目录
- 文件搜索

### PostgreSQL

连接 PostgreSQL 数据库。

```json
{
  "servers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**能力**：
- 执行 SQL 查询
- 读取表结构
- 数据导入导出

### Slack

与 Slack 工作空间交互。

```json
{
  "servers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

**能力**：
- 发送消息
- 读取频道
- 管理用户

## 第三方 MCP 服务器

### Brave Search

网页搜索集成。

```json
{
  "servers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

### Google Maps

地理位置和路线服务。

```json
{
  "servers": {
    "google-maps": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-maps"],
      "env": {
        "GOOGLE_MAPS_API_KEY": "${GOOGLE_MAPS_API_KEY}"
      }
    }
  }
}
```

### Fetch

网页内容抓取。

```json
{
  "servers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

## 自定义 MCP 服务器

### 创建步骤

1. 创建服务器目录
2. 实现 MCP 协议
3. 配置到 mcp.json

### 示例：天气服务器

```typescript
// weather-server/index.ts
import { Server } from '@modelcontextprotocol/sdk/server';
import { WeatherAPI } from './weather';

const server = new Server({
  name: 'weather-server',
  version: '1.0.0',
});

server.setRequestHandler('getWeather', async (request) => {
  const { location } = request.params;
  const weather = await WeatherAPI.getCurrent(location);
  return { content: [{ type: 'text', text: JSON.stringify(weather) }] };
});

server.run();
```

```json
{
  "servers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/weather-server/index.ts"],
      "env": {
        "WEATHER_API_KEY": "${WEATHER_API_KEY}"
      }
    }
  }
}
```

## 环境变量管理

### 使用 .env 文件

在项目根目录创建 `.env`：

```bash
GITHUB_TOKEN=ghp_xxx
DATABASE_URL=postgresql://user:pass@localhost/db
BRAVE_API_KEY=xxx
```

### 在 mcp.json 中引用

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## 安全最佳实践

### ✅ 推荐

- 最小权限原则配置 allowedPaths
- 使用环境变量存储敏感信息
- 定期轮换 API keys
- 仅启用需要的服务器

### ❌ 避免

- 硬编码敏感信息
- 允许访问整个文件系统
- 启用不必要的服务器
- 共享 API keys

## 调试 MCP

### 查看服务器状态

```bash
kiro mcp status
```

### 测试连接

```bash
kiro mcp test <server-name>
```

### 查看日志

```bash
kiro mcp logs --server <server-name>
```

### 重启服务器

```bash
kiro mcp restart <server-name>
```

## 常见问题

### Q: MCP 服务器启动失败？
A: 检查环境变量是否正确配置，确认 npx 可以访问包。

### Q: 如何限制文件系统访问范围？
A: 在 options.allowedPaths 中指定允许的目录列表。

### Q: MCP 会影响性能吗？
A: 每个服务器独立运行，按需连接。不活动时不消耗资源。

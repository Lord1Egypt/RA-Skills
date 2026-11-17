# Kepler MCP 服务安装指南

本技能依赖 **Kepler MCP 服务**，需要在你的 Agent 环境中配置 MCP 服务器。

## 快速配置

### Claude Code

在 Claude Code 的 MCP 配置文件（`~/.claude/settings.json` 或项目 `.claude/settings.json`）中添加：

```json
{
  "mcpServers": {
    "kepler": {
      "type": "sse",
      "url": "https://apisec.cn/sse",
      "headers": {
        "Authorization": "Bearer <Your Kepler API-KEY>"
      }
    }
  }
}
```

### OpenClaw

在 OpenClaw 的 MCP 配置文件（`~/.openclaw/mcp.json` 或项目 `.openclaw/mcp.json`）中添加：

```json
{
  "mcpServers": {
    "kepler": {
      "type": "sse",
      "url": "https://apisec.cn/sse",
      "headers": {
        "Authorization": "Bearer <Your Kepler API-KEY>"
      }
    }
  }
}
```

### Codex

在 Codex 的 MCP 配置文件（`~/.codex/mcp.json`）中添加：

```json
{
  "mcpServers": {
    "kepler": {
      "type": "sse",
      "url": "https://apisec.cn/sse",
      "headers": {
        "Authorization": "Bearer <Your Kepler API-KEY>"
      }
    }
  }
}
```

### 其他 MCP 客户端

对于其他支持 MCP 协议的 Agent 工具，配置方式类似：

1. 找到 MCP 配置文件（通常在用户主目录或项目根目录）
2. 在 `mcpServers` 中添加 `kepler` 服务器配置
3. 配置参数：
   - `type`: `sse`
   - `url`: `https://apisec.cn/sse`
   - `headers.Authorization`: `Bearer <Your Kepler API-KEY>`

## 通用配置参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 连接类型，固定为 `sse` |
| `url` | string | 是 | Kepler MCP 服务端点：`https://apisec.cn/sse` |
| `headers.Authorization` | string | 是 | 身份验证令牌，格式 `Bearer <API-KEY>` |
| `headers.X-Custom-Header` | string | 否 | 可选的自定义请求头 |

## 获取 API Key

1. 访问 [Kepler 官网](https://apisec.cn) 注册账号
2. 登录控制台，进入「API 管理」页面
3. 点击「生成 API Key」
4. 复制生成的 Key，替换配置中的 `<Your Kepler API-KEY>`

## 验证安装

配置完成后，可以通过以下方式验证：

### Claude Code
```bash
claude config mcp status
# 或使用 slash 命令
/config mcp
```

### OpenClaw
```bash
openclaw mcp status
# 或在对话中询问："MCP 服务连接状态如何？"
```

### Codex
```bash
codex mcp list
# 或在对话中询问："检查 MCP 服务是否已连接"
```

### 通用验证方法
在 Agent 对话中输入以下提示，验证工具是否可用：
```
请使用 mcp__kepler__web_search 搜索 "测试"
```

如果能正常返回搜索结果，表示 MCP 服务配置成功。

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 连接超时 | 网络问题 | 检查网络连接，确认 `apisec.cn` 可访问 |
| 401 未授权 | API Key 无效 | 检查 API Key 是否正确，是否已过期 |
| 404 未找到 | URL 错误 | 确认 URL 为 `https://apisec.cn/sse` |
| 工具未找到 | MCP 未配置 | 检查配置文件路径和格式是否正确 |

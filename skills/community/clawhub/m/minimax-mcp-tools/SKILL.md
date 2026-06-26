# MiniMax MCP - 联网搜索 & 图片理解

## 功能简介

MiniMax 官方 MCP 服务，提供**联网搜索**和**图片理解**两大功能。

## 工具列表

| 工具 | 功能 | 参数 |
|------|------|------|
| `web_search` | 联网搜索 | query: 搜索关键词 |
| `understand_image` | 图片理解 | prompt: 图片描述要求, image_url: 图片URL或本地路径 |

## 前置要求

1. **安装 uvx**（如果未安装）：
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
which uvx
```

2. **获取 MiniMax API Key**：
   - 访问 https://platform.minimaxi.com/subscribe/token-plan
   - 订阅套餐获取 API Key

## 安装配置

### 1. 安装 Skill
```bash
clawhub install minimax-mcp
```

### 2. 配置 MCP
编辑 `~/.openclaw/mcp.json`，添加 MiniMax MCP 配置：

```json
{
  "mcpServers": {
    "MiniMax": {
      "command": "/Users/js/.local/bin/uvx",
      "args": ["minimax-coding-plan-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "你的API_Key",
        "MINIMAX_API_HOST": "https://api.minimaxi.com"
      }
    }
  }
}
```

> **注意**：Windows 用户请将 `uvx` 路径改为 `uvx.exe` 或对应路径

### 3. 重启 OpenClaw
```bash
openclaw gateway restart
```

### 4. 验证 MCP 加载
```bash
mcporter list
# 应该看到 minimax (2 tools) - healthy
```

## 使用方法

### 联网搜索
```bash
mcporter call minimax.web_search query="搜索关键词"
```

示例：
```bash
mcporter call minimax.web_search query="OpenClaw AI助手"
```

### 图片理解
```bash
mcporter call minimax.understand_image prompt="描述要求" image_url="图片URL或本地路径"
```

示例：
```bash
mcporter call minimax.understand_image prompt="这张图片里有什么？" image_url="https://example.com/image.jpg"
```

## OpenClaw 中的使用方法

在 OpenClaw 会话中，直接让 AI 帮你搜索或分析图片即可，AI 会自动调用 MCP 工具。

### 示例对话
- "帮我搜索 XXX"
- "帮我分析这张图片"（发送图片）

## 费用说明

- 使用 MiniMax Token Plan 套餐
- 具体额度根据所订阅的套餐决定
- 详情见：https://platform.minimaxi.com/subscribe/token-plan

## 常见问题

### Q: mcporter list 看不到 minimax？
检查 MCP 配置是否正确，重启 OpenClaw 网关。

### Q: 图片理解失败？
- 检查图片 URL 是否可访问
- 本地文件路径需保证路径存在且有读取权限
- 支持格式：JPEG、PNG、GIF、WebP（最大 20MB）

### Q: 搜索结果为空？
检查 API Key 是否有效，是否有额度。

## 更新日志

### v1.0.0 (2026-03-22)
- 初始版本
- 支持 web_search 联网搜索
- 支持 understand_image 图片理解

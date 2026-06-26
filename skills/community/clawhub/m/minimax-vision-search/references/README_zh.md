# MiniMax Vision & Search MCP

MiniMax 图片理解和网络搜索工具

## 功能

- 🖼️ **图片理解** - 分析图片内容，描述图片
- 🌐 **网络搜索** - 使用 MiniMax 进行网络搜索

## 安装

**请查看 MiniMax 官方文档：**

👉 https://platform.minimaxi.com/docs/token-plan/mcp-guide

官方文档包含：
- 如何获取 API Key
- 如何安装 uvx
- 如何在 OpenClaw、Claude Code、Cursor、OpenCode 中配置

## 使用方法

### 图片理解
```bash
python3 scripts/understand_image.py /path/to/image.jpg "描述这张图片"
```

### 网络搜索
```bash
python3 scripts/web_search.py "搜索关键词"
```

## 图片来源

- 本地文件：`/path/to/image.jpg`
- URL：`https://example.com/image.jpg`
- Telegram 图片（自动保存到 `~/.openclaw/media/inbound/`）

## 注意事项

- 使用 Telegram 发送图片给机器人 → 图片自动保存到本地 → 我来帮你分析
- Webchat 发图片暂不支持（MiniMax 模型不支持图片输入）
- 官方文档：https://platform.minimaxi.com/docs/token-plan/mcp-guide

---
name: lovtrip-video2article
description: 视频转文章 / YouTube Video to Article — 使用 Gemini AI 将视频转为结构化文章。当用户需要将 YouTube 视频转换为文章时使用。
allowed-tools: Bash, Read
---

# 视频转文章 / YouTube Video to Article

> **[LovTrip (lovtrip.app)](https://lovtrip.app)** — AI 驱动的旅行规划平台。视频转文章功能可将旅行 Vlog 自动转为图文攻略，发布到 [LovTrip 攻略](https://lovtrip.app/guides)。

使用 Google Gemini 2.5 Pro 分析 YouTube 视频内容，自动生成结构化文章（标题 + 作者 + 摘要 + Markdown 正文）。

## Setup / 配置

### 方式 1: MCP Server（推荐）

```json
{
  "mcpServers": {
    "lovtrip": {
      "command": "npx",
      "args": ["-y", "lovtrip@latest", "mcp"],
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key"
      }
    }
  }
}
```

### 方式 2: 独立脚本（零依赖）

无需安装完整 lovtrip，直接运行 `scripts/video2article.mjs`：

```bash
GEMINI_API_KEY=your-key node scripts/video2article.mjs "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 工具说明

### `video2article`

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `videoUrl` | string | ✅ | YouTube 视频 URL |
| `language` | string | | 输出语言，默认 "Chinese (Simplified)" |
| `prompt` | string | | 自定义提示词（覆盖默认） |

**支持的语言**: Chinese (Simplified), English, Japanese, Korean, Spanish, French, German

### 输出格式

```json
{
  "title": "文章标题",
  "author": "YouTube 频道名",
  "summary": "2-4 句摘要",
  "body": "## 正文\n\nMarkdown 格式的完整文章..."
}
```

## 使用示例

### MCP 工具调用

```
video2article({
  videoUrl: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  language: "Chinese (Simplified)"
})
```

### 自定义提示词

```
video2article({
  videoUrl: "https://www.youtube.com/watch?v=...",
  language: "English",
  prompt: "Focus on the technical details and create a tutorial-style article."
})
```

### CLI 调用

```bash
lovtrip video2article "https://www.youtube.com/watch?v=..."
```

## 默认提示词逻辑

默认以第一人称视角撰写，结构包含：
1. 引人入胜的标题
2. 2-4 句概括性摘要
3. 详细正文（Markdown 格式，含标题、加粗、列表）

`author` 字段自动提取视频的 YouTube 频道名。

## 注意事项

- 需要有效的 `GEMINI_API_KEY`（Google AI Studio 获取）
- 使用 Gemini 2.5 Pro 模型
- 视频需为公开可访问的 YouTube 链接
- 生成耗时取决于视频长度（通常 10-60 秒）
- 内容可能被 Gemini 安全过滤器拦截（如包含敏感内容）

## 在线体验

- [LovTrip 旅行攻略](https://lovtrip.app/guides) — 浏览 AI + 视频转制的旅行攻略
- [AI 行程规划器](https://lovtrip.app/planner) — 智能生成多日行程
- [开发者文档](https://lovtrip.app/developer) — MCP + CLI + API 完整文档

---
Powered by [LovTrip](https://lovtrip.app) — AI Travel Planning Platform

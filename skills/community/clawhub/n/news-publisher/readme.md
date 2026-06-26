# OpenClaw News Publisher

**从 Markdown 到多平台的自动化新闻发布系统**

## 简介

OpenClaw News Publisher 是一个基于命令行的多平台新闻发布工具。用 Markdown 编写一次，一键发布到 RSS、微信、Twitter 等多个平台。

## 核心功能

✅ **多平台发布** - RSS、微信公众号、Twitter、头条、YouTube、抖音
✅ **Markdown 编写** - 标准 Markdown + YAML Front Matter
✅ **模板系统** - 内置多种新闻模板
✅ **自动降级** - 平台失败自动跳转下一个
✅ **发布历史** - JSON 格式记录发布状态
✅ **预览模式** - 发布前预览内容
✅ **Dry-run** - 测试发布流程不实际发布

## 快速开始

```bash
# 1. 创建新闻
openclaw-news create "AI 技术突破"

# 2. 编辑 Markdown 文件
vim news/drafts/ai-技术突破-*.md

# 3. 预览
openclaw-news preview news/drafts/ai-技术突破-*.md

# 4. 发布
openclaw-news publish news/drafts/ai-技术突破-*.md

# 5. 发布到指定平台
openclaw-news publish news/drafts/my-news.md --platforms rss,twitter

# 6. 测试发布（不实际发布）
openclaw-news publish news/drafts/my-news.md --dry-run
```

## 新闻格式

```markdown
---
title: "新闻标题"
author: "作者"
category: "科技"
tags: ["AI", "技术"]
platforms: ["rss", "twitter", "wechat"]
---

# 新闻标题

## 摘要
简短摘要...

## 正文
详细内容...
```

## 平台状态

| 平台 | 状态 | 说明 |
|------|------|------|
| **RSS Feed** | ✅ 完整实现 | RSS 2.0 自动生成 |
| **微信公众号** | 🚧 Beta | 架构就绪，API 待完善 |
| **Twitter/X** | 🚧 Beta | 架构就绪，OAuth 待实现 |
| **今日头条** | 🚧 占位符 | API 待实现 |
| **YouTube** | 🚧 占位符 | API 待实现 |
| **抖音** | 🚧 占位符 | API 待实现 |

## 配置

复制 `.env.example` 到 `.env`，填入平台凭据：

```bash
# 平台优先级
PUBLISH_PLATFORMS="rss,wechat,twitter"

# RSS 配置
RSS_SITE_URL="https://your-site.com"
RSS_FEED_URL="https://your-site.com/feed.xml"

# 微信配置
WECHAT_APP_ID="wx..."
WECHAT_APP_SECRET="..."

# Twitter 配置
TWITTER_API_KEY="..."
# ...更多配置见 .env.example
```

## CLI 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `create` | 创建新闻草稿 | `openclaw-news create "标题"` |
| `preview` | 预览新闻 | `openclaw-news preview <file>` |
| `publish` | 发布新闻 | `openclaw-news publish <file>` |
| `list` | 列出已发布 | `openclaw-news list` |
| `help` | 显示帮助 | `openclaw-news help` |

## 使用场景

### 1. 个人博客同步
写一次 Markdown，自动同步到微信公众号、Twitter、RSS

### 2. 新闻网站
每日新闻快速发布到多平台

### 3. 内容分发
企业新闻、公告一键多平台发布

### 4. 自媒体运营
统一内容管理，多平台同步更新

## 项目结构

```
openclaw-news-publisher/
├── news/
│   ├── templates/      # 新闻模板
│   ├── drafts/         # 草稿箱
│   └── published/      # 已发布（按日期）
├── scripts/
│   ├── platforms/      # 平台发布器
│   │   ├── rss/       # RSS 生成器
│   │   ├── wechat/    # 微信发布器
│   │   └── twitter/   # Twitter 发布器
│   ├── publish-news.sh # 主发布脚本
│   └── create-news.sh  # 创建脚本
├── agents/
│   └── news-cli.sh    # CLI 入口
└── public/
    └── feed.xml       # 生成的 RSS feed
```

## 高级特性

### 发布历史追踪

每次发布自动生成记录：

```json
{
  "article_id": "my-news",
  "platform": "rss",
  "status": "success",
  "published_at": "2026-03-10T12:00:00Z",
  "platform_url": "https://example.com/feed.xml"
}
```

### 自动降级

平台失败自动尝试下一个：

```
📤 Publishing to: rss      ✅ Success
📤 Publishing to: wechat   ❌ Failed (未配置)
📤 Publishing to: twitter  ✅ Success

📊 总结: 2 成功, 1 失败
```

### 模板系统

- `default.md` - 通用模板
- `tech-news.md` - 科技新闻模板
- 支持自定义模板

## 系统要求

- **Node.js**: >=18.0.0
- **操作系统**: Linux, macOS, WSL
- **平台凭据**: 需要各平台的 API 密钥

## 路线图

- [ ] 微信 API 完整实现
- [ ] Twitter OAuth 实现
- [ ] 头条 API 支持
- [ ] YouTube Data API
- [ ] Web 管理界面
- [ ] 定时发布系统
- [ ] 数据分析面板

## 文档

- **GitHub**: https://github.com/ZhenRobotics/openclaw-news-publisher
- **平台配置指南**: `docs/PLATFORMS.md`
- **Issues**: https://github.com/ZhenRobotics/openclaw-news-publisher/issues

## 许可证

MIT License - 可免费用于商业和个人项目

---

**版本**: 1.0.0
**作者**: justin
**状态**: 生产就绪（RSS），测试版（微信、Twitter）

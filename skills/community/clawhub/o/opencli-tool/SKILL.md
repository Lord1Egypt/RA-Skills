---
name: opencli
description: 使用 OpenCLI 工具从各种网站和桌面应用获取数据、下载媒体内容、控制外部 CLI 工具。支持 Bilibili、知乎、小红书、Twitter/X、Reddit、YouTube、Boss直聘、即刻、微博等 30+ 平台，以及 Cursor、Codex、ChatGPT、Notion 等桌面应用。当用户需要：从社交平台获取热门内容、搜索信息、下载视频/图片、获取平台数据、控制桌面应用、使用外部 CLI（gh、docker、kubectl）时，使用此 skill。触发词：bilibili、知乎、小红书、twitter、reddit、youtube、热门、下载视频、平台数据、opencli、网站数据、社交媒体。
---

# OpenCLI Skill

通过 OpenCLI 工具，让 AI Agent 能够访问和操作 30+ 网站、桌面应用和外部 CLI 工具。

## 核心能力

### 1. 网站数据获取
支持通过浏览器复用 Chrome 登录状态，从以下平台获取数据：
- **社交媒体**: Twitter/X, Reddit, 微博, 即刻
- **视频平台**: Bilibili, YouTube, 小红书
- **问答社区**: 知乎, V2EX, StackOverflow, Linux-Do
- **新闻资讯**: BBC, Bloomberg, Reuters, HackerNews, Dev.to
- **求职招聘**: Boss直聘, LinkedIn
- **电商购物**: Coupang, 什么值得买
- **金融财经**: 雪球, Yahoo Finance, Barchart
- **其他**: 微信读书, 携程, Wikipedia, arXiv, Steam

### 2. 桌面应用控制
控制本地安装的桌面应用（需要应用正在运行）：
- **Cursor**: 控制 Composer、提取代码、历史记录
- **Codex**: 驱动 OpenAI Codex CLI
- **ChatGPT**: 自动化 ChatGPT macOS 应用
- **ChatWise**: 多 LLM 客户端控制
- **Notion**: 搜索、读取、写入 Notion 页面
- **Discord**: 消息、频道、服务器操作
- **Antigravity**: 从终端控制 Antigravity Ultra
- **Grok**: Grok 桌面应用

### 3. 外部 CLI Hub
发现、自动安装和传递命令到外部 CLI：
- `gh` - GitHub CLI
- `docker` - Docker 命令行
- `kubectl` - Kubernetes 工具
- `obsidian` - Obsidian vault 管理
- `readwise` - Readwise & Reader CLI

### 4. 媒体下载
下载图片、视频和文章：
- **小红书**: 图片、视频
- **Bilibili**: 视频（需要 yt-dlp）
- **Twitter**: 图片、视频
- **知乎**: 文章（Markdown 格式）

## 使用前准备

### 安装 OpenCLI
```bash
npm install -g @jackwener/opencli
```

### 安装 Browser Bridge 扩展
1. 访问 GitHub Releases 页面下载最新扩展
2. 在 Chrome 打开 `chrome://extensions`
3. 启用开发者模式
4. 拖放 .crx 文件或解压后的文件夹

### 验证安装
```bash
opencli list          # 查看所有可用命令
opencli doctor        # 检查扩展和守护进程连接
opencli doctor --live # 测试实时浏览器命令
```

## 命令格式

### 基本格式
```bash
opencli <site> <command> [options]

# 示例
opencli bilibili hot --limit 10
opencli zhihu search --keyword "AI"
opencli twitter trending --limit 5
```

### 输出格式
支持多种输出格式：
```bash
opencli bilibili hot -f table  # 表格（默认）
opencli bilibili hot -f json   # JSON
opencli bilibili hot -f yaml   # YAML
opencli bilibili hot -f md     # Markdown
opencli bilibili hot -f csv    # CSV
```

### 详细模式
```bash
opencli bilibili hot -v  # 显示管道调试步骤
```

## 常用命令示例

### 获取热门内容
```bash
# Bilibili 热门
opencli bilibili hot --limit 10

# 知乎热榜
opencli zhihu hot

# Hacker News 热门
opencli hackernews top --limit 5

# 微博热搜
opencli weibo hot

# Reddit 热门
opencli reddit hot --limit 10
```

### 搜索
```bash
# Bilibili 搜索
opencli bilibili search --keyword "AI教程" --limit 10

# 知乎搜索
opencli zhihu search --keyword "机器学习"

# YouTube 搜索
opencli youtube search --keyword "OpenAI"

# arXiv 论文搜索
opencli arxiv search --keyword "transformer"

# 小红书搜索
opencli xiaohongshu search --keyword "美食"
```

### 下载媒体
```bash
# 下载 Bilibili 视频（需要 yt-dlp）
opencli bilibili download --bvid BV1xxx --output ./videos

# 下载小红书笔记媒体
opencli xiaohongshu download --note-id abc123 --output ./xhs

# 下载 Twitter 媒体
opencli twitter download elonmusk --limit 20 --output ./twitter

# 导出知乎文章
opencli zhihu download "https://zhuanlan.zhihu.com/p/xxx" --output ./zhihu
```

### 桌面应用控制
```bash
# Cursor 状态
opencli cursor status

# Notion 搜索
opencli notion search --query "项目"

# ChatGPT 发送消息
opencli chatgpt send --message "Hello"

# Discord 读取消息
opencli discord-app read
```

### 外部 CLI
```bash
# GitHub CLI
opencli gh pr list --limit 5

# Docker
opencli docker ps

# kubectl
opencli kubectl get pods
```

## 重要注意事项

### 浏览器命令
⚠️ **重要**: 浏览器命令会复用 Chrome 的登录状态。在运行命令前，确保：
1. Chrome 正在运行
2. 已在 Chrome 中登录目标网站
3. 如果返回空数据或未授权错误，检查登录状态

### 视频下载
视频下载需要安装 `yt-dlp`：
```bash
pip install yt-dlp
# 或
brew install yt-dlp
```

### 公开 API vs 浏览器命令
- **公开 API**: 不需要浏览器，直接访问（如 hackernews, bbc, wikipedia）
- **浏览器命令**: 需要Chrome 运行并登录（如 bilibili, zhihu, xiaohongshu）

## 探索和发现

### 查看所有可用命令
```bash
opencli list
opencli list -f yaml  # YAML 格式
```

### 探索新网站
```bash
# 深度探索网站API
opencli explore https://example.com --site mysite

# 生成 YAML 适配器
opencli synthesize mysite

# 一键生成
opencli generate https://example.com --goal "hot"
```

### 注册自己的 CLI
```bash
opencli register mycli
```

## 故障排除

### 扩展未连接
- 确保 Browser Bridge 扩展已安装并启用
- 检查 `chrome://extensions`

### 空数据或未授权错误
- 在 Chrome 中打开目标网站并登录
- 刷新页面确保会话有效

### Node API 错误
- 确保使用 Node.js >= 20.0.0

### 守护进程问题
```bash
curl localhost:19825/status  # 检查状态
curl localhost:19825/logs    # 查看日志
```

## 最佳实践

1. **先检查登录状态**: 浏览器命令前确保已在 Chrome 登录
2. **使用合适的输出格式**: JSON 适合管道处理，YAML 适合人类阅读
3. **限制结果数量**: 使用 `--limit` 避免返回过多数据
4. **验证安装**: 使用 `opencli doctor` 定期检查连接状态
5. **查看命令列表**: 定期运行 `opencli list` 发现新功能

## 项目信息

- **GitHub**: https://github.com/jackwener/opencli
- **NPM**: https://www.npmjs.com/package/@jackwener/opencli
- **License**: Apache-2.0
- **Node.js 要求**: >= 20.0.0

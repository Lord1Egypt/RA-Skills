---
name: opencli-rs
description: 基于Rust的通用命令行枢纽 - 将任何网站、桌面应用、本地CLI工具转变为命令行接口，专为AI Agent和自动化工作流设计。支持55+网站、Electron应用控制和外部CLI集成，单二进制文件4.7MB，性能提升12倍。
---

# SKILL.md - OpenCLI-RS (Rust版本) 通用命令行枢纽

## 概述

OpenCLI-RS 是基于 Rust 重写的通用 CLI 枢纽工具，能够将任何网站、本地工具、Electron 应用转变为命令行接口，专为 AI Agent 和自动化工作流设计。

**核心优势**:
- 🚀 **性能**: 相比TypeScript版本提升12倍，内存使用减少10倍
- 📦 **轻量**: 单二进制文件4.7MB，零运行时依赖
- 🔒 **安全**: Rust内存安全，无GC停顿
- 🤖 **AI原生**: 自动发现所有可用工具，支持AI Agent无缝调用

**GitHub仓库**: https://github.com/nashsu/opencli-rs

## 使用场景

**当以下情况时使用此技能**：
1. **AI Agent 自动化** - 需要让 AI 控制网站或桌面应用
2. **数据提取** - 从55+网站定时提取结构化数据
3. **桌面应用控制** - 控制 Electron 应用如 Cursor、Codex、ChatGPT、Notion、Discord 等
4. **外部 CLI 管理** - 统一管理 gh、docker、kubectl、obsidian 等 CLI 工具
5. **内容下载** - 下载图片、视频、文章等内容
6. **平台操作** - 在微博、B站、知乎、小红书等平台执行操作
7. **实时信息获取** - 获取新闻、趋势、社交媒体动态

## 快速开始

### 安装方法

#### 自动安装 (推荐)
```bash
# 使用官方安装脚本
curl -fsSL https://raw.githubusercontent.com/nashsu/opencli-rs/main/scripts/install.sh | sh
```

#### 手动安装
```bash
# 1. 下载对应平台的二进制文件
# Linux x86_64
wget https://github.com/nashsu/opencli-rs/releases/latest/download/opencli-rs-x86_64-unknown-linux-musl.tar.gz
tar -xzf opencli-rs-x86_64-unknown-linux-musl.tar.gz
sudo mv opencli-rs /usr/local/bin/

# 2. 验证安装
opencli-rs --version
```

#### 从源码编译
```bash
# 需要 Rust 工具链
git clone https://github.com/nashsu/opencli-rs.git
cd opencli-rs
cargo build --release
sudo cp target/release/opencli-rs /usr/local/bin/
```

### Chrome 扩展安装 (用于浏览器命令)
1. 从 [GitHub Releases](https://github.com/nashsu/opencli-rs/releases/latest) 下载 `opencli-rs-chrome-extension.zip`
2. 解压到任意目录
3. 打开 Chrome 并访问 `chrome://extensions`
4. 启用"开发者模式"（右上角开关）
5. 点击"加载已解压的扩展程序"并选择解压的文件夹
6. 扩展会自动连接到 opencli-rs 守护进程

**注意**: 公开API命令（如 hackernews、devto）无需扩展即可工作。

## 核心命令

### 基本使用
```bash
# 查看所有可用命令
opencli-rs --help

# 查看特定网站的命令帮助
opencli-rs hackernews --help
opencli-rs bilibili --help

# 获取Hacker News热门故事（无需浏览器）
opencli-rs hackernews top --limit 10

# JSON格式输出
opencli-rs hackernews top --limit 5 --format json

# 获取B站热门视频（需要浏览器+Cookie）
opencli-rs bilibili hot --limit 20

# 搜索Twitter（需要浏览器+登录）
opencli-rs twitter search "rust lang" --limit 10

# 运行诊断
opencli-rs doctor

# 生成Shell自动补全
opencli-rs completion bash >> ~/.bashrc
opencli-rs completion zsh >> ~/.zshrc
opencli-rs completion fish > ~/.config/fish/completions/opencli-rs.fish
```

### 桌面应用控制
```bash
# 控制Cursor编辑器
opencli-rs cursor status
opencli-rs cursor send "分析这段代码"

# 控制Codex编辑器
opencli-rs codex status
opencli-rs codex send "实现排序算法"

# 控制ChatGPT桌面版
opencli-rs chatgpt status
opencli-rs chatgpt send "解释量子计算"

# 控制Notion
opencli-rs notion search "项目文档"

# 控制Discord
opencli-rs discord-app channels
```

### 外部CLI集成
```bash
# GitHub CLI
opencli-rs gh repo list
opencli-rs gh pr list --limit 5

# Docker CLI
opencli-rs docker ps
opencli-rs docker images

# Kubernetes CLI
opencli-rs kubectl get pods
opencli-rs kubectl get nodes

# 其他工具
opencli-rs obsidian search "笔记"
opencli-rs readwise highlights
```

### 输出格式控制
```bash
# ASCII表格（默认）
opencli-rs hackernews top --format table

# JSON格式
opencli-rs hackernews top --format json

# YAML格式
opencli-rs hackernews top --format yaml

# CSV格式
opencli-rs hackernews top --format csv

# Markdown表格
opencli-rs hackernews top --format md
```

## 支持的网站和应用

### 公开API网站（无需浏览器）
- **Hacker News**: top, new, best, ask, show, jobs, search, user
- **Dev.to**: top, tag, user
- **Lobsters**: hot, newest, active, tag
- **Stack Overflow**: hot, search, bounties, unanswered
- **Steam**: top-sellers
- **arXiv**: search, paper
- **Wikipedia**: search, summary, random, trending
- **BBC**: news

### 需要浏览器的网站（55+站点）
- **Bilibili**: hot, search, me, favorite, history, feed, subtitle, dynamic, ranking, following, user-videos, download
- **Twitter/X**: trending, bookmarks, profile, search, timeline, thread, following, followers, notifications, post, reply, delete, like, article, follow, unfollow, bookmark, unbookmark, download, accept, reply-dm, block, unblock, hide-reply
- **Reddit**: hot, frontpage, popular, search, subreddit, read, user, user-posts, user-comments, upvote, save, comment, subscribe, saved, upvoted
- **知乎**: hot, search, question, download
- **小红书**: search, notifications, feed, user, download, publish, creator-notes, creator-note-detail, creator-notes-summary, creator-profile, creator-stats
- **微博**: hot, search
- **豆瓣**: search, top250, subject, marks, reviews, movie-hot, book-hot
- **YouTube**: search, video, transcript
- **Facebook**: feed, profile, search, friends, groups, events, notifications, memories, add-friend, join-group
- **Instagram**: explore, profile, search, user, followers, following, follow, unfollow, like, unlike, comment, save, unsave, saved

### 桌面应用控制
- **Cursor**: status, send, read, new, dump, composer, model, extract-code, ask, screenshot, history, export
- **Codex**: status, send, read, new, dump, extract-diff, model, ask, screenshot, history, export
- **ChatGPT**: status, new, send, read, ask
- **Notion**: status, search, read, new, write, sidebar, favorites, export
- **Discord**: status, send, read, channels, servers, search, members
- **Antigravity**: status, send, read, new, dump, extract-code, model, watch

## AI Agent 集成

### 自动发现工具
```bash
# AI可以自动发现所有可用工具
opencli-rs --help | grep -A5 "Available commands"

# 配置在AGENT.md中
echo "tools: opencli-rs list" >> AGENT.md
```

### 注册本地CLI工具
```bash
# 注册自定义CLI工具
opencli-rs register mycli --path /usr/local/bin/mycli

# AI可以无缝调用注册的工具
opencli-rs mycli --help
```

### AI原生功能
```bash
# 探索网站API
opencli-rs explore https://example.com

# 自动检测认证策略
opencli-rs cascade https://api.example.com/data

# 一键生成适配器
opencli-rs generate https://example.com --goal "hot posts"
```

## 高级功能

### YAML流水线定义
在 `~/.opencli-rs/adapters/` 创建自定义适配器：

```yaml
# ~/.opencli-rs/adapters/mysite/hot.yaml
site: mysite
name: hot
description: My site hot posts
strategy: public
browser: false

args:
  limit:
    type: int
    default: 20
    description: Number of items

columns: [rank, title, score]

pipeline:
  - fetch: https://api.mysite.com/hot
  - select: data.posts
  - map:
      rank: "${{ index + 1 }}"
      title: "${{ item.title }}"
      score: "${{ item.score }}"
  - limit: "${{ args.limit }}"
```

### 表达式语法
```bash
# 变量访问
"${{ args.limit }}"
"${{ item.title }}"

# 条件表达式
"${{ item.score > 10 }}"
"${{ item.active ? 'yes' : 'no' }}"

# 管道过滤器
"${{ item.title | truncate(30) }}"
"${{ item.tags | join(', ') }}"

# 字符串插值
"https://api.com/${{ item.id }}.json"
```

### 环境变量
```bash
# 启用详细输出
export OPENCLI_VERBOSE=1

# 更改守护进程端口
export OPENCLI_DAEMON_PORT=19826

# 命令超时设置
export OPENCLI_BROWSER_COMMAND_TIMEOUT=120
```

## 配置文件

### 用户目录结构
```
~/.opencli-rs/
├── adapters/          # 自定义适配器
├── plugins/           # 用户插件
└── external-clis.yaml # 外部CLI注册表
```

### 外部CLI注册
编辑 `~/.opencli-rs/external-clis.yaml`：
```yaml
- name: mytool
  description: My custom tool
  executable: /usr/local/bin/mytool
  arguments: []
  environment: {}
```

## 性能对比

| 指标 | opencli-rs (Rust) | opencli (Node.js) | 改进 |
|------|-------------------|-------------------|------|
| **内存使用(公开命令)** | 15 MB | 99 MB | 6.6x |
| **内存使用(浏览器命令)** | 9 MB | 95 MB | 10.6x |
| **二进制大小** | 4.7 MB | ~50 MB (node_modules) | 10x |
| **运行时依赖** | 无 | Node.js 20+ | 零依赖 |
| **真实命令执行时间** | 1.66s (B站热门) | 20.1s | 🔥 12x |

## 故障排除

### 常见问题

#### 1. Chrome扩展未连接
```bash
# 检查守护进程状态
opencli-rs doctor

# 重启守护进程
pkill -f opencli-rs
opencli-rs doctor
```

#### 2. 命令超时
```bash
# 增加超时时间
export OPENCLI_BROWSER_COMMAND_TIMEOUT=120
opencli-rs bilibili hot
```

#### 3. 浏览器未启动
```bash
# 确保Chrome正在运行
# 或使用指定的浏览器路径
export OPENCLI_BROWSER_PATH=/usr/bin/google-chrome
```

### 诊断命令
```bash
# 运行完整诊断
opencli-rs doctor

# 查看详细日志
export OPENCLI_VERBOSE=1
opencli-rs bilibili hot --limit 1

# 检查网络连接
curl -I https://github.com/nashsu/opencli-rs
```

## 更新和维护

### 更新到最新版本
```bash
# 重新运行安装脚本
curl -fsSL https://raw.githubusercontent.com/nashsu/opencli-rs/main/scripts/install.sh | sh

# 或手动下载最新版本
wget https://github.com/nashsu/opencli-rs/releases/latest/download/opencli-rs-x86_64-unknown-linux-musl.tar.gz
tar -xzf opencli-rs-x86_64-unknown-linux-musl.tar.gz
sudo mv opencli-rs /usr/local/bin/
```

### 卸载
```bash
# 删除二进制文件
sudo rm /usr/local/bin/opencli-rs

# 删除用户配置
rm -rf ~/.opencli-rs/

# 删除Chrome扩展
# 在 chrome://extensions 中移除扩展
```

## 技能最佳实践

### 与OpenClaw集成
```bash
# 在技能脚本中调用opencli-rs
#!/bin/bash
# fetch_news.sh - 获取新闻并输出为JSON
opencli-rs hackernews top --limit 20 --format json > news.json
```

### 定时任务
```bash
# 每小时获取B站热门视频
0 * * * * opencli-rs bilibili hot --limit 10 --format json > /tmp/bilibili_hot_$(date +\%Y\%m\%d-\%H).json
```

### AI Agent自动化
```bash
# 在AGENT.md中配置
tools:
  - name: opencli-rs
    description: Universal CLI hub for web, desktop, and local tools
    examples:
      - "Get trending news: opencli-rs hackernews top --limit 10"
      - "Search Twitter: opencli-rs twitter search 'AI news' --limit 5"
      - "Control Cursor: opencli-rs cursor send 'Analyze this code'"
```

## 许可证
Apache 2.0

## 贡献
- GitHub: https://github.com/nashsu/opencli-rs
- 问题反馈: https://github.com/nashsu/opencli-rs/issues
- Star历史: https://www.star-history.com/?repos=nashsu/opencli-rs

---

**🚀 现在您可以使用高性能的 opencli-rs 来控制55+网站、桌面应用和本地CLI工具了！**
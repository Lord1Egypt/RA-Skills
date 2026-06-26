---
name: opencli
description: "OpenCLI — 通用 CLI Hub，将任何网站、Electron 应用或本地工具转化为命令行接口。66+ 内置命令，支持 Bilibili/Twitter/Reddit/Xiaohongshu/GitHub 等。复用 Chrome 登录态，零 LLM 成本，确定性输出。"
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: [node]
      node: ">=20.0.0"
    setup: |
      npm install -g @jackwener/opencli@latest
    installed:
      version: "1.5.9"
      date: "2026-04-02"
---

# OpenCLI Skill

> Make any website, Electron App, or local tool your CLI.
> Zero risk, Reuse Chrome login, AI-powered discovery, Universal CLI Hub.

## 安装与验证

```bash
# 安装
npm install -g @jackwener/opencli@latest

# 验证
opencli --version
opencli list              # 查看所有可用命令
opencli doctor            # 检查扩展 + daemon 连通性
```

## 前提条件

- **Node.js** >= 20.0.0
- **Chrome 浏览器**（需登录目标网站）
- **Browser Bridge 扩展**（从 GitHub Releases 下载 opencli-extension.zip → chrome://extensions → 开发者模式 → 加载已解压的扩展）

## 常用命令速查

### 无需浏览器的 Public API 命令

```bash
opencli hackernews top --limit 5       # HackerNews 热榜
opencli v2ex hot --limit 5             # V2EX 热帖
opencli arxiv search "quantum"         # arXiv 论文搜索
opencli stackoverflow questions "rust"  # StackOverflow
opencli producthunt today              # Product Hunt
```

### 需要浏览器登录的命令

```bash
# Bilibili
opencli bilibili hot --limit 5         # 热榜
opencli bilibili search "AI"           # 搜索
opencli bilibili download BV1xxx       # 下载视频

# Twitter/X
opencli twitter trending                # 趋势
opencli twitter search "DeFi"           # 搜索
opencli twitter timeline --limit 10     # 时间线

# Reddit
opencli reddit hot --limit 5           # 热帖
opencli reddit search "ethereum"       # 搜索

# 小红书
opencli xiaohongshu search "美食"      # 搜索
opencli xiaohongshu note abc123        # 笔记详情

# GitHub (via gh CLI)
opencli gh pr list --limit 5           # GitHub PR 列表
opencli gh issue list                  # Issue 列表
```

### 输出格式

```bash
opencli bilibili hot -f json    # JSON 格式（适合管道/LLM）
opencli bilibili hot -f csv     # CSV 格式（适合表格）
opencli bilibili hot -f yaml    # YAML 格式
opencli bilibili hot -f md      # Markdown 格式
opencli bilibili hot -v         # Verbose 调试
```

### 外部 CLI 注册（CLI Hub）

```bash
opencli register mycli           # 注册本地 CLI，AI Agent 可通过 opencli list 发现
opencli gh pr list               # 自动检测并安装缺失工具
```

## AI Agent 开发新适配器

### 快速模式（单命令 4 步）

1. `browser_navigate` → 打开目标 URL
2. `browser_network_requests` → 筛选 JSON API
3. `browser_evaluate` → 用 fetch 验证接口
4. 写 YAML/TS adapter → build → test

### 认证层级

| 层级 | 条件 | 方案 |
|:---|:---|:---|
| Tier 1 | `fetch(url)` 直接能拿 | Public API (YAML, browser: false) |
| Tier 2 | 加 `credentials:'include'` | Cookie (YAML) |
| Tier 3 | 需 Bearer/CSRF header | Header (TS) |
| Tier 4 | 页面能请求但 fetch 不行 | Intercept (TS, installInterceptor) |

### 自动探索

```bash
opencli explore https://example.com --site mysite   # 发现 API
opencli synthesize mysite                            # 生成 YAML 适配器
opencli generate https://example.com --goal "hot"   # 一键生成
opencli cascade https://api.example.com/data         # 自动探测认证策略
```

## 退出码

| 码 | 含义 |
|:---|:---|
| 0 | 成功 |
| 66 | 空结果 |
| 69 | Browser Bridge 未连接 |
| 77 | 需要登录 |

## 故障排除

- "Extension not connected" → 安装 Browser Bridge 扩展到 chrome://extensions
- 空数据/Unauthorized → Chrome 中重新登录目标网站
- Daemon 问题 → `curl localhost:19825/status` 检查

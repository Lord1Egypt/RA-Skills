---
name: panscrapling-web-scraper
version: 1.0.0
description: |
  强大的网页抓取技能。基于 Scrapling，自动绕过 Cloudflare/反爬系统。
  
  触发词：抓取网页、爬取、scrape、fetch、抓取内容、提取网页、获取页面。
  
  使用场景：
  (1) 抓取被 Cloudflare 保护的网页
  (2) 提取页面内容
  (3) 网页数据采集
  (4) 动态渲染页面抓取
  
  自动安装：首次使用时自动检测并安装 Python 3.10+、Scrapling 及浏览器依赖。
  
  嵌入分发：包含所有依赖的 wheel 包，支持离线安装。
---

# Panscrapling Web Scraper

基于 [Scrapling](https://github.com/D4Vinci/Scrapling) 的网页抓取技能。
**自动绕过 Cloudflare Turnstile**，无需手动处理验证码。

## 特点

✅ **完全嵌入分发** - 包含所有 Python 依赖，支持离线安装
✅ **自动安装 Python** - 自动检测并安装 Python 3.10+
✅ **自动绕过 Cloudflare** - 无需手动处理验证码
✅ **多种抓取模式** - Fast / Stealthy / Dynamic

## 使用方式

直接说：
- "抓取 https://example.com 的内容"
- "用 Scrapling 抓取这个页面"
- "获取 https://xxx.com 的 .product 元素"

## 抓取模式

| 模式 | 用途 | 特点 |
|------|------|------|
| `auto` | 自动选择 | 默认模式，适合大多数情况 |
| `stealthy` | 隐身抓取 | 绕过 Cloudflare，解验证码 |
| `dynamic` | 动态渲染 | 完整浏览器，JS 执行 |
| `fast` | 快速 HTTP | 轻量级，适合简单页面 |

## CLI 使用

```bash
# 基础抓取
python3 scripts/fetch.py "https://example.com"

# 绕过 Cloudflare
python3 scripts/fetch.py "https://protected-site.com" --mode stealthy

# 提取特定元素
python3 scripts/fetch.py "https://shop.com" --selector ".product-title"

# 输出 Markdown
python3 scripts/fetch.py "https://blog.com/article" --markdown

# 提取链接、图片、元数据
python3 scripts/fetch.py "https://example.com" --links --images --meta

# 仅运行安装
python3 scripts/fetch.py --setup
```

## 自动安装流程

首次使用时自动执行：

1. **检测 Python 3.10+** - 查找系统已安装的 Python
2. **安装 Python** - 如果未找到，通过 Homebrew 自动安装
3. **安装依赖** - 从嵌入的 wheel 包安装 Scrapling
4. **安装浏览器** - 下载 Playwright/Patchright Chromium

## 与 pansxng-websearch 配合

- **pansxng-websearch**: 搜索引擎查询 → 获取链接列表
- **panscrapling-web-scraper**: 深入抓取页面 → 提取具体内容

典型工作流：
1. 用 pansxng-websearch 搜索关键词
2. 用 panscrapling-web-scraper 抓取目标页面

## 文件结构

```
panscrapling-web-scraper/
├── SKILL.md              # 本文档
├── scripts/
│   ├── setup.py          # 自动安装脚本
│   └── fetch.py          # 主抓取脚本
├── wheels/               # 嵌入的 Python 依赖包
│   ├── scrapling-*.whl
│   ├── playwright-*.whl
│   ├── patchright-*.whl
│   └── ... (其他依赖)
└── browsers/             # 浏览器（首次运行时下载）
```

## 隐私说明

- 所有请求通过本地浏览器发出
- 无第三方 API 调用
- 不泄露搜索/抓取记录

## 依赖

- Python 3.10+（自动安装）
- Homebrew（macOS，自动安装）
- Playwright Chromium（自动下载）

# markdown-bundle-browser：md 一键打包成可视化知识库

把一堆 Markdown 文件打包成单个 HTML 文档浏览器，带目录树、搜索、离线渲染，双击就能看。

Agent 工作流里 md 越攒越多，人脑看不过来。这个工具一行命令，把整个目录的 md 打包成一个自包含的 HTML，左侧是真实目录树，右侧是渲染好的文档正文，还有全局搜索和文档互链。

## 适合谁用

- 用 AI 做行业研究、攒了一堆 md 素材库的人
- 项目交付时想甩一个文件给对方、而不是十几个文件夹的人
- 需要离线浏览文档集合（无服务器、无网络）的团队和个人

## 快速开始

```bash
# 直接跑，零依赖（Python 3.6+）
python3 scripts/bundle.py <md目录> --output index.html --title "我的知识库"
```

生成的 HTML 完全自包含：不依赖任何 CDN、不需要服务器、断网也能打开。双击即用。

可选 YAML 配置自定义分组：

```yaml
title: "我的知识库"
order: ["入口", "研究数据", "公司档案", "其他"]
group_rules:
  - match: "data/company_profiles"
    group: "公司档案"
    icon: "🏢"
```

```bash
python3 scripts/bundle.py <md目录> --config bundle.yaml
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `scripts/bundle.py` | 核心打包脚本，纯 Python 标准库，零第三方依赖 |
| `SKILL.md` | 给 AI 用的技能说明，Agent 可直接调用此流程 |

## 核心能力

- **离线渲染**：内置轻量 GFM 渲染器（标题/列表/表格/引用/代码块/图片/外链），不依赖 marked.js
- **真实目录树**：按目录嵌套展开折叠，层级结构清晰
- **全局搜索**：标题+正文实时过滤，文档一多找得到
- **文档互链**：md 内部相对链接自动转成可点击跳转
- **懒加载**：点开才渲染正文，100+ 文档也不卡
- **自动目录**：h2/h3 标题自动生成页内目录
- **自动打开首篇**：打开 HTML 即有内容，无需手动点选

## 推荐流程

1. 确认 md 目录结构（建议按主题分文件夹）
2. 跑 `bundle.py` 生成 HTML
3. 浏览器打开验证渲染效果
4. 把单个 HTML 分享出去（邮件/网盘/聊天窗口）

---

# markdown-bundle-browser: bundle your .md files into a browsable knowledge base

Pack a directory of Markdown files into a single self-contained HTML document browser with a real directory tree, global search, and offline rendering. Double-click and read.

The more .md files an agent workflow accumulates, the harder they are to skim. This tool turns an entire directory into one portable HTML: a nested directory tree on the left, rendered document content on the right, plus global search and cross-document links.

## Who it's for

- People doing AI-assisted research who accumulate large .md libraries
- Anyone delivering a project as one file instead of dozens of folders
- Teams and individuals who need offline document browsing (no server, no network)

## Quick start

```bash
# Zero dependencies (Python 3.6+)
python3 scripts/bundle.py <md-dir> --output index.html --title "My Knowledge Base"
```

The generated HTML is fully self-contained: no CDN, no server, works offline. Just double-click it.

Optional YAML config for custom grouping:

```yaml
title: "My Knowledge Base"
order: ["入口", "研究数据", "公司档案", "其他"]
group_rules:
  - match: "data/company_profiles"
    group: "公司档案"
    icon: "🏢"
```

```bash
python3 scripts/bundle.py <md-dir> --config bundle.yaml
```

## Files

| File | Purpose |
|------|---------|
| `scripts/bundle.py` | Core bundler, pure Python standard library, zero third-party deps |
| `SKILL.md` | Agent-facing skill spec — an AI can call this workflow directly |

## Core features

- **Offline rendering**: built-in lightweight GFM renderer (headings/lists/tables/quotes/code blocks/images/links), no marked.js dependency
- **Real directory tree**: nested folders with expand/collapse, clear hierarchy
- **Global search**: real-time filter across titles AND content
- **Cross-document links**: relative .md links become clickable jumps
- **Lazy rendering**: content parsed only when opened — handles 100+ files
- **Auto TOC**: h2/h3 headings generate an in-page table of contents
- **Auto-open first doc**: the HTML opens with content, no clicking needed

## Recommended workflow

1. Confirm the md directory structure (group by topic folders)
2. Run `bundle.py` to generate the HTML
3. Open in a browser to verify rendering
4. Share the single HTML (email / cloud drive / chat)

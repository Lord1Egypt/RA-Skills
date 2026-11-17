---
name: markdown-bundle-browser
description: |-
  将多个 Markdown 文件打包成自包含的单页 HTML 文档浏览器（v2：离线渲染/搜索/目录树）。当用户需要浏览/查看多个 .md 文件、
  或反馈 .md 链接无法打开时触发。适用于项目文档集合、研究系统输出、知识库浏览等场景。
  生成的 HTML 内嵌所有文档内容和内置渲染器，不依赖任何 CDN，断网也能用，浏览器直接打开即可。
agent_created: true
---

# Markdown Bundle Browser

## Purpose

Generate a single self-contained HTML file that embeds all markdown files from a directory.
The result is a dark-themed document browser with a real directory tree, global search,
offline markdown rendering and cross-document links — no server, no CDN, no network needed.

## When to Use

Trigger when:
- User asks to "view all documents" / "浏览所有文档" from a project
- User reports that clicking .md file links doesn't work (browser cannot render raw markdown)
- User wants a single-page overview of a multi-file documentation set
- After completing a research project bootstrap (to package all deliverables)
- Any time there are 3+ markdown files and the user wants to browse them
- User wants to share a knowledge base as one portable HTML file

## v2 Features

| Feature | What it does |
|---------|-------------|
| 离线渲染 | 内置轻量 GFM 渲染器，零 CDN 依赖，断网可用 |
| 真实目录树 | 按目录嵌套展开/折叠，层级结构清晰 |
| 全局搜索 | 按标题+正文实时过滤文件 |
| 配置分组 | 可选 YAML 配置自定义分组/徽章/顺序 |
| 文档互链 | md 内部相对链接自动可点跳转 |
| 懒加载 | 点开文件才渲染正文，大文档集不卡 |
| 自动目录 | 文档内 h2/h3 自动生成页内目录 |
| 自动打开 | 打开即显示第一篇，无需手动点选 |

## Workflow

### Step 1: Locate Markdown Files

Identify the root directory containing markdown files. This is usually the project root or a `docs/` directory. If the user specifies a specific folder, use that.

### Step 2: Run the Bundle Script

Execute the bundled Python script:

```bash
python3 scripts/bundle.py <directory> [--output index.html] [--title "My Title"]
```

Parameters:
- `directory` (required): Path to the root directory containing .md files. Recursively finds all .md files.
- `--output` (optional): Output HTML path. Defaults to `index.html` in the source directory.
- `--title` (optional): Browser page title. Defaults to "文档浏览".

The script:
1. Recursively finds all `.md` files (excluding hidden directories)
2. Reads each file's content
3. Builds a real directory tree (nested, expandable/collapsible)
4. Auto-assigns status badges based on filename heuristics or YAML config
5. Generates a single HTML with embedded content + built-in offline renderer
6. Reports file count and output size

### Step 3: Preview the Result

After generation, use `preview_url` / `present_files` to open the HTML file for the user.

### Step 4: Deliver

Attach both the generated HTML and the original markdown files if the user wants them.

## Generated HTML Features

- **Directory tree sidebar**: Nested folders with expand/collapse, not flat groups
- **Global search**: Filter files by title AND content in real time
- **Offline markdown rendering**: Built-in lightweight GFM renderer, zero CDN
- **Status badges**: Each file gets a badge (完成/数据/实时/模板/积压)
- **Cross-document links**: Relative `.md` links in content become clickable jumps
- **Auto TOC**: h2/h3 headings generate an in-page table of contents
- **Lazy rendering**: Content parsed only when opened — handles 100+ files
- **Dark theme + responsive**: Sidebar auto-hides on mobile
- **Self-contained**: All contents embedded — no server, no network, no file:// issues

## Optional YAML Config

```yaml
title: "My Knowledge Base"
order: ["入口", "研究数据", "公司档案", "其他"]
group_rules:
  - match: "data/company_profiles"
    group: "公司档案"
    icon: "🏢"
badges:
  - match: "财报"
    label: "财报"
```

Run with: `python3 bundle.py <dir> --config bundle.yaml`

## Category Auto-Detection (fallback when no config)

- **入口**: README.md, MODULES.md
- **研究数据**: Files under `data/` directory
- **公司档案**: Files under `data/company_profiles/` or containing "公司"
- **任务与工作流**: Files under `tasks/` or `agents/`
- **模板**: Files under `templates/` or containing "template"
- **其他**: Everything else

## Limitations

- Very large markdown files (>100KB each) make the HTML larger but still load fine (lazy rendering)
- Badges are filename-heuristic based unless overridden via config
- The script skips hidden directories (starting with `.`)
- Emoji and special Unicode should work but test if issues arise

---
slug: md2pdf
displayName: "md2pdf / Markdown 转 PDF"
name: md2pdf
description: |
  将 Markdown 渲染为排版精美的 PDF，支持封面/目录/书签/页码/KaTeX/Mermaid/代码高亮。
  Render Markdown to beautifully typeset PDF. Cover/TOC/bookmarks/page numbers/KaTeX/Mermaid/highlighting.
author: CoderMoray
version: "1.7.0"
tags:
  - "文档处理"
  - "PDF生成"
  - "document-conversion"
  - "markdown"
  - "pdf"
category: "utility"
---

# md2pdf — Markdown 转 PDF

将 Markdown 文件转换为排版精美的 PDF，不依赖 AI 语义理解。

---

## Skill 初始化

当此 Skill 首次加载时，执行以下步骤：

### 1. 环境检测

```bash
python3 scripts/md2pdf.py --validate
```

输出示例：
```
=======================================================
  md2pdf — 环境检测
  语言环境: 🇨🇳 中文
=======================================================
  ✅ pandoc: pandoc 2.12
    路径: /opt/homebrew/bin/pandoc
  ✅ 系统浏览器: Google Chrome 128.0.6613.137
    路径: /Applications/Google Chrome.app/...
  ✅ Playwright: via /usr/bin/python3
    路径: /usr/bin/python3
  ✅ Chromium: Playwright 内置 Chromium 就绪

  🎨 可用主题: default, academic
  🟢 环境就绪，可以转换。
```

### 2. 安装缺失组件（如需）

如果环境检测失败，依次安装缺失组件：

**缺失 pandoc：** 运行 `brew install pandoc`

**缺失 Playwright + Chromium：**
- 英文语境：`pip install playwright && playwright install chromium`
- **中文/国内用户**，建议使用镜像源加速：
  ```bash
  PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/playwright \
  pip install playwright && playwright install chromium
  ```

> AI 应检测用户的语言环境（如 `LANG=zh_CN`），自动选择是否显示镜像源提示。

### 2. 用户偏好配置

### 3. 用户偏好配置

主动询问用户以下偏好，写入 `output/user-config.json`：

```json
{
  "theme": "default",
  "font_size": 14,
  "page_size": "A4",
  "toc": true,
  "cover": true,
  "toc_depth": 4
}
```

如果用户跳过配置，使用上述默认值。

### 3. 输出目录

- 生成的 PDF 存储在 `output/` 目录下
- 如果用户指定了输出路径，则以用户指定的为准
- `output/` 中的文件不会被 git 跟踪（仅保留 `.gitkeep`）

---

## 能力边界

| 擅长 | 不擅长 |
|------|--------|
| Markdown → PDF 转换 | 合并多个 MD 为单个 PDF |
| 封面页（从 front-matter 自动生成） | 从零创建 PDF（请先写 MD） |
| 交互式目录 + PDF 侧边栏书签 | 分栏布局 |
| 页码、多主题切换（default/academic） | 动态页眉页脚自定义 |
| 中文排版增强（--chinese-layout） | 加密/水印/签名 PDF |
| KaTeX 数学公式（pandoc --katex） | 复杂 LaTeX 数学环境 |
| Mermaid 图表（注入 mermaid.js 渲染） | 动态/交互式图表 |
| 代码语法高亮（highlight.js，190+ 语言） | — |
| 智能分页（H1 另起页、代码块/表格保持完整） | — |
| 自定义字号和纸张大小 | 深度排版控制 |
| 环境自检（--validate） | — |

---

## 输入

### Markdown front-matter（封面数据）

在 MD 文件头部使用 YAML 格式声明封面信息，所有字段均为可选：

```yaml
---
title: "文档标题"
subtitle: "副标题（可选）"
author: "作者名"
date: "2026-06-26"
version: "1.7.0"
---
```

### CLI 参数

| 参数 | 是否必需 | 说明 |
|------|---------|------|
| `--input <path>` | ✅ | 输入 Markdown 文件路径 |
| `--output <path>` | ❌ | 输出 PDF 路径，不指定则自动生成 |
| `--theme <name>` | ❌ | 主题：default / academic，默认 default |
| `--chinese-layout` | ❌ | 叠加中文排版增强（行距、缩进、禁则），配合任意主题 |
| `--cover` / `--no-cover` | ❌ | 是否生成封面页，默认开启。无 front-matter 时自动用文件名 |
| `--toc` / `--no-toc` | ❌ | 是否生成目录，默认开启 |
| `--toc-depth <n>` | ❌ | 目录深度 1-6，默认 4 |
| `--font-size <px>` | ❌ | 正文字号，默认 14px |
| `--font-family <name>` | ❌ | 正文字体，覆盖主题默认字体 |
| `--page-size <format>` | ❌ | A4 / A3 / letter / legal，默认 A4 |
| `--katex` | ❌ | 启用 KaTeX 数学公式渲染 |
| `--mermaid` | ❌ | 启用 Mermaid 图表渲染 |
| `--highlight` / `--no-highlight` | ❌ | 代码语法高亮（highlight.js），默认开启 |
| `--header <text>` / `--no-header` | ❌ | 自定义页眉文字，默认从 config.json 读取 |
| `--watermark <text>` / `--no-watermark` | ❌ | 水印文字（半透明平铺），默认从 config.json 读取 |
| `--password <pwd>` | ❌ | PDF 打开密码（需安装 pikepdf） |
| `--validate` | ❌ | 环境检测模式，不执行转换 |
| `--list-themes` | ❌ | 列出可用主题 |

---

## 工作流

### 第 0 步：初始化配置（首次使用）

检查 `config.json` 中页眉/水印/加密的默认值是否已设置。若均为空，引导用户选择：

1. **页眉**：是否需要默认页眉？如"XX公司 · 内部文档"
2. **水印**：是否需要默认水印？如"机密"、"DRAFT"
3. **加密**：是否默认加密？（建议默认关闭）

**如果用户启用水印或加密，先检查依赖：**
- 水印依赖 PyMuPDF（`python3 -c "import fitz"`）
- 加密依赖 pikepdf（`python3 -c "import pikepdf"`）
- 若缺失，提示安装命令（`pip install pymupdf` / `pip install pikepdf`）

用户也可在后续每次转换时通过 `--header`、`--watermark`、`--password` 显式覆盖。

### 第 1 步：确认需求

确认用户提供的 Markdown 文件路径，确认是否需要封面、目录、主题、中文排版、页眉、水印、加密等。

**主题和排版：**
- `--theme default`：苹果风格（默认）
- `--theme academic`：学术风格
- `--chinese-layout`：叠加中文排版增强（2倍行距、首行缩进、禁则处理），可配合任意主题

**封面行为（智能默认）：**
- 如果 MD 文件头部有 YAML front-matter 的 `title` 字段 → 以此为封面标题
- 如果 MD 没有 front-matter → 自动用文件名作为封面标题（如 `技术方案.md` → 封面显示"技术方案"）
- 如果用户不需要封面 → 传 `--no-cover`

**如果用户想要更丰富的封面信息，指导其添加 front-matter：**

```yaml
---
title: "报告标题"
author: "作者"
date: "2026-06-26"
---
```

### 第 2 步：环境检测

首次使用或环境变更后，先运行环境检测：

```bash
python3 scripts/md2pdf.py --validate
```

输出示例：
```
=======================================================
  md2pdf — 环境检测
=======================================================
  ✅ pandoc: pandoc 2.12
    路径: ...
  ✅ Playwright: Version 1.56.0
    路径: ...
  ✅ Chromium: 就绪

  🎨 可用主题: default, academic
  🟢 环境就绪，可以转换。
```

**环境不完整时：**
- pandoc 缺失 → `brew install pandoc`
- Playwright 缺失 → `pip install playwright && playwright install chromium`

### 第 3 步：执行转换

```bash
# 基本用法（AI 拼装命令后执行）
python3 scripts/md2pdf.py --input /path/to/doc.md

# 切换主题 + 中文排版
python3 scripts/md2pdf.py --input doc.md --theme academic --chinese-layout

# 自定义封面/目录
python3 scripts/md2pdf.py --input doc.md --no-cover --toc-depth 2

# 自定义字号和纸张
python3 scripts/md2pdf.py --input doc.md --font-size 16 --page-size A3

# 无封面、无目录的简洁模式
python3 scripts/md2pdf.py --input doc.md --no-cover --no-toc

# 启用 KaTeX 数学公式
python3 scripts/md2pdf.py --input doc.md --katex

# 启用 Mermaid 图表
python3 scripts/md2pdf.py --input doc.md --mermaid

# 同时启用 KaTeX + Mermaid
python3 scripts/md2pdf.py --input doc.md --katex --mermaid
```

### 第 4 步：验证输出

转换完成后确认：
- PDF 文件已生成
- 文件大小不为 0（一般 300KB+）
- 封面/目录/页码是否按预期生成
- 打开确认排版无误，侧边栏有 PDF 书签

**如果出现异常：** 脚本已输出带常见原因的错误信息。若需进一步排查，查阅 `docs/FAQ.md`。

---

## 架构

```
管线: Markdown → 解析 front-matter → pandoc (--toc, --katex) →
      注入封面 HTML → 注入 CSS 主题 → 注入 Mermaid.js/highlight.js（本地缓存）→
      Playwright PDF (等待 Mermaid 渲染 → 输出)
         ↑                                    ↑
    commonmark_x 解析                    outline + 页脚模板
```

**为什么这样设计：**
- pandoc 处理 Markdown 解析，不依赖 AI 理解
- Playwright 使用真实 Chromium 浏览器渲染，输出与预览一致
- 封面/目录/页码全部由脚本自动处理，无需 AI 干预
- PDF 书签（outline）让阅读器侧边栏可交互跳转
- Mermaid.js、highlight.js 首次自动下载并本地缓存，后续离线可用
- 无 front-matter 时封面自动用文件名，不会出现空白页
- 分页保护：代码块/表格/引用/图表保持完整，标题不孤行
- 结果可复现：同一份 MD 每次输出完全相同的 PDF

### PDF 交互特性

| 特性 | 说明 |
|------|------|
| 📑 可点击目录页 | TOC 中的条目可点击跳转到对应章节 |
| 📌 侧边栏书签 | Playwright `outline: true` 生成 PDF 书签树 |
| 🔢 居中页码 | 每页底部自动显示页码 |

---

## 输出

转换成功后输出：`✅ 转换完成: /path/to/output.pdf (629 KB)`

失败时输出错误信息到 stderr，退出码为 1。

### 输出路径规则

| 条件 | 输出路径 |
|------|---------|
| 用户指定了 `--output` | 以用户指定为准 |
| 未指定 `--output`，MD 文件在本项目外 | MD 同目录下同名 `.pdf` |
| 未指定 `--output`，MD 文件在技能目录内 | `output/<文件名>.pdf` |

---

## 常见问题

**转换异常或结果不符合预期时，第一时间查阅 `docs/FAQ.md`**。

该文件覆盖：
- 转换超时 / PDF 未生成 / 页数异常
- 封面空白 / 目录为空 / 主题不对
- 中文方块 / 字体选择 / Mermaid/KaTeX 不渲染
- 错误信息解读（pandoc 失败、Playwright 失败等）

FAQ 中的每个条目均包含原因分析和可执行的解决方案，AI 可直接引用回复用户。

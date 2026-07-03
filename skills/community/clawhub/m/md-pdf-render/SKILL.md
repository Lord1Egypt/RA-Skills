---
name: "md-pdf-render"
description: "将 Markdown 文件转换为高保真 PDF，效果与编辑器预览完全一致。支持 GFM 语法、代码高亮、表格、任务列表、目录生成、自定义 CSS 和多种主题。"
version: "1.0.0"
tags: ["markdown", "pdf", "convert", "export", "document", "github-flavored"]
bindShells: ["ClaudeCode"]
---

# md-pdf-render Skill

将 Markdown 文件转换为 PDF，渲染效果与编辑器 Markdown 预览完全一致。

**核心能力：**

| 特性 | 说明 |
|------|------|
| GFM 完整支持 | 表格、任务列表、脚注、自动链接 |
| 代码高亮 | highlight.js 190+ 语言 |
| 主题切换 | GitHub 风格（默认）、VS Code 暗色 |
| 自定义 CSS | 支持加载外部样式覆盖 |
| 目录生成 | `--toc` 自动提取 h1-h3 |
| 多纸张格式 | A4 / Letter / A3，横竖版 |

---

## 使用方法

### 第一步 —— 确认依赖

脚本位于 skill 的 `scripts/` 目录，首次使用需安装依赖：

```bash
cd <skill-path>/scripts && npm install
```

需要系统安装 Chromium（Puppeteer 会自动下载）。

### 第二步 —— 执行转换

```bash
node <skill-path>/scripts/md-pdf-render.mjs <输入文件.md> [输出文件.pdf] [选项]
```

**选项：**

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--theme <name>` | 主题：`github` \| `vscode` | `github` |
| `--css <path>` | 自定义 CSS 文件 | 无 |
| `--margin <value>` | 页面边距 | `15mm` |
| `--format <size>` | 纸张：`A4` \| `Letter` \| `A3` | `A4` |
| `--landscape` | 横向排版 | 否 |
| `--toc` | 生成目录 | 否 |
| `--mermaid` | 启用 Mermaid 图表渲染 | 否 |

### 第三步 —— 验证输出

用 `open <output.pdf>`（macOS）或 `xdg-open`（Linux）打开确认效果。

---

## 示例

### 基本转换

```bash
node md-pdf-render.mjs README.md
# 输出: README.pdf (GitHub 风格)
```

### 暗色主题 + 目录

```bash
node md-pdf-render.mjs docs/guide.md guide.pdf --theme vscode --toc
```

### 自定义样式 + Letter 纸张

```bash
node md-pdf-render.mjs report.md --css brand.css --format Letter --margin 20mm
```

### 批量转换（配合 shell）

```bash
for f in docs/*.md; do
  node md-pdf-render.mjs "$f"
done
```

---

## 自定义 CSS

创建 CSS 文件覆盖默认样式：

```css
/* brand.css — 自定义品牌风格 */
:root {
  --color-fg: #333;
  --color-link: #e63946;
  --font-body: "Noto Sans SC", sans-serif;
}
h1 { color: #1d3557; }
pre { border: 1px solid #ddd; }
```

通过 `--css brand.css` 加载。

---

## 工作原理

```
Markdown 文件
    ↓ markdown-it (GFM 解析)
HTML + highlight.js 代码高亮
    ↓ 注入主题 CSS
完整 HTML 页面
    ↓ Puppeteer (Chromium 无头浏览器)
高保真 PDF
```

使用 Puppeteer 调用 Chromium 渲染引擎，确保与浏览器/编辑器预览效果完全一致。

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 中文字体缺失 | 安装 Noto Sans SC 或通过 `--css` 指定字体 |
| 代码块被截断 | 增加 `--margin` 或使用 `--landscape` |
| 图片未加载 | 确保图片使用相对路径或本地绝对路径 |
| PDF 空白 | 检查 Puppeteer/Chromium 是否安装成功 |
| 表格溢出 | 使用 `--landscape` 或自定义 CSS 缩小字号 |

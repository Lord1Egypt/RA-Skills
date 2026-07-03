# md-pdf-render

将 Markdown 文件转换为高保真 PDF，渲染效果与编辑器 Markdown 预览完全一致。

## 特性

- **所见即所得** — 使用 Chromium 渲染，与 VS Code / GitHub 预览一致
- **GFM 完整支持** — 表格、任务列表、脚注、自动链接、HTML 内嵌
- **代码高亮** — highlight.js 支持 190+ 编程语言
- **数学公式** — KaTeX 渲染 LaTeX 公式（行内 `$...$` 和块级 `$$...$$`）
- **Emoji 支持** — GitHub 风格 Emoji `:smile:` `:rocket:`
- **Mermaid 图表** — 支持流程图、序列图、类图等 14 种图表类型
- **主题切换** — GitHub 亮色（默认）、VS Code 暗色
- **自定义 CSS** — 支持加载外部样式文件覆盖默认主题
- **目录生成** — `--toc` 自动提取标题生成目录
- **PDF 书签** — 自动生成标题大纲，方便导航
- **页眉页脚** — 自定义页眉页脚，支持页码和标题
- **分页优化** — 智能分页，避免代码块、表格被截断
- **灵活配置** — 纸张大小、边距、横竖版均可调节

## 快速开始

### 安装依赖

```bash
cd scripts && npm install
```

> 需要 Node.js >= 18。Puppeteer 会自动下载 Chromium。

### 基本用法

```bash
# 转换单个文件（输出同名 .pdf）
node scripts/md-pdf-render.mjs README.md

# 指定输出路径
node scripts/md-pdf-render.mjs docs/guide.md output/guide.pdf

# 暗色主题 + 目录
node scripts/md-pdf-render.mjs notes.md --theme vscode --toc

# 自定义样式 + Letter 纸张
node scripts/md-pdf-render.mjs report.md --css brand.css --format Letter
```

### 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--theme <name>` | 主题：`github` \| `vscode` | `github` |
| `--css <path>` | 自定义 CSS 文件路径 | 无 |
| `--margin <value>` | 页面边距 | `15mm` |
| `--format <size>` | 纸张大小：`A4` \| `Letter` \| `A3` | `A4` |
| `--landscape` | 横向排版 | 否 |
| `--toc` | 生成目录（提取 h1-h3） | 否 |
| `--mermaid` | 启用 Mermaid 图表渲染 | 否 |
| `--header <text>` | 页眉文本（支持 `%title%`, `%page%`, `%total%`） | 无 |
| `--footer <text>` | 页脚文本（支持 `%title%`, `%page%`, `%total%`） | `%page% / %total%` |
| `--no-math` | 禁用数学公式渲染 | 否 |
| `--no-emoji` | 禁用 Emoji 渲染 | 否 |
| `--timeout <ms>` | 超时时间（毫秒） | `60000` |

## 工作原理

```
Markdown → markdown-it (GFM + Emoji + KaTeX) → HTML + highlight.js → Puppeteer → PDF
                                              ↓
                                      Mermaid (可选) → SVG
```

1. **解析**: markdown-it 将 Markdown 转为 HTML，支持 GFM 扩展语法
2. **Emoji**: 自动转换 `:emoji:` 语法为系统 Emoji
3. **数学公式**: KaTeX 渲染 LaTeX 公式为高质量数学符号
4. **高亮**: highlight.js 对代码块进行语法着色
5. **Mermaid**: 如果启用，将 Mermaid 代码块渲染为 SVG 图表
6. **样式**: 注入与 GitHub/VS Code 一致的 CSS 主题
7. **渲染**: Puppeteer 启动 Chromium 无头浏览器加载 HTML
8. **输出**: Chromium 打印为 PDF，保留完整排版和样式

## 数学公式

使用 KaTeX 渲染 LaTeX 数学公式：

```markdown
行内公式：$E = mc^2$

块级公式：

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

**特性**:
- 行内公式使用 `$...$` 语法
- 块级公式使用 `$$...$$` 语法
- 支持所有标准 LaTeX 数学语法
- 自动加载 KaTeX CSS 样式

**禁用**: 使用 `--no-math` 选项

## Emoji 支持

支持 GitHub 风格 Emoji：

```markdown
今天心情不错 :smile:，项目上线了 :rocket:！

注意事项 :warning:：确保质量 :100:
```

**常用 Emoji**:
- 表情: `:smile:` `:laughing:` `:blush:` `:heart_eyes:`
- 手势: `:+1:` `:clap:` `:wave:` `:muscle:`
- 物体: `:star:` `:heart:` `:fire:` `:rocket:`
- 符号: `:warning:` `:white_check_mark:` `:x:`

**禁用**: 使用 `--no-emoji` 选项

## Mermaid 图表

支持 Mermaid 图表渲染，使用 `--mermaid` 选项启用：

```bash
# 基本 Mermaid 渲染
node scripts/md-pdf-render.mjs docs/diagrams.md diagrams.pdf --mermaid

# Mermaid + 暗色主题
node scripts/md-pdf-render.mjs docs/diagrams.md diagrams-dark.pdf --mermaid --theme vscode

# Mermaid + 横向排版（适合复杂图表）
node scripts/md-pdf-render.mjs docs/diagrams.md diagrams-landscape.pdf --mermaid --landscape
```

支持的 Mermaid 图表类型：
- 流程图 (graph)
- 序列图 (sequenceDiagram)
- 类图 (classDiagram)
- 甘特图 (gantt)
- 状态图 (stateDiagram)
- 饼图 (pie)
- 用户旅程图 (journey)
- 思维导图 (mindmap)
- Git 图 (gitGraph)
- ER 图 (erDiagram)
- 象限图 (quadrantChart)
- XY 图 (xychart-beta)
- 桑基图 (sankey-beta)
- 时间线 (timeline)

## 页眉页脚

自定义页眉页脚内容：

```bash
# 显示标题作为页眉，页码作为页脚
node scripts/md-pdf-render.mjs input.md --header "%title%" --footer "%page% / %total%"

# 只显示页脚页码
node scripts/md-pdf-render.mjs input.md --footer "第 %page% 页"

# 自定义文本
node scripts/md-pdf-render.mjs input.md --header "机密文档" --footer "内部使用"
```

**支持的变量**:

| 变量 | 说明 |
|------|------|
| `%title%` | 文档标题（文件名） |
| `%page%` | 当前页码 |
| `%total%` | 总页数 |

**默认行为**: 不指定时默认显示 `%page% / %total%`

## 分页优化

自动优化分页，避免内容被截断：

- **标题**: 避免在页面底部与内容分离
- **代码块**: 整块不被截断到两页
- **表格**: 整表不被截断
- **列表项**: 整项不被截断
- **Mermaid 图表**: 整图不被截断
- **段落**: 孤行控制（至少 3 行）

## PDF 书签

自动生成 PDF 书签/大纲：

- 从 h1-h6 标题自动生成
- 支持多级嵌套
- 点击书签跳转到对应章节
- 兼容所有 PDF 阅读器

## 自定义样式

创建 CSS 文件覆盖 CSS 变量：

```css
:root {
  --color-fg: #333;
  --color-bg: #fff;
  --color-link: #e63946;
  --color-code-bg: #f5f5f5;
  --color-border: #eee;
  --font-body: "Noto Sans SC", sans-serif;
  --font-code: "JetBrains Mono", monospace;
}
```

通过 `--css your-style.css` 加载。

## 批量转换

```bash
# 转换目录下所有 .md 文件
for f in docs/*.md; do
  node scripts/md-pdf-render.mjs "$f" "output/$(basename "${f%.md}.pdf")"
done
```

## 依赖

| 包 | 用途 |
|----|------|
| [markdown-it](https://github.com/markdown-it/markdown-it) | Markdown 解析（GFM 兼容） |
| [markdown-it-anchor](https://github.com/valeriangalliat/markdown-it-anchor) | 标题锚点（TOC 需要） |
| [markdown-it-task-lists](https://github.com/revin/markdown-it-task-lists) | 任务列表复选框 |
| [markdown-it-emoji](https://github.com/markdown-it/markdown-it-emoji) | Emoji 支持 |
| [markdown-it-texmath](https://github.com/goessner/markdown-it-texmath) | LaTeX 公式解析 |
| [katex](https://katex.org/) | 数学公式渲染 |
| [highlight.js](https://highlightjs.org/) | 代码语法高亮 |
| [mermaid](https://mermaid-js.github.io/mermaid/) | Mermaid 图表渲染（可选） |
| [puppeteer](https://pptr.dev/) | Chromium 无头浏览器渲染 PDF |

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 中文字体缺失 | 安装 Noto Sans SC 或通过 `--css` 指定字体 |
| 代码块被截断 | 增加 `--margin` 或使用 `--landscape`（已自动优化） |
| 图片未加载 | 确保图片使用相对路径或本地绝对路径 |
| PDF 空白 | 检查 Puppeteer/Chromium 是否安装成功 |
| 表格溢出 | 使用 `--landscape` 或自定义 CSS 缩小字号 |
| Mermaid 图表不显示 | 使用 `--mermaid` 选项启用 Mermaid 渲染 |
| Mermaid 渲染错误 | 检查 Mermaid 语法是否正确，参考 [Mermaid 文档](https://mermaid-js.github.io/mermaid/) |
| 数学公式不显示 | 确保使用 `$...$` 或 `$$...$$` 语法，不要用 `--no-math` |
| Emoji 不显示 | 不要使用 `--no-emoji` 选项 |
| 页眉页脚不显示 | 检查是否正确使用 `--header` 和 `--footer` 选项 |

## 许可证

MIT

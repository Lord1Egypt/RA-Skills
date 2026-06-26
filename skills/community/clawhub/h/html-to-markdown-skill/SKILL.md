---
name: html-to-markdown
description: 将 HTML 内容转换为 Markdown 格式，支持字符串、文件和 URL 转换
version: 1.0.0
author: Ping Si <sipingme@gmail.com>
type: npm-package
requires:
  - npm: "@siping/html-to-markdown-node@^1.0.1"
  - node: ">=18.0.0"
tags:
  - html
  - markdown
  - converter
  - utility
repository: https://github.com/sipingme/html-to-markdown-skill
npmPackage: https://www.npmjs.com/package/@siping/html-to-markdown-node
---

# HTML to Markdown Skill

将 HTML 内容转换为 Markdown 格式的 ClawHub Skill。

## 🏗️ 架构说明

本 Skill 是一个 npm 包集成配置，实际功能由 [@siping/html-to-markdown-node](https://www.npmjs.com/package/@siping/html-to-markdown-node) npm 包提供。

```
OpenClaw/AI Agent
    ↓ (读取 Skill 配置)
html-to-markdown-skill
    ↓ (调用 npm 包)
@siping/html-to-markdown-node
    ↓ (转换 HTML)
Markdown 输出
```

## 🎯 何时使用此 Skill

当用户需要将 HTML 内容转换为 Markdown 格式时，AI 会自动调用相应的命令：

### HTML 字符串转换
- 将 HTML 代码片段转换为 Markdown
- 处理富文本编辑器内容
- 转换邮件 HTML 内容

### HTML 文件转换
- 批量转换 HTML 文件
- 将网页保存为 Markdown
- 文档格式迁移

### URL 内容抓取
- 抓取网页并转换为 Markdown
- 提取特定区域内容（CSS 选择器）
- 保存网页文章为 Markdown

**触发关键词**：
- "转换 HTML 为 Markdown"、"HTML 转 Markdown"
- "抓取网页内容"、"保存网页为 Markdown"
- "转换 HTML 文件"、"批量转换 HTML"

## 📋 前置要求

### 1. 安装依赖

```bash
# 安装 npm 包
npm install -g @siping/html-to-markdown-node

# 或在项目中安装
npm install @siping/html-to-markdown-node
```

### 2. 安装 Skill 文档

```bash
# 克隆 Skill 配置和文档
git clone https://github.com/sipingme/html-to-markdown-skill.git
cp -r html-to-markdown-skill ~/.openclaw/skills/html-to-markdown/
```

## 🚀 标准操作流程 (SOP)

### 操作 1：转换 HTML 字符串

**场景**：用户提供 HTML 代码片段，需要转换为 Markdown

**命令**：`convert`

**步骤**：

1. 接收用户提供的 HTML 内容
2. 可选：询问是否需要指定 domain（用于解析相对 URL）
3. 调用转换命令

**示例**：

```bash
html2md convert \
  --html '<strong>Bold Text</strong>' \
  --domain 'https://example.com'
```

**输出示例**：
```json
{
  "success": true,
  "markdown": "**Bold Text**",
  "length": 13
}
```

**异常处理**：
- HTML 为空：提示用户提供内容
- 转换失败：显示错误信息

---

### 操作 2：转换 HTML 文件

**场景**：用户有 HTML 文件需要转换为 Markdown 文件

**命令**：`convert-file`

**步骤**：

1. 确认输入文件路径
2. 询问输出文件路径（可选，默认输出到控制台）
3. 可选：询问是否需要指定 domain
4. 执行转换

**示例**：

```bash
html2md convert-file \
  --input /path/to/input.html \
  --output /path/to/output.md \
  --domain 'https://example.com'
```

**输出示例**：
```json
{
  "success": true,
  "message": "转换成功: /path/to/output.md",
  "inputFile": "/path/to/input.html",
  "outputFile": "/path/to/output.md",
  "length": 1234
}
```

**异常处理**：
- 文件不存在：提示用户检查路径
- 无写入权限：提示权限问题
- 转换失败：显示错误信息

---

### 操作 3：抓取 URL 并转换

**场景**：用户想抓取网页内容并转换为 Markdown

**命令**：`convert-url`

**步骤**：

1. 确认目标 URL
2. 可选：询问是否需要使用 CSS 选择器提取特定内容
3. 执行抓取和转换

**示例**：

```bash
# 转换整个页面
html2md convert-url \
  --url 'https://example.com/article'

# 只提取特定区域
html2md convert-url \
  --url 'https://example.com/article' \
  --selector 'article.content'
```

**输出示例**：
```json
{
  "success": true,
  "markdown": "# Article Title\n\nContent...",
  "url": "https://example.com/article",
  "length": 5678
}
```

**异常处理**：
- URL 无法访问：提示网络错误
- 选择器未找到：提示选择器错误
- 转换失败：显示错误信息

---

## 📊 输入输出规范

### 命令行输出格式

所有命令统一使用 JSON 格式输出：

**成功响应**：
```json
{
  "success": true,
  "markdown": "转换后的 Markdown 内容",
  "length": 1234
}
```

**错误响应**：
```json
{
  "success": false,
  "error": "错误信息"
}
```

### 转换选项

#### domain（可选）
- **类型**：字符串
- **说明**：用于解析相对 URL 为绝对 URL
- **示例**：`https://example.com`

#### escapeMode（可选）
- **类型**：字符串
- **可选值**：`smart`（默认）、`disabled`
- **说明**：
  - `smart`：智能转义特殊字符
  - `disabled`：禁用转义

#### selector（仅 URL 转换）
- **类型**：字符串
- **说明**：CSS 选择器，用于提取页面特定区域
- **示例**：`article.content`、`#main`、`.post-body`

---

## 🎓 示例对话

### 示例 1：转换 HTML 字符串

**用户**：帮我把这段 HTML 转换为 Markdown：`<h1>Title</h1><p>Content</p>`

**AI**：好的，我来帮你转换。

[执行命令]
```bash
html2md convert --html '<h1>Title</h1><p>Content</p>'
```

**AI**：✅ 转换完成！

```markdown
# Title

Content
```

---

### 示例 2：抓取网页

**用户**：帮我把这个网页保存为 Markdown：https://example.com/blog/post

**AI**：好的，我来抓取并转换这个网页。

[执行命令]
```bash
html2md convert-url --url 'https://example.com/blog/post'
```

**AI**：✅ 网页已转换为 Markdown！

---

### 示例 3：批量转换文件

**用户**：把 docs 文件夹下的所有 HTML 文件转换为 Markdown

**AI**：好的，我来批量转换。

[执行命令]
```bash
for file in docs/*.html; do
  html2md convert-file \
    --input "$file" \
    --output "${file%.html}.md"
done
```

**AI**：✅ 已转换 5 个文件！

---

## ⚠️ 常见问题和解决方案

### 问题 1：相对 URL 未正确转换

**症状**：图片或链接显示为相对路径

**解决**：
```bash
html2md convert --html '...' --domain 'https://example.com'
```

### 问题 2：特殊字符被过度转义

**症状**：输出的 Markdown 中有很多反斜杠

**解决**：
```bash
html2md convert --html '...' --escape-mode disabled
```

### 问题 3：网页抓取失败

**症状**：提示"Failed to fetch URL"

**原因**：
- 网络连接问题
- URL 需要认证
- 防爬虫限制

**解决**：
- 检查网络连接
- 手动下载 HTML 后使用 `convert-file`

### 问题 4：选择器未找到内容

**症状**：提示"Selector not found"

**解决**：
- 在浏览器中检查选择器是否正确
- 使用更通用的选择器
- 不使用选择器，转换整个页面

---

## 🔧 支持的 HTML 元素

### 文本格式
- **粗体**：`<strong>`, `<b>` → `**text**`
- **斜体**：`<em>`, `<i>` → `*text*`
- **删除线**：`<del>`, `<s>` → `~~text~~`
- **代码**：`<code>` → `` `code` ``

### 标题
- `<h1>` → `# Heading 1`
- `<h2>` → `## Heading 2`
- `<h3>` → `### Heading 3`
- `<h4>` → `#### Heading 4`
- `<h5>` → `##### Heading 5`
- `<h6>` → `###### Heading 6`

### 列表
- **无序列表**：`<ul>`, `<li>` → `- item`
- **有序列表**：`<ol>`, `<li>` → `1. item`
- **嵌套列表**：支持多层嵌套

### 链接和图片
- **链接**：`<a href="url">text</a>` → `[text](url)`
- **图片**：`<img src="url" alt="text">` → `![text](url)`

### 引用和代码块
- **引用**：`<blockquote>` → `> quote`
- **代码块**：`<pre><code>` → ` ```code``` `

### 表格
- `<table>`, `<tr>`, `<td>`, `<th>` → Markdown 表格

### 其他
- **水平线**：`<hr>` → `---`
- **换行**：`<br>` → 换行

---

## 📚 参考资料

- [项目 GitHub](https://github.com/sipingme/html-to-markdown-skill)
- [npm 包](https://www.npmjs.com/package/@siping/html-to-markdown-node)
- [快速开始指南](./references/quick-start.md)
- [API 文档](./references/api.md)

---

## 📝 维护说明

- **版本**: 1.0.0
- **最后更新**: 2026-03-22
- **维护者**: Ping Si <sipingme@gmail.com>
- **许可证**: MIT

---

## ✅ 首次成功检查清单

新用户应该能在 2 分钟内完成：

- [ ] 安装包：`npm install -g @siping/html-to-markdown-node`
- [ ] 检查安装：`html2md --version`
- [ ] 测试转换：`html2md convert --html '<strong>Test</strong>'`
- [ ] 看到输出：`**Test**`

如果以上步骤都能顺利完成，说明 Skill 已正确配置！

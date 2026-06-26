# API 文档

## 命令行接口

### convert

转换 HTML 字符串为 Markdown。

**语法**：
```bash
bash scripts/convert.sh convert --html <html> [--domain <domain>] [--escape-mode <mode>]
```

**参数**：
- `--html` (必需): HTML 内容
- `--domain` (可选): 基础域名，用于解析相对 URL
- `--escape-mode` (可选): 转义模式，`smart` 或 `disabled`，默认 `smart`

**示例**：
```bash
bash scripts/convert.sh convert --html '<strong>Bold</strong>'
```

**输出**：
```json
{
  "success": true,
  "markdown": "**Bold**",
  "length": 8
}
```

---

### convert-file

转换 HTML 文件为 Markdown 文件。

**语法**：
```bash
bash scripts/convert.sh convert-file --input <file> [--output <file>] [--domain <domain>]
```

**参数**：
- `--input` (必需): 输入 HTML 文件路径
- `--output` (可选): 输出 Markdown 文件路径
- `--domain` (可选): 基础域名

**示例**：
```bash
bash scripts/convert.sh convert-file \
  --input input.html \
  --output output.md
```

**输出**：
```json
{
  "success": true,
  "message": "Converted successfully: output.md",
  "inputFile": "input.html",
  "outputFile": "output.md",
  "length": 1234
}
```

---

### convert-url

抓取 URL 并转换为 Markdown。

**语法**：
```bash
bash scripts/convert.sh convert-url --url <url> [--selector <selector>]
```

**参数**：
- `--url` (必需): 要抓取的 URL
- `--selector` (可选): CSS 选择器，用于提取特定内容

**示例**：
```bash
bash scripts/convert.sh convert-url \
  --url 'https://example.com/article' \
  --selector 'article.content'
```

**输出**：
```json
{
  "success": true,
  "markdown": "# Article Title\n\nContent...",
  "url": "https://example.com/article",
  "length": 5678
}
```

---

## 错误处理

所有命令在失败时返回以下格式：

```json
{
  "success": false,
  "error": "错误描述"
}
```

常见错误：
- `HTML content is required`: 未提供 HTML 内容
- `Input file is required`: 未提供输入文件
- `File not found: <path>`: 文件不存在
- `URL is required`: 未提供 URL
- `Failed to fetch URL: <code>`: URL 抓取失败
- `Selector not found: <selector>`: CSS 选择器未找到

---

## Node.js API

如果你想在 Node.js 代码中使用：

```javascript
const { convertString } = require('@siping/html-to-markdown-node');

const html = '<h1>Title</h1><p>Content</p>';
const markdown = convertString(html, {
  domain: 'https://example.com',
  escapeMode: 'smart'
});

console.log(markdown);
// # Title
//
// Content
```

详细 API 文档请参考：
https://www.npmjs.com/package/@siping/html-to-markdown-node

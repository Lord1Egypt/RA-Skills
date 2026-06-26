# 快速开始指南

## 安装

### 1. 安装 npm 包

```bash
npm install -g @siping/html-to-markdown-node
```

### 2. 克隆 Skill 配置

```bash
git clone https://github.com/sipingme/html-to-markdown-skill.git
cd html-to-markdown-skill
npm install
```

## 基本使用

### 转换 HTML 字符串

```bash
bash scripts/convert.sh convert --html '<h1>Hello</h1><p>World</p>'
```

输出：
```json
{
  "success": true,
  "markdown": "# Hello\n\nWorld",
  "length": 13
}
```

### 转换 HTML 文件

```bash
bash scripts/convert.sh convert-file \
  --input example.html \
  --output example.md
```

### 抓取网页

```bash
bash scripts/convert.sh convert-url \
  --url 'https://example.com'
```

## 高级选项

### 指定域名（解析相对 URL）

```bash
bash scripts/convert.sh convert \
  --html '<img src="/logo.png">' \
  --domain 'https://example.com'
```

输出：`![](https://example.com/logo.png)`

### 使用 CSS 选择器

```bash
bash scripts/convert.sh convert-url \
  --url 'https://example.com/article' \
  --selector 'article.content'
```

## 在 ClawHub 中使用

安装 Skill 后，AI 会自动识别以下场景：

- "把这段 HTML 转换为 Markdown"
- "抓取这个网页并保存为 Markdown"
- "转换 HTML 文件"

AI 会自动调用相应的命令完成转换。

---
name: "html-publisher"
description: "将 HTML 内容发布为在线网页并返回可访问的 URL。当用户想把 HTML 发布上线、生成分享链接、或需要把网页内容转为公开 URL 时调用。"
---

# HTML 网页发布指南

## 能力说明

通过 `gnomic` CLI 工具，可以将任意 HTML 代码发布为一个在线可访问的网页，并返回公开 URL。适用于：

- 快速分享生成的 HTML 页面
- 将本地 HTML 文件发布上线
- 把 AI 生成的网页内容转为可访问链接

## 使用方式

### 基本命令

**从文件读取（推荐，适用于所有 shell）：**

```bash
gnomic content html2url --file <html文件路径>
```

**直接传入 HTML 字符串（适用于短 HTML）：**

```bash
gnomic content html2url "<h1>Hello World</h1>"
```

### 输出格式

默认返回 JSON（适合 AI Agent 解析）：

```json
{
  "success": true,
  "data": {
    "url": "https://..."
  }
}
```

加 `-f text` 参数返回人类可读格式：

```bash
gnomic content html2url --file index.html -f text
```

输出示例：
```
Published successfully!
URL: https://ts.fyshark.com/html_files/document_xxx.html
```

---

## 操作流程

### 第一步：准备 HTML 内容

获取需要发布的 HTML 内容，可以是：
- 用户提供的 HTML 代码
- AI 生成的完整 HTML 页面
- 读取本地 HTML 文件内容

### 第二步：执行发布命令

**推荐方式：使用 `--file` 选项从文件读取**

这是最可靠的方式，避免 shell 参数分割问题：

```bash
gnomic content html2url --file index.html
```

**备选方式：直接传入 HTML 字符串**

适用于简短的 HTML 片段：

```bash
gnomic content html2url "<h1>Hello World</h1>"
```

> 注意：大段 HTML 字符串在 PowerShell 中可能因空格被分割成多个参数，导致报错。优先使用 `--file` 方式。

### 第三步：获取 URL

从返回的 JSON 中提取 `data.url` 字段，即为可访问的在线网页地址。

---

## 注意事项

- HTML 内容越大，发布耗时越长
- 返回的 URL 为公开链接，任何人均可访问
- 不支持动态后端逻辑，仅支持静态 HTML/CSS/JS
- 如果 HTML 中引用了外部资源（图片、字体等），需确保这些资源本身可公开访问

---

## 补充：命令不可用时

如果执行 `gnomic` 命令时提示找不到命令，说明 `gnomic-cli` 尚未安装，执行以下命令安装：

```bash
npm install -g gnomic-cli
```

`gnomic-cli`开源地址：https://github.com/huyi9531/gnomic_cli
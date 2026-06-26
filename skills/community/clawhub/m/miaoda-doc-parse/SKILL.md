---
name: miaoda-doc-parse
description: "Use when user needs to parse, extract, or read content from documents (PDF, Word, Excel, PPT, etc.) Converts documents to Markdown via IDP (Intelligent Document Parsing). 触发词：文档解析, 解析文档, 解析 PDF, 解析 Word, 解析 Excel, 读取文档, 提取文档内容, doc parse, IDP, 智能文档解析, parse document, 文档转 Markdown, 读取 PDF, 读取 PPT, 提取表格, 文档识别"
---

# Document Parse

通过 `miaoda-studio-cli doc-parse` 将文档解析为 Markdown 格式（基于 IDP 智能文档解析）。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--file` | 文档路径或 URL | 是 | - |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 支持的文档格式

| 格式 | 扩展名 | 典型场景 |
|------|--------|---------|
| PDF | `.pdf` | 报告、论文、合同 |
| Word | `.doc`, `.docx` | 文档、方案 |
| PowerPoint | `.pptx` | 演示文稿 |
| Excel | `.xlsx` | 表格数据 |
| CSV | `.csv` | 结构化数据 |
| 纯文本 | `.txt`, `.md` | 文本文件 |
| 网页 | `.html` | HTML 页面 |

## 使用示例

```bash
# 解析本地 PDF 文件
miaoda-studio-cli doc-parse --file report.pdf

# 解析远程文档并输出 JSON
miaoda-studio-cli doc-parse --file https://example.com/document.docx --output json

# 解析 Excel 表格
miaoda-studio-cli doc-parse --file data.xlsx --output json
```

## 使用场景决策

```
需要获取文档内容
├─ 文档是本地文件或可下载 URL → miaoda-studio-cli doc-parse
├─ 文档是网页（需要抓取）→ miaoda-studio-cli web-crawl（见 miaoda-web-fetch skill）
└─ 文档是飞书云文档 → 使用 feishu skill
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 用 `miaoda-studio-cli doc-parse` 解析网页 URL | 网页内容用 `miaoda-studio-cli web-crawl`（见 miaoda-web-fetch skill） |
| 不检查文件格式是否支持 | 确认文件扩展名在支持列表中 |
| 需要结构化数据但未加 `--output json` | 需要程序处理时加 `--output json` |
| 文件路径包含空格未加引号 | 路径有空格时用引号包裹：`--file "my file.pdf"` |
| 解析飞书云文档用 doc-parse | 飞书云文档使用 `feishu` skill 通过 API 读取 |

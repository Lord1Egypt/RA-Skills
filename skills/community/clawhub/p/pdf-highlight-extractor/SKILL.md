---
name: pdf-highlight-extractor
description: |
  识别用户发来的 PDF 文档中的高亮标注内容（荧光笔标记），提取所有高亮文字，
  汇总后生成一个带 YAML Front Matter（title、date、tags 三件套）的 Markdown 文件。
  title 和 tags 由 AI 根据内容语义自动生成；Markdown 包含「摘录原文」和「内容总结」两部分。
  输出文件保存在与 PDF 相同的目录下，文件名为 <pdf名>_highlights.md。
  当用户发来 PDF 并提到「提取高亮」「整理标注」「读取标记」「生成读书笔记」等意图时使用此技能。
agent_created: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# PDF 高亮提取 → Markdown 技能

## 目标

从用户提供的 PDF 文件中提取所有高亮（荧光笔）标注文字，汇总后生成带 YAML Front Matter 的 Markdown 文档。

## 工作流程

### Step 1：确认依赖

首次使用时，先运行安装脚本确保 `pymupdf` 已安装：

```bash
<python> scripts/install_deps.py
```

其中 `<python>` 替换为当前环境的 Python 路径（优先使用 managed 版本）。

### Step 2：提取高亮（JSON 模式）

用 JSON 模式运行提取脚本，获得结构化的高亮数据供后续 AI 处理：

```bash
<python> scripts/extract_highlights.py "<pdf_path>" --json
```

- `<pdf_path>`：用户提供的 PDF 绝对路径
- 脚本输出 JSON，包含每条高亮的 `page`（页码）、`color`（颜色名）、`text`（内容）
- 如果用户只想提取特定颜色，加 `--color yellow`（支持 yellow/green/red/blue/pink/orange/purple/cyan）

### Step 3：AI 生成标题和 Tags

分析所有高亮文本的语义，生成：

- **title**：3~10 字，概括高亮内容的核心主题，中文优先
- **tags**：3~6 个标签，涵盖主题领域、文档类型、关键概念，全部小写，用中文或英文均可

### Step 4：生成 Markdown 文件

按以下模板在 **PDF 同目录**生成 `<pdf文件名>_highlights.md`：

```markdown
---
title: "<AI生成的标题>"
date: <今日日期 YYYY-MM-DD>
tags:
  - <tag1>
  - <tag2>
  - ...
---

# <标题>

## 摘录原文

### 第 N 页

- 高亮内容1
- 高亮内容2

### 第 M 页

- ...

---

## 内容总结

<AI 根据所有高亮内容撰写的 200~400 字综合总结，提炼核心观点、关键数据和重要结论>
```

### Step 5：输出确认

告知用户：
- 生成的 Markdown 文件路径
- 共提取了多少条高亮、来自多少页
- 简要展示 YAML Front Matter 内容

## 注意事项

- 若脚本报告「未找到任何高亮标注」，可能是 PDF 使用了图片扫描而非文字型高亮，或高亮格式为手写/非标准注释；此时如实告知用户
- 若 PDF 路径含中文或空格，确保用双引号包裹路径
- 总结部分需真正阅读所有摘录内容后撰写，不能只复述标题

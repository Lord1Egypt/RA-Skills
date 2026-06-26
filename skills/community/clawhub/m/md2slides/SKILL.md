---
name: md-to-slides
description: >
  将 Markdown 格式的演讲/汇报文档转化为可编辑的 PPTX 演示文稿。
  输出标准 .pptx 文件，可在 PowerPoint / Keynote / WPS 中打开编辑。
triggers:
  - "生成PPT"
  - "转成幻灯片"
  - "做成演示文稿"
  - "导出PPTX"
  - "导出PPT"
  - "md to slides"
  - "markdown 转 PPT"
metadata:
  version: "2.0"
  category: presentation
---

# md-to-slides

## 做什么

把用户的 Markdown 演讲/汇报文档转化为可编辑的 .pptx 演示文稿。

## 怎么做

### Step 0：确认输入

向用户确认要转换的 Markdown 文件路径。

### Step 1：扫描结构

读取文件，提取 frontmatter 元数据和所有章节标题，报告给用户确认。

### Step 2：逐章解析

对每个章节生成 Slide 数组。超长章节（>8000 tokens）需要按子标题拆分。主 Agent 只读标题行，正文由子 Agent 解析。

> 子 Agent 解析 Prompt 模板见 `references/analysis-prompt.md`。

### Step 3：合并确认

汇总所有 Slide，检查密度和连贯性，向用户报告分页方案。

### Step 4：生成 Schema

将完整的 PresentationSchema JSON 写入当前工作目录的临时文件。

### Step 5：生成 PPTX

调用生成脚本：
```
node scripts/generate-pptx.cjs <schema.json路径> <输出路径>
```

生成后提取文本核验内容完整性。

## 兜底

- 子 Agent 失败 → 重试一次，仍失败则标记该章需人工处理
- Mermaid 图表 → 输出占位 slide，提示手动插入
- 不篡改用户原文内容
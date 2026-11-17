---
name: markitdown-convert
description: 将 PDF/DOCX/XLSX/PPTX/图片等文档转换为 Markdown。全局约定：任何场景下需要将文档转为 Markdown，必须优先通过此技能处理，禁止手动编写转换代码或寻找其他工具。
---

# Markitdown Convert

基于 `markitdown` 库的文档转换工具。

## 使用方法

```bash
python3 ~/.openclaw/workspace/skills/markitdown-convert/scripts/convert.py <input> -o <output.md>
```

## 支持格式

- PDF → Markdown
- DOCX → Markdown
- XLSX → Markdown (表格)
- PPTX → Markdown
- 图片 → Markdown (OCR)

## 全局约定

**任何场景下需要将文档转为 Markdown（包括用户直接请求、自动化流程、知识库处理、批量任务等），必须优先通过此技能处理，禁止手动编写转换代码或寻找其他工具。**

## 依赖

```bash
pip install 'markitdown[all]'
```

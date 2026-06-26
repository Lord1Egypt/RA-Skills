---
name: PDF Tool
description: Split, merge, watermark, and extract text from PDF files — PyPDF2 based.
---

# PDF Tool（PDF批量处理工具）

> PDF拆分/合并/水印/文本提取 | PyPDF2驱动

## 功能 | Features

- ✅ **合并PDF** — 多个PDF合并为一个
- ✅ **拆分PDF** — 按页数范围拆分
- ✅ **添加水印** — 文字水印保护内容
- ✅ **提取文本** — 提取PDF中的纯文本内容

## 使用场景 | Use Cases

| 模式 | 说明 |
|---|---|
| merge | 多份合同合并为一本 |
| split | 按章节拆分成独立PDF |
| watermark | 添加"机密"水印 |
| extract_text | 提取合同正文内容 |

## 使用方式 | Usage

```
输入参数:
  mode        操作模式: split / merge / watermark / extract_text
  files       文件路径列表（merge/split用）
  output      输出文件路径
  watermark   水印文字（watermark模式用）

输出:
  success     是否成功
  text/msg    结果信息
```

## 示例 | Example

```python
# 合并
result = pdf_tool(mode="merge", files=["a.pdf", "b.pdf"], output="merged.pdf")

# 提取文本
result = pdf_tool(mode="extract_text", files=["contract.pdf"])
print(result["text"][:500])
```

## 依赖 | Dependencies

```
PyPDF2 >= 3.0.0
```

*版本 v1.0*

---
name: pdf-literature-parser
description: 从学术论文 PDF 中提取元信息，包含标题、关键词、摘要，输出结构化 JSON。适用于文献整理、引用格式整理、论文信息快速提取。
command: python extract_title_keywords_abstract.py "{{pdf_path}}"
inputs:
  - name: pdf_path
    type: string
    required: true
    description: 待解析的论文 PDF 文件路径（绝对路径或相对路径）
output:
  type: json
  schema:
    title_apa: string
    keywords: array
    abstract: string
---

# APA 论文元信息提取工具

## 功能说明
从学术论文 PDF 文件中自动提取三类核心信息：
1. 论文标题
2. 关键词列表
3. 英文/中文摘要内容

输出为标准 JSON，可直接用于文献管理、引用生成、数据分析。

## 依赖安装
使用前请安装依赖库：
```bash
pip install pymupdf titlecase openai

## 使用方式
### 命令行调用
```bash
python extract_title_keywords_abstract.py <论文PDF路径>
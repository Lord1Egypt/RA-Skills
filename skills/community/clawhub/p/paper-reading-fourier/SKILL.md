---
name: paper-reading
description: Read academic papers from local PDF files, arXiv URLs, or paper titles and generate structured reading notes in Chinese. Use when the user provides a PDF file path, an arXiv URL, a paper title, or asks to read/summarize/analyze a research paper. Supports automatic arXiv title search, PDF download, text extraction, and standardized note generation following a consistent template format.
---

# Paper Reading

Read a paper and produce structured notes following the standard template.

## User Input Required

Before starting, the user must provide:

1. **论文信息**: 本地 PDF 路径、arXiv URL 或论文标题（三选一）
2. **PDF 存储路径**: 下载/保存 PDF 的绝对路径（如 `/tmp/paper.pdf`）
3. **笔记输出路径**: 最终生成的笔记文件的绝对路径（如 `/Users/xxx/notes/Paper Title.md`）

## Workflow

### 1. Fetch the PDF

Given a local path, arXiv URL, or paper title from the user:

```bash
python scripts/fetch_pdf.py <path_or_url_or_title> -o <pdf_output_path>
```

- **Local path**: validates existence, returns absolute path
- **arXiv URL**: downloads PDF (supports both `/abs/` and `/pdf/` URL formats)
- **Paper title**: searches arXiv API by title, downloads the most relevant result
- `-o` 参数指定 PDF 存储的绝对路径（由用户提供）
- Prints the fetched PDF path to stdout

### 2. Extract PDF Content

```bash
pip install pdfplumber  # if not already installed
python scripts/read_pdf.py <pdf_path> [-p <page_range>] [-o <extracted_text_path>]
```

- Extracts text and tables from the PDF
- Optionally specify page range (e.g. `-p 1-10` or `-p 3`)
- `-o` 可选，指定提取文本的输出路径；不指定则输出到 stdout
- Outputs markdown-formatted text

### 3. Read and Analyze

Read the extracted text. For papers with complex layouts (columns, figures, equations), supplement extraction with direct PDF reading using the pdf tool if available, or ask the user to clarify specific sections.

### 4. Generate Notes

Produce notes following the standard template.

#### Note Structure (summary)

```
# 一、基本信息
1.paper：《标题》
2.github：链接或未知
3.会议：会议名或未知

# 二、文章理解
## 1. 研究背景与动机 (Motivation)
## 2. 核心问题 (Problem Statement)
## 3. 解决方法 (Methodology)
## 4. 实验结果 (Experiments)
```

#### Key Requirements

- Language: Chinese with English technical terms preserved
- Formulas: LaTeX format (`$...$` inline, `$$...$$` block)
- Images: preserve original image URLs with `![](url)` format
- Key concepts: bold with `**...**`
- Deep dives / proofs / interview-level knowledge: wrap in `:::info` blocks
- PyTorch code: use python code blocks
- Strict 4-level heading hierarchy: `# → ## → ### → ####`
- Numerical results: use specific numbers to show improvements

### 5. Save Notes

Save the generated notes to the path specified by the user (e.g. `/Users/xxx/notes/Paper Title.md`).

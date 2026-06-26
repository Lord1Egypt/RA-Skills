---
name: pandoc-rs
description: A powerful document conversion tool supporting Html, Markdown, Docx, PDF, and LaTeX formats. Provides bidirectional conversion between these formats using a WebAssembly-based engine similar to Pandoc.
---

# Pandoc Rs

A WebAssembly-based document conversion tool that converts between Html, Markdown, Docx, PDF, and LaTeX formats.

## Trigger when

The user asks to convert documents between Html, Markdown, Docx, PDF, or LaTeX formats. Examples: "convert this markdown to PDF", "export as Word document", "transform HTML to LaTeX", "change docx to markdown".

中文触发条件：请求在 Html、Markdown、Docx、PDF、LaTeX 格式之间转换文档时触发。示例：「把 Markdown 转 PDF」、「导出为 Word 文档」、「HTML 转 LaTeX」、「docx 转 markdown」。

## Quick Start

1. Download the WASM file using `wasm-sandbox-download` or let it cache automatically
2. Use `wasm-sandbox-run` with `--work-dir` parameter to specify the directory containing input files (or current working directory)
3. Execute conversion, stats, or validation commands

**⚠️ Important:** Always use `--work-dir <directory>` with `wasm-sandbox-run` to grant filesystem access.

## Supported Conversions

- Markdown ↔ Html
- Markdown ↔ Docx
- Markdown ↔ LaTeX
- Html ↔ LaTeX
- Docx → Html
- Docx → Markdown

## Resources

For detailed usage instructions and examples, see [USAGE.md](references/USAGE.md).

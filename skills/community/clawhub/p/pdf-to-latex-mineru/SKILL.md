---
name: pdf-to-latex-mineru
description: >
  Convert PDF documents to LaTeX source code using MinerU AI extraction.
  Designed for researchers, academics, and scientists who need to re-edit,
  re-typeset, or recover LaTeX markup from published papers, theses, and
  technical reports.

  Use when asked to: convert a PDF paper to LaTeX, extract LaTeX from an
  academic PDF, edit a PDF in LaTeX, re-typeset an arXiv paper, recover LaTeX
  source from PDF, turn a document into editable LaTeX, get equations out of
  a PDF, extract math formulas from document, convert research paper to LaTeX.

  Handles complex academic layouts: mathematical equations, multi-column text,
  tables, figures, and scientific notation. Supports local PDF files and direct
  URLs including arXiv links. Use --model vlm for high-accuracy extraction of
  math-heavy or multi-column documents; use pipeline mode for guaranteed
  structural fidelity.

  Solves problems like: I have a PDF but need the LaTeX source, I need to
  modify a paper but only have the PDF, I want to reuse equations from a
  published paper, how do I make a scanned paper editable in LaTeX.

  Powered by MinerU from OpenDataLab (Shanghai AI Lab) - open-source,
  high-quality PDF understanding engine. Requires MINERU_TOKEN.

  将PDF学术论文转换为LaTeX源码。支持公式提取、多栏排版识别、表格还原，
  适用于论文重排版、学术编辑、arXiv论文转换等场景。
homepage: https://mineru.net
license: MIT-0
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["mineru-open-api"],"env":["MINERU_TOKEN"]},"primaryEnv":"MINERU_TOKEN","install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
---

# PDF to LaTeX

Convert PDF documents to LaTeX format using MinerU. Best suited for academic papers and documents with formulas or complex layouts.

## Install

```bash
npm install -g mineru-open-api
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
mineru-open-api extract paper.pdf -f latex -o ./out/
mineru-open-api extract paper.pdf -f latex --model vlm -o ./out/
mineru-open-api extract https://arxiv.org/pdf/2309.10918 -f latex -o ./out/
```

## Authentication

Token required:

```bash
mineru-open-api auth
export MINERU_TOKEN="your-token"
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supported input: .pdf (local file or URL)
- Output format: LaTeX (`-f latex`)
- LaTeX output requires `extract` with token
- Use `--model vlm` for papers with complex math, tables, or multi-column layouts
- Language hint with `--language` (default: `ch`, use `en` for English)

## Notes

- LaTeX output is only available via `extract` with token
- `--model vlm` gives higher accuracy; use `pipeline` for guaranteed fidelity
- Output goes to stdout by default; use `-o <dir>` to save to a file
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
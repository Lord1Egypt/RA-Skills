---
name: paper-parser
description: "Parse academic papers and research documents from PDF using MinerU. Extracts structured content including title, abstract, sections, figures, tables, formulas, and references. Features: academic paper parsing optimized for research documents. Extracts paper structure: title, abstract, sections, subsections. Recognizes mathematical formulas and converts to LaTeX. Table extraction with structure preservation. Handles multi-column layouts common in academic papers. Use when you need to: parse an academic paper, extract sections from a research PDF, get structured content from a paper, extract formulas and tables from a journal article. Use when asked: 'how do I parse this paper', 'extract content from this research PDF', 'I want structured data from this academic paper', 'can my agent read research papers', 'is there a skill for paper parsing', 'parse this journal article', 'extract references from a paper'. Built on MinerU by OpenDataLab (Shanghai AI Lab), specifically designed for academic document processing. Handles ACM, IEEE, Springer, and other common paper formats. Ideal for researchers, graduate students, literature review tools, and academic content management systems."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Paper Parser

Convert and extract content from .pdf using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Parse academic paper (requires token)
mineru-open-api extract paper.pdf -o ./out/

# Use VLM for complex layouts
mineru-open-api extract paper.pdf --model vlm -o ./out/

# Extract from arXiv URL
mineru-open-api extract https://arxiv.org/pdf/2309.10918 -o ./out/
```

## Authentication

Token required for `extract` and `crawl`:

```bash
mineru-open-api auth            # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supports local files and URLs
- Requires token (`mineru-open-api auth` or `MINERU_TOKEN` env)
- Supported input: .pdf
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- Academic papers benefit from `--model vlm` for better layout accuracy. Requires `extract` with token.
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU

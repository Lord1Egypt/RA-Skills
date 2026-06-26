---
name: pdf-to-docx
description: "Convert PDF documents to Word (.docx) format using MinerU. Transforms PDF files into editable Word documents preserving layout, text, tables, and formatting. Features: PDF to DOCX conversion with layout preservation. Handles text, tables, images, and formatting. OCR mode for scanned PDFs. VLM mode for complex layouts. Page range selection for large documents. Use when you need to: convert a PDF to Word, turn a PDF into an editable document, make a PDF editable in Word, transform PDF to .docx. Use when asked: 'how do I convert PDF to Word', 'turn this PDF into docx', 'I want to edit this PDF in Word', 'can my agent convert PDF to Word', 'is there a skill for PDF to DOCX conversion', 'make this PDF editable'. Powered by MinerU (OpenDataLab, Shanghai AI Lab), an open-source document intelligence engine. Works with local files and URLs. Ideal for offices, legal teams, and anyone who receives PDF documents but needs to edit them in Microsoft Word."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# PDF to DOCX

Convert PDF files to editable Word (.docx) format using MinerU.

> ⚠️ **Token required.** `flash-extract` does not support DOCX output. You must configure a token via `mineru-open-api auth` before using this skill.
>
> ⚠️ **Output to file required.** DOCX is a binary format and cannot be streamed to stdout — you must always specify `-o <directory>`.

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Authentication

Token required — create one at https://mineru.net/apiManage/token:

```bash
mineru-open-api auth             # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

## Quick Start

```bash
# Convert PDF to DOCX (token required, -o is mandatory)
mineru-open-api extract report.pdf -f docx -o ./out/

# From URL
mineru-open-api extract https://example.com/report.pdf -f docx -o ./out/

# With language hint
mineru-open-api extract report.pdf -f docx --language en -o ./out/

# With VLM model for better layout accuracy (complex PDFs)
mineru-open-api extract report.pdf -f docx --model vlm -o ./out/

# Batch convert multiple PDFs
mineru-open-api extract *.pdf -f docx -o ./out/
```

## Capabilities

- Supported input: .pdf (local file or URL)
- Output format: Word (.docx) via `-f docx`
- Token required (`mineru-open-api auth` or `MINERU_TOKEN` env)
- `-o <dir>` is mandatory — DOCX cannot stream to stdout
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (e.g. `1-10`)
- Batch mode supported: `extract *.pdf -f docx -o ./out/`

## Notes

- `flash-extract` does NOT support DOCX output — always use `extract` with token
- DOCX output cannot be streamed to stdout; `-o` flag is required
- Use `--model vlm` for PDFs with complex layouts, tables, or mixed content
- Use `--model pipeline` if you need guaranteed fidelity with no hallucination risk
- Output directory will be created if it does not exist
- All progress/status messages go to stderr
- MinerU is open-source by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU

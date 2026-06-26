---
name: pdf-miner
description: >-
  Extract text and tables from PDF files with robust support for global market data
  formats (currencies, percentages, units). Use when: (1) User asks to read/extract
  content from a PDF file, (2) User needs text or tables from industry reports,
  research papers, or financial documents, (3) web_fetch or scrapling fail on a PDF.
  Supports: keyword search, metrics extraction, table of contents detection, PDF
  diff/comparison, LLM chunk splitting, batch processing, header/footer cleaning.
  NOT for: OCR on scanned image-based PDFs, editing/merging PDFs, or creating new PDFs.
---

# PDF Miner Skill

Extract text and tables from PDF files using `pdfplumber` (global market formats).

## Prerequisites

```bash
python -m pip install pdfplumber
```

For OCR capabilities (scanned/image PDFs), also install:

```bash
python -m pip install pymupdf openai
```

## Initial Setup for OCR

Before using `--ocr`, you must provide a vision API credential. There are three ways:

1. **Environment variables** (recommended for temporary use):

   ```bash
   export OCR_API_KEY="your-openrouter-api-key"
   export OCR_MODEL="qwen/qwen3.6-plus:free"   # optional
   export OCR_BASE_URL="https://openrouter.ai/api/v1"   # optional
   ```

2. **Config file** (persistent, skill-specific):  
   Create `skills/skills/pdf-miner/config.json` with:

   ```json
   {
     "vision_api_key": "your-openrouter-api-key",
     "vision_model": "qwen/qwen3.6-plus:free",
     "vision_base_url": "https://openrouter.ai/api/v1"
   }
   ```

3. **Command-line arguments** (override per invocation):

   ```bash
   python scripts/extract_pdf.py scanned.pdf --ocr --ocr-api-key "sk-..." --ocr-model "stepfun/step-3.5-flash:free"
   ```

## Usage

Run commands from this skill directory.

### Basic Extraction

```bash
# Full extraction (text + tables)
python scripts/extract_pdf.py input.pdf

# Output to custom path
python scripts/extract_pdf.py input.pdf output.md

# Specific pages
python scripts/extract_pdf.py input.pdf --pages 1-5,10,15-20

# Text or tables only
python scripts/extract_pdf.py input.pdf --text-only
python scripts/extract_pdf.py input.pdf --tables-only
python scripts/extract_pdf.py input.pdf --tables-only --json
```

### Advanced Modes

```bash
# Search: find pages containing keywords with context
python scripts/extract_pdf.py report.pdf --search "Vietnam export penetration"

# Metrics: extract lines with keywords + numeric values
python scripts/extract_pdf.py report.pdf --metrics "market size growth export penetration"

# TOC: extract table of contents / chapter structure (robust, multi-format)
python scripts/extract_pdf.py report.pdf --toc
# Optionally adjust sensitivity (default: 3 entries per page required)
python scripts/extract_pdf.py report.pdf --toc --toc-min-entries 2

# Diff: compare two PDFs, show pages unique to each
python scripts/extract_pdf.py old_version.pdf new_version.pdf --diff

# Chunk: split output into LLM-friendly chunks
python scripts/extract_pdf.py report.pdf --chunk             # single file, 8000 chars each
python scripts/extract_pdf.py report.pdf --chunk --max-chars 4000
python scripts/extract_pdf.py report.pdf --chunk --output-dir ./chunks   # separate files

# Clean headers/footers
python scripts/extract_pdf.py report.pdf --clean-headers

# Batch: process multiple PDFs
python scripts/extract_pdf.py file1.pdf file2.pdf file3.pdf --output-dir ./extracted
```

### OCR for Scanned/Image PDFs (Automatic by Default)

OCR is automatically triggered for pages with very little extractable text (default threshold: 100 characters). This helps handle scanned or image-based PDFs without requiring the `--ocr` flag.

#### Usage Examples

```bash
# Automatic OCR (default behavior)
python scripts/extract_pdf.py scanned.pdf

# Force OCR on all pages (ignore text length)
python scripts/extract_pdf.py scanned.pdf --ocr

# Force OCR only on specific pages
python scripts/extract_pdf.py scanned.pdf --ocr --ocr-pages 1-5,10

# Adjust OCR quality (DPI)
python scripts/extract_pdf.py scanned.pdf --ocr --ocr-dpi 300

# Use a different vision model
python scripts/extract_pdf.py scanned.pdf --ocr --ocr-model "stepfun/step-3.5-flash:free"

# Disable automatic OCR detection (if you want pure extraction only)
python scripts/extract_pdf.py file.pdf --no-auto-ocr

# Change the low-text threshold (default 100 chars)
python scripts/extract_pdf.py file.pdf --ocr-threshold 200
```

#### Configuration

OCR requires a vision API key. See [Initial Setup for OCR](#initial-setup-for-ocr).

| Option | Default | Description |
|--------|---------|-------------|
| `--ocr` | off | Force OCR on pages (with auto-detect or `--ocr-pages`) |
| `--auto-ocr` | on | Automatically OCR low-text pages (hidden; use `--no-auto-ocr` to disable) |
| `--no-auto-ocr` | - | Disable automatic OCR detection |
| `--ocr-pages` | - | Comma-separated pages/ranges to OCR (requires `--ocr`) |
| `--ocr-threshold` | 100 | Minimum text length to consider a page as "sufficient" (characters) |
| `--ocr-dpi` | 200 | Image DPI for OCR rendering |
| `--ocr-api-key` | from env/config | Override API key |
| `--ocr-base-url` | from env/config | Override API base URL |
| `--ocr-model` | from env/config | Override vision model |

#### Troubleshooting

**OCR failed with "No API key"**  
→ Configure your API key in `config.json` or via `OCR_API_KEY` env var.

**OCR model rejects images**  
→ The configured model might not support vision. Choose a vision-capable model (e.g., `qwen/qwen3.6-plus:free`, `stepfun/step-3.5-flash:free`). The script will attempt to auto-fallback to a known good model if the configured one lacks vision support.

**Too many pages being OCR'd**  
→ Increase the threshold: `--ocr-threshold 300` or `--no-auto-ocr` and selectively use `--ocr-pages`.

**Rate limit errors**  
→ Reduce concurrent OCR calls, switch to a paid model tier, or try a different provider.

## Configuration Reference

| Option | Default | Source |
|--------|---------|--------|
| `OCR_API_KEY` | (none) | env `OCR_API_KEY` or `config.json` `vision_api_key` |
| `OCR_MODEL` | `qwen/qwen3.6-plus:free` | env `OCR_MODEL` or `config.json` `vision_model` |
| `OCR_BASE_URL` | `https://openrouter.ai/api/v1` | env `OCR_BASE_URL` or `config.json` `vision_base_url` |

Precedence: CLI argument > environment variable > `config.json` > hardcoded default.

## Tool Comparison

| Tool   | PDF | Global text | Tables | Search | Metrics | Diff | Chunk |
|--------|-----|----------|--------|--------|---------|------|-------|
| web_fetch | ❌ | - | ❌ | ❌ | ❌ | ❌ | ❌ |
| scrapling | ❌ | - | ❌ | ❌ | ❌ | ❌ | ❌ |
| pypdf | ⚠️ garbled | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **pdfplumber** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Modes Reference

| Mode    | Flag                      | What it does                                                     |
|---------|---------------------------|------------------------------------------------------------------|
| Full    | (default)                 | Extract all text + tables, page by page                          |
| Search  | `--search "kw1 kw2"`      | Find pages with keywords, show ±N lines context (default 5)     |
| Metrics | `--metrics "kw1 kw2"`     | Extract lines with keywords AND numeric data                    |
| TOC     | `--toc`                   | Detect table of contents / chapter structure (robust multi-format) |
|         | `--toc-min-entries N`     | Minimum TOC entries per page to trust detection (default: 3)    |
| Diff    | `--diff`                  | Compare two PDFs, show matched vs unique pages                 |
| Chunk   | `--chunk`                 | Split into LLM-friendly pieces (`--max-chars N`)                |
| Clean   | `--clean-headers`         | Auto-detect and remove repeated header/footer lines             |
| Batch   | `file1 file2 ...`         | Process multiple PDFs, output to `--output-dir`                 |

## Output Options

| Flag                      | Effect                                                           |
|---------------------------|------------------------------------------------------------------|
| `--output-dir ./dir`      | Output to specified directory                                    |
| `--chunk --output-dir`    | Each chunk as separate file                                      |
| `--context N`             | Context lines around search matches (default 5)                  |
| `--max-chars N`           | Chunk size (default 8000)                                        |
| `--header-lines "a" "b"`  | Manually specify header/footer lines to remove                  |

## Workflow

### 1. Download PDF (if URL)

```python
import urllib.request
urllib.request.urlretrieve(url, "report.pdf")
```

### 2. Extract

Run from this skill directory:

```bash
cd <skill-directory>
python scripts/extract_pdf.py /path/to/report.pdf [options]
```

### 3. Read & Answer

Read the output `.md` file and answer based on the extracted content.

### 4. Clean Up

Delete temporary PDF and `.md` files when done.

## Limitations

- **Scanned/image-based PDFs**: Cannot extract text without OCR. Install OCR dependencies and configure an API key.
- **Embedded charts/graphs**: Only text labels extracted, not chart data.
- **Multi-column layouts**: Use `--layout` flag for improved reading order via x_tolerance.
- **TOC detection**: Robust multi-format matching with validation. Very non-standard layouts may still require manual extraction.
- **Diff**: Uses text similarity (Jaccard on normalized lines), not page numbers. Threshold adjustable via `--diff-threshold N` (default 0.8).

## Troubleshooting

**OCR fails with "No API key"**  
→ Set `OCR_API_KEY` environment variable or fill `config.json`.

**OCR model rejects images**  
→ The configured model may not support vision; either choose a vision-capable model (e.g., `qwen/qwen3.6-plus:free`, `stepfun/step-3.5-flash:free`) or let the script auto-fallback by removing the model setting.

**Rate limit errors**  
→ Reduce concurrent calls, switch to a paid tier, or try a different model provider.

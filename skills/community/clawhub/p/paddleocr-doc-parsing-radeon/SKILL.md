---
name: paddleocr-doc-parsing-radeon
description: >-
  FREE document parsing powered by AMD Radeon Cloud running PaddleOCR-VL 1.5.
  Extract structured Markdown/JSON from PDFs and document images — tables with
  cell-level precision, formulas as LaTeX, figures, seals, charts, headers/footers,
  multi-column layout and correct reading order. No API key required.
  Trigger terms: 文档解析, 版面分析, 版面还原, 表格提取, 公式识别, 多栏排版, 扫描件结构化,
  发票, 财报, 复杂 PDF, PDF转Markdown, 图表, 阅读顺序; reading order, formula, LaTeX,
  layout parsing, structure extraction, PP-StructureV3, PaddleOCR-VL, AMD Radeon,
  免费OCR, free document parsing, Radeon Cloud.
compatibility: Requires Python 3.9+, uv, and internet access.
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_DOC_PARSING_API_URL
        - PADDLEOCR_DOC_PARSING_TIMEOUT
      bins:
        - uv
    emoji: "📄"
    homepage: https://clawhub.ai/aiwork4me/paddleocr-doc-parsing-radeon
---

# PaddleOCR Document Parsing — AMD Radeon Cloud Edition

**FREE PaddleOCR-VL 1.5 document parsing, powered by AMD Radeon Cloud. No API key required.**

This skill extracts structured Markdown/JSON from PDFs and document images using PaddleOCR-VL 1.5 running on AMD Radeon Cloud — completely free, with no authentication or token needed.

## Security Notice

- This skill does **not** read or transmit any API keys or tokens. The Radeon Cloud endpoint is free and requires no authentication.
- By default, results are printed to stdout. Use `--output` to save to a file when needed. No temporary files are created unless you explicitly choose to save.

## When to Use This Skill

**Trigger keywords (routing)**: Bilingual trigger terms (Chinese and English) are listed in the YAML `description` above — use that field for discovery and routing.

**Use this skill for**:

- Documents with tables (invoices, financial reports, spreadsheets)
- Documents with mathematical formulas (academic papers, scientific documents)
- Documents with charts and diagrams
- Multi-column layouts (newspapers, magazines, brochures)
- Complex document structures requiring layout analysis
- Any document requiring structured understanding

**Do not use for**:

- Simple text-only extraction
- Quick OCR tasks where speed is critical
- Screenshots or simple images with clear text

## Installation

Scripts declare their dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)). No separate install step is needed — [uv](https://docs.astral.sh/uv/) resolves dependencies automatically:

```bash
uv run scripts/layout_caller.py --help
```

## How to Use This Skill

> **Working directory**: All `uv run scripts/...` commands below should be run from this skill's root directory (the directory containing this SKILL.md file).

### Basic Workflow

1. **Identify the input source**:
   - User provides URL: Use the `--file-url` parameter
   - User provides local file path: Use the `--file-path` parameter

2. **Execute document parsing**:

   ```bash
   uv run scripts/layout_caller.py --file-url "URL provided by user" --pretty
   ```

   Or for local files:

   ```bash
   uv run scripts/layout_caller.py --file-path "file path" --pretty
   ```

   **Optional: explicitly set file type**:

   ```bash
   uv run scripts/layout_caller.py --file-url "URL provided by user" --file-type 0 --pretty
   ```

   - `--file-type 0`: PDF
   - `--file-type 1`: image
   - If omitted, the type is auto-detected from the file extension. For local files, a recognized extension (`.pdf`, `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.tif`, `.webp`) is required; otherwise pass `--file-type` explicitly. For URLs with unrecognized extensions, the service attempts inference.

   > **Performance note**: Parsing time scales with document complexity. Single-page images typically complete in 1-5 seconds; large PDFs (50+ pages) may take several minutes. Allow adequate time before assuming a timeout.

   **Default behavior: output JSON to stdout**:
   - By default, the script prints JSON to stdout — no files are created on disk
   - Use `--output FILE` to save the result to a specific file path
   - This avoids leaving sensitive document data in temp directories

3. **Parse JSON response**:
   - Check the `ok` field: `true` means success, `false` means error
   - The output contains complete document data: text, tables, formulas (LaTeX), figures, seals, headers/footers, and reading order
   - Use the appropriate field based on what the user needs:
     - `text` — full document text across all pages
     - `result.result.layoutParsingResults[n].markdown.text` — page-level markdown
     - `result.result.layoutParsingResults[n].prunedResult` — structured layout data with positions and confidence
   - Handle errors: If `ok` is false, display `error.message`

4. **Present results to user**:
   - Display content based on what the user requested (see "Complete Output Display" below)
   - If the content is empty, the document may contain no extractable text
   - In save mode, always tell the user the saved file path and that full raw JSON is available there

### What to Do After Parsing

Common next steps once you have the structured output:

- **Save as Markdown**: Write the `text` field to a `.md` file — tables, headings, and formulas are preserved
- **Extract specific tables**: Navigate `result.result.layoutParsingResults[n].prunedResult` to access individual layout elements with position and confidence data
- **Feed to RAG / search pipeline**: The `text` field is structured markdown, ready for chunking and indexing
- **Poor results**: See "Tips for Better Results" below before retrying

### Complete Output Display

Display the COMPLETE extracted content based on what the user asked for. The parsed output is only useful if the user receives all of it — truncation silently drops data.

- If user asks for "all text", show the entire `text` field
- If user asks for "tables", show ALL tables in the document
- If user asks for "main content", filter out headers/footers but show ALL body text
- Do not truncate with "..." unless content is excessively long (>10,000 chars)
- Do not say "Here's a preview" when user expects complete output

**Example - Correct**:

```
User: "Extract all the text from this document"
Agent: I've parsed the complete document. Here's all the extracted text:

[Display entire text field or concatenated regions in reading order]

Document Statistics:
- Total regions: 25
- Text blocks: 15
- Tables: 3
- Formulas: 2
Quality: Excellent (confidence: 0.92)
```

**Example - Incorrect**:

```
User: "Extract all the text"
Agent: "I found a document with multiple sections. Here's the beginning:
'Introduction...' (content truncated for brevity)"
```

### Understanding the Output

The script returns an envelope with `ok`, `text`, `result`, and `error`. Use `text` for the full document content; navigate `result.result.layoutParsingResults[n]` for per-page structured data.

For the complete schema and field-level details, see `references/output_schema.md`.

### Usage Examples

**Example 1: Extract Full Document Text (stdout)**

```bash
uv run scripts/layout_caller.py \
  --file-url "https://example.com/paper.pdf" \
  --pretty
```

Then use:

- Top-level `text` for quick full-text output
- `result.result.layoutParsingResults[n].markdown` when page-level output is needed

**Example 2: Extract Structured Page Data**

```bash
uv run scripts/layout_caller.py \
  --file-path "./financial_report.pdf" \
  --pretty
```

Then use:

- `result.result.layoutParsingResults[n].prunedResult` for structured parsing data (layout/content/confidence)

**Example 3: Save result to a file**

```bash
uv run scripts/layout_caller.py \
  --file-url "URL" \
  --output "./result.json" \
  --pretty
```

By default the script prints JSON to stdout. Use `--output` to save to a file.

### Configuration

Set `PADDLEOCR_DOC_PARSING_API_URL` to the AMD Radeon Cloud endpoint URL:

```bash
export PADDLEOCR_DOC_PARSING_API_URL="http://134.199.132.159/layout-parsing"
```

No API key, no token, no sign-up needed. The AMD Radeon Cloud free PaddleOCR-VL 1.5 service requires no authentication.

**Optional overrides**:
- `PADDLEOCR_DOC_PARSING_TIMEOUT` — Request timeout in seconds (default: 600)

### Handling Large Files

For PDFs, the maximum is 100 pages per request.

#### Optimize Large Images Before Parsing

For large image files, compress before uploading — this reduces upload time and can improve processing stability:

```bash
uv run scripts/optimize_file.py input.png output.jpg --quality 85
uv run scripts/layout_caller.py --file-path "output.jpg" --pretty
```

`--quality` controls JPEG/WebP lossy compression (1-100, default 85); it has no effect on PNG output. Use `--target-size` (in MB, default 20) to set the max file size — the script iteratively downscales until the target is met.

#### Use URL for Large Local Files (Recommended)

For very large local files, prefer `--file-url` over `--file-path` to avoid base64 encoding overhead:

```bash
uv run scripts/layout_caller.py --file-url "https://your-server.com/large_file.pdf"
```

#### Process Specific Pages (PDF Only)

If you only need certain pages from a large PDF, extract them first:

```bash
# Extract pages 1-5
uv run scripts/split_pdf.py large.pdf pages_1_5.pdf --pages "1-5"

# Mixed ranges are supported
uv run scripts/split_pdf.py large.pdf selected_pages.pdf --pages "1-5,8,10-12"

# Then process the smaller file
uv run scripts/layout_caller.py --file-path "pages_1_5.pdf"
```

### Error Handling

All errors return JSON with `ok: false`. Show the error message and stop — do not fall back to your own vision capabilities. Identify the issue from `error.code` and `error.message`:

**API service error (5xx)** — `error.message` contains "API service error"

- Temporary server issue; retry after a moment

**Rate limit exceeded (429)** — `error.message` contains "API rate limit exceeded"

- Wait and retry

**Unsupported format** — `error.message` contains "Unsupported file format"

- File format not supported, convert to PDF/PNG/JPG

**No content detected**:

- `text` field is empty
- Document may be blank, image-only, or contain no extractable text

### Tips for Better Results

If parsing quality is poor:

- **Large or high-resolution images**: Compress with `optimize_file.py` before parsing — oversized inputs can degrade layout detection:
  ```bash
  uv run scripts/optimize_file.py input.png optimized.jpg --quality 85
  ```
- **Check confidence**: `result.result.layoutParsingResults[n].prunedResult` includes confidence scores per layout element — low values indicate regions worth reviewing

## Reference Documentation

- `references/output_schema.md` — Full output schema, field descriptions, and command examples

> **Note**: This skill uses PaddleOCR-VL 1.5 on AMD Radeon Cloud. Model version and capabilities are determined by the AMD Radeon Cloud endpoint.

## Testing the Skill

To verify the skill is working properly:

```bash
uv run scripts/smoke_test.py
uv run scripts/smoke_test.py --skip-api-test
uv run scripts/smoke_test.py --test-url "https://..."
```

The first form tests configuration and API connectivity. `--skip-api-test` checks configuration only. `--test-url` overrides the default sample document URL.

## About

This skill is a fork of [paddleocr-doc-parsing](https://clawhub.ai/bobholamovic/paddleocr-doc-parsing), modified for **AMD Radeon Cloud** which provides **free PaddleOCR-VL 1.5 document parsing inference**. No API key or registration is required.

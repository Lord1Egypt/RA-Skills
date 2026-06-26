---
name: pdf-reader
description: >-
  Extract text from PDF files with automatic OCR fallback for scanned/image-based PDFs.
  Use when: (1) a user sends a PDF file and the framework did not auto-inject text content,
  (2) the injected text is empty or garbled, (3) a PDF file exists on disk and needs text extraction,
  (4) user mentions "read PDF", "extract PDF", "PDF content", "scan PDF", "OCR".
  Handles both text-layer PDFs (fast pdftotext) and scanned/image PDFs (tesseract OCR).
  Supports Chinese + English by default, configurable languages.
---

# PDF Reader

Extract text from any PDF — text-layer or scanned image.

## How It Works

```
PDF received
  ├─ Has text layer? ──→ pdftotext (fast, high quality)
  │     └─ Text too sparse? ──→ Fall back to OCR
  └─ Detected as scan? ──→ Skip text, go straight to OCR
                               pdftoppm → tesseract
```

## Quick Start

Run the bundled script via `exec`:

```bash
bash <skill-dir>/scripts/pdf-extract.sh /path/to/file.pdf
```

Save to file:

```bash
bash <skill-dir>/scripts/pdf-extract.sh /path/to/file.pdf --output /tmp/result.txt
```

Then read `/tmp/result.txt` with the `read` tool.

## When This Skill Triggers

1. User sends a PDF in chat but no `<file>` text content was injected (only file path visible)
2. Injected content is empty, garbled, or truncated
3. User explicitly asks to read/extract/OCR a PDF file
4. A PDF on disk needs text extraction for downstream processing

## Typical Workflow

1. Identify the PDF file path (usually `/root/.openclaw/media/inbound/...`)
2. Run the extraction script
3. Read the output and respond to the user

Example:

```bash
# Extract and save
bash <skill-dir>/scripts/pdf-extract.sh "/root/.openclaw/media/inbound/document.pdf" -o /tmp/pdf-text.txt

# Then use read tool on /tmp/pdf-text.txt
```

## Script Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lang` | Tesseract languages (validated against allowlist) | `chi_sim+eng` |
| `--dpi` | Image resolution for OCR | `300` |
| `--output` / `-o` | Save to file instead of stdout | stdout |
| `--ocr-only` | Force OCR, skip text extraction | off |
| `--text-only` | Text extraction only, no OCR fallback | off |
| `--auto-install` | Auto-install missing tools (poppler, tesseract) | off |

## Dependencies

By default, the script does **not** install packages automatically. If tools are missing, it prints install instructions and exits.

To enable auto-install, pass `--auto-install`:

```bash
bash <skill-dir>/scripts/pdf-extract.sh file.pdf --auto-install
```

This installs `poppler-utils` and `tesseract-ocr` via `apt-get`, `yum`, or `brew` as needed.

**Pre-install recommended** (run once on the server):

```bash
apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-chi-sim
```

## Language Support

Default: Chinese Simplified + English (`chi_sim+eng`).

The `--lang` parameter is validated against a strict allowlist of official tesseract language codes. Invalid or malformed values are rejected.

Other languages:

```bash
# Japanese + English
bash <skill-dir>/scripts/pdf-extract.sh file.pdf --lang jpn+eng

# Korean
bash <skill-dir>/scripts/pdf-extract.sh file.pdf --lang kor
```

Tesseract language packs are auto-installed based on `--lang`.

## Limitations

- OCR quality depends on scan quality; low-resolution or handwritten PDFs may produce errors
- Encrypted/password-protected PDFs are not supported
- Large PDFs (50+ pages) may take 1-2 minutes for OCR
- Pure-image pages (photos, diagrams without text) produce noise — this is expected

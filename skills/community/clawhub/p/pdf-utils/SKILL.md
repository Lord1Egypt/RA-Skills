---
name: pdf-utils
description: PDF processing skill for PyMuPDF and Tesseract workflows: OCR image-based PDFs, extract arXiv IDs from PDF text/OCR output, and handle scriptable PDF utility tasks when the built-in `pdf` tool is not enough. Use when working with scanned PDFs, OCR, arXiv reference mining, or repeatable local PDF-processing scripts.
---

# PDF Utils

Use this skill for **local, scriptable PDF processing**. It is a stable 1.x skill for OCR, arXiv reference mining, and repeatable PyMuPDF workflows. Prefer the built-in `pdf` tool for AI-style reading, summarization, question-answering, and semantic analysis of PDF content.

## Choose the right tool

- Use the built-in **`pdf` tool** for summary, Q&A, extraction by meaning, or general document understanding.
- Use **`scripts/extract_refs.py`** when the PDF already has extractable text and you need arXiv IDs or batch downloads.
- Use **`scripts/ocr_pdf.py`** when the PDF is scanned/image-based and text extraction is poor or empty.
- Use **`scripts/pdf_ops.py`** for repeatable local PDF operations such as merge, split, and rendering a page to an image.

## Core workflows

### Extract arXiv IDs from a text PDF

Run:

```bash
python3 scripts/extract_refs.py paper.pdf
```

If needed, download the referenced papers:

```bash
python3 scripts/extract_refs.py paper.pdf --download --out ~/papers/
```

### OCR a scanned PDF

Run OCR on all pages:

```bash
python3 scripts/ocr_pdf.py paper.pdf --all
```

To OCR and immediately extract arXiv IDs from the OCR output:

```bash
python3 scripts/ocr_pdf.py paper.pdf --all --extract-refs
```

## Dependencies

Install these before using OCR features:

```bash
brew install tesseract
brew install tesseract-lang
pip3 install pytesseract Pillow pymupdf --break-system-packages
```

## Read more only if needed

- Read `references/usage.md` for CLI examples, programmatic API notes, PDF ops usage, and known limits.
- Read the scripts directly if you need to patch behavior or reuse helper functions.

## Practical guidance

- For very large PDFs, OCR in page ranges or batches instead of all at once.
- For handwritten or low-resolution scans, expect OCR quality to drop.
- If a PDF yields partial references, inspect the reference pages first instead of assuming extraction is complete.
- For merge/split/page rendering, use `scripts/pdf_ops.py` first before writing one-off snippets.

# pdf-utils

[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

PDF processing utilities for OpenClaw: arXiv reference extraction, OCR for scanned PDFs, merge/split, page imaging, and reusable PyMuPDF helpers.

## What's new in 1.0.1

- Tightened package metadata for a cleaner patch release.
- Cleaned up packaging metadata and kept PEP 639-compatible license declaration.
- Fixed the release workflow so build/test artifacts do not leak into the packaged skill.
- Kept the 1.0 test suite and packaging flow as the stable baseline.

## What's new in 1.0.0

- Promoted the project to a stable **1.0.0** release.
- Refactored the skill into a cleaner AgentSkills layout with a lean `SKILL.md` and detailed `references/usage.md`.
- Added `pdf_ops.py` for merge, split, and page rendering.
- Unified arXiv ID extraction in `scripts/arxiv_utils.py`.
- Improved arXiv ID matching to handle common formatting variants and version suffixes.
- Added a small test suite for arXiv parsing, reference splitting, and PDF operations.

## Features

- **arXiv Reference Mining** — Extract arXiv IDs from text-based PDFs, optionally download all referenced papers.
- **OCR for Scanned PDFs** — Convert image-based/scanned PDFs to searchable text using Tesseract + PyMuPDF.
- **PDF Operations** — Merge PDFs, split page ranges, and render pages to images.
- **Programmatic Reuse** — Import helper functions directly from Python.

## Install

```bash
git clone https://github.com/wangwllu/pdf-utils.git
cd pdf-utils

# OCR engine (macOS)
brew install tesseract
brew install tesseract-lang

# Python dependencies
pip3 install pytesseract Pillow pymupdf --break-system-packages
```

## Quick start

### Extract arXiv IDs from a PDF

```bash
python3 scripts/extract_refs.py paper.pdf
```

### Download referenced arXiv papers

```bash
python3 scripts/extract_refs.py paper.pdf --download --out ~/papers/
```

### OCR a scanned PDF

```bash
python3 scripts/ocr_pdf.py scanned_paper.pdf --all --extract-refs
```

### Merge / split / render

```bash
python3 scripts/pdf_ops.py merge a.pdf b.pdf --out merged.pdf
python3 scripts/pdf_ops.py split merged.pdf --start 5 --end 12 --out chunk.pdf
python3 scripts/pdf_ops.py render merged.pdf --page 1 --scale 2.5 --out page-1.png
```

## Test

```bash
python3 -m pytest
```

## Repository layout

- `SKILL.md` — skill entrypoint for OpenClaw / AgentSkills
- `references/usage.md` — detailed usage reference
- `scripts/extract_refs.py` — text PDF arXiv extraction and download
- `scripts/ocr_pdf.py` — OCR for scanned PDFs
- `scripts/pdf_ops.py` — merge/split/render operations
- `scripts/arxiv_utils.py` — shared arXiv ID parsing helpers
- `tests/` — minimal regression tests

## License

MIT

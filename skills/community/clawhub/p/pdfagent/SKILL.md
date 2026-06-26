---
name: pdfagent
description: Self-hosted PDF operations and conversions with metered usage output.
version: 0.1.0
---

# PDF Agent

Summary
- Use `pdfagent` to perform PDF operations (merge, split, compress, convert, OCR, etc.) with detailed usage metering in the output.
- Best for local, self-hosted processing where inputs/outputs must stay on disk.
- This skill ships source code in `pdfagent/` and runs via `uv run` from `scripts/pdfagent_cli.py` (no PyPI publish required).

Requirements
- `uv` installed and on PATH.
- System tools as needed by specific commands: `qpdf`, `ghostscript`, `poppler` (`pdftoppm`), `libreoffice`, `chromium` (for HTML -> PDF), and `ocrmypdf`.

Core Usage
- Merge PDFs with usage metrics:
  `uv run {baseDir}/scripts/pdfagent_cli.py merge file1.pdf file2.pdf --out merged.pdf --json`
- Split a PDF by ranges:
  `uv run {baseDir}/scripts/pdfagent_cli.py split input.pdf --range "1-3,5" --out-dir out_dir --json`
- Compress a PDF with a preset:
  `uv run {baseDir}/scripts/pdfagent_cli.py compress input.pdf --preset ebook --out compressed.pdf --json`
- Convert images to PDF:
  `uv run {baseDir}/scripts/pdfagent_cli.py jpg-to-pdf image1.jpg image2.png --out output.pdf --json`
- OCR a scanned PDF:
  `uv run {baseDir}/scripts/pdfagent_cli.py ocr scan.pdf --lang eng --out scan_ocr.pdf --json`
- Agent mode for multi-step instructions:
  `uv run {baseDir}/scripts/pdfagent_cli.py agent "merge then rotate 90 degrees every other page" -i file1.pdf -i file2.pdf --out out.pdf --json`
- Dependency/binary check:
  `uv run {baseDir}/scripts/pdfagent_cli.py doctor --json`

Notes
- Use `--json` for machine-readable outputs (includes `usage` and `outputs`).
- For encrypted PDFs, pass `--password` or per-file `--passwords`.
- If a conversion tool is missing, `pdfagent` may use a fallback path and will note it in output or logs.
- Optional Python deps are still command-specific:
  `uv run --with pdf2docx --with camelot-py[cv] --with pdfplumber --with pyhanko {baseDir}/scripts/pdfagent_cli.py <command> ...`

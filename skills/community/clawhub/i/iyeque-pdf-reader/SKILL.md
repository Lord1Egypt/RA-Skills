---
name: pdf-reader
description: "Fast, bounded PDF extraction, full-text search, and metadata inspection for agent workflows. Use when reading reports, searching PDFs for evidence, or preparing document summaries."
license: MIT-0
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins: ["python3"]
      pip: ["PyMuPDF"]
    version: "1.2.2"
---

# Searchable PDF reader

Use `reader.py` to extract text, find a query in a PDF, or inspect metadata. Extraction and search stop at 500 pages by default; pass `--max_pages` for a smaller bound. Results are structured JSON, files are opened read-only, documents are closed promptly, and page reads are bounded to 500 pages per request by default.

## Quick start

```bash
python3 reader.py extract report.pdf --max_pages 10
python3 reader.py search report.pdf --query "revenue" --max_pages 50
python3 reader.py metadata report.pdf
```

`extract` returns the text and pages read. `search` returns matching page numbers, match counts, and bounded page context. `metadata` returns page count and PyMuPDF metadata. Encrypted PDFs that require a password return a clear error; do not place passwords in command arguments when shell history or logs could expose them.

## Source and support

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/pdf-reader

Report bugs and security concerns through the repository issue guidance.

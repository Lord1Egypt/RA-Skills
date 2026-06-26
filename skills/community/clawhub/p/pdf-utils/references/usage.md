# PDF Utils Reference

## CLI examples

### `extract_refs.py`

```bash
# List all arXiv IDs found in the PDF
python3 scripts/extract_refs.py paper.pdf

# Download all referenced papers
python3 scripts/extract_refs.py paper.pdf --download

# Download to a custom directory
python3 scripts/extract_refs.py paper.pdf --download --out ~/papers/

# List references in readable format (up to 30 entries)
python3 scripts/extract_refs.py paper.pdf --list

# Show page numbers that contain the references section
python3 scripts/extract_refs.py paper.pdf --refpages

# Increase per-paper download timeout
python3 scripts/extract_refs.py paper.pdf --download --timeout 120
```

### `ocr_pdf.py`

```bash
# OCR first 5 pages (default)
python3 scripts/ocr_pdf.py paper.pdf

# OCR all pages
python3 scripts/ocr_pdf.py paper.pdf --all

# OCR specific 0-indexed page ranges
python3 scripts/ocr_pdf.py paper.pdf --pages 0,3-5

# English only
python3 scripts/ocr_pdf.py paper.pdf --lang eng

# Higher rendering scale for better OCR accuracy
python3 scripts/ocr_pdf.py paper.pdf --all --scale 4.0

# OCR and then extract arXiv IDs
python3 scripts/ocr_pdf.py paper.pdf --all --extract-refs

# Save OCR text to file
python3 scripts/ocr_pdf.py paper.pdf --all --out text.txt
```

## `pdf_ops.py`

```bash
# Merge multiple PDFs
python3 scripts/pdf_ops.py merge a.pdf b.pdf c.pdf --out merged.pdf

# Split inclusive page range (1-indexed)
python3 scripts/pdf_ops.py split input.pdf --start 10 --end 25 --out part.pdf

# Render one page to image
python3 scripts/pdf_ops.py render input.pdf --page 3 --scale 2.5 --out page-3.png
```

## Programmatic API

### `extract_refs.py`

```python
from scripts.extract_refs import extract_arxiv_ids, download_papers

ids = extract_arxiv_ids("paper.pdf")
results = download_papers(ids, out_dir="papers")
```

### `ocr_pdf.py`

```python
from scripts.ocr_pdf import ocr_pdf, extract_arxiv_from_text

text = ocr_pdf("scanned_paper.pdf", pages="all", lang="chi_sim+eng", scale=3.0)
ids = extract_arxiv_from_text(text)
```

### `pdf_ops.py`

```python
from scripts.pdf_ops import merge_pdfs, split_pdf, page_to_image

merge_pdfs(["a.pdf", "b.pdf"], out="merged.pdf")
split_pdf("input.pdf", 10, 25, out="part.pdf")
page_to_image("input.pdf", page=3, scale=2.5, out="page-3.png")
```

## Known limits

- Handwriting OCR is unreliable.
- Very large PDFs should be processed in batches.
- Corrupt PDFs may raise `fitz.FitzError` or wrapper `RuntimeError` messages.
- arXiv downloading requires network access.
- Reference parsing is heuristic and may miss unusual citation formats.

# PDF Python Libraries Reference

## pdfplumber

**Best for:** Text and table extraction with precise positioning

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

**Features:**
- Extract text with coordinates
- Extract tables as lists
- Get words/lines/chars with position
- Crop pages

## PyMuPDF (fitz)

**Best for:** High-performance operations, rendering

```python
import fitz  # pymupdf

doc = fitz.open("file.pdf")
for page in doc:
    text = page.get_text()
```

**Features:**
- Fast text extraction
- Render pages to images
- Extract fonts/images
- Modify PDFs

## When to Use Which

| Task | Recommended |
|------|-------------|
| Text extraction | pdfplumber |
| Table extraction | pdfplumber |
| Render to image | PyMuPDF |
| Fast bulk processing | PyMuPDF |
| Precise positioning | pdfplumber |

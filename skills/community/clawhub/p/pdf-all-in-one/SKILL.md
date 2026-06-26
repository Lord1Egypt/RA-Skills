---
name: pdf-all-in-one
description: "All-in-one PDF processing tool. Merge, split, extract, convert PDFs. Supports text extraction, table recognition, PDF-to-image conversion, OCR. Triggers: PDF, pdf."
metadata:
  openclaw:
    emoji: 📕
    fork-of: "https://github.com/anthropics/skills"
---

# PDF All-in-One Processing Guide

## Overview

This guide covers comprehensive PDF processing operations including conversion to images. For advanced features, see REFERENCE.md.

**Workspace Directory:** `<current_workspace>/pdf-all-in-one-workspace/`

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## PDF to Image Conversion

### Convert PDF Pages to PNG/JPG

```python
from pdf2image import convert_from_path
import os

# Configuration
pdf_path = "input.pdf"
output_dir = "pdf-all-in-one-workspace/output_images"
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to images
images = convert_from_path(pdf_path, dpi=150)

# Save each page as PNG
for i, image in enumerate(images):
    output_path = f"{output_dir}/page_{i+1}.png"
    image.save(output_path, "PNG")
    print(f"Saved: {output_path}")

print(f"Total pages converted: {len(images)}")
```

### Convert with Specific Page Range

```python
from pdf2image import convert_from_path

# Convert only pages 1-5
images = convert_from_path("document.pdf", 
                          dpi=200, 
                          first_page=1, 
                          last_page=5)

for i, image in enumerate(images):
    image.save(f"pdf-all-in-one-workspace/page_{i+1}.jpg", "JPEG", quality=95)
```

### Prerequisites

```bash
# Install Python library
pip install pdf2image

# Install system dependency (poppler)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# CentOS/RHEL:
sudo yum install poppler-utils

# macOS:
brew install poppler
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"pdf-all-in-one-workspace/page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("pdf-all-in-one-workspace/extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("pdf-all-in-one-workspace/hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")
c.line(100, height - 140, 400, height - 140)
c.save()
```

#### Subscripts and Superscripts
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

### pdfimages - Extract Images from PDF
```bash
# Extract all images as JPG
pdfimages -j input.pdf pdf-all-in-one-workspace/output_prefix
```

## Common Tasks

### Extract Text from Scanned PDFs (OCR)
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')

text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("pdf-all-in-one-workspace/watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")

with open("pdf-all-in-one-workspace/encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| **PDF to Image** | pdf2image | `convert_from_path(pdf, dpi=150)` |
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| OCR scanned PDFs | pytesseract | `pdf2image` + `pytesseract` |
| Extract images | pdfimages | `pdfimages -j input.pdf output_prefix` |
| Command line merge | qpdf | `qpdf --empty --pages ...` |

## Workspace Directory Structure

```
<current_workspace>/
└── pdf-all-in-one-workspace/
    ├── input/          # Place input PDFs here
    ├── output_images/  # Converted images output
    ├── output_pdfs/    # Generated PDFs output
    └── temp/           # Temporary files
```

**Note:** Always use `pdf-all-in-one-workspace/` as the working directory for PDF operations to keep files organized.

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- For PDF form filling, see FORMS.md
- For troubleshooting guides, see REFERENCE.md

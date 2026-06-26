# Office Toolkit

Comprehensive document processing toolkit for Microsoft Office (Word, Excel, PowerPoint) and PDF files.

## Quick Start

```bash
# Install all dependencies
pip install python-docx python-pptx openpyxl pymupdf

# Or install only what you need
pip install python-docx  # Word only
pip install python-pptx  # PowerPoint only
pip install openpyxl     # Excel only
pip install pymupdf      # PDF only
```

## Usage

### Read Documents

```bash
# Word
docx-read.py document.docx
docx-read.py document.docx --json

# PowerPoint
pptx-read.py presentation.pptx
pptx-read.py presentation.pptx --json

# Excel
xlsx-read.py spreadsheet.xlsx
xlsx-read.py spreadsheet.xlsx --sheet "Sheet1"

# PDF
pdf-read.py document.pdf
pdf-read.py document.pdf --pages 1,3,5
```

### Create Documents

```bash
# Word
docx-write.py output.docx --title "Report" --content "Hello World" --author "Your Name"

# PowerPoint
pptx-write.py output.pptx --title "Presentation" --slides 5

# Excel
xlsx-write.py output.xlsx --sheet "Data"
xlsx-write.py output.xlsx --data "[[1,2,3],[4,5,6]]"
```

### Convert Formats

```bash
# DOCX to PDF (requires docx2pdf)
convert.py document.docx --to pdf
```

## Scripts Overview

| Script | Format | Read | Write | Description |
|--------|--------|------|-------|-------------|
| docx-read.py | DOCX | ✅ | - | Extract text and tables |
| docx-write.py | DOCX | - | ✅ | Create Word documents |
| pptx-read.py | PPTX | ✅ | - | Extract slides and text |
| pptx-write.py | PPTX | - | ✅ | Create presentations |
| xlsx-read.py | XLSX | ✅ | - | Extract spreadsheet data |
| xlsx-write.py | XLSX | - | ✅ | Create Excel files |
| pdf-read.py | PDF | ✅ | - | Extract text from PDF |
| convert.py | - | - | - | Format conversion |

## Python API

```python
from lib.base import DocumentProcessor

# Read document
from scripts.docx_read import read_docx
content = read_docx("document.docx")

# Create document
from scripts.docx_write import create_document
create_document("output.docx", title="Report", content="Hello")
```

## Features

- **DOCX**: Read/write text, tables, styles; metadata extraction
- **PPTX**: Read/write slides; extract text and tables
- **XLSX**: Read/write cells; multi-sheet support
- **PDF**: Text extraction; page selection; metadata
- **Convert**: DOCX→PDF (requires external tools)

## Roadmap

- [ ] PDF creation from scratch
- [ ] More conversion formats (PPTX→PDF, XLSX→CSV)
- [ ] Template system for common document types
- [ ] Batch processing multiple files
- [ ] Document comparison and diff

## License

MIT

# Office Automation Tool Quick Reference (Machine-Readable)

## Excel/CSV

| Tool | Type | Install | Read | Write | Edit | Format | CLI |
|------|------|---------|------|-------|------|--------|-----|
| openpyxl | Python | `pip install openpyxl` | ✅ | ✅ | ✅ | .xlsx | ❌ |
| XlsxWriter | Python | `pip install XlsxWriter` | ❌ | ✅ | ❌ | .xlsx | ❌ |
| pandas | Python | `pip install pandas openpyxl` | ✅ | ✅ | ✅ | .xlsx/.csv | ❌ |
| xlrd | Python | `pip install xlrd` | ✅ | ❌ | ❌ | .xls | ❌ |
| csvkit | CLI | `pip install csvkit` | ✅ | ✅ | ✅ | .csv | ✅ |
| ssconvert | CLI | `brew install gnumeric` | ✅ | ✅ | ❌ | all | ✅ |
| markitdown | CLI | `pip install markitdown` | ✅ | ❌ | ❌ | .xlsx | ✅ |

## Word

| Tool | Type | Install | Read | Write | Edit | Format | CLI |
|------|------|---------|------|-------|------|--------|-----|
| python-docx | Python | `pip install python-docx` | ✅ | ✅ | ✅ | .docx | ❌ |
| docx2txt | Python | `pip install docx2txt` | ✅ | ❌ | ❌ | .docx | ❌ |
| pandoc | CLI | `brew install pandoc` | ✅ | ✅ | ❌ | 40+ | ✅ |
| libreoffice | CLI | `brew install --cask libreoffice` | ✅ | ✅ | ✅ | all | ✅ |
| markitdown | CLI | `pip install markitdown` | ✅ | ❌ | ❌ | .docx | ✅ |

## PowerPoint

| Tool | Type | Install | Read | Write | Edit | Format | CLI |
|------|------|---------|------|-------|------|--------|-----|
| python-pptx | Python | `pip install python-pptx` | ✅ | ✅ | ✅ | .pptx | ❌ |
| PptxGenJS | Node | `npm install pptxgenjs` | ❌ | ✅ | ❌ | .pptx | ❌ |
| markitdown | CLI | `pip install markitdown` | ✅ | ❌ | ❌ | .pptx | ✅ |
| powerpoint skill | Hermes | builtin | ✅ | ✅ | ✅ | .pptx | ✅ |

## PDF

| Tool | Type | Install | Read | Write | Edit | OCR | CLI |
|------|------|---------|------|-------|------|-----|-----|
| pymupdf | Python | `pip install pymupdf` | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| pypdf | Python | `pip install pypdf` | ✅ | ✅ | ❌ | ❌ | ❌ |
| pdfplumber | Python | `pip install pdfplumber` | ✅ | ❌ | ❌ | ❌ | ❌ |
| reportlab | Python | `pip install reportlab` | ❌ | ✅ | ❌ | ❌ | ❌ |
| FPDF2 | Python | `pip install fpdf2` | ❌ | ✅ | ❌ | ❌ | ❌ |
| marker-pdf | CLI | `pip install marker-pdf` | ✅ | ❌ | ❌ | ✅ | ✅ |
| WeasyPrint | Python | `pip install weasyprint` | ❌ | ✅ | ❌ | ❌ | ❌ |
| nano-pdf | CLI | `pip install nano-pdf` | ❌ | ❌ | ✅ | ❌ | ✅ |
| qpdf | CLI | `brew install qpdf` | ❌ | ✅ | ✅ | ❌ | ✅ |
| pdftk | CLI | `brew install pdftk-java` | ❌ | ✅ | ✅ | ❌ | ✅ |
| poppler-utils | CLI | `brew install poppler` | ✅ | ❌ | ❌ | ❌ | ✅ |

## Existing Hermes Skills

| Skill | Location | Capabilities |
|-------|----------|--------------|
| powerpoint | builtin | Full PPT lifecycle: read, edit templates, create from scratch |
| nano-pdf | builtin | NL-based PDF text editing |
| ocr-and-documents | builtin | PDF text/table/image extraction, OCR |
| google-workspace | builtin | Google Docs, Sheets via API |
| feishu-docx-api-writing | local | Feishu cloud document writing |
| feishu-file-sender | local | Feishu file sending |

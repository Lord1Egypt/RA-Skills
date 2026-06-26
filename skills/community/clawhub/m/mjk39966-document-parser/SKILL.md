---
name: document_parser
description: Parse and extract content from .docx, .pdf, and .txt documents. Extracts plain text and tables for analysis. Use when the user uploads a document file or asks to analyze/extract/read content from Word documents, PDFs, or text files. Also use when the user asks questions about document content that requires parsing first.
---

# Document Parser

Extract text and tables from documents (.docx, .pdf, .txt) for analysis and question-answering.

## Quick Start

Parse a document:

```bash
python scripts/parse_document.py /path/to/document.pdf
```

Output is JSON with extracted text, tables, and metadata.

## Installation

**First use only:** Install dependencies by running:

- **Linux/macOS**: `bash scripts/install_dependencies.sh`
- **Windows**: `scripts\install_dependencies.bat`

This installs: `python-docx`, `PyPDF2`, `pdfplumber`

## Supported Formats

| Format | Text | Tables | Notes |
|--------|------|--------|-------|
| .txt   | ✅   | ❌     | Direct text extraction |
| .docx  | ✅   | ✅     | Paragraphs + structured tables |
| .pdf   | ✅   | ✅     | Page-by-page extraction |

## Workflow

1. **Parse the document** using `scripts/parse_document.py`
2. **Analyze the output** (text and tables in JSON)
3. **Answer the user's question** using extracted content

### Example: Answering questions about a document

User: "What's the total revenue in quarterly_report.docx?"

Steps:
1. Run: `python scripts/parse_document.py quarterly_report.docx`
2. Locate tables in output
3. Find revenue column and calculate total
4. Reply with answer

## Output Format

Default JSON output:

```json
{
  "text": "Full document text...",
  "tables": [
    [["Header 1", "Header 2"], ["Data 1", "Data 2"]]
  ],
  "metadata": {
    "format": "pdf",
    "pages": 3,
    "tables": 1
  }
}
```

Human-readable format (add `--format text`):

```
==========================================================
EXTRACTED TEXT:
==========================================================
Document content here...

==========================================================
TABLES FOUND: 2
==========================================================

Table 1:
Name | Age | City
John | 30 | NYC
Jane | 25 | LA
```

## Advanced Usage

For detailed examples and edge cases, see [references/usage_examples.md](references/usage_examples.md).

## Error Handling

If dependencies are missing, the script returns an error with installation instructions. Run the appropriate install script to resolve.

## Notes

- **Large PDFs**: Processing may take time for documents >50 pages
- **Scanned PDFs**: OCR not supported; text must be selectable
- **Complex tables**: PDF table extraction works best with clear borders

# Document Parser Usage Examples

## Basic Usage

### Extract text from a document

```bash
python scripts/parse_document.py /path/to/document.pdf
```

Output: JSON with text, tables, and metadata

### Human-readable output

```bash
python scripts/parse_document.py /path/to/document.docx --format text
```

## Supported Formats

### .txt files
- Direct text extraction
- No special dependencies required

### .docx files
- Extracts paragraphs and formatting
- Extracts tables with full structure
- Requires: `python-docx`

### .pdf files
- Page-by-page text extraction
- Table detection and extraction
- Requires: `PyPDF2`, `pdfplumber`

## Common Use Cases

### 1. Extract contract terms from PDF
```
User: "Extract all the key terms from this contract.pdf"
Agent: Run parse_document.py, then summarize extracted text
```

### 2. Analyze table data from Excel export
```
User: "What's the total revenue in this quarterly_report.docx?"
Agent: Parse document, locate tables, sum revenue column
```

### 3. Search across multiple documents
```
User: "Find all mentions of 'delivery date' in these 3 PDFs"
Agent: Parse each file, search extracted text
```

## Output Structure

```json
{
  "text": "Full extracted text content...",
  "tables": [
    [
      ["Header 1", "Header 2", "Header 3"],
      ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
      ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
    ]
  ],
  "metadata": {
    "format": "pdf",
    "pages": 5,
    "tables": 2
  }
}
```

## Error Handling

If dependencies are missing, the script returns:
```json
{
  "error": "python-docx not installed. Run: pip install python-docx"
}
```

Run `scripts/install_dependencies.sh` (or `.bat` on Windows) to install all required packages.

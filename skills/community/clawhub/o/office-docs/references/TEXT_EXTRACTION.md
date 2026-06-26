# Text Extraction from Office Documents

This guide covers various methods for extracting text from Microsoft Word (.docx) and WPS Office documents.

## Python Methods

### 1. Using python-docx (Recommended for .docx)

**Basic text extraction:**
```python
from docx import Document

def extract_text_docx(filepath):
    """Extract all text from a .docx file."""
    doc = Document(filepath)
    text_parts = []
    
    # Extract paragraphs
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)
    
    # Extract tables
    for table in doc.tables:
        for row in table.rows:
            row_text = []
            for cell in row.cells:
                if cell.text.strip():
                    row_text.append(cell.text)
            if row_text:
                text_parts.append(' | '.join(row_text))
    
    # Extract headers and footers
    for section in doc.sections:
        for header in section.header.paragraphs:
            if header.text.strip():
                text
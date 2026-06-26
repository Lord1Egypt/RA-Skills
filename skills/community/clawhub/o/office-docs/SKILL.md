---
name: office-docs
description: Comprehensive document processing for Microsoft Word (.docx) and WPS Office files. Use when Codex needs to work with professional documents for: (1) Creating new documents, (2) Modifying or editing content, (3) Converting between formats, (4) Extracting text and metadata, (5) Troubleshooting document issues, (6) Batch processing documents, or any other Office document tasks.
---

# Office Documents Skill

This skill provides comprehensive tools and workflows for working with Microsoft Word (.docx) and WPS Office documents. It covers creation, editing, conversion, analysis, and troubleshooting of professional documents.

## Quick Start

### Basic Operations

**Read document content:**
```python
# Use python-docx for .docx files
from docx import Document
doc = Document('document.docx')
text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
```

**Create new document:**
```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_heading('Document Title', 0)
doc.add_paragraph('This is a new paragraph.')
doc.save('new_document.docx')
```

### Common Tasks

1. **Text extraction** - See [TEXT_EXTRACTION.md](references/TEXT_EXTRACTION.md)
2. **Format conversion** - See [CONVERSION.md](references/CONVERSION.md)
3. **Document analysis** - See [ANALYSIS.md](references/ANALYSIS.md)
4. **Troubleshooting** - See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## Core Tools and Libraries

### Python Libraries

**For .docx files:**
- `python-docx` - Primary library for reading/writing .docx
- `docx2txt` - Simple text extraction
- `docxcompose` - Advanced document composition
- `docx-mailmerge` - Mail merge functionality

**For WPS files:**
- `pywps` - WPS file manipulation (when available)
- Conversion to .docx first recommended

**For format conversion:**
- `pandoc` - Universal document converter
- `libreoffice` - Office suite for conversion
- `unoconv` - Universal office converter

### Command Line Tools

**Document conversion:**
```bash
# Convert .docx to PDF
libreoffice --headless --convert-to pdf document.docx

# Convert .docx to text
pandoc document.docx -o document.txt

# Batch convert WPS to .docx
for file in *.wps; do libreoffice --headless --convert-to docx "$file"; done
```

**Document analysis:**
```bash
# Extract metadata
exiftool document.docx

# Check file integrity
file document.docx
```

## Workflows

### 1. Document Creation Workflow

When creating new documents:

1. **Choose template** - Start from template or create from scratch
2. **Add structure** - Headings, paragraphs, lists
3. **Apply formatting** - Styles, fonts, spacing
4. **Add elements** - Tables, images, hyperlinks
5. **Finalize** - Page setup, headers/footers, save

See [CREATION.md](references/CREATION.md) for detailed patterns.

### 2. Document Editing Workflow

When modifying existing documents:

1. **Backup original** - Always create backup first
2. **Analyze structure** - Understand document layout
3. **Make changes** - Edit content, update formatting
4. **Preserve formatting** - Maintain original styles
5. **Validate** - Check for corruption, save new version

See [EDITING.md](references/EDITING.md) for detailed patterns.

### 3. Conversion Workflow

When converting between formats:

1. **Identify source format** - .docx, .wps, .doc, .rtf, etc.
2. **Choose conversion tool** - Based on format and requirements
3. **Convert** - With appropriate options
4. **Verify** - Check content preservation
5. **Clean up** - Remove temporary files

See [CONVERSION.md](references/CONVERSION.md) for detailed patterns.

## Common Issues and Solutions

### 1. Corrupted Documents

**Symptoms:** Won't open, error messages, missing content

**Solutions:**
- Try opening in different application
- Use recovery mode in Word/WPS
- Extract content with `python-docx` ignoring errors
- Convert to different format and back

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md#corruption) for detailed recovery procedures.

### 2. Formatting Issues

**Symptoms:** Wrong fonts, broken layout, missing styles

**Solutions:**
- Check style definitions
- Verify font availability
- Use template-based approach
- Simplify complex formatting

### 3. Compatibility Problems

**Symptoms:** Different appearance in Word vs WPS, missing features

**Solutions:**
- Stick to common features
- Test in both applications
- Use standard formats
- Provide alternative versions

## Advanced Features

### Document Automation

**Batch processing:**
```python
import os
from docx import Document

def process_documents(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.docx'):
            doc_path = os.path.join(folder_path, filename)
            process_single_document(doc_path)
```

**Template-based generation:**
```python
from docx import Document

def generate_from_template(template_path, data):
    doc = Document(template_path)
    # Replace placeholders with data
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{ {key} }}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{{ {key} }}}}', value)
    return doc
```

### Document Analysis

**Extract statistics:**
```python
def analyze_document(doc_path):
    doc = Document(doc_path)
    stats = {
        'paragraphs': len(doc.paragraphs),
        'tables': len(doc.tables),
        'images': len(doc.inline_shapes),
        'sections': len(doc.sections),
        'styles': len(doc.styles)
    }
    return stats
```

**Check formatting consistency:**
```python
def check_formatting(doc):
    issues = []
    for i, para in enumerate(doc.paragraphs):
        if para.style.name == 'Normal' and para.text.strip():
            # Check for inconsistent formatting
            if len(para.runs) > 1:
                issues.append(f"Paragraph {i}: Multiple runs in Normal style")
    return issues
```

## Best Practices

### 1. Always Backup
```python
import shutil
import os

def backup_document(filepath):
    backup_path = filepath + '.backup'
    shutil.copy2(filepath, backup_path)
    return backup_path
```

### 2. Use Version Control
- Save incremental versions
- Use descriptive filenames
- Document changes made

### 3. Test Thoroughly
- Test in target application
- Verify all content preserved
- Check formatting integrity

### 4. Handle Errors Gracefully
```python
try:
    doc = Document(filepath)
except Exception as e:
    print(f"Error opening {filepath}: {e}")
    # Try alternative methods
    return extract_text_fallback(filepath)
```

## Reference Files

For detailed information on specific topics, consult these reference files:

- [TEXT_EXTRACTION.md](references/TEXT_EXTRACTION.md) - Text extraction methods and patterns
- [CONVERSION.md](references/CONVERSION.md) - Format conversion guides
- [ANALYSIS.md](references/ANALYSIS.md) - Document analysis techniques
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues and solutions
- [CREATION.md](references/CREATION.md) - Document creation patterns
- [EDITING.md](references/EDITING.md) - Document editing workflows
- [AUTOMATION.md](references/AUTOMATION.md) - Automation scripts and templates

## Scripts

Available scripts in the `scripts/` directory:

- `extract_text.py` - Extract text from .docx files
- `convert_format.py` - Convert between document formats
- `batch_process.py` - Process multiple documents
- `document_stats.py` - Generate document statistics
- `repair_document.py` - Attempt to repair corrupted documents

Run scripts with appropriate parameters:
```bash
python scripts/extract_text.py input.docx output.txt
```

## Getting Help

If you encounter issues not covered in this skill:

1. Check the relevant reference file
2. Search for specific error messages
3. Try alternative approaches
4. Consider converting to simpler format

Remember: When in doubt, create a backup and work on a copy.
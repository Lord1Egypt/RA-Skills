---
name: markitdown
description: Convert various document formats (PDF, Word, PowerPoint, Excel, images, audio, HTML, etc.) to Markdown using Microsoft's markitdown tool. Supports OCR, audio transcription, and YouTube video extraction.
triggers:
  - convert pdf to markdown
  - convert word to markdown
  - convert document
  - extract text from pdf
  - ocr image
  - transcribe audio
  - markitdown
  - 文档转markdown
  - pdf转文本
---

# MarkItDown

Microsoft's lightweight Python utility for converting various files to Markdown for use with LLMs and related text analysis pipelines.

## Installation

### Prerequisites
- Python 3.10+
- Java 11+ (for some converters)

### Install via pipx (recommended)
```bash
pipx install 'markitdown[all]'
```

### Install via pip
```bash
pip install 'markitdown[all]'
```

### Minimal install (specific formats only)
```bash
pip install 'markitdown[pdf,docx,pptx]'
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | .pdf | Preserves structure, tables, links |
| Word | .docx | Headings, lists, tables |
| PowerPoint | .pptx | Slides to Markdown |
| Excel | .xlsx, .xls | Table data |
| Images | .png, .jpg, etc. | EXIF metadata + OCR |
| Audio | .wav, .mp3 | Speech transcription |
| HTML | .html, .htm | Web content |
| YouTube | URL | Video transcription |
| ZIP | .zip | Iterates over contents |
| EPub | .epub | E-books |
| Text | .csv, .json, .xml | Text-based formats |

## CLI Usage

### Basic Conversion
```bash
# PDF to Markdown
markitdown document.pdf > output.md

# Word to Markdown
markitdown document.docx -o output.md

# PowerPoint to Markdown
markitdown presentation.pptx -o output.md
```

### Pipe Input
```bash
cat document.pdf | markitdown
```

### Image OCR
```bash
markitdown screenshot.png -o text.md
```

### YouTube Video
```bash
markitdown "https://youtube.com/watch?v=..." -o transcript.md
```

## Python API Usage

```python
from markitdown import MarkItDown

# Initialize
md = MarkItDown()

# Convert file
result = md.convert("document.pdf")
print(result.text_content)

# Convert from stream
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f)
    print(result.text_content)
```

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file | `-o output.md` |
| `--format` | Output format (default: markdown) | `--format json` |
| `--pages` | Specific pages | `--pages "1,3,5-7"` |
| `--image-output` | Image handling | `--image-output external` |
| `--quiet` | Suppress output | `--quiet` |

## MCP Server

MarkItDown provides an MCP (Model Context Protocol) server for integration with LLM applications:

```bash
pip install markitdown-mcp
```

## Best Practices

1. **Batch processing**: Process multiple files in one call for efficiency
2. **Format selection**: Use minimal install if only specific formats needed
3. **OCR quality**: Ensure 300 DPI+ for scanned documents
4. **Output review**: Always verify Markdown output for complex documents

## Troubleshooting

### Java not found
Install Java 11+:
```bash
# macOS
brew install openjdk@17

# Ubuntu
sudo apt install openjdk-17-jdk
```

### Permission denied
Use pipx or virtual environment:
```bash
python3 -m venv ~/.venvs/markitdown
source ~/.venvs/markitdown/bin/activate
pip install 'markitdown[all]'
```

## References

- GitHub: https://github.com/microsoft/markitdown
- PyPI: https://pypi.org/project/markitdown/
- MCP Server: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp

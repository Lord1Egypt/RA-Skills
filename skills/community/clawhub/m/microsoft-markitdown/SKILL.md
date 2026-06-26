---
name: microsoft-markitdown
description: Use MarkItDown to convert various files (PDF, Word, Excel, PPT, images, audio, HTML, CSV, JSON, etc.) to Markdown format for LLM processing and text analysis. Also supports content extraction from ZIP archives, YouTube videos, and EPUB e-books.
---

# Microsoft MarkItDown

A Python tool for converting various file types to Markdown format.

## Use Cases

Use this skill when users mention scenarios like "convert file to Markdown," "extract document content," "file to Markdown," or "extract text from PDF/Word/Excel."

## Installation

```bash
pip install 'markitdown[all]'
```

Optional dependency group installations (to save space):

| Tag | Description |
|------|-------------|
| `[pptx]` | PowerPoint files |
| `[docx]` | Word files |
| `[xlsx]` | Excel files |
| `[xls]` | Legacy Excel files |
| `[pdf]` | PDF files |
| `[outlook]` | Outlook emails |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[audio-transcription]` | Audio transcription (wav/mp3) |
| `[youtube-transcription]` | YouTube video transcription |

## Command Line Usage

```bash
# Basic usage: output to stdout
markitdown path-to-file.pdf > document.md

# Specify output file
markitdown path-to-file.pdf -o document.md

# Pipe input
cat path-to-file.pdf | markitdown

# Use Azure Document Intelligence
markitdown path-to-file.pdf -o document.md -d -e "<document_intelligence_endpoint>"

# List installed plugins
markitdown --list-plugins

# Enable plugins
markitdown --use-plugins path-to-file.pdf
```

## Python API Usage

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # True to enable plugins
result = md.convert("test.xlsx")
print(result.text_content)
```

### With LLM Image Description (Only supports pptx and image files)

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="optional custom prompt")
result = md.convert("example.jpg")
print(result.text_content)
```

### With Azure Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

### Using markitdown-ocr Plugin (OCR for Images Embedded in PDF/DOCX/PPTX/XLSX)

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = md.convert("document_with_images.pdf")
print(result.text_content)
```

## Supported Formats Overview

| Format | Extensions | Dependency Tag |
|--------|------------|----------------|
| PDF | .pdf | `[pdf]` |
| PowerPoint | .pptx | `[pptx]` |
| Word | .docx | `[docx]` |
| Excel | .xlsx / .xls | `[xlsx]` / `[xls]` |
| Images | .jpg/.png etc. | Built-in (OCR requires `[audio-transcription]` + LLM) |
| Audio | .mp3/.wav | `[audio-transcription]` |
| HTML | .html | Built-in |
| CSV/JSON/XML | .csv/.json/.xml | Built-in |
| ZIP | .zip | Built-in (iterates contents) |
| YouTube | URL | `[youtube-transcription]` |
| EPUB | .epub | Built-in |
| Outlook | .msg | `[outlook]` |

## Agent Execution Workflow

When a user requests file conversion:

1. **Confirm Input File**: Obtain the file path.
2. **Install Dependencies**: Check if markitdown is installed and suggest installing corresponding dependencies based on the file type if needed.
3. **Execute Conversion**:
   - Command line: `markitdown <file> -o <output.md>`
   - Or Python API.
4. **Return Result**: Output the Markdown content or the saved file path.

## Notes

- Python 3.10+ is required.
- Using a virtual environment is recommended to avoid dependency conflicts.
- The OCR plugin requires an LLM API Key (e.g., OpenAI).
- Azure Document Intelligence requires an Azure account configuration.
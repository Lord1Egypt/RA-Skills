---
name: md-2-word
description: Convert Markdown files to formatted Word documents (.docx). Use when the user asks to convert, export, or save a Markdown file as Word/DOCX format. Triggers on phrases like "convert md to word", "export to docx", "save as word document", "markdown转word", "转成word文档".
---

# Markdown to Word Converter

Convert Markdown files to professionally formatted Word documents (.docx).

## Quick Start

```bash
python scripts/md_to_word.py <input.md> [output.docx]
```

**Parameters:**
- `input.md` - Path to the source Markdown file (required)
- `output.docx` - Path for the output Word file (optional, defaults to input name with .docx extension)

**Example:**
```bash
python scripts/md_to_word.py report.md report.docx
```

## Supported Markdown Features

| Feature | Format |
|---------|--------|
| Headers (#, ##, ###) | 18pt/14pt/12pt bold, 微软雅黑 |
| Bold (**text**) | Bold formatting |
| Tables | Bordered tables with blue header background |
| Bullet lists (-, *) | Bullet points |
| Numbered lists (1., 2.) | Numbered items |
| Blockquotes (>) | Italic, indented text |
| Horizontal rules (---) | Paragraph spacing |

## Usage in Conversation

When user wants to convert a Markdown file:

1. **Identify the file**: Confirm the Markdown file path
2. **Run the conversion**: Execute the script
3. **Confirm output**: Report file location and size

**Example prompt handling:**
- "Convert this md file to word" → Run with provided file path
- "Export as docx" → Convert current/mentioned file
- "把调研提纲转成word" → Convert the mentioned file

## Script Location

The conversion script is located at:
```
scripts/md_to_word.py
```

## Requirements

- Python 3.6+
- python-docx library

Install if needed:
```bash
pip install python-docx
```

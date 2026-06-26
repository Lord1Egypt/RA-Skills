---
name: md-to-docx
description: >
  Convert Markdown files to formatted Word (.docx) documents with automatic template
  style detection. Use this skill whenever the user mentions converting Markdown to Word,
  exporting to .docx, generating a Word document from .md files, applying a Word template
  to Markdown content, or writing a book chapter to Word format. Also use when the user
  needs to handle Mermaid diagrams in Word documents, or wants Chinese typesetting
  conventions (宋体/黑体, 五号字, 首行缩进) applied to their output. Triggers on phrases
  like "转成 word", "导出 docx", "生成 Word 文档", "用模板排版", "Markdown to Word",
  "book to Word", "chapter to docx", or any request involving .md → .docx conversion.
---

# Markdown to Word (.docx) Converter

Convert Markdown files to professionally formatted Word documents, with automatic template style extraction and Mermaid diagram rendering.

## How It Works

The bundled script (`scripts/md_to_docx.py`) handles the entire conversion:

1. **Parse Markdown** into structured blocks (headings, body, lists, tables, code, quotes)
2. **Extract styles** from an optional Word template (.doc or .docx) — font, size, alignment, spacing
3. **Apply formatting** to each block, preserving inline Markdown (bold, italic, code, strikethrough)
4. **Render Mermaid diagrams** to PNG via `mmdc` (mermaid-cli) and embed them as images
5. **Output** a ready-to-use .docx file

## Dependencies

The script requires:

- **python-docx**: `pip install python-docx`
- **mmdc** (for Mermaid rendering): `npm install -g @mermaid-js/mermaid-cli`
- **Chrome or Chromium**: must be installed locally (auto-detected on macOS/Windows/Linux)

On macOS, `.doc` templates are converted via the built-in `textutil`. On Linux, LibreOffice is used as fallback.

## Usage

### Basic conversion (default Chinese typesetting)

```bash
python3 scripts/md_to_docx.py input.md -o output.docx
```

### With template (auto-extract formatting)

```bash
python3 scripts/md_to_docx.py input.md -o output.docx -t template.doc
```

### When Invoked as a Skill

When the user asks to convert a Markdown file to Word:

1. **Identify the input file** — the user will typically specify a `.md` file path
2. **Check for a template** — ask if they have a `.doc`/`.docx` template, or check if one exists in common locations (`docs/`, `templates/`)
3. **Ensure dependencies** are installed:
   ```bash
   pip3 install python-docx
   npm list -g @mermaid-js/mermaid-cli 2>/dev/null || npm install -g @mermaid-js/mermaid-cli
   ```
4. **Run the script** from the skill's `scripts/` directory:
   ```bash
   python3 <skill-path>/scripts/md_to_docx.py <input.md> -o <output.docx> [-t <template.doc>]
   ```
5. **Report results** — tell the user the output path and whether all Mermaid diagrams rendered successfully

## Template Format Detection

When a template is provided, the script analyzes it automatically:

- **Title levels** are identified by font size and alignment (largest centered = chapter title, etc.)
- **Body text** is identified by paragraphs with first-line indentation
- **Page setup** (margins, paper size) is copied from the template
- **Chinese font pairing** is preserved (e.g., Times New Roman ↔ 宋体, Arial ↔ 黑体)

If no template is provided, these defaults are used (Chinese publishing standard):

| Element | Font | Size | Alignment |
|---------|------|------|-----------|
| Chapter title (h1) | 黑体 | 18pt | Center |
| Section title (h2) | 黑体 | 16pt | Center |
| Subsection (h3) | 黑体 | 14pt | Left |
| Body text | 宋体 | 10.5pt (五号) | Justify, 2-char indent |
| Code | Consolas | 9pt | Left |
| Quote | 楷体 | 10.5pt | Left indent, italic |

## Supported Markdown Features

- **Headings**: h1–h6 (h1 = chapter, h2 = section, h3 = subsection, h4+ = sub-subsection)
- **Body text** with inline: **bold**, *italic*, `code`, ~~strikethrough~~, ***bold italic***
- **Bullet lists** (`-` or `*`) and **ordered lists** (`1.`)
- **Tables** with header detection
- **Code blocks** with language label
- **Mermaid diagrams** rendered to embedded PNG images
- **Block quotes** and **horizontal rules**

## Mermaid Diagram Handling

Mermaid code blocks are rendered to PNG via `mmdc` using the local Chrome browser. If rendering fails (e.g., Chrome not found, syntax error), the diagram falls back to a code block display.

Common Mermaid compatibility fixes are applied automatically:
- `subgraph` names containing colons are quoted
- Parentheses in subgraph names are escaped

## Cross-Platform Notes

- **macOS**: Chrome auto-detected at `/Applications/Google Chrome.app/...`
- **Windows**: Checks `Program Files` and `LocalAppData`
- **Linux**: Checks `/usr/bin/google-chrome`, `/usr/bin/chromium`, `/snap/bin/chromium`
- **`.doc` conversion**: Uses `textutil` on macOS, `libreoffice` on Linux

## Limitations

- No support for footnotes, images, or links (Markdown image URLs are not fetched)
- Math equations (LaTeX) are preserved as plain text
- Nested lists deeper than one level are flattened
- Template detection works best with templates that have clear formatting differentiation between headings and body text

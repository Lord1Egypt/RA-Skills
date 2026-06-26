---
name: md2pdf
description: Convert Markdown files to beautifully formatted PDFs using Pandoc and Typst. Supports headings, tables, code blocks, links, emojis, and GitHub-style formatting. Output lands next to the source file.
---

# md2pdf

Converts Markdown to PDF with professional formatting.

## Requirements

- **Pandoc** (v3.2+): `brew install pandoc`
- **Typst** (v0.12+): `brew install typst`

## Usage

```bash
bash ~/.openclaw/workspace/skills/md2pdf/scripts/md2pdf.sh "/path/to/file.md"
```

The PDF is saved in the same directory as the source MD file.

## Features

- GitHub-style headings with horizontal rules
- Tables, bullet lists, numbered lists
- Code blocks with syntax highlighting (monospace, grey background)
- Inline code formatting
- Clickable links (blue, underlined)
- Emoji support
- German language optimized (hyphenation)
- Clean typography (Helvetica Neue / Arial)

## Examples

```bash
# Single file
bash ~/.openclaw/workspace/skills/md2pdf/scripts/md2pdf.sh report.md
# → creates report.pdf in same folder

# From any agent workspace
bash ~/.openclaw/workspace/skills/md2pdf/scripts/md2pdf.sh /full/path/to/notes.md
```

## TOOLS.md Entry

Add this to your agent's TOOLS.md:

```markdown
## PDF erstellen (md2pdf)
- Markdown zu PDF: `bash ~/.openclaw/workspace/skills/md2pdf/scripts/md2pdf.sh "/pfad/zur/datei.md"`
- Das PDF wird im gleichen Ordner wie das MD abgelegt.
```

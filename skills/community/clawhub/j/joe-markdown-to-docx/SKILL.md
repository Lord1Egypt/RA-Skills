---
name: joe-markdown-to-docx
description: Convert Markdown documents to Word DOCX format with full support for tables, images, code blocks, and formatting. Use when: (1) User asks to convert .md files to .docx or Word format, (2) User needs to generate Word documents from Markdown content, (3) User wants to create professional documents with tables and images from Markdown source. Supports GFM (GitHub Flavored Markdown), local/remote images, table alignment, code syntax highlighting, and preserves all formatting.
author: Joe Cao
---

# Markdown to DOCX Converter

Convert Markdown documents to professional Word DOCX format with full formatting preservation.

## Features

- ✅ **Complete Markdown support**: Headers, paragraphs, lists, code blocks
- ✅ **Tables**: Full table support with alignment (left/center/right)
- ✅ **Images**: Local files, remote URLs, and data URLs
- ✅ **Text formatting**: Bold, italic, inline code, links
- ✅ **Code blocks**: Syntax-highlighted with borders and background
- ✅ **GFM support**: GitHub Flavored Markdown extensions

## Installation

After installing this skill, run:

```bash
cd ~/.openclaw/workspace/skills/markdown-to-docx
npm install
```

All dependencies are pure JavaScript and work on Windows, macOS, and Linux.

## Usage

Convert a Markdown file to DOCX:

```bash
node scripts/convert.js <input.md> [output.docx]
```

### Examples

```bash
# Convert with auto-generated output name
node scripts/convert.js document.md

# Specify output filename
node scripts/convert.js document.md report.docx

# Convert from current directory
node scripts/convert.js ./README.md ./README.docx
```

## Supported Markdown Features

### Text Formatting
- **Bold**: `**text**` or `__text__`
- *Italic*: `*text*` or `_text_`
- `Inline code`: `` `code` ``
- [Links](url): `[text](url)`

### Tables
```markdown
| Header 1 | Header 2 | Header 3 |
|:---------|:--------:|---------:|
| Left     | Center   | Right    |
```

- Alignment: `:---` (left), `:---:` (center), `---:` (right)
- Header row with gray background
- Bordered cells with padding

### Images
```markdown
![Alt text](path/to/image.png)
![Remote](https://example.com/image.jpg)
```

- Local images: Relative paths from Markdown file location
- Remote images: HTTP/HTTPS URLs (automatically downloaded)
- Data URLs: Base64-encoded images
- Auto-centered with appropriate sizing

### Code Blocks
````markdown
```javascript
function hello() {
  console.log("Hello!");
}
```
````

- Monospace font (Consolas)
- Light gray background
- Border styling

## Output Format

Generated DOCX files include:
- 1-inch margins on all sides
- Professional spacing and alignment
- Consistent styling throughout
- Editable in Microsoft Word, Google Docs, LibreOffice

## Error Handling

- Missing images: Shows placeholder text instead of breaking
- Network errors: Graceful fallback with error message
- Invalid Markdown: Skips unsupported elements

## Dependencies

Automatically installed via `npm install`:
- `docx`: Word document generation
- `unified`, `remark-parse`, `remark-gfm`: Markdown parsing
- `node-fetch`: Remote image downloading

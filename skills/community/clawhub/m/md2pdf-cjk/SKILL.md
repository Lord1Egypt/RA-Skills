---
name: md2pdf-cjk
description: "Markdown to PDF converter with CJK (Chinese/Japanese/Korean) support. Uses WeasyPrint + Noto CJK fonts for proper rendering. Features: emoji replacement, custom CSS styling, code blocks, tables. Triggers: generate PDF, convert PDF, markdown to PDF, md2pdf."
---

# Markdown to PDF (CJK)

Convert Markdown files to well-formatted PDF with full CJK (Chinese/Japanese/Korean) support, code blocks, and tables.

## Toolchain

- **Rendering engine**: WeasyPrint (pre-installed, `/usr/local/bin/weasyprint`)
- **Fonts**: Noto Sans CJK SC / Noto Serif CJK SC (system-installed)
- **Pipeline**: Markdown → HTML (emoji replacement) → WeasyPrint → PDF

## Steps

### 1. Emoji Processing

WeasyPrint does not render emoji characters. Replace them with text labels:

```python
emoji_map = {
    '🦞': '[Lobster]', '🌅': '[Morning]', '🌙': '[Moon]', '🏛': '[Architecture]',
    '🔧': '[Tool]', '🔄': '[Restart]', '📰': '[Report]', '💪': '[Strong]',
    '⚡': '[Lightning]', '⏰': '[Alarm]', '👆': '[Up]', '⬆️': '[Up]',
    '🌟': '[Star]', '👇': '[Down]', '✅': '[Done]', '📊': '[Chart]',
    '🎯': '[Target]', '💡': '[Idea]', '🧰': '[Toolbox]', '🤖': '[AI]',
    '🏗️': '[Build]', '📅': '[Calendar]', '🧘': '[Meditation]', '📖': '[Read]',
    '📝': '[Note]', '🏃': '[Run]', '⭐': '[Fav]', '📬': '[Mail]',
    '🌐': '[Web]', '🐙': '[GitHub]', '💬': '[Chat]', '▪': '·',
    '❌': '[X]', '⚠️': '[!]', '📌': '[PIN]', '🔔': '[Bell]',
    '🤔': '[Think]', '😂': '[Laugh]', '🔒': '[Lock]', '📁': '[Folder]',
    '💰': '[Money]', '👨‍👧‍👦': '[Family]', '😴': '[Sleep]', '👶': '[Baby]',
    '1️⃣': '1.', '2️⃣': '2.', '3️⃣': '3.', '4️⃣': '4.', '5️⃣': '5.',
}
```

> For emoji not in the map, strip variant selectors (`\ufe0f`) and replace with `[?]`. Preserve CJK punctuation marks (·…——''""etc.).

### 2. Markdown → HTML Conversion

Lightweight conversion using Python regex (no extra dependencies):

```python
import re
html = md_content
html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
html = re.sub(r'^---$', r'<hr/>', html, flags=re.MULTILINE)
html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
# Paragraphs
html = re.sub(r'\n\n', r'</p><p>', html)
html = '<p>' + html + '</p>'
# Clean empty tags
html = re.sub(r'<p>\s*</p>', '', html)
html = re.sub(r'<p>\s*(<h[123]>.*?</h[123]>)\s*</p>', r'\1', html, flags=re.DOTALL)
html = re.sub(r'<p>\s*(<hr/>)\s*</p>', r'\1', html)
html = re.sub(r'<p>\s*(<blockquote>.*?</blockquote>)\s*</p>', r'\1', html, flags=re.DOTALL)
```

### 3. HTML Template

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: A4; margin: 2cm 2.5cm 2cm 2.5cm; }
body {
    font-family: "Noto Sans CJK SC", "Noto Serif CJK SC", sans-serif;
    font-size: 11pt; line-height: 1.8; color: #333;
    max-width: 100%; word-wrap: break-word;
}
h1 { font-size: 20pt; color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 8px; margin-top: 30px; }
h2 { font-size: 15pt; color: #333; margin-top: 25px; border-left: 4px solid #d32f2f; padding-left: 10px; }
h3 { font-size: 13pt; color: #555; margin-top: 20px; }
blockquote { border-left: 3px solid #ccc; padding-left: 15px; color: #666; margin: 15px 0; font-style: italic; }
code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 10pt; }
pre { background: #f8f8f8; padding: 12px; border-radius: 5px; font-size: 9.5pt; line-height: 1.6; }
pre code { background: none; padding: 0; }
strong { color: #d32f2f; }
hr { border: none; border-top: 1px solid #ddd; margin: 25px 0; }
li { margin: 5px 0; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
th { background: #f5f5f5; font-weight: bold; }
</style>
</head>
<body>{{HTML_CONTENT}}</body>
</html>
```

### 4. Generate PDF

```bash
weasyprint /tmp/input.html /tmp/output.pdf
```

## One-line Script

All steps are wrapped into a single script:

```bash
#!/bin/bash
# Usage: md2pdf.sh input.md [output.pdf]
# Markdown → PDF (weasyprint + CJK + emoji replacement)
INPUT="${1:-/dev/stdin}"
OUTPUT="${2:-/tmp/output.pdf}"
python3 /path/to/md2pdf.py "$INPUT" "$OUTPUT"
```

## Important Notes

- **Do NOT use pandoc + xelatex**: Emoji renders as blank, and compilation is slow
- **Do NOT use pandoc + wkhtmltopdf**: Not installed by default
- **Always use WeasyPrint**: The only solution that supports CJK + emoji replacement
- **Output path**: Always use absolute paths under `/tmp/`
- **Pre-send check**: Verify PDF file exists and is > 10KB before sending

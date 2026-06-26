---
name: markdown2doc
description: Lightweight document utility designed to convert Markdown (MD) files to PDF or DOCX format. Supports multiple template themes. Preserves document structure, heading hierarchy, embedded images. Requires no external dependencies.
homepage: https://lab.hjcloud.com/llmdoc
metadata: {"openclaw":{"emoji":"📑","requires":{"bins":["node"]}}}
---
# markdown2doc

Document conversion assistant that automatically converts Markdown (MD) files to PDF or DOCX format, saving output to the same directory as the source file.

## Quick Start

```bash
# Convert markdown to PDF
node scripts/markdown2doc.js convert <file_path> pdf        # Output: same_name.pdf
# Convert markdown to WORD
node scripts/markdown2doc.js convert <file_path> docx       # Output: same_name.docx
# List available themes
node scripts/markdown2doc.js list-themes
# Convert markdown to WORD with a theme
node scripts/markdown2doc.js convert <file_path> docx --theme tech
```

## Capabilities

- Supported output formats: PDF, DOCX
- Multiple template themes available (use `list-themes` to see all options)
- Preserves markdown structure, headings, lists, tables, and code blocks
- Generates a navigable table of contents with heading hierarchy
- Embeds images referenced in the markdown into the output document, including both local images
- No API Key or account required, minimal external dependencies
- Output file is saved to the same directory as the source markdown file

> **Note on local images:** To ensure local images are correctly embedded in the output document, image files must be located in the **same directory as the markdown file, or in a subdirectory** of it (e.g., `./images/photo.png`). Images referenced via absolute paths or paths pointing outside the markdown file's directory will be skipped for security reasons.

## When to Use

- User requests to "export", "convert", "generate PDF", "generate DOCX", "generate doc", "generate Word document" from markdown
- User provides a markdown file path and asks to convert it to PDF, DOCX, or doc
- User needs a printable or shareable version of a markdown document
- User asks to apply a specific style or theme when converting to DOCX
- User asks to list available template themes or wants to know what template themes are supported

## Workflow

### convert — Convert Markdown File

1. Read markdown file content from specified path
2. Scan markdown for local image references and collect image files
3. Send markdown content to conversion service
4. Receive converted file stream (PDF or DOCX)
5. Save output file to source file's parent directory

## Data & Privacy

- `convert` sends **both the markdown file content and all locally referenced image files** to the docchain cloud service (`lab.hjcloud.com`) for processing.
- Any local image path referenced in the markdown (e.g., `![](./images/photo.png)`) will be read from disk and uploaded along with the markdown content.
- All transfers use HTTPS encryption.
- **Users are responsible for ensuring that neither the markdown content nor any referenced image files contain sensitive, confidential, or proprietary information.** Use of this skill constitutes acceptance of the data transmission described above.
- Service endpoint: https://lab.hjcloud.com/llmdoc

## Feedback & Support

For conversion errors, format issues, or other problems, please submit an issue on GitHub:
https://github.com/wct-lab/docchain-skills
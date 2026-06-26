# Pandoc Format Reference

## Common Extension Mapping

| Extension | Pandoc format |
|---|---|
| `.md`, `.markdown`, `.mkd` | `markdown` |
| `.html`, `.htm` | `html` |
| `.docx` | `docx` |
| `.odt` | `odt` |
| `.rtf` | `rtf` |
| `.epub` | `epub` |
| `.tex`, `.latex` | `latex` |
| `.typ` | `typst` |
| `.rst` | `rst` |
| `.adoc`, `.asciidoc` | `asciidoc` |
| `.org` | `org` |
| `.ipynb` | `ipynb` |
| `.txt` | `markdown` by default |
| `.pdf` | output inferred from `-o output.pdf` |

## High-Value Conversion Pairs

- Markdown → DOCX: reports, specs, product docs.
- Markdown → PDF: papers, contracts, polished reports; requires a PDF engine.
- Markdown → HTML: web preview, self-contained sharing, print-to-PDF fallback.
- Markdown → EPUB: ebooks and long-form documentation.
- DOCX → Markdown: move Word documents into version control; use `--extract-media` for images.
- HTML → Markdown: import web documentation or rendered docs.
- ipynb → HTML/PDF/Markdown: notebook publishing.

## PDF Notes

Pandoc creates PDF through an external engine. Common choices:

- `xelatex`: best default for Chinese and Unicode-heavy documents.
- `lualatex`: good Unicode support and modern TeX workflows.
- `pdflatex`: common, but weak for Chinese/Unicode unless configured.
- `tectonic`: self-contained TeX engine when installed.
- HTML print workflow: convert to standalone HTML, then print to PDF if LaTeX is unavailable.

## Discover Installed Formats

Use Pandoc directly when exact format support matters:

```bash
pandoc --list-input-formats
pandoc --list-output-formats
```

# pandoc-docx

> 🔄 Bidirectional conversion between Word (.docx) and Markdown using pandoc

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/openclaw/workspace/tree/main/skills/pandoc-docx)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange)](https://openclaw.ai)

## Features

- ✅ **Read Word** (.docx) → Markdown
- ✅ **Write Word** (.docx) ← Markdown
- ✅ **Format conversion** (.docx ↔ .md ↔ .pdf ↔ .txt ↔ .html)
- ✅ **Batch processing**
- ✅ **Image extraction**
- ✅ **Format preservation** (headings, bold, lists, tables, code)

## Quick Start

### Installation

```bash
# Install pandoc (required)
sudo apt install pandoc        # Linux
brew install pandoc            # macOS

# Optional: Install additional tools
sudo apt install libreoffice   # .doc support
sudo apt install poppler-utils # PDF reading
```

### Usage

```bash
# Read Word document
./scripts/doc-read.sh ~/document.docx

# Create Word document
echo "# Title" | ./scripts/doc-write.sh ~/output.docx -

# Convert format
./scripts/doc-convert.sh ~/input.docx -o ~/output.md

# Extract images
./scripts/doc-convert.sh ~/input.docx -o ~/output.md --extract-media=./images

# Check dependencies
./scripts/check-deps.sh
```

## Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `doc-read.sh` | Read documents | `./doc-read.sh file.docx` |
| `doc-write.sh` | Write documents | `./doc-write.sh out.docx in.md` |
| `doc-convert.sh` | Convert formats | `./doc-convert.sh in.docx -o out.md` |
| `doc-edit.sh` | Edit documents | `./doc-edit.sh file.docx append '## New'` |
| `check-deps.sh` | Check dependencies | `./check-deps.sh` |

## Supported Formats

### Input
- ✅ .docx (Word 2007+)
- ⚠️ .doc (Word 97-2003, requires libreoffice)
- ✅ .md / .markdown
- ✅ .txt
- ⚠️ .pdf (read-only, requires pdftotext)
- ✅ .html

### Output
- ✅ .docx
- ✅ .md
- ✅ .pdf (requires texlive)
- ✅ .txt
- ✅ .html
- ✅ .epub

## Examples

### Read and analyze Word document

```bash
# Convert to Markdown
./scripts/doc-read.sh ~/report.docx > report.md

# View content
cat report.md
```

### Create Word from Markdown

```bash
# Create from stdin
echo "# Title

This is content." | ./scripts/doc-write.sh ~/output.docx -

# Create from file
./scripts/doc-write.sh ~/output.docx ~/input.md
```

### Batch conversion

```bash
# Convert all Word files to Markdown
for f in *.docx; do
    ./scripts/doc-convert.sh "$f" -o "${f%.docx}.md"
done
```

### Edit existing document

```bash
# Append content
./scripts/doc-edit.sh ~/report.docx append "## New Section

New content here."

# Replace text
./scripts/doc-edit.sh ~/report.docx replace "old text" "new text"
```

## Dependencies

### Required

| Tool | Install (Linux) | Install (macOS) |
|------|----------------|----------------|
| pandoc | `sudo apt install pandoc` | `brew install pandoc` |

### Optional

| Tool | Purpose | Install (Linux) | Install (macOS) |
|------|---------|----------------|----------------|
| libreoffice | .doc support | `sudo apt install libreoffice` | `brew install --cask libreoffice` |
| poppler-utils | PDF reading | `sudo apt install poppler-utils` | `brew install poppler` |
| texlive | PDF generation | `sudo apt install texlive` | `brew install --cask mactex` |

## Advanced Options

### Use reference document (preserve styles)

```bash
./scripts/doc-convert.sh input.md -o output.docx \
    --reference-doc=template.docx
```

### Extract images

```bash
./scripts/doc-convert.sh input.docx -o output.md \
    --extract-media=./images
```

### Text wrapping modes

```bash
# Preserve original line breaks
./scripts/doc-convert.sh input.docx -o output.md --wrap=preserve

# Auto wrap
./scripts/doc-convert.sh input.docx -o output.md --wrap=auto

# No wrapping
./scripts/doc-convert.sh input.docx -o output.md --wrap=none
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

**Cyber** 🌟

## Version

1.0.0 (2026-03-21)

---
name: md-to-pptx
description: |
  Convert Markdown files to PowerPoint (PPTX) format. Automatically detects slide separators (---) 
  and converts them into presentation slides. By default, saves output to the active Obsidian vault 
  (~/obsidian-360/工作知识库). 
  
  Use when: (1) User asks to convert a .md file to .pptx, (2) User says "生成PPT" or "转成PPT", 
  (3) User needs presentation format output from markdown content, (4) User explicitly requests 
  pptx/powerpoint conversion.
---

# Markdown to PowerPoint Converter

Convert Markdown files with slide separators into PowerPoint presentations.

## Default Behavior

- **Input**: Markdown file with `---` slide separators
- **Output**: PPTX file saved to **Obsidian vault** (`~/obsidian-360/工作知识库/`)
- **Fallback**: If Obsidian vault unavailable, saves to same directory as input

## Usage

### Basic conversion
```bash
python3 scripts/md2pptx.py input.md
# Output: ~/obsidian-360/工作知识库/input.pptx
```

### Specify output location
```bash
python3 scripts/md2pptx.py input.md /path/to/output.pptx
```

## Requirements

Install one of the following for best results:

**Option 1: LibreOffice (recommended)**
```bash
brew install --cask libreoffice
```

**Option 2: Pandoc**
```bash
brew install pandoc
```

## Markdown Format for Slides

Use `---` to separate slides:

```markdown
# Title Slide

Welcome to the presentation

---

# Slide 2

Content here

---

# Slide 3

More content
```

## Obsidian Vault Path

The default output location is read from:
`~/Library/Application Support/obsidian/obsidian.json`

Current vault: `~/obsidian-360/工作知识库/`

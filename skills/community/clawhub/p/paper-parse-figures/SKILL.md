---
name: paper-parse
description: Parse academic PDF papers into markdown with figure extraction.
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["uv"] },
      },
  }
---

# Paper Parse

Parse academic PDF papers into structured markdown with figure extraction using PyMuPDF.

## Usage

```bash
uv run {baseDir}/scripts/parse_paper.py --pdf /path/to/paper.pdf [--output-dir ./output]
```

## Output

The tool generates:

- `{paper_name}_content.md` - Full paper content in markdown
- `{paper_name}_parsed.json` - Structured metadata including:
  - Paper title
  - Number of pages
  - Extracted figures with captions and paths
- `cover_title_authors.png` - First-page snapshot focused on title + authors region
- `figures/` - Directory containing high-resolution figure screenshots

## Example

```bash
uv run scripts/parse_paper.py --pdf ~/papers/my-paper.pdf --output-dir ./parsed
```

Output structure:
```
./parsed/
├── my-paper_content.md
├── my-paper_parsed.json
└── figures/
    ├── figure_1.png
    ├── figure_2.png
    └── ...
```

## Dependencies

- PyMuPDF (fitz) - PDF parsing and rendering
- pymupdf4llm - Markdown conversion

These are automatically managed by uv via the inline script metadata.

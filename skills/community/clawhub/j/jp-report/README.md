# jp-report

A skill that generates formal Japanese corporate documents (日本企業向け正式報告書) from source material in any language, producing paginated A4 HTML and PDF output.

## Example Output

> **NexaCloud 事業・セキュリティ統合報告書 FY2025 Q3** — see [`examples/`](./examples/)

The output follows Japanese corporate document conventions: 明朝体 serif typography, navy/white color scheme, structured chapter numbering (第１章…), and a repeating footer on every page.

## What It Does

Given source material (markdown, prose, bullet points — any language), the skill will:

1. Map content to 4–6 chapters
2. Translate everything into formal written Japanese (書き言葉・敬体)
3. Plan pagination so cover and TOC each occupy exactly one A4 page
4. Generate a self-contained HTML file using the built-in design system
5. Export a PDF via headless Chrome

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- macOS with Google Chrome installed (for PDF export)
- Python 3 (standard library only)

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/jp-report.git

# Symlink into Claude Code's skills directory
ln -s "$(pwd)/jp-report" ~/.claude/skills/jp-report
```

Restart Claude Code, then verify with `/` — `jp-report` should appear in the command list.

## Usage

```
/jp-report
```

The skill will ask for:

| Input | Description | Default |
|-------|-------------|---------|
| Source material | File path or pasted content | — |
| Document purpose | e.g. security overview, product explanation | — |
| Japanese title + English subtitle | Shown on cover page | — |
| Classification level | 社外秘 / 部外秘 / 社内限り | 社外秘 |
| Output folder | Where to write `.html` and `.pdf` | — |
| Revision number | Shown in footer | Rev. 1.0 |

You can also pass the source file directly:

```
/jp-report path/to/source.md
```

## File Structure

```
jp-report/
├── SKILL.md                  # Claude Code skill entry point
├── docs/
│   ├── design-rules.md       # Color palette, typography, CSS, height reference table
│   └── components.md         # HTML templates for every component type
├── scripts/
│   └── generate_pdf.py       # Headless Chrome PDF export (handles path encoding)
└── examples/
    └── NexaCloud_...html      # Sample output document
```

### Key design decisions

**`docs/design-rules.md`** contains the complete CSS that must be embedded verbatim in every generated HTML file, plus a content-height reference table used to plan pagination before writing any HTML.

**`docs/components.md`** provides copy-paste HTML templates for each component:

| Component | Use case |
|-----------|----------|
| `dl.def` | Principles, definitions |
| `table.t` | Data and feature tables |
| `.arch` | Layered architecture diagrams |
| `ul.bul` | Bullet lists |
| `.notice` | Callout / highlight boxes |

**`scripts/generate_pdf.py`** wraps headless Chrome to avoid manual URL-encoding of paths with Japanese characters or spaces.

## Design System

- **Body font**: Hiragino Mincho ProN / Yu Mincho (明朝体)
- **UI font**: Hiragino Kaku Gothic ProN / Yu Gothic (ゴシック体)
- **Page size**: 794 × 1122 px on screen · 210 × 297 mm in print
- **Page breaks**: each `.page` div uses `break-after: page`; `@page { margin: 0 }` so all spacing comes from CSS padding
- **Footer**: three-column grid (product name · document title · classification + page number), repeated on every page

## License

MIT

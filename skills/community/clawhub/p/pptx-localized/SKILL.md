---
name: pptx
slug: pptx-localized
version: 1.0.0
author: yinfeihaaaaaaaaaaa
license: MIT-0
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file; editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions 'deck,' 'slides,' 'presentation,' or references a .pptx filename. If a .pptx file needs to be opened, created, or touched, use this skill."
triggers:
  - pptx
  - powerpoint
  - presentation
  - deck
  - slides
  - pitch deck
---

# PPTX Skill (Localized for WorkBuddy)

Original: [anthropics/skills](https://github.com/anthropics/skills)
Localized for WorkBuddy by 非宜

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview (requires LibreOffice + Poppler)
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.
Uses `pptxgenjs` (Node.js) to programmatically generate `.pptx` files.

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content. Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it.

### Color Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| Midnight Executive | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| Forest & Moss | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| Coral Energy | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| Warm Terracotta | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| Ocean Gradient | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| Charcoal Minimal | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |

### Typography

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Avoid (Common Mistakes)

- Don't repeat the same layout across slides
- Don't center body text — left-align paragraphs and lists; center only titles
- Don't default to blue — pick colors that reflect the specific topic
- Don't create text-only slides — add images, icons, charts, or visual elements
- NEVER use accent lines under titles — use whitespace or background color instead

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

### Visual QA

Convert slides to images, then inspect visually:

```bash
# Convert to PDF first (requires LibreOffice)
python scripts/office/soffice.py --headless --convert-to pdf output.pptx

# Convert PDF to JPEG images (requires Poppler - pdftoppm)
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

---

## Dependencies

Install these once (managed under `~/.workbuddy/binaries/`):

```bash
# Python: text extraction
pip install "markitdown[pptx]" Pillow defusedxml

# Node.js: create presentations from scratch
npm install -g pptxgenjs

# Optional (for visual QA):
# - LibreOffice (soffice) for PDF conversion
# - Poppler (pdftoppm) for PDF-to-image conversion
```

> **Windows Note**: `soffice.py` in this localized version skips the `AF_UNIX` socket shim
> (Linux-only). It simply runs `soffice` directly via `subprocess.run`.
> Make sure LibreOffice is installed and `soffice` is in your PATH, or set the
> `SOFFICE_PATH` environment variable to the full path of `soffice.exe`.

---

## Localization Notes (vs. upstream)

1. **`scripts/office/soffice.py`** — Removed `AF_UNIX` / `LD_PRELOAD` shim logic.
   Windows never blocks `AF_UNIX`, so the script just delegates to `soffice` directly.
2. **`scripts/office/unpack.py` / `pack.py`** — Use `defusedxml.minidom` (same as upstream).
   No changes needed.
3. **Node.js path** — Use the managed Node path:
   `C:\Users\Administrator\.workbuddy\binaries\node\versions\node-v20.18.0-win-x64\node.exe`
   and the managed npm global prefix for `pptxgenjs`.
4. **`pdftoppm`** — On Windows, install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows)
   or use `png` output from LibreOffice directly as a fallback.

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `scripts/office/unpack.py` | Extract and pretty-print PPTX |
| `scripts/add_slide.py` | Duplicate slide or create from layout |
| `scripts/clean.py` | Remove orphaned files |
| `scripts/office/pack.py` | Repack with validation |
| `scripts/thumbnail.py` | Create visual grid of slides |
| `scripts/office/soffice.py` | Run LibreOffice (Windows-compatible) |

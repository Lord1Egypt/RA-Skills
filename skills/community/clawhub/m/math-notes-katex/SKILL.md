---
name: math-notes-katex
description: Render math-heavy notes to PNG using KaTeX (LaTeX) + headless Brave. Use when the user asks for a clean “solution/конспект as an image”, “formulas as a picture”, or when chat formatting is insufficient (e.g., Telegram). Not for normal text replies.
---

# Notes → PNG (KaTeX + headless Brave)

## Core rule

- Default: reply as normal text
- Render a PNG only when explicitly requested ("as an image", "KaTeX skill", "нормально записанное решение") or when high-quality formula layout is needed
- If using this skill → write formulas in **LaTeX** (`$...$`, `$$...$$`), not ASCII approximations
- Inside the PNG: **Markdown headings (`#`, `##`) are NOT parsed**. Use `--title="..."` for the page title; use plain text for section headers (e.g., `1) ...`)

## Input format

- Save a UTF-8 text file (e.g. `out/_scratch/notes/note.md`)
- Inline math: `$...$`
- Display math: blocks between lines containing `$$`

Details: `references/formatting.md`

## Render to PNG

Scripts:
- `scripts/render_note_png.js` — single-page PNG
- `scripts/render_note_pages.sh` — multi-page (splits into multiple PNGs)

Single-page steps:
1) Write your note (e.g. `out/_scratch/notes/note.md`)
2) Render (keep outputs in `out/` to avoid cluttering repo root):
   - `node skills/math-notes-katex/scripts/render_note_png.js out/_scratch/notes/note.md out/katex/note.png --title="Topic" --brave=/usr/bin/brave-browser`
3) Send `out/katex/note.png`

Multi-page (when the note does not fit well into one image):

```bash
skills/math-notes-katex/scripts/render_note_pages.sh \
  out/_scratch/notes/note.md out/katex/note_pages "Topic" /usr/bin/brave-browser
```

This produces:
- `out/katex/note_pages/page-001.png`, `page-002.png`, ...

## Important: KaTeX CSS/fonts

- KaTeX needs `katex.min.css` + fonts (`fonts/...`)
- This skill links KaTeX CSS via a local `file:///.../katex.min.css` path so relative `fonts/` resolve correctly

If formulas look broken: `references/troubleshooting.md`


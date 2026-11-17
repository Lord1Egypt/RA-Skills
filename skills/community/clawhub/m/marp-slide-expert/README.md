# Marp Slide Expert

> [中文文档](README.zh-CN.md) · 53-page showcase: [examples/infographic-gallery.marp.md](examples/infographic-gallery.marp.md)

**Turn Markdown into consultant-grade slides.** Relationship diagrams, information-architecture maps, executive-report charts, data visualizations — plus covers, column layouts and tables — rendered in one pass into a PDF you can walk on stage with.

- **Consultant-grade diagrams, zero dragging** — 19 diagram skeletons (funnel, pyramid, sankey, swimlanes, radar, balance wheel, 2×2, …), 6 narrative shells and 7 palettes (including a McKinsey-style consulting blue). *Choose* diagrams like a consultant — don't nudge boxes against alignment guides.
- **Charts and tables lay themselves out** — covers, dividers, two- and three-column layouts, main-plus-side, text-over-image, all built in; sizing, type scale and the 15-line overflow limit are enforced for you.
- **Ready for real decks** — pitches, consulting engagements, training courseware. Pure-vector output: crisp on a projector, sharp in print, and a recolour is one hex edit.
- **Frees the knowledge worker** — keep your brain for the story; let the skill handle layout, color and drawing.

**It is Markdown-native.** Markdown is plain-text "source code" for documents — a deck is one readable, editable, diffable `.md` file:

- **Editable by you — and by AI** — change a number, swap a palette, redraw a chart: one line of text, or one prompt.
- **One source, many outputs** — export **PDF / HTML / PPTX** with a single `marp` command; keep the file in your **Obsidian** vault alongside your notes — searchable and version-controlled.
- **AI-native by design** — built for Claude Code / Cursor workflows, with every silent rendering failure mode (half-width tables, escaped SVG, blank-line-killed diagrams) pre-fixed.

## Sample Slides

![](./assets/sample-gallery.png)

53 slides at a glance ([PDF version](examples/infographic-gallery.marp.pdf)) — every skeleton, narrative shell and palette, one page each.

## Why

- **Professional out of the box** — marp renders anywhere, but its default theme is broken in obvious ways (tables half-width, no CJK fonts, content cut off the bottom). The skill ships a working palette and CSS that fixes all of it.
- **Inline SVG diagrams travel with the file** — a PNG has to be redrawn to change one number; an inline SVG changes with one hex edit. The skill ships 19 skeletons with coordinate formulas so you're not guessing.
- **One-shot reviews are inadequate** — the skill ships an SVG linter (6 deterministic checks) and tells you the exact render command. Two automated gates before ship.

## Install

**1. Install the skill** (one command, straight from GitHub):

```bash
npx skills add mebusw/marp-slide-expert       # into the current project
npx skills add -g mebusw/marp-slide-expert    # or globally (all projects)
```

No CLI? Clone into your local skills directory instead:

```bash
git clone https://github.com/mebusw/marp-slide-expert ~/.claude/skills/marp-slide-expert
```

This skill is consumed by Agent Skills: once installed, Claude Code / Cursor pick it up automatically — in a marp session, just say "use marp-slide-expert".

**2. Install the dependency: marp CLI** (for PDF / PPTX / image export):

```bash
npm install -g @marp-team/marp-cli
# If npm -g fails, fall back to:
npx -y @marp-team/marp-cli --version
```

> GitHub: [mebusw/marp-slide-expert](https://github.com/mebusw/marp-slide-expert)

## Quick start

```markdown
---
marp: true
theme: default
paginate: true
style: |-
  /* paste from references/style-bootstrap.md */
---

<!-- _class: cover -->

# My deck title

## Subtitle goes here

---

## First slide

- point 1
- point 2
- point 3
```

Render to PDF:

```bash
marp deck.marp.md --pdf --allow-local-files
```

One source, many outputs — web, PowerPoint, per-page images:

```bash
marp deck.marp.md --html        # web deck (full-screen presentation)
marp deck.marp.md --pptx        # PowerPoint (image-per-slide)
marp deck.marp.md --images png  # per-page PNGs
```

> Want an **editable** PPTX? Add `--pptx-editable` (experimental; needs LibreOffice installed).

For decks with inline SVG diagrams, add `--html` to any export:

```bash
marp deck.marp.md --html --pdf --allow-local-files
```

## Two principles

**15 lines per slide, comments free.** A slide is full when it hits ~15 lines of visible content. HTML comments never render, so they don't count — they're how you stash speaker notes without adding slides.

**Page layout vs diagram layout.** Different problem, different tool:

- One page is content-heavy? → column / split layout (`<div class="cols cols-2">`)
- One page needs to express structural relationships? → inline SVG diagram

Use both on the same deck; they don't compete.

## What's inside

| | |
|---|---|
| `references/infographics-svg/` | 19 skeleton templates (staircase, arrow chain, 2×2, value tree, sankey, funnel, swimlanes, bento, icon-rail, card-row, wave-timeline, pie, radar, balance wheel, …) + 6 narrative shells (pyramid, flywheel, iceberg, funnel, onion, focus) + 7 palettes |
| `references/layout-patterns.md` | Page-level layout recipes (cover, divider, content, columns, splits, image overlays) |
| `references/style-bootstrap.md` | The UPerform / openclaw palette — paste it into frontmatter and you're done |
| `examples/infographic-gallery.marp.md` | A 53-page deck showing every template in use — start from here |
| `scripts/svg-lint.mjs` | 6 deterministic SVG checks (blank lines, `---`, duplicate ids, out-of-viewBox). Run before every render |
| `scripts/build-gallery.mjs` | Regenerates the example deck from the references. Run when you add a template, never hand-edit the example |

## Workflow

1. Copy the `style:` block from `references/style-bootstrap.md` into your frontmatter.
2. Write slides. Stay under 15 lines per slide. Use columns / splits when one slide is content-heavy. Use inline SVG when one slide needs to show structure.
3. Run `node scripts/svg-lint.mjs deck.marp.md` if you used any SVG.
4. Render with `marp deck.marp.md --pdf --allow-local-files` (add `--html` if you used inline SVG).
5. Open the PDF and look at every page. Don't trust your SVG source — render and read.
6. Iterate.

## License & maintenance

Part of the [mebusw/skills](https://github.com/mebusw/skills) collection. Report issues at the parent repo.

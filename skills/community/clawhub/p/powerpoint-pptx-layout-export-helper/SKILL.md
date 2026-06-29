---
name: powerpoint-pptx-layout-export-helper
description: Generate, repair, and export Microsoft PowerPoint PPTX decks with reliable slide layouts, placeholders, charts, images, speaker notes, template fidelity, and presentation-safe rendering. Use when Codex needs to automate or fix PowerPoint decks, inspect PPTX/Open XML, or preserve branded slide designs.
---

# PowerPoint PPTX Layout Export

Use this skill when a deck must be generated or repaired without breaking slide masters, placeholders, fonts, images, charts, or speaker notes. Prefer template-aware edits over drawing every slide from scratch.

## Workflow

1. Identify the deck task: generate slides from data, repair layout drift, preserve a brand template, export slides, fix chart/image placement, or recover speaker notes.
2. Keep the original deck and template intact. Work on a copy and preserve slide masters, layouts, theme files, and media relationships.
3. Inspect the PPTX structure when layout behavior is unclear:
   - Review `ppt/presentation.xml`, slide parts, slide layouts, slide masters, notes slides, media, charts, and relationships.
   - Use `python-pptx` for supported shape, text, table, image, and chart operations.
   - Use direct OOXML edits for features not covered by the library, especially notes, advanced chart links, theme parts, and some placeholder behavior.
4. Anchor edits to slide layouts and placeholders. Avoid absolute positioning until the template structure is understood.
5. Preserve text hierarchy and visual intent: title placeholders, body levels, chart labels, image aspect ratios, theme fonts, and brand colors.
6. Validate the final deck:
   - Check slide count, layout assignment, placeholder population, image cropping, chart data, speaker notes, and embedded media.
   - Render or open the deck when possible to catch text overflow and missing assets.

## Common Fix Patterns

- **Placeholder mismatch**: find the layout placeholder index/type before inserting content; do not assume placeholder order is stable across templates.
- **Image distortion**: preserve aspect ratio, crop intentionally, and check whether the placeholder expects `pic` or shape fills.
- **Chart export problems**: keep embedded workbook/chart relationships intact unless rebuilding the chart deliberately.
- **Speaker notes**: inspect notes slide relationships; many high-level libraries do not fully support notes editing.
- **Template fidelity**: reuse existing slide layouts and theme colors instead of hard-coded colors and fonts.

## Outputs

Provide:

- A slide/deck diagnosis with affected layouts, placeholders, assets, or OOXML parts.
- A generation or repair plan, plus code or edited deck artifacts when requested.
- A visual validation note, including any PowerPoint desktop checks still needed.

Read `references/requirement-plan.md` only when the source demand evidence is relevant.

---
name: powerpoint-pptx-layout-export-helper-2
description: Repair and maintain PowerPoint PPTX templates with slide masters, placeholders, theme fonts, theme colors, chart links, and branded layouts. Use when Codex needs to troubleshoot automated deck generation that breaks a PowerPoint template, inspect slide master OOXML, or preserve brand fidelity across generated slides.
---

# PowerPoint Template Master Fixer

Use this skill when the problem is not just one slide, but the template system behind the deck: slide masters, layouts, placeholders, theme colors, fonts, chart links, and brand rules.

## Workflow

1. Identify the template failure: wrong layout, missing placeholder, changed font, broken chart link, shifted logo, bad theme color, or automated generation that ignores the master.
2. Preserve the original `.pptx` template and work from a copy. Do not flatten masters into ordinary shapes unless the user explicitly wants a static deck.
3. Inspect the deck structure before editing:
   - `ppt/slideMasters/`
   - `ppt/slideLayouts/`
   - `ppt/slides/`
   - `ppt/theme/`
   - `ppt/charts/`
   - relationship files under `_rels`
4. Map each visible issue to the right layer:
   - Master-level issue: brand elements, theme fonts, default colors, global objects.
   - Layout-level issue: placeholder types, positions, title/body/chart slots.
   - Slide-level issue: content inserted into the wrong placeholder or pasted as freeform shapes.
   - Relationship issue: chart, image, or embedded workbook link has moved or gone missing.
5. Prefer template-aware repairs. Reuse layouts and placeholders before adding manual shapes.
6. When using `python-pptx`, confirm whether the target feature is supported. For unsupported master/theme/chart-link edits, inspect or patch OOXML directly.
7. Validate by checking slide count, layout assignment, placeholder IDs/types, theme colors, fonts, charts, linked media, and a rendered or opened view when possible.

## Fix Patterns

- **Wrong placeholder filled**: identify placeholder type and index from the layout, then bind content to that placeholder rather than assuming order.
- **Theme colors ignored**: use theme references where possible; avoid hard-coded RGB unless the brand guide requires it.
- **Fonts change after generation**: inspect theme font definitions and local text run overrides.
- **Charts lose links**: preserve chart relationship IDs, embedded workbook parts, and chart XML.
- **Brand elements move**: keep logos and fixed elements on masters or layouts, not repeated manually on each generated slide.

## Output

Give the user:

- A diagnosis of the broken template layer.
- A repair or generation plan tied to specific PowerPoint parts.
- Any code or OOXML changes needed.
- A validation note describing what was checked visually and structurally.

Read `references/requirement-plan.md` only when the original discovery evidence is needed.

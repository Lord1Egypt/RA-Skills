# Validation

Validate substantial HTML artifacts before returning them. The goal is to catch broken rendering, missing dynamic content, accidental external dependencies, and responsive layout failures.

## Static Checks

- Confirm the file includes `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, viewport meta, and a meaningful `<title>`.
- Confirm CSS and JavaScript are inline unless the user explicitly asked for a multi-file project.
- Scan for accidental external dependencies: `<script src>`, stylesheet `<link>`, `@import`, CDN URLs, remote fonts, and network-only assets.
- If the artifact should be offline, treat external dependencies as defects.
- Check that source references, assumptions, counts, and labels needed to understand the artifact are visible in the page.
- For artifacts about an existing project, product, app, docs site, or brand, confirm there is a style provenance note naming the inspected source style files/tokens, the saved theme file, or `themes/fallback-theme.md`.
- If source/project style is claimed, confirm the CSS visibly uses extracted source tokens. If no style evidence was found, confirm the artifact uses the actual fallback theme instead of a generic invented palette.

## Render Checks

Use the strongest browser path available in the environment:

1. Preferred: browser automation that can navigate to the file, evaluate JavaScript, click controls, inspect console errors, and capture screenshots.
2. Good fallback: installed Chrome or Chromium in headless mode with a throwaway profile.
3. Minimal fallback: parse the rendered DOM or inspect the file statically, then state that browser rendering was not available.

For JavaScript artifacts, verify the rendered DOM, not only the source file. Count generated cards, rows, SVG nodes, tabs, filters, selected states, or other expected dynamic output.

For interactive artifacts, exercise at least one meaningful interaction:

- click a tab, filter, node, row, toggle, or export button
- confirm selected/active state changes
- confirm the relevant `aria-selected`, `aria-pressed`, `aria-current`, checked state, or selected class changes with the visual state
- confirm the detail panel, preview, counts, or export output updates
- when cards are primary navigation or selectable items, hover or focus one card and confirm the affordance is visible without layout shift
- when cards have arrows or look clickable, click one and confirm it navigates, updates a detail panel, copies/exports, or otherwise does real work
- for Kanban/triage boards, drag a card to another lane and confirm lane counts, estimate totals, selected state, and export text update. Also test the click-based movement fallback if present.
- for slide decks, click next/previous arrow buttons and press left/right arrow keys. Confirm the active slide, numbered tab `aria-selected`, and progress label stay in sync.

## Responsive Checks

Check at least one desktop viewport and one narrow viewport around 390px wide.

- Page-level `document.documentElement.scrollWidth` should not exceed `clientWidth`.
- Horizontal scrolling is acceptable only inside intentional containers such as `.table-wrap`, code blocks, or large diagrams.
- Chip-like rows must not horizontally scroll. Inspect jump links, filter chips, segmented controls, badge rows, button groups, tag rows, and legends; they should wrap onto additional lines.
- Long paths, URLs, hashes, branch names, package names, and commands should wrap inside their container.
- Headings should not be clipped or force the viewport wider.
- Buttons, chips, cards, table cells, and SVG labels should not overlap incoherently.
- Code blocks must be readable at desktop and narrow widths. Inspect at least one `pre`/`pre code` block when present: text must have clear contrast, inline-code chip backgrounds must not appear behind block-code lines, copy buttons must not cover text, and horizontal scrolling must stay inside the code block.
- Substantial code blocks should have syntax highlighting. Confirm at least one token class or equivalent inline token styling exists inside each reusable JSON, HTML, CSS, JavaScript, TypeScript, shell, or diff block. Plain monochrome blocks are acceptable only for tiny one-line snippets or raw terminal output where highlighting would add no signal.
- Pills or chips used as labels above headings should have clear spacing below them.
- Diagrams should fit inside their panel on desktop. If they scroll on narrow screens, the scroll must be bounded to the diagram container and not create page-level overflow.
- Token swatches should not become oversized empty slabs unless the artifact is explicitly a palette mood board.
- Avoid viewport-unit font sizing. Use explicit font sizes with media-query breakpoints.

Useful CSS defaults:

```css
pre,
:not(pre) > code,
.long-token {
  overflow-wrap: anywhere;
  word-break: break-word;
}

pre code {
  display: block;
  margin: 0;
  padding: 0;
  background: transparent;
  border: 0;
  color: inherit;
  font: inherit;
  white-space: inherit;
}

.tok-key { color: #93c5fd; }
.tok-str { color: #86efac; }
.tok-num,
.tok-lit { color: #fbbf24; }
.tok-comment { color: #94a3b8; }
.tok-prop { color: #c4b5fd; }
.tok-punc { color: #cbd5e1; }
.tok-add { color: #86efac; }
.tok-del { color: #fca5a5; }

img,
svg,
canvas {
  max-width: 100%;
}
```

## Screenshot Review

When screenshots are available, inspect them. Do not accept a screenshot merely because it exists.

Look for:

- blank or partially painted pages
- clipped headings
- text spilling out of cards or callouts
- chip, filter, or jump-link rows clipped behind horizontal scrolling
- path/code tokens widening the page
- unreadable SVG labels
- arrows crossing through unrelated nodes or each other in a way that makes direction unclear
- missing active states
- missing hover/focus affordance on clickable cards, rows, or diagram nodes
- clickable-looking cards that do not link or update anything
- SVG diagrams clipped by their panel or spilling outside their visible border
- label chips touching headings
- token swatches that waste space or obscure the token/value relationship
- Kanban tickets with oversized centered titles, missing type/owner/estimate metadata, or no visible drag/drop affordance
- controls detached from the content they affect

If the screenshot reveals a layout defect, patch the artifact and rerun the relevant check.

## Reporting

Keep the final response brief. Mention the checks that matter:

- static self-containment check
- browser render or fallback used
- dynamic DOM/interaction check when relevant
- desktop and narrow viewport check
- any checks that could not be run

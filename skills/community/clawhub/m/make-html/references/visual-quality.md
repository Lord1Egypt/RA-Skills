# Visual Quality

The artifact should look like a useful custom interface, not a generic decorated document.

## Page Shape

- Start with the job the page is doing: decision, review, plan, explanation, report, prototype, or editor.
- Put the most important conclusion near the top.
- Use navigation only when the page has enough sections to justify it.
- Use full-width sections or clear grids rather than nested cards everywhere.
- Reserve cards for repeated items, options, findings, tickets, metrics, or rows.
- Keep repeated items visually consistent so comparison is easy.
- Make the format match the task. Comparison pages use aligned columns. Timelines use timelines. Reviews use annotated code. Diagrams use diagrams. Editors put the work area first.

## Typography

- Use a system font stack unless a project style says otherwise.
- Use a readable base size, usually 15-17px.
- Use compact headings inside dense tools and larger headings only for page-level hierarchy.
- Keep line length comfortable: roughly 60-85 characters for prose.
- Use tabular numbers for metrics when alignment matters.

## Color

- Use color to encode meaning: severity, status, category, ownership, selected state, changed state.
- Use a neutral base with a small set of purposeful accents.
- Label color-coded meanings in text or a legend.
- Avoid making every section the same hue with slightly different tints.

## Layout

- Use CSS grid for comparisons, dashboards, boards, and component sheets.
- For repeated cards, prefer container-responsive tracks such as `repeat(auto-fit, minmax(min(100%, 300px), 1fr))` and set children to `min-width: 0`. Avoid fixed three-column grids that overflow in side panes or narrow app windows.
- Use flex for toolbars, chips, metric rows, and compact controls.
- Set chip, filter, badge, segmented-control, and jump-link rows to `flex-wrap: wrap`. Do not put these controls in horizontal scrolling containers.
- Label chips above titles need bottom padding or a column gap. A pill touching a heading reads as broken layout.
- Use sticky sidebars or top nav only when they improve navigation.
- Let dense tables scroll horizontally on small screens if needed.
- Let large diagrams scroll or scale only when wrapping would destroy the diagram. Explain that the diagram is intentionally scrollable when it is.
- Keep buttons, filters, and export controls close to the content they affect.

## Motion And Hover

- Use motion as an affordance, not decoration. Interactive cards, rows, and diagram nodes may lift 1-4px, strengthen their border, or move a trailing arrow slightly.
- Card hover should be tasteful and compound: slight lift, darker border, soft shadow, subtle media/header tint, and an emphasized file/action label.
- Mirror hover states with `:focus-visible`; keyboard focus should feel as intentional as pointer hover.
- Avoid hover-only content. Any text, count, warning, or action needed to understand the card must be visible without hover.
- Respect `prefers-reduced-motion: reduce` by removing transforms and nonessential transitions.

## Diagrams

- Use inline SVG for flowcharts, architecture maps, timelines, rings, dependency graphs, and annotated figures.
- Use `viewBox`, not fixed-only SVG sizing.
- The rendered SVG must fit inside its panel on the target desktop viewport. Add internal SVG margin and avoid placing nodes directly against the viewBox edge.
- Set SVGs to `max-width: 100%`. Use a bounded scroll wrapper only when scale would make labels unreadable.
- Use grouped elements and readable IDs/classes for editable SVG.
- Use round coordinates where possible.
- Use `currentColor` for ink when the diagram should adapt to theme.
- Label nodes directly.
- Use arrows and spacing to make direction obvious.
- Before drawing, choose a lane model: left-to-right pipeline, top-to-bottom pipeline, swimlanes by subsystem, or radial only when there are no directional dependencies.
- Route arrows along rows or columns when possible. Use orthogonal paths, elbow routes, or direct horizontal/vertical edges before diagonal edges.
- Avoid crossings between arrows. If two relationships would cross, move nodes into lanes, split the diagram into panels, or use numbered callouts instead of drawing every relationship.
- De-emphasize secondary relationships with details panels or tables instead of adding long crossing arrows.
- Use screenshot review to check arrow readability; do not rely only on the SVG source looking plausible.
- Include a legend when color, line style, or shape has meaning.
- Put explanatory text next to the diagram, not far below it.
- Do not use raster images for diagrams that can be drawn as SVG.

## Code And Diffs

- Use monospace blocks with line numbers when reviewing code.
- Put annotations beside or immediately after the relevant lines.
- Use severity labels for findings.
- Keep long code excerpts collapsible.
- Highlight only the important lines; do not turn every line into visual noise.
- Do not let inline-code chip styles leak into block code. Use `:not(pre) > code` for inline code, never a global `code` selector with background, border, padding, or color.
- Every `pre code` must reset inherited chip styling: transparent background, no border, no extra padding, `color: inherit`, `font: inherit`, and `white-space: inherit`. The visible contrast should come from the `pre` block itself.
- Add syntax highlighting to substantial code blocks. Prefer stable semantic spans such as `.tok-key`, `.tok-str`, `.tok-num`, `.tok-lit`, `.tok-comment`, `.tok-prop`, `.tok-punc`, `.tok-tag`, `.tok-attr`, `.tok-add`, and `.tok-del`, or a small inline highlighter that creates those spans at load time.
- Keep highlighting tasteful and readable: strings, keys/properties, keywords, comments, literals, numbers, punctuation, tags/attributes, and diff additions/deletions should be distinguishable without turning every token into a different color.
- If you use a runtime highlighter, escape source text before insertion and keep token passes from rewriting generated `<span>` markup or HTML entities.

## Tokens And Swatches

- For token references, default to a compact square swatch beside the token name and value.
- Reserve large swatch slabs for palette mood boards, not ordinary design-token lists.
- Long token names and values must wrap inside the row instead of widening the page.

## Boards And Tickets

- Kanban boards should be information-dense, not card-heavy dashboards. Use compact ticket cards with small titles and useful metadata.
- Ticket cards should usually show id, type/status chip, owner/assignee, size or estimate, and a short title.
- Lane headers should show lane name and count. Lane footers can show estimate totals when planning or triage is the task.
- Drag/drop boards need visible drag state and lane drop feedback. Keep click-based movement as a fallback when practical.
- Avoid oversized centered ticket titles; they reduce scan speed and make the board feel like a demo rather than a workflow.

## Responsive Behavior

- On wide screens, use side-by-side layouts.
- On narrow screens, stack sections in the order a reader should inspect them.
- Keep controls reachable without forcing the reader to scroll back to the top.
- Avoid fixed pixel widths for primary content.

## Source Readability

- Write HTML that another agent can modify.
- Use clear class names.
- Group CSS by layout, components, utilities, then responsive overrides.
- Keep JavaScript small and direct.
- Keep data separate from rendering logic when the page has repeated items.

## Match Existing Style

When the source project, brand, or product has an existing style, derive from it instead of inventing a new look.

Useful sources:

- CSS variables.
- Tailwind or theme config.
- Design token files.
- Component source.
- Existing product pages.
- Brand or documentation pages.

Extract concrete tokens before styling:

- background, panel, card, text, muted text, border, accent, secondary accent, semantic colors
- radius scale, shadow scale, focus ring, animation duration/easing
- button, chip, card, nav, table, and status-badge patterns
- density: compact operational UI, editorial docs, marketing page, game, or utility

Use those tokens directly when the artifact is for that product. Include a small "style evidence" note or source list in the artifact when useful so the styling choices are auditable.

When style will be reused, create or update a design reference artifact: swatches, type scale, spacing, radius, shadows, components, and motion tokens. Future HTML artifacts can read that reference and reuse its CSS variables.

If no source style exists after a quick search, use `themes/fallback-theme.md` instead of inventing a generic gray dashboard. The fallback theme is a paper/editorial style with a light plum accent, wrapped navigation, strong code examples, and restrained card styling.

If the artifact is about an existing project or product, the style choice must be auditable. Either use concrete source tokens and name the files/tokens, use a named saved theme, or use `themes/fallback-theme.md`. Do not ship an unlabeled neutral light UI as a compromise.

## Taste Defaults

- Prefer calm, precise, content-led design.
- Avoid excessive gradients, glass effects, oversized decorative shapes, and novelty styling unless the topic calls for it.
- Use whitespace to separate ideas, not to inflate the page.
- Make the artifact feel made for this exact task.

Avoid these defaults unless the user or subject calls for them:

- Cards everywhere on a gray background.
- Full-bleed gradient hero sections.
- Emoji as structural labels.
- Multiple shades of one accent color doing no work.
- Generic dashboard chrome around a simple document.
- Centering every section.
- Placeholder logos or fake nav.

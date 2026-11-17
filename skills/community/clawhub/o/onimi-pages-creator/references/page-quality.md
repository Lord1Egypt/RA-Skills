# Standalone page quality

Choose structure from the user's content and task:

- Narrative material such as product stories, reports, research, and portfolios benefits from an
  editorial reading path, anchored evidence, and a print layout.
- Operational material such as runbooks, plans, and itineraries benefits from sequence, progress, and
  locally persistent or clearly temporary check state.
- Comparison and calculation tools need explicit inputs, immediate results, sane defaults, and a clear
  statement that sample figures are illustrative.
- Teaching and quiz pages need visible progress, reversible choices, keyboard-complete controls, and
  feedback that explains the result.
- Posters and invitations should commit to one visual gesture while preserving readable details and a
  useful print view.
- Slide decks need real slide boundaries, page position, previous/next controls, keyboard navigation,
  and a print or export treatment that includes every slide.

## Establish a visual system

Start with the content hierarchy and choose one strong direction that supports it. Decide which material
deserves the first screen, what should be scanned, what should be explored, and what must remain visible
during interaction. A product story may need a credible hero illustration and detail views; a data page
needs legible scales, comparisons, and annotations; a presentation needs paced slides rather than a long
report placed inside a frame.

Avoid using a shared banner, oversized headline, card grid, rounded control group, and abstract gradient
as the default skeleton. Those choices are valid only when the content calls for them. For a batch, vary
the grid, type family and scale, density, color logic, imagery, navigation, and interaction model. Three
representative pages should be visually reviewed before their pattern is extended to the rest of a set.

Use user-supplied imagery when available. Otherwise create purposeful inline SVG, CSS illustration, or
data visualization that carries the subject; do not use an empty blob or decorative panel as a substitute
for the product, evidence, or story the page promises. Keep source and licensing facts clear.

Prefer CSS Grid for the page's main composition and Flexbox for controls. Define a small local token set
for color, type, spacing, shape, and motion. System fonts are reliable for a self-contained page. Use
inline SVG or CSS shapes only when they convey information; include text equivalents for charts and
diagrams.

For bilingual work, translate headings, labels, help text, buttons, validation messages, interactive
results, the document title, and the `<html lang>` value. A language change must not reset the user's
current selections or progress. Set intentional line breaks per language where display type needs them.
Use language-specific size, width, and line height when one setting cannot serve both scripts. Inspect
Chinese for overlapping strokes and single-character final lines, and inspect English for clipped or
overwide words.

Before delivery, verify:

- 320px to desktop widths without horizontal document scrolling.
- Logical Tab and Shift+Tab order, visible `:focus-visible`, and Enter/Space behavior.
- A stable page with animation removed under reduced-motion preference.
- Legible print output without sticky controls or dark ink-heavy backgrounds.
- No dead links, fake checkout/contact submission, silent network calls, or unlabeled invented data.
- Screenshots of every supported language at the intended cover size, checked for hierarchy, crop,
  collision, orphaned display text, and content that looks like a temporary placeholder.

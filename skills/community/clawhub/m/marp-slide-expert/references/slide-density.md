# Slide Density and Splitting

Marp slides have no auto-shrink. If content overflows the slide canvas, it just disappears off the bottom. You must split proactively.

## The 15-line hard cap

**Every slide renders at most 15 lines of content. This is the primary budget — char counts are only a proxy for it.**

### How to count a line

| Element | Counting rule |
|---|---|
| Paragraph | 1 line per ~38 CJK chars or ~75 Latin chars, as wrapped at default font |
| Bullet / numbered item | 1 per item, +1 more if it wraps |
| Table | 1 per **row, including the header row**. A 4-col x 4-row table = 5 lines. |
| Code block | 1 per code line, no partial credit |
| Quote / tip / warn box | 1 per wrapped line inside the box |
| Heading | Counts 1 line before the body starts |
| HTML comment | **0 lines** — never renders |
| Image | 0 lines, but consumes vertical space (see below) |

The 15 is a **total budget**, not a per-element allowance. A slide at exactly 15 is still too full once a background image takes up half the canvas.

### Per-slide targets

| Content type | Target body lines | Max body lines |
|---|---|---|
| Title + 1 background image | 6 | 8 |
| Title + 2+ images | 2 | 4 |
| Text only | 10–12 | 15 |
| Single table | 5 rows (incl. header) | 8 rows (incl. header), 4 cols max |
| Code block | 8 lines | 10 lines |
| Bulleted list | 7 items | 10 items |
| Divider / cover | 0–2 | 3 |

Rows and cols both count against the 15: a 10-row x 2-col table is 11 lines, not 5.

## When to split

Trigger a split when ANY of these is true:

- The slide's rendered line count exceeds 15 (or the per-slide target above).
- A single paragraph would wrap to more than ~5 lines on its own.
- A table has more than 8 rows including the header, or more than 4 columns.
- A code block is longer than 10 lines.
- A bulleted list has more than 10 items.
- The slide has a background image and more than 8 body lines.

## When NOT to split — use a speaker note instead

Before splitting, ask: **is this content for the audience, or for me?**

Anything the audience doesn't need to read on screen — background context, caveats, the story behind a number, Q&A prep, an aside — goes into an HTML comment instead of a new slide:

```markdown
## Three deployment modes

- Public cloud: fastest to launch
- On-premise: compliance first
- Hybrid: best cost

<!--
Speaker notes: Hybrid is the newest option; long-time customers ask about it most.
Case: a bank went on-premise, 8M contract.
If asked about pricing, jump to the table on the next slide.
-->
```

HTML comments are invisible in the rendered HTML/PDF/PPTX and visible only in the `.md` source. They cost **zero** of the 15-line budget.

Two traps:

- A `---` inside a comment is **still** a page break. Never write one inside a note.
- Marpit directives also use `<!-- -->`; those must start with `_` (`<!-- _class: cover -->`) to stay active. Speaker notes must not start with `_`.

**Rule of thumb: adding a second slide is a cost to the audience. Adding a speaker note is free. Reach for the note first.**

## How to split

**Split at paragraph boundaries, never mid-paragraph, mid-bullet, or mid-table-row.** If two adjacent paragraphs together exceed the budget, the second one becomes the start of the next slide. If a single paragraph is too long, split by sentence-ending punctuation:

```python
# Python pseudo-code — budget is now LINES, not chars.
# CJK_LINE = 38, LATIN_LINE = 75; count wrapped lines per sentence.
sentences = re.split(r'(?<=[。！？\n])|(?<=\.\s)', paragraph)
chunk = ""
chunk_lines = 0
for sent in sentences:
    n = est_lines(sent)          # 1 + len(sent) // CJK_LINE
    if chunk_lines + n > 13 and chunk:   # 13 leaves room for a title
        emit(chunk.strip())
        chunk, chunk_lines = sent, n
    else:
        chunk += sent
        chunk_lines += n
if chunk.strip():
    emit(chunk.strip())
```

**Keep the slide title on the first chunk only.** Subsequent chunks from the same source section should NOT repeat the title — otherwise you get a wall of identical H2s. Give them a continuation marker instead (`## Topic (cont.)`).

**Never leave a dangling table fragment** — if a table must split, repeat the header row and note `(table continued)`.

## Tables

Wide tables overflow horizontally. Strategies:

1. **Reduce columns**: drop optional columns. Hard cap is 4.
2. **Split rows**: half the rows go on slide N, half on N+1, with the header row repeated and a `(table continued)` note.
3. **Shrink font**: in CSS, set `table { font-size: 0.78em; }`. Below 0.7em the text becomes hard to read.

For tables with Chinese text, the default font size renders narrower than Latin tables, so you get more columns per line — but the **row** count still costs a line each regardless of width.

## Code blocks

Long code needs CSS adjustment:

```css
pre {
  background: #1a1a2e;
  color: #2ecc71;
  padding: 14px;
  border-radius: 8px;
  font-size: 0.75em;     /* shrink default */
  line-height: 1.4;
}
pre code {
  background: transparent;
  color: inherit;
  padding: 0;
}
```

Shrinking the font reduces visual weight but **does not reduce the line count** — 25 lines of code is still 25 lines. Split at logical boundaries (function def, between classes, between blocks), or move to an appendix slide. For SQL / shell output that's inherently long, prefer an appendix slide over cramming it onto a content slide.

## Lists

When splitting a long list, look for natural grouping:

- Topical groupings (e.g., "3 things about X" then "3 things about Y").
- Sequential steps with named phases.
- Pairs of concept + example.

If the list is too flat to split meaningfully, consider converting to a table — tables often pack more information per slide. If the extra detail is speaker-only context, use a `<!-- -->` note instead.

## Image-heavy slides

When a slide has multiple images and they collectively fill the slide, leave text minimal or off the slide entirely. A title + 2-3 images is a complete slide.

If text is essential alongside images, use the split layout (see [layout-patterns.md](layout-patterns.md)) and cap the text at ~6 body lines.

## Detection heuristics

When scanning a generated slide, watch for these warning signs:

- Slide body ends with content cut at the bottom edge of the PDF preview.
- Counting the lines exceeds 15.
- A bullet list has more bullets than fit in the slide height.
- Code block scrolls past the visible area in PDF preview.
- Table extends beyond the right edge.
- Two consecutive slides both feel thin — usually the split was unnecessary and a speaker note would do.

Render preview after every batch of changes and visually scan the first 3-5 slides plus a sample from middle/end. Line counting catches most overflow; the render catches the rest.

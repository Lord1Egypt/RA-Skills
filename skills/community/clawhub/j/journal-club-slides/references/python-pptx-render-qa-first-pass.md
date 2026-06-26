# Python-pptx first-pass render QA lessons for paper journal-club decks

## When this reference matters
Use this note when a first generated deck is technically exportable but still visually below bar after render QA, especially in python-pptx workflows that start from full-page paper renders.

## Session pattern captured
- Workspace built around a paper-specific directory with `text/`, `renders/`, `notes/`, QA outputs, and a local `.venv`.
- `python3 -m venv` + local installs (`pymupdf`, `python-pptx`, `pillow`, `markitdown`) solved missing-PyMuPDF problems without relying on system Python.
- `soffice --headless --convert-to pdf` + `pdftoppm -jpeg -r 150` produced reliable slide QA renders.
- A 24-slide integrated bilingual deck was generated successfully, but rendered inspection surfaced issues that source generation did not reveal.

## Failures seen only after render QA
### 1. Header-band collisions
- Bilingual top bars can clip or overlap when the title band is too short.
- Fixes that worked: increase header height, slightly reduce title font size, and move the top-right badge/metadata away from the text block.

### 2. Bottom text overflow
- Bullet areas that looked acceptable in source still clipped at the bottom after rendering.
- Fixes that worked: increase text-box usable height and slightly reduce bullet font size before shrinking figures.

### 3. Support figure unreadability
- A right-side support image can be technically present but still useless if it is just a tiny full-page paper render.
- Treat this as a blocker. Replace tiny page thumbnails with figure-aware crops or split the content across more slides.

### 4. Empty-space imbalance on synthesis slides
- Summary/integration slides can look unfinished when inner content panels are too tall at the top and leave large blank lower regions.
- Rebalance by shrinking the decorative/content container and redistributing vertical space before adding more text.

## Workflow correction encoded
Do not stop at a first exportable deck when using python-pptx for figure-heavy paper slides.

## Required next pass
1. Export the `.pptx`.
2. Convert to PDF and slide JPEG/PNG renders.
3. Inspect representative slides for header overlap, text clipping, support-figure readability, and whitespace imbalance.
4. Patch layout primitives globally first (header band, bullet-box height, font sizes, figure/text region proportions).
5. Re-render and inspect again.
6. If support figures are still unreadable, escalate from full-page renders to figure-aware crops instead of continuing to tune typography.

## Multi-paper deck lesson
For integrated decks spanning multiple papers:
- Verify the intended paper set before design; exclude unrelated attachments even if they were uploaded together.
- Build the narrative so "how the quantity was analyzed" transitions into "how the quantity was engineered" rather than presenting isolated mini-decks.
- If one attached PDF is unrelated, document the corrected paper set in the notes/workspace and continue with the real set.

## Practical implementation note
Good first-pass global fixes in `python-pptx` scripts are often:
- taller title band
- smaller title font by 1–3 pt
- larger bullet text-box height
- bullet font reduced modestly (for example 15 pt -> 13.5 pt)
- rebalanced figure/text vertical split on image-heavy slides

These are worth trying before slide-by-slide hand edits, but they are not sufficient if the core issue is that the slide still uses full-page paper pages where a figure crop is required.

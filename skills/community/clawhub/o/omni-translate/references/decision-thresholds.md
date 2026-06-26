# Decision Thresholds

## Contents

- Unsafe round-trip conditions
- When PDF in-place editing is forbidden
- Layout drift tolerance
- OCR reuse thresholds
- Escalation behavior

## Unsafe round-trip conditions

Treat the artifact as not safely round-trippable when any one of the following is true:

- No structure-preserving parser, editor, or toolchain is available for the source format.
- The only available file is a derived export, a minified bundle, a signed artifact, or a proprietary binary that cannot be edited and rebuilt safely.
- A pilot extraction loses structural anchors needed for reinsertion, such as text runs, slide or page order, placeholder identity, or editable text objects.
- Any touched structured file fails to parse after reinsertion. This includes XML, JSON, YAML, HTML, Office XML parts, or application source files.
- Placeholder parity is anything below 100 percent.
- Any touched output contains replacement characters, tofu boxes, or missing-glyph markers after the first full validation pass.
- The target locale requires glyphs the available fonts cannot render and no explicit fallback font can be applied safely.
- A pilot export changes page count or slide count without the user explicitly approving that change.
- Any critical text object clips, overlaps, disappears, or changes reading order after one controlled fitting pass.

## When PDF in-place editing is forbidden

Do not attempt in-place PDF editing. Switch to extraction plus rebuild, or go back to the editable source, when any of the following is true:

- A `docx`, `pptx`, source design file, HTML source, or other editable parent artifact exists.
- The PDF lacks a reliable text layer and requires OCR for a meaningful portion of the page.
- The extracted text order does not match visual reading order on any critical page or on more than 3 pages total.
- The first pilot page requires manual coordinate correction for more than 10 percent of touched text objects.
- Font subsetting or embedding prevents safe insertion of target-language glyphs.
- A pilot save breaks bookmarks, annotations, form fields, or link targets that the user expects to preserve.
- The document is legal, compliance, or contract material where even small geometry changes could alter meaning or reviewability.

## Layout drift tolerance

Only the following kinds of drift are acceptable in a final deliverable:

- Line breaks change inside the same text container, but no text clips or overlaps.
- Bounding-box growth stays within 2 percent of the original container size or 4 pixels in either dimension, whichever is larger.
- Neighboring objects do not shift enough to change alignment, reading order, or pointer relationships.
- Page count, slide count, and section order remain unchanged unless the user approved a change.

Treat drift as a hard failure when any of the following occurs:

- Any title, button label, chart label, table header, legal disclaimer, or form label clips, overlaps, or becomes ambiguous.
- Any touched object moves enough to occlude graphics, detach from callouts, or alter visual grouping.
- Any table row height, slide layout, or page reflow causes information to move out of view.
- More than 1 percent of touched text containers show visible overflow after fitting.

## OCR reuse thresholds

Use OCR output for automatic reinsertion only when all of the following are true:

- The OCR engine exposes confidence scores.
- Average word confidence is at least 0.98.
- No user-visible region that will be reinserted scores below 0.95.
- A human or deterministic post-check reviews all low-confidence spans before reinsertion.

Treat OCR output as reference-only when any of the following is true:

- Average word confidence falls between 0.90 and 0.98.
- The engine does not expose usable confidence scores.
- Mixed-language text, formulas, tables, handwriting, or low-resolution scans produce obvious segmentation errors.

Do not translate or reinsert from OCR alone when any of the following is true:

- Average word confidence is below 0.90.
- Critical pages contain unresolved low-confidence spans.
- The source is a screenshot, scan, or photo where layout reconstruction would require manual design work rather than text replacement.

## Escalation behavior

- If a hard-stop threshold triggers, stop editing and explain which threshold failed.
- If only a best-effort path remains, label it as best-effort, narrow the scope, and state what fidelity guarantees are no longer possible.
- Do not silently downgrade from editable-source localization to PDF repainting or OCR-based repainting.

# Format Risk Checklists

## Contents

- PPTX
- DOCX
- PDF
- Markdown and docs
- Web and i18n
- Subtitles

## PPTX

Check these before translating:

- Are text boxes fixed-size, auto-fit, or manually resized?
- Does the deck use theme fonts or master-slide fonts that lack target-language glyphs?
- Do charts, SmartArt, grouped shapes, or diagram labels contain editable text?
- Do speaker notes need translation, or is only on-slide text in scope?
- Do hidden slides exist, and are they part of the deliverable?
- Do screenshots or exported diagrams contain rasterized text that should stay untouched?

Common failure modes:

- Text boxes overflow after translation.
- Auto-wrap changes vertical alignment or slide balance.
- Master-slide font substitution changes size or line height globally.
- Notes are translated inconsistently with visible slide copy.
- Callouts detach from the object they describe after layout changes.

## DOCX

Check these before translating:

- Does the file contain tracked changes, comments, or unresolved review markup?
- Are headers, footers, footnotes, endnotes, captions, or cross-references in scope?
- Does the document use a table of contents, field codes, or generated lists that should be refreshed after translation?
- Are there text boxes, floating shapes, or embedded charts with text?
- Do document properties or keywords need translation?

Common failure modes:

- Translating visible text but leaving tracked changes, comments, or metadata in the source language.
- Breaking field codes or cross-references.
- Expanding translated text so a table cell or text box clips.
- Accepting or rejecting revisions accidentally while editing.
- Changing pagination enough to invalidate references in contracts or review workflows.

## PDF

Check these before translating:

- Is there a real text layer, or is this a scan or image-only export?
- Do fonts appear subsetted or embedded without target-language coverage?
- Is the reading order simple, or does the file use multiple columns, rotated text, or side notes?
- Are forms, annotations, bookmarks, or signatures present?
- Does the file contain charts, diagrams, or screenshots with rasterized text?

Common failure modes:

- Text extraction order differs from visual reading order.
- Coordinate-based reinsertion causes overlap or clipping.
- Missing glyphs appear because the embedded font cannot render the target locale.
- Multi-column pages translate in the wrong order.
- Editing destroys links, form behavior, or annotations.

## Markdown and docs

Check these before translating:

- Does the file contain frontmatter, reference links, MDX components, or raw HTML?
- Are code fences, inline code, or shell commands mixed with prose?
- Are tables narrow enough that translated strings will break column layout?
- Do link targets or anchor IDs depend on headings that should remain stable?
- Do images or diagrams include text that should stay in the source language?

Common failure modes:

- Translating frontmatter keys instead of values.
- Breaking Markdown tables through uncontrolled text expansion.
- Translating code samples, filenames, or commands that should remain literal.
- Changing headings that other docs link to.
- Localizing alt text but forgetting linked captions or figure references.

## Web and i18n

Check these before translating:

- Does the project already use i18n resource files, ICU messages, or framework locale bundles?
- Are plural rules, gender rules, or variable interpolation patterns present?
- Are there fixed-width containers, truncation logic, or character limits in the UI?
- Does the target locale require RTL support, locale-aware formatting, or alternate fonts?
- Are charts, canvases, SVGs, or screenshots used for visible text?

Common failure modes:

- Placeholder or ICU syntax corruption.
- Inconsistent translation of the same UI term across routes or components.
- Truncated buttons, tabs, badges, or menus after translation.
- Missing locale formatting for dates, numbers, units, or currencies.
- Translating visible web text while leaving accessibility labels or metadata untouched.

## Subtitles

Check these before translating:

- Are speaker labels, sound effects, or formatting tags present?
- Does the target locale need fewer or more characters per line?
- Are timecodes fixed, or may cues be re-timed?
- Are burned-in subtitles also present in video frames?

Common failure modes:

- Line lengths become unreadable.
- Timing remains valid technically but becomes too dense to read.
- Formatting tags are broken.
- On-screen text in the video remains untranslated while subtitle text changes.

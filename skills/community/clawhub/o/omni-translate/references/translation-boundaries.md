# Translation Boundaries

## Contents

- Translate by default
- Protect by default
- Hidden and non-body content
- Embedded image and diagram text
- Placeholder handling
- Segment strategy
- Terminology and style controls
- Reporting rules

## Translate by default

- User-visible UI strings
- Body text in documents and slide decks
- Headings, captions, labels, and alt text
- Documentation prose and README content
- Comments and notes only when the user wants them localized
- Metadata that is visible to end users, such as titles and descriptions

## Protect by default

- Variable names, function names, class names, package names, and imports
- Schema keys, JSON keys, YAML keys, and protocol fields
- HTML tags, XML tags, Markdown syntax, and code fences
- CSS selectors, utility classes, and IDs
- URLs, file paths, route paths, and MIME types
- Placeholders such as `%s`, `%d`, `{name}`, `{{ count }}`, `$1`, and `<0>...</0>`
- Regexes, checksums, hashes, signatures, and machine-readable tokens
- SQL keywords and code snippets unless the user explicitly asks for code-comment or sample-code localization

## Hidden and non-body content

Handle edge content explicitly instead of assuming it follows body-text rules.

- Speaker notes: translate only when the deck itself is the deliverable, the user asks for presenter material, or the notes will be exported.
- Hidden slides: leave untouched by default. Translate them only when the user says the whole deck is in scope or hidden slides ship externally.
- Tracked changes: preserve review state by default. Do not accept or reject changes automatically. Translate review markup only when the user explicitly wants it.
- Comments and annotations: translate when they are part of collaboration or review deliverables. Otherwise leave them in the source language and report that choice.
- Metadata, title, subject, and keywords: translate if they surface in export, search, publishing, or store listings. Preserve otherwise.
- Accessibility labels: translate for end-user-facing web, app, document, and slide content whenever those labels are actually consumed by users or assistive tech.
- Filenames: do not rename unless the user explicitly asks and all references can be updated safely.
- Embedded charts, SmartArt, and diagram labels: translate only when the underlying object is editable and the chart logic or references remain intact.

## Embedded image and diagram text

- Editable SVG or vector artwork: edit source text objects directly.
- Layered design sources: edit the source file and re-export the image or PDF.
- Flattened screenshots, scanned diagrams, or raster exports: do not paint over text by default. Prefer caption translation, side annotations, or explicit best-effort reconstruction.
- OCR on image text is reference-only unless the thresholds in `decision-thresholds.md` allow automatic reuse.
- If the image text is decorative and not required for understanding, translate only the caption or alt text unless the user asks for image reconstruction.
- If the image text is legally, medically, or procedurally important, require editable source or manual review before replacing it.

## Placeholder handling

- Protect placeholders before translation and restore them after translation.
- Preserve placeholder count, order, and formatting.
- Watch for ICU message syntax, plural rules, and nested templating.
- Keep HTML entities, Markdown link targets, and escaped sequences intact.

## Segment strategy

- Assign stable IDs to every segment before translation.
- Keep enough surrounding context to avoid term drift, but do not merge unrelated segments.
- Preserve deliberate whitespace, list markers, punctuation, and numbering when they carry structure.
- Split mixed-content segments so code or markup remains untouched while visible prose is translated.

## Terminology and style controls

- Apply terminology in this priority order:
  1. Official brand or legal translation
  2. Project glossary or translation memory
  3. User-provided bilingual examples or prior approved output
  4. Domain-standard dictionaries
  5. Model default translation
- Lock brand names, product SKUs, trademarks, internal code names, and approved no-translate terms before translation.
- Keep critical UI terms, chart labels, and recurring documentation phrases absolutely consistent within the same artifact.
- Do not auto-rewrite an already approved segment unless it fixes a glossary conflict, placeholder bug, or factual error. If a locked segment must change, report it.
- Decide once whether acronyms stay unchanged, expand on first mention, or use a localized long form with the original acronym. Then apply that rule consistently.
- Decide whether tone should be literal, marketing-oriented, or instructional before translating.
- Expect language expansion in German, French, Spanish, and many other locales. Expect contraction in some CJK cases.
- Plan for line wrapping, text overflow, and table growth before reinsertion.

## Reporting rules

- State what was translated.
- State what was intentionally protected.
- State how hidden content, metadata, filenames, and embedded image text were handled.
- Call out any segments skipped because safe round-tripping was unclear.
- Mention glossary decisions and locked terms that materially affect the output.

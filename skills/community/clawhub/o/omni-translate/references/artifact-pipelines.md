# Artifact Pipelines

## Contents

- Code and web
- Markdown and docs
- Office containers
- PDFs
- Mixed folders
- Raster text and screenshots
- Subtitles

## Code and web

Use this path for repositories, frontends, static sites, documentation sites, Markdown docs, and apps that render text at runtime.

### Recommended approach

1. Find the true source of user-visible text.
2. Prefer i18n resource files, CMS content, or configuration over raw source rewriting.
3. If strings are hard-coded, extract only the literals or text nodes that are meant for users.
4. Preserve identifiers, imports, class names, props, schema keys, routes, and protocol strings.
5. Rebuild and run tests after reinsertion.
6. Load `format-risk-checklists.md` and `translation-boundaries.md` before touching mixed code-and-copy files.

### High-risk areas

- JSX or template literals that mix code and copy
- Markdown code fences and inline code
- Locales with strong text expansion in narrow layouts
- CSS with fixed widths, `white-space: nowrap`, or absolutely positioned labels
- Generated or minified assets that should never be edited directly

### Validation

- Run the build, tests, and linting if available.
- Visually inspect pages at desktop and mobile breakpoints.
- Check buttons, menus, cards, tables, and form labels for overflow.
- Verify placeholders, links, and interpolation variables remain intact.

## Markdown and docs

Use this path for Markdown repositories, documentation sites, MDX, knowledge-base exports, and text-heavy docs where structure is mostly textual.

### Recommended approach

1. Preserve frontmatter, headings, anchor stability, and code fences.
2. Translate prose, captions, and alt text, but protect commands, filenames, links, and literal snippets.
3. Re-check tables, callouts, and reference-style links after reinsertion.
4. Refresh generated docs output only after the source files validate.

### High-risk areas

- Frontmatter keys mixed with translatable values
- Headings that other pages link to by anchor
- Markdown tables with narrow columns
- MDX or raw HTML embedded in prose
- Images whose meaning depends on untranslated in-image text

### Validation

- Re-render the docs if a toolchain exists.
- Verify headings, anchors, tables, and code fences remain intact.
- Check that localized captions and alt text still match the media they describe.

## Office containers

Use this path for `pptx`, `docx`, and similar editable document bundles.

### Recommended approach

1. Treat the file as a structured container, not a flat binary blob.
2. Extract text with run, paragraph, slide, note, and shape boundaries preserved.
3. Reinsert translated text into the same structural nodes.
4. Keep hyperlinks, speaker notes, comments, headers, footers, and metadata aligned with the source.
5. Open the result in a compatible editor and inspect every page or slide.
6. Apply `locale-sensitive-typography.md` whenever the target locale changes punctuation, glyph width, or font coverage.

### High-risk areas

- Text boxes sized tightly around English copy
- Mixed formatting inside a single paragraph or run
- Tables and charts with fixed cell sizes
- Theme fonts that do not cover the target script
- Embedded diagrams or screenshots containing rasterized text

### Validation

- Open the file in PowerPoint, Word, or LibreOffice.
- Review each page or slide for truncation, overlap, and font fallback.
- Export to PDF when needed and compare the visual result to the source.

## PDFs

Use this path only when the user explicitly needs the PDF translated or when no editable source exists.

### Recommended approach

1. Decide whether the PDF is text-based or scanned.
2. If editable source exists, stop and translate the source instead.
3. For text-based PDFs, extract layout-aware text spans and preserve page coordinates or block structure.
4. For scanned PDFs, use OCR and state clearly that exact fidelity is not guaranteed.
5. Rebuild with font coverage verified for the target language.
6. Run a pilot page first. If any hard-stop threshold in `decision-thresholds.md` triggers, abandon in-place editing and switch to extraction plus rebuild or to the editable source.

### High-risk areas

- Scanned pages and low-quality OCR
- Subset or embedded fonts without target-language glyphs
- Mixed writing directions
- Tables, annotations, and forms
- Legal or compliance PDFs where spacing changes can matter

### Validation

- Review every page for missing glyphs, overlap, clipping, and broken reading order.
- Confirm page count, bookmarks, links, and form behavior if applicable.
- Check for replacement characters, tofu boxes, or silently dropped text.

## Mixed folders

Use this path when a delivery contains both source artifacts and exports, such as a repo plus generated site files, or a `pptx` plus a matching PDF.

### Recommended approach

1. Inventory all artifact types before translating anything.
2. Identify the highest-fidelity source for each output.
3. Translate sources first and regenerate derived artifacts.
4. Do not edit both the source and the derived export unless there is a specific reason.

### Common source priorities

- `pptx` over exported `pdf`
- `docx` over exported `pdf`
- templates or localization files over compiled frontend bundles
- Markdown or CMS content over rendered HTML exports

## Raster text and screenshots

Use this path for screenshots, diagrams, or images whose text is baked into pixels.

### Recommended approach

1. Ask whether an editable source exists.
2. If not, decide whether the image should remain unchanged, receive translated captioning, or be rebuilt from source layers.
3. Use OCR for reference by default, not automatic paint-over replacement.
4. Rebuild the visual in layers or by editing the image only when the user accepts best-effort reconstruction or an editable source exists.
5. Treat the result as best-effort, not lossless round-tripping.

### Validation

- Compare alignment, font substitution, contrast, and readability.
- Make sure translated callouts still point at the right UI or diagram elements.

## Subtitles

Use this path for `srt`, `vtt`, and subtitle-like timing files.

### Recommended approach

1. Preserve cue order, timestamps, and formatting tags unless retiming is part of the request.
2. Translate dialogue, speaker labels, and sound cues according to project style.
3. Re-check line lengths and reading density after translation.

### High-risk areas

- Dense translated cues that remain technically valid but unreadable
- Formatting tags or speaker markers damaged during translation
- Burned-in subtitles or on-screen labels in the video remaining untranslated

### Validation

- Verify subtitle files still parse.
- Spot-check reading density and on-screen overlap in a media player if possible.

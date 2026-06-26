# Quality Gates

## Contents

- Universal gates
- Pass and fail thresholds
- Code and web gates
- Office gates
- PDF gates
- Acceptance report template
- Failure conditions

## Universal gates

- Confirm the output opens without corruption in the native tool or runtime.
- Confirm encoding is valid and no replacement characters appear.
- Confirm placeholder parity between source and target.
- Confirm links, anchors, references, and cross-file relationships still resolve.
- Confirm skipped and protected segments are documented.
- Confirm the target language is consistent and obvious mistranslations are corrected.

## Pass and fail thresholds

These thresholds define whether final delivery passes.

- Placeholder parity must be 100 percent.
- Structured files touched during translation must remain 100 percent parseable.
- Page count and slide count must remain unchanged unless the user explicitly approved a change.
- Critical overflow must be zero. Critical means titles, buttons, form labels, chart labels, table headers, disclaimers, and other text whose clipping changes meaning or usability.
- Replacement characters, tofu boxes, and missing-glyph markers must be zero in touched output.
- Broken links or unresolved references in touched content must be zero.
- Non-critical drift is acceptable only when it stays within the drift tolerance defined in `decision-thresholds.md` and is disclosed in the acceptance report.
- Every intentionally skipped item must appear in the handoff report.

## Code and web gates

- Install, build, and run tests where practical.
- Verify no syntax errors were introduced while translating literals.
- Inspect key pages at desktop and mobile breakpoints.
- Check buttons, forms, nav items, modals, tables, and cards for overflow or clipping.
- Verify locale bundles, fallback chains, and interpolation variables still work.

## Office gates

- Open the file in a compatible editor.
- Review every slide, page, header, footer, note, and comment that was touched.
- Check text boxes, tables, charts, and callouts for truncation or overlap.
- Verify target-language glyph coverage and font fallback behavior.
- Export to PDF if delivery requires it and inspect the exported result.

## PDF gates

- Review every page visually.
- Look for missing glyphs, tofu boxes, clipped lines, overlap, and broken reading order.
- Verify annotations, links, bookmarks, and form fields if they exist.
- Compare source and target page counts and spot-check page geometry.

## Acceptance report template

Use this structure in the final handoff:

- Scope: identify the files, pages, slides, or folders localized.
- Pipeline: state the chosen pipeline and any threshold-based decisions.
- Target locale: name the target language and locale if known.
- Protected content: list what remained intentionally untranslated.
- Placeholder parity: `pass` only if 100 percent.
- Parseability: report valid versus touched structured files.
- Links and references: report whether touched links, anchors, or references remained intact.
- Page or slide count: report source and target counts.
- Critical overflow: report the count and require zero for pass.
- Non-critical drift: report any remaining drift and confirm it is within tolerance.
- Encoding and glyph check: report whether any garbled text or missing glyphs remain.
- Skipped items: list any content intentionally left untranslated or unresolved.
- Residual risks: list any best-effort limitations that still matter.

## Failure conditions

Stop and report the limitation when any of the following is true:

- Only a derived artifact is available and the editable source is required for safe fidelity.
- The artifact depends on fonts that cannot render the target script.
- The source is scanned or rasterized and OCR confidence is too low.
- The file is generated, minified, signed, or otherwise unsafe to edit directly.
- The requested scope would require translating protected machine-readable tokens.

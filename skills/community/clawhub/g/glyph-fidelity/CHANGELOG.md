# Changelog — glyph-fidelity

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.2.0 — 2026-10-08

- **Changed — README:** documents the missing-glyph workflow added in v1.1.0 and the Questions/write-permission contract.

## v1.1.0 — 2026-10-08

### One all-caps tracking formula; ligature fix no longer claims a Figma write

Checked against the Figma Plugin API docs and by reading text layers in a live Figma file
(`Foundations — Symphonia Score (Free)`, Typography page, read-only).

- **Changed — Rule 1:** formula is now `TS = max(3%, min(12%, 160 / FS))` (floor lowered from `5%`
  to `3%`). It replaces the separate "compress to `+3–5%` above 32px" instruction, which
  contradicted the old `5%` floor, and is now the single source for `text-typesetting` Branch A.
  The "use the formula or the bands, not both" choice is gone — there are no bands.
- **Fixed — Rule 3:** `setRangeFontFeatures` and `opentypeFlags` do not exist. The Plugin API has
  no setter for OpenType features; the ligature state is read with `getRangeOpenTypeFeatures` and
  the fix is reported as a step for the user.
- **Fixed — `textCase` value:** `"UPPER"`, not `UPPERCASE`.
- **Changed — README:** formula and Figma behaviour updated; repository link corrected.
- **Added — "Questions" section:** read first, report, then ask; a question only when the value can't
  be read and changes the result; always before a write. Lists the questions this skill may need.
- **Added — Rule 5, missing glyphs:** characters beyond basic Latin checked for font coverage;
  `hasMissingFont` in Figma; glyph-level fallback can only be checked visually. Source: Google Fonts
  Knowledge.

## v1.0.0 — 2026-07-08

Initial release.

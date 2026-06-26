# Locale-Sensitive Typography

## Contents

- When to load this guide
- CJK punctuation and spacing
- Numbers, units, and dates
- Font coverage and fallback
- Vertical text and special layout
- Mixed-script safety rules

## When to load this guide

Load this file whenever the target locale is Chinese, Japanese, Korean, mixed-script, or otherwise sensitive to punctuation, glyph coverage, or locale-specific formatting.

## CJK punctuation and spacing

- Do not insert spaces between consecutive CJK characters.
- Keep code, URLs, file paths, and placeholders untouched even when they appear next to CJK text.
- Follow the project style guide for spaces between CJK and Latin letters or digits. If no guide exists, preserve the source document's spacing pattern consistently instead of normalizing the whole artifact.
- Replace punctuation with locale-appropriate full-width or half-width forms only in user-visible prose, never inside code, structured data, commands, or identifiers.
- Re-check line breaks after replacing punctuation. Chinese and Japanese punctuation often changes break opportunities and can shift tables, labels, and captions unexpectedly.

## Numbers, units, and dates

- Localize numbers, date formats, time formats, and measurement units only when they are user-visible content.
- Preserve version numbers, API names, protocol strings, file paths, and data literals exactly.
- Keep numeric precision, currency codes, and unit conversions unchanged unless the user explicitly asks for unit conversion rather than language translation.
- Ensure locale-specific separators and date order do not break table alignment or parser expectations.

## Font coverage and fallback

- Do not rely on implicit editor fallback for final delivery. Choose an explicit fallback font whenever the original font lacks glyphs for the target script.
- Review touched pages, slides, and labels after any font substitution. CJK fallback can change line height, text width, punctuation placement, and baseline alignment.
- Treat missing glyphs, tofu boxes, or silent fallback to an unapproved font as a failed validation.
- If the source uses Simplified Chinese, Traditional Chinese, Japanese, or Korean branding rules, follow the approved locale-specific brand forms instead of generic script conversion.

## Vertical text and special layout

- Preserve vertical writing direction if the source already uses it. Do not convert vertical text to horizontal unless the user asks.
- Re-check ruby text, stacked labels, narrow callouts, and poster-style typography after translation.
- Avoid automatic tracking or letter-spacing changes in CJK text unless the design system already uses them.
- If a slide, poster, or PDF depends on precise text placement around artwork, treat any manual typography adjustment as part of layout QA, not as optional cleanup.

## Mixed-script safety rules

- Keep brand names, acronyms, and technical tokens in their approved script and casing.
- Decide once whether acronyms stay Latin, are explained on first mention, or are left untouched; then apply that rule consistently.
- When Chinese, Japanese, or Korean text appears alongside English UI terms, confirm spacing, punctuation, and line wrapping on the final rendered artifact, not only in extracted text.
- Review narrow containers such as badges, buttons, charts, and labels individually. Mixed-script text often passes string-level checks but fails visually.

# Changelog — microtypography

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.3.0 — 2026-10-08

- **Added — Rule 1d, functional Unicode spacing:** defines narrow no-break, figure, thin and hair spaces, plus the non-breaking hyphen, with explicit use and non-use cases.
- **Added — compatibility guard:** verify font and renderer support; fall back to `U+00A0` or the original character rather than producing tofu or unreliable line breaking.
- **Added — Figma handling:** insert literal Unicode characters and preserve mixed range styles with the existing end-to-start edit procedure.
- **Verified — live Figma probes:** `textWrapStyle = "PRETTY"` persists; delete/insert replacement preserves mixed range styles; hanging punctuation overhangs `"`, `“`, `„`, `«`, and `(` in Inter but not `—`.
- **Clarified — short-word house rule:** the post-punctuation threshold of up to three letters remains an opt-in editorial heuristic, not a PWN rule. *Polszczyzna na co dzień* (2006, pp. 527–528) was unavailable for verification and is not used as a supporting citation.
- Sources: Unicode Standard Chapter 6, UAX #14, BIPM SI Brochure, NIST SI guidance, and Microsoft Typography whitespace standards.

## v1.2.0 — 2026-10-08

- **Changed — README:** documents the Figma mode added in v1.1.0 and the Questions/write-permission contract.
- **Pending decision at that version:** no rule for thin, hair, narrow no-break, figure spaces or non-breaking hyphens was added before user acceptance; accepted and implemented in v1.3.0.

## v1.1.0 — 2026-10-08

### Figma mode added

Checked against the Figma Plugin API docs and by reading text layers in a live Figma file
(`Foundations — Symphonia Score (Free)`, Typography page, read-only).

- **Added — "Figma Node Integration" section:** which rules apply to wrapping vs single-line text
  nodes; editing with `deleteCharacters` / `insertCharacters` so range styles survive; text driven
  by a variable or a component property is reported, not edited; `textWrapStyle = "BALANCE"` as the
  native counterpart of the CSS `text-wrap` advice; report first, write on request.
- **Changed — Rule 4 (hanging punctuation):** in Figma, uses the native `hangingPunctuation`
  property. The hand-off of an indent computation to `text-typesetting` is removed.
- **Fixed — cross-reference:** "`text-typesetting` Rule 6" → "Step 6".
- **Added — trigger:** a microtypography pass on selected Figma text layers.
- **Changed — README:** repository link corrected.
- **Fixed — dash sources (Rule 1c):** the unspaced em dash is attributed to the Chicago Manual of
  Style, the spaced en dash to Bringhurst §5.2.1. Behaviour is unchanged; only the attribution was wrong.
- **Added — "Questions" section:** read first, report, then ask; a question only when the value can't
  be read and changes the result; always before a write. Lists the questions this skill may need.
- **Still not verified:** behaviour of the Figma mode in the Figma agent; `PRETTY` itself was verified through the Plugin API in v1.3.0.
- **Added — Rule 1, headings vs running text:** titles always fixed, narrow body columns where possible
  (PWN, *Zasady pisowni i interpunkcji*, §54.8.1).
- **Added — Rule 1, short word after a comma:** opt-in house rule, off by default. The three-letter
  threshold is the skillset's own; no published rule was found for it.
- **Added — Rule 2, terms:** Polish names (*wdowa*, *bękart*, *szewc*, *sierotka*) mapped to the
  English terms the skill uses.

## v1.0.0 — 2026-07-08

Initial release.

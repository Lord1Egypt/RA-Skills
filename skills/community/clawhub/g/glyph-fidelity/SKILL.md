---
name: glyph-fidelity
description: Use when checking that letterform-level detail survives a transform — all-caps tracking by a continuous formula, ligature collisions under negative tracking, and inline acronyms needing their own subrange treatment to keep paragraph color even.
triggers:
  use_when:
    - user applies or reviews an ALL CAPS text transform
    - user asks about ligatures breaking under tight tracking
    - user asks how to handle an acronym (HTML, ZUS, USA) inside running prose
    - user asks why a heading "looks wrong" after transforming to uppercase
  do_not_use_for:
    - the base tracking direction/size rules for a text style (see text-typesetting Step 2 — this skill refines edge cases on top of it)
    - number figure styles (see text-typesetting Step 4)
    - hanging punctuation / dash rendering (see microtypography Rule 1c/4, text-typesetting Step 6/7)
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.2.0"
  status: accepted
---

# Glyph Fidelity

## Purpose

Protect letterform structure from the failure modes a naive tracking/case transform introduces — under- or over-tracked all-caps text, ligatures that collapse into illegible blobs under negative tracking, inline acronyms that break the paragraph's even visual "color" (texture) — and from glyphs that silently come from another font.

## When To Use

- Any time text is transformed to all caps (CSS `text-transform: uppercase`, Figma `textCase: "UPPER"`), to compute the correct tracking rather than a guessed round number.
- Reviewing a heading or label where letters look like they're touching or merging.
- Text containing acronyms (3+ consecutive capital letters) inside otherwise sentence-case prose.

## When NOT to use

- This isn't the primary tracking-direction logic — `text-typesetting` Step 2 (Branch A/B) decides *whether* tracking is positive or negative. This skill holds the all-caps formula that Branch A uses and covers the structural side-effects (ligatures, acronym color) that Step 2 doesn't address.

## Inputs

- `font-size` (px).
- The text content itself (to detect ligature-prone letter pairs and inline acronyms).
- Current tracking value, if reviewing an existing style.

## Outputs

- A precise tracking percentage for all-caps runs (continuous formula, not a banded guess).
- Flags for any ligature collision risk, with the fix (disable standard ligatures for that range).
- Flags for inline acronyms, with the subrange fix (own tracking + size adjustment).

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- Whether to simulate small caps or drop them, when the font has no small-caps feature (Rule 2).

## Workflow

### Rule 1 — All-caps tracking (continuous formula)

For any text-run transformed to uppercase, tracking (`TS`) is a function of font-size (`FS`, in px), not a fixed band:

```
TS = max(3%, min(12%, 160 / FS))
```

Reference values: `10px → +12%`, `14px → +11.4%`, `16px → +10%`, `20px → +8%`, `32px → +5%`, `40px → +4%`, `54px` and above `→ +3%`. The `12%` cap keeps very small text from spreading apart. The `3%` floor is there because all-caps text never goes to zero or negative tracking; large display headings (`FS > 32px`) land between `+3%` and `+5%` on their own.

This is the same formula `text-typesetting` Step 2 Branch A uses. There is one source for all-caps tracking, so both skills return the same number for the same size. The font-weight modifier (`text-typesetting` Step 2c) is applied to the result afterwards. In Figma, write it as `letterSpacing = { unit: "PERCENT", value: TS }`.

### Rule 2 — Small caps: never fake it

If `Small Caps` styling is required, never simulate it by shrinking the base font (`fontSize × 0.8`) and capitalizing — this produces thin, spindly letterforms with the wrong stroke weight relative to true small caps, which are drawn by the type designer at the correct weight. Check for and use the native OpenType feature instead:

- CSS: `font-variant-caps: small-caps;` (or `all-small-caps` if lowercase-context is needed too).
- Figma: `textNode.textCase = "SMALL_CAPS"`.
- If the font doesn't expose small caps at all, say so explicitly and let the user decide between a real (but imperfect) simulation and dropping the request — don't silently fake it either way.

### Rule 3 — Ligature collision under negative tracking

Negative tracking (`TS < -2%`, per `text-typesetting` Step 2 Branch B at large sizes) pulls letters closer together. Built-in ligatures (`fi`, `fl`, `ffi`, `ffl`) are pre-drawn as fused glyphs — at sufficiently negative tracking, the already-fused shape can start visually colliding with its neighbors, reading as a blob rather than two/three distinct letters.

- Trigger: tracking value more negative than `-2%` on a text containing ligature-prone pairs.
- Fix: disable standard ligatures for that specific range rather than reducing the tracking further (reducing tracking would undo the heading-tightening `text-typesetting` was asked to do).
  - CSS: `font-variant-ligatures: no-common-ligatures;` on the affected range.
  - Figma: ligatures are the `LIGA` OpenType feature. `textNode.getRangeOpenTypeFeatures(start, end)` reads its state, but the Plugin API has no setter for OpenType features. Report the affected range and ask the user to switch ligatures off for it in the Type settings panel (Details tab). Don't report the fix as applied.
- Only disable ligatures on the specific range that triggered the check — don't disable ligatures globally across a node that also contains normally-tracked text.

### Rule 4 — Inline acronyms break paragraph color

A run of 3+ consecutive capital letters (`HTML`, `ZUS`, `USA`) inside otherwise sentence-case prose reads visually heavier and denser than the surrounding lowercase text — it creates a dark "spot" that breaks the paragraph's even visual texture (what Bringhurst calls color).

- Trigger: any inline run of ≥3 consecutive uppercase letters within sentence-case body text.
- Fix: isolate the acronym into its own subrange and apply:
  - Tracking: `+5%` on that subrange only.
  - Font-size: reduce by `1px` relative to the surrounding body text (a small optical correction — full-size acronyms read as shouting relative to the lowercase around them).
- Don't apply this to acronyms already styled as small caps or already in an all-caps heading (Rule 1 already governs those) — this rule is specifically for inline mixed-case contexts.

### Rule 5 — Missing glyphs

When a font has no glyph for a character, software either shows an empty box ("tofu") or silently takes the character from a fallback font. In an interface the second case is the common one and the harder to spot: a few letters in a word come from a different typeface, slightly off in weight, width or height.

- Trigger: text containing characters beyond basic Latin — Polish letters (`ą ć ę ł ń ó ś ź ż` and their capitals), typographic quotes (`„ ” “`), dashes (`– —`), `×`, currency signs — set in a font that may not cover them. Check every language the interface ships in, not only the one in the mockup.
- Fix: choose a font or a font style that covers the language. Don't replace the characters with look-alikes.
- Figma: `textNode.hasMissingFont` tells you that the whole font is unavailable to the document — report that first, since nothing else about the node can be trusted until it's resolved. A single glyph taken from a fallback font can't be read from the Plugin API: check a screenshot of the node for letters that differ from their neighbours, and say that the check was visual.

## Quality Checklist

- [ ] All-caps tracking computed from the formula and stated with the input `font-size` shown — the same value `text-typesetting` Branch A gives for that size.
- [ ] Small caps verified as a native OpenType feature before use; simulated small caps only used with explicit user awareness.
- [ ] Ligature collision checked whenever tracking is more negative than `-2%`; fix disables ligatures on the affected range only, doesn't further reduce tracking. In Figma it is reported as a step for the user, not applied by script.
- [ ] Inline acronyms (3+ caps) in sentence-case prose isolated into a subrange with `+5%` tracking and `-1px` size, not left at body-text default.
- [ ] Characters beyond basic Latin checked for coverage in every shipping language; `hasMissingFont` reported; glyph fallback checked visually and labelled as such.
- [ ] Figma writes (if any) only applied on explicit request.

## References

- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — even paragraph "color" (visual texture) as a compositor's goal; acronyms and all-caps runs as color-breaking outliers requiring correction.
- Felici, J. (2003). *The Complete Manual of Typography*. Adobe Press — ligature behavior under tight tracking; true small caps vs. faked/scaled capitals.
- Google Fonts Knowledge, "Tofu" and "Language support in fonts" — a missing character shows as tofu when no fallback is available; it should be avoided at all costs.
- OpenType registered features: `liga` (standard ligatures), `smcp`/`c2sc` (small caps).
- Figma Plugin API Docs: `TextNode.textCase`, `TextNode.setRangeLetterSpacing`, `TextNode.setRangeFontSize`, `TextNode.getRangeOpenTypeFeatures` (read-only).
- Related skills: [`text-typesetting`](../text-typesetting/README.md) (base tracking direction/size — this skill refines edge cases on top of it), [`microtypography`](../microtypography/README.md) (character-level text rules independent of a design tool).

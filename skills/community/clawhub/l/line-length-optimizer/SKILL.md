---
name: line-length-optimizer
description: Use when checking or fixing the measure (line length) of a text block — verifying a paragraph or container sits in the 45–75 character range (35–45 on mobile) per Bringhurst/Latin readability guidance, and producing a max-width/ch fix.
triggers:
  use_when:
    - user asks to optimize line length or "measure"
    - user asks for max-width for body text or a container
    - user pastes a paragraph and asks if the column is too wide/narrow
    - user asks for readable column width, desktop vs mobile
  do_not_use_for:
    - headings, labels, or single-line UI strings
    - full type-scale generation (see type-scale-generator)
    - vertical rhythm / spacing between blocks (see vertical-spacing)
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.1.0"
  status: accepted
---

# Line Length Optimizer

## Purpose

Check whether a block of body text sits within a comfortable reading measure, and produce a concrete CSS fix (`max-width` in `ch` or `px`) when it doesn't. Based on the standard typographic range: **45–75 characters per line** on desktop, **35–45** on mobile (Bringhurst, Latin — see References).

## When To Use

- Reviewing a container/component that holds body copy (article, blog post, card description) for readable width.
- The user pastes a paragraph and asks "is this column too wide?" or gives a `max-width`/font-size and asks if it's in range.
- Not for headings, buttons, labels, or anything that's one line by design — measure only matters for wrapping prose.

## Inputs

One of:
- A CSS snippet or container width + font-size (compute expected characters-per-line), or
- A block of text + a stated or assumed container width, or
- Just a block of text with no width given — in that case, output the *recommended* `max-width` rather than judging an existing one.

Target device: desktop, mobile, or both (default: report both).

## Outputs

- Verdict: in range / too wide / too narrow, with the measured or estimated characters-per-line.
- A concrete fix: `max-width: NNch;` (preferred — `ch` scales with font, unlike a fixed `px`) or an equivalent `px` value if the codebase doesn't use `ch`.
- Change log explaining the math, not just the answer.

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- The target device (desktop or mobile), when the container width doesn't make it clear. Without an answer, report both.

## Workflow

1. **Get characters-per-line.**
   - If given a text block: count average characters per line (including spaces) across the paragraph, or estimate from total character count ÷ expected line count if it's reflowing.
   - If given `max-width` + `font-size` (+ `font-family` if known): estimate using `ch` unit semantics — 1ch ≈ the width of "0" in the given font, so `max-width: 65ch` targets ~65 characters regardless of font-size. If the input uses `px` instead of `ch`, note that the actual character count will vary by font and flag it as a reason to prefer `ch`.

2. **Compare against target range.**
   - Desktop: 45–75 characters, 65 is the commonly cited sweet spot (Bringhurst).
   - Mobile: 35–45 characters.
   - Serif body text tolerates the higher end of the range better than sans-serif at small sizes — note this as a soft factor, not a separate hard range.

3. **Verdict + fix.**
   - In range: confirm, no change needed.
   - Too wide: recommend `max-width: 65ch;` (or narrower, e.g. 60ch, if the content is dense/technical) on the text container.
   - Too narrow: recommend removing an over-tight `max-width` or `padding`, or increasing container width — narrow columns cause more line breaks and more ragged/hyphenation pressure, which interacts with `microtypography`'s Rule 3.
   - If mobile and desktop diverge, recommend a responsive value: either two breakpoint-specific `max-width` values, or a `ch`-based value that already scales reasonably since mobile font-sizes are usually smaller too — call out if a media query is actually needed (e.g. desktop uses a much larger font-size, breaking the `ch` scaling assumption).

4. **Report, don't silently edit a stylesheet.** Output the CSS as a suggestion in the response; only apply it to a file if the user explicitly asks you to edit that file.

## Figma Node Integration

When running with Figma access (Figma MCP / plugin context), read the selected node instead of asking the user to paste text:

- **`textNode.textAutoResize`** — determines what "width" even means for this node:
  - `NONE` or `HEIGHT` → the node has a fixed width; read `textNode.width` (or the bounding box) directly and treat it as the measured container width.
  - `WIDTH_AND_HEIGHT` (auto-width) → there is no fixed measure to check; the box grows with content. Flag this instead of computing a verdict — recommend switching to `HEIGHT` (auto-height, fixed width) if the intent is a readable paragraph column, since auto-width text has no line wrap at all.
  - `TRUNCATE` → fixed width and height with the overflow cut off; measure the width as for `NONE`, and flag that part of the text is hidden.
- **`textNode.fontSize`** and **`textNode.fontName.family`** — needed to convert a pixel width into an estimated character count (characters-per-line ≈ width in px ÷ average glyph width, which scales with `fontSize` and varies by typeface — monospace and condensed faces need a different divisor than a default sans).
- **Action back to Figma:** if the fix is "too wide," the agent may resize the node's width directly (set `textNode.resize(newWidth, textNode.height)` or the equivalent plugin API call) to the pixel width corresponding to ~65 characters at the node's current `fontSize`/font — but only when the user has asked for a direct fix, not as a silent default. Otherwise, report the recommended width and let the user apply it.

## Quality Checklist

- [ ] Character count is stated explicitly (measured or estimated), not just "looks too wide."
- [ ] Recommendation uses `ch` unless the codebase's existing convention is `px`/`rem` — match existing convention if shown in the input.
- [ ] Desktop and mobile both addressed, even if the answer is "same value works for both, here's why."
- [ ] Didn't touch headings, labels, or non-wrapping UI text — flag if the user's target isn't actually body prose.
- [ ] If a fix is suggested for a real file, it's proposed, not silently applied, unless the user explicitly asked for a direct edit.
- [ ] Noted the interaction with `microtypography` Rule 3 when the fix affects ragged-edge risk (narrower column → more hyphenation/rag pressure).

## References

- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — standard *measure*: 45–75 characters per line, 66 as the classic ideal.
- Hochuli, J. (2008). *Detail in Typography*. Hyphen Press — how the eye scans a line, and why an optimal word count per line reduces reading fatigue.
- Latin, M. (2017). *Better Web Typography for a Better Web*. — practical `ch`-based implementation for web body text, and the mobile 35–45 character range.
- Figma Plugin API Docs: `TextNode.textAutoResize`.
- Related skill: [`microtypography`](../microtypography/SKILL.md) — apply after fixing measure, since a corrected column width changes where ragged-edge and hyphenation risks actually occur.

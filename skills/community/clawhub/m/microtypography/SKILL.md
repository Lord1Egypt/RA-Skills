---
name: microtypography
description: |
  Polish body text before publishing — Polish or English — by fixing hanging single-letter conjunctions/prepositions, adding orphan guards, flagging widow risks, and handling ragged-edge risks without rewriting copy.
triggers:
  use_when:
    - user asks for microtypography
    - user asks to fix hanging conjunctions or hanging prepositions
    - user asks for sieroty i wdowy
    - user asks for a publishing/typesetting pass on markdown, HTML, or plain text
    - user pastes long-form body copy and asks for typography polish
    - agent has Figma access and user asks for a microtypography pass on selected text layers
  do_not_use_for:
    - code
    - tables
    - short UI labels
    - copywriting or wording rewrites
    - layout work that requires rendered page inspection
license: MIT
model: Claude Sonnet 4.5
compatibility: |
  Designed for Claude Code, Codex, VS Code, OpenCode, Cursor, and GitHub Copilot.
  No external dependencies, no MCP required, no network access at runtime.
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.3.0"
  created: 2026-07-08
  updated: 2026-10-08
  status: accepted
---

# Microtypography

## Purpose

Clean up a block of text at the sentence/paragraph level so it reads well when typeset — no single-letter words stranded at line end, no single-word "orphan" lines left dangling, no unreported widow risk at a column/page break, and no unmanaged ragged-edge risk.

## When To Use

- Before publishing a blog post, landing page copy, case study, or any long-form markdown/HTML content.
- When the user asks to "fix hanging conjunctions", "sieroty i wdowy", "clean up typesetting", "polish this text", or pastes a paragraph and asks for a typography pass.
- Not for code, tables, short UI strings, or single-line labels — there's no line-wrap to protect.

## Inputs

- The text to fix (markdown, HTML, or plain text).
- Target language: Polish, English, or mixed (detect per-paragraph if mixed).
- Output format: same as input by default; ask if ambiguous (e.g. plain text pasted but destined for HTML).

## Outputs

- The corrected text in the same format as the input, with non-breaking spaces inserted and any widow/orphan fixes applied.
- A short change log: what was changed and why (grouped by rule), so the edit is auditable — do not silently rewrite wording.
- For ragged-edge handling: either a direct rewrap for hard-wrapped text, or a non-destructive set of soft-hyphen insertions and CSS/review flags for reflowing text (see Rule 3).
- For hanging punctuation: a CSS suggestion for reflowing output, or the native `hangingPunctuation` switch for Figma display headings (see Rule 4).
- With Figma access: a change log per text node, applied to the nodes only on request (see Figma Node Integration).

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- The language, when a paragraph is too short or too mixed to detect.
- The English dash convention (unspaced em dash or spaced en dash), when the text doesn't already show a consistent one (Rule 1c).

## Workflow

### Rule 1 — Hanging single-letter conjunctions/prepositions (non-breaking space)

Insert a non-breaking space between a single-letter (or otherwise "small") conjunction/preposition and the word that follows it, so it can never be the last character on a line.

**Polish** — single-letter words that must never end a line: `i, a, o, u, w, z, k` (and their capitalized sentence-start forms). Also treat short two-letter forms as strong candidates when local style guides require it: `by, że, aż, iż, ze, we, do, na, od, po, ku` — apply these only if the project's style guide asks for it; the single-letter rule is non-negotiable, the two-letter rule is a style choice.

**English** — single-letter words: `a, I`. English typesetting is generally more lenient than Polish (no hard rule against "a" or "I" ending a line), so treat this as optional polish, not a hard fix, unless the user asks for strict typesetting.

**Headings are stricter than running text.** PWN's spelling rules (§54.8.1) draw the line: in narrow columns, one-letter conjunctions and prepositions may stay at the end of a line in running text, but in titles — of books, chapters, articles and the like — they must always move to the next line. For an interface this means:
- Headings, card titles, dialog titles and any other title that wraps: always fix.
- Body text in a narrow container (a card, a sidebar, a mobile column): fix where it's possible; a leftover is not an error.

**Short word after a comma (opt-in, house rule).** A word of up to three letters that follows a comma, semicolon or colon and opens a clause — `, ale`, `, że`, `, bo`, `, to`, `, czy` — is bound to the next word with NBSP, so it doesn't hang at the end of a line right after the punctuation. Off by default; apply it only when the user or the project's style guide asks. Published PWN guidance cited below covers one-letter words and says requirements for longer words are milder; it does not establish this three-letter, post-punctuation threshold. The threshold and punctuation condition are this skillset's own editorial heuristic, not a published rule. *Polszczyzna na co dzień* (PWN 2006, pp. 527–528) was suggested as a possible lead but was not available for verification, so it is not cited as support.

**Mechanics per format:**
- Plain text / markdown: replace the space after the conjunction with ` ` (non-breaking space, renders as ` ` visually but blocks the line break). In markdown source this is the literal NBSP character, not an HTML entity, unless the target is HTML.
- HTML: use `&nbsp;` between the word and what follows.
- Do not insert NBSP inside code spans, URLs, or already-escaped content.

### Rule 1b — Numbers, units, and dimensions

- **Multiplication sign in dimensions:** in a dimension pattern (`<number> x <number>`, e.g. `1920x1080`, `3 x 4 m`), replace the `x`/`X`/`*` with the proper multiplication sign `×`. Don't touch a bare `x` that isn't between two numbers (variable names, "x-axis", "Grade x").
- **No-break spacing between number and unit/currency:** bind a numeric value to its abbreviated unit or currency code so the pair cannot split: `100 PLN`, `50 m`, `16 px`, `3 kg`. Use the character-selection and locale rules in Rule 1d; currency symbols do not all take the same placement or spacing. Spelled-out words ("100 dolarów") follow ordinary language rules.
- Skip both inside code spans, URLs, and literal code (CSS values like `1920x1080` in a config file are not prose).

### Rule 1c — Smart punctuation

**Dashes — three different characters, three different spacing rules. Don't collapse them into one "make it fancy" transform:**

- **Em dash `—`** (parenthetical break, US convention per *The Chicago Manual of Style*): no surrounding spaces — `word—word`. Replace a double hyphen `--` used this way with a bare em dash, not a spaced one.
- **En dash `–`** as a sentence-level parenthetical break (PL convention, and Bringhurst's recommendation for English, §5.2.1): surrounded by spaces — `word – word` — and those spaces should be NBSP if the dash sits near a line-wrap-risky position (short word before/after), otherwise a regular space is fine.
- **En dash `–` in a numeric/date range** (`10-15kg`, `2020-2023`): **no spaces at all** — `10–15 kg`, `2020–2023`. This is a different use of the same character from the sentence-dash case above; don't apply spacing rules meant for prose to a range. Add the NBSP-before-unit fix from Rule 1b where a unit follows (`10–15 kg`).
- **Hyphen `-`**: never surrounded by spaces, in any context (compound words, prefixes). Don't touch hyphens that aren't standing in for an em/en dash — most hyphens in normal text are correct as-is.
- Confirm which EN house style applies (unspaced em dash vs. spaced en dash) if the input doesn't already show a consistent pattern — don't silently pick one.

**Quotation marks:** detect the paragraph's language and convert straight quotes `"..."` to the typographically correct pair: Polish `„...”`, English `“...”`. Only convert quotes that wrap actual quoted/spoken text — leave straight quotes inside code, JSON, or attribute values untouched.

Both are opt-in-by-default in code-adjacent contexts (README snippets, inline code) — never touch quotes or dashes inside a code span, fenced block, or URL.

**Design-tool context:** if the dash/range sits inside a Figma text node (not markdown/HTML prose), the character choice above still applies, but kerning and per-range tracking around the dash are handled by [`text-typesetting`](../text-typesetting/README.md) Step 6, not here — this skill decides *which character and spacing*, that skill decides *how it renders*.

### Rule 1d — Choose a space by function, not appearance

Unicode spaces encode different behaviour. Do not replace an ordinary or non-breaking space with a narrower character merely because it looks better in one font.

| Character | Use | Do not use for |
|---|---|---|
| Narrow no-break space `U+202F` | Human-facing number–unit and number–currency-code pairs (`16 px`, `100 PLN`), and optional groups of three digits in long numbers (`12 345 678`) when the font and target platform render it correctly | Currency-symbol placement that is controlled by locale (`$10`, `10 zł`), code, data files, or identifiers |
| Figure space `U+2007` | A deliberate blank digit position in tabular numeric display; it has the width of a tabular digit | General word spacing or the default thousands separator; its full-digit width is usually too large |
| Thin space `U+2009` | Manual optical separation where a line break remains acceptable, such as nested quotation marks or a local punctuation collision | Any relationship that must stay on one line; use a no-break character instead |
| Hair space `U+200A` | Exceptional manual optical correction at display sizes, after visual inspection | Automatic cleanup, ordinary prose, number–unit binding, or thousands grouping |
| Non-breaking hyphen `U+2011` | A hyphenated proper name, model, identifier, or short compound whose parts must not split across lines | Every hyphenated word; normal words should retain their usual line-break opportunities |

Rules and fallbacks:

- BIPM requires a space between a numerical value and an SI unit, and permits grouping long numbers in threes with spaces. NIST describes the grouping space as thin, fixed and non-breaking. This skill uses `U+202F` for that digital typesetting role, with `U+00A0` as the compatibility fallback.
- Before inserting `U+202F`, `U+2007`, `U+2009`, `U+200A`, or `U+2011`, verify that the target font contains the glyph/advance and that the target renderer preserves the intended break behaviour. If that cannot be verified, keep ordinary spacing or use `U+00A0`; do not create tofu or an invisible portability bug for a smaller gap.
- Apply number grouping only to human-facing prose and labels, not to four-digit values, years, account numbers, phone numbers, serials, source code, or machine-readable data.
- Thin and hair spaces are optical tools, not semantic glue. Never use them as substitutes for `U+00A0` or `U+202F` where a line break must be prohibited.

### Rule 2 — Widows and orphans

**Terms.** The English and Polish names don't map one to one, so say which one you mean. This skill uses the English terms as defined below. In Polish typesetting: *wdowa* is a very short last line of a paragraph (what this rule calls an orphan), *bękart* is the last line of a paragraph at the top of a new column or page (what this rule calls a widow), *szewc* is the first line of a paragraph left at the bottom of a column, and *sierotka* is a short word left at the end of a line (Rule 1). In an interface there are no page breaks, so *bękart* and *szewc* appear only in multi-column or paginated layouts; the case that matters is the single word on the last line.

- **Orphan** (in typesetting terms as used here: a single word, or a very short line, left alone at the *end* of a paragraph, wrapping to its own line): reflow by tightening wording (rare) or, more practically, by inserting an NBSP between the last two words of the paragraph so they can't be split — the standard cheap fix.
- **Widow** (a short line — often one word — left alone at the *top* of a new column/page after a page break): flag it; fixing it requires knowing the actual line breaks at render time, which this skill can't see from raw text. Note it in the output as "widow risk — verify after layout" rather than guessing a fix.
- Prefer the same NBSP-between-last-two-words technique proactively at the end of every paragraph as a low-cost orphan guard, not just when one is spotted.

### Rule 3 — Ragged edges

Split by whether the text has hard line breaks or reflows.

**Case A — hard-wrapped text** (terminal output, poetry, plain-text captions, README manually wrapped to N columns): this is fixable directly only when the hard line breaks are part of body prose, not code or tables. Recompute the wrap with a best-fit / minimal-raggedness algorithm (minimize the variance of line-end positions across the paragraph — a lightweight Knuth-Plass-style pass, not naive greedy wrap, since greedy wrap maximizes rag). Apply the fix; note the target column width used in the change log.

**Quantified rag threshold** (applies to both cases, but especially narrow containers — mobile, UI cards): measure the longest and shortest line in the paragraph. If `(longest − shortest) / container_width > 20%`, the rag is bad enough to act on, not just cosmetically uneven — this is the trigger point, not a vague "looks ragged" judgment call. Below 20%, leave it; natural word-length variation produces some rag and over-correcting flattens it artificially.

**Case B — reflowing text** (normal markdown/HTML rendered by a browser/CMS): the source doesn't control where lines actually break, so there's nothing to rewrap. Two things are still legitimate to do here, both non-destructive to wording:

1. **Soft hyphens (`&shy;` in HTML, soft-hyphen char `­` in markdown/plain text)** on long, unbreakable words (long Polish compounds, CamelCase, long tokens) so *if* the renderer needs to break there, it hyphenates cleanly instead of overflowing or forcing an ugly gap. Insert at defensible syllable or morpheme boundaries only. If you cannot identify safe break points, do not guess; flag the word for manual review instead.
2. **CSS recommendation** (report, don't silently edit a stylesheet unless asked): `hyphens: auto;` and `text-wrap: pretty;` on body copy, `text-wrap: balance;` on headings. This is the correct fix location for rag in reflowing text — flag it as a suggested CSS change alongside the text output.

Do not reword sentences to control line length in Case B — that changes content, not typesetting, and violates the "don't alter wording" rule. If reflow genuinely looks bad only after rewording could fix it, offer it as an explicit **opt-in suggestion** the user must accept separately, never auto-applied.

### Rule 4 — Hanging punctuation

A punctuation mark sitting at the very start or end of a line of text (an opening quote, dash, bullet, or parenthesis) reads as breaking the column's optical edge, even though it's technically inside the margin — the eye aligns to the letterforms, not the punctuation. Hanging punctuation pushes that mark slightly outside the block so the *letters* line up cleanly.

- **Reflowing HTML/markdown (Case B territory):** recommend the CSS property `hanging-punctuation: first last;` on the paragraph/block — this is the correct, native fix and needs no text-level change. Report it as a suggestion alongside other CSS recommendations (Rule 3 Case B), don't silently add it to a stylesheet.
- **Plain text/markdown source:** nothing to do — hanging punctuation is a rendering-layer property, not something the source text encodes. Don't attempt a manual workaround (extra spaces, etc.) here.
- **Design-tool context (Figma):** Figma has a native switch, `textNode.hangingPunctuation`. For a display heading (≥24px) that opens with `"`, `“`, `„`, `«`, or `(`, report it and, on request, set `hangingPunctuation = true` — a live Inter probe confirmed left overhang for those marks. The same probe did not move an opening em dash (`—`), so don't promise that the native switch will hang it. See Figma Node Integration. No indent value needs computing.
- Only applies to headings/display text and the first/last line of justified or visually-prominent blocks — not worth flagging for ordinary body paragraphs where the effect is negligible.

### Steps

1. Detect language per paragraph (or ask if ambiguous).
2. Apply Rule 1 across the whole text.
3. Apply Rule 1b (dimensions and number–unit binding), Rule 1c (smart dashes and quotes), and Rule 1d (functional space choice), skipping code/URLs.
4. Apply Rule 2 at the end of every paragraph, plus flag any widow risk near page/column breaks if such breaks are indicated in the input.
5. Apply Rule 3: if the input has hard line breaks, rewrap using the minimal-raggedness pass (Case A); otherwise insert soft hyphens on long unbreakable words and report a CSS suggestion (Case B) — never skip silently.
6. Apply Rule 4: recommend `hanging-punctuation: first last;` for reflowing HTML/CSS output; in Figma, flag eligible display headings and set `hangingPunctuation` on request.
7. Return corrected text + change log + any manual-review flags.

## Figma Node Integration

When running with Figma access, work on the selected text nodes instead of asking the user to paste text.

- **Which rules apply to which node.** Rules 1b and 1c (units, dimensions, dashes, quotes) apply to any text node. Rules 1, 2 and 3 only matter where text wraps: `textAutoResize` is `"HEIGHT"`, `"NONE"` or `"TRUNCATE"` and the content runs to more than one line. Skip them on single-line labels and on auto-width nodes (`"WIDTH_AND_HEIGHT"`), which never wrap.
- **Read:** `textNode.characters`, `textAutoResize`, `fontSize`, `textWrapStyle`, `hangingPunctuation`. A non-breaking space in `characters` is the literal character U+00A0; a soft hyphen is U+00AD. HTML entities mean nothing here.
- **Special spaces in Figma.** Insert the literal Unicode character (`U+202F`, `U+2007`, `U+2009`, `U+200A`, `U+2011`), never an HTML entity. Treat every insertion as a character edit and preserve range styles with the same end-to-start `deleteCharacters` / `insertCharacters` procedure. If the font or screenshot shows tofu, a missing advance, or unexpected width, revert to `U+00A0` or the original character and report the compatibility fallback.
- **Leave these nodes alone and report them instead:** text driven by a variable (`boundVariables.characters`) or by a component property (`componentPropertyReferences.characters`). The fix belongs in the variable value or the component property, not in the layer.
- **Write without losing range styles.** Assigning `textNode.characters = ...` on a node with mixed styles (a bold word, a link) flattens it to one style. Replace character by character instead: `deleteCharacters(start, end)` then `insertCharacters(start, text, "BEFORE")`, working from the end of the string to the start so earlier indices stay valid. Load every font the node uses first (`getStyledTextSegments(["fontName"])`, then `figma.loadFontAsync` for each).
- **Rule 3 in Figma.** There is no stylesheet to recommend. For headings and short display blocks, set `textWrapStyle = "BALANCE"` — the native counterpart of `text-wrap: balance`. Don't insert soft hyphens unless the user asks: they stay in the copy when it is handed off. The 20% rag threshold can't be read from the node, because the Plugin API doesn't expose line boxes; judge it from a screenshot of the node, or say that it wasn't measured.
- **Rule 4 in Figma.** For a display heading (≥24px) that opens with `"`, `“`, `„`, `«`, or `(`, offer `hangingPunctuation = true`. A live Inter probe confirmed those marks and found that `—` does not move. This is a native text property; no indent needs computing.
- **Dashes.** This skill still decides only *which character and spacing*. Kerning and local tracking around a dash at display sizes belong to `text-typesetting` Step 6.
- **Action back to Figma:** report the change log first (node name, rule, before → after). Write to the nodes only when the user asks for a direct application.

## Quality Checklist

- [ ] No single-letter PL conjunction/preposition (`i, a, o, u, w, z, k`) ends a line — verify by checking each occurrence got an NBSP, not just a regex pass.
- [ ] EN `a`/`I` handled per requested strictness (default: leave as-is unless asked for strict mode).
- [ ] Dimension `x` correctly converted to `×` only between two numbers, never touching variable/axis names.
- [ ] Numbers bound to units/currency codes with the Rule 1d no-break character; currency symbols follow locale; numeric ranges use an en dash and keep the following unit with the number.
- [ ] Special spaces follow Rule 1d: narrow no-break for supported number–unit/grouping cases, figure space only for blank digit positions, thin/hair spaces only for inspected optical corrections, and non-breaking hyphen only where a split would be harmful.
- [ ] Target font and renderer support checked before special spaces are inserted; compatibility fallback reported when used.
- [ ] Dashes and quotes converted per detected language, and only in prose — not inside code, URLs, or attribute values.
- [ ] No paragraph ends in a single stranded word (orphan) — last two words of every paragraph joined with NBSP.
- [ ] NBSP not inserted inside code, URLs, or markup attributes.
- [ ] Output format matches input format (or the explicitly requested one).
- [ ] Change log lists every rule applied, not just a diff.
- [ ] Ragged-edge: Case A (hard-wrapped) shows before/after rewrap; Case B (reflowing) lists soft-hyphen insertions and the CSS suggestion, not left blank.
- [ ] Wording itself was not altered beyond what's needed for orphan-joining — this is a typesetting pass, not a copy edit. Any reword-for-rag suggestion is clearly marked opt-in, separate from applied changes.
- [ ] Rule 1/Rule 2 overlap checked: if the paragraph's last word pair already got an NBSP from Rule 1 (e.g. ends in "... w trakcie."), don't apply a second, redundant NBSP for the orphan guard — note the overlap instead of double-binding.
- [ ] Hanging punctuation: CSS suggestion given for reflowing output; in Figma, eligible display headings flagged and `hangingPunctuation` set only on request.
- [ ] In Figma: text replaced with `deleteCharacters`/`insertCharacters`, never by reassigning `characters` on a mixed-style node; variable- and property-driven text reported, not edited.

## References

- Felici, J. (2003). *The Complete Manual of Typography*. Adobe Press — widow/orphan control and paragraph-level polish as core typesetting hygiene, distinct from page-level (macrotypography) concerns.
- Mittelbach, F. & Goossens, M. et al. — LaTeX `microtype` package documentation — the term of art *microtypography*: character/word-level spacing and hyphenation control, as distinct from macrotypography (grid, columns, page layout).
- Polska norma redakcyjna (Wolański, A. (2008). *Edycja tekstów. Praktyczny poradnik*. PWN) — niełamliwa spacja po spójnikach i przyimkach jednoliterowych jako standard redakcyjny; odzwierciedlona w regułach autokorekty InDesign "Polish rules".
- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — hanging punctuation: optical margin alignment for quotes, dashes, and other marks at line/column edges; §5.2.1, spaced en dashes rather than em dashes to set off phrases.
- *The Chicago Manual of Style* (17th ed., 2017). University of Chicago Press — the unspaced em dash as the US publishing convention.
- CSS Working Group: `hanging-punctuation` property (`first`, `last`, `force-end` values) — native browser implementation of the same principle.
- Figma Plugin API Docs: `TextNode.characters`, `TextNode.insertCharacters`, `TextNode.deleteCharacters`, `TextNode.textWrapStyle`, `TextNode.hangingPunctuation`.
- PWN. *Zasady pisowni i interpunkcji*, §54.8.1 [204] — one-letter conjunctions and prepositions may stay at the end of a line in running text in narrow columns; in titles they must always move to the next line.
- Bańko, M. *Poradnia językowa PWN*, "słowa jednoliterowe na końcu wiersza" — an editorial rule, not a spelling rule; it concerns one-letter words, and the requirements for longer words are milder.
- Unicode Consortium. *The Unicode Standard*, Chapter 6, "Space Characters" — `U+2007` figure space has tabular digit width; `U+2009` thin space and `U+200A` hair space are progressively narrow spaces; `U+00A0` is the non-breaking counterpart of the ordinary space.
- Unicode Consortium. *Unicode Line Breaking Algorithm (UAX #14)* — no-break behaviour of `U+00A0`, `U+202F`, `U+2007`, and `U+2011`.
- BIPM. *The International System of Units (SI Brochure)*, §§5.4.3–5.4.4 — a space separates a number from its unit; long digit strings may be grouped in threes with spaces.
- NIST. *Writing with SI (Metric System) Units* — technical writing uses a thin, fixed, non-breaking space for digit grouping.
- Microsoft Typography. *Character design standards — Space characters for Latin 1* — reference advance widths and intended typographic roles of figure, thin, and hair spaces.
- Wikipedia (pl), "Sierotka (typografia)" and "Bękart (typografia)" — Polish terms; secondary source, citing PWN, Felici and Wolański.
- Related skill: [`text-typesetting`](../text-typesetting/README.md) — Step 6 handles kerning and local tracking around dashes in Figma; Step 7 reaches the same hanging-punctuation switch from the type-style side.

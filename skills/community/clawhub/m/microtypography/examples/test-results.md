# Microtypography skill — test run

Manual dry-run of `skills/microtypography/SKILL.md` against four cases: PL reflowing markdown, EN reflowing markdown (strict mode), Case A hard-wrapped rewrap, Case B soft-hyphen + CSS suggestion. Run by following the skill's own Steps 1–5 and Quality Checklist.

**Notation used below** (source markdown would contain the real invisible characters, not these glyphs):
- `␣` = non-breaking space (U+00A0)
- `­` = soft hyphen (U+00AD) — visible only if the renderer decides to break there

---

## Test 1 — Polish, reflowing markdown

**Input**

> Projekt i wdrożenie systemu wymagały ścisłej współpracy z zespołem. To był proces, w którym każdy detal miał znaczenie, a ostateczny efekt zależał od jakości komunikacji i determinacji zespołu.

**Language detected:** Polish (single paragraph).

**Output**

> Projekt i␣wdrożenie systemu wymagały ścisłej współpracy z␣zespołem. To był proces, w␣którym każdy detal miał znaczenie, a␣ostateczny efekt zależał od jakości komunikacji i␣determinacji␣zespołu.

**Change log**

- Rule 1 (PL single-letter conjunctions/prepositions): `i`, `z`, `w`, `a`, `i` each got NBSP before the following word (5 occurrences).
- Rule 1 two-letter forms (`od`): left alone — two-letter rule not requested, default off.
- Rule 2 (orphan guard): last two words of the paragraph (`determinacji zespołu.`) joined with NBSP.
- Rule 2 (widow): no page/column break indicated in input — nothing to flag.
- Rule 3: reflowing prose, Case B — no long unbreakable PL compounds present, so no soft hyphens needed. No CSS change needed beyond the standing recommendation (see Test 4).

**Checklist**

- [x] No single-letter PL conjunction ends a line (all 5 have NBSP)
- [x] Orphan guard applied at paragraph end
- [x] No widow indicators in input — correctly not fabricated
- [x] NBSP not inserted into code/URLs (none present)
- [x] Output format = input format (markdown)
- [x] Wording unchanged

---

## Test 2 — English, reflowing markdown, strict mode

User asked for strict handling of single-letter `a`/`I` (not the default-lenient mode).

**Input**

> I know a plan like this takes time, and I trust the team to deliver it well.

**Output**

> I␣know a␣plan like this takes time, and I␣trust the team to deliver it␣well.

**Change log**

- Rule 1 (EN strict mode): `I` (×2) and `a` (×1) each got NBSP before the following word.
- Rule 2 (orphan guard): last two words (`it well.`) joined with NBSP.
- Rule 3: reflowing, Case B — no long unbreakable tokens present, nothing to hyphenate.

**Checklist**

- [x] `a`/`I` handled per requested strictness (strict → fixed, confirmed opt-in not silently applied elsewhere)
- [x] Orphan guard applied
- [x] Wording unchanged
- [x] Output format = input format

**Note:** confirms the skill correctly treats EN Rule 1 as opt-in — this run only applied it because strict mode was explicitly requested, matching the "leave as-is unless asked" default.

---

## Test 3 — Ragged edges, Case A (hard-wrapped text)

Simulates a manually wrapped plain-text block (e.g. terminal output or a README pinned to a column width) with an intentionally bad, high-variance wrap.

**Input** (hard-wrapped, note wildly uneven line lengths)

```
This is a short line that ends here abruptly
and then this next line goes on for way longer than the first one did
short
another quite long line filled with words
```

Line lengths: 45, 71, 5, 42 — high variance, visibly ragged, one near-empty line.

**Output** (rewrapped at target width 40, minimal-raggedness pass)

```
This is a short line that ends here
abruptly and then this next line goes
on for way longer than the first one
did short another quite long line
filled with words
```

Line lengths: 36, 38, 37, 34, 18 (last line naturally shorter — end of paragraph, not a defect).

**Change log**

- Rule 3, Case A: detected hard line breaks in input → reflowed the whole paragraph and rewrapped at 40 columns using a best-fit pass instead of the original ad-hoc breaks. Target width noted here since it wasn't specified by the user — flagged as an assumption to confirm.
- Rule 1/2 also re-checked after rewrap (none applicable — no PL/EN single-letter words at risk here, last line is the natural paragraph end, not an orphan).

**Checklist**

- [x] Recomputed wrap, not just flagged
- [x] Target column width stated explicitly (assumption to confirm with user)
- [x] Line-length variance reduced (71/5 spread → 36–38 spread, +18 tail)
- [x] Before/after both shown in change log

---

## Test 4 — Ragged edges, Case B (reflowing text, soft hyphen + CSS)

**Input** (HTML paragraph, long unbreakable Polish compound word)

```html
<p>Kluczowym wyzwaniem projektu okazała się nieprzewidywalność wymagań klienta w trakcie sprintu.</p>
```

**Output**

```html
<p>Kluczowym wyzwaniem projektu okazała się nie&shy;prze&shy;wi&shy;dy&shy;wal&shy;ność wymagań klienta w&nbsp;trakcie&nbsp;sprintu.</p>
```

(`&nbsp;` is used because the target format is HTML.)

**Change log**

- Rule 3, Case B: `nieprzewidywalność` (19 chars, no natural break point) is long enough to risk overflow or an ugly forced break in a narrow column → inserted soft hyphens (`&shy;`) at syllable boundaries. No other words in this sentence qualified.
- Rule 1: `w trakcie` → `w&nbsp;trakcie`.
- Rule 2: last two words (`trakcie sprintu.`) joined as `trakcie&nbsp;sprintu.`. This creates a three-word protected phrase with Rule 1 (`w&nbsp;trakcie&nbsp;sprintu.`), which is acceptable because both protections apply to different word pairs.
- **CSS suggestion** (reported, not auto-applied): add `hyphens: auto; text-wrap: pretty;` to the body-copy class, and `text-wrap: balance;` to headings, as the actual fix location for reflow rag in the browser.

**Checklist**

- [x] Soft hyphens only in long unbreakable word, at syllable boundaries
- [x] CSS suggestion reported separately from the text edit, not silently added to a stylesheet
- [x] No reword applied to control line length — none needed here, and none would've been auto-applied per the opt-in rule
- [x] Rule 1/2 interaction noted explicitly and applied to the correct final word pair

---

## Summary

All four cases pass the skill's own checklist. Two gaps found during the dry-run and already fixed in `SKILL.md`:

1. Rule 3 originally said "skip ragged-edge checks for reflowing prose" — too weak, gave no actionable output for the common web-content case. Replaced with the Case A / Case B split (rewrap vs. soft-hyphen + CSS) so the skill always produces something concrete.
2. Rule 1/Rule 2 overlap (a word pair that's already NBSP-bound by Rule 1 shouldn't get a second, redundant NBSP from Rule 2) was added as an explicit checklist line so future runs don't double-apply the same pair.

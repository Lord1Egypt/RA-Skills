# Proofreading and Layout Audit

## Aim

Perform a final mechanical pass after logic and continuity decisions are stable.
Correct errors without flattening voice, dialect, intentional fragments, or genre rhythm.

## Check

- Typographical errors, duplicated or missing characters/words
- Chinese and English punctuation consistency
- Mismatched quotation marks, brackets, ellipses, and dashes
- Character names, titles, honorifics, terminology, capitalization, and numerals
- Paragraph breaks, dialogue speaker changes, headings, lists, and Markdown layout
- Accidental repeated sentences or near-duplicate paragraphs
- Broken references such as “the former/latter,” pronouns, dates, chapter numbers, or footnotes
- Extra spaces, inconsistent full-width/half-width punctuation, and malformed links

## Missing-Word And Sentence-Skeleton Pass

Run this after plot, argument, and continuity edits so later rewrites do not reintroduce
omissions.

1. Reduce each sentence to subject -> predicate -> required object/complement. Check
   whether transitive verbs, result complements, quantities, and head nouns still have
   the slots their meaning requires.
2. Circle structural words: 把, 被, 对, 向, 从, 给, 让, 使, 比, because, if, although,
   and similar connectors. Confirm that each has an object or matching clause and does
   not stop at punctuation.
3. Compare parallel clauses slot by slot. A missing verb, object, classifier, negative,
   or repeated name often appears as an unexplained asymmetry.
4. Resolve pronouns, former/latter references, omitted subjects after speaker changes,
   and dialogue attributions against the nearest valid antecedent.
5. Read the repaired sentence in its neighboring context. Insert a word only when the
   intended slot is uniquely recoverable; otherwise mark the ambiguity for the author.

Do not use fluent rewriting to hide uncertainty. Report the original span, the missing
slot, the minimal insertion, and why that insertion is recoverable.

## Preserve

- Intentional spoken repetition, hesitation, self-correction, dialect, and slang
- Deliberate sentence fragments and rhythm
- Technical notation and quoted source wording
- Established house style when it differs from a generic style guide

## Method

1. List exact locations and original text.
2. Classify each item as definite error, consistency choice, or authorial style.
3. Apply only definite corrections automatically.
4. Present ambiguous consistency choices separately.
5. Do not rewrite plot, argument, characterization, or tone during proofreading.
6. Make a final omission-only pass after corrections; verify that every edit leaves a
   grammatically and semantically complete sentence skeleton.
7. In dialogue, first test whether a particle, hesitation, subject drop, contraction,
   or fragment is recoverable from speaker and turn context. Preserve it when intentional;
   restore only a uniquely recoverable required slot.

## Output

```text
Proofreading Audit
- Definite corrections:
- Possible omissions: location / broken slot / minimal repair / confidence
- Consistency decisions needed:
- Layout and formatting fixes:
- Intentionally preserved forms:
```

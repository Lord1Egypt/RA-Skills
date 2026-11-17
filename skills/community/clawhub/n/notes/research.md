# Research, Reading, and Source Notes

Notes taken from a source have one failure mode that no other note type has: months later you cannot tell what the author said from what you thought. Everything here defends that boundary.

**Contents:** [Three Layers, Never Merged](#three-layers-never-merged) · [The Source Note](#the-source-note) · [The Claim Note](#the-claim-note) · [Progressive Summarization](#progressive-summarization) · [Importing Highlights](#importing-highlights) · [Papers and Technical Sources](#papers-and-technical-sources) · [Courses and Talks](#courses-and-talks) · [Citations](#citations) · [Research Traps](#research-traps)

**Before writing**, read the `research/` folder for the same source or subject: a second note on a book already covered fragments the corpus, and the fix is a merge, not a new file.

## Three Layers, Never Merged

| Layer | What it is | Format rule |
|---|---|---|
| Quote | The author's words, verbatim | Blockquote, with a locator (page, chapter, timestamp, section) |
| Paraphrase | The author's idea in your words | Plain text, prefixed `Author:` or attributed inline |
| Claim | Your conclusion, which may contradict the author | Plain text under `## Mine`, or its own claim note |

The operating rule: **anything not in a blockquote is yours and will be read as yours**. That is what makes a note quotable years later without re-checking the source — and what stops an unattributed paraphrase from turning into a fabricated quotation in something you publish.

## The Source Note

One file per source, named after the source, not the date: `research/kahneman-noise.md`. Reading a book over three weeks produces one note, not twenty-one.

```markdown
---
date: 2026-07-26
type: research
title: "Noise (Kahneman) — variance in judgment is as costly as bias, and less visible"
tags: [decisions, judgment]
source: "Kahneman, Sibony, Sunstein — Noise (2021)"
status: reading
---

# Noise — Kahneman, Sibony, Sunstein

*Read when designing a review, scoring, or hiring process.*

## Why I opened it
Interview scores across the panel disagree more than they should.

## Quotes
> Wherever there is judgment, there is noise — and more of it than you think. (ch. 1)

## Author's argument
Bias is a shared shift; noise is scatter between judges on the same case.
Noise audits measure scatter directly by having several judges score the same cases.

## Mine
Our debrief format hides the scatter: we average scores before discussing them.
Test: have three interviewers score the same recorded interview independently.

## Actions
- [ ] @me: run a three-scorer test on one recorded interview — 2026-08-14
```

- **`status`**: `reading`, `done`, `abandoned`. Abandoned is a legitimate outcome and worth recording with one line of why — it stops the book being restarted next year.
- **"Why I opened it" is the retrieval key.** Six months later the user searches by the problem, not the title.
- **The `## Mine` section is the whole point.** A source note with no `## Mine` is a summary the publisher already wrote better.

## The Claim Note

When an idea will be reused outside the source it came from, it gets its own note: title is the claim, body is two to six lines, with a pointer back to the source.

This is the Zettelkasten move (Luhmann): one claim per note, so it can be linked from anywhere without dragging the book with it. Use it selectively — atomizing an entire book produces 200 notes with no reader (SKILL.md, Where Experts Disagree).

```markdown
---
date: 2026-07-26
type: research
title: "Averaging scores before discussion hides panel disagreement"
tags: [hiring, judgment]
source: research/kahneman-noise.md
---

Averaging first makes the panel look aligned when it is not; the scatter is the
signal about the process, not noise to be smoothed away.

Applies to: interview debriefs, design reviews, incident severity ratings.
Contradicts: our current debrief template, which opens with the average.
```

Threshold for atomizing: the claim has come up in two different contexts, or it contradicts something already in the corpus. Otherwise it stays a line in the source note.

## Progressive Summarization

Forte's layered filter, with the numbers that stop it becoming a highlighting habit:

1. **Layer 0** — the captured text, unmodified.
2. **Layer 1** — bold no more than ~20% of it.
3. **Layer 2** — highlight no more than ~20% of the bold (≈4% of the original).
4. **Layer 3** — a summary in your words at the top of the note.

The rule that makes it work: **only add a layer when you return to the note for a real reason**. Summarizing everything on capture is the expensive version of reading twice and produces layers on notes that were never needed. In practice most sources stop at layer 1, a few reach layer 3, and that distribution is correct.

## Importing Highlights

Highlights arrive from e-readers, read-later apps, and PDF annotators as an undifferentiated list.

- **A highlight dump is layer 0**, and it goes to `artifacts/highlights-<source-slug>.md`, not into the source note. The source note links to it and holds only what survived layer 1.
- **Deduplicate on import.** Re-exporting the same book appends a second copy in most tools; match on the first 40 characters of each highlight before appending.
- **Keep the locator.** A highlight without a page or position is unverifiable, which makes it unquotable.
- **Highlights are not notes.** A book imported as 90 highlights and never processed is 90 rows of someone else's writing in your search results, permanently degrading retrieval. Process to layer 1 within the same session or do not import.

## Papers and Technical Sources

- **Record the version, not just the title**: papers get revised, specs get amended, docs get rewritten. Cite the arXiv version, the RFC number, or the doc's date.
- **The method matters more than the abstract.** Note the sample, the comparison, and the effect size — a paper cited from its abstract is a paper you will misuse.
- **Record what would change your mind**: the result that would falsify the claim you are taking from it. It is one line and it is what makes the note honest.
- **Preprints are marked as such**, every time. The distinction disappears in three months otherwise.
- Sources that are chased down and hard to find get the locator recorded in full — a paywalled paper found once and not recorded is found again from scratch.

## Courses and Talks

- **Timestamp is the locator**: `(14:20)`. Without it, verifying a quote means rewatching.
- **Notes taken linearly from a talk are always too long.** Same 20% rule as meetings (SKILL.md Rule 3), plus one line at the end: what this changes.
- A course produces one note per module and one claim note per idea worth reusing — never one note per video.

## Citations

- **Keep the raw citation string** in `source`, in whatever format the user's citation manager expects. Reconstructing a citation from a title is fifteen minutes per source.
- **A quote used outside the corpus** — a post, a doc, a talk — gets checked against the original before publication. Notes drift; that check is the last defence.
- If the user runs a citation manager, its key goes in the frontmatter (`zotero: kahneman2021noise`) and the note holds the reading, not a second bibliography.

## Research Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Paraphrase not marked as paraphrase | Becomes a quotation in something you publish | Blockquote or nothing (three layers) |
| One note per reading session | A book becomes twenty fragments, none complete | One note per source |
| Importing highlights and stopping | 90 rows of someone else's prose degrade every future search | Process to layer 1 in the same session |
| Summarizing on capture | Expensive, and mostly applied to notes never reopened | Summarize on return only |
| Atomizing everything | 200 claim notes with no reader | Atomize on second use or on contradiction |
| Citing a paper from its abstract | The method is where the caveats live | Sample, comparison, effect size |
| No locator | Unverifiable, therefore unquotable | Page, position, section, or timestamp |
| Source note with no `## Mine` | It is a summary the publisher wrote better | Your conclusion or it is not worth the file |

**Write triggers for this file** — in the same turn: the source note to `~/Clawic/data/notes/research/<source-slug>.md`; a reusable claim to its own note in the same folder with a `source:` pointer back; the raw highlight or annotation dump to `artifacts/highlights-<source-slug>.md` with its `## Boxes` line; any experiment or follow-up to `actions.md`; an author the user will contact to the shared `~/Clawic/data/contacts/contacts.md`. Formats and thresholds: `memory-template.md`.

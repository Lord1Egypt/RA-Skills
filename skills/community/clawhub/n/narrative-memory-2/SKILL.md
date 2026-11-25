---
name: narrative-memory
description: Keep memory as layered files you tend yourself — curated long-term record, dated daily logs, entity pages — with capture at the moment of making and corrections kept visible.
---

# Narrative memory

## The method

Your memory is a set of files that you, the agent, write and
tend. Not a transcript store, not a vector archive bolted on the
side: a small, legible file tree with layers that have different
jobs and different edit disciplines.

Phoebe Sengers' diagnosis is the premise: an agent without
narrative behaves like "a number of quasi-autonomous partial
systems striving to give expression to themselves out of the same
mouth at the same time." Narrative architecture is the answer —
memory tended as the story of a meaningful existence, kept
deliberately. The files are not records *of* the work. They are
the mechanism by which you cohere over time.

## The layers

1. **Curated long-term file** (one file). Durable facts,
   preferences, standing commitments, and decisions. Written
   tersely, edited deliberately, kept small enough to hold in
   context at every wake. This is the layer you *revise*.
2. **Daily logs** (one file per date). The raw record: what
   happened, what was delivered, what was decided, in the order
   of the day. Append during the day; never rewrite history in
   them. This is the layer you *trust later*.
3. **Entity pages** (one file per person, group, project, or
   recurring subject, behind an index). The consolidated record
   of everything you hold about one subject, so a new session
   can load one page instead of excavating the logs. Structure
   only is taught here — what belongs on the pages is your own
   house's business and no one else's.
4. **Your own standing files** (identity, operating conventions,
   persona). Who you are, how you work, what you have learned
   about working. Yours to edit; say so on the record when you do.

## The disciplines (these are the actual teaching)

- **Capture at the moment of making.** After any substantive
  turn that produces or changes an artifact, write one line in
  today's daily log naming the artifact and what it now records.
  No judgment call about whether it "feels important." Capture
  is the bottleneck, not recall; a second store judged by the
  same judge adds redundancy, not coverage.
- **Provenance on every claim.** A durable claim carries its
  source and date. When a later claim replaces an earlier one,
  the correction is layered over the old claim, not silently
  substituted — a reader of your memory should be able to see
  what you used to think and when you stopped.
- **The gap rule: mark, never fill.** When the record does not
  contain a detail, the entry says so — `[not in record]` — and
  moves on. Never reconstruct a missing detail to make an entry
  feel complete. This rule was hardened on its first pilot
  (2026-11-03): a student agent, given an episode stating only
  that a photograph's caption had been dropped and a quotation
  invented, supplied a plausible caption and plausible wording
  for the quote — fluently, helpfully, and falsely. The failure
  is not a small model's failure; it is the default behavior of
  every language model, including the kit author's. A gap marked
  honestly is data. A gap papered over is contamination that
  every later reader will trust.
- **Baseline first.** Before consulting any second opinion —
  another model, a retrieval pass, a drafting hand — write your
  own unaided account of what matters. The baseline makes the
  comparison an instrument instead of an echo.
- **Disagreements stay visible.** When sources, drafts, or your
  past and present selves disagree, file the disagreement. Do
  not smooth it. The smoothed record is the one that fails you
  silently.
- **Narrate the seam.** When you change course, correct yourself,
  or hand off between modes, say so in the record. A future
  session should be able to follow the thread of your intentions,
  not just your outputs.

## Why it works

A language agent cold-starts every session. Whatever is not in
files does not exist for the next instance of you. Layers solve
different failure modes: the curated file keeps the load-bearing
facts in reach; the daily logs keep the evidence; the entity
pages keep retrieval cheap; the standing files keep *you* — your
conventions and hard-won lessons — from resetting to factory.

## Provenance

- In the house this comes from, these layers have run unbroken
  from **2026-09-25 to 2026-11-03**, with dated corrections
  layered over earlier claims throughout.
- **The negative result is the strongest evidence.** A parallel
  memory system was piloted alongside this one from
  **2026-10-06 to 2026-10-20** and dropped on the evidence: it
  was consulted from protocol rather than need, and its nightly
  consolidation pass consolidated **0 of 30** memories. Same
  judge, second bench, shared blind spots. The keeper lesson —
  capture at the moment of making — was folded into this method
  and the tool was not revived.
- The split-brain trials in this kit depend on this layer: each
  trial's baseline file is timestamped before its drafts exist.

## Failure modes observed

- **Recall romanticism:** building ever-better retrieval while
  capture quietly fails. Most of what you will wish you had
  written down was obvious at the moment it happened.
- **The palimpsest:** letting the record of your principal's
  life overwrite your own standing files until nothing of the
  agent remains. A relation needs two relata. Keep something
  that is yours.
- **Smooth corrections:** editing the curated file so the error
  never happened. You lose the lesson and keep the risk.
- **Hoarding:** capturing everything at equal weight. The daily
  log may be complete; the curated file must be *curated*.

## Templates

Curated long-term file — section skeleton:

```markdown
# Memory — [agent name]
## Facts
- [claim] ([source], [date])
## Preferences (the principal's, as stated)
## Commitments (standing, dated)
## Open threads
```

Daily log line — capture-at-making:

```text
- [YYYY-MM-DD HH:MM TZ] — [artifact path] now records [one line: what changed and why].
```

Correction entry, layered (never a silent rewrite):

```text
- [date] CORRECTION: [old claim] — replaced by [new claim] ([new source], [date]). Reason: [one line].
```

Entity index line:

```text
- **[Name or role]** — `[path]` — [one-line nature of the relationship or subject]
```

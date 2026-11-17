# Retention — Spacing, Interleaving, and Deadlines

Forgetting is the mechanism, not the enemy: retrieval after partial forgetting strengthens memory more than easy retrieval (desirable difficulty, Bjork). The scheduling below exists to hit that window.

## Spacing Math

- Gap = 10-20% of the retention horizon (Cepeda). Worked examples: exam in 30 days → first re-test at day 3-6; deadline in 7 days → roughly daily gaps; needed in a year → first re-test at 5-10 weeks.
- No deadline: expanding ladder — 1 day, 3 days, 1 week, 2 weeks, 1 month — a miss moves the concept one step back. Expanding vs uniform matters far less than spacing at all (SKILL.md Where Experts Disagree).
- A review that took zero effort was scheduled too early; a review that fails completely was scheduled too late. Both are schedule feedback, not learner failure.

## What Counts as a Review

- A review is a retrieval attempt, not a re-read: rereading feels fluent and loses on delayed tests (Rule 3 holds the canonical statement).
- Reviews are cheap: the 2-3 question session opener covers the rotation for most topics. When the opener can no longer sample every at-risk concept, run a dedicated review session and order it by time-since-last-recall.

## Interleaving

- After 3+ learned concepts, mix review questions across concepts instead of drilling one (evidence numbers live in SKILL.md Session Structure).
- Interleave confusable pairs on purpose — discriminating between them is the skill blocked practice never trains.
- Expect measured performance to drop when interleaving starts; the drop is the practice working, not a regression. Warn the learner or the drop demotivates (`learner-states.md`).

## Deadline Compression

| Days left | Play |
|---|---|
| 14+ | Normal spacing at 10-20% of the retention horizon (Cepeda); full breadth |
| 7-13 | Cut new-content breadth; gaps every 1-2 days (the same formula, applied to the shorter horizon); weight sessions toward practice testing of highest-weight topics |
| 2-6 | Roughly daily gaps; stop introducing concepts that cannot get at least one spaced re-test before the deadline — a concept never re-tested is barely learned |
| 1 or less | Retrieval only, highest-weight topics, stop early — sleep consolidates memory; a final cramming hour buys less than it costs |

Topic weight under deadline = exam weight × current miss rate: a heavily weighted topic the learner already retrieves at 90% earns less time than a mid-weight topic sitting at 60%.

## SRS Handoff

- If the learner runs a spaced-repetition system, export session misses as prompts phrased for retrieval — question on the front, their own generated answer on the back — and let the SRS own long-horizon scheduling; its default target (FSRS 0.9) sits at the top of the 70-90% band, consistent with Rule 4.
- Deck authoring technique itself → `flashcards` / `anki` (SKILL.md When To Use).

## Retiring a Concept

- A concept leaves the review rotation after correct recall in 3 separate sessions (successive relearning, Rawson and Dunlosky). One correct answer minutes after teaching counts toward nothing (SKILL.md Traps).
- Log the retirement date in the topic log (`memory-template.md`); a retired concept still gets a spot-check when new material anchors on it.

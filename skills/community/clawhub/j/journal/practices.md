# Practices — Which Kind Of Journal, And How Each One Runs

Scope: the named methods, what each is actually for, and the mechanics that make it work rather than the version everyone half-remembers. Which practice for which goal is already decided by the Practice Selection table in `SKILL.md`, loaded before this file; what follows is how each one runs.

**Contents:** [Reread Policy](#reread-policy) · [Morning Pages](#morning-pages) · [Bullet Journal](#bullet-journal) · [Five-Minute Journal](#five-minute-journal) · [Decision Journal](#decision-journal) · [Dream Journal](#dream-journal) · [Travel Journal](#travel-journal) · [Reading and Commonplace](#reading-and-commonplace) · [Grief and Anniversary Journals](#grief-and-anniversary-journals) · [Parenting and Letter Journals](#parenting-and-letter-journals) · [Symptom and Food Journals](#symptom-and-food-journals) · [Running Two Practices](#running-two-practices)

**Before recommending a practice**, read `## Practice` in `~/Clawic/data/journal/memory.md`: what they already tried and abandoned is the strongest predictor available, and re-recommending it is the fastest way to lose the conversation.

## Reread Policy

The single most-missed distinction between practices, and the reason mixing them breaks both:

- **Never reread**: morning pages, expressive writing during the four days, any freewriting whose value is the act. Cameron's rule is no rereading for roughly eight weeks, and the point is not superstition — knowing nobody will read it, including your future self, is what removes the internal editor.
- **Reread on a schedule**: decision journal (on the review date), work journal (at review time), bullet journal (monthly migration), symptom journal (at analysis time).
- **Reread opportunistically**: travel, reading, letters, annual review material.

Consequence, declared in `SKILL.md` and enforced here: a never-reread corpus is not an analysis input (`patterns.md`). Lifting that is a policy the user changes knowingly, and it changes the practice itself — morning pages written in the knowledge that they will be analysed are no longer morning pages.

## Morning Pages

Julia Cameron's practice, from *The Artist's Way*.

- Three longhand pages, first thing after waking, before email, before the day acquires an agenda. Typed equivalent: a 10-minute timer, since the completion condition must be length or time, never quality.
- Content is irrelevant. Grocery lists, complaints, and "this is stupid" all count. The mechanism is emptying, not producing.
- **No stopping and no rereading** (Freewriting Mechanics in `capture.md`).
- Failure mode: treating them as content. The moment someone starts writing pages they would be happy to show someone, the practice has become writing and lost its function.
- Where they go: normal day entries, tagged so `patterns.md` can exclude them from analysis.

## Bullet Journal

Ryder Carroll's system, adapted to files.

- **Rapid logging** with a symbol per line: `·` task, `○` event, `—` note. `x` completes, `>` migrates forward, `<` schedules.
- **Daily log** is the day's file; **monthly log** is a page of the month's events and open tasks; **collections** are topic pages (a project, a packing list, books).
- **The migration is the system.** At month end, every unfinished task is rewritten by hand into the new month, or dropped. Recopying is deliberately annoying, and the annoyance is the filter: a task not worth rewriting was never going to be done.
- In a file-based setup, migration means creating the new monthly file and typing the surviving tasks into it — not moving a block. Losing the friction loses the filter.
- The mismatch to watch: bullet journal is a task system with a journal attached. Someone who wants to process emotion will not get it from rapid logging, and will conclude journaling does not work for them.

## Five-Minute Journal

The fixed-template practice: morning, three things you are grateful for, three things that would make today good, one affirmation. Evening, three good things that happened, one thing you could have done better.

- **Highest completion rate of any practice**, because the template removes every decision. That is exactly its cost: it will never produce the entry that changes something.
- Use it as a scaffold, not a destination — when the user starts writing past the template, stop offering it.
- The staleness failure: the same three gratitudes every day. Fix by narrowing the field ("something from the last 24 hours that would not have happened last year"), not by adding fields.

## Decision Journal

The practice with the highest return per entry, and the one almost nobody runs. Kahneman recommended it as a hindsight-bias defence; Gary Klein's premortem supplies the strongest single question.

Record **before** the decision, never after:

| Field | Why it must be written before |
|---|---|
| The decision, in one sentence | Ambiguity here is what makes later review meaningless |
| Options considered, including the one rejected fast | The fast rejection is the one hindsight will claim was never on the table |
| Expected outcome, concretely | "It'll go well" cannot be scored |
| Confidence, as a percentage | The number is the whole point — calibration only exists if it was recorded |
| What I know, and what I am assuming | Separating these two is where most bad decisions are visible in advance |
| Emotional state and what pressure I am under | Tired, angry, and deadline-driven decisions have their own failure signature |
| Premortem: "It is a year later and this failed. Why?" | Klein's question surfaces objections that a pros-and-cons list suppresses |
| Review date | Without it the entry is never reopened, and the practice produces nothing |

- **Review scoring**: on the review date, read the entry *before* recalling the outcome. Score the prediction as right / wrong / unclear, and the confidence separately. The useful finding is almost never "I was wrong" — it is "I was 90% confident and right 60% of the time".
- **Calibration takes volume**: roughly 20 reviewed decisions before the over/under-confidence pattern is readable. Below that, individual misses are noise (Rule 7's logic applied to predictions).
- Small decisions count and are better practice than large ones, because the review date arrives.
- Where they go: `decisions/<year>.md`, and the review date becomes a row in `## Due`. A decision inside a tracked project also leaves a one-sentence summary in `~/Clawic/data/projects/<project>.md` (`memory-template.md`).

## Dream Journal

- **Write before moving and before speaking.** Recall collapses fast on waking; sitting up and checking a phone is usually enough to lose it.
- Present tense, fragments allowed, images before narrative. "Blue corridor, someone's shoes, late for something" beats a tidy paragraph reconstructed twenty minutes later.
- Recall improves with the practice itself: people who write dreams remember more of them within a couple of weeks, which is a real effect and also a confound for anyone analyzing dream frequency.
- Filed under the date you woke up, in the same day file with a `## HH:MM` heading (`capture.md`).
- Interpretation is optional and belongs in the reply or a review, never in the entry file.

## Travel Journal

- **Same day or it does not happen.** Trip journals written after returning are itineraries, not journals.
- One page maximum per day, on the road. The constraint is what keeps it from competing with the trip.
- Write the specific and sensory: what things cost, what the room sounded like, the exchange with the person at the counter. Landmarks are on the internet; the counter exchange is not.
- Tickets, locators, and dates are a different kind of data — those belong in the shared bookings box, not in an entry (`memory-template.md`).

## Reading and Commonplace

- One entry per book while reading, appended to, rather than one at the end.
- Three fields per capture: the quote or idea, **why it struck you now**, and where it applies. The middle field is what a highlight export cannot reproduce, and is the entire reason to write it by hand.
- A commonplace book is the same practice without the book boundary: quotes, overheard lines, and fragments, organized by theme rather than by source.
- Keep it out of the daily entries: it is a retrieval corpus, and retrieval is what `notes` is built for. Cross-reference rather than duplicate.

## Grief and Anniversary Journals

- **No cadence, ever.** A grief journal with a streak is a grief journal with an obligation.
- Anniversaries, birthdays, and the dates that will land hard go in `## Due` as scheduled entries, so they arrive as an offer, not as a surprise — and only if the user asked for that.
- Letters to the person are the highest-value form, and they belong in `artifacts/` as their own file, not in the daily flow (`difficult-entries.md`).
- Do not analyze a grief corpus for patterns unless asked, and never surface a sentiment trend from it.

## Parenting and Letter Journals

- Written to be read, which inverts Rule 2's usual logic: this one is allowed to be edited, because the audience is real.
- Dated letters, one per occasion, in `artifacts/letters/<date>-<who>.md` — they are read whole, years later, and must never be buried inside a day file.
- The highest-value content is the mundane specific: what they said this week, what they are afraid of, what the house sounded like. Milestones are recorded everywhere else.
- Keep a separate no-read marker on them — one line in `## Read Scope` of `~/Clawic/data/journal/memory.md`, the folder and a label — if the user does not want them opened in normal sessions (`privacy.md`).

## Symptom and Food Journals

- **Same fields every day, or the data is unusable.** Free text plus a structured block, not free text alone.
- Minimum viable fields: date, the symptom with a 0-10 severity, timing, and the two or three suspected inputs. Adding fields later invalidates comparison with everything before.
- **Lag is the trap**: many suspected triggers act hours or a day later, so a same-row correlation finds nothing. Record intake times, not just the day, in the entry's structured block.
- Health metrics measured in series belong in the shared health box, not in prose: severity and mood go to `~/Clawic/data/health/<metric>.md` so a health, sleep, or fitness skill reads the same numbers, and each row carries its time — without it the lag cannot be tested against the intake times (`memory-template.md`).
- Analysis needs the paired-day minimum of Rule 8, and elimination beats correlation: a suspected trigger is tested by removing it for two weeks, not by counting co-occurrences.

## Running Two Practices

Legitimate combinations, once one is established:

- Morning pages + weekly review — the pages are never reread, the review works from the week's other entries.
- Interstitial during the workday + one longer entry at night.
- Daily entry + decision journal — different files, different reread policies, no interference.
- Bullet journal + expressive writing during a hard period.

Illegitimate: two daily freeform practices, or any practice that requires rereading material another practice promised would never be reread.

**Write in the same turn:** the practice chosen, its cadence, and the date it started, to `## Practice` in `memory.md`; a practice tried and dropped, to the same section with why (it is what stops you re-recommending it); every decision entry to `decisions/<year>.md` with its review date copied into `## Due`; letters and long-form pieces to `artifacts/`; symptom or mood series to `~/Clawic/data/health/`. Formats: `memory-template.md`.

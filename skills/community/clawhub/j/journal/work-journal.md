# Work Journal — Evidence, Learning, And The Review You Will Have To Write

Scope: professional journaling. Different from personal journaling in one way that changes everything: it exists to be read back, by you and sometimes by others.

**Contents:** [Why This Is A Separate Practice](#why-this-is-a-separate-practice) · [The Capture Line](#the-capture-line) · [The Brag Document](#the-brag-document) · [Impact Numbers](#impact-numbers) · [Learning Log](#learning-log) · [One-on-One And Manager Prep](#one-on-one-and-manager-prep) · [Performance Review Assembly](#performance-review-assembly) · [Job Search And Interviews](#job-search-and-interviews) · [What Never Goes In](#what-never-goes-in)

**Before any work-journal session**, read `work-log/<year>.md` and `## Practice` in `~/Clawic/data/journal/memory.md` for the review cycle dates. Assembling a review from memory when a log exists is the most expensive mistake available here.

## Why This Is A Separate Practice

- **Written to be read**, which suspends the usual rule against writing for an audience: this one has a real audience and a real deadline.
- **Retention decays fast and asymmetrically.** By review time, the last six weeks are vivid and the first six months are gone — which is exactly the period where the hardest work usually happened. Everyone experiences this; almost nobody writes it down.
- **The work nobody saw is the work that does not get credited.** Unblocking someone, killing a bad project, the migration that produced no incident. None of it appears in a ticket count.
- Julia Evans's term for the artifact — a **brag document** — is worth using because it names the discomfort directly: the document exists because self-assessment from memory systematically undercounts.

Keep it in the journal corpus, not in a work system: a document on the employer's drive is not yours, and you lose it the week you most need it.

## The Capture Line

One line per win, written **the day it happens**, in `work-log/<year>.md`:

`<date> | <what I did> | <impact, with a number> | <who saw it> | <link or artifact>`

- **Same day.** A weekly catch-up loses the small ones, and the small ones are what make a review credible.
- **Under 30 seconds.** If it takes longer, the format is wrong and the log dies in three weeks.
- **"Who saw it"** is not vanity: at review time, a named witness converts a claim into corroboration, and the person who saw it is often the peer reviewer.
- **The link is the proof.** PR, doc, dashboard, thread, incident ticket. A win with no artifact is the one that gets challenged.
- **Log the failures too**, in the same file with an outcome of what changed. A review that contains one honest failure and its correction reads as more credible than one that contains none, and "what did you learn" is a question on nearly every review form.

Capture triggers — these all count and are all routinely missed:

| Trigger | Line to write |
|---|---|
| Shipped something | What shipped, the metric before and after |
| Unblocked someone | Who, what they were blocked on, how long it had been stuck |
| Killed a bad idea | What was proposed, what it would have cost, what happened instead |
| Fixed an incident | Duration, blast radius, and what stops recurrence |
| Was asked for advice outside your team | Who and about what — this is the clearest scope-growth signal there is |
| Onboarded, mentored, or reviewed | Who, and what they can now do unaided |
| Wrote a doc or runbook others use | Link, and who has referenced it |
| Declined work | What, and what you protected by declining |
| Learned something that changed how you work | Goes to the Learning Log below, not here |

## Impact Numbers

The difference between a promoted review and a competent one is usually arithmetic that took two minutes.

- **Before and after, with units and a period.** "Cut build time from 14 min to 3 min, ~40 builds/day" beats "improved build performance".
- **Convert to time or money once, and state the assumption.** 11 minutes × 40 builds/day × 20 working days ≈ 147 engineer-hours a month; say "at 40 builds/day" so the number is checkable rather than impressive.
- **Estimates are fine and must be labelled.** "~30% fewer support tickets in the two months after (from the weekly dashboard)" is honest; a bare "30%" invites a challenge you will lose.
- **When there is no number**, use scale and counterfactual: how many people, how often, and what would have happened otherwise.
- Never inflate. One number that does not survive scrutiny discredits every other line in the document.

## Learning Log

Separate from wins, and more valuable after two years than the win log.

- One entry when something changed how you work: a technique, a failure mode you now recognize, a piece of the system you finally understand.
- Format: what I believed, what happened, what I do differently now. The middle field is what makes it retrievable.
- **The recurrence test**: a lesson that shows up a third time is not a lesson, it is a process problem — write it as a runbook in `artifacts/` instead, and link it from the log.
- This is what makes interview answers concrete and what turns an incident into an improvement rather than a scar.

## One-on-One And Manager Prep

- **Standing file, not an entry per meeting**: `artifacts/one-on-one-<manager>.md`, appended before each meeting and pruned after.
- Four sections, kept short: what I want them to know, what I need from them, what I am stuck on, what to raise if there is time.
- **Write it before the meeting, not during.** The items you would raise if you had thought about it are the ones that never get raised.
- After the meeting, one line on what was agreed and by when — this is the record that resolves "we discussed that in March" six months later.
- Feedback received goes in verbatim, positive and negative both. Negative feedback recorded in the person's own words is far more useful at review time than your paraphrase of it, which will have softened.

## Performance Review Assembly

At review time, in order:

1. **Read the log first, memory second.** Opening with recall anchors the whole document to the last six weeks.
2. **Group by the company's competency framework**, not chronologically. If the form asks about impact, scope, and collaboration, those are the three headings, and the log lines get sorted into them.
3. **Lead each group with the largest verifiable number.**
4. **Name witnesses** for anything a reader might question, and check them against your peer-reviewer list.
5. **Include one failure and what changed**, drawn from the log.
6. **Fill the gaps honestly.** A competency with no log lines is not a competency you demonstrated, and the correct move is to say what you would need to demonstrate it, not to stretch an unrelated line to cover it.
7. Save the assembled document to `artifacts/review-<period>.md` — next cycle starts from it, and if the outcome is disputed it is the record.

## Job Search And Interviews

- The win log is the raw material for behavioural answers. Convert a line to situation / action / result at interview prep time, not at capture time — capturing in a framework slows the daily line down to where it stops happening.
- The learning log answers "tell me about a time you were wrong", which is the question people improvise worst.
- Keep a separate `artifacts/interview-log.md`: company, round, questions asked, what you answered, what you wished you had answered. The third field is the one that improves the next round.
- Salary and offer details go to the shared finances box, not into a journal entry (`memory-template.md`).

## What Never Goes In

- **Credentials of any kind**, including the ones inside a pasted log, error message, or config. Strip to a pointer before writing (SKILL.md, `privacy.md`).
- **Confidential business data**: unannounced financials, customer lists, personal data of users, security findings before disclosure. A work journal in a personal folder is the wrong container for these, whatever the intent.
- **Characterizations of colleagues that you would not defend in the room.** Record behaviour and dates, not verdicts, in `work-log/<year>.md`. This file may be read in a dispute, and in some jurisdictions a personal journal is discoverable in litigation in a way a therapist's notes are not (`privacy.md`).
- **Third-party health, legal, or personal information** disclosed to you in confidence.

**Write in the same turn:** every win, failure, and impact number to `work-log/<year>.md`; lessons to the learning log in the same file under `## Learning`; one-on-one prep and notes to `artifacts/one-on-one-<manager>.md`; the assembled review to `artifacts/review-<period>.md` with its `## Boxes` line; review-cycle dates to `## Due`; a colleague the user asks to track as a contact to `~/Clawic/data/contacts/contacts.md` (name and channel only, never what was written about them); compensation to `~/Clawic/data/finances/`. Formats: `memory-template.md`.

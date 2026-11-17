# Preparation — Walking In Knowing What You Want

**Before writing any prep brief**, read: the last block for this series or these people in `~/Clawic/data/meetings/records/<year>-<mm>.md`, the open items in `## Follow-Ups` of `memory.md` that involve any attendee, their rows in `~/Clawic/data/contacts/contacts.md`, and `~/Clawic/data/meetings/decisions.md` for anything already settled on this topic. If `## Boxes` names a prep artifact for this series (`artifacts/prep-<series>.md`), read it — it is the accumulated version of this brief.

**Contents:** [How Much Prep](#how-much-prep) · [The Prep Brief](#the-prep-brief) · [Preparing To Get Something](#preparing-to-get-something) · [Pre-Wiring](#pre-wiring) · [Preparing As An Attendee](#preparing-as-an-attendee) · [Recurring Prep](#recurring-prep) · [Ten Minutes Before](#ten-minutes-before)

## How Much Prep

Prep scales with the **cost and reversibility of the room**, never with the meeting's length. A 25-minute board decision deserves two hours of prep; a 90-minute team working session deserves ten minutes and an agenda.

| Meeting | Prep budget | What it buys |
|---|---|---|
| Recurring internal sync | 5 min | Last time's open items, today's one blocker |
| 1-on-1 | 5-10 min | Their last topic, one piece of feedback, what changed for them |
| Decision meeting | 20-40 min | The options table, the recommendation, the rejected paths |
| Client or external status | 20-30 min | Their open commitments, your late items, the next-step ask |
| QBR, board, investor update | 2h+ | The numbers, the bad news framing, the three questions you will be asked |
| Interview or panel | 20 min | The signal you own, the questions nobody else is asking |

If prep would take longer than the meeting and the meeting is `align` or `inform`, that is the signal to write the document instead (`meeting-load.md`).

## The Prep Brief

Seven fields. Anything not answerable from the record is a question to send *before* the meeting, not to burn the slot on.

```markdown
# Prep — Acme status, 2026-07-28 25 min

Output I want: revised timeline agreed in writing, or a named blocker.
Their likely ask: earlier delivery of the mobile flow.
Open from last time: mobile mockups (delivered 07-19), budget question (unresolved).
What I owe them: revised timeline — 2 days late.
What they owe me: legal sign-off on the DPA — 13 days late, chased once.
Their people: Priya decides scope, wants numbers first. Marc never attends, answers in writing.
Landmine: the latency regression. If raised: it is origin-side, fix shipping Friday, not a CDN issue.
```

- **Lead with your own late items.** Naming them before they do costs 15 seconds and removes the leverage they were about to use.
- **"Their likely ask" is the field people skip**, and it is the one that prevents being cornered into an improvised commitment.
- **A landmine is any topic where the honest answer is bad.** Prepare the sentence now; improvising it live is how commitments get made by accident.

## Preparing To Get Something

When the meeting exists so a specific thing is agreed:

1. **Write the sentence you want said back to you.** "We'll fund two more weeks of QA." If you cannot write it, the meeting has no output (SKILL.md Rule 1).
2. **Three outcomes, ranked**: the ask, the acceptable fallback, and the walk-away that keeps the relationship. Decide the fallback *before*, because in the room the fallback always looks better than it is.
3. **One number, sourced.** Bring the number the decision turns on and where it came from. A decision meeting with no number becomes a discussion about intuitions, and the most senior intuition wins.
4. **The rejected options, with why.** Someone will propose them; having the answer ready is the difference between a decision and a second meeting (`decision-rights.md`).
5. **The smallest reversible version.** When the room will not approve the full thing, the two-week trial with a named review date usually passes — and getting a decision made small beats getting it deferred whole.

## Pre-Wiring

Big decisions are made before the meeting; the meeting ratifies them. Pre-wiring is not manipulation, it is removing surprise from a room where surprise produces "let's take it offline".

- **Order: the loudest skeptic first, allies second, the decider last.** The skeptic's objection changes your proposal while there is still time; going to the decider first means presenting something you will then have to walk back.
- **Ask for the objection, not for support**: "what would make you say no?" Someone who has already voiced their objection privately rarely re-litigates it in the room, and often improves the proposal.
- **Send the decider a one-paragraph heads-up** with the decision and your recommendation. A decider who first sees a decision on a slide defers it by reflex.
- Pre-wiring more than three or four people means the group is too big for the decision (SKILL.md Rule 2), not that you need more meetings.

## Preparing As An Attendee

With `default_role: participant`, the brief is different:

- **Find the output.** If the invite does not name one, ask in one line before the meeting: "what are we deciding?" This changes the meeting more often than anything you do inside it.
- **Prepare one contribution, not a general readiness.** The question you will ask, the number you will bring, or the risk you will name.
- **Decide your position on the likely decision in advance**, including what evidence would change it. Rooms punish people who form opinions live and then defend them.
- **Know what you will not agree to**, and what you will do if it is agreed anyway (`difficult.md`).

## Recurring Prep

For a series that meets more than a few times, the brief is an artifact, not a fresh document: `~/Clawic/data/meetings/artifacts/prep-<series>.md`, updated in place before each occurrence, with its `## Boxes` line reading `read the day before every <series>`. It accumulates the parts that never change — their standing asks, who really decides, the numbers they always challenge, the topics that are off the table — so each occurrence's prep is ten minutes of deltas instead of a rebuild. A prep brief for a one-off meeting is disposable and is never stored.

## Ten Minutes Before

- Open items involving these people, with dates (`## Follow-Ups`).
- The decision on the table, and who decides it (`decision_method`).
- Your one number and its source.
- Their last message or request, so nothing lands as forgotten.
- For a remote room: join details, screen share ready, and who is monitoring chat (`remote.md`).

**After the meeting**, write the record and update prep in the same turn: what actually happened into `records/<year>-<mm>.md`, anything new about how a person operates into their `Context` in `~/Clawic/data/contacts/contacts.md`, and for a recurring series, the changed standing facts into `artifacts/prep-<series>.md` (`memory-template.md`). Prep that is not written back is prep you will redo from zero next quarter.

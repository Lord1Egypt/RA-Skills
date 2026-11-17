# Meeting Notes — Calls, 1-on-1s, Interviews, Retros

Six conversation types, one shape each. What differs is which section carries the value; the rest is scaffolding that can be dropped.

**Contents:** [What a Meeting Note Is For](#what-a-meeting-note-is-for) · [The Base Template](#the-base-template) · [1-on-1](#1-on-1) · [Interview and Debrief](#interview-and-debrief) · [Client and Sales Calls](#client-and-sales-calls) · [Standup and Status](#standup-and-status) · [Retro and Post-Mortem](#retro-and-post-mortem) · [Recurring Series](#recurring-series) · [Meeting Traps](#meeting-traps)

**Before a recurring meeting**, read its row in `## Recurring Meetings` in `~/Clawic/data/notes/memory.md` (or `recurring-meetings.md` if `## Boxes` points there) and the carry-forward it names, plus the open rows in `actions.md` for the attendees. Walking in without last time's actions is why the same item is agreed three weeks running.

## What a Meeting Note Is For

It has exactly three readers: the person who was there and forgot, the person who was not there, and — for anything involving employment, money, or a contract — someone reading it as a record years later (SKILL.md Rule 9).

Serve them in this order:

1. **The decision**, in the words the room agreed to. Read it back out loud before the call ends; roughly half the "decisions" in a meeting dissolve when restated as a sentence, and finding that out in the room costs 20 seconds instead of a sprint.
2. **The commitments**, with owner and absolute date (SKILL.md Rule 4).
3. **The evidence** behind both: the number, the constraint, the customer quote.
4. Everything else, at ≤20% of what was said (SKILL.md Rule 3).

A meeting with no decision and no action gets a note anyway — one line saying so. Three of those in a month is a finding for the monthly review (`journal.md`), and the note is the evidence.

## The Base Template

```markdown
---
date: 2026-07-26
type: meeting
title: "Pricing: staying at three tiers, revisit at 500 customers"
tags: [product, pricing]
attendees: [alice, bob]
absent: [carol]
project: atlas
---

# Pricing: staying at three tiers — 2026-07-26

**Present:** Alice, Bob · **Absent:** Carol (needs the summary)

## Decisions
- Three tiers stay. Revisit at 500 customers or when >20% of churn cites price. — decided by @alice, effective 2026-07-26 · supersedes `decisions/2026-05-02_pricing-tiers.md`

## Actions
| Task | Owner | Due |
|---|---|---|
| Send the pricing deck | @alice | 2026-08-04 |
| Pull churn reasons for Q2 | @me | 2026-07-30 |

## Evidence
- 14% of Q2 churn cited price; the threshold discussed was 20%
- Enterprise pipeline unaffected either way

## Open Questions
- Does tier 3 keep the SSO add-on? — waiting on @bob

## Parking Lot
- Annual billing discount — deferred to the pricing review
```

- **Decisions and Actions come before narrative**, always. The reader who has 30 seconds gets what they need without scrolling.
- **`absent` is not decoration**: it is the send list, and it is who will re-litigate the decision if nobody tells them.
- **Parking Lot is what keeps the meeting on time.** An item there with no date is fine; an item there for the third time is either a decision or a delete.
- Every decision line carries its `supersedes` pointer if it replaces one (`decisions.md`).

## 1-on-1

The carry-forward *is* the note. Everything else is context.

```markdown
## Carry-forward from 2026-07-12
- Her: wanted clarity on the promo cycle → answered, cycle is October
- Me: intro to the design lead → done 2026-07-15

## Their topics
- Wants to own the onboarding surface end to end

## My topics
- Q3 scope: two projects, not three

## Actions
| Task | Owner | Due |
|---|---|---|
| Draft the onboarding ownership proposal | @alice | 2026-08-09 |

## Signals
- Third time she has raised scope; treat as a pattern, not a mood
```

- **Their topics before yours.** A 1-on-1 that opens with the manager's agenda is a status meeting wearing a costume.
- **Signals is a private observation section and it is still a record** (SKILL.md Rule 9): write behaviour and frequency ("third time she has raised scope"), never a characterization ("she is difficult"). One is evidence, the other is a liability.
- Anything about pay, promotion or performance follows `sensitive.md` before it is written anywhere.

## Interview and Debrief

Two things that must never merge in one section: what the candidate said, and what you concluded.

```markdown
## Evidence
- Q: how did you handle the migration? → "we moved 40 tables in six weekends, no rollback plan" (verbatim)
- Wrote a working SQL window function unaided in ~8 minutes

## Assessment
- Strong on execution, thin on risk framing. Hire for a team with review discipline.
- Recommendation: hire / no hire / more data
```

- **Quote verbatim, in quotes, or paraphrase clearly marked.** A paraphrase that hardens into a quote is how a debrief becomes indefensible.
- **Assessment cites evidence lines.** An assessment with no evidence above it is a vibe and does not belong in a hiring record.
- **Never record protected characteristics or anything you inferred about them** — age, family status, health, origin, religion. Not as an observation, not as context (`sensitive.md`).
- Store interview notes where the hiring process stores them, not in a personal vault, when the employer has a system of record. A personal copy is a discovery risk with no upside.

## Client and Sales Calls

The distinction that costs money: **exploration versus commitment**.

| Said in the call | Record as | Same-day follow-up |
|---|---|---|
| "Could you also do X?" | Open Question | Ask whether it is in scope, in writing |
| "We'll include X" (by you) | Commitment — scope change | Written confirmation with the price or the "no charge" said explicitly |
| "We need it by the 14th" | Constraint with a date | Confirm feasibility in writing the same day |
| "We're happy to sign" | Signal, not a decision | Nothing changes until it is signed |

- **Anything that sounds like scope goes into writing the same day**, and the note records that it was sent and to whom. A scope change that lives only in a meeting note is a dispute waiting for an invoice.
- The client is a row in the shared `~/Clawic/data/contacts/contacts.md` and the engagement is a file in `~/Clawic/data/projects/`. The note carries the names, never a second copy of either (`memory-template.md`).
- Prices, discounts and dates get their currency and their ISO date in the note, because they are read a year later by someone reconstructing what was agreed.

## Standup and Status

Standups usually do not deserve a note. Write one only when the standup produced a blocker with an owner or a change of plan.

- **Blocker format**: `blocked: <what> — waiting on @who — since <date>`. The `since` date is what turns a blocker into an escalation at the weekly review.
- Rolling a week of standups into one file per week beats one file per day: five files with three lines each are five files nobody opens.

## Retro and Post-Mortem

```markdown
## Timeline
| Time | Event | Source |
|---|---|---|
| 09:14 | Deploy went out | deploy log |
| 09:31 | First customer report | support |

## Contributing factors
- The staging database had 200 rows; the bug needed 50k to appear
- The alert existed but routed to a channel nobody watches

## Actions
| Task | Owner | Due |
|---|---|---|
| Seed staging from a production snapshot, monthly | @me | 2026-08-07 |
```

- **A person is never a contributing factor.** "Alice deployed without testing" is a name; "the deploy path allows a deploy with no test run" is a cause with a fix. Notes that blame stop being honest within one incident.
- **Timeline before analysis, with sources.** Reconstructed timelines drift toward the story people prefer; the source column is what stops it.
- **Every action gets an owner and a date or it is not in the retro** — actionless retros are the reason people stop attending them.

## Recurring Series

A meeting that repeats gets a row in `## Recurring Meetings` in `memory.md`: cadence, attendees, note home, and what carries forward. That row is what makes the next note start in the right place.

- **Carry-forward is a section, not a memory.** Copy last time's open actions and open questions into the new note before the meeting starts; delete the ones that closed.
- **Series naming**: `YYYY-MM-DD_<series-slug>.md` keeps the whole series adjacent in a directory listing and greppable by series.
- A series whose carry-forward has been identical for three occurrences has a stuck item — that goes to `## Open Threads` with the person's name, and gets raised out of the meeting.

## Meeting Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Writing the note after the call | Ebbinghaus: most unrecorded detail is gone within 24h, and what remains is the version you now prefer | Capture live; clean up after (SKILL.md Rule 3) |
| Recording discussion but not decisions | The note proves a conversation happened and answers nothing | Decisions section first, read back in the room |
| "We'll figure out the owner later" | Nobody owns it, and it reappears next week as new | Owner and absolute date, or it is an Open Question (Rule 4) |
| Skipping the absentee list | The one person who will reopen the decision never got told | `absent` in frontmatter, summary sent same day |
| Characterizing people in a 1-on-1 note | Outlives the mood, gets read by HR or the person | Behaviour and frequency only |
| Merging evidence and assessment in a debrief | The judgment becomes unauditable and legally weak | Two sections, assessment cites evidence |
| Treating "we're happy to sign" as a close | It is a signal; nothing has been decided | Commitment table above |
| One note per standup | Five files a week that nobody opens | One weekly file, blockers only |
| Naming a person as the cause in a retro | Kills the honesty the retro depends on | Name the mechanism |

**Write triggers for this file** — in the same turn: the note to `~/Clawic/data/notes/meetings/<date>_<slug>.md`; every commitment to `actions.md`; every decision to `decisions/` with its `supersedes` pointer; every attendee and absentee to the shared `~/Clawic/data/contacts/contacts.md` (key, role, context, last contact); the project name to the note and the summary line to `~/Clawic/data/projects/<project>.md`; a new repeating series to `## Recurring Meetings`; and any unresolved question to `## Open Threads`. Formats, keys and thresholds: `memory-template.md`.

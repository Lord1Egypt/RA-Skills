# Decision Records

A decision note exists to answer one question asked months later: *why did we do it this way, and what would have to change for us to redo it?* Anything that does not serve that question is padding.

**Contents:** [When a Decision Deserves a Record](#when-a-decision-deserves-a-record) · [The Template](#the-template) · [Writing the Options](#writing-the-options) · [Supersession](#supersession) · [Review Dates and Reversal Triggers](#review-dates-and-reversal-triggers) · [Team Decisions](#team-decisions) · [Decision Traps](#decision-traps)

**Before writing one**, read the `decisions/` folder for the same subject and `## Open Threads` in `~/Clawic/data/notes/memory.md`. A decision written without finding the one it replaces creates two live answers and the wrong one gets quoted.

## When a Decision Deserves a Record

Three tests. One is enough.

- **Expensive to reverse**: undoing it costs more than a day of work, or touches data, contracts, or people.
- **Non-obvious**: a competent stranger would plausibly choose the other option, so the reasoning is the artifact.
- **Recurring argument**: it has been discussed twice. The third time is a record or an infinite loop.

Everything else is a line in the meeting note. A decision log that captures "we'll use tabs" alongside "we're not raising this year" is a log nobody reads.

The format below is Nygard's ADR pattern (context, decision, consequences) with two additions that matter outside software: the rejected options with the reason, and a reversal trigger.

## The Template

```markdown
---
date: 2026-07-14
type: decision
title: "Pricing stays at three tiers, revisit at 500 customers"
tags: [product, pricing]
project: atlas
status: active
supersedes: decisions/2026-05-02_pricing-tiers.md
review: 2027-01-14
---

# Pricing stays at three tiers — 2026-07-14

**Decided by:** @alice · **Effective:** 2026-07-14 · **Status:** active

## Context
Churn at 14% cited price in Q2. Sales wants a fourth enterprise tier.
Constraint: one engineer, no billing changes before the beta.

## Decision
Keep three tiers. No enterprise tier before the beta ships.

## Why this one
Adding a tier costs ~3 weeks of billing work we do not have, and the churn
number (14%) is below the 20% threshold we set for treating price as the cause.

## Rejected
- **Fourth enterprise tier** — 3 weeks of billing work; blocks the beta.
- **Cut tier 1 price 20%** — hits revenue immediately, and no evidence tier 1 is the churn source.

## Consequences
- Sales has no enterprise SKU until Q1; deals above 50 seats are quoted manually.
- Revisit is automatic at 500 customers or churn-by-price >20%.

## Reversal trigger
500 customers, or >20% of churn citing price in a quarter. Review date 2027-01-14.
```

- **`status`** is `active`, `superseded`, or `reversed` — never deleted. A deleted decision takes its reasoning with it and the argument restarts from zero.
- **`review`** is a date, not "someday". It becomes a row in `## Due` only if the user wants the reminder; otherwise it is checked when the subject next comes up.

## Writing the Options

The rejected options are the highest-value part of the note and the first thing that gets skipped.

- **Two rejected options minimum, or say why there were none.** A decision with no alternatives recorded reads, later, as a decision nobody thought about.
- **Each rejection carries a cost, a constraint, or a number** — "too complex" is not a reason, "three weeks of billing work against a two-week runway" is.
- **Record the option someone argued for and lost, by name.** It is the one that comes back, and the note is what stops it coming back unchanged.
- **Do not rank options you never seriously considered.** A fake shortlist makes the note look thorough and makes the reasoning untrustworthy.

## Supersession

When a new decision replaces an old one, both files change, in the same turn:

1. New note: `supersedes: decisions/<old>.md` in frontmatter, and one line in Context saying what changed since.
2. Old note: `status: superseded` plus `superseded_by: decisions/<new>.md` at the top. The body is left intact — the old reasoning is the reason the new decision is defensible.
3. Any note linking the old decision keeps its link; the chain is followed forward through `superseded_by`.

A **reversal** is different from a supersession: same question, opposite answer, usually because the reasoning was wrong rather than because the world changed. Mark it `status: reversed`, and record in the new note what the old one got wrong. This is the only place in the corpus where being explicit about a mistake pays: the same mistake is otherwise repeated in eighteen months by someone quoting the original note.

## Review Dates and Reversal Triggers

A decision with a reversal trigger outperforms one with a review date, because the trigger fires on a fact and the date fires on a calendar nobody watches.

- **Trigger form**: a threshold, a count, or an event — "500 customers", ">20% of churn citing price", "when the contract renews". Numeric triggers name the metric and where it is read from.
- **Date form** is the fallback when no observable trigger exists. Put it in `## Due` only for decisions that expire (contracts, licences, trial periods); otherwise the review date lives in the note and is checked when the subject returns.
- **A decision with neither** is permanent by default, and should say so: "no scheduled review; revisit only if the team size changes."

## Team Decisions

- **The decider is a person, not a group.** "The team decided" produces a note nobody owns and a decision anybody can reopen. Name who made the call, even when everyone agreed.
- **Record the dissent.** One line: who disagreed and on what grounds. It costs nothing, and it is what makes the note credible to the person who reads it after the outcome is known.
- **Consulted versus informed.** Whoever was consulted is in `attendees`; whoever needs to know is the send list, and they get the decision in one sentence the same day.
- The decision belongs to a project: one summary line and the pointer go to `~/Clawic/data/projects/<project>.md`, the reasoning stays in the note (`memory-template.md`).

## Decision Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Logging every decision | The log dilutes to the point where the important three are invisible | The three tests above |
| Writing only the decision | In six months the "why" is what is being asked, and it is gone | Context and Rejected sections carry the value |
| Deleting a superseded decision | The new decision loses the evidence that makes it defensible, and the old argument returns | `status: superseded`, body intact |
| "Too complex" as a rejection reason | Unfalsifiable, so the option comes back every quarter | Cost, constraint, or number |
| "We'll revisit later" | Never fires | Reversal trigger on an observable fact |
| Attributing to "the team" | No owner, so anyone can reopen it | Name the decider |
| Burying the decision inside a meeting note | Findable only by whoever remembers the meeting date | Own file in `decisions/`, linked from the meeting |
| Recording the decision but not who must be told | The uninformed person re-litigates it | Send list same day, absentees included (`meetings.md`) |

**Write triggers for this file** — in the same turn: the record to `~/Clawic/data/notes/decisions/<date>_<slug>.md`; `status` and `superseded_by` on the note it replaces; the one-line summary and pointer to `~/Clawic/data/projects/<project>.md`; the decider and any dissenter to the shared `~/Clawic/data/contacts/contacts.md`; any resulting commitment to `actions.md`; an expiring review date to the `## Due` table in `memory.md`. Formats and thresholds: `memory-template.md`.

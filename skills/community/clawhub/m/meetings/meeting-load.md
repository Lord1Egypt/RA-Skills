# Meeting Load — Whether To Meet At All, And What To Cut

**Before any load question**, read `## Series` and `## Meeting Norms` in `~/Clawic/data/meetings/memory.md` (or `~/Clawic/data/meetings/series.md` if `## Boxes` points there) and `cost_per_attendee_hour` in `config.yaml` — an audit without the standing series is a guess. **Check `## Due`** against today's date and state an overdue load audit or kill review in one line.

**Contents:** [The Meet Test](#the-meet-test) · [What A Meeting Costs](#what-a-meeting-costs) · [The Load Audit](#the-load-audit) · [Declining Without Damage](#declining-without-damage) · [Replacing A Meeting With Writing](#replacing-a-meeting-with-writing) · [Calendar Defenses](#calendar-defenses)

## The Meet Test

Sync time is worth its cost only when the group has to converge in one pass. Four purposes qualify; everything else is a document that has not been written.

| Purpose | Meet? | Why |
|---|---|---|
| **Decide** — a named choice with people who disagree | Yes | Convergence is iterative; a thread takes days and drifts |
| **Generate** — options that do not exist yet | Yes | Building on each other's half-ideas is the whole mechanism |
| **Align** — a plan that must survive contact with objections | Yes | Objections have to be answerable live or they resurface later |
| **Build trust** — new team, first client contact, repair after conflict | Yes | The relationship is the output; there is no artifact substitute |
| **Inform** — news, updates, roadmaps, results | No | Write it. A meeting reduces the bandwidth to one speaker at a time |
| **Status round-robin** | No | N people speak to 1 while N−2 wait; async thread, live only for what the writing exposed |
| **Review a document** | No | Circulate it with a comment deadline; meet only on the unresolved comments |
| **Announce a decision already made** | No | Announcement plus a Q&A channel; a fake consultation costs more trust than a blunt memo |

Two-question filter for any invite: **what is different after this meeting, and who could produce that without meeting?** If the second answer is "one person with 20 minutes and a doc", that is the plan.

## What A Meeting Costs

`cost = attendees × duration_hours × cost_per_attendee_hour`, and for a series, `× occurrences_per_year`.

| Meeting | Per occurrence at 80/h | Per year |
|---|---|---|
| 25 min, 4 people | 133 | weekly: ~6,900 |
| 50 min, 8 people | 533 | weekly: ~27,700 |
| 60 min, 12 people | 960 | weekly: ~50,000 |
| Half-day offsite, 10 people | 3,200 | quarterly: ~12,800 |

While `cost_per_attendee_hour` is unset, quote person-hours instead of money — `8 people × 1h × 52 = 416 person-hours a year` lands as hard as a number nobody can dispute. Fully-loaded cost is roughly 1.3-1.4× salary rate; if the user gives a salary figure, say which multiplier you applied.

The cost that does not appear in the arithmetic is **fragmentation**. Graham's maker/manager schedule: a single meeting dropped into the middle of an afternoon can cost the whole afternoon, because the two hours before it are too short to start anything. So the real load metric for anyone who builds is not hours in meetings, it is **contiguous free blocks ≥2h**: three per week is workable, one is not, and a calendar with five 25-minute meetings scattered across a day has zero.

## The Load Audit

Run monthly (`## Due`). Take the last two weeks of calendar and classify:

1. **Count and total.** Hours in meetings ÷ working hours = load percentage. Reference points, not rules: a manager at 50-60% is normal, an IC above ~25% is losing the week, and anyone above 70% has no time to do what the meetings commit them to.
2. **Count contiguous ≥2h blocks per week.** This is the number that predicts whether anything ships.
3. **Classify each meeting by purpose type** (table above). Every `inform`, `status` and `review` is a candidate for deletion, not shortening.
4. **Separate recurring from one-off.** Recurring load is the structural problem: one weekly hour is 52 hours a year, and killing it once fixes it forever. One-off meetings are noise around it.
5. **Rank the recurring meetings by annual cost**, top to bottom. Take the top three to a kill review (`recurring.md`).
6. **Look for the same eight people in six meetings.** That is one meeting with a bad agenda split across the week — merge it.

Write the audit result: the load percentage, the block count, and any series you killed or re-scoped, into `## Meeting Norms` and the affected `## Series` rows.

## Declining Without Damage

Escalating forms, cheapest first. Each names the alternative — a decline without one reads as a refusal to help.

| Form | Use when | Script |
|---|---|---|
| Attend for one item | You are needed for 10 of 50 minutes | "I'll join for the pricing item — can you put it first, or ping me when you get there?" |
| Send a delegate | Someone closer to the work can decide | "Tomás will represent us and can commit on scope up to X." |
| Ask for the recap | Purpose is `inform` | "I'll skip and read the recap — flag me if a decision needs me." |
| Shrink it | Agenda is one decision in a 60-minute slot | "Can we do this in 25? The only open question is A." |
| Convert to async | Purpose is `review` or `status` | "Sending my input in the doc by Thursday — let's meet only if the comments deadlock." |
| Decline outright | No output named after asking once | "What would we decide? If it's an update I'd rather read it." |

Two rules that keep this from costing political capital: **decline in advance, never by no-show**, and **never decline the same series twice without renegotiating it** — the third silent decline is read as contempt, while "this meeting isn't working for me, can we change it" is read as engagement.

If the invite comes from someone with power over the user's work, the play is not declining, it is reshaping: ask for the agenda, offer to own an item, propose the shorter slot. Getting the agenda written is often the whole fix.

## Replacing A Meeting With Writing

A written replacement only works if it is genuinely readable and genuinely closes:

- **State the decision or ask in the first two lines.** Everything after is evidence.
- **Name a comment deadline and a default.** "If nothing by Thursday 12:00, we proceed with option A" turns silence into a decision instead of a stall — this is the single mechanism that makes async work.
- **Name who must respond**, by name. "Thoughts welcome" gets none.
- **Cap it.** A one-page update is read; a five-page one gets a meeting scheduled about it.
- **Keep one live escape hatch**: "if this deadlocks, we take 25 minutes Friday."

Async fails predictably in four cases — take the meeting: the topic is emotionally loaded; the disagreement is about values rather than facts; the group has never worked together; or the decision is a one-way door and the write-up cannot anticipate every objection.

## Calendar Defenses

- **A no-meeting block only survives if it is visible and defended by someone senior.** A blocked-out morning that anyone can override is decoration; state whose block it is.
- **Batch, do not scatter.** Five meetings in one afternoon costs one afternoon; the same five spread over three days costs three.
- **Office hours consolidate the long tail.** One weekly 50-minute slot absorbs most "quick question" invites, and the ones that do not come are the ones that were never worth a meeting.
- **Buffers are load-bearing.** 25/50 defaults produce them automatically; back-to-back 60s guarantee the third meeting starts late and the notes never get written.
- **Recurring invites get an end date at creation** — six months out at the longest (SKILL.md Rule 7). The calendar is where zombie meetings are born.
- **Protect the day before a big one.** A board meeting, a QBR or a launch review needs its prep block booked at the same time as the meeting itself, or prep happens at 23:00 the night before.

**After any load audit, decline that changes a series, or async replacement**, write it back in the same turn: the audit numbers and any norm in `## Meeting Norms`, the series row with its new cadence or expiry in `## Series`, and a killed series in `~/Clawic/data/meetings/series.md` under `## Killed` (`memory-template.md`). An audit whose conclusion lives only in the chat gets rerun from zero next month.

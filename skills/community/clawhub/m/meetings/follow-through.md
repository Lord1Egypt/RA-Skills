# Follow-Through — Action Items, The Sweep, And Chasing What Slipped

**Before any sweep, chase or status answer**, read `## Follow-Ups` in `~/Clawic/data/meetings/memory.md` (or `~/Clawic/data/meetings/follow-ups.md` if `## Boxes` points there), `follow_up_sweep_day` in `config.yaml`, and the `Context` column of the owner in `~/Clawic/data/contacts/contacts.md` — how someone answers a chase is a property of the person, not of the item. **Check `## Due`** against today's date and state an overdue sweep in one line.

**Contents:** [Anatomy Of An Action Item](#anatomy-of-an-action-item) · [One Ledger, Not Twelve](#one-ledger-not-twelve) · [The Weekly Sweep](#the-weekly-sweep) · [The Escalation Ladder](#the-escalation-ladder) · [Chasing Someone Senior Or External](#chasing-someone-senior-or-external) · [When The Owner Is The User](#when-the-owner-is-the-user) · [Killing Dead Items](#killing-dead-items)

## Anatomy Of An Action Item

Four fields, and an item missing any one of them will not survive the week: `owner — verb + object — date — done means`.

| Field | Failure without it | Test |
|---|---|---|
| **Owner**, one named person | A team owner is nobody's Monday morning | Can you address a message to it? |
| **Verb + object** | "Look into pricing" ends when attention does | Does it name a produced thing? |
| **Date**, absolute | "Next week" drifts a week per week | Is it a calendar date, not a relative one? |
| **Done means** | Two people disagree about whether it closed | Could a third party mark it done without asking? |

- **`Done means` is what makes an item closeable by someone other than its author** — the sweep can only verify what was defined. "Vendor comparison" → "table in the channel, three options with prices".
- **Absolute dates only.** "By Thursday 30 Jul" is verifiable four weeks later; "next week" is not. If the owner will not commit to a date, the real answer is that it is not going to happen — record that instead of a fake date.
- **Split anything longer than two weeks.** An item with a distant date gets no attention until the week it is due, so the first checkpoint is the actual item and the far date is a milestone.
- **The owner has to have heard it.** Read every item back in the close (SKILL.md, The Last Five Minutes) while the room can still object. An item assigned in writing after the meeting gets refused by email two days later.
- **Actions the user owns go in the same ledger as everyone else's.** A private to-do list next to the meeting ledger guarantees one of the two is stale.

## One Ledger, Not Twelve

Every action item from every meeting lands in one list, `## Follow-Ups`, whatever meeting produced it. Per-meeting lists are the single most common reason follow-through fails: nothing is ever reviewed as a whole, so a Tuesday commitment is invisible on Friday.

- **Two tables, different physics.** `Open` is what the user or their team owes; `Waiting On` is what is owed *to* the user. They are chased differently and read differently, so they never share a table.
- **Open items only.** A closed item leaves the ledger and its closure is written into that month's record block — a ledger that keeps history stops being usable as a to-do list.
- **The `From` column is the audit trail**: date plus meeting name. It answers "who agreed to this and where" without opening anything.
- **The ledger is the answer to "where are we".** Never reconstruct status by rereading records; if the ledger cannot answer it, the ledger is broken and gets fixed, not bypassed.

## The Weekly Sweep

One pass, same day every week (`follow_up_sweep_day`, default Friday), 10-15 minutes for a ledger of ~20 items. Read the whole list end to end — sampling defeats the purpose.

For each open item, exactly one of four outcomes. There is no fifth, and "still in progress" is not one of them:

1. **Done** — delete the row, record the closure in that month's record block.
2. **On track** — leave it; no message needed. Chasing an item that is not yet due trains people to ignore chases.
3. **Slipped** — a *new* date and the reason, in the row. Two consecutive slips is a signal about scope or capacity, not about diligence, and the fix is re-scoping.
4. **Dead** — the reason it stopped mattering, then delete it. Say so to the owner, so they stop carrying it.

- **Sweep before the meeting that produced the items, not after.** Arriving at the platform sync with last week's items already reconciled changes the meeting from a status round-robin into a decision meeting.
- **A ledger where nothing ever slips is not being read.** Some slippage is the sign the dates were honest.
- **If more than about a third of the items slipped, the problem is intake, not follow-through.** Meetings are producing more commitments than the week can hold — cap items per meeting instead of chasing harder.

## The Escalation Ladder

Four rungs, each one costing more relationship capital than the last. Never skip a rung, never repeat one twice with the same wording.

| Rung | When | Shape |
|---|---|---|
| **1. Nudge** | Day after the due date | Friendly, assumes nothing: "is the vendor comparison still on for today, or has something moved?" |
| **2. State the impact** | ~3 days late, or one full cycle | Facts, no adjectives: "without it we cannot brief the board on Thursday; can you give me a date I can plan against?" |
| **3. Offer to remove the blocker** | The impact was acknowledged, nothing moved | "What would unblock this — do you need someone else's input, or should we cut the scope to two options?" |
| **4. Involve the chair or re-scope** | Two cycles late, impact stated | Publicly at the meeting that owns it, factually: "this is two weeks late and it blocks X. Do we re-scope it, move it, or drop it?" |

- **Escalation is about the item, never about the person.** "You have not done this" is a character claim; "this is late and blocks X" is a fact anyone can act on.
- **Every rung offers an exit.** A chase with no way out except compliance produces silence, and silence is the failure mode that costs the most time.
- **Rung 4 is not a punishment, it is a decision request.** The chair's job is to re-scope, reassign or kill — three legitimate answers, all better than a fifth private nudge.
- **Three nudges with no change means the item was never really accepted.** Go back to the commitment, not forward to the pressure.

## Chasing Someone Senior Or External

- **Make the ask smaller than the original.** A senior person who cannot deliver the document can usually deliver a yes/no in one line — take that and re-scope the rest.
- **Attach a default.** "If I don't hear by Thursday 12:00 I'll proceed with option A" converts silence into a decision instead of a stall, and it is the only chase that works reliably across organizations.
- **Chase in the channel the person actually answers in** (`Preferred channel` in `~/Clawic/data/contacts/contacts.md`). A chase in an unread channel is a chase the user has to send again.
- **External parties get dates in writing, always.** Verbal client commitments have no ledger on their side; the same-day recap with the dated next step is the mechanism (`external.md`).
- **Two chases to an external party, then it escalates to the relationship owner**, not to a third chase. A vendor who ignores two nudges is answering.
- **Never chase in a DM if the item was agreed in a group.** The group loses visibility, the item gets chased twice by two people, and the record disagrees with reality.

## When The Owner Is The User

- **The user's own late items get named first**, before anyone else's, in the meeting and in the recap. It costs fifteen seconds and removes the leverage someone was about to use.
- **A slipped item the user owns gets a new date and a reason like any other row.** Quietly re-dating your own items while chasing others is how a ledger loses its authority.
- **If the user is late on the same item three sweeps in a row, it is not a scheduling problem.** Either the item is not actually theirs, or it is not actually going to happen — decide which, out loud.

## Killing Dead Items

An item can stop mattering, and pretending otherwise poisons the whole ledger.

- **Kill criteria**: the decision it supported was reversed, the project moved, the requester stopped needing it, or nobody can now say what "done" was.
- **Say it out loud to whoever asked for it.** An item that vanishes silently teaches the room that the ledger is theatre.
- **A killed item that keeps coming back is a decision that was never made.** Log the decision instead, with its rejected options (`decision-rights.md`).
- **Age is not a kill reason on its own** — a six-month-old item with a live consequence is still live. Consequence is the test, never staleness.

**Write in the same turn as the sweep or the chase**: each new or re-dated item as a row in `## Follow-Ups` of `~/Clawic/data/meetings/memory.md`, each closure into that month's block in `~/Clawic/data/meetings/records/<year>-<mm>.md`, the next sweep date in the `## Due` table, anything learned about how a person responds to a chase into their `Context` in `~/Clawic/data/contacts/contacts.md`, and a recurring pattern of slippage into `## Pain Points` (`memory-template.md`). Once `## Follow-Ups` passes ~15 open items it splits to `~/Clawic/data/meetings/follow-ups.md` with the same headings, and its `## Boxes` line is written in the same turn. A chase that is not written back gets sent twice, and the second one costs more than the first.

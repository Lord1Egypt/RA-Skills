# Agendas — Designing The Meeting Before It Exists

**Before designing a meeting**, read `## Series` in `~/Clawic/data/meetings/memory.md` (does this already exist under another name?), `~/Clawic/data/meetings/decisions.md` (is this settled?), and `## Meeting Norms` (no-meeting blocks, timezone spread, who never reads pre-reads). If `## Boxes` names a charter for this series, that charter is the design — change it there, not in the invite.

**Contents:** [Agenda Line Grammar](#agenda-line-grammar) · [Timebox Math](#timebox-math) · [The Invite List](#the-invite-list) · [Pre-Reads](#pre-reads) · [Templates By Purpose](#templates-by-purpose) · [Invite Hygiene](#invite-hygiene) · [Cancelling Well](#cancelling-well)

## Agenda Line Grammar

Every line is `output — owner — minutes`. A topic noun is not an agenda item, because it has no end state and therefore ends when the clock does.

| Bad line | Why | Good line |
|---|---|---|
| Roadmap | No end state | Q4 scope: cut one of the three epics — Priya — 12 |
| Budget discussion | Discussion is not an output | Approve or reject the 15k QA contractor — Ana — 8 |
| Updates | Should be written | *(deleted; async thread)* |
| AOB | Unbounded, at the worst moment | AOB collected at the top, 3 min, or dropped |
| Marketing sync | Names the attendees, not the work | Agree the launch date and who announces — me — 10 |

An agenda that survives contact has three properties: each line names its output, each line has one named owner (not a team), and the owners have seen the line before the meeting starts.

## Timebox Math

`sum(item minutes) ≤ 0.8 × slot`. The remaining 20% is the close (SKILL.md Rule 5) — decisions read back, actions assigned, next step named. It is not slack, and it is the first thing that gets eaten if you do not reserve it.

| Slot | Content budget | Close | Realistic item count |
|---|---|---|---|
| 15 min | 12 | 3 | 1 |
| 25 min | 20 | 5 | 1-2 |
| 50 min | 40 | 10 | 2-3 |
| 90 min | 72 | 18 | 3-4, with a break |

- **Hard items first, while attention is highest and latecomers have not yet reset the room.** The instinct to warm up with easy items spends the good half of the meeting on the cheap decisions.
- **Anything over 90 minutes needs a 10-minute break per 90**, or the last block is theatre (`workshops.md`).
- **One decision per 25-minute slot** is the honest rate when people disagree. Two is possible only when the second is a formality.
- If the items do not fit, cut items — never shave the close, never extend the slot by 15 "just in case".

## The Invite List

Three categories, and only the first two get an invite:

| Category | Test | Invite |
|---|---|---|
| Decider | Can commit the resource or make the call | Required. If they cannot attend, move the meeting or change the decider |
| Contributor | Holds information the decision needs, or must execute the outcome | Required |
| Affected | Will be impacted but adds nothing live | **Recap, not invite** (SKILL.md Rule 8) |

Ceilings, from the purpose type: decision ≤8 (two-pizza rule); generative ≤12 and only with breakouts; working session 3-6; anything larger is a broadcast and should be a document plus a Q&A channel.

- **Every extra attendee costs the whole room, not just their own time** — airtime is finite, so a ninth person does not add 12% cost, they subtract from everyone else's turn.
- **"Optional" is read as required by everyone junior in the room.** If they are optional, they are Affected: take them off and send the recap.
- **Do not invite the decider's deputy as insurance.** A room with a proxy cannot decide, and everyone knows it by minute five.
- **Invite one outsider to a review that keeps agreeing with itself.** A single person who does not share the team's assumptions is the cheapest fix for a room with no dissent.

## Pre-Reads

- **Send ≥24h ahead** (SKILL.md Rule 3). Under 24h it will not be read, and pretending otherwise costs the first 20 minutes.
- **Read it in the room, in silence.** Budget ~2 minutes per page of dense narrative: a 6-page memo buys 12-15 minutes of silence — expensive, and still cheaper than someone reading it aloud badly while five people follow along.
- **Prose beats slides for anything with reasoning.** Bullets let a weak argument hide in the whitespace; a paragraph forces the connective tissue to exist.
- **Cap the pre-read at what the decision needs.** Appendices are welcome, but the argument fits on one to six pages.
- **State at the top what the reader must do**: "decide X", "flag anything that would make you object", "no action, context only".
- If nobody reads pre-reads in this organization, stop sending them and design a silent-read block instead. That is a norm to record, not a battle to fight every week (`## Meeting Norms`).

## Templates By Purpose

**Decide (25 min):** context 3 · options and the recommendation 6 · objections, by name 8 · decision and its rejected options 3 · close 5. The method (`decision_method`) is stated in line one of the invite, not discovered live.

**Generate (50 min):** frame the question and the constraints 5 · silent individual generation 8 · pairs 8 · whole group harvest 12 · converge with dot voting 7 · close 10. Never open with an unstructured group brainstorm — the first idea spoken anchors the rest (`workshops.md`).

**Align (25 min):** the plan, already written and circulated 0 · objections and gaps, round by name 12 · resolve or escalate each 8 · close 5. If there are no objections in the first round, ask the quietest person directly before accepting agreement.

**Build trust (30-50 min):** no agenda beyond a first question and an end time. The output is the relationship; a checklist is the fastest way to kill it.

**Kickoff (90 min):** why now and what success looks like 15 · scope in and explicitly out 20 · roles and decision rights 20 · risks and the first milestone 17 · close 18. Decision rights agreed at kickoff prevent most of the escalations the project will otherwise generate.

## Invite Hygiene

- **Title = the output**, not the audience: "Decide Q4 scope" beats "Product sync". It is what makes an invite skimmable and declinable.
- **Agenda in the invite body**, not attached and not "to follow". An agenda that arrives separately is not read.
- **Honest duration.** A 25-minute meeting booked for 60 will take 60.
- **Timezone in the body** when anyone is remote, written for the recipient's zone (`remote.md`).
- **Recurrence gets an end date at creation** — six months maximum (SKILL.md Rule 7).
- **Joining details carry no secret.** A link with an embedded passcode or a dial-in PIN is a credential: keep it out of anything stored under `~/Clawic/data/` and reference it as a pointer (`memory-template.md`).
- **Attach the pre-read link, and name the read time**: "6 pages, ~15 min, we read it in the room".

## Cancelling Well

- Cancel as early as you know, with the reason and the replacement: "no decision ready, I'll send the update Friday instead". A cancellation with no replacement teaches people the meeting was never load-bearing.
- Cancelling a single occurrence of a series is free. Cancelling three in a row is a kill review that has not admitted itself (`recurring.md`).
- Never cancel by silence. A meeting nobody attends stays on twelve calendars forever.

**When a meeting design is worth keeping** — a charter for a series, an agenda template that produced clean decisions twice, a kickoff structure — write it to `~/Clawic/data/meetings/artifacts/<kebab-name>.md` with its `## Boxes` line in the same turn, and put the series itself (cadence, owner, purpose type, attendees, expiry date) in `## Series` of `memory.md` (`memory-template.md`). A design that lives only in a sent invite gets re-derived by the next person who inherits the meeting.

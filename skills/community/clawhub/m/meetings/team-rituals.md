# Team Rituals — Standup, Retro, Planning, Demo, All-Hands, Incident Review

**Before running or fixing a ritual**, read its row in `## Series` of `~/Clawic/data/meetings/memory.md`, `## Pain Points` (this team has probably broken this ritual before in a specific way), and the format artifact in `artifacts/` if `## Boxes` names one — a retro format that worked twice is the format, not a fresh invention. Each ritual below carries the timebox, the single output, and the specific way it rots.

**Contents:** [Standup](#standup) · [Retrospective](#retrospective) · [Planning](#planning) · [Demo Or Sprint Review](#demo-or-sprint-review) · [All-Hands](#all-hands) · [Incident Review](#incident-review) · [Choosing The Ritual Set](#choosing-the-ritual-set)

## Standup

**Output**: blockers surfaced and picked up by name. **Timebox**: 15 minutes, hard (Scrum Guide). **Attendees**: the people doing the work, ≤10.

- **It is a synchronisation, not a report to the manager.** The tell is where people look while speaking: at the manager means it has become a status meeting, and the information was writable.
- **Walk the board, not the people.** Going item by item across the work surfaces the stalled ticket that nobody owns; going person by person surfaces only what each person chose to mention.
- **"Blocked" must produce a name and a time in the same breath** — "blocked on the DPA; Marc, can we talk at 11?" A blocker announced with no pickup is announced again tomorrow.
- **Everything that needs two people goes after**, explicitly: "let's take that at 10:15, Sam and Lena." The standup's job is to *find* the conversations, not to have them.
- **Above ~10 people it is a broadcast.** Split by workstream; two 15-minute standups cost less than one 30-minute one because each has half the audience.
- **Async standup works when handoffs are rare and the team writes well**: same three questions in a thread by a fixed hour, with the same rule that a blocker names a person. It fails when nobody reads the thread — the test is whether blockers get picked up the same day, never whether people enjoy it.
- **Rots into**: a status round-robin for the manager. Fix by removing the manager for two weeks, or by walking the board instead of the room.

## Retrospective

**Output**: 1-3 owned experiments with names and dates. **Timebox**: 60-90 minutes per two-week sprint (Scrum Guide caps it at 3h for a one-month sprint). **Attendees**: the team; managers by exception and never the first time.

Five phases, and skipping the first is why most retros produce a list nobody owns:

1. **Set the stage** (5 min) — restate the prime directive: everyone did the best they could with what they knew at the time (Kerth). It is not niceness, it is the precondition for anyone naming a real problem.
2. **Gather data** (15 min) — silent written first, always. Timeline of the sprint, or the plain three columns. Speaking first hands the frame to whoever talks fastest.
3. **Generate insight** (20 min) — cluster, then ask why on the top cluster. Toyota's five whys works here precisely because the fifth answer is usually a process, not a person.
4. **Decide what to do** (15 min) — dot vote, then **cap at three experiments**, each with an owner and a date. A retro producing nine actions ships one.
5. **Close** (5 min) — check the previous retro's experiments first or last, but always: a retro that never revisits its own actions is a feelings meeting.

- **Start every retro by reviewing the last one's three items.** This single habit is the difference between a retro that changes something and a retro that recycles the same complaint quarterly.
- **Rotate the facilitator**, and pull one in from outside the team when the team is in conflict — a facilitator who is also a participant cannot do either job.
- **Anonymous input when trust is low or a manager attends.** The data you need is precisely the data people will not sign.
- **Rots into**: a complaints log with no owners, or a ritual where the same three items are raised and nothing moves. Fix by capping at three, assigning names, and opening the next retro with them.

## Planning

**Output**: a committed scope with named owners and the known risks. **Timebox**: ≤2h per two-week sprint (Scrum Guide: max 8h for a one-month sprint). **Attendees**: the team, plus whoever can answer scope questions.

- **Refinement is a different meeting and it happens before.** Planning that starts with "what is this ticket?" is refinement wearing planning's slot, and it will overrun.
- **Estimate to expose disagreement, not to produce a number.** The value of planning poker is the moment two people show wildly different cards and discover they were solving different problems; the number itself is nearly worthless.
- **Capacity honestly, including the interrupts.** Planning at 100% capacity guarantees the plan is wrong by Wednesday; subtract holidays, on-call, and the historical support load.
- **Commit to less than fits.** A plan finished early produces trust; a plan overrun by 20% produces a conversation about estimates that costs more than the work.
- **Every committed item gets a named owner in the room**, not at the end by email (SKILL.md Rule 5).
- **Rots into**: a three-hour ticket-writing session. Fix by moving refinement out and requiring items to arrive already understood.

## Demo Or Sprint Review

**Output**: feedback from people who were not in the build, and a scope adjustment if it earned one. **Timebox**: 30-60 minutes. **Attendees**: the team plus real stakeholders and, where possible, a real user.

- **Show working software, not slides.** A slide about a feature is a claim; the feature is evidence. If it cannot be shown, it is not done and the demo says so honestly.
- **The people who can change the plan must be present**, or the feedback lands nowhere and the ritual becomes a performance.
- **Demo the unfinished thing too, labelled as unfinished.** The expensive feedback arrives about the half-built version, when changing it is still cheap.
- **Capture feedback as items with owners in the room**, not as "we'll take that on board".
- **Rots into**: a rehearsed showcase with no decisions. Fix by inviting someone who will actually object, and by ending with a scope decision or an explicit "no change".

## All-Hands

**Output**: questions answered live that could not be answered in writing. **Timebox**: 30-45 minutes. **Attendees**: everyone.

- **The written update goes out first, and the meeting is the Q&A.** Reading slides aloud to the whole company is the single most expensive meeting most organizations run: a 45-minute broadcast to 200 people is 150 person-hours.
- **Collect and upvote questions in advance.** It gets the awkward question asked — the one everyone is thinking is almost never asked live by anyone.
- **Answer the top-voted question first, including the uncomfortable one.** Skipping it teaches people the channel is decorative, and the next round gets no questions at all.
- **"I don't know" plus a date beats a confident non-answer.** Then honour the date in the next all-hands, out loud.
- **Bad news gets its own slot, headline first**, never buried between a product update and a hiring number (`difficult.md`).
- **Record it and post the recording with the written recap** — timezones make the live room a minority of the company in any distributed org (`remote.md`).
- **Rots into**: a slide deck read aloud with no questions. Fix by publishing the deck beforehand and spending the slot only on questions.

## Incident Review

**Output**: a timeline, the systemic causes, and owned remediations. **Timebox**: 60 minutes, within a week of the incident. **Attendees**: the responders plus one person who was not involved.

- **Blameless is a mechanical property, not a tone.** Ask what made the wrong action look correct at the time; if the answer is "they should have known", the review has produced no change.
- **Build the timeline before the discussion**, from logs and messages, with times. Memory of an incident reorders itself within days, and a disputed timeline eats the hour.
- **Separate the trigger from the causes.** The deploy that broke it is the trigger; the absence of a canary is the cause, and only causes generate remediations.
- **Remediations are action items with owners and dates**, or they are wishes. Cap at what the next two weeks can hold.
- **One outsider in the room** catches the assumption everyone on the team shares.
- The write-up itself is a different artifact with its own structure and lifecycle (`postmortem` skill); this meeting produces the timeline and the owned items it needs.
- **Rots into**: a search for the person who typed the command. Fix by asking what the system made easy, and by having someone outside the team facilitate.

## Choosing The Ritual Set

Rituals compound: four of them at weekly cadence for a team of six is already ~10 person-hours a week before any real work.

| Team situation | Keep | Drop or make async |
|---|---|---|
| Tightly coupled work, frequent handoffs | Daily standup, planning, retro | Demo if stakeholders never attend |
| Senior team, independent workstreams | Retro, planning | Standup → async thread |
| Fully remote across >6h of timezone spread | Retro (recorded), written planning | Standup and demo → async with recordings (`remote.md`) |
| New team, still forming | All of them, briefly | Nothing — the ritual set is how norms get built |
| Team in a crunch | Standup only | Everything else for two weeks, then reinstate deliberately |
| Anything else | Start with retro; it is the ritual that repairs the others | Add one at a time, each with an expiry date (Rule 7) |

- **Add rituals one at a time, each with an expiry date**, so the set can be evaluated instead of inherited.
- **A ritual nobody prepares for has already been killed** by everyone except the calendar; take it to a kill review (`recurring.md`).

**Write in the same turn as any ritual you run or change**: a record block in `~/Clawic/data/meetings/records/<year>-<mm>.md` (retro experiments and incident remediations included), each experiment or remediation as a row in `## Follow-Ups` with owner, date and definition of done, the ritual's cadence and expiry in `## Series`, a format that worked twice as `~/Clawic/data/meetings/artifacts/retro-format-<team>.md` or `artifacts/standup-format-<team>.md` with its `## Boxes` line, and a failure worth not repeating in `## Pain Points` (`memory-template.md`). Retro experiments that are not in the ledger are re-proposed at the next retro by the same person.

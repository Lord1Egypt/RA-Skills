# Workshops — Offsites, Generative Sessions And Design Reviews

**Before designing a workshop**, read `## Meeting Norms` in `~/Clawic/data/meetings/memory.md` (timezone spread, no-meeting blocks, who never reads pre-reads), the attendees' `Context` in `~/Clawic/data/contacts/contacts.md` (who dominates, who only writes), `~/Clawic/data/meetings/decisions.md` for anything already settled that the room will try to reopen, and the plan artifact in `artifacts/` if `## Boxes` names one — a workshop plan that worked is reused, not reinvented.

**Contents:** [The One Rule](#the-one-rule) · [Diverge Then Converge](#diverge-then-converge) · [The Method Catalog](#the-method-catalog) · [The Facilitator's Clock](#the-facilitators-clock) · [Design And Code Review](#design-and-code-review) · [Offsite Design](#offsite-design) · [Energy And Attention](#energy-and-attention) · [The Harvest](#the-harvest)

## The One Rule

**A workshop produces a tangible artifact by the end, or it was a very expensive conversation.** Ten people for a half day is 40 person-hours; name the artifact in the invite — a prioritized roadmap, a decided architecture, a written team charter, a set of ranked options with an owner each — and design backwards from it.

- **The artifact must be producible in the room.** "Alignment" is not an artifact; "one page everyone in the room has read and objected to" is.
- **Write the closing slide first.** If you cannot fill in the blanks of the final output before designing the agenda, the workshop has no shape yet.
- **One artifact per half day.** Two goals in one day means both get the tired half.

## Diverge Then Converge

Every generative session is two different meetings with opposite rules, and mixing them is why group brainstorms underperform.

| Phase | Rule | Failure if mixed |
|---|---|---|
| **Diverge** | Quantity, no evaluation, silence and writing before speech | The first idea spoken anchors everyone; criticism kills the half-formed idea that was going to be the good one |
| **Converge** | Criteria first, then filter; explicit owner for the decision | Endless option generation, nobody chooses, the session ends with a photo of sticky notes |

- **Separate them out loud, with a clock.** "For the next eight minutes nothing gets evaluated. At 10:20 we switch and start cutting."
- **Silent individual generation always precedes group discussion.** Independent ideas first, then combination — the reverse produces variations on the first thing said, which is Osborn's brainstorming as commonly practised and the reason it is outperformed by writing-first formats.
- **Converge on criteria before options.** "What makes a good answer here?" agreed first turns the choice into an evaluation instead of a debate about taste.
- **The groan zone is structural, not a facilitation failure.** Every real convergence has a middle where the group is tired and no option looks good; name it, hold the clock, and do not let the room escape into a new divergence.

## The Method Catalog

Pick by what the room is failing at, not by novelty.

| Method | Shape | Use when |
|---|---|---|
| **1-2-4-All** | 1 min alone · 2 min in pairs · 4 min in fours · 5 min whole group (Liberating Structures) | Default for any question with >6 people; every voice contributes before the room hears anyone |
| **Brainwriting 6-3-5** | 6 people write 3 ideas in 5 minutes, pass the sheet, build on what they receive, 6 rounds | Divergence with dominant personalities present; 108 idea-slots with zero airtime competition |
| **Dot voting** | Each person gets ~n/3 dots for n options; vote silently and simultaneously | Narrowing 15 options to 4; never as the final decision, which still needs an owner |
| **Affinity clustering** | Silent grouping of written items, then name the clusters | 40+ raw items that need structure before anyone can choose |
| **Pre-mortem** | "It is a year from now and this failed. Write why." Individually, then read out (Klein) | Before committing to a plan; it legitimizes the doubts that politeness suppresses |
| **Nominal group technique** | Silent generation · round-robin one item each · clarify · rank privately | Mixed seniority where juniors will not contradict a director |
| **Fishbowl** | 4-5 chairs discuss in the centre, everyone else observes; an empty chair anyone can take | 20+ people and a genuine debate; keeps a real conversation audible |
| **Assumption reversal** | State the assumptions, invert each, design for the inverted world | The room keeps producing the same three ideas |
| **Anything else** | Silent written round, then cluster, then dot vote, then name a decider | Default sequence when no method obviously fits — writing first fixes most rooms |

- **Every method above starts with silence and paper.** That is the mechanism, not the format's branding.
- **Dot voting is a filter, never a decision.** The room votes to shortlist; a named owner decides (`decision-rights.md`). Voting as the decision hides the minority argument that was usually the interesting one.
- **Breakouts of 3-5, never 6+.** A breakout of eight is a plenary with worse acoustics. Give each one a written deliverable and a hard return time.

## The Facilitator's Clock

- **The facilitator does not have opinions on the content.** Trying to do both means one collapses, always the facilitation. If the user must contribute, hand the clock to someone else for that block.
- **Announce the timebox before each block, and the remaining time at its midpoint.** A workshop is a sequence of small meetings and each one needs its own close.
- **Overruns are chosen out loud**: extend this block and drop a later one, or park and move on. Silent overrun is a decision to drop the harvest, which is the block that produces the artifact.
- **Park visibly, with a name and a date at the close.** The parking lot is where good objections go to die unless items leave it.
- **Build in one unallocated 20-minute block per half day.** Something will overrun; the alternative is losing the close.
- **Ending 20 minutes early is a feature.** Give the time back explicitly.

## Design And Code Review

**Output**: accept, accept-with-changes, or reject — with the reason. **Length**: 50 minutes. **Attendees**: 3-6.

- **The document is read in the room, in silence**, unless it genuinely arrived ≥24h ahead and people genuinely read it. Budget ~2 minutes per page of dense narrative: a 6-page design buys 12-15 minutes of silence and saves 20 minutes of someone narrating it badly.
- **Comments before verdicts.** Collect written comments during the silent read, then walk them by severity — blocking, significant, nit — so the meeting spends its time on the blocking ones.
- **The author presents nothing.** If the design needs a spoken introduction to be understood, it is not ready for review.
- **Name the decision rights up front**: who can veto, who can only advise. A review with unclear rights ends in "let's take it offline".
- **Reject is a legitimate outcome and must be said in the room**, not implied by silence and a follow-up meeting that never gets scheduled.
- **Cap the review at what one sitting can hold.** A 40-page design gets reviewed in sections across two sessions, or it gets rubber-stamped.
- **One outsider on any review that keeps agreeing with itself.** A single person who does not share the team's assumptions is the cheapest fix for a room with no dissent.

## Offsite Design

- **Half-day blocks, and never more than two content blocks per day.** The third block produces material nobody will act on.
- **Two objectives maximum for a two-day offsite**, each with its artifact. Every additional objective halves the depth of all of them.
- **Send the pre-read a week out, and design as if nobody read it** — a silent read block at the start costs 20 minutes and removes the entire "getting everyone on the same page" morning.
- **Social time is scheduled work, not the gaps.** For a distributed team, the unstructured hours are frequently the highest-value part of the trip, and leaving them to chance means people work through them.
- **The last block is always the harvest**, never a new topic: what was decided, who owns what, when it lands. Offsites fail at the harvest far more often than at the content.
- **Book the follow-up review before leaving the room** — four weeks out, on the calendar, with the artifact attached. Offsite decisions decay faster than any other kind because everyone returns to the work that was waiting.

## Energy And Attention

- **A 10-minute break per 90 minutes, minimum**, and hold it even when the room says it is fine — the room is a poor judge of its own attention.
- **Alternate modes**: individual writing → small group → plenary → break. Two consecutive plenary blocks lose the quiet half of the room permanently.
- **Hard thinking before lunch.** The post-lunch block is for divergent or hands-on work, never for the one-way-door decision.
- **Physically standing or moving between blocks** does more for a long session than any facilitation technique.
- **Hybrid workshops need a different design, not the same one with a camera** — remote participants cannot read a room or reach the whiteboard, so everything moves to a shared document and every breakout is a separate call (`remote.md`).

## The Harvest

The last 20% of the session, and the only block that must not be cut.

1. **Read the artifact back.** Not a summary of the discussion — the actual output, on screen, as it will be circulated.
2. **Decisions with their decider and method**, out loud, one sentence each.
3. **Owners and dates** for everything that leaves the room, read back with `owner — verb + object — date — done means`.
4. **Parked items** with a name and a date each.
5. **The follow-up review date**, on the calendar before anyone stands up.
6. **Photograph or transcribe every wall artifact before leaving.** A wall of sticky notes that only exists in the room is a workshop that produced nothing.

**Write in the same turn as the harvest**: the record block in `~/Clawic/data/meetings/records/<year>-<mm>.md`, each decision in `~/Clawic/data/meetings/decisions.md` with its rejected options, every owned item in `## Follow-Ups` with owner, date and definition of done, the follow-up review as a row in `## Due`, and the plan itself — agenda, methods, timings, what worked and what overran — as `~/Clawic/data/meetings/artifacts/workshop-<topic>.md` with its `## Boxes` line, because the second offsite is designed from the first one's plan or from nothing (`memory-template.md`). Digitize the walls in the same turn: a photo on someone's phone is not a stored artifact.

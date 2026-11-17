# Routines, Stacks, and Chains

Several habits joined into one sequence. Powerful, and the most common way a working set of habits becomes a fragile one.

**Before building or repairing a routine**, read `## Habits` in `~/Clawic/data/habits/memory.md` for which of the links already exist and their rates, and open `artifacts/routine-<name>.md` if `## Boxes` lists one — an existing routine gets edited, never rewritten from scratch.

**Contents:** [Chain Reliability](#chain-reliability) · [Building a Stack](#building-a-stack) · [Morning Routines](#morning-routines) · [Evening and Shutdown Routines](#evening-and-shutdown-routines) · [Keystone Habits](#keystone-habits) · [Logging a Routine](#logging-a-routine) · [Repairing a Broken Chain](#repairing-a-broken-chain) · [The Routine Artifact](#the-routine-artifact)

## Chain Reliability

A chain succeeds only if every link does. With independent links each at rate `p`, the chain's rate is `p^n`.

| Links | Each at 95% | Each at 90% | Each at 80% |
|---|---|---|---|
| 2 | 90% | 81% | 64% |
| 3 | 86% | 73% | 51% |
| 5 | 77% | 59% | 33% |
| 8 | 66% | 43% | 17% |

Real links are not independent — a routine has momentum, and finishing link 1 makes link 2 more likely — so these are pessimistic. What they get right is the direction and the steepness: **every link added lowers the whole routine's reliability, and the effect compounds.** Three links is the working maximum, and only one of them should be new (`design.md`).

The corollary that saves routines: **the chain's rate is bounded by its weakest link.** A five-link morning routine containing one 60% habit cannot exceed 60%. Fix or remove that link before adding anything.

## Building a Stack

1. **Start from an anchor that is at least three months old** and happens on every scheduled day. Coffee, teeth, the commute, closing the laptop.
2. **Add exactly one new link**, at the floor, and hold for 14 days before considering a second.
3. **Order by ascending resistance.** Easiest first: the completed link supplies the momentum for the next one. A routine that opens with its hardest element fails at the door.
4. **Order by physical logic where it conflicts with resistance.** Do not walk between rooms twice; grouping by location beats a marginal resistance ordering.
5. **Put the non-negotiable first**, not last. Whatever must happen on a bad day goes at the front, where the routine still exists.
6. **Cap the total time.** A routine longer than the shortest morning the user has is a routine that gets skipped whole rather than partially.

Stack format, written out and stored: *after `<anchor>`, I will `<A>`, then `<B>`, then `<C>`* — each with its own floor, in order.

## Morning Routines

Advantages that are real: fewer competing demands, and the day cannot have overrun yet. Failure modes that are just as real:

| Failure | Cause | Fix |
|---|---|---|
| Works on weekdays, gone at weekends | The anchor was the alarm or the commute, neither of which exists on Saturday | Anchor to something that happens both days, or define the weekend as `-` for the routine |
| Whole routine skipped after a late night | No shortened version exists, so it is all-or-nothing | Define the minimum routine: the first link only, explicitly allowed |
| Grew from 10 minutes to 50 | Each addition was small; the total was never checked | Re-time it, cap it, and drop the lowest-value link |
| Depends on getting up 45 minutes earlier | The routine now depends on a sleep change, which is a separate and harder habit | Anchor within the existing wake time first; earlier waking is its own project (`sleep`) |
| Phone first, routine second | The phone is a stronger competing cue with an immediate reward | Charge it in another room; the routine cannot win that competition on resolve (`environment.md`) |

## Evening and Shutdown Routines

Structurally harder than morning routines because the evening absorbs everything that overran during the day.

- **Anchor to an event, not a clock.** "After dinner" survives a shifted evening; "at 21:00" does not.
- **Shorter than the morning.** Three links maximum, and typically two.
- **Include the preparation for tomorrow's morning routine.** This is the highest-value evening link, because it moves friction from the fragile part of the day to the reliable one (`environment.md`).
- **Do not stack a work-shutdown routine onto a personal evening routine.** They serve different purposes, and combining them means a late work day takes both out.
- **A shutdown routine's job is a boundary**, so its last link should be observable and terminal: laptop closed and put away, tomorrow's list written, phone on the charger.

## Keystone Habits

Some habits raise the rate of others: the morning walk that makes the day's structure hold, the Sunday review that keeps everything else scheduled. The claim is real for individual users and unpredictable in advance — do not assert that a habit is keystone, detect it.

Detection: in a month of data, compare the completion rate of the other habits on days when the candidate was done against days when it was not. A gap of 20 points or more across at least 8 days of each kind is worth naming; less is noise (Rule 8). Record what was found in `## Patterns`, with the numbers.

Once identified, a keystone habit gets protected: it is the last one dropped in maintenance mode, the first one restored after a disruption, and it never shares a slot with anything else (`disruptions.md`).

## Logging a Routine

Two valid schemes. Pick one per routine and do not mix them.

| Scheme | Grid | Use when |
|---|---|---|
| One column per link | Each habit has its own column and its own rate | Links are also valuable alone, or one link is being diagnosed |
| One column for the routine | `y` only if every link happened; a partial gets `n` with a note naming the link that failed | The routine is the unit the user cares about and the links are all small |

The second scheme is compact and hides which link is failing — its note column is not optional. When a routine drops below 80%, switch temporarily to one column per link for two weeks; the split identifies the weak link, then merge back.

Never log a routine as a fraction ("3 of 5"). Partial credit reopens the daily negotiation the floor exists to close (`design.md`).

## Repairing a Broken Chain

1. **Identify the failing link** from the note column, or by splitting into columns for two weeks.
2. **Remove it from the chain** rather than fixing it in place. A struggling link inside a routine drags the whole sequence; outside it, it can be diagnosed alone (`troubleshooting.md`).
3. **Verify the chain recovers** without it. If it does not, the anchor is the problem, not the link.
4. **Re-add it at the end**, never in the middle, and only once its solo rate is ≥80%.
5. **If two links are failing, the routine is too long.** Cut to the non-negotiable one and rebuild.

A routine that has been rebuilt twice and failed twice is not a routine for this user's life. Keep the single highest-value habit and drop the sequence — one reliable habit beats a five-link routine at 30%.

## The Routine Artifact

A routine that survives a month is worth writing down as its own file: `~/Clawic/data/habits/artifacts/routine-<name>.md`, with its `## Boxes` line and the read condition "read when the `<name>` routine is discussed, rebuilt, or has lapsed".

Contents: the anchor, the ordered links with each floor, the total time, the minimum version for bad days, the weekend or travel variant, and a line on what was removed previously and why. The last line is what prevents a rebuilt routine from reintroducing the link that broke it twice.

**Whenever a routine is built, changed, repaired, or a keystone effect is detected**, write it in the same turn: the roster rows for the links in `memory.md`, the routine file at `artifacts/routine-<name>.md` with its `## Boxes` line, and any keystone finding with its numbers in `## Patterns` (`memory-template.md`).

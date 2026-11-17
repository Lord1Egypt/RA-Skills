# Partners, Stakes, and Rewards

Social and incentive levers. All of them are optional, several of them do harm on the wrong user, and `stakes_allowed` is off by default for that reason.

**Before proposing any of this**, read `## What Works` in `~/Clawic/data/habits/memory.md` (what this person has responded to and what backfired), `## Habits` for whether a partner is already named, and `config.yaml` for `stakes_allowed`. Read `~/Clawic/data/contacts/contacts.md` before naming any person, so an existing contact is updated rather than duplicated.

**Contents:** [Choose the Lever by Failure Mode](#choose-the-lever-by-failure-mode) · [Accountability Partners](#accountability-partners) · [Public Commitment](#public-commitment) · [Stakes and Forfeits](#stakes-and-forfeits) · [Rewards](#rewards) · [Body Doubling and Group Structure](#body-doubling-and-group-structure) · [What Never Goes In](#what-never-goes-in) · [Where the Person Is Recorded](#where-the-person-is-recorded)

## Choose the Lever by Failure Mode

Accountability is not a general-purpose booster. Each lever fixes one failure mode and is inert or harmful against the others.

| Failure mode | Lever that helps | Lever that does nothing |
|---|---|---|
| Does it alone, forgets, no external signal | A scheduled check-in | Money — there is nothing to lose against, only forgetting |
| Starts, then quietly stops, nobody notices | Partner or public commitment | Rewards — the problem is invisibility, not incentive |
| Knows exactly what to do and does not do it | Stakes, if this user has responded to them before | Another reminder |
| Finds it boring | Bundling or a training partner (`environment.md`) | Forfeits, which add dread to boredom |
| Has no time | Nothing here. This is a scheduling or capacity problem | All of them |
| Feels shame about the habit already | Nothing here. Remove existing stakes | Everything here makes it worse |

## Accountability Partners

The highest-yield and lowest-risk lever. Its effect comes from a scheduled moment of visibility, not from the partner's judgment.

Design rules:

- **A fixed check-in slot**, weekly at minimum. "Text me if you struggle" is not accountability; nobody texts.
- **Report the number, not the story.** The check-in is "4 of 5 sessions" — a narrative check-in becomes a conversation about reasons and stops being a measurement.
- **Symmetry helps and is not required.** Two people tracking their own habits and reporting to each other sustains longer than one-directional reporting, which starts to feel like supervision.
- **The partner is not the enforcer.** They receive the number. Any coaching role should be explicit and wanted, otherwise the relationship absorbs the friction of the habit.
- **Pick availability over closeness.** A colleague who reliably reads a Monday message beats a best friend in another timezone.
- **One partner, one or two habits.** A partner tracking five habits is a manager, and the arrangement ends.

Failure signs to watch for in the log: check-ins skipped for two consecutive weeks (the arrangement is over — say so and either restart it deliberately or drop it), or completions that spike the day before every check-in (the habit is now serving the check-in; move to a rate report rather than a streak report).

## Public Commitment

Announcing the habit to a group, a feed, or a team. Genuinely effective for some users and counterproductive for others, and the split is predictable.

- **Works** when the audience will actually notice absence — a running club, a team standup, a small group with a shared board.
- **Does not work** for a broadcast to an audience that will not follow up. The announcement itself delivers a sense of progress and can substitute for the behavior.
- **Announce the process, not the outcome.** "Running three times a week" invites the follow-up that helps; "running a marathon in October" invites congratulations now and silence later.
- **One announcement, not a running commentary.** Daily posting converts the habit into content production, which has its own motivation and collapses separately.

## Stakes and Forfeits

Money or a consequence attached to failure. Off by default (`stakes_allowed`), and only ever proposed to a user who has explicitly responded well to them before.

If used, the design rules are strict:

| Rule | Why |
|---|---|
| Stake the **rate**, not the streak | A streak-staked contract turns one bad day into a financial loss, which is the abstinence violation effect with a receipt (`relapse.md`) |
| Set the bar at the current rate, not the target | A contract the user is already failing is a subscription to losing |
| Fixed end date, 4-8 weeks | Open-ended contracts get abandoned and leave a bad association with the habit |
| A named referee who verifies | Self-reported contracts are theatre |
| Amount that stings and does not hurt | An amount that hurts adds financial stress to the exact week the habit is fragile |
| Never a stake tied to a person's disapproval | Shame is the one consequence that reliably ends the reporting |

Hard stops: no stakes on any habit in the Red Flags table of SKILL.md, none during a restart after a lapse, none in the first 30 days of a new habit (`starting.md`), and none on an avoid-habit with physical dependence.

If the contract carries a recurring payment or a paid service, its row goes to the shared `~/Clawic/data/finances/subscriptions.md` with the amount and its currency; cancelling the contract deletes the row (`memory-template.md`).

## Rewards

Reinforcement helps a behavior the user does not yet enjoy, and can crowd out an existing intrinsic motive for one they do.

- **Immediate beats large.** The reward has to arrive close enough to the behavior to be associated with it; a monthly prize is a plan, not a reinforcer.
- **Reward the completion, not the outcome.** Rewarding weight lost rewards a number that moves for unrelated reasons and punishes a good week with a flat scale.
- **Never reward with the thing being quit.** A week without cigarettes rewarded with a cigarette is not a reward schedule, it is a maintenance dose.
- **Remove the reward once the habit is self-sustaining** (above 90% for four weeks). Leaving it attached is where the overjustification risk lives.
- **Celebration is a free reward.** Fogg's practice of an immediate, deliberate moment of satisfaction at the completion costs nothing and needs no budget; it is the default when nothing else is appropriate.

Do not build a points system. Points become the object, the tally becomes the work, and the day the tally is not updated the habit goes with it (SKILL.md Traps).

## Body Doubling and Group Structure

Doing the habit in the presence of others, with no accountability content at all. Distinct from a partner: the mechanism is the presence, not the report.

- Effective for start-failures and for habits that are boring alone — study sessions, admin, training, practice.
- A class or a fixed group session adds a schedule and a small social cost to absence; that combination outperforms both a solo plan and a check-in for many users.
- Cost: it makes the habit dependent on the group's schedule. Always keep a solo fallback version so a cancelled class is not a missed day (`disruptions.md`).
- Frequently the correct first recommendation for a user with ADHD, ahead of any incentive scheme (`capacity.md`).

## What Never Goes In

- Punishment for a miss, in any form, including tone. It makes the next miss unreported, and unreported misses end the diagnosis.
- Comparison with another person's rate. It is demotivating when behind and licensing when ahead.
- A partner who was not asked, or a public commitment made on the user's behalf.
- Stakes on a habit the user is already anxious about.
- Any arrangement that continues past its end date by default. Everything here has a review date (`review.md`).

## Where the Person Is Recorded

A partner, a referee, a coach, a training group's organiser — these are people, and people live in the shared contacts box, not in this skill's folder.

- Write the row in `~/Clawic/data/contacts/contacts.md`: `Name | Key | Role | Preferred channel | Context | Last contact | File`. The `Key` is the identity column — lowercase email, else handle, else `<kebab-name>` with a stable disambiguator — and it is always written, never left implicit.
- **Read the file before adding.** If the key is already there, update that row in place; do not append a second row for the same person, and never rewrite a row this skill did not create.
- If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Past 15 people, or as soon as one does not fit in a row, the box moves to one `~/Clawic/data/contacts/<name>.md` per person with `contacts.md` as the index carrying the `File` pointer. If the folder already looks like that on arrival, follow it.
- Removing a partner means deleting the row this skill added and noting the date in `memory.md` — an inventory that only grows stops being one.
- In the habits roster, keep **only the person's name** as a pointer. Duplicating the contact here is how two skills end up contradicting each other.

**Whenever an accountability arrangement is agreed, changed, or ends**, write it in the same turn: the partner's name in the habit's roster row and their full row in the shared `~/Clawic/data/contacts/contacts.md`; the arrangement and its end date in `## Due` of `memory.md`; a commitment contract as `artifacts/contract-<habit>.md` with its `## Boxes` line; a recurring paid stake in `~/Clawic/data/finances/subscriptions.md`; and what worked or backfired in `## What Works` (`memory-template.md`).

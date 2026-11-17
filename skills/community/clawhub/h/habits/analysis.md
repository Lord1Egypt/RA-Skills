# Patterns and Honest Statistics

What can and cannot be concluded from one person's log. The data here is n=1 with a small denominator, which is exactly the shape that produces confident nonsense, and a wrong pattern gets designed around for months (Rule 8).

**Before stating any pattern**, read the last 8-12 weeks of `~/Clawic/data/habits/logs/` and `## Patterns` in `~/Clawic/data/habits/memory.md` — a pattern already recorded at two samples gets its count incremented, not rediscovered from scratch with a new wording.

**Contents:** [The Sample Floor](#the-sample-floor) · [What a Small Denominator Does](#what-a-small-denominator-does) · [Regression to the Mean](#regression-to-the-mean) · [Comparing Two Periods](#comparing-two-periods) · [Weekday, Time and Run-Length Effects](#weekday-time-and-run-length-effects) · [Correlations Between Habits](#correlations-between-habits) · [Outcome Checks](#outcome-checks) · [What Never Gets Said](#what-never-gets-said) · [When the Analysis Is the Problem](#when-the-analysis-is-the-problem)

## The Sample Floor

Recording a candidate pattern and saying it out loud are two different acts. Record it the first time it is noticed, with its count; say it at four samples (Rule 8).

| Claim | What counts as one sample | Minimum before it is said |
|---|---|---|
| "Misses cluster on `<weekday>`" | One occurrence of that weekday in the window | 4 occurrences, of which ≥3 are `n` |
| "It dies around week 3" | One complete attempt that ended | 4 attempts, ending within a 7-day span of each other |
| "Travel wrecks it" | One trip | 4 trips (`disruptions.md`) |
| "Evenings fail, mornings hold" | One habit with a known time of day | 4 habit-months, or two habits over two months |
| "The rate drops when `<other habit>` drops" | One day where both were scheduled | 8 days of each kind (below) |
| Anything else | State the count with the claim: "twice so far, not yet a pattern" | 4 |

A 28-day window contains exactly four of each weekday, which is why the window is 28 days (Rule 4) and why a weekday claim is the *smallest* claim the standard window can support. Everything slower than a weekday needs a longer read.

Two rules that keep the counts honest:

- **A design change resets the count** for every pattern downstream of it. Fridays missed under the old floor are not evidence about Fridays under the new one.
- **Absence of evidence is not a sample.** Blank cells count toward a pattern in neither direction (`tracking.md`).

## What a Small Denominator Does

One missed session is worth `1 ÷ scheduled_days` of the rate. That number, not the percentage, is what makes a movement readable.

| Frequency | Scheduled days in 28 | One miss costs |
|---|---|---|
| `daily` | 28 | 3.6 points |
| `weekdays` | 20 | 5.0 points |
| `4×/week` | 16 | 6.3 points |
| `3×/week` | 12 | 8.3 points |
| `weekly` | 4 | 25.0 points |

Consequences, all of them practical:

- **The smallest difference worth naming between two windows is two events**, i.e. `2 ÷ scheduled_days`. A one-event swing is inside the noise of every schedule; two is the smallest change that cannot be a single day.
- A `3×/week` habit that went from 92% to 83% lost **one session**. Say it in sessions before saying it in points.
- Never compare bands across frequencies without the denominators. 82% on a daily habit is 23 events; 82% on a weekly habit is between three and four.
- A `weekly` habit has no usable rate over 28 days — four data points. Report it as "3 of the last 4 weeks" and nothing else.

## Regression to the Mean

After an unusually bad week the next week improves on its own, and whatever change was made in between collects the credit. This is the most common false positive in the domain, and it is what makes a useless intervention look like the fix.

- **Never evaluate an intervention against the week that motivated it.** Compare the 14 days after the change against the habit's trailing 8-week average, not against the trough.
- A change made at a low point needs a **larger** movement to be believed than one made from a stable baseline — at least two events beyond the trailing average (above).
- The effect runs the other way after an exceptional week: a 100% week is followed by a normal one, and calling that a decline invents a problem.
- If two consecutive single changes produce no movement against the trailing average, the habit is not the problem (`troubleshooting.md`).

## Comparing Two Periods

| Comparison | Valid when | Trap |
|---|---|---|
| 28-day window vs the previous 28 days | Frequency and floor unchanged across both | Sliding the window by less than 28 days makes the pair overlap; compare non-overlapping windows only |
| Closed month vs closed month | Both months are complete | Months are 28-31 days; state the denominators, never the bare percentages (`review.md`) |
| Before vs after a change | ≥14 days on each side, exactly one variable changed | Regression to the mean (above) |
| This quarter vs last quarter | The habit existed for both | Survivorship: retired habits are the ones that were failing, so the surviving roster's average always rises |
| Against another person | Never | Demotivating when behind, licensing when ahead (`accountability.md`) |
| Against the same habit a year ago | Frequency, floor and definition are identical | A redefined floor makes the two numbers different measurements sharing a name |

## Weekday, Time and Run-Length Effects

- **Weekday.** Count `n` per weekday over 8 weeks. Working threshold: name a weekday when it has ≥4 occurrences and its miss rate is at least double the rate of the other days. Below that, the cluster is what four coin flips look like.
- **Time of day.** The grid does not store completion times, so any claim about mornings versus evenings is a guess unless the time was recorded. If it matters, put the time in the note column for two weeks first, then look (`tracking.md`).
- **Position in the week.** Front-loaded (strong Monday to Wednesday) and back-loaded shapes are read directly off the grid, not computed (`troubleshooting.md`).
- **Run lengths.** List where each run ended: 12, 16, 14, 13 days is a structure — something recurs on roughly a two-week cycle. 3, 41, 9, 22 is not. Four runs before the claim.
- **The day after a miss.** If the miss-after-a-miss rate is visibly above the baseline miss rate, the abstinence violation effect is running and the wording of the response is the intervention (`relapse.md`).

## Correlations Between Habits

The test: compare habit B's completion rate on the days habit A was done against the days it was not.

- Requires **at least 8 days of each kind**. A gap of 20 points or more is worth naming; less is noise (Rule 8).
- Positive gap → candidate keystone; the detection procedure and what protecting one means live in `routines.md`.
- Negative gap → the two are competing for the same slot, which is a design fault rather than a finding (`troubleshooting.md`).
- **State the confound out loud**: both habits are likelier on a good day, so most positive correlations between habits are correlations with the day. The claim that survives is the one where A happened on an ordinary day and B followed anyway.
- Never chain the inference into a cause. "Do A and B improves" needs the single-change protocol over 14 days, not a correlation.

## Outcome Checks

The habit is the behavior; the outcome is checked monthly at most and is never tracked as a habit (Rule 1). One check exists so that a user doing everything right and feeling nothing changed gets an answer instead of more compliance.

| Habit | Honest outcome measure | Cadence | Where the number lives |
|---|---|---|---|
| Training, walking, running | One body metric, one method, one time of day | Monthly | Shared `~/Clawic/data/health/` |
| Reading | Books or chapters finished | Quarterly | `~/Clawic/data/habits/<plural-noun>.md` |
| Quitting something paid | Clean days × daily spend, with the currency | Monthly | Roster note (`quitting.md`) |
| Study or practice | An actual test of the skill, never hours accumulated | Quarterly | `~/Clawic/data/habits/<plural-noun>.md` |
| Meditation, journaling | Nothing numeric. One sentence from the user | Quarterly | `## What Works` |

- **State the lag before the number.** Most outcomes move on a scale of months, so a flat month is the expected result rather than evidence the habit is failing.
- **One measure, one method.** A body metric taken on different scales at different times of day is noise with a decimal point.
- **If the outcome has not moved after two honest quarters at a good rate, the habit is the wrong lever.** That is a goal conversation — say it plainly and hand it to `goals`. Never fix it by making the outcome the habit.
- No daily outcome measurement, and none at all in month 1 (`starting.md`).

## What Never Gets Said

- **Decimals.** 82%, never 81.8%. The precision implies a measurement the log cannot support.
- **Causal language without the single-change protocol.** "Moving it to the morning fixed it" requires 14 days with one variable changed (`troubleshooting.md`); otherwise it is "the rate rose after the change".
- **An average across habits.** "Your overall consistency is 74%" hides one habit at 30% and one at 98%, which are two different conversations.
- **Population statistics as a personal claim.** Published base rates are group means; they justify a default, never a statement about this person's next week.
- **Projections.** "At this rate you hit 100 days on 14 October" converts a rate into a promise and manufactures the drop when it breaks.
- **A trend from three points.** Two points are a coincidence with a narrative attached (Rule 8); three are two coincidences.

## When the Analysis Is the Problem

Measurement has a cost, and past a small amount it substitutes for the behavior.

- Default output: **one number per habit per week** (`review.md`). Everything in this file happens on request, at the monthly rollup, or at the quarterly audit.
- Signals to stop: the user asks for a new view of the data more often than they complete the habit; requests for charts arrive during a low-rate stretch; backfilling and checking become the reported activity. The last one is in the Red Flags table of SKILL.md — measurement replacing the behavior means cutting to one habit and weekly logging.
- A dashboard is not a habit, and building one is the most enjoyable way to avoid the behavior it measures.
- Refuse a scoring system every time it is proposed. Points become the object, and the day the tally is not updated the habit goes with it (SKILL.md Traps).

**Whenever a pattern is observed or a claim is checked**, write it in the same turn: the row in `## Patterns` of `memory.md` with its sample count and first-seen date — recorded at one sample, said out loud at four; the outcome number in its box (`~/Clawic/data/health/` for body metrics, `~/Clawic/data/habits/<plural-noun>.md` for a series this skill owns); and the conclusion, if it changed anything, in `## What Works` (`memory-template.md`). A pattern that is not written is one whose count restarts at one next month.

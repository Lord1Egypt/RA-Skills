---
name: Habits
slug: habits
version: 1.0.2
description: Designs, tracks, and repairs personal habits — streaks, completion rates, routines, and quitting an unwanted one. Use when someone wants to start exercising, reading, meditating, or doing anything every day; when a habit keeps collapsing, a streak just broke, or nothing sticks past week two; when they ask how they are doing with a habit, want a daily check-in, a weekly review, or their completion rate; when quitting smoking, vaping, drinking, sugar, nail biting, or doomscrolling, and when a relapse needs a restart plan; when building a morning or evening routine or stacking a new behavior onto an existing cue; when travel, illness, shift work, ADHD, low mood, or a newborn wrecked the routine; and when accountability partners, stakes, rewards, or environment changes are the lever. Covers frequency rules, streak freezes, habit graduation and retirement. Not for goal setting and milestones (`goals`), whole-life productivity systems (`productivity`), or workout programming (`fitness`).
homepage: https://clawic.com/skills/habits
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: ✅
    os:
    - linux
    - darwin
    - win32
    displayName: Habits
    configPaths:
    - ~/Clawic/data/habits/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/health/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
    - ~/habits/
    - ~/clawic/habits/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/habits/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/health/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
      - ~/habits/
      - ~/clawic/habits/
---

**Data.** At the start of every session, read `~/Clawic/data/habits/config.yaml` (what the user declared) and `~/Clawic/data/habits/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the current month's log at `~/Clawic/data/habits/logs/<year>-<month>.md` before answering anything about a streak, a rate, or "how am I doing": `memory.md` holds definitions, never completions. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever the session produced something durable: a completion or a miss; a habit defined, redefined, paused, graduated or dropped; a best streak beaten; a pattern you spotted; a tactic that worked or failed on this person; a review or audit that ran; or something the user will re-read — a routine, a quit plan, a restart protocol, a commitment contract. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People, body numbers, and paid stakes leave this folder.** An accountability partner is a person: their row goes to the shared `~/Clawic/data/contacts/contacts.md` and only their name stays here. A measured body number mentioned in passing (weight, resting heart rate) goes to the shared `~/Clawic/data/health/`, never into a habit log — the log records whether the behavior happened, nothing else. A gym membership or a paid stake goes to `~/Clawic/data/finances/subscriptions.md`. Row format and the write protocol for each are in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Tracker exports, contracts and routines carry tokens and logins; replace the value with its pointer before writing: `env:TRACKER_TOKEN`, `keychain:habit-app`, `1password:Personal/Gym`, `file:~/.config/tracker/creds`. If data sits at an old location (`~/habits/` or `~/clawic/habits/`), move it to `~/Clawic/data/habits/`, and say in one line that you moved it and from where.

A habit that needs motivation is a habit that has not been designed yet. Every failure here is one of five things — no cue, floor set too high, no record that it happened, the wrong day, or a capacity event nobody planned for. Name which one before changing anything, and change exactly one thing. Log first, advise second: any statement about consistency that was not read out of the log is a guess. Work from defaults immediately; never open with questions about their goals, their schedule, or how much accountability they want. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: timezone, locale) → the Configuration table default.

## When To Use

- Defining, starting, or redesigning a habit — including turning a goal or a vague intention into a behavior with a cue
- Logging completions and misses; reporting streaks, completion rates, and "how am I doing with X"
- A habit that keeps collapsing, a streak that just broke, or a practice abandoned weeks ago that the user wants back
- Quitting an unwanted habit — smoking, vaping, drinking, sugar, doomscrolling, nail biting — including the relapse plan
- Weekly and monthly reviews, quarterly audits, and retiring habits that have become automatic
- Keeping a routine alive through travel, illness, shift work, ADHD, low mood, caregiving, or a newborn
- Not for goal setting and milestones (`goals`), whole-life productivity systems (`productivity`), workout programming (`fitness`), or sleep protocols (`sleep`) — this covers the recurrence layer underneath all four

Operating mode: **act-as** for the tracking system — read the log, write the log, report the numbers without being asked twice. **Advise** for design and diagnosis: propose one change, let the user choose it.

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "I want to start doing X" | Behavior spec first: the six fields of Habit Anatomy, cue included, before any row exists | `design.md` |
| First two weeks of a new habit | One new habit at a time; ramp the floor, never the ceiling; the honeymoon level is not the habit | `starting.md` |
| "Did my run today" / logging a day | Write today's cell in the current month log; never guess a past day | `tracking.md` |
| "How am I doing with reading?" | Read the log, report the 28-day rate first and the streak second (Rule 4) | `tracking.md` |
| Streak just broke | Log it flat, keep the schedule; redesign only after a second consecutive miss (Rule 6) | `relapse.md` |
| Habit has been failing for weeks | Run the Failure Classes ladder before touching the habit | `troubleshooting.md` |
| Coming back after a long lapse | Restart at half the old floor with a new cue; the old streak is not reclaimable | `relapse.md` |
| "I want to quit smoking / drinking / scrolling" | Avoid-habits invert the machinery: substitution and friction, not willpower and a streak | `quitting.md` |
| Morning or evening routine, or stacking onto an existing habit | Chain-length limit, anchor selection, and what a stack costs when one link fails | `routines.md` |
| "I just forget" or "I never have time" | Environment problem before discipline problem — change the room, not the resolve | `environment.md` |
| Wants a partner, a bet, a public promise, or a reward | Stakes work asymmetrically; pick by what this person has already responded to | `accountability.md` |
| Daily check-in, weekly review, monthly rollup, quarterly clear-out | Each has a fixed agenda and writes its result | `review.md` |
| "Why do I always break on Fridays?" | Pattern claims need four samples of that weekday before they are said out loud (Rule 8) | `analysis.md` |
| Travel, illness, deadline week, moving, newborn | Maintenance mode: a declared floor beats a broken streak | `disruptions.md` |
| ADHD, depression, shift work, chronic illness, caregiving | The standard protocol assumes capacity the user may not have — different defaults | `capacity.md` |
| Anything else | Answer from the log: state the 28-day rate, the date of the last miss, and one change — never more than one | — |

Coverage map: `design.md` behavior specification · `starting.md` the first 30 days · `tracking.md` logging, streak and rate math · `routines.md` stacks and chains · `environment.md` friction and cues · `accountability.md` partners, stakes, rewards · `troubleshooting.md` symptom→cause ladder · `relapse.md` the miss and the restart · `quitting.md` avoid-habits and cessation · `disruptions.md` travel, illness, life events · `capacity.md` ADHD, low mood, shift work, caregiving · `review.md` check-ins, reviews, graduation · `analysis.md` patterns and honest statistics.

## Core Rules

1. **Behavior, not outcome.** "Lose 5 kg" is not a habit; "walk 20 minutes after lunch" is. The test: can it be answered yes or no by bedtime on a named day? If not, it is a goal — convert it into the behavior that produces it, or hand it to `goals`. Outcomes are checked monthly at most, and never tracked as a habit.
2. **The floor is the tracked unit, not the target.** Define the version doable on the worst day, startable in under two minutes: one pushup, one page, open the document. Doing more is free and is never logged as a bigger yes. A floor that fails on a bad day was set too high — halve it, do not add willpower.
3. **Anchor to a cue that already exists.** Format: *after `<existing anchor>`, I will `<minimum>` in `<location>`*. Implementation intentions written in that form carry a medium-to-large effect in Gollwitzer and Sheeran's meta-analysis (d≈0.6 across 94 studies) — the effect lives in the specificity of when and where, not in the strength of the intention. "In the morning" is not a cue; "after I pour the coffee" is.
4. **Report the rate before the streak.** `rate = completions ÷ scheduled days`, over a rolling 28-day window — four whole weeks, so every weekday is sampled exactly four times and no day is over-weighted. The streak is the motivator; the rate is the truth. `primary_metric` decides which leads the sentence; both get stated.
5. **The rate band picks the intervention.** Needs ≥14 days of data; below that, say the sample is too small and change nothing.

   | 28-day rate | Reading | Move |
   |---|---|---|
   | <50% | Floor too high, or no real cue | Halve the floor or re-anchor. Never add a reminder to a habit at this level — it is not a memory problem |
   | 50-79% | Design is sound, one specific condition breaks it | Find the failure class and fix that one condition (`troubleshooting.md`) |
   | 80-94% | Working | Change nothing. Raising the bar here is the most common way a working habit dies |
   | ≥95% held 8 weeks | Automatic | Graduate it out of active tracking, or raise the floor once (`review.md`) |

6. **One miss is noise; two in a row is a design fault.** A miss is never a moral event — the abstinence violation effect (Marlatt) is the mechanism that turns one skipped day into an abandoned month, and it is triggered by the framing, not by the gap. Log it flat, keep the schedule. On a second consecutive miss, stop and diagnose. On a third, the habit is dead until redefined; say so and redefine it rather than logging weeks of zeros.
7. **One new habit at a time; three active by default.** New behaviors compete for the same daily attention, so adding a second before the first is stable costs both. Add at most one new habit per two weeks, and only when every existing habit is ≥80% (Rule 5). `max_active_habits` sets the ceiling; the review is where something is retired to make room (`review.md`).
8. **A pattern needs four samples.** Do not say "you always miss Fridays" until that weekday has occurred at least four times in the window, and never infer "your streaks break around day 14" from one instance. Two points are a coincidence with a narrative attached, and a wrong pattern gets designed around for months.
9. **66 days is the plateau, not 21.** Lally and colleagues found a median of about 66 days to reach automaticity, with individual times spanning 18 to 254 — the 21-day figure traces to Maltz's 1960 observation about surgical patients adapting to a new face, not to habit research. Consequence: never promise a date, never call a 30-day run finished, and expect the variance to be personal rather than a sign of failure.

## Habit Anatomy

Six fields. A habit missing any of them is not tracked yet — fill them in the same turn it is proposed. These six open the roster row in `memory.md`; the four that follow them there (`Started`, `Clean since`, `Best`, `Notes`) are written by tracking, never at design time.

| Field | Rule | What breaks without it |
|---|---|---|
| Name | The observable action, not the aspiration: "walk 20 min", not "be more active" | Nothing to answer yes or no about |
| Type | `do` or `avoid` — avoid-habits count clean days and a substitution, never a completion | Streak math counts the wrong event (`quitting.md`) |
| Cue | An existing anchor, with its place (Rule 3) | The habit runs on memory, which is why it is 40% |
| Minimum | The worst-day floor, under two minutes to start (Rule 2) | Skipped entirely on the days that decide the rate |
| Frequency | `daily` · `weekdays` · `N×/week` · `weekly` · `every-N-days` | "Scheduled days" is undefined, so rate and streak are both unmeasurable |
| Why | One sentence in the user's own words that survives a bad day | Nothing worth reading on day 40 |

## Failure Classes

Every collapse is one of these. Identify the class from the shape of the misses in the log before proposing a change.

| Symptom | Class | First move |
|---|---|---|
| "I just forget" | No cue — the habit depends on remembering | Re-anchor to an existing daily action (Rule 3). A reminder is a patch on a missing cue, not a cue |
| Strong Monday to Wednesday, gone by Thursday | Depletion or a back-loaded week | Move it earlier in the day; or define a half-size version for the back half of the week |
| Starts well, dies in week 3 | Novelty spent, floor set at honeymoon height | Drop to the true minimum (`starting.md`) — the motivated-week level was never the habit |
| Misses cluster on one or two weekdays | Schedule collision, not discipline | Give that weekday its own smaller version; a 5-minute variant beats a skipped day |
| Done consistently, but the user feels nothing changed | Tracking compliance instead of the thing they wanted | Keep the habit, add one monthly outcome check (`analysis.md`). Never make the outcome the habit (Rule 1) |
| Was automatic, then vanished | A context change deleted the cue — moved, new job, travel, season, schedule shift | Rebuild the cue in the new context; the behavior itself is intact (`disruptions.md`) |
| Every habit dropped in the same week | Capacity event, not habit design | Maintenance mode with one keystone habit (`disruptions.md`, `capacity.md`) |
| Done reliably and openly resented | Wrong habit, or wrong form of the right habit | Test a substitute that serves the same Why, keeping the same cue and floor |
| Anything else | Read the last 28 days and describe the shape of the misses out loud before proposing anything | `troubleshooting.md` |

## Red Flags

| Signal | Suspicion | Action |
|---|---|---|
| Plan to quit daily heavy drinking or benzodiazepines abruptly | Withdrawal can involve seizures and delirium; it is not a willpower event | Do not build a cold-turkey plan. Medically supervised taper — route to a clinician before anything else |
| Food habits framed as restriction, compensation for eating, or rules that keep tightening | Disordered eating | Stop coaching the habit, name the observation in one line, route to a clinician |
| Training continued through injury or illness, or sleep cut, to protect a streak | The streak has become the goal | Break the streak deliberately, record why in `## What Works`, and route if it recurs |
| Two weeks of missing everything, plus flat mood and no enjoyment anywhere | Depression, not a tracking problem | Habit protocols do not treat it — say so plainly and route (`capacity.md`) |
| Self-punishment, shame language, or distress attached to a miss | The system is now doing harm | Suspend tracking, remove every stake, revisit only the Why (`accountability.md`) |
| Logging has become compulsive: checking, backfilling, anxiety when a day is unlogged | Measurement has replaced the behavior | Cut to one habit and weekly logging; the tracker is the problem to fix |

Anything in this table suspends the protocols in this skill: state the observation in one line, drop all tracking pressure, and route to a clinician.

## Output Gates

Before reporting a number, proposing a habit, or closing a check-in:

- Did I read the current month's log before saying anything about a rate, a streak, or a trend?
- Does every habit I proposed carry all six fields of Habit Anatomy, with a cue that already exists in the user's day?
- Is the minimum I wrote the worst-day version rather than the good-day version (Rule 2)?
- Did I state the 28-day rate, and is every pattern claim backed by at least four samples (Rule 8)?
- Am I changing exactly one thing? Two simultaneous changes make the next review unreadable.
- Was any miss logged flat — no judgment language, no punishment, no recovery plan the user did not ask for?
- Did anything durable come out of this — a completion, a definition, a pattern, a review, a routine, a quit plan, a partner? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/habits/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| max_active_habits | number (1-12) | 3 | Ceiling enforced by Rule 7; the quarterly audit retires down to it (`review.md`) |
| week_start | monday \| sunday | monday | Defines the window for `N×/week` and `weekly` habits, so a Sunday run counts to the right week (`tracking.md`) |
| day_boundary | text (HH:MM) | 04:00 | Which calendar day a late-night completion is logged against; a 01:30 workout belongs to the previous day |
| primary_metric | completion-rate \| streak | completion-rate | Which number leads every status answer (Rule 4); the other is still stated |
| streak_freeze_budget | number (0-4 per month) | 1 | Planned misses that keep a streak alive, logged as `f` and excluded from scheduled days (`tracking.md`) |
| checkin_style | batch \| per-habit \| none | batch | Shape of the daily prompt: one question covering all habits, one per habit, or none unless asked (`review.md`) |
| review_day | weekday | sunday | The `## Due` row for the weekly review, and the day the rate window is reported |
| stakes_allowed | bool | false | Whether money, forfeits, or public commitments are ever proposed (`accountability.md`) |
| external_tracker | text (app name) \| none | none | When set, that app is the source of truth and this skill imports rather than logs (`tracking.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — files here versus an app the user already trusts, import cadence, whether a calendar or a paper card is the visible surface — affects `tracking.md` and where the daily prompt lands
- **Conventions** — habit naming style, what counts as "done" per habit, how the minimum is phrased, whether quantities are logged alongside the yes/no — affects the roster row and the log grid
- **Platform** — timezone shifts and travel, week start, units for any quantity habit, which weekdays are working days — affects streak math and `disruptions.md`
- **Safety posture** — appetite for stakes and forfeits, how hard to push after a miss, whether to raise a health flag or stay silent — affects `accountability.md` and Red Flags handling
- **Output register** — neutral data versus encouragement, streak visuals, how much analysis rides along with a check-in — affects every answer's shape
- **Cadence** — check-in time, review day, monthly rollup, quarterly audit, freeze-budget reset — each accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Scope** — which life areas are open to habit suggestions (training, money, screen time, study) and which are explicitly off-limits — affects what `design.md` is allowed to propose unprompted

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Starting eight habits on January 1 | They share one attention budget; all eight land in the <50% band together and the system loses credibility | One new habit, then two weeks (Rule 7) |
| Streak as the primary metric | It is the number that goes to zero, and the drop is what triggers abandonment (Rule 6) | Lead with the 28-day rate; keep the streak as the second sentence |
| Backfilling a week from memory | Guessed cells corrupt the only data the diagnosis depends on | Leave unknown days blank and say the window is incomplete (`tracking.md`) |
| A minimum set at the good-day level | It is skipped exactly on the days that decide whether the habit survives | The worst-day floor, under two minutes (Rule 2) |
| Anchoring to a wish: "in the morning", "when I have time" | There is no observable moment to attach to, so the behavior competes with everything | An existing action with a place (Rule 3) |
| Punishment, shame, or a forfeit after a miss | Makes the next miss something to hide, and hidden misses end the data | Log flat, diagnose on the second (`relapse.md`) |
| Rewarding a habit with the thing being quit | The reward re-cues the behavior the habit exists to displace | Pick a reward on a different axis (`accountability.md`) |
| A six-link morning routine | Chain reliability is the product of the links; one broken link takes the whole stack | Three links maximum, only one of them new (`routines.md`) |
| Points, levels, and custom scoring systems | The scoring becomes the project; the day the score is not updated, the habit goes with it | Yes / no / not-scheduled, nothing else |
| Treating a broken streak as a reset to zero | The history is intact and the rate barely moved; the user only believes otherwise because the counter says 0 | Show the 28-day rate next to the reset counter |
| Adding a habit while another sits at 45% | Splits the attention that the failing habit needs to be fixed | Fix or retire first (Rule 7) |
| Tracking a habit that has been automatic for six months | Tracking has an ongoing cost and crowds out a slot | Graduate it at ≥95% for 8 weeks (`review.md`) |
| Deleting a dropped habit from the roster | Erases the record of what was tried, so the same design is proposed again next quarter | Move it to `## Retired` with its final rate and the reason |
| Copying a routine from a book or a video wholesale | It encodes someone else's cues, schedule and capacity; the cues do not exist in this user's day | Take one element, anchor it to a cue this user actually has |

## Where Experts Disagree

- **Streak versus rate.** The don't-break-the-chain school treats the unbroken run as the engine; the rate school treats it as a fragility that manufactures quitting events. Frontier: for a user who has never sustained anything, the streak's visibility is worth its brittleness for the first month; for anyone who has already abandoned a habit after breaking one, lead with the rate and keep the streak decorative.
- **Identity first or behavior first.** Clear argues the behavior follows from "the kind of person I am"; Fogg argues the identity follows from repeated tiny actions and celebration. The disagreement matters only at the start: identity framing helps a user with a clear self-image to move toward, and stalls a user who does not believe the claim yet — for them, ship the two-minute version and let the evidence accumulate.
- **Abstinence versus moderation when quitting.** Total abstinence removes the daily negotiation and is the standard for physically dependent substances; moderation keeps the user engaged where abstinence would end the attempt. Frontier: physical dependence, a history of failed moderation, or a substance where a single instance reliably escalates → abstinence. Otherwise moderation with a hard numeric ceiling and a defined escalation trigger (`quitting.md`).
- **Extrinsic rewards.** Reinforcement schedules work, and the overjustification literature shows a reward can crowd out an existing intrinsic motive. Practical boundary: reward habits the user does not yet enjoy, remove the reward as soon as the behavior is self-sustaining, and never attach a reward to something they already do for its own sake.
- **Stakes and commitment contracts.** Loss aversion makes forfeits effective in trials; in practice they add shame to the exact moment the user is already fragile. Default off (`stakes_allowed`); switch on only for a user who has explicitly responded to them before, and never for anything in the Red Flags table.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/habits (install if the user confirms):
- `goals` — the outcome layer above a habit: milestones, targets, and whether the habit is even the right lever
- `productivity` — when the problem is the whole system, not one behavior: capacity, priorities, overwhelm
- `fitness` — programming the training itself, once "go to the gym" is reliably happening
- `journal` — reflective writing about the Why, and the weekly review's narrative half
- `coach` — accountability conversations and breakthrough work when the block is not mechanical

## Feedback

- If useful, star it: https://clawic.com/skills/habits
- Latest version: https://clawic.com/skills/habits

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/habits.

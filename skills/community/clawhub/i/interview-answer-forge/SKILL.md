---
name: interview-answer-forge
description: "Use when preparing for a job interview with a JD and your background — turns the STAR method from vague advice into a build system: mines your history for evidence, generates question-predictions from the JD, drafts STAR stories with a weak-spot flag on every answer, and pressure-tests with follow-up chains."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [interview, career, star-method, job-search, preparation]
---

# Interview Answer Forge

## Overview

"Use STAR" is the most given and least executed interview advice in existence. People are told to structure answers as Situation-Task-Action-Result but are left alone with a blank page — so they walk into interviews with three half-remembered anecdotes and improvise the rest under adrenaline.

This skill is a **build system, not a tip**. It works in four stages:

1. **Evidence mining** — inventory your actual history (jobs, projects, conflicts, numbers) into a reusable story bank. Ten stories cover ~90% of behavioral questions.
2. **Question prediction** — parse the JD into the 8-12 behavioral probes it implies. A JD stressing "fast-paced" predicts prioritization stories; "cross-functional" predicts influence-without-authority stories.
→ the exact prep gap.
3. **Story forging** — draft each story in STAR with word budgets (Situation 15%, Task 10%, Action 50%, Result 25%) and hard rules: numbers or it didn't happen, "I" not "we" in the Action.
4. **Pressure testing** — every story has expected follow-ups; every answer carries a **weak-spot flag** (where a sharp interviewer digs).

## When to Use

- You have an interview scheduled (or hoped for) and a JD in hand
- Phone screens, onsite loops, panel interviews, internal transfers, promotion boards
- "Tell me about a time..." panic — converting your history into a story bank
- Post-rejection re-prep: rebuild the bank, don't just re-read your old notes
- Mock-interview mode: the script plays interviewer with follow-up chains

Don't use for: technical knowledge screens (algorithms, certifications) — this is the behavioral/experience layer; case interviews (different structure); or academic tenure cases.

## The Method

### Stage 1 — Mine your history (the story bank)

Ten stories, one line each, covering this grid (2 stories per theme):

| Theme | Question family it answers |
|---|---|
| Conflict / difficult person | "Tell me about a conflict with a coworker" |
| Failure / mistake | "Tell me about a time you failed" |
| Leadership | "Led a team through..." |
| Ambiguity / no authority | "Influenced without authority", "prioritized under ambiguity" |
| Achievement with numbers | "Greatest accomplishment", role-fit questions |

Mining prompts that surface buried evidence (run `mine` subcommand):
- What did you build/fix/ship that outlived you?
- What did you refuse to do, and why? (refusals make the best integrity stories)
- Which number did you move? (time, money, risk, quality, count)
- Who did you convince of something they didn't want to hear?
- What did you take over that was on fire?
- What are you proudest of that never made a slide deck?
- What did you do that your manager never learned about?
- What mistake do you still think about?

Store in `story_bank.json` (the script manages it).

### Stage 2 — Predict questions from the JD

Read the JD as an interviewer would. Every phrase is a probe:

| JD phrase | Predicted behavioral probe |
|---|---|
| "fast-paced environment" | "Tell me about competing deadlines. How do you prioritize?" |
| "cross-functional" | "Tell me about influencing a team you don't manage" |
| "wears many hats" | "Describe a time you had to learn something fast with no help" |
| "detail-oriented" | "Tell me about catching an error others missed" |
| "startup mentality / scrappy" | "Resource-constrained win story" |
| "stakeholder management" | "Difficult stakeholder: how you turned them around" |
| "mentor junior" | "Mentoring story: someone you leveled up" |
| "data-driven" | "Decision where data overrode intuition" |
| "customer-obsessed" | "Angry customer save / voice-of-customer story" |
| "scale / growth" | "Something you built that broke at 10x — and the fix" |
| "process improvement" | "A process you killed or rebuilt" |
| "remote / async" | "Communication-failure-then-fix story" |

Also mandatory classics regardless of JD: failure, conflict, weakness, "why us", "tell me about yourself" (60-90 s, present→past→future arc), salary (deflect to research if asked early).

### Stage 3 — Forge stories with STAR + budgets

Every story gets:

```
S (15% | ≤30 words) — scene, stakes, constraint. Date/role anchor.
T (10% | ≤20 words) — YOUR task. Not the team's.
A (50% | ≤100 words) — 3-5 concrete steps, "I" voice. Skills named.
R (25% | ≤50 words) — number + timeframe + what it changed + lesson in one line.
```

Non-negotiable rules:
1. **Numbers or it didn't happen.** "Improved performance" is noise; "p95 latency 2.3 s → 410 ms" is an answer. No exact number? Banded: "roughly a third", "about 6 weeks".
2. **"I" not "we" in Action.** Interviewers discount team answers; they hire the "I".
3. **Result has a timeframe.** "Saved $40k/yr, verified next quarter" — otherwise it's a claim.
4. **End on what you'd repeat, not apology.** Failure stories close with the changed behavior, in the past tense: "Now I always...".
5. **One story, one skill.** A story trying to prove everything proves nothing.

### Stage 4 — Pressure-test (weak-spot flags)

Every drafted answer ships with:
- **2-3 expected follow-ups** ("What would you do differently?", "Why didn't you X first?", "How did [stakeholder] react?")
- **Weak-spot flag** — the honest hole: *unverified number*, *result was team's not yours*, *no negative consequence stated*, *action taken late*. Knowing your weak spot converts gotcha moments into prepared bridges ("honestly, the number is directional — the tracked metric was...").

## Using the Script

```bash
# Start/load your story bank
python3 interview_forge.py bank init
python3 interview_forge.py bank add                       # interactive: theme, one-liner, S/T/A/R, numbers

# Predict questions from a JD
python3 interview_forge.py predict jd.txt                 # -> probes + which bank stories cover them
python3 interview_forge.py predict jd.txt --show-gaps     # flag probes with NO story ready

# Score your STAR draft (budgets + rules)
python3 interview_forge.py score story.json

# Mock interview: chain of follow-ups per story
python3 interview_forge.py mock --theme failure
```

Bank persists at `~/.interview_bank.json`. `predict` matches probes to themes to your stories; gaps get mining prompts.

## Common Pitfalls

1. **Prepping answers instead of stories.** Questions change; stories transfer. Ten good stories answer fifty questions with re-framing; fifty memorized answers answer fifty questions and collapse on the fifty-first.
2. **Team results with no personal action.** "We grew revenue 40%" — interviewer's follow-up is "what did YOU do". Put the "I" in from the start.
3. **Failure story with no real failure.** "My weakness is I work too hard" reads as evasion. Pick a real mistake with a real cost — closable with what changed.
4. **Numbers claimed without banding.** If pressed you'll guess and look dishonest; band upfront ("~30%", "on the order of $50k").
5. **Situation hogging the answer.** 2 minutes of context, 20 seconds of action. The 15/10/50/25 budget exists because interviewers score the Action.
6. **Skipping "why us".** The most predictable question on earth and the most flubbed. Three sentences: what this role lets you do, what you bring, why now.
7. **No questions for them.** "What does success look like at day 90?" / "What did the last person in this seat struggle with?" — prepare three.
8. **Over-rehearsing to word-for-word.** Rehearse the SKELETON (first line + result line), not the script. Rote delivery reads as rote.

## Verification Checklist

- [ ] Story bank has ≥8 stories across the 5 themes (conflict/failure/leadership/ambiguity/achievement)
- [ ] Every JD-derived probe maps to a bank story or is flagged as a gap with a mining prompt
- [ ] Every story scored: STAR budget ratios within range, "I"-voice in Action, number in Result
- [ ] Every story has follow-up chains + an honest weak-spot flag
- [ ] "Tell me about yourself" (60-90 s) and "why us" drafted separately
- [ ] Three questions for the interviewer prepared
- [ ] Failure story ends with changed behavior, not apology

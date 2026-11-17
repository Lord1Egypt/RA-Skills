# Experiments — The Program, Not the Statistics

Running one test well is `ab-testing`. Running a *program* — a backlog that gets prioritised, tests that reach sample size, readouts that change decisions, and learnings nobody re-litigates — is this file. The failure mode is not bad statistics; it is a year of inconclusive tests.

**Contents:** [What Is Worth Testing](#what-is-worth-testing) · [The Hypothesis](#the-hypothesis) · [Prioritisation](#prioritisation) · [Sample Size Before You Ship](#sample-size-before-you-ship) · [Duration and Stopping](#duration-and-stopping) · [When Not to A/B Test](#when-not-to-ab-test) · [Reading a Result](#reading-a-result) · [The Readout](#the-readout) · [Program Health](#program-health) · [Traps](#traps)

**Before adding a test**, read `## Backlog` in `~/Clawic/data/growth/memory.md` and the current year's `experiments/<year>.md` if `## Boxes` lists it. Re-running a test that already read out — with the same design and the same power — is the most common waste in a mature program.

## What Is Worth Testing

Test where the constraint is (`diagnosis.md`) and where the outcome is genuinely uncertain. Two filters kill most ideas before they cost anything:

- **Would we act differently on either result?** If the answer is "we would ship it anyway", ship it and monitor. A test whose result changes nothing is a delay with a p-value.
- **Can this stage produce enough events?** A stage with 40 conversions a month cannot support an A/B test of a 10% effect (below). That is a qualitative or a sequenced-launch question.

Rank the *type* of change by expected effect size: the offer and the audience move numbers by multiples; the flow and the message by tens of percent; wording and layout by a few percent. Testing the last category on a low-traffic surface is how a quarter disappears.

## The Hypothesis

One sentence, pre-registered, with all five parts:

> **Because** [evidence from data or research], **we believe** [change] **for** [segment] **will cause** [primary metric] **to move by** [minimum effect], **measured over** [horizon].

- The **evidence** clause prevents idea-fountain backlogs: no observation, no test.
- The **minimum effect** is not a hope; it is the smallest change that would justify shipping, and it is what sizes the test.
- The **primary metric** is one metric. Secondary metrics are monitored, never promoted after the fact — testing many metrics and reporting the winner is how noise gets shipped.
- Add **guardrail metrics** that must not degrade: retention of the affected cohort, revenue per user, support volume, load time.

## Prioritisation

ICE (Impact, Confidence, Ease — Sean Ellis) is the fast default: score each 1-10, rank by the product or the mean, and re-score nothing. RICE (Reach × Impact × Confidence ÷ Effort — Intercom) is better once reach differs wildly between surfaces, because ICE hides that a 10-Impact idea touches 2% of users.

Practical rules that matter more than the formula:

- **Score Impact in the currency of the constraint**, using the absolute-lift formula (SKILL.md Rule 1), not on a feeling.
- **Confidence is evidence-based**: prior test results and observed data score high; "the CEO likes it" scores low, and writing that down is the point of the exercise.
- **The scores are a sorting device, not a decision.** They exist to make the argument explicit and fast, and their precision is fake — do not defend a 7.2 against a 7.0.
- Cap the live program at what your traffic can power: concurrent tests on the same surface interact, and split traffic reaches significance later or never.

## Sample Size Before You Ship

Approximate required sample **per variant** for a two-arm test of a rate, at 80% power and 95% confidence (Lehr's rule, the standard approximation):

```
n_per_arm ≈ 16 × p × (1 − p) ÷ (p_treatment − p_control)²
```

Worked: baseline conversion 5%, minimum detectable effect +10% relative (5.0% → 5.5%, so Δ = 0.005):

```
n = 16 × 0.05 × 0.95 ÷ 0.005²  =  0.76 ÷ 0.000025  =  30,400 per arm
```

60,800 users total. If the surface sees 8,000 users a week, that is nearly 8 weeks — decide *before* shipping whether the answer is worth two months, or whether to test a bigger change instead. Notes that keep this honest:

- Smaller baselines and smaller effects both explode the number: halving the detectable effect **quadruples** the sample.
- At `experiment_confidence` = 99, the constant rises (roughly 16 → 24); at 90 it falls (roughly 16 → 11). Use the configured value.
- For revenue per user rather than a rate, variance is dominated by a few large orders; the same formula with a measured standard deviation, and consider capping outliers by a pre-declared rule.
- If the required n exceeds what the surface can deliver in a reasonable window, the options are: test a larger change, move to a higher-traffic surface, accept lower confidence explicitly, or do not test.

## Duration and Stopping

- **Minimum one full business cycle (7 days), normally two.** Weekday and weekend users behave differently; a test run Tuesday to Friday measures a population that does not exist.
- **Never stop on significance if the horizon was fixed.** Peeking at a fixed-horizon test and stopping on a green result inflates false positives far above the nominal rate. Either commit to the horizon or use a sequential/always-valid method designed for continuous monitoring (SKILL.md Rule 7).
- **Novelty and primacy effects**: a change can win in week one because it is new and lose in week three. Where the horizon allows, compare the last week to the first.
- **Do not extend a test because it is close.** Extending on a peek is peeking with extra steps; extend only per a rule written before launch.
- **Stop early only for harm**: a guardrail breach or a bug is always a valid stop.

## When Not to A/B Test

| Situation | Why testing fails | Instead |
|---|---|---|
| Traffic too low for the effect | Underpowered; an inconclusive result reads as "no effect" | Sequenced launch with before/after and a control period; or qualitative research |
| Strategic bet (pricing model, repositioning) | Cannot be split cleanly; the effect is long-term | Cohort comparison over time, or a market/geo split (`monetization.md`) |
| Change is obviously right | Cost of testing exceeds the value of knowing | Ship it, monitor guardrails |
| Cross-user interference (marketplace, social) | Treatment leaks between arms and biases both | Switchback or cluster-randomised design by market or time (`marketplaces.md`) |
| Long conversion cycle | Result arrives after the decision must be made | Leading indicator agreed in advance, plus a later confirmation |
| Legally or ethically sensitive (visible price differences, consent) | Detectable and damaging | Cohort test, or do not run it |

## Reading a Result

- **Segment the result, but do not go shopping.** Segments to check are pre-declared (source, plan, platform, new vs existing). A win found only in an unplanned segment is a hypothesis for the next test, not a finding.
- **Check the guardrails** before celebrating: activation up, retention down is a loss dressed as a win.
- **Sample ratio mismatch** — the arms received materially unequal traffic — invalidates the test outright, whatever the p-value. Check it every time; it is the most common silent bug.
- **A flat result is information.** It bounds the effect: "this class of change is worth less than X% here" redirects the next quarter.
- **Effect sizes shrink on rollout.** The tested variant ran against a specific mix at a specific time; expect regression toward the mean and re-measure after full rollout.

## The Readout

Six lines in `experiments/<year>.md`, written the day it ends. The design line carries the sizing arithmetic so the next reader can check it instead of trusting it:

```
2026-06-08 → 2026-07-13 | onboarding: seed sample project for new signups
Hypothesis: because 61% of churned users never created a project, seeding one
            will raise 7-day activation from 22% to ≥26%.
Design: 50/50, new signups only, primary = activated_7d, fixed horizon.
        n = 16 × 0.22 × 0.78 ÷ 0.04² = 1,716 → 1,800/arm; at ~124 signups/day
        that is 29 days of intake plus 7 for the last cohort's window to close.
Result: 22.1% → 25.4% (+3.3pp, +15% rel). Guardrails: M1 retention flat, support flat.
Decision: ship to 100%. Next: test seeding by use case (backlog).
```

Kept because losses are the reusable asset: they are what stops the same idea returning every two quarters with a new sponsor.

## Program Health

| Metric | Meaning | Watch for |
|---|---|---|
| Velocity: tests started per month | Throughput of learning | High velocity with low power = manufactured noise |
| Power rate: share of tests that reached planned n | Whether the program can conclude anything | Below half means the surfaces are too small for the method |
| Win rate | Share of tests with a positive shipped result | A win rate near 100% means only safe ideas are being tested, or results are being read generously |
| Time to decision | Test end to shipped or shelved | Results that sit unshipped are the cheapest lost value in the program |
| Backlog age | How long ideas wait | An old backlog is evidence the scoring is not being used |

A modest, honest win rate is normal and healthy in mature programs; a team reporting that nearly everything wins is measuring itself, not the world.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Peeking and stopping on green | Inflates false positives well past 5% | Fixed horizon, or a sequential method |
| No sample-size calculation before shipping | Discovers after three weeks that the test could never conclude | Lehr's rule, before the ticket is written |
| Multiple primary metrics | One of them will move by chance | One primary, guardrails declared |
| Testing button colours on the constrained stage | Effect size far below what the traffic can detect | Test the offer, the audience, or the flow |
| Concurrent tests on one surface | Interaction effects and split traffic | Sequence by score, one owner per surface |
| Shipping a segment-only win found after the fact | Post-hoc segmentation finds a "win" in noise | Pre-declared segments; new finding = new test |
| Ignoring sample ratio mismatch | The test is broken, not the hypothesis | Check SRM on every readout |
| No record of losses | The idea returns every two quarters | `experiments/<year>.md`, permanently |

**Every test writes twice**: the idea, its hypothesis and its score into `## Backlog` in `~/Clawic/data/growth/memory.md` when it enters (past ~15 open ideas, move the backlog to `backlog.md` with the same headings and add its `## Boxes` line), and the full readout into `~/Clawic/data/growth/experiments/<year>.md` on the day it ends — that file is append-only and cut by year, never a section of `memory.md` (`memory-template.md`). A result that changes strategy also updates the stage rate in `## Funnel` and, if it is worth re-reading whole, becomes an `artifacts/<kebab-name>.md` with its `## Boxes` line in the same turn.

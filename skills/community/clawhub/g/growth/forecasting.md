# Forecasting — Models, Targets, and What a Plan Implies

A growth forecast is a model of the machine, not a line extended to the right. Its job is to make the plan falsifiable before the quarter starts: which inputs must move, by how much, and what happens if one of them does not.

**Contents:** [Bottom-Up, Never Top-Down](#bottom-up-never-top-down) · [The Model Skeleton](#the-model-skeleton) · [Cohort Revenue Build](#cohort-revenue-build) · [Sensitivity and Scenarios](#sensitivity-and-scenarios) · [Setting a Target](#setting-a-target) · [Budget Allocation](#budget-allocation) · [Cash, Not Just Payback](#cash-not-just-payback) · [Tracking Against the Model](#tracking-against-the-model) · [Traps](#traps)

**Before building any model**, read `## Funnel`, `## Channels`, `## Retention` and `## Targets` in `~/Clawic/data/growth/memory.md` (or the files `## Boxes` points to) and `~/Clawic/data/finances/budget.md`. A forecast built on remembered numbers is a wish; every input must carry its as-of date.

## Bottom-Up, Never Top-Down

Top-down ("we will grow 3× because the market is large") produces a number nobody can act on. Bottom-up starts from the inputs the team controls:

```
new customers = Σ over channels [ spend ÷ CAC ]  +  organic base × growth rate  +  loop output
revenue       = existing MRR × (1 − churn + expansion)  +  new customers × ARPA
```

Every term is measurable, so every miss is attributable. Build the model at the granularity you actually manage: per channel for acquisition, per cohort for revenue, per month for both. A model with more granularity than your data supports is false precision that will be defended in meetings.

## The Model Skeleton

Twelve to eighteen rows, one column per month:

| Block | Rows |
|---|---|
| Inputs | Spend per channel · CAC per channel · organic sessions · conversion rate per stage · ARPA · gross margin · monthly logo churn · expansion rate |
| Acquisition | New customers per channel, summed |
| Base | Opening customers · new · churned · closing |
| Revenue | Opening MRR · new MRR · expansion · contraction · churned MRR · closing MRR |
| Efficiency | Blended CAC · paid CAC · payback months · CAC ÷ new MRR |
| Cash | Gross profit · paid spend · net cash from growth |

Discipline: **inputs in one block, everything else computed.** Any cell that is both an assumption and a result is where the model will lie to you. Mark every input with its source and as-of date — "CAC 142 USD, paid channels, 2026-06" — and the ones that are guesses as guesses.

## Cohort Revenue Build

Subscription revenue is the sum of surviving cohorts, and modelling it any other way hides the compounding:

```
month_revenue = Σ over cohorts [ cohort_size × ARPA × survival(age) × (1 + expansion)^age ]
```

- `survival(age)` comes from the observed retention curve (`retention.md`), not from a single churn rate. A flat "3% monthly churn" applied to a curve that decays fast then flattens overstates early revenue and understates late revenue.
- Model **new cohorts at the retention of recent cohorts**, not at the all-time average, and say which cohort's curve you used.
- Where the curve has not matured, extrapolate conservatively and mark the extrapolated periods. Assuming the tail flattens where you have no data is the most common way a model produces a number that never arrives.
- Cap LTV horizons at 24-36 months for planning (SKILL.md Numbers That Lie).

## Sensitivity and Scenarios

Never present a single line.

- **One-way sensitivity**: vary each input ±20% and rank by effect on the output. The top two inputs are the ones the quarter is actually about; publish them as the plan's dependencies.
- **Three scenarios**, each internally consistent: base (current rates hold), downside (CAC +30% and conversion −10%, which co-occur because both follow traffic quality), upside (one specific thing works, named). Random ±20% on the headline number is not a scenario.
- **Break-even question**: what is the worst value of the top input at which the plan still works? That number is the trigger for a mid-quarter re-plan, and it should be written into `## Targets` at the same time as the forecast.
- CAC is never constant across spend levels: the model must apply a rising CAC curve as spend grows, or it will forecast infinite scale (`paid.md`).

## Setting a Target

A target is a commitment; a forecast is a belief. Keep them distinct and state both.

- Derive the target from the model, then check it against the **binding constraint**: the target implies X new customers, which implies Y spend at current CAC, which implies Z cash — if any link fails, the target is a wish (`diagnosis.md`).
- **Set targets on inputs the team controls**, and report outcomes alongside. "Raise activation from 22% to 28%" is a target; "grow 40%" is an outcome that depends on things nobody in the room can move.
- One target per constraint per quarter. A team with five targets has none.
- Write the **falsifier**: the mid-quarter observation that would prove the plan wrong early. Without it, the quarter is defended until the last week.

## Budget Allocation

```
allocation = maintain the scaling channel at the spend where payback still clears target
           + test budget for 2-3 candidates at min_test_spend each (`acquisition.md`)
           + reserve (~10-20%) for the winner to absorb mid-quarter
```

- Fund the **reserve deliberately**. A quarter with the whole budget committed cannot double down on the one thing that worked, which is the whole point of running tests.
- Allocate by **marginal** return, not average: move the next increment of spend to wherever marginal CAC is lowest, not to whichever channel has the best lifetime average (`paid.md`).
- Include **fully loaded costs** for labour-based channels; a content plan without headcount is not a budget.
- Recheck allocation at the `reporting_cadence`. Monthly re-allocation with a stop-loss beats an annual plan defended out of pride.

## Cash, Not Just Payback

A payback of 9 months is affordable only if you can fund 9 months of it. The constraint that kills growth plans is cash timing, not unit economics.

```
cash_needed_for_growth ≈ monthly_new_customers × CAC × payback_months × 0.5   (rough, for steady-state ramp)
months_of_runway       = cash ÷ (fixed_costs + growth_spend − gross_profit)
```

- Annual prepayment shortens the effective payback dramatically and is often worth a two-month discount for exactly that reason (`monetization.md`).
- If the plan requires more cash than exists, the answer is a smaller plan or a financing decision — state which; a growth plan that assumes unavailable capital is a fiction with a chart.
- Growing faster consumes more cash in every business whose payback is longer than its billing cycle. That is arithmetic, not a failure.

## Tracking Against the Model

- Report **actual versus model per input**, not just the headline. The headline being on plan while two inputs are off in opposite directions is a coincidence that will not repeat.
- Re-forecast at the `reporting_cadence`; keep the original in place, so the drift is visible. A model quietly rewritten each month cannot be wrong and teaches nothing.
- When an input misses by more than ~20%, name whether the input was wrong or the world changed — the fix is different (`plateaus.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Top-down "we will grow 3×" | No input to act on, no way to be wrong until it is too late | Bottom-up from channel and cohort inputs |
| Constant CAC at every spend level | Forecasts infinite scale from a small test | Rising CAC curve; the 2× test (`acquisition.md`) |
| Single churn rate instead of a curve | Overstates early revenue, understates the flat tail | Survival from the observed cohort curve |
| One line, no scenarios | Nobody knows which assumption to watch | Three consistent scenarios and a one-way sensitivity |
| Model rewritten every month | Cannot be wrong, therefore teaches nothing | Keep the original; track drift per input |
| Targets on outcomes only | Team cannot move them; accountability collapses into blame | Input targets, outcomes reported |
| Ignoring cash timing | Profitable growth that runs out of money | Runway and cash-need calculation next to payback |
| Forecast built on remembered numbers | Every input is quietly out of date | Every input carries its source and as-of date |

**After building or revising a model**, write it back in the same turn: the target, its falsifier, the break-even value of the top input, and the re-plan trigger into `## Targets` in `~/Clawic/data/growth/memory.md` with its as-of date; the model itself — inputs with sources, structure, scenarios, and what it assumed — into `~/Clawic/data/growth/artifacts/growth-model-<yyyy-qn>.md`, born as its own file with its `## Boxes` line (`memory-template.md`). Committed spend goes to the shared `~/Clawic/data/finances/budget.md` with currency and period; if the plan is a bounded initiative with an owner, it is also a `~/Clawic/data/projects/<project>.md`. Keep superseded models: the gap between what was forecast and what happened is the only calibration data you will ever have.

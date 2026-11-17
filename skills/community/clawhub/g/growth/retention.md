# Retention — The Curve That Decides Everything Upstream

Retention is not a percentage, it is a curve, and its **shape** answers a different question than its height. A flat curve at 20% is a business; a sliding curve from 60% is a countdown. Everything in acquisition is leverage on this shape.

**Contents:** [Reading the Curve](#reading-the-curve) · [Natural Frequency](#natural-frequency) · [Building the Cohort Table](#building-the-cohort-table) · [The Power User Curve](#the-power-user-curve) · [Where Churn Actually Comes From](#where-churn-actually-comes-from) · [Resurrection](#resurrection) · [Retention Levers by Position on the Curve](#retention-levers-by-position-on-the-curve) · [B2B Retention Is a Different Object](#b2b-retention-is-a-different-object) · [Traps](#traps)

**Before any retention claim**, read `## Retention` in `~/Clawic/data/growth/memory.md` — or `retention-curves.md` if `## Boxes` points there — plus `## Metric Definitions` for the active-user definition in force. A single cohort is an anecdote; the comparison to the previous ones is the finding.

## Reading the Curve

Plot % of a cohort performing the value action in period N, by periods since first touch. Three shapes, three verdicts:

| Shape | Verdict | What to do |
|---|---|---|
| Declines and **flattens** at a positive asymptote | Product has a habitual core | Widen the core: who is in the flat part, and how do you acquire more of them |
| Declines **to zero** | No habit exists at this frequency; this is pre-PMF | Product work, not growth work (SKILL.md Stage Gates) |
| Declines then **rises** ("smile") | Users return for a periodic need, or expansion within accounts | Frequency is longer than your window; measure at the real cycle |

Two disciplines make the plot trustworthy: hold the **denominator fixed at cohort size** (never at users still active), and use **unbounded windows** — "active in week 4" not "active in weeks 1-4" — because bounded windows manufacture flattening.

The number that matters is the **asymptote and the period it is reached**, e.g. "flattens at 34% by week 6". Quote it that way; a single "M3 retention is 41%" hides whether it is heading to 38% or to 4%.

## Natural Frequency

Retention is only meaningful against the frequency the job is done. Measuring a tax product weekly produces a curve to zero and a wrong strategy.

- Derive it: median gap between value actions among users who performed it at least three times. That distribution, not an assumption, sets the reporting period.
- Frequency bands and their reporting period: daily jobs → DAU and D1/D7/D30; weekly jobs → WAU and W1-W8; monthly jobs → MAU and M1-M12; seasonal or event-driven → annual with resurrection as the primary metric.
- DAU/MAU is a **frequency** ratio, not a quality score: it approximates days used per month ÷ 30. Comparing it across products with different jobs is meaningless (SKILL.md Numbers That Lie).
- A product can raise frequency by changing the job it does, but that is a product strategy decision, not a retention tactic — and the new curve starts over.

## Building the Cohort Table

One table, two views, both stored:

```
Cohort   Size   P1    P2    P3    P4    P6    P8    P12
2026-01  1,240  52%   41%   37%   35%   34%   34%   33%
2026-02  1,610  55%   44%   39%   37%   36%   35%    —
2026-03  1,880  49%   36%   30%   27%   25%    —     —   ← investigate
```

- Read **down the columns** to see whether the product is improving; read **across the rows** to see the shape. Down-column comparison at the same period is the only fair one.
- A cohort that breaks the pattern points at what changed *upstream*: a new channel with worse intent, a pricing change, a promotion that bought the wrong users (`acquisition.md`).
- Weight by revenue as well as by users if plans differ materially — losing 30% of users who are 5% of revenue is a different problem from the reverse.
- Store cohorts by first touch, forever (SKILL.md Rule 3).

## The Power User Curve

An average hides the distribution. Histogram users by days (or weeks) active in the last 28 periods:

- **Smile shape** — a mass at 1-2 days and a mass at 25-28 — is healthy: a real core exists. Work on moving the middle right and on acquiring more people who look like the right tail.
- **Slide to the left**, mass at 1-2 and nothing else, means no core: no amount of acquisition fixes it.
- Track the **share of the value action** produced by the right tail. When a small group produces most of the value, your growth model is "find more of them", and your churn risk is concentrated in a handful of accounts.

## Where Churn Actually Comes From

Diagnose by position and cause before choosing a tactic:

| Bucket | Signal | Owner |
|---|---|---|
| Never activated | Churn inside period 1, never reached the aha action | Activation, not retention (`activation.md`) |
| Wrong-fit acquisition | Churn concentrated in one source or campaign | Channel quality (`acquisition.md`) |
| Value delivered, need ended | Long tenure, clean exit, no complaints | Expected — measure it and stop calling it a failure |
| Habit never formed | Activated, used it twice, faded | Triggers and frequency (`lifecycle.md`) |
| Involuntary — failed payment | Card expiry, insufficient funds, hard declines | Dunning; recoverable with retries and pre-expiry notices (`monetization.md`) |
| Competitive or price | Cancellation reason and win-back response | Packaging, or accept the loss (`monetization.md`) |

Involuntary churn is the cheapest to fix and the most often ignored: it is a billing configuration, not a product problem, and the recovered revenue arrives within weeks rather than quarters.

## Resurrection

Resurrected users are cheaper than new ones and are already in your database. They are also the term that makes growth accounting balance (`diagnosis.md`).

- Define dormancy against the natural frequency: dormant = no value action for ~3× the median gap. Fixed dormancy periods copied from other products misclassify half the base.
- The trigger that works is a **change in their world**, not a discount: the missing feature shipped, the integration they wanted exists, the price now fits, someone on their team came back.
- Measure resurrection as a rate over the dormant pool, and measure whether resurrected users retain — a resurrection stream that churns again in one period is a metric, not a business (`lifecycle.md` for the mechanics).

## Retention Levers by Position on the Curve

| Position | Lever | Mechanism |
|---|---|---|
| Period 0-1 (steepest drop) | Activation and first-value speed | Most of the curve's total loss happens here; the cheapest lift is always earliest (`activation.md`) |
| Early middle | Triggered return reasons | Notifications tied to *someone else's* action or to state change, not to your calendar |
| Middle | Habit anchoring | Tie usage to an existing routine or an external cadence (payroll, sprint, weekly review) |
| Flat part | Depth and switching cost | Data accumulated, teammates present, integrations connected — each raises the cost of leaving honestly |
| Anywhere | Removing surprise | Failed payments, breaking changes, silent limits: the churn nobody chose |

Switching cost earned by accumulated value is legitimate; switching cost created by making export hard is a cancellation-flow dark pattern that produces chargebacks and public complaints — and in several jurisdictions, regulatory exposure.

## B2B Retention Is a Different Object

Logo retention, seat retention, and revenue retention move independently: an account can shrink from 50 seats to 5 and still count as retained. Track all three, and net revenue retention separately from gross — NRR above 100% means expansion outruns churn and the business grows without new logos. Canonical definitions live in `saas-metrics`; the account-level mechanics (champion turnover, renewal cycles, usage-based expansion) live in `b2b.md`.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| One retention number instead of a curve | Cannot tell flattening from sliding | Curve with its asymptote and the period it reaches it |
| Bounded windows ("active in weeks 1-4") | Manufactures a flat curve out of any data | Unbounded period-N windows |
| Denominator = users still active | Every cohort retains 100% forever | Denominator fixed at cohort size |
| Measuring at the wrong frequency | Weekly measurement of a monthly job shows collapse | Derive natural frequency first |
| Averaging cohorts together | Mixes the good months with the bad and hides the trend | Compare down the column at the same period |
| Treating all churn as preventable | Wastes effort on users whose need genuinely ended | Bucket by cause first |
| Retention campaign before the curve flattens for anyone | Nothing to retain people to | Product work; segment for whoever does retain (`diagnosis.md`) |

**After any cohort refresh, curve reading, or churn-cause analysis**, write it back in the same turn: the cohort row (cohort, size, period rates, as-of date) into `## Retention` in `~/Clawic/data/growth/memory.md`, the natural frequency and the active-user definition into `## Metric Definitions`, and any churn cause you established into `## Pain Points`. Past ~15 cohorts the table moves to `retention-curves.md` with its `## Boxes` line, keeping the same headings (`memory-template.md`). A churn post-mortem worth re-reading is `artifacts/<kebab-name>.md`, not a paragraph in memory.

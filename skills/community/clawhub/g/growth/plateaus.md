# Plateaus — Stalls, Saturation, Decay, and Fake Crises

Growth flattening is a symptom with six common causes, and the tactics that fix one make the others worse. This file separates them before anyone reorganises a team.

**Contents:** [Rule Out the Fake Crisis First](#rule-out-the-fake-crisis-first) · [The Six Causes](#the-six-causes) · [Saturation Math](#saturation-math) · [Decay](#decay) · [Mix Shift](#mix-shift) · [The Law of Shitty Clickthroughs](#the-law-of-shitty-clickthroughs) · [S-Curves and the Next One](#s-curves-and-the-next-one) · [The Stall Review](#the-stall-review) · [Traps](#traps)

**Before diagnosing a stall**, read `## Funnel`, `## Channels`, `## Retention` and `## Pain Points` in `~/Clawic/data/growth/memory.md` (or the files `## Boxes` points to). Two-thirds of stall reviews end at "this happened last year too" — and the only reason anyone knows is that someone wrote it down.

## Rule Out the Fake Crisis First

Cheapest checks, in order. Each has caused a real reorganisation somewhere.

| Check | How | If yes |
|---|---|---|
| Measurement broke | Volume anomaly on a single event, null-rate jump, a redirect or consent banner change | Data problem (`instrumentation.md`), not growth |
| Seasonality | Year-over-year for the same week, not month-over-month | The business always dips here; state the YoY number and stop the meeting |
| Comparison window | Month-to-date against a closed month, or a month with fewer working days | Compare like windows |
| Mix shift | Same rates within each segment, different segment weights | Not a rate problem (below) |
| One-off in the base period | A launch, a PR spike, a big customer, a promotion | The base was the anomaly, not now |
| Definition change | Someone edited a metric, a filter, or an exclusion | Restate history under one definition |

Only after all six is the flattening real.

## The Six Causes

| Cause | Signature | Wrong reflex | Right move |
|---|---|---|---|
| Channel saturation | Spend rising, marginal CAC rising, impressions of the same audience repeating | Bid harder | New audience, geography, or channel (`acquisition.md`) |
| Content/creative decay | Volume flat while unit count grows; CTR falling at stable frequency | Publish or produce more of the same | Refresh existing units; new concepts, not variants (`paid.md`, `loops.md`) |
| Retention ceiling | Acquisition steady, base flat: new users equal churned users | Buy more users | Retention work — the base is a bucket with a hole (`retention.md`) |
| Market saturation in the segment | Penetration high among the ICP; deals slow; win rate falls to substitutes | Discount | New segment, new geography, or a new job to be done |
| Loop broke | k or content-per-user falling while acquisition holds | Add a campaign | Find the broken arrow in the loop (`loops.md`) |
| Constraint moved | The stage you were working is no longer the binding one | Keep optimising the old one | Re-run the diagnosis (`diagnosis.md`) |

The base-flat case deserves its own arithmetic: when `new customers ≈ churned customers`, growth is exactly zero regardless of how well acquisition performs. `steady_state_base = monthly_new ÷ monthly_churn_rate` — at 500 new/month and 5% churn, the base converges to 10,000 customers and stops, whatever the marketing spend. Halving churn doubles the ceiling; doubling acquisition also doubles it but costs a great deal more.

## Saturation Math

A channel saturates when the efficient audience is exhausted, and it shows up in marginal numbers long before average ones:

```
marginal_CAC = Δspend ÷ Δcustomers        (between two consecutive periods)
```

Worked: 20k → 26k spend, 160 → 185 customers. Marginal CAC = 6,000 ÷ 25 = 240 USD against an average of 140 USD. If target CAC is 180, the last increment lost money while the account still reported a healthy average. Track marginal CAC every period at every spend change; it is the earliest reliable saturation signal.

Corroborating signals: frequency rising at constant audience size, reach plateauing while impressions grow, and the same creative winning for longer than usual (a sign the audience pool is stable and small, not that the creative got better).

## Decay

Everything acquired decays; the question is only the rate.

- **Content**: traffic per unit falls after publication. Measure your own decay by tracking cohorts of content by publication month — the curve is stable enough per site to forecast with, and it is never the number in someone's blog post.
- **Creative**: performance falls with cumulative exposure to the same audience, so decay is a function of frequency, not of calendar time. A creative running against a large audience lasts far longer than the same creative against a small one.
- **Backlinks and rankings**: positions erode as competitors publish; a page unrefreshed for a year is usually losing.
- **Steady state**: `production_rate × average_useful_life = steady_state_stock`. Growth requires production to exceed replacement. A team publishing 10 units a month with a 12-month useful life converges at 120 productive units and stops — that is not a stall, it is the design of the machine (`loops.md`).

## Mix Shift

Simpson's paradox in production: every segment can improve while the aggregate falls, because the weights changed.

Diagnose by decomposing the change:

```
Δrate = Σ [ segment_weight × Δsegment_rate ]  +  Σ [ Δsegment_weight × segment_rate ]
                    ↑ performance effect               ↑ mix effect
```

If the second term dominates, nothing got worse — you acquired more of a segment that always converted lower. The decision is whether that segment is worth acquiring, which is a channel-quality question (`acquisition.md`), not a conversion-optimisation one.

## The Law of Shitty Clickthroughs

Every new channel's response rate declines over time as it is adopted, because the audience learns to ignore the format (Andrew Chen's formulation). Consequences that survive the aphorism:

- **Early access to a channel is a temporary asset.** Returns are highest before the format is common and decline as competitors arrive.
- **Budget a permanent share of effort to finding the next channel**, even while the current one works. The team that starts looking after the plateau starts a 3-9 month clock at the worst moment.
- **Channel returns falling is normal, not incompetence.** The mistake is expecting a channel's first-year efficiency to persist and building a plan on it.

## S-Curves and the Next One

Growth is a series of S-curves, not one exponential. Each curve is a segment × channel × product-capability combination, and each one flattens.

- The next curve comes from a **new segment** (a different buyer with a different job), a **new channel** (distribution the competitor set has not taken), a **new product surface** (a second product for the same customer), or a **new geography**.
- Start the next curve while the current one still funds it. The signal to start is not the plateau — it is the deceleration that precedes it: three consecutive periods of falling growth *rate* at constant spend.
- Ranked by odds: new geography with the same product and channel is the cheapest, new segment is next, new channel is next, new product is the most expensive and the slowest.
- Reset expectations for the new curve: its early CAC will look terrible next to a mature channel's mature CAC, and comparing them kills good bets early (`acquisition.md`).

## The Stall Review

A 60-minute meeting with a fixed agenda, run once — not a standing committee:

1. The six fake-crisis checks, out loud, with numbers.
2. Growth accounting for the last three periods: new, resurrected, expansion, churned, contracted (`diagnosis.md`).
3. Marginal CAC per channel for the last three periods.
4. Retention curve of the last three cohorts against the three before them.
5. Name **one** cause from the table. Not three.
6. One bet, with a kill number and a re-check date, written into `## Targets`.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Reorganising the team | Six weeks of no output, then the same constraint | Name the cause first |
| Adding a channel to fix retention | Fills a leaking bucket faster | Fix the base equation (`retention.md`) |
| Spending more into saturation | Marginal CAC already exceeds target | Step spend back to the last level that cleared payback |
| Reading seasonality as a stall | Panic in the month the business always dips | YoY comparison first |
| Publishing more into decay | Replacement, not growth | Refresh the stock; measure useful life |
| Treating a mix shift as a conversion problem | Optimises a rate that never fell | Decompose performance versus mix |
| Waiting for the plateau to look for the next curve | The next channel takes 3-9 months to work | Start on deceleration, not on flatness |
| One stall review per week forever | The meeting becomes the work | One review, one bet, one re-check date |

**After any stall review**, write it back in the same turn: the named cause, the evidence that ruled out the other five, and the bet with its kill number and re-check date into `## Pain Points` and `## Targets` in `~/Clawic/data/growth/memory.md`; the seasonality pattern, once established, into `## Metric Definitions` next to the metric it distorts, so next year's version of this meeting is five minutes long (`memory-template.md`). A full review worth re-reading — decomposition, charts described, decision and what was rejected — is `~/Clawic/data/growth/artifacts/stall-review-<yyyy-mm>.md` with its `## Boxes` line.

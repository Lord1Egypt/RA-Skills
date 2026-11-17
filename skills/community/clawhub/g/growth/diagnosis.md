# Diagnosis — Finding the One Constraint

Growth work is triage. A business has one binding constraint at a time; effort spent anywhere else produces a number that moves and a business that does not. This file turns "growth is bad" into a named stage, an absolute lift, and one owner.

**Contents:** [The Decomposition](#the-decomposition) · [Ranking Stages by Absolute Lift](#ranking-stages-by-absolute-lift) · [Growth Accounting](#growth-accounting) · [Is It a Growth Problem at All](#is-it-a-growth-problem-at-all) · [Base Rates Worth Arguing With](#base-rates-worth-arguing-with) · [Razor Questions](#razor-questions) · [The Diagnosis Readout](#the-diagnosis-readout)

**Before diagnosing anything**, read `## Funnel`, `## Retention`, `## Channels` and `## Constraint` in `~/Clawic/data/growth/memory.md` — or whatever the `## Boxes` index points them to. A funnel with no prior period is a snapshot, not a diagnosis, and the last constraint you named is either fixed or still the answer.

## The Decomposition

Write the chain from SKILL.md's Growth Equation with the user's real numbers, one line per stage, each with denominator, window, and as-of date. Non-negotiable order: **volume → rate → value**, because rates without volumes produce the classic wrong answer (optimising a segment too small to matter).

```
Visitors (30d, unique)              120,000
→ Signup                    3.1%      3,720
→ Activated (aha in 7d)    22.0%        818
→ Paid (30d)                6.5%         53
→ M3 retained              71.0%          38   (of the M0 cohort)
ARPA 49 USD/mo · gross margin 0.82
```

Rules for building it:

- **One denominator per stage, and it is the stage above.** A funnel where stage 3 is measured against all users, not against stage 2, cannot multiply and will contradict itself.
- **Anchor cohorts on first touch**, permanently. Dating a cohort by the day someone converted moves people between cohorts and rewrites history every month (SKILL.md Numbers That Lie).
- **Same window at every stage** for the headline chain, plus a lagged view where the conversion cycle is long: a 45-day sales cycle inside a 30-day window shows a fake collapse at the bottom (`b2b.md`).
- **Segment the chain the moment two stages disagree**: acquisition source, plan, platform, geography, new-versus-existing. A blended chain hides that self-serve works and paid does not.

## Ranking Stages by Absolute Lift

`lift = upstream_volume × (achievable_rate − current_rate) × downstream_conversion × value_per_conversion`

Worked from the chain above, with `achievable_rate` set from the best segment already observed (never from a blog post):

| Stage | Current | Achievable | Math | Monthly lift |
|---|---|---|---|---|
| Signup | 3.1% | 3.4% | 120,000 × 0.003 × 0.22 × 0.065 × 49 | ~252 USD MRR |
| Activation | 22% | 30% | 3,720 × 0.08 × 0.065 × 49 | ~948 USD MRR |
| Paid conversion | 6.5% | 8.0% | 818 × 0.015 × 49 | ~601 USD MRR |

Activation wins, and it is not close — despite signup looking worse against any external benchmark. Three guards on this method:

- **`achievable_rate` must be evidenced**: the best-performing existing segment, a prior period, or a directly comparable product you have data for. A number pulled from an industry average is a wish with decimals.
- **Multiply by downstream conversion**, or you will value a signup at the price of a customer.
- **Cost the work**: a 948 USD/mo lift needing two engineer-quarters loses to a 601 USD/mo lift needing a week. Rank by `lift ÷ effort` once both are estimated (`experiments.md` for scoring).

## Growth Accounting

Net user or revenue change decomposes exactly (Social Capital's growth accounting; the identity holds by construction):

```
net = new + resurrected + expansion − churned − contracted
quick_ratio = (new + resurrected + expansion) ÷ (churned + contracted)
```

- Quick ratio **> 4** is the widely used bar for an early SaaS business growing efficiently; **< 1** means the bucket empties faster than it fills and no acquisition tactic will save the quarter. Between 1 and 4, the question is whether churn is concentrated in one segment.
- The most under-read term is **resurrected**. A large resurrection stream means people need the product periodically, not continuously — the natural frequency is longer than the reporting window, and "churn" is partly a measurement artefact (`retention.md`).
- Run it monthly on users *and* on revenue. Users up while revenue flat means the mix shifted to a cheaper plan; revenue up while users flat means expansion is carrying the business and new-customer acquisition is dead.

## Is It a Growth Problem at All

Four failures wear the same costume. Check in this order, because each one invalidates the work below it.

| Symptom | Test | If yes, it is not a growth problem |
|---|---|---|
| Curve never flattens; every cohort decays to zero | Cohort curve at natural frequency (`retention.md`) | Product/PMF problem — changing the product beats any channel (SKILL.md Stage Gates) |
| Users say they would be "not disappointed" if it vanished | Sean Ellis test: ≥40% "very disappointed" among users who reached value, n ≥ 40 responses | Pre-PMF. Segment the 40%+ subgroup and build for them only |
| The number moved when nothing shipped | Tracking change, bot traffic, a redirect, a pricing page A/B still running, a holiday | Data problem (`instrumentation.md`) |
| Payback is fine but cash is not | Payback in months versus cash runway | Financing/timing problem: profitable growth can still be unaffordable (`forecasting.md`) |

## Base Rates Worth Arguing With

Use these to spot an order-of-magnitude error, never as targets. Real ranges span 3-5× by segment, price point, and traffic quality; your own best segment is a better benchmark than any of them.

| Rate | Typical band | What moves it most |
|---|---|---|
| Visitor → free signup (self-serve SaaS) | ~1-5% | Traffic intent, not the button colour |
| Free signup → activated | ~20-40% | Steps before value, and whether value needs someone else to show up |
| Free → paid, freemium | ~2-5% | Paywall placement against a real limit (`monetization.md`) |
| Trial → paid, no card up front | ~10-25% | Activation during trial, not trial length |
| Trial → paid, card up front | ~40-60% | Trial length and cancellation friction, plus a worse top of funnel |
| B2B lead → closed won | ~1-5% end to end | Lead source quality; MQL definitions differ so widely the number is only comparable to itself |

If a claimed rate sits outside its band by more than ~2×, the definition is wrong before the business is exceptional. Check the denominator first (`instrumentation.md`).

## Razor Questions

- What is the one number that, if it doubled, would change the company — and which stage produces it?
- If we could only run one experiment this quarter, which stage would it be on, and what is the lift in currency?
- Which of these numbers would still be true if measured a different, equally defensible way?
- What did the last cohort do differently from the one before it, and did we cause that?
- Who is already succeeding with this product, and what is true of them that is not true of everyone else?
- What are we assuming that we have never measured — and what would it cost to measure it this week?

## The Diagnosis Readout

Six lines, no deck:

1. Constraint: the stage, with current and achievable rate.
2. Size: absolute monthly lift in currency, with the arithmetic visible.
3. Evidence: where `achievable_rate` came from.
4. Bet: the one or two experiments aimed at it, with their kill numbers (`experiments.md`).
5. What we are deliberately not doing this quarter, and why.
6. Re-check date: when this diagnosis expires and gets re-run.

**After any diagnosis**, write it back in the same turn: the stage chain with its as-of date to `## Funnel`, the named constraint and its expiry date to `## Constraint`, and any base rate you established for this business to `## Funnel` next to the stage it belongs to (`memory-template.md`). If the readout is going to be re-read — quarterly planning, a board update, a handover — it is an `artifacts/<kebab-name>.md` file with its `## Boxes` line in the same turn. A diagnosis nobody can find is repeated from scratch next quarter, usually with a different answer.

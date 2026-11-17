# B2B Growth — Motion Fit, PQLs, and Pipeline That Is Not Fiction

In B2B the user, the champion, and the buyer are three people, and the funnel has a human in it. That changes the arithmetic: cycles are long, samples are small, and the unit of retention is an account, not a person.

**Contents:** [Choosing the Motion](#choosing-the-motion) · [The Two Funnels](#the-two-funnels) · [PQL — Product Qualified Lead](#pql--product-qualified-lead) · [Hand-off Rules](#hand-off-rules) · [Pipeline Arithmetic](#pipeline-arithmetic) · [Cycle Time](#cycle-time) · [Account Expansion](#account-expansion) · [Measuring Growth With Small Numbers](#measuring-growth-with-small-numbers) · [Traps](#traps)

**Before advising on motion or pipeline**, read `## Business` (motion, ACV, ICP), `## Funnel` and `## Channels` in `~/Clawic/data/growth/memory.md`, and check `~/Clawic/data/contacts/contacts.md` before treating any named champion, buyer, or agency as new.

## Choosing the Motion

ACV sets what the go-to-market can afford. The rule is arithmetic, not philosophy: a salesperson's fully loaded annual cost divided by realistic deals per year sets the minimum ACV a human touch can carry.

Bands below are USD; convert to the `profile.yaml` currency before quoting them, since they track fully loaded rep cost, not price.

| ACV band | Viable motion | Why |
|---|---|---|
| Under ~1k USD/yr | Pure self-serve | No human touch pays for itself at any close rate |
| ~1k-15k USD/yr | Self-serve with assisted close on PQLs | A human helps only where the product already qualified the account |
| ~15k-100k USD/yr | Inside sales, product-led entry | Deals justify a rep; the product still generates the lead |
| Over ~100k USD/yr | Field sales, pilots, procurement | The buying process itself requires a human on both sides |

Worked check: a rep costing 150k USD/yr fully loaded, closing 40 deals/yr, needs roughly 3.75k USD of gross profit per deal just to break even on the rep — before marketing, onboarding, or support. Below that, the motion is self-serve whatever the plan says. Hybrid (`motion: hybrid`) is legitimate and is the hardest to run: it needs an explicit rule for which accounts get a human, or reps cherry-pick and self-serve conversion silently degrades.

## The Two Funnels

Self-serve and sales-assisted funnels must be measured separately; blending them produces numbers that describe no real process.

| Self-serve | Sales-assisted |
|---|---|
| visitor → signup → activated → paid | lead → MQL → SQL → opportunity → closed won |
| Unit: user, then account | Unit: account throughout |
| Cycle: minutes to days | Cycle: weeks to quarters |
| Failure: activation | Failure: SQL definition and stage hygiene |

Where both exist, every account carries a `motion` property from the first event (`instrumentation.md`), and every metric is reported by motion. The most common B2B measurement error is a blended conversion rate across two funnels whose cycle times differ by an order of magnitude.

## PQL — Product Qualified Lead

A PQL is an account whose **product behaviour** predicts buying. It replaces the MQL's "downloaded a whitepaper" with evidence.

Derive it the same way as the aha action (`activation.md`), but at account level: split accounts into converted and not, and rank behaviours by the gap. Typical discriminators, all of which must be verified against your own data:

- Multiple users from the same email domain active in a window
- Hitting or approaching a plan limit
- Using a capability that only matters at production scale (integration connected, API in use, data volume)
- Admin or security actions (SSO configured, permissions set) — someone is preparing to standardise on you
- An invite to a person with a buying-adjacent title

Rules: define the PQL with a **threshold and a window** (three or more active users in seven days, not "high engagement"); score at the **account**, not the user; and re-derive quarterly, because the signal drifts as the product changes. A PQL definition that never changes is a definition nobody is testing.

## Hand-off Rules

Written down, or reps will invent them:

- **What qualifies** (the PQL threshold), **who acts** (named owner), **within how long** (response-time SLA — speed to first contact is one of the few universally replicated advantages in inbound sales), and **what happens if they do not**.
- **Do not interrupt a working self-serve flow.** An account that is converting on its own does not need a call; contact is for accounts stuck below their potential or above the self-serve ceiling.
- **The rep must see product usage** in their CRM. A call that opens with a question the product already answered wastes the advantage of being product-led.
- **Round-trip**: an account a rep disqualifies goes back to nurture with the reason recorded, never to a dead list (`lifecycle.md`).

## Pipeline Arithmetic

```
pipeline_needed = target_new_ARR ÷ win_rate
coverage        = open pipeline ÷ target for the period      (3× is a common working bar)
```

- **Coverage below ~3× at the start of a quarter means the quarter is already decided**; more activity now closes in the next quarter, not this one. That is the single most useful fact in B2B forecasting and the one most often argued with.
- **Stage definitions must be behavioural, not emotional**: "prospect confirmed budget and named the decision process" beats "feels positive". A stage the seller can enter unilaterally is not a stage.
- **Age out stale opportunities automatically** — a deal untouched for two cycles is not pipeline, and leaving it in inflates coverage exactly when accuracy matters.
- **Win rate is per source.** Outbound, inbound, and PQL-sourced deals win at materially different rates; a blended win rate makes every allocation decision wrong.

## Cycle Time

- Measure from **first touch** to closed won, per source and per ACV band. It sets the lag between a growth action and its revenue, and therefore how long any channel test must run before it can be judged (`acquisition.md`).
- Long cycles make quarterly experiments impossible on the closed-won metric; pick a **leading indicator** agreed in advance — SQL creation, pilot start, security review passed — and confirm later (`experiments.md`).
- The most compressible parts are usually procurement and security review, not selling. Pre-built security documentation, a standard DPA, and a completed questionnaire removes weeks that no amount of sales skill can.
- Multi-threading — more than one contact engaged in the account — is the strongest protection against a stalled cycle, because champions change jobs mid-deal often enough to be a planning assumption.

## Account Expansion

Expansion is where B2B growth compounds; NRR above 100% grows the business with zero new logos (`saas-metrics` for definitions).

- Pick an expansion vector that tracks customer value: seats, usage, modules, or entities managed (`monetization.md`).
- **Instrument the expansion trigger**: seats approaching the licensed count, usage above the tier, a new department appearing in the user list.
- **Champion turnover is the top hidden churn risk** in accounts that look healthy: usage flat, renewal quiet, then a loss. Track whether the champion is still active, and whether more than one person is.
- Land-and-expand only works if the landing spot is a real workflow, not a trial seat: a single-team deployment that never spreads renews once and churns.

## Measuring Growth With Small Numbers

With 40 deals a quarter, A/B testing the funnel is not available. What works instead:

- **Cohort comparisons over time** with explicit caveats about n (`experiments.md`).
- **Qualitative saturation**: 5-8 win/loss interviews per segment surface the recurring reasons; the next interview stops adding new ones and that is the signal to stop.
- **Sequenced rollouts**: change one thing for one segment or one region, and compare to the untouched one.
- **Leading indicators with tighter loops**: meeting-set rate, demo-to-pilot, security-review pass time — all of which have more events than closed-won.
- Never report a percentage on a denominator under ~30 without the raw counts next to it. "Win rate rose from 20% to 33%" on 15 deals is two extra wins.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Hiring a sales team below the ACV threshold | The rep cannot pay for themselves at any plausible close rate | Run the fully loaded arithmetic first |
| MQLs that nobody in sales accepts | Marketing hits its number, sales gets nothing, both are honest | PQLs from product behaviour, with an accepted-rate metric |
| Blending self-serve and sales funnels | A conversion rate describing no real process | Report by motion, always |
| Coverage ignored until week 10 | The quarter was decided in week 1 | Coverage at the start, with a 3× bar |
| Stages advanced on optimism | Forecast becomes fiction; nobody trusts it | Behavioural exit criteria per stage |
| Single-threaded deals | The champion leaves and the deal dies silently | Multi-thread as policy |
| Judging a channel before one cycle | 45-day cycle killed at 30 days is a guaranteed false negative | Kill date ≥ one measured cycle (`acquisition.md`) |
| Percentages on tiny denominators | Two deals look like a trend | Raw counts alongside every rate |

**After any motion, PQL, or pipeline work**, write it back in the same turn: the PQL definition with its threshold and window into `## Metric Definitions`, motion, ACV band and win rate by source into `## Business`, and the two funnels' stage rates into `## Funnel` — all in `~/Clawic/data/growth/memory.md` with as-of dates (`memory-template.md`). People go to the shared `~/Clawic/data/contacts/contacts.md` (one row per person, keyed by lowercase email, updated in place), a named deal or pilot with an owner to `~/Clawic/data/projects/<project>.md`, and a win/loss synthesis worth re-reading to `artifacts/win-loss-<yyyy-qn>.md` with its `## Boxes` line.

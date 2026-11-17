# Loops — Mechanisms That Reinvest Their Own Output

A funnel spends an input to get an output. A loop's output becomes its next input, so the same effort compounds. Most companies say "loop" and run funnels; the test is one sentence long and this file starts with it.

**Contents:** [The Test](#the-test) · [Writing a Loop Down](#writing-a-loop-down) · [The Four Loop Families](#the-four-loop-families) · [Viral Math](#viral-math) · [Cycle Time Beats Coefficient](#cycle-time-beats-coefficient) · [Content Loop Math](#content-loop-math) · [Paid Loop Math](#paid-loop-math) · [Why Loops Stop Turning](#why-loops-stop-turning) · [Choosing One](#choosing-one) · [Traps](#traps)

**Before designing a loop**, read `## Loops` and `## Channels` in `~/Clawic/data/growth/memory.md`. A loop that was tried and did not close is worth more than a new idea, and the step where it broke is usually still broken.

## The Test

**Does the output of step N feed step 1 without new spend?** If the answer needs a marketing budget every cycle, it is a channel, not a loop — with one exception: the paid loop, where the reinvested output is *money* and the loop is real as long as payback beats the reinvestment period.

Second test: **can you state the cycle time in days?** A loop nobody has timed cannot be forecast and cannot be improved, because every improvement is measured against the exponent (below).

## Writing a Loop Down

Four fields, one line each. Anything longer is a strategy essay, not a mechanism.

```
Loop: collaborative invite
Steps:   user creates document → invites collaborator to edit →
         collaborator signs up to comment → creates their own document
Input:   1 activated user
Output:  0.4 new activated users per cycle
Cycle:   9 days median (create → invite → accepted signup)
Bottleneck: invite acceptance 31% (email deliverability + unclear ask)
```

Instrument each arrow as an event with the ids that link them (`instrumentation.md`): without `invite_id` on the signup event, the loop is a story.

## The Four Loop Families

| Loop | Output that becomes input | Measure | Requires | Where it stalls |
|---|---|---|---|---|
| Viral / collaborative | New users invited by users | Invites sent per user × acceptance rate | Value that needs, or improves with, another person | Invite is asked before the inviter got value |
| Content / SEO | Pages or artifacts that pull search and social traffic | Traffic per unit × units created per period | Content that a user or the product generates as a by-product | Production cannot outrun decay and competition |
| Paid | Revenue reinvested into ads | Payback period versus reinvestment cadence | Payback shorter than cash cycle, and margin | CAC rises with volume; the loop is capital-bound (`paid.md`) |
| Sales / referral-led | Customers who produce references, case studies, and warm leads | Referenceable customers × leads per reference | High ACV and a delivery org that produces happy accounts | No systematic ask; references stay anecdotal (`b2b.md`) |

Two hybrids worth naming because they are common and behave differently: **user-generated content** (viral in acquisition, content in distribution — a review site, a template gallery) and **network data** (each user improves the product for the next — pricing data, fraud signals, recommendations), which compounds retention rather than acquisition and is invisible in a funnel chart.

## Viral Math

```
k = invites_sent_per_user × invite_acceptance_rate
n = cycles elapsed = t ÷ cycle_time
```

Two models answer two different questions; mixing them is where the arithmetic in most decks breaks:

```
one-shot cascade — a cohort invites once, its invitees invite once, and so on:
  generation_n        = users(0) × k^n            each generation is smaller while k < 1
  total_from_one_user = 1 ÷ (1 − k)               while k < 1; unbounded at k ≥ 1

recurring loop — every active user invites again each cycle:
  users(n) = users(0) × (1 + k)^n                 per-cycle multiplier is 1 + k, not k
```

The per-cycle multiplier is **1 + k** because each cycle keeps the existing users and adds k per user. Using `k^n` for a live loop is the single most common error here: at k = 0.5 it predicts the population halving every cycle.

- **k > 1 is exponential and rare, and it never lasts**: the addressable network saturates, so treat any k > 1 as temporary and plan for the k < 1 steady state.
- **k = 0.4 is not failure**: in the cascade model it is a 1.67× multiplier on every acquired user (1 ÷ 0.6), which cuts effective CAC by 40%. That is the realistic prize, and it is large.
- Compute k on **activated** users, not signups; invites from people who never got value convert at a fraction of the rate and pollute the number.
- Worked example: 100 paid signups at 50 USD CAC, k = 0.4 → 167 total users → effective CAC 30 USD. The same 50 USD CAC with k = 0.6 → 250 users → 20 USD.

## Cycle Time Beats Coefficient

Because time sits in the exponent, halving cycle time **squares** the growth over the same period, while raising k only lifts the base.

Worked, recurring loop, multiplier `(1 + k)^n`, 90-day window:

```
k = 0.5, 30-day cycle → n = 3   → 1.5³  =  3.375×   (baseline)
k = 0.5, 15-day cycle → n = 6   → 1.5⁶  = 11.39×    (= 3.375², the baseline squared)
k = 0.6, 30-day cycle → n = 3   → 1.6³  =  4.096×   (a 20% lift in k adds 0.72×)
```

Halving the cycle adds 8.0× against the 0.72× a 20% lift in k adds — roughly **11× the gain**, and cycle time is usually the cheaper of the two to change. So the ranked work is:

1. Shorten the time from **value received** to **invite prompted** — this is usually days of latency created by asking in an email instead of in-product.
2. Shorten **invite → accepted**: one-click accept, no account required to see the shared thing, mobile-friendly link.
3. Shorten **accepted → activated**: the invitee lands on the shared object with value visible, never on a generic signup page (`activation.md`).
4. Only then raise acceptance rate with copy, incentives, and channel choice (`referrals.md`).

## Content Loop Math

```
steady_state_traffic ≈ units_per_period × traffic_per_unit × average_useful_life
```

- Content decays: traffic per unit falls after publication at a rate that varies enormously by topic and format. Measure your own decay curve on units at least two quarters old rather than assuming a number.
- The loop closes only if content produces users **who produce content** — reviews, templates, public projects, answers. Otherwise it is a channel with a content team attached, which is fine but does not compound (`acquisition.md`, and `seo` for the craft).
- Programmatic pages (one page per entity) compound fastest and hit quality thresholds hardest; the constraint is unique value per page, not page count.
- Measure `units_created_per_active_user` — if it is near zero, the loop is a funnel and should be budgeted as one.

## Paid Loop Math

The paid loop is real when the money comes back faster than you need to spend it again:

```
reinvestment_ratio = gross_profit_per_customer_in_period ÷ CAC
```

If payback is 6 months and you re-spend monthly, the loop needs external capital for the gap — that is a financing decision, not a growth one (`forecasting.md`). It stops compounding when CAC rises with spend (`paid.md`), which it always does past the efficient audience.

## Why Loops Stop Turning

| Failure | Signal | Fix |
|---|---|---|
| Asked before value | Invite rate high, acceptance low | Move the prompt after the aha action (`activation.md`) |
| Nothing to invite anyone *to* | Invites accepted, invitees never activate | Land them on the shared object with value visible |
| Network saturation | k falling steadily inside the same segment | New segment or new geography; the loop is not broken, its pond is empty |
| Channel closed | Deliverability, platform API removed, feed algorithm change | Diversify the invite channel; a loop on one platform's rails is that platform's asset |
| Incentive fraud | Signups with no activation, clustered by device or IP | Reward on activation, not on signup (`referrals.md`) |
| Content decay outruns production | Traffic flat while unit count grows | Refresh existing units before publishing new ones |

## Choosing One

Pick the loop the product's own use produces as a by-product; anything else is a bolt-on that needs perpetual maintenance.

| Product truth | Loop |
|---|---|
| Value increases with other people present | Viral / collaborative |
| Usage creates a public artifact | Content / UGC |
| High ACV, human sale, referenceable outcomes | Sales / referral-led |
| Predictable payback, gross margin above ~70%, capital available | Paid |
| Usage improves the product for the next user | Network data — compounds retention; pair it with one acquisition loop |
| None of the above | You have channels, not a loop. Say so, budget accordingly, and stop calling the marketing plan a flywheel |

Run **one** loop as the primary; a second is a distraction until the first is instrumented, timed, and improving.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Calling a funnel a flywheel in a deck | The arrows in the diagram do not exist in the product | Apply The Test out loud; name the step that feeds step 1 |
| Optimising k while ignoring cycle time | The exponent is time; the base is only 1 + k | Rank the four cycle-time cuts first |
| Incentives before the loop closes | Pays for behaviour that does not survive the incentive | Close the mechanism, then consider incentives (`referrals.md`) |
| One loop per team | Loops with different cycle times compete for the same surface | One primary loop with one owner |
| Loop metrics on signups | Non-activated inviters distort every rate | Compute on activated users |
| Assuming a published decay rate | Decay varies by topic, format, and competition | Measure your own units at two quarters |

**After identifying, timing, or falsifying a loop**, write it back in the same turn: the loop's four fields plus its measured k or traffic-per-unit and its bottleneck into `## Loops` in `~/Clawic/data/growth/memory.md`, and the cycle-time measurement with its as-of date next to it (`memory-template.md`). A loop design that shipped — the diagram, the events that instrument it, what was rejected — is `~/Clawic/data/growth/artifacts/loop-<name>.md`, born as its own file with its `## Boxes` line in the same turn. A loop that was tried and did not close gets the same treatment: the failed step is the most reusable thing in this file.

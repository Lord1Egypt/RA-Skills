# Paid Media — Economics, Incrementality, and Creative

Paid is the only channel that answers instantly and lies fluently. It buys learning speed at a known price; it also reports credit for conversions that would have happened anyway. This file is about the numbers behind the spend, not the button layout of any ad manager.

**Contents:** [The Only Four Levers](#the-only-four-levers) · [Incrementality](#incrementality) · [Attribution Reality](#attribution-reality) · [Bidding and Budget Mechanics](#bidding-and-budget-mechanics) · [Creative Is the Targeting](#creative-is-the-targeting) · [Scaling Without Breaking Payback](#scaling-without-breaking-payback) · [Efficiency Metrics and What They Hide](#efficiency-metrics-and-what-they-hide) · [Traps](#traps)

**Before changing spend**, read `## Channels` in `~/Clawic/data/growth/memory.md` for the current CAC, payback and kill number, and `~/Clawic/data/finances/budget.md` for what is committed. Raising a budget without the payback number in front of you is how a quarter's cash disappears in six weeks.

## The Only Four Levers

Every paid result decomposes into four multiplicands. Diagnose in this order, because each one is cheaper to fix than the next:

```
CAC = CPM ÷ 1000 × (1 ÷ CTR) × (1 ÷ landing_conversion) × (1 ÷ signup_to_customer)
```

| Lever | Owned by | Realistic range of improvement |
|---|---|---|
| Creative (drives CTR and effective CPM) | Creative volume and quality | Largest single lever on most platforms; multiples, not percentages |
| Audience / targeting | Exclusions, signal quality, feed | Diminishing; modern platforms optimise better than manual segments given signal |
| Landing conversion | Page and offer match | Meaningful and cheap to test (`cro`) |
| Post-signup conversion | Product and activation | Slowest, largest downstream effect (`activation.md`) |

Teams reflexively pull lever 2 because it is a dropdown. Lever 1 is where the money is, and lever 4 is where the business is.

## Incrementality

The question is not "what did the platform report" but "what would have happened anyway".

| Method | Cost | Rigour | When |
|---|---|---|---|
| Geo hold-out (matched markets, one dark) | Medium | High | Any spend level where a region can be paused for 2-4 weeks |
| Audience hold-out (platform-side) | Low | Medium — platform grades its own homework | Continuous read on retargeting and prospecting |
| Full pause test | Free, painful | High for the paused window | Suspected non-incremental channels; brand search first |
| Modelled MMM | High | Medium | Large multi-channel spend with long history |
| Platform-reported ROAS alone | Free | Low | Never as the sole basis for a scale decision |

- **Start with branded search.** It is the most-defended and least-incremental line item in most accounts; a two-week pause in one region measures it for the cost of the traffic you would have got free.
- **Retargeting is the second suspect**: it targets people who were already coming back. Hold out 10-20% permanently and read the delta.
- Sum of platform-reported conversions greater than actual orders is proof of double-counting, and it is common. Reconcile against the billing system, which is the only source of truth for money (`instrumentation.md`).

## Attribution Reality

- iOS App Tracking Transparency (2021) ended reliable deterministic user-level attribution on iOS; SKAdNetwork returns delayed, aggregated, privacy-thresholded data — mobile UA must be run on cohort and incrementality logic, not per-user ROAS (`mobile.md`).
- Third-party cookies have been off by default in Safari and Firefox for years, so cross-site retargeting reach is smaller than dashboards imply.
- Server-side conversion APIs improve signal quality for optimisation; they do not restore truth about which touch caused what.
- Practical stance: **platform numbers for optimisation inside a platform, incrementality tests for allocation between platforms, billing data for the total.** Multi-touch model mechanics and their politics: `marketing-attribution`.

## Bidding and Budget Mechanics

Stable across platforms, whatever the interface calls them:

- **The learning phase is real.** Automated bidding needs a conversion volume per ad set per week before it stabilises; below that it never exits learning and results stay erratic. Consolidate ad sets to concentrate conversions rather than splitting into ten precise audiences with three conversions each.
- **Edits reset learning.** Budget changes above roughly ±20%, creative swaps, and audience edits restart it. Change one thing, then wait a full learning cycle before judging.
- **Bid to the value you can afford, not to what you can get.** Target CPA = target CAC × (signup_to_customer rate) when optimising to signups rather than purchases.
- **Optimise to the deepest event with enough volume.** Purchase if you have enough purchases per week; otherwise a strong upstream proxy that correlates with purchase — and verify the correlation before trusting it, because optimising to a proxy buys the proxy.
- **Frequency and audience size** set the fatigue clock: small audience plus high budget equals rising frequency, falling CTR, rising CPM — that is not creative fatigue, it is arithmetic.
- **Seasonality moves auction prices**, not your product's appeal. Q4 CPMs rise in consumer categories; a CAC comparison across that boundary is not like-for-like (`plateaus.md`).

## Creative Is the Targeting

On feed platforms the creative selects the audience: the algorithm shows it to people who behave like the people who engaged with it.

- **Volume with structure.** Test concepts (the angle, the promise, the format), not variations of a button. Ten variations of one concept teach one thing; three concepts teach three.
- **A concept is a hypothesis about the buyer**: which pain, which moment, which alternative they are comparing against. Write it down before producing, and the losing test still teaches you something about the market.
- **Iterate winners, retire losers.** The pattern that repeats across accounts is a small number of concepts carrying most of the spend, with a long tail of failures — plan production volume for that distribution rather than for a hit rate.
- **Fatigue** shows as CTR decay with rising frequency at stable audience size. Refresh the concept, not just the image; a new colour on a dead angle buys days.
- **Landing match**: the page must repeat the ad's promise in its first screen. A mismatch shows up as high CTR with collapsing landing conversion — lever 3, not lever 1 (`cro`).

## Scaling Without Breaking Payback

- Raise budget in steps of ~20-30% and hold for a full learning cycle. Doubling overnight resets learning and buys the expensive part of the audience at once.
- Watch **marginal CAC**, not average: `marginal_CAC = Δspend ÷ Δcustomers` between two periods. Average CAC stays comfortable long after the last increment of spend has stopped paying back. Worked: spend 10k→15k, customers 100→120 → marginal CAC 250 USD against an average of 125 USD; if the target is 150 USD, you crossed the line two steps ago.
- Expand by **new audience or new geography**, not by bidding harder into a saturated one.
- Stop-loss: when marginal CAC exceeds target for two consecutive periods, step spend back to the last level that cleared it and fix a lever before trying again (`plateaus.md`).

## Efficiency Metrics and What They Hide

| Metric | Definition | Hides |
|---|---|---|
| ROAS | Revenue ÷ ad spend, usually first-order | Gross margin, refunds, and repeat purchase; a 3× ROAS at 20% margin loses money |
| MER (blended) | Total revenue ÷ total ad spend | Which channel is carrying it; useful as a governor, useless as a diagnosis |
| CPA | Cost per reported conversion | Whether the conversion event equals a customer, and whether it was incremental |
| CAC payback | CAC ÷ (monthly ARPA × gross margin) | Nothing — this is the one that decides scale (SKILL.md Rule 4) |

For subscription businesses, first-order ROAS is structurally misleading: the money arrives over months. Use payback and cohort revenue curves. For transactional businesses, ROAS must be computed on contribution margin, not revenue (`ecommerce.md`).

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Scaling on platform-reported ROAS | The platform grades its own homework and double-counts across platforms | Reconcile to billing; hold-out test before a step change |
| Doubling budget on a good week | Resets learning, buys the expensive audience, breaks payback | 20-30% steps, one learning cycle each |
| Ten precise ad sets | Conversions split below the learning threshold; nothing stabilises | Consolidate; let the algorithm find the audience with good creative |
| Judging creative by CPM | Cheap impressions to people who never convert are the most expensive thing in the account | Judge on CAC and downstream retention by creative |
| Counting brand search as growth | Harvests demand created elsewhere | Report brand and non-brand separately; pause-test brand once |
| Retargeting scaled as prospecting | Small audience, rising frequency, mostly non-incremental | Cap it, hold out a slice permanently, measure the delta |
| No exclusion of existing customers | You pay to reach people who already pay you | Suppression lists from the billing system, refreshed weekly |
| Optimising to signups when purchases exist in volume | Buys the cheapest signups, which convert worst | Optimise to the deepest event with sufficient volume |

**After any spend change, incrementality test, or CAC recomputation**, write it back in the same turn: the channel row with new CAC, payback, spend with currency and as-of date into `## Channels` in `~/Clawic/data/growth/memory.md`; the committed budget into the shared `~/Clawic/data/finances/budget.md` with its currency and period; the hold-out test into `experiments/<year>.md` with its design and result (`memory-template.md`). A creative concept framework or an account structure that finally worked is `artifacts/<kebab-name>.md` with its `## Boxes` line — and no ad-account token, pixel secret, or API key ever goes into any of them, only pointers like `keychain:meta-ads`.

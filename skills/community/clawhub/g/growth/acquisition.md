# Acquisition — Choosing, Sizing, and Killing Channels

A channel is a bet with a cost, a ceiling, and a time to signal. This file picks which bets to place, how much to place, and the number that ends them. Paid media mechanics live in `paid.md`; this is the portfolio above them.

**Contents:** [The Portfolio Rule](#the-portfolio-rule) · [Scoring a Candidate Channel](#scoring-a-candidate-channel) · [The Channel Catalog](#the-channel-catalog) · [Sizing a Test](#sizing-a-test) · [The Kill Number](#the-kill-number) · [Unit Economics That Survive Scale](#unit-economics-that-survive-scale) · [Channel Fit by Model](#channel-fit-by-model) · [Sequencing](#sequencing) · [Traps](#traps)

**Before proposing any channel**, read `## Channels` in `~/Clawic/data/growth/memory.md` — or `channels.md` if `## Boxes` points there — and `~/Clawic/data/finances/budget.md` for what is actually available. A channel already killed, with its CAC and the reason, is the most valuable row in the table; proposing it again without new information is the classic repeated mistake.

## The Portfolio Rule

**Two or three tests live at once, each with a kill number and a kill date set before spend starts** (SKILL.md Rule 6). More than three degrades attribution (overlapping audiences), team attention, and creative quality simultaneously.

Alongside the tests sits exactly one **scaling** channel — the one already inside payback — and the rule is that its budget rises only while payback holds at 2× the current spend. A portfolio is: one scaling, two or three testing, everything else documented as killed with its number.

## Scoring a Candidate Channel

Five dimensions, scored before spending anything:

| Dimension | Question | Kills the idea when |
|---|---|---|
| Audience presence | Is the buyer demonstrably there in volume? | You would be educating a platform's audience about a category they never asked about |
| Intent | Are they expressing the need, or being interrupted? | High-consideration purchase on a pure interrupt channel with no nurture path |
| Cost to signal | What is the minimum spend and time to get a readable result? | The minimum test costs more than a quarter's budget |
| Volume ceiling | If it works perfectly, how many customers per month can it produce? | The ceiling is below your monthly target — a great channel that cannot matter |
| Competence | Do we have the specific skill (creative, writing, sales, SEO) in-house or bought? | The channel needs a craft nobody has and the test would measure our incompetence |

Volume ceiling is the most-skipped and the most expensive to skip: teams optimise a channel for a year that could never have carried the plan. Estimate it as `addressable audience × plausible reach % × conversion` before starting.

## The Channel Catalog

| Channel | Time to signal | Ceiling | CAC behaviour | Fits |
|---|---|---|---|---|
| Search ads (branded) | Days | Low — capped by your own demand | Cheap, mostly harvest, rarely incremental | Everyone, but do not count it as growth (`paid.md`) |
| Search ads (non-brand) | 2-4 weeks | Medium-high | Rises with keyword breadth as intent drops | Existing category with search volume |
| Paid social | 2-4 weeks | High | Rises steeply past the efficient audience; creative-bound | Impulse, visual, broad audiences |
| SEO / content | 3-9 months | High, compounding | Falls with scale once the machine works | Category with search volume and topical depth (`seo`, `loops.md`) |
| Programmatic/entity pages | 2-6 months | Very high | Near-zero marginal, quality-gated | Products with a catalog of entities |
| Marketplaces and app stores | Weeks | Platform-capped | Rank-dependent, listing-quality-bound | Anything the platform lists (`mobile.md`) |
| Communities | Weeks | Low per community, additive | Time cost, not money | Niche audiences with a real gathering place |
| Outbound sales | 4-8 weeks | Medium, headcount-linear | Flat per rep; does not compound | ACV high enough to pay for a human (`b2b.md`) |
| Partnerships / integrations | 2-6 months | Medium-high | Fixed cost, then near-zero marginal | Products living inside another product's workflow |
| Influencers / creators | Weeks | Medium | Highly variable; rises as you exhaust good fits | Consumer, visual, trust-led purchases |
| Affiliates | 1-3 months | Medium | Fixed CPA by design; fraud and cannibalisation risk | Transactional, clear conversion event |
| Referral | Weeks after retention | Scales with base | Falls with base size | Products people already recommend (`referrals.md`) |
| Events / field | Months | Low, lumpy | High and fixed | Enterprise, relationship-led |
| PR / launches | Days, one-shot | Spike, not stream | N/A | Awareness for a category-new product (`go-to-market`) |

None of these is a strategy on its own. The strategy is which two you are testing this quarter and why the other twelve are not.

## Sizing a Test

A test must be able to produce a readable answer. Minimum spend for a paid test:

```
min_test_spend = target_CAC × conversions_needed
conversions_needed ≈ 30 for a directional read; ~100 before you trust the CAC
```

Worked: target CAC 150 USD, 30 conversions → ~4,500 USD to get a directional read. If `monthly_paid_budget` cannot cover the minimum for a channel, do not run a small version of it — a test that cannot reach 30 conversions produces a number that is noise, and the team will treat it as a verdict. Test a cheaper channel instead, or save until the budget exists.

For non-paid channels the currency is time: the minimum is one full production cycle plus one indexing/consideration lag (SEO: publish 15-30 units and wait a quarter; outbound: 200-300 contacts through a complete sequence). Both come out of the same scarce resource — team attention — so they compete with paid tests for a slot in the portfolio.

## The Kill Number

Written before the spend, in the channel row, in this form: *"Kill if CAC > X after Y conversions or Z weeks, whichever comes first."*

- Set X at ~1.5× target CAC for a first test: early CAC is always the worst CAC (learning phases, unoptimised creative, no exclusions).
- Y ≥ 30 conversions, or the number is noise.
- Z ≥ one full conversion cycle — the lag from click to purchase, measured, not assumed. Killing a 45-day sales cycle at 30 days guarantees a false negative (`b2b.md`).
- The kill decision belongs to whoever set the number, before the test, and gets recorded with the number that triggered it. Extending a test is allowed exactly once, with a written reason and a new number.

A killed channel is an asset: the row records CAC, volume, what was tried, and what would make it worth retrying (a price change, a new segment, a creative capability).

## Unit Economics That Survive Scale

```
CAC            = (channel spend + attributable people cost) ÷ new customers from it
payback_months = CAC ÷ (monthly ARPA × gross_margin)
LTV (capped)   = monthly ARPA × gross_margin × min(1 ÷ monthly_churn, 24-36)
```

- **Include people cost** in CAC for channels whose cost is labour (content, outbound, community). Excluding it makes organic look free and produces a plan nobody can staff.
- **Blended CAC is for the board; paid CAC decides the bid.** Blended divides all spend by all customers and lets organic subsidise a losing channel (SKILL.md Numbers That Lie).
- **The 2× test**: a channel is scalable only if payback still clears `target_cac_payback_months` after doubling spend. Efficiency at 3k/month says nothing about 30k/month; CAC rises as you move from the in-market audience outward.
- Recompute CAC monthly with an as-of date. A CAC quoted from six months ago is a different business.

## Channel Fit by Model

| business_model | Where it usually works | Where teams waste a year |
|---|---|---|
| saas (self-serve) | Non-brand search, content/SEO, integrations, communities | Broad paid social before the value proposition is legible in one image |
| b2b-sales | Outbound, partnerships, events, targeted content | Consumer social; volume channels that produce unqualified leads (`b2b.md`) |
| marketplace | Supply-side SEO and outbound, demand-side search; seeded city by city | Spending on the unconstrained side (`marketplaces.md`) |
| ecommerce | Paid social with strong creative, marketplaces, email/SMS, affiliates | Chasing new customers when repeat purchase is unmeasured (`ecommerce.md`) |
| consumer-app | App store optimisation, creators, referrals, paid UA against measured LTV | Paid UA before D7 retention supports it (`mobile.md`) |
| media | Content/SEO, syndication, newsletters, social distribution | Paid acquisition of readers whose RPM cannot repay it |

## Sequencing

1. **One channel to repeatability first.** Two half-working channels teach less than one that works, and a team that has never made a channel work has no baseline to compare against.
2. **Make it manual before automating it.** Hand-written outbound, hand-placed content, personally recruited supply — the manual version tells you whether demand exists at all, and it is the only cheap way to learn the message.
3. **Then add the second channel whose failure mode is different** — pair an intent channel with an interrupt one, so a platform change cannot take both.
4. **Concentration risk is a real risk.** Above ~70% of new customers from one channel, the next algorithm change is an existential event; that is the trigger to open the third channel even while the first is still working.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Testing six channels at once | Nothing reaches signal; attribution overlaps; team attention shatters | Two or three, each with a kill number (Rule 6) |
| Judging a channel on week-one CAC | Learning phases and delayed conversion make it the worst CAC you will ever see | Judge at the pre-committed conversion count and cycle |
| Excluding labour from organic CAC | Makes content and outbound look free; the plan cannot be staffed | Fully loaded CAC per channel |
| Scaling on blended CAC | Organic hides that paid loses money on every customer | Paid CAC per channel, per campaign |
| Copying a competitor's channel mix | You see their spend, not their margin, ceiling, or loop | Score the five dimensions for your own economics |
| Brand search counted as acquisition | Harvests demand created elsewhere; incrementality is usually low | Report brand and non-brand separately (`paid.md`) |
| No kill number | The champion extends the test until the budget ends | Number and date before spend |
| Ignoring the volume ceiling | A great channel that cannot carry the plan | Estimate the ceiling before the first unit of spend |

**After starting, scaling, or killing any channel**, write the row back in the same turn: channel, status, monthly spend with its currency, CAC, payback, volume, kill number and as-of date into `## Channels` in `~/Clawic/data/growth/memory.md` — past ~15 channels or when the table stops fitting, move it to `channels.md` with the same headings and add its `## Boxes` line (`memory-template.md`). Budget commitments go to the shared `~/Clawic/data/finances/budget.md`, an agency or freelancer to `~/Clawic/data/contacts/contacts.md`, and a channel post-mortem worth re-reading to `artifacts/channel-<name>-postmortem.md` with its `## Boxes` line.

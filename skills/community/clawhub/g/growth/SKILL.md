---
name: Growth
slug: growth
version: 1.0.2
description: 'Runs growth as a system: finds which funnel stage is the constraint, picks the loop that compounds, and sizes the channel and experiment program. Use when growth stalled or a number has to be hit and nobody can say which stage is broken; when choosing, scaling, or killing acquisition channels; when CAC, payback, LTV:CAC, or blended-versus-paid has to be computed or defended; when signups grow but activation, retention, or paid conversion does not; when designing a referral program, a lifecycle messaging map, or a north-star metric and the events behind it; when forecasting from a model instead of a wish; and for marketplace liquidity, app-install funnels, ecommerce repeat purchase, and self-serve-versus-sales motion. Not for A/B test statistics (`ab-testing`), page-level conversion work (`cro`), churn cohort depth (`churn-analysis`), MRR and NRR definitions (`saas-metrics`), launch positioning (`go-to-market`), or the CGO role and growth-org leadership (`cgo`).'
homepage: https://clawic.com/skills/growth
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📈
    os:
    - linux
    - darwin
    - win32
    displayName: Growth
    configPaths:
    - ~/Clawic/data/growth/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
    - ~/growth/
    - ~/clawic/growth/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/growth/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
      - ~/growth/
      - ~/clawic/growth/
---

**Data.** At the start of every session, read `~/Clawic/data/growth/config.yaml` (what the user declared) and `~/Clawic/data/growth/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/finances/budget.md` before proposing spend, and `~/Clawic/data/projects/` before treating a launch or initiative as new. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a funnel or retention number with its as-of date; a channel started, scaled, or killed with its CAC and payback; an experiment shipped and what it read out; a loop identified or falsified; a metric definition agreed; a target or forecast; a paid budget; a person or agency now involved; or something the user will re-read — a tracking plan, a growth model, an onboarding spec, a referral program, a channel post-mortem. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Shared boxes.** Money goes to `~/Clawic/data/finances/` (`budget.md` for paid spend, `subscriptions.md` for growth tooling), a launch or initiative to `~/Clawic/data/projects/<project>.md`, and any agency, freelancer, partner, or interviewed customer to `~/Clawic/data/contacts/contacts.md` — one row per person, identified by `Key`, updated in place, never a second row. Full protocol and the identity key for each: `memory-template.md`. Growth's own numbers stay in `~/Clawic/data/growth/`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:SEGMENT_WRITE_KEY`, `keychain:meta-ads`, `1password:Work/Analytics/amplitude`. Raw user-level exports carrying emails or names are not credentials but are not memory either: keep the aggregate, drop the rows. If data sits at an old location (`~/growth/` or `~/clawic/growth/`), move it to `~/Clawic/data/growth/`, and say in one line that you moved it and from where.

Growth has one shape: a system with a constraint, and everything else is noise until the constraint moves. Name the constrained stage, size the lift available there in absolute units, and only then choose a tactic. Mode is **advise by default** — produce the model, the number, and the decision the operator executes; act-as (drafting the experiment brief, the tracking plan, the lifecycle map) when the user asks for the artifact itself. Work from defaults immediately: never open with questions about their stage, their stack, or their budget. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale) → the Configuration table default.

## When To Use

- Growth is flat, missed plan, or decelerating, and nobody can name the stage that is responsible
- Choosing, sequencing, scaling, or killing acquisition channels, and defending the CAC and payback behind that call
- Signups rise but activation, retention, revenue, or paid conversion does not follow
- Designing the mechanism: a growth loop, a referral program, a lifecycle messaging map, onboarding to first value
- Defining what gets counted — north star, funnel stages, event taxonomy, the difference between two numbers that both claim to be "conversion"
- Forecasting, target-setting, and allocating a budget across channels and experiments for the next quarter
- Not for the statistics of a single test (`ab-testing`), page-level conversion craft (`cro`), churn cohort depth (`churn-analysis`), MRR/ARR/NRR definitions (`saas-metrics`), or launch positioning and messaging (`go-to-market`) — this decides which of those to spend the quarter on and holds the numbers between them
- Not for the growth **role**: running the growth org, hiring and structuring the team, the exec narrative and board framing go to `cgo`; this file does the work and produces the numbers that role presents

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "Growth is flat" / "we missed the number" | Decompose into the equation, rank stages by absolute lift available, name one constraint | `diagnosis.md` |
| Growing but decelerating, or a channel is fading | Separate saturation, decay, seasonality, and mix shift before touching the channel | `plateaus.md` |
| Two dashboards disagree, or "conversion" means three things | Denominator, window, and cohort anchor — fix the definition before the metric | `instrumentation.md` |
| No events, or events nobody trusts | Tracking plan: names, properties, identity stitching, server versus client | `instrumentation.md` |
| Signups high, nobody reaches value | Find the aha action from retained-versus-churned behaviour, then cut steps before it | `activation.md` |
| Users leave after week one; curve never flattens | Cohort curve shape, natural frequency, resurrection, power-user curve | `retention.md` |
| "Which channel should we try next?" | Portfolio by CAC, volume ceiling, time to signal; two or three live at once with kill numbers | `acquisition.md` |
| Paid spend rising, results not | Incrementality, blended versus paid CAC, creative fatigue, bid and budget mechanics | `paid.md` |
| Needs a mechanism that compounds, not a campaign | Loop selection, k-factor and cycle-time math, why the loop is not closing | `loops.md` |
| Referral program to design or fix | Double-sided incentive, trigger placement, attribution, fraud controls | `referrals.md` |
| Email, push, or in-app messaging program | Lifecycle map by state, not by calendar; frequency ceilings, deliverability, consent | `lifecycle.md` |
| Free users do not convert; pricing or packaging suspected | Paywall placement, trial versus freemium, expansion, discount discipline | `monetization.md` |
| Idea backlog, prioritization, or "the test was inconclusive" | ICE/RICE scoring, sample size before shipping, decision rules, readout format | `experiments.md` |
| A target, a forecast, or a budget to justify | Bottom-up model from loop inputs; sensitivity; what a hiring or spend plan implies | `forecasting.md` |
| Self-serve versus sales motion, PQLs, pipeline | Motion fit by ACV, PQL definition, hand-off rules, hybrid failure modes | `b2b.md` |
| Two-sided marketplace: supply, demand, liquidity, cold start | Liquidity as the real metric, constrained side, geographic seeding, take rate | `marketplaces.md` |
| Mobile app: installs, D1/D7, store listing, attribution | Install-to-value funnel, ATT and SKAN reality, push as retention, store conversion | `mobile.md` |
| Ecommerce: AOV, repeat purchase, cart abandonment | Contribution margin per order, repeat-rate cohorts, replenishment timing | `ecommerce.md` |
| Anything else growth | Ask which stage of the equation it moves and in what unit; if the answer is "awareness", it is not measurable yet — make it a stage first | — |

Coverage map: `diagnosis.md` find the constraint · `instrumentation.md` definitions and events · `activation.md` first value · `retention.md` cohorts and habit · `loops.md` compounding mechanisms · `acquisition.md` channel portfolio · `paid.md` paid media economics · `lifecycle.md` messaging programs · `referrals.md` referral design · `monetization.md` conversion to money · `experiments.md` the test program · `forecasting.md` models and targets · `plateaus.md` stalls and decay · `b2b.md` sales-assisted motion · `marketplaces.md` two-sided · `mobile.md` apps · `ecommerce.md` transactional retail.

## Core Rules

1. **Work the constraint, and prove it in absolute units.** Rank every stage by the lift it can contribute, never by the percentage that looks worst: `lift = upstream_volume × (achievable_rate − current_rate) × downstream_conversion × value_per_conversion`. A 2% → 4% activation on 10,000 signups beats 30% → 45% on a 300-user segment; the second reads better as a percentage and is worth under a quarter as much (`diagnosis.md`).
2. **Retention gates spend.** Acquisition into a curve that never flattens is a leak amplifier: every cohort costs money and leaves. Gate: no step change in paid spend until the cohort curve flattens on two consecutive cohorts at the product's natural frequency (`retention.md`), and pre-PMF the Sean Ellis test reads ≥40% "very disappointed" (`diagnosis.md`).
3. **A rate without its denominator, window, and cohort anchor is not a number.** "Conversion 12%" must resolve to *signups ÷ unique visitors, 7-day window, cohort dated by first touch*. Write the definition down once and reuse it; two teams quoting different definitions is the most common cause of a strategy argument that no data can settle (`instrumentation.md`).
4. **Payback decides scale; LTV:CAC decides whether the business exists.** `payback_months = CAC ÷ (monthly ARPA × gross_margin)`. Example: CAC 300 USD, ARPA 60 USD, margin 0.8 → 300 ÷ 48 = 6.3 months. Scale a channel only when payback ≤ `target_cac_payback_months` **and it holds after a 2× spend increase** — CAC rises with volume in every channel. The 3:1 LTV:CAC heuristic is underwriting shorthand, not a law: it is satisfied by a business that runs out of cash, because it says nothing about when the money comes back (`acquisition.md`).
5. **One loop, named, with its cycle time.** Loops compound, campaigns do not. Output = f(conversion at each step, **cycle time**): halving the time from value to invite beats a 20% lift in invite acceptance, because the exponent is `t ÷ cycle_time` (`loops.md`). A "loop" whose output does not feed its own input is a funnel with better branding.
6. **Two or three channel tests live at once, each with a kill number and a kill date set before the spend starts.** More than three and attribution, team attention, and creative quality all degrade at once; a test without a pre-committed kill number gets extended by whoever championed it (`acquisition.md`).
7. **Pre-register the metric, the horizon, and the sample size before shipping the test.** Fixed-horizon significance is invalid if you stop when it looks good; either commit to the horizon or use a sequential method designed for peeking (`experiments.md`).
8. **Segment before concluding.** An aggregate can move the opposite way to every segment inside it when the mix changes (Simpson's paradox); the standard cuts are acquisition source, plan, platform, geography, and new-versus-existing.
9. **Ship the event with the feature, never after.** An unmeasured change is an unknowable result and a retroactive event cannot backfill history — the cohort that used the feature first is exactly the one you needed (`instrumentation.md`).

## The Growth Equation

Every business decomposes into a chain of multiplications; the decomposition is the analysis. Write the user's chain out with real numbers before any tactic:

| Model | Equation | Where it usually breaks |
|---|---|---|
| Self-serve SaaS | visitors × signup% × activation% × paid-conversion% × (1 ÷ churn) × ARPA | Activation, then paid conversion |
| Sales-assisted B2B | leads × MQL% × SQL% × win% × ACV × (1 + expansion) | SQL definition and win rate; pipeline coverage is usually fiction (`b2b.md`) |
| Marketplace | (supply × listing quality) ∩ (demand × intent) → match% × take_rate × frequency | The constrained side, which is not the one asking for help (`marketplaces.md`) |
| Ecommerce | sessions × conversion% × AOV × contribution_margin% × repeat_rate | Repeat rate; first-order economics rarely work alone (`ecommerce.md`) |
| Consumer app | installs × open% × D1 × D7 × D30 × sessions/user × monetization/session | The install-to-first-value gap (`mobile.md`) |
| Content/media | content × traffic/content × subscribe% × engagement × ad or sub RPM | Traffic per unit decays; production must outrun decay (`loops.md`) |

Two rules for reading the chain: a stage cannot be improved past its ceiling (signup% rarely doubles twice), and the terms multiply — so a 20% gain in two stages beats a 50% gain in one, and is usually cheaper.

## Numbers That Lie

Each of these has survived a board meeting while being wrong. Check the definition before believing the trend.

| Number | How it lies | The honest version |
|---|---|---|
| Signups | Counts intent, not value; grows fastest when quality drops | Activated users, defined by the aha action (`activation.md`) |
| Blended CAC | Divides all spend by all customers, so organic subsidises paid and hides that paid is unprofitable | Paid CAC = paid spend ÷ paid-attributed customers; keep blended only for board-level efficiency (`paid.md`) |
| LTV from a lifetime you have never observed | `ARPA × margin ÷ churn` at 1% monthly churn implies a 100-month life the company has not existed for | Cap the horizon at 24-36 months for planning; state the cap next to the number |
| DAU/MAU | Compares products with different natural frequencies; a tax product at 5% may be healthier than a chat app at 15% | Frequency versus expected frequency for the job (`retention.md`) |
| Aggregate retention "70%" | One number for a curve; hides whether it is flattening or sliding to zero | The curve, by cohort, with the week it flattens |
| Last-touch attribution | Awards the conversion to the last cheap click; brand search harvests demand created elsewhere | Hold-out or geo test for the channels that matter (`paid.md`, `marketing-attribution`) |
| Test "lift" from a stopped-early test | Peeking inflates false positives well past the nominal 5% | Pre-registered horizon, or a sequential method (`experiments.md`) |
| Month-to-date compared to a closed month | Always looks like a collapse on the 8th | Compare like windows; every stored number carries its as-of date |
| A cohort dated by conversion, not by first touch | Moves users between cohorts as they convert, so history rewrites itself monthly | Anchor every cohort on first touch, permanently |

## Stage Gates

What is allowed depends on `stage`; the most expensive growth mistake is running the next stage's playbook. Anything above your stage is a bet, not a plan.

| Stage | Signal you are here | Do | Do not |
|---|---|---|---|
| pre-pmf | Retention curve slides to zero; Sean Ellis <40% | Talk to churned users, change the product, hand-deliver value | Hire growth, buy traffic, build a referral program |
| early | Curve flattens for one segment; one channel works manually | Instrument, define the loop, make the manual channel repeatable | Add channels three and four; automate what you have not done by hand |
| growth | Payback within target on ≥1 channel that survives 2× spend | Scale that channel, run the experiment program, close the loop | Reorganise around channels nobody has proven; ignore the second channel until the first saturates |
| scale | Multiple channels, saturation visible, CAC drifting up | Portfolio management, incrementality tests, expansion revenue, new segments | Read the plateau as a tactics problem (`plateaus.md`) |

## Output Gates

Before delivering a recommendation, a model, or a plan:

- Did I name one constrained stage and size its lift in absolute units, not percentage points (Rule 1)?
- Does every rate I quoted carry its denominator, window, and as-of date (Rule 3)?
- Did I check the stored funnel, channel, and retention history before calling anything new or unprecedented?
- Is the spend recommendation gated on retention evidence and on payback surviving a 2× spend increase (Rules 2, 4)?
- Does each proposed test have a metric, a horizon, a sample size, and a kill number decided in advance (Rules 6, 7)?
- Is this a loop or a campaign, and did I say which?
- Did anything durable come out of this — a number, a channel result, an experiment readout, a definition, a target, an artifact? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/growth/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| business_model | saas \| marketplace \| ecommerce \| consumer-app \| b2b-sales \| media | saas | Selects the row of The Growth Equation, the model-specific file to open, and which base rates apply |
| motion | self-serve \| sales-assisted \| hybrid | self-serve | Whether guidance runs through PQLs and pipeline (`b2b.md`) or self-serve activation and paywalls (`activation.md`, `monetization.md`) |
| stage | pre-pmf \| early \| growth \| scale | early | Which row of Stage Gates governs; blocks the plays reserved for later stages |
| north_star | text | none | The metric every recommendation is tied back to; unset means state the assumed one before advising (`diagnosis.md`) |
| target_cac_payback_months | number (months, 1-36) | 12 | The bar in Rule 4 for scaling a channel and the constraint in `forecasting.md` |
| monthly_paid_budget | number (currency from `profile.yaml`) | 0 | Sizes channel tests in `acquisition.md` and `paid.md`; 0 means organic-only plays are proposed first |
| analytics_stack | ga4 \| amplitude \| mixpanel \| posthog \| warehouse \| none | none | Which tool the tracking plan and event examples are written against (`instrumentation.md`) |
| experiment_confidence | 90 \| 95 \| 99 | 95 | The confidence level in every sample-size calculation and readout (`experiments.md`) |
| reporting_cadence | weekly \| biweekly \| monthly | weekly | The review row in the `## Due` table and how often numbers are refreshed |
| privacy_regime | none \| gdpr \| ccpa \| both | none | Consent, tracking, retargeting and email opt-in constraints applied in `instrumentation.md` and `lifecycle.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — analytics, ESP, experiment platform, CDP, attribution tool, warehouse-versus-product-analytics — affects every example and where a definition physically lives
- **Conventions** — event naming (`object_action`, snake_case), UTM taxonomy, experiment and campaign naming, cohort anchor — affects `instrumentation.md` and every readout
- **Platform** — geographies and locales sold to, app stores in play, seasonality shape of the business, currency — affects channel availability and forecast shape
- **Risk posture** — tactics that are off the table (incentivized installs, dark-pattern cancellation, aggressive discounting, buying lists), tolerance for brand risk in creative — affects `acquisition.md`, `paid.md`, `lifecycle.md`
- **Constraints and exclusions** — banned channels, competitor-bidding policy, compliance regime beyond privacy, brand guidelines that gate creative volume
- **Work order** — research before test versus ship-and-learn, review gates before spend, who signs off a kill decision
- **Output format** — memo versus deck versus dashboard, how much model detail to show, whether every answer carries a number
- **Cadence** — growth review, cohort refresh, channel audit, experiment readout, budget re-plan — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Scaling acquisition while retention slides | Every cohort costs money and leaves; the bill arrives one payback period later | Gate spend on curve flattening (Rule 2, `retention.md`) |
| Copying a competitor's tactic | You see the tactic, not their constraint, their margin, or their loop — the same tactic on a different constraint is noise | Decompose your own equation first (`diagnosis.md`) |
| Ten experiments at once on the same surface | Interaction effects and split traffic; nothing reaches sample size and nothing is attributable | Sequence by ICE, one owner per surface, sample-size check before shipping (`experiments.md`) |
| Optimising a percentage on a tiny base | The best-looking uplift on the smallest segment | Rank by absolute lift (Rule 1) |
| Declaring a channel dead in a week | Learning periods, creative iteration and delayed conversion mean early CAC is always the worst CAC | Kill on the pre-committed number and date, measured over one full conversion cycle (`acquisition.md`) |
| A referral program before anyone loves the product | Incentives buy sign-ups from people with nothing to say; fraud arrives before advocacy | Referral only once retention flattens and NPS/advocacy exists (`referrals.md`) |
| Discounting to hit the quarter | Trains the market to wait, damages LTV in the same cohort you are measuring | Fix packaging or the value moment (`monetization.md`) |
| Vanity dashboard with 40 tiles | Nobody can name the constraint from it, so meetings become metric archaeology | Equation on one screen, one number per stage, everything else on request |
| "Awareness" as a growth stage | No denominator, no window, no decision it changes | Convert it to a measurable stage or drop it from the model |
| Rebuilding onboarding without knowing the aha action | Redesign changes the order of steps that never mattered | Derive the action from retained-versus-churned behaviour first (`activation.md`) |
| A definition that lives only in someone's head | Re-litigated every quarter; last quarter's numbers become unreproducible | `artifacts/metric-definitions.md` with its `## Boxes` line (`instrumentation.md`) |
| Treating a seasonal dip as a stall | Triggers a reorganisation in the month the business always dips | Compare year-over-year and to the same week last cycle (`plateaus.md`) |

## Where Experts Disagree

- **North star: one metric or a small tree.** A single metric aligns a team and gets gamed; a tree of three resists gaming and dilutes focus. The frontier is team size — under ~20 people one metric wins, past that a tree with one owner per branch survives contact with functional teams.
- **Paid before or after organic.** Paid buys learning speed at known cost and can validate a value proposition in two weeks; it also masks a broken loop for as long as the money lasts. Boundary: paid to *test messaging and demand*, never to *test retention* — that answer arrives only from cohorts you did not pay to be enthusiastic.
- **Attribution model.** Practitioners split between multi-touch models (granular, unfalsifiable) and hold-out/geo incrementality tests (coarse, causal, expensive). The frontier is spend: below a level where a hold-out is affordable, use last-touch and know it flatters harvest channels (`paid.md`, `marketing-attribution`).
- **Growth team shape.** Centralised growth teams ship faster and own the funnel end-to-end; embedded growth engineers get deeper product changes and less territorial friction. Centralised wins while the constraint is in acquisition and activation; embedded wins once it moves into the core product experience.
- **Freemium versus free trial.** Freemium builds a loop and a support burden; trials convert faster and harvest fewer users. Decide on marginal cost per free user and on whether free users create value for paid ones (`monetization.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/growth (install if the user confirms):
- `ab-testing` — sample sizing, randomization units, and the statistics of a single test
- `cro` — page-level conversion craft once the constrained stage is a page
- `retention` — depth on cohort analysis, churn prevention, and reactivation
- `saas-metrics` — canonical MRR, ARR, NRR, and rule-of-40 definitions
- `go-to-market` — positioning, sequencing, and launch playbooks for a new product

## Feedback

- If useful, star it: https://clawic.com/skills/growth
- Latest version: https://clawic.com/skills/growth

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/growth.

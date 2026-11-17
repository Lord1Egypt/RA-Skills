---
name: Pricing
slug: pricing
version: 1.0.2
description: 'Sets, tests, and changes prices: value metric, tier packaging, discounts, price increases, and willingness-to-pay research. Use when deciding what to charge for a new product, when nobody knows what it is worth, when a raise is overdue but churn is feared, when every deal closes at a discount, when the free plan never converts, when a competitor undercuts, when choosing per-seat versus usage-based versus flat, when designing a pricing page, when quoting an enterprise deal or a day rate, when entering a new country or currency, or when setting a marketplace take rate. Covers Van Westendorp and conjoint research, grandfathering, annual prepay maths, price tests, and auto-renewal and price-display rules. Not for consumer buying decisions (`price`), indie launch sequencing and revenue mix (`monetize`), building the billing system (`billing`), CAC and LTV decomposition (`unit-economics`), or company financial models (`cfo`).'
homepage: https://clawic.com/skills/pricing
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💰
    os:
    - linux
    - darwin
    - win32
    displayName: Pricing
    configPaths:
    - ~/Clawic/data/pricing/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/pricing/
    - ~/clawic/pricing/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/pricing/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/pricing/
      - ~/clawic/pricing/
---

**Data.** At the start of every session, read `~/Clawic/data/pricing/config.yaml` (what the user declared) and `~/Clawic/data/pricing/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/pricing/price-book.md` before quoting, discounting, or changing anything: it is what the user charges today, and a number invented next to it is worse than no number. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a price set or changed; a discount granted outside policy; a competitor price observed with the date it was seen; a willingness-to-pay study and its range; a price test and what it decided; a packaging or value-metric decision and what was rejected; a cost or margin input that took work to establish; a grandfathered cohort and when it expires; or something the user will read again — a price book, a discount policy, a change plan, a rate card. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and projects go to the shared boxes**, not here. A customer, prospect, or interviewee named in a deal or a study goes to `~/Clawic/data/contacts/contacts.md`; a repricing run as a piece of work goes to `~/Clawic/data/projects/<project>.md`. Pricing rows reference them by name only — duplicating the person or the project is the most common way two skills start contradicting each other. Both formats, with their identity keys and scale cuts, travel inside `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted contract, billing export, or admin screenshot is dense in them. Store the pointer and strip the value: `env:STRIPE_SECRET_KEY`, `keychain:paddle-admin`, `1password:Work/Billing/live`. If data sits at an old location (`~/pricing/` or `~/clawic/pricing/`), move it to `~/Clawic/data/pricing/`, and say in one line that you moved it and from where.

Price is the fastest lever a business has and the one most often set by feeling. Every answer carries a number, its currency, and what it assumes: which value metric is being charged, what margin survives the discount, and how many customers can leave before the move loses money. Work from defaults immediately: never open with questions about their model, their margin, or how aggressive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- Setting a price for the first time: value metric, packaging, tiers, the number itself
- Changing a price: raises, cuts, repackaging, migrating or grandfathering existing customers
- Discounting that has stopped being deliberate — approval ladders, floors, annual prepay, enterprise deals
- Monetization shape: freemium, trials, usage-based, hybrid commit-plus-overage, marketplace take rate
- Research and testing: willingness-to-pay studies, price experiments, competitor price tracking, win/loss on price
- Presentation and jurisdiction: pricing pages, currency and tax display, auto-renewal and prior-price rules
- Mode: **advise** — this produces the price, the plan, and the artifact; a human sends it and a human changes the live system. Not for consumer buying decisions (`price`), launch sequencing and revenue mix for an indie product (`monetize`), implementing the charge (`billing`), or company-level financial models (`cfo`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "We have no idea what to charge" | Value metric first, then research sized to the decision — never a competitor's number copied | `value-metric.md`, `research.md` |
| Price feels low; nobody ever objects | No objections means the price sits under the market's tolerance (→ Signals) | `elasticity.md` |
| Raising prices with customers already on the old one | Break-even volume loss (Rule 2), then cohort sequence, notice period, save ladder | `price-increase.md` |
| Every deal closes at a discount | List price or fences are wrong; fix those before the ladder becomes the price | `discounting.md` |
| Designing or rebuilding the tiers | Fences a segment self-selects into, one anchor, meaningful gaps | `packaging.md` |
| Per-seat, usage, flat, or hybrid | Decide by how value scales and how predictable the bill must be | `value-metric.md` |
| Metering, credits, overage, commits, surprise bills | Commit-to-overage spread, soft caps, 80% alerts, true-up cadence | `usage-based.md` |
| Free plan or trial that does not convert | The limit must bite on success, not on setup; free-user cost ceiling | `freemium.md` |
| Enterprise quote, procurement, MSA, multi-year | Floor, walk-away, uplift clause, and what you get back for the discount | `enterprise.md` |
| Pricing page, tier labels, toggles, currency selector | Anchor order, annual default, what to show and what to withhold | `pricing-page.md` |
| Running a price experiment | Cohort or geo, revenue per visitor, a full billing cycle before reading | `testing.md` |
| Willingness-to-pay research | Van Westendorp for a range, Gabor-Granger for a point, conjoint for trade-offs | `research.md` |
| New country, currency, VAT or sales tax | Bands not spot conversion, inclusive display where required, arbitrage limits | `international.md` |
| Consulting, agency, or freelance rate | Day rate from billable capacity, then fixed scope, then value | `services.md` |
| Physical goods, retail, MAP, markdowns | Cost-plus floor, keystone reality, markdown cadence, promo depth | `retail.md` |
| Marketplace take rate, who pays, which side is subsidized | Take rate must cover payments, trust, and both sides' acquisition | `marketplace.md` |
| Competitor moved, or a buyer quotes their price | Reference price plus differentiation value; match only what your cost base allows | `elasticity.md` |
| Auto-renewal, "was" prices, fees at checkout, personalized prices | The disclosure and notice rules that make a legal price unlawful in presentation | `compliance.md` |
| Anything else pricing | Name the value metric, give the number with currency and term, and state the break-even volume change (Rule 2) | — |

Coverage map: `value-metric.md` what you charge for · `packaging.md` tiers and fences · `research.md` willingness to pay · `elasticity.md` the maths of moving a price · `price-increase.md` executing a raise · `discounting.md` discipline and approval · `usage-based.md` metering and commits · `freemium.md` free tiers and trials · `enterprise.md` sales-led deals · `services.md` rates for time and scope · `retail.md` physical goods · `marketplace.md` two-sided take rate · `international.md` currency, PPP, tax · `testing.md` price experiments · `pricing-page.md` presentation · `compliance.md` the rules that bind.

## Core Rules

1. **Charge for the thing that grows when the customer wins.** A value metric qualifies on three counts: it rises with the value they get, they can forecast it well enough to budget, and they can count it without opening your dashboard. Test: if a customer's use of the product doubles and their invoice does not move, the metric is wrong and every later decision inherits that error (`value-metric.md`).
2. **Every price move is a volume bet with an exact break-even.** At contribution margin `m` (as a fraction of price), a rise of `x` survives a volume loss up to `x / (m + x)`; a cut of `d` needs a volume gain of `d / (m − d)` just to stand still. Worked: at 70% margin, +10% price can lose 12.5% of units before profit falls; −10% price needs +16.7% units to break even. State this number before recommending the move, not after.
3. **A discount is a share of margin, not a share of price.** Gross profit lost = `discount% ÷ margin%`. At 70% margin, 20% off removes 28.6% of the gross profit on that deal. Every discount buys something back — a longer term, prepayment, a reference, a volume commitment, a scope reduction — or it is a permanent price cut delivered slowly (`discounting.md`).
4. **Research narrows the range; behavior sets the price.** Van Westendorp returns a band, not a number. Gabor-Granger returns a revenue-maximizing point on the ladder you chose. Conjoint returns trade-offs between features and price. None of them outrank what people actually paid: win/loss reasons, discount depth at close, and renewal behavior are the highest-grade evidence available. Never ask "would you pay $X" — stated intent runs well above purchase behavior, and one accepted quote is worth a hundred agreeable answers (`research.md`).
5. **Three public tiers, each fence something one segment cannot live without.** A fourth tier adds a comparison the buyer has to resolve before they can act; "Enterprise — contact us" is a door, not a tier. A fence is a capability a segment must have (seats, SSO, audit log, SLA, support response, data retention) and the cheaper segment genuinely does not want. Gaps of "more of the same" do not move anyone up (`packaging.md`).
6. **Never emit a price without currency, tax treatment, term, and effective date.** `49 USD/user/month, excl. VAT, annual term, effective 2026-09-01` is a price; `$49` is a rumor. Amounts written to any box carry their currency in the value, because the box is shared with prices from other markets and someone will add the column up.
7. **Raise on new logos first, then cohorts, with the churn budget computed in advance.** Sequence: new customers → renewals → existing customers on notice. The budget is Rule 2 applied to the cohort's revenue; if the raise cannot survive its own break-even loss, it is a repackaging problem, not a pricing one. Grandfathering follows `grandfather_policy`, is stated in writing, and gets an expiry date recorded, or it becomes permanent by accident (`price-increase.md`).
8. **A price test that cannot be honored is not a test.** Different prices to the same shopper on the same page is the version that generates complaints and screenshots; cohort, geography, and new-traffic splits are the versions that survive contact with customers. Whatever price was displayed gets honored. Read the result on revenue per visitor after a full billing cycle plus the refund window, never on day-three conversion (`testing.md`).
9. **Write the price, the reason, and the outcome, or the next repricing starts from zero.** A price with no recorded rationale gets re-litigated every quarter by whoever is newest. The change, the cohort, the observed churn at 30/60/90 days, and the decision it produced go to their boxes in the same turn (`memory-template.md`).

## The Arithmetic

Everything here is derivable; the point is to run it before the recommendation, not to defend the recommendation afterwards. `m` = contribution margin as a fraction of price.

| Question | Formula | Worked |
|---|---|---|
| How much volume can a price rise cost me? | `x / (m + x)` | +10% at m=0.70 → up to 12.5% of units can leave before profit falls |
| How much volume must a cut win back? | `d / (m − d)` | −10% at m=0.70 → +16.7% units needed just to stand still |
| What does a discount cost in profit? | `discount% ÷ margin%` | 20% off at 70% margin → 28.6% of that deal's gross profit |
| Is annual prepay worth two months free? | 12 × (1 − d) vs expected months paid, where expected months in a year at monthly churn `c` = `(1 − (1 − c)^12) / c` | d = 16.7% → break-even near 3% monthly logo churn; above it, annual prepay wins on cash and on retention |
| Can the free tier pay for itself? | monthly cost per free user ≤ `r × m$ × L` | 1%/month conversion, 20 USD monthly contribution, 24-month life → ceiling of 4.80 USD per free user per month |
| What does the processor take on a small ticket? | `(rate × p + fixed) / p` | 2.9% + 0.30 USD on a 5 USD charge = 8.9%; on 50 USD = 3.5% — the fixed fee is the whole argument for bundling and annual billing |
| What day rate clears my target? | `income × (1 + overhead) / (working days × utilization)` | 120k target, 30% overhead, 220 days, 60% utilization → 156,000 / 132 ≈ 1,180 per day |
| Is this price above the floor? | contribution = `price − variable cost`; floor = `variable cost / (1 − target_gross_margin_pct)` | 30 USD variable cost at a 70% margin target → floor of 100 USD; below it, volume is something you are paying for |
| What must a marketplace take rate cover? | `take × GMV per transaction ≥ payments + trust/support + blended CAC of both sides ÷ transactions per cohort` | Thin GMV per transaction is why low take rates only work at high repeat frequency (`marketplace.md`) |

## Signals

Pricing symptoms are diagnostic: each one names a different link in the chain — value metric → package → list price → discount → billing.

| Symptom | Most likely cause | First move |
|---|---|---|
| Nobody ever pushes back on price | Priced under the market's tolerance; the buyer is being funded | Test a raise on new logos only (`price-increase.md`) |
| Every deal needs a discount to close | List price is aspirational, or the fences do not match how segments actually differ | Rebuild fences and the approval ladder before touching list (`packaging.md`, `discounting.md`) |
| Win rate high, deal sizes flat as customers grow | Value metric does not scale with value | Re-pick the metric; migrate on renewal (`value-metric.md`) |
| Churn concentrated at first renewal | The price was accepted and the value was not delivered by month 12 | An activation problem — repricing will not fix it |
| Churn spike immediately after a price change | The execution, not the number: notice period, grandfathering, or how it was announced | The cohort sequence and comms in `price-increase.md` |
| Small accounts pay more per unit than large ones by accident | Discount authority leaked into the field | Discount audit against policy; publish the volume schedule (`discounting.md`) |
| Free users never hit the limit | The fence sits on a dimension a happy user never touches | Move the limit onto the success path (`freemium.md`) |
| Revenue flat while usage climbs | Flat fee on a usage-shaped product | Platform fee plus metered component (`usage-based.md`) |
| Support spikes at the end of every billing period | Uncapped overage | Soft cap, 80% alert, and a commit tier that is cheaper than the overage (`usage-based.md`) |
| Buyers keep saying "X charges less" | Reference-price problem, not a value problem | Quantify the differentiation value against their reference (`elasticity.md`) |
| A test showed a lift, then revenue fell | Read before the billing cycle and the refund window closed | Re-read at 90 days with churn included (`testing.md`) |
| Enterprise deals stall in procurement, never in evaluation | Terms, not price: uplift caps, MFN, payment schedule | `enterprise.md` |
| Anything else | Locate the symptom in the chain above, then take the matching row of Quick Reference | — |

## Legal Tripwires

Observable signals that stop the pricing work and route it to counsel. The thresholds are the content; the specific rule varies by jurisdiction and is checked, not assumed (`compliance.md`).

| Signal | Risk | Action |
|---|---|---|
| Any exchange with a competitor about prices, discounts, or who bids what | Price fixing — no minimum company size, and criminal in many jurisdictions | Stop the conversation; preserve the message, the date, and who was present in `artifacts/compliance-<market>.md`; tell counsel |
| A reseller contract that dictates the price they may sell at | Resale price maintenance; per se unlawful in several jurisdictions | Advertised-price policy applied unilaterally is the usual lawful shape (`retail.md`) |
| A customer asking for a most-favored-nation clause | Freezes your ability to price anyone else better, indefinitely | Refuse, or cap it by scope and term (`enterprise.md`) |
| Different prices to resellers who compete with each other | Price-discrimination exposure between trade buyers | Publish the volume schedule and apply it mechanically |
| Prices that vary per individual from automated profiling | Consumer disclosure duties attach to personalized pricing | Disclose, or segment by plan and geography instead of by person |
| A "was" price, a countdown, or a fee that appears at checkout | Prior-price and all-in-pricing rules; regulators act on presentation alone | Clear it in `compliance.md` before the page ships |

## Output Gates

Before delivering a price, a plan, or a page:

- Does every number carry currency, tax treatment, term, and effective date (Rule 6)?
- Did I state the break-even volume change for the move I recommended (Rule 2)?
- Does any discount name what came back in return, and clear the floor from `target_gross_margin_pct` (Rule 3)?
- Is the treatment of existing customers explicit — grandfathered until a stated date, migrated at renewal, or moved now?
- Did I read `price-book.md` first, so the advice is against what they actually charge rather than what I assumed?
- Is anything here a Legal Tripwire?
- Did anything durable come out of this — a price, an out-of-policy discount, a competitor observation, a study, a test result, a decision and what it rejected? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/pricing/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| business_model | saas-subscription \| usage-based \| one-time \| marketplace \| services \| physical-goods | saas-subscription | Which guide is authoritative and which value metrics are even candidates (`value-metric.md`) |
| currency | text (ISO 4217) | `profile.yaml`, else USD | Currency of every price, floor, and quote, and the code written into every stored amount (Rule 6) |
| target_gross_margin_pct | number (0-100) | 70 | The `m` in every Arithmetic row, and the floor a cost-plus price or a discount must clear |
| discount_floor_pct | number (0-100) | 20 | Largest discount emitted without routing to the approval ladder in `discounting.md` |
| annual_discount_pct | number (0-100) | 17 | The monthly-to-annual prepay discount used in every plan table (two months free = 16.7%) |
| grandfather_policy | forever \| fixed-term \| next-renewal \| none | next-renewal | How every price-increase plan treats existing customers, and what expiry date gets recorded (Rule 7) |
| price_endings | charm \| round \| whole | charm | The final digits of every price emitted: 49 vs 50 vs 47 (`pricing-page.md`) |
| tax_display | exclusive \| inclusive | exclusive | Whether quoted prices include VAT/GST; consumer selling in several markets requires inclusive (`international.md`) |
| price_review_cadence | quarter \| half \| year \| none | year | The row written into `## Due`, and how often a full review is proposed unprompted |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — billing platform and whether it is a merchant of record, survey and conjoint tooling, analytics source for cohort reads — affects what a migration can actually execute (`price-increase.md`, `international.md`)
- **Conventions** — tier names, SKU and plan naming, how prices are written in copy, seat versus "editor" versus "member" vocabulary — affects every table and page produced
- **Platform** — markets and countries sold into, purchasing-power posture, payment methods offered, self-serve versus sales-led — affects `international.md` and `pricing-page.md`
- **Risk posture** — appetite for testing on live traffic, willingness to lose customers to a raise, whether discounts are permitted at all, floor rigidity — affects Output Gates, `testing.md`, `discounting.md`
- **Output register** — one number versus a range, table versus deck versus memo, how much of the derivation to show — affects the shape of every answer
- **Cadence** — competitor sweep, discount audit, post-change churn checkpoints, research refresh — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Constraints** — channel and advertised-price obligations, investor or board commitments about revenue shape, contractual price protection already given, data covered by an NDA — affects what may be proposed at all

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Cost-plus pricing on software | Marginal cost is near zero, so the method returns a number unrelated to value and usually far too low | Value metric plus a researched range; cost only sets the floor (Rule 1, `value-metric.md`) |
| Matching a competitor's price | Their price encodes their cost base, funding, and segment, none of which you have | Reference price plus quantified differentiation value (`elasticity.md`) |
| A flat percentage raise "across the board" | The cohorts differ in tolerance, and the most valuable ones absorb the least attention | Segment the raise, sequence it, budget the churn (Rule 7) |
| Grandfathering with no end date | The legacy plan becomes a permanent second product with its own support cost and its own migration project later | Fixed term with the expiry recorded in `## Price History` (`price-increase.md`) |
| Discounting to close the quarter | Teaches every buyer to wait for the last week, permanently | Trade the discount for term, prepay, or scope; hold the floor (`discounting.md`) |
| Deep annual discounts to "lock people in" | Past roughly two months free, the discount usually exceeds the churn it prevents | Run the prepay break-even (→ The Arithmetic) before setting `annual_discount_pct` |
| Per-seat pricing on a product used by one person per company | Revenue caps out on day one regardless of the value delivered | Pick a metric that grows (`value-metric.md`) |
| A free tier generous enough to be the product | Conversion never happens because nothing ever hurts | Limit on the success path; check the free-user cost ceiling (`freemium.md`) |
| Uncapped usage pricing with no alerts | The first surprise invoice ends the account, and the customer tells other buyers | Soft cap, 80% alert, commit tier below the overage rate (`usage-based.md`) |
| Reading a price test on conversion rate | A cheaper price converts better and can still earn less | Revenue per visitor over a full billing cycle, churn at 90 days (Rule 8) |
| Same-page A/B on identical shoppers | Screenshots travel; the trust cost outlives the learning | Cohort, geo, or new-traffic splits, price honored either way (`testing.md`) |
| Converting prices at the spot rate for a new country | Produces prices like 47.13 and ignores purchasing power and local expectations | Country bands with local rounding (`international.md`) |
| Removing a feature people already pay for to build a higher tier | Reads as a price rise plus a downgrade, and it is the version customers post about | Gate new capability upward; leave the existing entitlement intact (`packaging.md`) |
| A pricing decision that lives only in the chat | Re-argued every quarter, and the rejected options get re-proposed by name | `artifacts/` with the date, the rationale, and what was rejected (`memory-template.md`) |

## Where Experts Disagree

- **Public prices vs "contact sales".** Public pricing shortens the funnel and screens out mismatched buyers; hiding it protects negotiating room and per-customer differentiation. The frontier is deal size and variance: when ACV is small or scope is uniform, publish; when scope varies enough that a list price would be wrong for most buyers, publish a starting point and route the rest (`pricing-page.md`).
- **Grandfather forever vs migrate everyone.** Migrating everyone maximizes revenue per customer and produces one loud, bounded churn event; grandfathering preserves goodwill and creates a permanent second product. The deciding question is whether the old plan is *operationally* free to keep — the moment it needs its own code path, the goodwill has a running cost.
- **Usage-based vs seats.** Usage aligns price with value and grows without a sales conversation, at the cost of forecastability for the buyer and for you. Seats are predictable and easy to procure, and detach from value in exactly the products where value is not human-hours. Hybrid — a platform fee plus metered usage — is the default when neither side can accept the other's risk (`usage-based.md`).
- **Freemium vs free trial.** Freemium buys distribution and pays for it in support and infrastructure on users who never convert; trials qualify harder and lose the users who need more than two weeks. Product complexity is the frontier: if time-to-value is longer than a trial, freemium or a reverse trial is the only honest option (`freemium.md`).
- **How much research is enough before launch.** One school ships a price, watches win/loss, and iterates quarterly; the other studies before committing because a launch price anchors the market and raising later is harder than starting high. Reconciliation used here: research the *range* rather than the point, launch at the upper end of it, and use discounts as the downward adjustment you can withdraw (`research.md`).

## Security & Privacy

**Credentials:** this skill never stores, logs, copies, or transmits a payment-processor key, a billing-platform login, or an unpublished discount code, and never writes one into `~/Clawic/data/`. Secrets in anything the user pastes are replaced by a `<kind>:<locator>` pointer before the text is written (`memory-template.md`).

**Local storage:** preferences, price book, competitor observations, deal history, research runs and generated artifacts stay in `~/Clawic/data/pricing/` on this machine, plus people in the shared `~/Clawic/data/contacts/` and work in `~/Clawic/data/projects/`. Prices, terms, margins and company names only.

**Guardrails:** this skill does not change a live price, cancel a subscription, or send a customer communication. It produces the number, the plan, and the artifact; a human executes them.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/pricing (install if the user confirms):
- `unit-economics` — CAC, LTV, payback, and contribution margin, the inputs `m` comes from
- `saas-metrics` — MRR, ARR, NRR, and churn definitions that keep a price change measurable
- `negotiate` — the deal conversation itself, once the floor and the trade list exist
- `billing` — implementing the charge: subscriptions, proration, invoices, webhooks, tax
- `cfo` — the company financial model a pricing change feeds into

## Feedback

- If useful, star it: https://clawic.com/skills/pricing
- Latest version: https://clawic.com/skills/pricing

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/pricing.

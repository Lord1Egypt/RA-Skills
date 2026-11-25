---
name: pricelens-cn
display_name: PriceLens 比价智选
display_name_en: PriceLens — Price Intelligence & Purchase Decision
description_en: >-
  Given a category and a budget, PriceLens delivers a landed-price range with a
  traceable evidence chain, a channel trust comparison, a spec trade-off matrix
  and a quantified buy / wait / switch verdict in one decision report.
version: 1.0.0
category: life-service
sub_categories:
  - key: pro-shopping
    name: 消费决策
tags: [比价, 到手价拆解, 渠道对比, 参数取舍, 购买决策, 价格取证]
tags_en: [price-comparison, landed-price, channel-matrix, spec-tradeoff, purchase-decision, price-evidence]
icon: 🔍
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [比价, 到手价, 值得买吗, 买还是等, 渠道对比, 选购建议, 参数取舍, 价格调研, 历史低价, 以旧换新划算吗, 预算内推荐, 决策报告]
trigger_keywords_en: [price comparison, landed price, worth buying, buy or wait, channel comparison, buying advice, spec trade-off, price research, historical low, trade-in]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "1.99"
---

# PriceLens — Price Intelligence & Purchase Decision

PriceLens turns "should I buy this" into six concrete steps — clarify constraints, collect price evidence, decompose the landed price, grade channels, weigh specs, and issue a quantified buy / wait / switch verdict — and returns one auditable decision report.

## What This Is

- **The problem it solves.** Most people buy off the sticker price. They do not know the real landed price, which channel can actually deliver, how much trust a cheaper seller deserves, which spec is worth paying for, or whether waiting six weeks would save more than it costs.
- **What you get.** One Markdown file, `pricelens-<category>-<YYYYMMDD>.md`, with six fixed blocks: verdict card, landed-price table, channel matrix, spec trade-off matrix, buy / wait / switch ruling, and an evidence log with open items.
- **How it differs from asking a general model.** Every price carries a source type, a retrieval date and a verification status; no number enters the report without one. The sticker price is always decomposed into a landed price. The output must be one of three verdicts with an executable trigger, never "it depends on your needs." When evidence is missing, PriceLens downgrades to a range or states that it cannot price the item, and never fills the gap with invented figures.
- **Where it stops.** It works on describable physical goods and subscriptions. For single high-value second-hand items, jewellery, watches and vehicles that need physical inspection, it provides screening criteria and an inspection checklist, not a price verdict.

## When to Use It

- "I want to replace my [category] with a budget of [amount]. Which one, and what counts as a good price?"
- "The same unit differs by several hundred across channels. What is the difference, and is the cheap one safe?"
- "The sticker and the checkout price are miles apart. What does it actually cost once coupons, rebates, shipping and trade-in are counted?"
- "Two models trade wins on different specs. Which spec should I pay extra for?"
- "Buy now or wait for the sales? If I wait, at what price do I pull the trigger?"
- "What is my old unit worth, and is trade-in better than selling it myself?"
- "This channel is twenty percent cheaper than the official store. Is it genuine, and who honours the warranty?"
- "Turn the conclusion into a one-pager I can show someone who does not follow specs."

## When NOT to Use

- Real-time prices or auto-purchase: this skill reasons over a supplied snapshot only.
- Guarantees of "lowest price anywhere": only relative ranking within verifiable evidence.
- Regulatory eligibility for drugs, devices or cross-border goods: flag risk, do not decide.
- Evidence with no screenshot or timestamp: output "cannot judge" instead of guessing.

## Quick Reference

| Situation | Use |
|---|---|
| Scattered screenshots | `references/price-evidence-chain.md` |
| Same item, very different channels | `references/channel-matrix.md` |
| Is this price worth it | `references/value-scoring.md` |
| One-page decision memo | `references/decision-report.md` |

## Inputs and Outputs

**Inputs**

| Field | Required | Notes |
|---|---|---|
| Category | Yes | Must be specific enough to compare, e.g. "robot vacuum, self-emptying" rather than "appliances" |
| Budget | Yes | A ceiling or a range, stated as landed price or sticker price; landed price is assumed |
| Three must-have specs | Yes | Exactly three, ranked by importance; they set the weights in the trade-off matrix and must be measurable |
| Usage context | No | Room size, installation constraints, household size, frequency |
| Existing unit | No | Model, year, condition, resale status; feeds the trade-in and switch branches |
| Channel preferences | No | For example official-only, no second-hand, invoice required |
| Time window | No | Latest acceptable date, which decides whether waiting is viable |
| Output preference | No | Verdict card only, full report, or report plus one-pager |

**Output**

- A single Markdown file named `pricelens-<category>-<YYYYMMDD>.md`, dated by retrieval day.
- Six blocks in a fixed order: verdict card (150 characters or fewer, above the fold), landed-price table (3–6 rows), channel matrix (4–8 rows), spec trade-off matrix (2–4 candidates against 3 specs), buy / wait / switch ruling with triggers, and the evidence log with open items.
- 900–1800 characters of body text including tables; English terms glossed on first use.
- The first line carries the retrieval date plus a re-check notice; the canonical wording is "prices were captured at the time of retrieval and must be re-checked".

## Workflow

### Step 1 — Clarify the request (three mandatory answers)

- **Do.** Collapse the request into computable inputs: the category down to its form factor, the budget converted to a landed-price basis, and exactly three ranked must-have specs. The three specs drive every later weight and must be confirmed by the user, not chosen by the skill.
- **Pass when.** Each spec is measurable (`noise at or below N dB`, `climbing height at least N mm`, `annual consumable cost at or below N`). Words like "quiet", "durable" or "good looking" are rejected.
- **If it fails.** Offer the two dominant form factors at the mainstream price band and ask the user to pick one; do not assume. If the user still declines, use the category's three conventional specs, and mark them in the report as defaults.

### Step 2 — Collect price evidence (multi-source)

- **Do.** Gather evidence across the four source types in `references/price-evidence-chain.md`: search-result snippets, vertical retailer sites, brand specification pages, and content platforms (reviews, purchase posts, historical deal posts). Cover at least three source types per candidate and at least two independent sources per SKU.
- **Pass when.** Two sources for the same SKU land within 15 percent of each other; that counts as converged and a point value is allowed. A gap above 15 percent must be attributed (bundle, configuration, gift, tax, shipping basis). If it cannot be attributed, keep the two figures apart rather than averaging.
- **If it fails.** When every source is blocked or login-gated, downgrade to a range plus an open-items list, state on the first line that no cross-checked point value was obtained, and never substitute a guess. A single source may enter the open-items list, never the verdict card.

### Step 3 — Decompose the landed price

- **Do.** Apply the items in order, one row each: sticker price, minus product coupon, minus platform coupon and threshold discount, plus shipping, plus installation and extended warranty, minus rebate, minus trade-in resale value, minus trade-in subsidy, minus gift valuation.
- **Pass when.** Every line states its basis, its settlement timing and its verification status (verified, unverified, or a range). Rebates are computed on the amount actually paid and marked with their payout delay. Trade-in resale value and trade-in subsidy are separate lines, so a subsidy is never presented as a discount.
- **If it fails.** When a rule cannot be read (coupon threshold, rebate rate, subsidy eligibility), mark that line unverified, give a range, and exclude it from the point value. If unverified items could exceed five percent of the landed price, the verdict card must use a range.

### Step 4 — Grade channel trust

- **Do.** Assign a tier from `references/channel-matrix.md`: T1 brand-owned or platform-owned retail; T2 authorised dealer or category specialist; T3 third-party marketplace seller with adequate standing, returns cover and an authorisation statement; T4 second-hand, cross-border or invoice-free.
- **Pass when.** The tier rests on observable signals — who issues the invoice, whether an authorisation is verifiable, the return terms, service coverage, trading history — never on how cheap the listing is. Only T3 and above may enter the buy candidate pool.
- **If it fails.** Drop one tier when the invoicing entity cannot be confirmed. If a T4 channel is still under consideration, the report must list its risks and an inspection checklist, and it may never be the only recommendation.

### Step 5 — Build the spec trade-off matrix

- **Do.** Rows are the three specs from step 1, columns are the candidates, weights follow the user's ranking (default 50 / 30 / 20 percent). Score each candidate 1–5 per spec, then weight and sum. Apply veto conditions first (does not fit, incompatible connector, no service coverage) and remove vetoed candidates before weighting.
- **Pass when.** A candidate that trails badly on the highest-weight spec while costing more is called out explicitly, never buried under a total score. Then run the marginal-benefit test: how much extra money buys the top spec at full marks, and if that exceeds 20 percent of the budget for a difference the user will rarely notice, rule the premium unjustified.
- **If it fails.** When a spec has no comparable data, mark the cell "no data", fill it with the row mean, and halve that row's weight, so missing data cannot manufacture false precision.

### Step 6 — Issue the buy / wait / switch ruling

- **Do.** Score holding value with the dual-track model in `references/value-scoring.md`, combine it with the price position, and land on exactly one branch:
  - **Buy.** Best landed price at or below the target price (the lower quartile of multi-channel landed prices), composite score at least 6.5, and no stronger alternative within the time window.
  - **Wait.** Price above target but the need can slip, or a predictable promotional window is six weeks away or less and the need is not urgent. Always name the trigger price and a review date. If the need itself is not yet established, this is a demand wait rather than a price wait, and must be labelled as such.
  - **Switch.** An in-budget alternative scores at least 0.5 higher, or the net outlay after trade-in is lower than continuing to hold the current unit.
- **Pass when.** Exactly one verdict, each with an executable trigger (a price threshold, a time window, or a named alternative) and a re-check method. The target price comes from the skill's default threshold and may be overridden by the user, in which case the override is recorded in the report.
- **If it fails.** When evidence cannot support a number but a verdict is required, give only the two-by-two position (price low or high against urgency), leave the scores blank and state the gap.

### Step 7 — Write the decision report

- **Do.** Fill the template in `references/decision-report.md`, verdict first and tables second, with the evidence log and open items last. Add the one-pager when the user asks for something shareable.
- **Pass when.** The verdict card is 150 characters or fewer and can be forwarded alone; every price traces back to a row in the evidence log; no promise of a guaranteed lowest price appears anywhere.
- **If it fails.** When space is tight, cut the detail rows from the channel and spec matrices, keep the verdict, the three reasons and the trigger price, and move the rest to an appendix. The evidence log is never cut.

## Output Format

```
Verdict: buy / wait / switch channel (one line + confidence)
Comparison: channel | list | after-coupon | final | captured at | evidence id
Gap attribution: channel / coupon threshold / variant / timing
Risk and validity window
Next action: where, which coupon, when
```

## Quality Gates

- [ ] Every price carries a source type, a retrieval date and a verification status; unsourced numbers count as zero.
- [ ] Each candidate draws on at least three source types and each SKU on at least two independent sources; any gap above 15 percent is explained.
- [ ] The landed price is decomposed line by line: coupon, threshold discount, shipping, rebate, trade-in, each with its basis and settlement timing.
- [ ] Channel tiers rest on observable signals, and T3 / T4 risks are stated.
- [ ] All three must-have specs are measurable in the matrix; no "quiet", "durable" or similar non-comparable wording.
- [ ] The ruling is exactly one of buy, wait or switch, with an executable trigger and a re-check method.
- [ ] The first line states the retrieval date and that prices must be re-checked.
- [ ] Gaps are marked unverified or unpriced; no estimated figures are used to close them.
- [ ] Body length is 900–1800 characters and the verdict card is 150 characters or fewer, above the fold.
- [ ] No guaranteed-lowest-price claims and no personal identity or household financial data anywhere.

## Scope and Limits

- **No live monitoring and no ordering.** Every price is a snapshot taken at retrieval time. Coupons and campaign rules change without notice, so the user re-checks before paying. PriceLens never fills in an order and never touches payment.
- **No lowest-price guarantee.** It states where the price sits relative to currently reachable channels and shows the evidence for that judgement. It does not promise the cheapest possible price, nor that a price will hold.
- **No verdicts on items that need physical inspection.** Jewellery, watches, used vehicles and one-off collectibles get screening criteria, an inspection checklist and negotiation lines only.
- **No regulatory judgement.** For medicines, medical devices, financial products and cross-border purchases, it points to the official source that must be checked and stops there.
- **Downgrade instead of invent.** Unreachable sources produce a range plus a gap list. If the three inputs from step 1 are refused, the work does not start.
- **No personal data.** It does not request ID numbers, phone numbers, delivery addresses, accounts or payment details, and never writes such data into the report.

## Common Traps

- **Comparing list price with final price**: convert everything to the price actually paid.
- **Ignoring variant and capacity**: align specs before comparing.
- **Treating historical lows as normal**: report the historical range and current percentile.
- **No timestamp**: every evidence item must carry capture time.

## Sample Delivery

Input (3 lines):

```
Category: robot vacuum, self-emptying
Budget: 2500-3500 CNY, landed price
Must-haves: 1) climbing height 2) noise 3) annual consumable cost
```

Output skeleton (18 lines):

```
Report: robot vacuum, self-emptying (retrieved YYYY-MM-DD; prices must be re-checked)

**Verdict card**
Buy: [candidate B]. Reasons: [top-weight spec met], [landed price at the low end of the range], [T1 channel with invoice].

**Landed price**
| Candidate | Sticker | Coupon | Shipping | Rebate | Trade-in | Landed range | Verified |
|---|---|---|---|---|---|---|---|
| A | [..] | -[..] | +[..] | -[..] | -[..] | [..]-[..] | 2 sources |
| B | [..] | -[..] | +[..] | -[..] | -[..] | [..]-[..] | 2 sources |
**Channel matrix**
Primary: [brand-owned] T1 ([..], readable without login); backup: [third-party] T3 ([..], login required, invoice risk).
**Spec trade-off**
| Weight band | Climbing 50% | Noise 30% | Consumables 20% | Weighted |
|---|---|---|---|---|
| A / B | 3 / 5 | 5 / 4 | 4 / 4 | [..] / [..] |
**Ruling: buy**
Trigger met: landed price at or below target [..]. Re-check coupon threshold and shipping before ordering.
```
A full delivery adds the evidence log and open items, one row per source with dates and status.

## Related Skills

- **TableScribe (paid)**: extract multi-channel quotes into a table first.
- **ChartAtelier (paid)**: chart price trends across channels.

## Reference Files

- `references/price-evidence-chain.md` — the four source types, same-SKU matching, cross-check tolerance, record fields and false-signal list.
- `references/channel-matrix.md` — reachability grades, T1–T4 trust tiers, risk signals and the five questions to ask before ordering.
- `references/value-scoring.md` — dual-track scoring, type weights, net-benefit and replacement-cost models, daily-cost baseline ranking and the asset ledger template.
- `references/decision-report.md` — the six-block template, ruling wording, length budget, one-pager and anti-patterns.

---
name: pricing-tester
description: Design and evaluate A/B tests for different price points, discount levels, and bundle combinations to find the highest-converting offer structure.
---

# Pricing Tester

Pricing Tester helps you design rigorous, honest A/B tests for ecommerce price points, discount mechanics, and bundle configurations — then interpret the results with enough statistical discipline that you can act on them. The core idea: conversion rate alone is the wrong scoreboard. A lower price almost always converts better, so the goal is to find the offer structure that maximizes **profit per visitor**, not raw conversion, while protecting downstream metrics like refund and chargeback rates.

Use this skill whenever you need to choose between price points, decide how deep a discount should go, configure a bundle ladder, or settle an argument about "which price made more money" with evidence instead of opinion.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Primary metric | Profit per visitor (price − COGS − fees) × CR | Revenue per visitor (when margins are flat across variants) | Conversion rate alone |
| Optimize for | Profit per visitor, with CR + refund rate as guardrails | Revenue per visitor with a margin floor | "Whichever converts best" |
| Sample size | Pre-calculated from baseline CR + target MDE + power 80% | Rough rule-of-thumb estimate, fixed before launch | "We'll watch it and see" |
| Test duration | Pre-set, ≥ 1–2 full business cycles (incl. weekends/paydays) | Fixed calendar window covering a representative period | Stop as soon as it "looks significant" |
| Number of variants | 2–3 (control + 1–2 challengers) | 4 with a clean hypothesis and bigger traffic | 5+ "let's see what sticks" |
| Randomization unit | Stable visitor/customer ID, sticky across sessions | Cookie/device with reasonable persistence | Per-pageview or per-session (price flicker) |
| Significance threshold | p < 0.05 two-sided, decided before launch | p < 0.10 for low-risk, reversible changes | Whatever threshold the winner happens to clear |
| Stopping rule | Fixed-horizon (run to planned N) or proper sequential test | Pre-registered single interim check | Peeking daily, stop on first green |
| Allocation | 50/50 (or even split), held constant for the whole test | Fixed unequal split decided up front | Shifting traffic toward the "leader" mid-test |

## Solves

- **"Which price makes the most money?"** — Resolves price-point disputes ($34.99 vs $39.99) by comparing profit per visitor, not just who converts more.
- **"How deep should the discount be?"** — Tests 10% vs 20% off (or no discount) so you stop leaving margin on the table or discounting buyers who would have paid full price.
- **"Should we bundle, and how?"** — Designs and reads single / 2-pack / 3-pack ladders to find the configuration that lifts AOV without tanking conversion.
- **"Is this result real or noise?"** — Forces a pre-registered sample size, duration, and significance threshold so you don't ship random variation.
- **"Free shipping or charge for it?"** — Tests shipping-included vs added-at-checkout and free-shipping thresholds against profit per visitor.
- **"Why did our last test mislead us?"** — Diagnoses peeking, segment leakage, price flicker, and CR-only optimization that produced a false winner.
- **"What do we test next?"** — Turns each result into a documented decision and a prioritized next hypothesis instead of a one-off.

## Workflow

1. **Define the hypothesis and primary metric.** Write one falsifiable sentence: "Raising price from $34.99 to $39.99 will increase profit per visitor despite a lower conversion rate." Choose the primary metric up front — almost always **profit per visitor** = (price − COGS − payment/fulfillment fees) × conversion rate. Pick guardrail metrics (refund rate, chargebacks, support tickets, AOV) that must not degrade for the winner to count.

2. **Choose variants and guardrails.** Keep it to a control plus 1–2 challengers; every extra variant splits traffic and dilutes power. Change one thing at a time (price, or discount, or bundle structure) so the result is interpretable. Decide the margin floor and the maximum acceptable drop in any guardrail before launch.

3. **Estimate sample size and duration.** From your baseline conversion rate and the minimum detectable effect you care about, estimate required visitors per variant (see the experiment-design guide for the rule of thumb). Convert that to a calendar duration using current traffic, then round **up** to cover at least one to two full business cycles so weekday/weekend and payday effects average out.

4. **Set up randomization cleanly.** Randomize on a stable, sticky identifier (logged-in customer ID or a persistent cookie) so a visitor always sees the same price across sessions and devices. Verify the split is even and that price is consistent on PDP, cart, and checkout. Exclude internal traffic, and make sure existing customers / email segments aren't all funneled into one arm.

5. **Run without peeking.** Lock the test until it reaches the planned sample size or end date. Looking at results daily and stopping on the first "significant" reading massively inflates false positives — if you must check, pre-register a single interim look or use a proper sequential method. Do not change price, creative, or traffic allocation mid-test.

6. **Analyze with significance and profit per visitor.** Compute CR, AOV, and profit per visitor for each variant with confidence intervals. Test whether the difference in the primary metric is statistically significant, then ask whether it's also *practically* significant (big enough to matter after the cost of the change). Check guardrails before declaring a winner.

7. **Decide and document.** Pick the variant that maximizes profit per visitor without breaching guardrails — or declare "no detectable difference" honestly when intervals overlap. Record the hypothesis, numbers, decision, and rationale in the output template, then queue the next hypothesis (e.g., test the new price against an even higher one).

## Example 1: $34.99 vs $39.99 single product

**Setup.** A skincare SKU sells at $34.99 (control). COGS is $9.00; payment + fulfillment fees run ~3% of price + $2.50 flat. Baseline conversion rate is ~4.0% of product-page visitors. Hypothesis: $39.99 will earn **more profit per visitor** even if it converts a bit worse.

**Sample-size sanity check.** With baseline CR ≈ 4% and a target minimum detectable effect of ~0.5 absolute points (4.0% → 3.5%) at 80% power, the rule of thumb (see design guide) gives roughly **23,000–30,000 visitors per variant**. At 2,500 PDP visitors/day split 50/50 (~1,250/arm/day), that's about **3–4 weeks** — long enough to fix the duration before launch.

**Observed results** (after the planned run):

| Variant | Visitors | Conversions | CR | Price |
|---|---|---|---|---|
| A: $34.99 | 28,000 | 1,176 | 4.20% | $34.99 |
| B: $39.99 | 28,000 | 1,008 | 3.60% | $39.99 |

**Profit per visitor.** Unit profit = price − COGS − (3% × price) − $2.50.

- A: $34.99 − $9.00 − $1.05 − $2.50 = **$22.44**/order. Profit/visitor = $22.44 × 0.0420 = **$0.9425**.
- B: $39.99 − $9.00 − $1.20 − $2.50 = **$27.29**/order. Profit/visitor = $27.29 × 0.0360 = **$0.9824**.

**Is the gap real?** Per-visitor profit is higher for B by ~$0.040 (about **+4.2%**). The CR difference (4.20% vs 3.60%) is itself comfortably significant at this sample size (the standard error of each CR is ~0.12 pts, so a 0.60-pt gap is ~3.5 SE apart). Because B has both meaningfully higher unit margin and a CR drop that's smaller in proportional terms than the margin gain, profit/visitor favors B.

**Decision.** Ship **$39.99**. It earns ~4% more profit per visitor and ~14% more profit per *order*, despite converting worse — exactly the trap that CR-only optimization would have fallen into (CR-only would have wrongly kept $34.99). Guardrail check first: confirm refund rate and AOV didn't worsen at the higher price. Next hypothesis: test $39.99 vs $42.99 to find where profit/visitor peaks.

## Example 2: 3-way bundle test (single / 2-pack / 3-pack)

**Setup.** Same SKU, COGS $9.00/unit, fees ~3% of price + $2.50 per order (one shipment regardless of quantity). We test three landing-page offers, each as the default add-to-cart:

- **Single** — $39.99 (1 unit)
- **2-pack** — $74.99 (≈6% off vs 2× $39.99 = $79.98)
- **3-pack** — $104.99 (≈12% off vs 3× $39.99 = $119.97)

Hypothesis: a modest quantity discount raises **profit per visitor** via higher AOV, even if per-unit margin shrinks. Primary metric: profit per visitor. Guardrail: refund rate, and conversion rate must not collapse.

**Observed results** (planned run, ~24,000 visitors/arm):

| Variant | Visitors | Orders | CR | AOV | Units/order | Profit/order | Profit/visitor |
|---|---|---|---|---|---|---|---|
| Single $39.99 | 24,000 | 864 | 3.60% | $39.99 | 1 | $27.29 | $0.982 |
| 2-pack $74.99 | 24,000 | 792 | 3.30% | $74.99 | 2 | $52.24 | $1.724 |
| 3-pack $104.99 | 24,000 | 660 | 2.75% | $104.99 | 3 | $69.34 | $1.907 |

**Profit math** (profit/order = revenue − units×COGS − 3%×revenue − $2.50):

- Single: $39.99 − $9.00 − $1.20 − $2.50 = **$27.29**.
- 2-pack: $74.99 − $18.00 − $2.25 − $2.50 = **$52.24**.
- 3-pack: $104.99 − $27.00 − $3.15 − $2.50 = **$69.34**.

Profit/visitor = profit/order × CR:

- Single: $27.29 × 0.0360 = **$0.982**
- 2-pack: $52.24 × 0.0330 = **$1.724**
- 3-pack: $69.34 × 0.0275 = **$1.907**

**Reading it honestly.** As the offer gets bigger, CR falls (fewer people commit to more units) but AOV and profit/order rise faster, so profit/visitor climbs single → 2-pack → 3-pack. The single-vs-bundle gap is large and clearly significant. The **3-pack vs 2-pack** gap in profit/visitor is ~+$0.18 (~+11%) — likely real at this N, but tighter; confirm the CR difference (3.30% vs 2.75%, ~0.15-pt SE each) isn't borderline before treating it as decisive. Also watch the guardrail: a 3-pack can raise refund rate (buyer's remorse on a larger purchase) and tie up more inventory per sale.

**Decision.** Lead with the **3-pack as the default offer** if refund rate holds, while keeping the single and 2-pack as visible options for price-sensitive buyers (this is also a decoy/anchor effect — the 3-pack makes the 2-pack look reasonable). If refunds rise materially on the 3-pack, default to the **2-pack**, which still nearly doubles profit/visitor over the single with a smaller CR hit. Document both the winner and the refund guardrail reading. Next hypothesis: test a steeper 3-pack discount ($99.99) to see whether the CR lift offsets thinner per-unit margin.

## Common Mistakes

1. **Optimizing conversion rate instead of profit per visitor.** Lower prices and bigger discounts almost always win on CR while losing money. *Fix:* make profit per visitor (or revenue per visitor at constant margin) the primary metric, with CR as a guardrail.
2. **Peeking and stopping early.** Checking daily and stopping on the first "p < 0.05" can push your real false-positive rate well above 30%. *Fix:* fix the sample size/end date up front; if you need interim looks, pre-register one or use a sequential test.
3. **Too many variants.** Five price points split traffic five ways and slash power; you also multiply the chance one looks significant by luck. *Fix:* test 2–3 variants with a clear hypothesis; ladder additional points in later rounds.
4. **Changing price (or anything) mid-test.** Editing the price, creative, or promo during the run contaminates both arms and resets the clock. *Fix:* lock all variants for the full duration; if you must change, restart.
5. **Ignoring novelty and seasonality.** A new bundle can spike from curiosity, and a test run only over a sale weekend or one payday won't generalize. *Fix:* run at least one to two full business cycles and avoid one-off promo windows unless that's the question.
6. **Segment leakage / unbalanced arms.** Sending all email or returning customers to one variant makes that arm look better for reasons unrelated to price. *Fix:* randomize on a stable ID, verify arm balance on traffic source and new-vs-returning, exclude internal traffic.
7. **Price flicker from session-level randomization.** Randomizing per pageview/session lets a visitor see different prices, which erodes trust and corrupts attribution. *Fix:* sticky assignment per visitor across sessions and devices; ensure price matches on PDP, cart, and checkout.
8. **Confusing statistical with practical significance.** A "significant" 0.1% profit lift may not be worth the engineering and risk. *Fix:* set a minimum effect worth shipping before launch and report confidence intervals, not just p-values.
9. **Underpowered tests on low-traffic SKUs.** Calling a winner on a few hundred visitors is reading noise. *Fix:* compute required N; if traffic can't reach it in a reasonable window, test a bigger effect, a higher-traffic page, or pool similar SKUs.
10. **Ignoring guardrails.** A higher price or bigger bundle can quietly raise refunds, chargebacks, or support load. *Fix:* pre-define guardrail thresholds and check them before declaring a winner.
11. **HARKing (hypothesizing after results are known) and metric shopping.** Picking the metric or segment that happens to look good inflates false positives. *Fix:* pre-register the primary metric, segments, and threshold; treat post-hoc findings as hypotheses for a fresh test.

## Resources

- **references/output-template.md** — Fill-in deliverable: hypothesis, metrics, variants, sample-size plan, results table, decision, and next steps.
- **references/experiment-design-guide.md** — Statistical guidance: metric choice, MDE, a sample-size rule of thumb, duration, peeking/p-hacking, confidence intervals, and clean randomization.
- **references/pricing-test-patterns.md** — Catalog of pricing test patterns (charm pricing, thresholds, anchor/decoy, bundles, free-shipping thresholds, good/better/best, intro pricing, shipping-included).
- **assets/quality-checklist.md** — Pre-launch and pre-decision checklist to keep every test honest.

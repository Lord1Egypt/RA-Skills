# Pricing Test Quality Checklist

Run this before launching and again before declaring a winner. Every box should be checkable with evidence, not hope.

## Hypothesis
- [ ] The hypothesis is written as one falsifiable sentence (change X → effect on metric → why).
- [ ] The expected direction and reasoning are stated before launch.
- [ ] We've defined what result would change our mind.
- [ ] Only one variable changes between control and challenger(s).

## Metric Choice
- [ ] The primary metric is set and locked before launch.
- [ ] The primary metric is profit per visitor (or revenue per visitor only if margins are equal across variants).
- [ ] The profit formula is written out: price − COGS − payment fee − fulfillment − other.
- [ ] Guardrail metrics are named (refund rate, chargebacks, AOV, support load, margin %).
- [ ] Guardrail thresholds (max acceptable degradation) are set in advance.

## Sample Size & Power
- [ ] Baseline conversion rate is measured, not guessed.
- [ ] A minimum detectable effect (MDE) is chosen from business value.
- [ ] Required visitors per variant are calculated (≥80% power, stated significance level).
- [ ] The MDE is large enough to actually reach the needed N in a sensible window.
- [ ] The number of variants (2–3) is justified given available traffic.
- [ ] If traffic is too low, we adjusted MDE/surface/threshold rather than running underpowered.

## Randomization
- [ ] Randomization is on a stable, sticky identifier (customer ID or persistent cookie).
- [ ] A visitor sees the same price across sessions and devices (no price flicker).
- [ ] Price is consistent across PDP, cart, and checkout for each variant.
- [ ] Traffic split is verified even and held constant for the whole test.
- [ ] Arms are balanced on source, device, and new-vs-returning (no segment leakage).
- [ ] Internal/staff traffic and bots are excluded.

## Execution Discipline
- [ ] Start date, end date, and sample-size target are fixed before launch.
- [ ] Duration covers at least one to two full business cycles.
- [ ] The window avoids distortions (sitewide sale, holiday, stockout) unless that's the test.
- [ ] A stopping rule is pre-registered (fixed-horizon, single interim look, or sequential).
- [ ] No peeking-and-stopping on the first significant reading.
- [ ] Price, creative, and allocation are not changed mid-test.

## Analysis Rigor
- [ ] Results are read only at the planned sample size / end date.
- [ ] The primary metric is compared with a confidence interval, not just a p-value.
- [ ] Significance is judged at the pre-registered threshold.
- [ ] We did not metric-shop or segment-shop after seeing the data (no HARKing).
- [ ] Any post-hoc finding is flagged as a hypothesis for a fresh test.
- [ ] Anomalies during the run (outages, spikes, imbalance) are noted.

## Profit Lens
- [ ] CR, AOV, and profit per visitor are computed for every variant.
- [ ] The decision is based on profit per visitor, not raw conversion rate.
- [ ] A lower-converting but higher-profit variant is correctly preferred when it earns more.
- [ ] The lift is practically significant (worth the change), not just statistically significant.

## Decision & Documentation
- [ ] All guardrails passed for the chosen winner.
- [ ] An honest "no detectable difference" is recorded when intervals overlap.
- [ ] The decision, numbers, and rationale are written in the output template.
- [ ] Expected profit impact at current traffic is estimated.
- [ ] Post-rollout monitoring metrics and duration are defined.
- [ ] The next hypothesis to test is queued.

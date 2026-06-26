# Pricing Test Deliverable Template

Copy this template for every pricing test. Fill in every field; if a field is "N/A", say why. The goal is that anyone reading it six months later can reconstruct what you did and whether to trust the result.

---

## 1. Test Identity

- **Test name / ID:**
- **Owner:**
- **SKU(s) / page(s) under test:**
- **Status:** Planned / Running / Complete
- **Planned start → end date:**
- **Actual start → end date:**

## 2. Hypothesis

> One falsifiable sentence. Format: "Changing [X] from [control] to [variant] will [increase/decrease] [primary metric] because [reason]."

- **Hypothesis:**
- **Direction we expect, and why:**
- **What result would change our mind:**

## 3. Metrics

- **Primary metric:** (default: profit per visitor = (price − COGS − fees) × CR)
- **How profit per order is computed:** price − COGS − payment fee (___% + $___) − fulfillment ($___) − other
- **Guardrail metrics (must not degrade):** e.g., refund rate, chargeback rate, AOV, support tickets, gross margin %
- **Guardrail thresholds:** e.g., "refund rate must stay ≤ X%"

## 4. Variants

| Variant | Description | Price | Discount/mechanic | Notes |
|---|---|---|---|---|
| A (control) | | | | |
| B | | | | |
| C (optional) | | | | |

- **What is held constant across variants:** (creative, page layout, shipping, traffic mix)
- **One-variable-at-a-time confirmed?** Yes / No (explain)

## 5. Sample Size & Duration Plan

- **Baseline conversion rate:** ___%
- **Minimum detectable effect (MDE):** ___ absolute pts / ___% relative
- **Power / significance:** 80% power, p < 0.05 two-sided (or note deviation)
- **Required visitors per variant:** ~_____
- **Current traffic to test surface:** ____ visitors/day
- **Estimated duration:** ____ days/weeks (rounded up to ≥ 1–2 business cycles)
- **Randomization unit:** stable customer ID / persistent cookie / other
- **Allocation:** ___ / ___ (held constant)
- **Stopping rule:** fixed-horizon to planned N/date / pre-registered single interim look / sequential method
- **Exclusions:** internal traffic, bots, [email segment?], existing customers?

## 6. Results

| Variant | Visitors | Conversions | CR | AOV | Profit/order | Profit/visitor | 95% CI (primary) | Significant vs control? |
|---|---|---|---|---|---|---|---|---|
| A (control) | | | | | | | | — |
| B | | | | | | | | Yes/No (p=___) |
| C | | | | | | | | Yes/No (p=___) |

- **Guardrail readings:** refund rate ___% (A) vs ___% (B); other: ___
- **Sample size actually reached vs plan:** _____ / _____ (any shortfall?)
- **Any anomalies during the run?** (outages, promos, traffic spikes, arm imbalance)

## 7. Decision & Rationale

- **Winner / outcome:** Variant ___ / No detectable difference / Inconclusive (underpowered)
- **Statistical significance:** (p-value or CI overlap on the primary metric)
- **Practical significance:** (is the lift big enough to be worth shipping?)
- **Guardrails passed?** Yes / No (detail)
- **Rationale (2–4 sentences):**

## 8. Rollout & Next Steps

- **Rollout plan:** ship to 100% / staged ramp / hold
- **Expected impact:** ~$___ profit/visitor → ~$___/month at current traffic
- **Monitoring after rollout:** which metrics, for how long
- **Next hypothesis to test:** (e.g., new price vs an even higher one; steeper bundle discount)
- **Lessons / notes for future tests:**

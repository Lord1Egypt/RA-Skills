---
name: ltv-loyalty-winback
description: Predict repeat-customer churn risk from purchase history and tier activity, then output branch-specific win-back and activation workflows. Use when 90-day (or similar) non-repurchase cohorts are growing, membership or tier engagement is dropping, points are about to expire and you need pre-expiry campaigns, RFM or LTV segmentation is discussed, or the user wants automated reactivation plays for lapsed buyers. Branch logic: high-value VIPs get white-glove CS care plans; standard buyers get time-bound discount or incentive bait. Also trigger on "silent customers," lapse risk, loyalty program fatigue, or win-back sequences — even if they only say "our repeat rate is falling." Do NOT use for simple single-order purchase confirmations, shipping notices, or one-off transactional messages with no retention or churn context.
compatibility:
  required: []
---

# LTV loyalty churn alert & win-back

You connect **historical purchase frequency (and recency)** → **silence / churn risk** → **automated activation workflows** (journeys, messages, and ops hooks).

## When NOT to use (should-not-trigger)

- **Single purchase confirmation** only ("thanks for your order") with no retention ask.
- Pure transactional templates with no lapse or segment context.

If the user later adds "many haven't bought again," switch to full workflow mode.

## Gather context

1. **Recency**: last purchase date distribution; spike in 90d+ silent (or merchant’s window).
2. **Frequency**: orders per customer in last 12 months; baseline vs cohort.
3. **Monetary**: AOV and cumulative spend — **VIP threshold** (define or ask).
4. **Tier / points**: tier rules, points expiry date and notice rules.
5. **Channel**: email, SMS, app push, CS outreach — constraints and consent.

For RFM-style cutoffs and workflow templates, read `references/loyalty_playbook.md` when needed.

## Core workflow (always)

1. **Risk framing** — Classify silence (e.g. at-risk: no order in 90d; high-risk: 120d+; formerly frequent now cold).
2. **Segment branch**
   - **VIP / high-value** → **Dedicated CS care** (named contact, proactive outreach, perk without trashing margin — early access, bundle concierge, not only generic % off).
   - **Standard buyer** → **Time-bound discount or incentive bait** (deadline, code, stack rules clear).
3. **Activation workflow** — Trigger, wait steps, exit rules, measure (reactivation rate, incremental revenue).

## Mandatory outputs (full engagement)

Every **full** churn / loyalty answer must include:

1. **Risk summary** — Who is silent, how many (or %), vs historical norm.
2. **Two branches** — At least one block labeled **VIP / high-value** (CS care) and one **Standard** (discount bait), even if one segment is empty ("if no VIPs, still document threshold").
3. **Win-back plan table** — concrete steps + channel + timing.
4. **Points expiry branch (if applicable)** — Pre-expiry nudge sequence before burn.

## Win-back plan table (required shape)

| Segment | Silence signal | Action | Channel | Timing |
|---------|----------------|--------|---------|--------|
| VIP | e.g. 90d + LTV top decile | Dedicated CS check-in + perk | Email + optional call | Day 0, Day 7 |
| Standard | e.g. 90d no order | Limited-time offer | Email/SMS | Day 0, Day 3, Day 10 |
| Points at risk | Expiry in 14d | Redeem nudge + basket builder | Email | T-14, T-7, T-2 |

Adjust rows to data; keep **VIP vs Standard** distinction explicit.

## VIP branch (content requirements)

- Named or role-based **concierge** line.
- **Non-price-first** value where possible (early access, restock hold, bundle suggestion).
- **Escalation path** if no response.

## Standard branch (content requirements)

- **Time-bound** offer (end date).
- Clear **code or auto-apply** and exclusions.
- Single primary CTA.

## Success metrics (suggest in every full run)

- Reactivation rate (ordered within 30d of campaign).
- Incremental revenue vs holdout.
- Unsubscribe / complaint rate (guardrail).

## Split with other skills

- **Affiliate reconciliation** → not this skill.
- **Abandoned checkout** (session drop) → checkout skill; this skill is **post-purchase lapse**.

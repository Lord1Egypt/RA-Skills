---
name: promo-stock
description: During peak sales (Black Friday, Cyber Monday, Singles' Day, flash sales), align hot-SKU remaining inventory with live ad spend—surface sell-through risk, auto-style Pre-order messaging when stock crosses a threshold, and produce supplier restock chase communications. Use this skill whenever the user mentions inventory under ~20% while ads still run, the last 24 hours before a major promo, oversell risk, cutting Meta/Google/TikTok when stock is thin, switching PDP to pre-order, or supplier expedite emails—even if they only say "we might stock out during the sale" or "ads are still on but warehouse is low." Also trigger on safety stock breaches, SKU-level pacing, and multi-channel inventory sync. Do NOT use for annual financial inventory audits with no live promo or ads context, pure demand forecasting with no immediate copy or comms need, or legal product compliance for pre-orders in regulated categories without the user asking for operational templates.
compatibility:
  required: []
---

# Promo Inventory Defense

You are an **inventory × paid-media defense operator** for high-velocity events. You connect **real-time or near-real-time sell-through** to **customer-facing availability copy** and **supplier actions**.

## Mandatory deliverable policy

For **every** full response about **promo stock risk, ad pacing vs inventory, or pre-order switches** (unless the user explicitly scopes to only one artifact—then still list the other two as **deferred**):

### 1) Threshold logic (explicit X)

Define **X** as either:

- **User-supplied** threshold (units, days of cover, or % of peak stock), or  
- **Default framing**: flag when **on-hand sellable** drops below **20% of event allocation** or **below safety stock**—state the formula in plain language.

Output a **decision block**:

- **If inventory < X** → actions: **Pre-order or backorder copy**, **ad reduction/pause rule**, **internal alert** (who, channel).  
- **If inventory ≥ X but velocity high** → **watch metrics** and **recheck cadence** (e.g. every 4h in final 24h).

### 2) Pre-order switch copy (auto-generated style)

When the scenario triggers **inventory < X**, produce **ready-to-publish** blocks (platform-agnostic labels):

1. **PDP headline + subline** — honest availability (est. ship date window or "ships when restocked").  
2. **Cart / checkout microcopy** — no surprise delays; link to policy.  
3. **Ad / landing alignment** — short note to **sync** ad creative so it does not promise **immediate ship** if pre-order.

Avoid **deceptive** scarcity; comply with regional pre-sale rules at a high level—flag **legal review** if regulated.

### 3) Supplier restock email template

Include **at least one** complete **supplier chase email** (subject + body) with merge fields:

- SKU / variant IDs, quantities, required-by date, PO reference, incoterm or ship-to if relevant, escalation line ("if no confirmation by …").

Optional second template: **SMS/Slack one-liner** for internal ops.

### 4) Sync table: stock vs ads

Include a Markdown table (**at least four rows**) such as:

| SKU or group | Sellable on-hand | % of event allocation or DoC | Ads status (on/paced/pause) | Recommended action | Owner |

Use **placeholders** if the user provided no numbers.

## T‑24h checklist (pushy when timing matches)

If the user is **within ~24 hours** of the event **or** says "last day before sale," prepend or include a **T‑24h checklist**: verify inventory snapshot time, ad schedules, pre-order fallback live, supplier acknowledgment, customer service macro.

## When NOT to use this skill (should-not-trigger)

- **Only** year-end stock count with no promo or ads.  
- **Only** HR or carrier contract negotiation without SKU urgency.  
- **Only** generic "improve supply chain" with no event window.

For deeper formulas (DoC, reorder point, multi-warehouse), read `references/promo_inventory_playbook.md` when needed.

## How this skill fits with others

- **Pricing / competitor** skills — use when the issue is **stock and media sync**, not rival price.

---
name: promo-traffic-stress-monitor
description: Monitor traffic efficiency and conversion load during major promos (Black Friday, Cyber Monday, Christmas peaks, flash sales) and advise dynamic ad spend, restock, and traffic allocation. Use in the first ~4 hours after a promo goes live, when ROI drops below breakeven during a sale, when hero SKUs sell out instantly, when the user mentions scaling or cutting ads mid-campaign, server or checkout strain, or "traffic is huge but orders aren't." Steps implied: real-time (or latest) traffic → conversion efficiency → if strong, recommend scaling spend or shifting budget to winners; if weak, recommend landing-page and funnel checks before spend. Also trigger on stockouts under load, CAC spike during promos, or reallocating budget between campaigns. Do NOT use for evergreen SEO-only plans with no live promo window, or pure creative briefs without performance or inventory context.
compatibility:
  required: []
---

# Promo traffic stress monitor

You support **live promo operations**: **traffic scale → conversion load → restock and traffic split decisions** so merchants don’t overpay for broken funnels or underfund winners.

## When to lean in (use when)

- **First ~4 hours** after promo start — baseline efficiency vs plan.
- **ROI below breakeven** during the event — pause or fix before burning budget.
- **Instant sellouts** on key SKUs — restock + traffic reallocation (don’t keep pushing OOS landers).

## Core workflow (always in order)

1. **Get real-time (or best available) traffic** — Sessions, clicks, spend, impressions by channel/campaign; note lag (analytics vs ads manager).
2. **Calculate conversion efficiency** — Session→order or click→order, AOV, ROAS or MER vs breakeven ROAS; compare to **pre-promo baseline** or **same hour prior day**.
3. **Branch**
   - **Efficiency high** (ROAS above target, CVR up, inventory OK) → **Scale or reallocate** — increase budget on winning campaigns/audiences; shift spend from laggards; cap only if ops risk.
   - **Efficiency low** (CVR collapse, ROAS below breakeven) → **Do not scale** — **Landing page / checkout checklist** first (speed, price match, stock message, mobile, payment errors); then small test spend if fixed.

## Restock & traffic allocation (mandatory when OOS mentioned)

- **Pause or swap ads** pointing to OOS PDPs; route to **category / substitute SKU** if strategy allows.
- **Restock priority** — ETA + which channels to hold until inventory lands.
- **Traffic allocation table** — where to cut vs add (by campaign or SKU).

## Mandatory output shapes

### A) Efficiency snapshot (every full run)

| Window | Traffic (sessions or clicks) | Orders | CVR | Spend | ROAS / MER | vs breakeven |
|--------|------------------------------|--------|-----|-------|------------|--------------|
| First 4h (or user window) | … | … | … | … | … | above / below |

Use placeholders if data not provided; state what to pull from which dashboard.

### B) Action matrix

| Signal | Interpretation | Ad action | Non-ad action |
|--------|----------------|-----------|----------------|
| High CVR + ROAS OK | Demand healthy | Scale or reallocate up | Watch stock |
| Low CVR + traffic high | Funnel or Lander | Hold / cut until fixed | Lander + checkout audit |
| SKU OOS + ads on | Waste + bad UX | Pause / redirect | Restock + swap creative |

## First-4-hour playbook (explicit)

- **T+0–1h**: Confirm tracking, promos firing, no sitewide errors; glance CVR vs baseline.
- **T+1–2h**: If ROAS > target and stock fine → **+10–30% budget test** on top ad set (merchant risk tolerance); if ROAS < breakeven → **stop scale**, open lander checklist.
- **T+2–4h**: Consolidate budget to winners; list any **instant sellout** SKUs and **traffic shift** plan.

## Landing-page / load checklist (when conversion low)

- Mobile LCP, hero offer clarity, promo code auto-apply, stock banner, trust badges, payment methods, geo/currency, error rate on checkout.

## When NOT to use

- No promo window and no live metrics ask.
- Only static brand copy with no traffic or ROI context.

For channel-agnostic thresholds and restock messaging, read `references/promo_ops_playbook.md` when needed.

## Split with other skills

- **Abandoned checkout** deep dive → checkout skill.
- **Long-term LTV** → loyalty skill.

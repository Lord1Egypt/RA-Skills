---
name: inventory-health-auditor
description: Audit ecommerce inventory notes or SKU exports, flag stockout, aging, overstock, capital lock-up, and promo-readiness risks, then turn partial inventory data into a prioritized replenish-hold-clear brief. Use when operators, buyers, planners, or founders need a weekly or monthly inventory diagnosis without live ERP, WMS, or BI integrations.
---

# Inventory Health Auditor

## Overview

Use this skill to translate SKU inventory notes, sales summaries, replenishment lead times, and campaign plans into a practical inventory action report. It is designed for weekly ops reviews, monthly inventory meetings, and pre-promo readiness checks.

This MVP is heuristic. It does **not** connect to live ERP, WMS, procurement, or marketplace systems. It relies on the user's exported data, pasted notes, and business context.

## Trigger

Use this skill when the user wants to:
- identify which SKUs are most at risk of stockout, aging, or overstock
- prioritize replenishment versus hold versus clearance actions
- prepare inventory review notes for ops, procurement, or warehouse meetings
- assess whether current stock is ready for a promotion or seasonal demand spike
- turn partial inventory exports into a management summary plus execution checklist

### Example prompts
- "Review our SKU inventory and tell me what needs replenishment first"
- "Which products are aging and tying up too much cash?"
- "Prepare an inventory health brief before our 618 promotion"
- "Help me spot stockout risk across our hero SKUs"

## Workflow
1. Capture the review goal, SKU scope, and whether the immediate concern is stockout, aging, or promo readiness.
2. Normalize the main signals: on-hand inventory, sales velocity, lead time, campaign timing, and seasonality.
3. Separate the likely risk pools: stockout risk, aging or overstock risk, capital lock-up, and structural imbalance.
4. Turn each risk pool into concrete actions such as replenish, throttle, bundle, clear, or pause purchasing.
5. Return a markdown inventory report with a priority queue and a 30-day action plan.

## Inputs
The user can provide any mix of:
- SKU inventory or on-hand stock notes
- 30 to 90 day sales velocity or sell-through context
- replenishment lead times, supplier constraints, or arrival timing
- campaign plans, promo windows, or seasonal tags
- category labels, hero SKUs, and long-tail notes
- cash, warehouse, or procurement constraints

## Outputs
Return a markdown report with:
- an inventory health summary
- a priority queue of major SKU risk types
- recommended actions across replenish, hold, clear, and review
- a 30-day action plan
- assumptions, evidence gaps, and limits

## Safety
- Do not claim access to live ERP, WMS, procurement, or forecasting systems.
- Keep replenishment quantities and purchase decisions human-approved.
- Downgrade certainty when sales velocity, lead time, or campaign timing is incomplete.
- Do not treat seasonality or new-product demand as proven when historical data is weak.

## Best-fit Scenarios
- weekly or monthly ecommerce inventory reviews
- pre-promo inventory readiness checks
- multi-SKU catalog management without heavy BI tooling
- operator or founder-led businesses that need a fast prioritization layer

## Not Ideal For
- real-time replenishment automation
- warehouse slotting optimization
- full demand forecasting or probabilistic planning models
- businesses with no SKU-level inventory or sales visibility at all

## Acceptance Criteria
- Return markdown text.
- Include summary, priority queue, action plan, and limits.
- Make the advisory framing explicit.
- Keep the report practical for ops, procurement, and inventory owners.

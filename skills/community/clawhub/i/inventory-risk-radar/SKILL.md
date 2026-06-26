---
name: inventory-risk-radar
description: Scan ecommerce inventory notes or CSV exports for stockout, overstock, aging, inbound-delay, and promo-readiness risk, then turn them into a ranked watchlist, days-of-cover summary, action ladder, scenario notes, and operator-ready meeting brief. Use when inventory planners, operations leads, finance-aware operators, founders, or marketplace teams need a lightweight risk-detection layer without live ERP, WMS, or demand-forecasting integrations.
---

# Inventory Risk Radar

## Overview

Use this skill to turn inventory, sales, and supplier notes into a practical risk brief. It helps teams prioritize which SKUs need immediate attention, what kind of risk is present, and which action path should be reviewed first.

This MVP is heuristic. It does **not** connect to live ERP, WMS, purchase-order systems, or forecasting engines. It relies on the user's provided stock position, velocity, lead-time, and business-context notes.

## Trigger

Use this skill when the user wants to:
- flag stockout, overstock, aging, or inbound-delay risk
- prepare a daily, weekly, or pre-promo inventory watchlist
- estimate where cash or revenue risk is likely building
- turn rough inventory exports into an ops-ready action memo
- align replenishment, markdown, and supplier follow-up priorities

### Example prompts
- "Create a daily inventory risk watchlist from these notes"
- "Which SKUs look most exposed before our promotion?"
- "Help me prioritize stockout versus overstock risk"
- "Turn this inventory and lead-time export into an ops meeting brief"

## Workflow

1. Capture the review mode, such as daily watchlist, replenishment review, pre-promo scan, or cash-risk review.
2. Normalize the likely inventory signals: on-hand, inbound, sales velocity, lead time, and aging pressure.
3. Classify the major risk types and translate them into business exposure.
4. Build the watchlist, action ladder, and scenario notes.
5. Return a markdown brief that operators can use in review meetings.

## Inputs

The user can provide any mix of:
- on-hand, reserved, available, inbound, or backorder notes
- recent sales velocity, sell-through, or promo assumptions
- supplier lead time, PO status, inbound ETA, or vendor reliability notes
- aging days, markdown history, or storage constraints
- margin, cash sensitivity, or strategic-SKU context
- review purpose such as daily monitoring, replenishment planning, or promo readiness

## Outputs

Return a markdown risk brief with:
- inventory risk dashboard
- days-of-cover summary
- critical, warning, and watch-tier notes
- action ladder and scenario notes
- owner-ready watchlist guidance
- assumptions, confidence notes, and limits

## Safety

- Do not claim access to live ERP, WMS, or supplier systems.
- Treat exposure estimates as directional unless the user provides complete inputs.
- Do not auto-create POs, transfers, markdowns, or ad changes.
- Keep replenishment, liquidation, and promo decisions human-approved.
- Reduce confidence when lead time, velocity, or SKU mapping is incomplete.

## Best-fit Scenarios

- SMB and mid-market ecommerce teams managing recurring stock risk
- weekly replenishment meetings or pre-promo reviews
- brands balancing stockout loss against cash tied up in slow movers
- operators who need a lighter decision layer than a full planning suite

## Not Ideal For

- manufacturing-grade MRP planning with BOM and production scheduling
- highly automated warehouse orchestration or real-time fulfillment control
- businesses with almost no sales, stock, or lead-time history
- workflows that require automatic purchasing or system execution

## Example Output Pattern

A strong response should:
- separate stockout, overstock, aging, and inbound-delay logic clearly
- show severity and likely action path, not only raw inventory commentary
- connect revenue risk and cash risk in the same brief when relevant
- include scenario thinking for promo uplift or inbound slippage
- surface assumptions when data quality is weak

## Acceptance Criteria

- Return markdown text.
- Include dashboard, watchlist, action, and limits sections.
- Make advisory limits explicit.
- Keep the brief practical for operations, purchasing, and finance-aware operators.

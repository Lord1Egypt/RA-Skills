---
name: pricing-strategy-advisor
description: Turn pricing notes, margin pressure, competitor context, discount behavior, and channel constraints into a practical pricing strategy brief with objective framing, move options, test ideas, and guardrails. Use when ecommerce teams, brand operators, category managers, or consultants need pricing guidance without live competitor crawlers, ERP feeds, or analytics APIs.
---

# Pricing Strategy Advisor

## Overview

Use this skill to structure pricing decisions when the team has partial information but still needs a clear commercial recommendation. It helps with pricing architecture, margin recovery, launch pricing, and discount discipline.

This MVP is heuristic. It does **not** fetch live competitor prices, cost feeds, marketplace data, or conversion dashboards. It relies on the user's supplied context and assumptions.

## Trigger

Use this skill when the user wants to:
- decide whether to raise, hold, narrow, or tier prices
- recover margin without blindly killing conversion
- tighten discount discipline or promo hygiene
- design a price ladder, bundle, or good-better-best structure
- prepare a pricing memo before a launch, seasonal reset, or negotiation

### Example prompts
- "Help me decide whether we should raise prices or cut discount depth"
- "Design a better pricing ladder for our core line"
- "We have competitor pressure and rising costs. What pricing moves make sense?"
- "Create a pricing test plan for this product launch"

## Workflow

1. Clarify the pricing objective and what business trade-off matters most.
2. Normalize the strongest signals, such as cost, conversion, competitor pressure, and discount behavior.
3. Separate structural pricing issues from temporary promo, inventory, or channel noise.
4. Recommend a short list of moves with guardrails and experiment ideas.
5. Return a markdown strategy brief with risks, metrics, and assumptions.

## Inputs

The user can provide any mix of:
- current and target prices, margins, or cost changes
- competitor references or marketplace context
- conversion, volume, AOV, or bundle behavior
- promo cadence, coupon usage, or markdown history
- channel constraints such as MAP, retailer parity, or marketplace conflict
- inventory pressure, premium positioning, or launch goals

## Outputs

Return a markdown pricing brief with:
- primary pricing objective
- pricing posture summary
- recommended moves and trade-offs
- test design ideas and guardrails
- metrics to monitor and escalation notes
- assumptions, confidence notes, and limits

## Safety

- Do not claim access to live competitor or conversion data.
- Do not present price elasticity as proven unless the user supplies evidence.
- Avoid auto-approving permanent price increases, channel exceptions, or MAP violations.
- Keep final pricing changes human-approved.
- Downgrade confidence when channel conflict or unit economics are unclear.

## Best-fit Scenarios

- DTC and marketplace brands reviewing price strategy quarterly or around major campaigns
- operators who need a structured recommendation before changing discount or ladder logic
- founders balancing growth, margin, and positioning without a full pricing stack
- consultants preparing a first-pass pricing memo

## Not Ideal For

- real-time competitor repricing systems
- heavily regulated pricing environments that require legal review
- highly quantitative elasticity modeling with experimental control data
- workflows that must write prices directly into commerce systems

## Acceptance Criteria

- Return markdown text.
- Include objective, recommendation, guardrail, and monitoring sections.
- Keep the advisory framing explicit.
- Make trade-offs practical for operators and decision-makers.

---
name: mobile-commerce-ux-auditor
description: Audit mobile shopping flows, identify conversion friction, prioritize UX issues, and suggest experiment backlogs for product teams, CRO specialists, and e-commerce operators. Use when reviewing mobile storefronts, PDPs, carts, checkouts, or app purchase flows from screenshots or textual flow descriptions without live analytics APIs.
---

# Mobile Commerce UX Auditor

## Overview

Use this skill to convert mobile shopping-flow notes into a commerce-specific UX audit. It focuses on common conversion blockers in mobile homepages, search, PDPs, carts, checkouts, and reorder flows.

This MVP is heuristic. It does **not** analyze real heatmaps, session replays, or analytics APIs. Instead, it applies a structured mobile-commerce checklist and produces a markdown audit that can feed a growth backlog.

## Trigger

Use this skill when the user wants to:
- audit a mobile storefront or app shopping flow
- diagnose low add-to-cart or checkout completion
- identify quick-win conversion fixes
- turn screenshots or flow notes into a prioritized UX backlog
- generate experiment ideas for A/B testing or redesign sprints

### Example prompts
- "Audit our mobile checkout flow"
- "Review these PDP screenshots for conversion friction"
- "Why is mobile add-to-cart low on our skincare store?"
- "Create a quick mobile commerce UX audit from these notes"

## Workflow

1. Capture the business goal and the stages the user is concerned about.
2. Map the input to mobile-commerce stages such as landing, PDP, cart, and checkout.
3. Apply a stage-specific issue library around clarity, trust, hierarchy, form burden, and tap friction.
4. Prioritize findings by likely revenue impact and implementation effort.
5. Return a markdown audit with findings, quick wins, and experiment ideas.

## Inputs

The user can provide any mix of:
- screenshots or textual descriptions of the mobile flow
- funnel goal, such as conversion lift or checkout drop-off reduction
- business context and target market
- known symptoms, such as hidden shipping info or low CTA visibility
- notes about device assumptions or audience

## Outputs

Return a markdown audit with:
- executive summary
- prioritized UX findings by stage
- quick wins
- experiment backlog
- assumptions and evidence gaps

## Safety

- Do not claim access to real analytics or behavioral tools.
- Treat recommendations as heuristics until validated with data.
- Avoid guaranteed uplift claims.
- State clearly when stage coverage is incomplete.

## Examples

### Example 1
Input: mobile PDP and checkout notes for a fashion store.

Output: highlight weak size guidance, delayed shipping clarity, and low-trust checkout signals, then propose specific fixes and tests.

### Example 2
Input: mobile grocery reorder flow.

Output: identify tap friction, reorder-path ambiguity, and cart-message overload, then convert them into a quick-win backlog.

## Acceptance Criteria

- Return markdown text.
- Cover at least 4 mobile-commerce findings or stages.
- Prioritize issues by severity or impact.
- Include at least 3 experiment or quick-win ideas.

---
name: new-product-launch-copilot
description: Turn a product idea, new SKU, or collection launch into a channel-ready ecommerce launch brief, messaging matrix, readiness checklist, milestone timeline, KPI framework, and risk watchlist. Use when operators, founders, growth leads, or consultants need structured launch planning across Shopify, Amazon, email, paid social, TikTok Shop, Xiaohongshu, or similar channels without live PM, ads, or analytics integrations.
---

# New Product Launch Copilot

## Overview

Use this skill to convert a rough launch idea into an execution-ready planning brief. It helps ecommerce teams align positioning, channel sequencing, asset readiness, launch timing, KPI definitions, and risk controls before go-live.

This MVP is heuristic. It does **not** create ads, publish listings, sync inventory, or access live project-management tools. It relies on the user's provided product notes, channel context, assets, and constraints.

## Trigger

Use this skill when the user wants to:
- prepare a launch brief for a new SKU, bundle, or seasonal collection
- turn product features into channel-ready messaging
- build a launch checklist, timeline, and dependency view
- spot launch-readiness gaps in assets, FAQ, support, analytics, or inventory
- define day-1, week-1, and launch-window KPIs before launch

### Example prompts
- "Create a launch plan for our new skincare serum"
- "Build a Shopify, email, and TikTok launch brief from these notes"
- "What are we missing before this Amazon bundle launch goes live?"
- "Turn this product idea into a multi-channel launch checklist"

## Workflow

1. Capture the launch objective, product promise, and target audience.
2. Map the likely launch channels, asset gaps, and operating dependencies.
3. Translate features into benefits, proof points, and channel hooks.
4. Build the readiness checklist, milestone plan, KPI frame, and risk watchlist.
5. Return a markdown launch brief that the team can execute and review.

## Inputs

The user can provide any mix of:
- product name, category, feature list, packaging notes, and price target
- launch goal such as first orders, demand validation, AOV growth, or waitlist building
- preferred channels such as Shopify, Amazon, email, paid social, TikTok Shop, Xiaohongshu, or creator outreach
- current assets such as PDP draft, imagery, video, UGC, FAQ, reviews, or influencer notes
- stock, budget, deadline, or compliance constraints
- competitor references or seasonal campaign context

## Outputs

Return a markdown launch brief with:
- launch thesis and positioning summary
- messaging matrix
- readiness checklist by workstream
- milestone timeline from pre-launch to post-launch
- KPI and risk framework
- post-launch learning loop
- assumptions, confidence notes, and limits

## Safety

- Do not claim access to live ads platforms, storefronts, or launch dashboards.
- Do not imply that the launch is ready just because a checklist exists.
- Keep claims, pricing, stock, and compliance decisions human-approved.
- Treat messaging and offer recommendations as draft strategy until reviewed.
- Downgrade certainty when proof assets, inventory, or tracking details are missing.

## Best-fit Scenarios

- DTC and marketplace teams launching a new SKU, bundle, or seasonal collection
- brands without a dedicated launch PM office
- operators who need a reusable launch playbook instead of scattered notes
- agencies or consultants creating first-pass launch plans for clients

## Not Ideal For

- enterprise launches with complex legal, medical, or cross-country governance
- workflows that require automated campaign building or listing creation
- launches with almost no product information or no basic asset inputs
- highly regulated claims where specialist approval is mandatory before messaging exists

## Example Output Pattern

A strong response should:
- explain the launch objective and the audience promise clearly
- bridge product features into channel-ready hooks and proof points
- show what must be ready by T-21, T-14, T-7, T-3, T-0, T+3, and T+7
- include KPI, owner, and risk thinking, not only copy ideas
- leave a visible assumptions block when key evidence is missing

## Acceptance Criteria

- Return markdown text.
- Include launch, checklist, timeline, KPI, and risk sections.
- Make advisory limits explicit.
- Keep the brief practical for ecommerce operators and growth teams.

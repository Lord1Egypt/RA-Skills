---
name: live-commerce-showrunner
description: Plan and run a live commerce session across Douyin, TikTok Shop, Taobao Live, Amazon Live, or similar channels. Use when a team needs a run of show, offer ladder, host script outline, staffing checklist, moderation plan, risk controls, or post-live debrief structure without live platform or GMV data access.
---

# Live Commerce Showrunner

## Overview

Use this skill to turn a rough live selling idea into an operator-ready show brief. It helps structure the show objective, offer flow, host responsibilities, moderation plays, risk controls, and debrief checklist.

This MVP is heuristic. It does **not** connect to live commerce dashboards, inventory systems, ad platforms, comment feeds, or payment tools. It relies on the user's provided channel context, product priorities, offer assumptions, and team constraints.

## Trigger

Use this skill when the user wants to:
- build a run of show for a live commerce session
- plan a launch, promo, clearance, or education-led livestream
- brief hosts, moderators, operators, and product assistants
- design the offer ladder, urgency moments, and comment-conversion plays
- create a pre-show checklist and post-show debrief template

### Example prompts

- "Help me plan a 45-minute Douyin live for our new skincare launch"
- "Create a run of show for a clearance livestream on TikTok Shop"
- "What should our host, moderator, and ops lead each do during the live?"
- "Build a backup plan for low traffic and inventory risk during a live selling event"

## Workflow

1. Capture the show goal, channel, lead products, and commercial constraints.
2. Choose the likely show type, such as launch, promo, education, or guest session.
3. Build the run of show with opening hook, proof moments, offer stacking, and close.
4. Define host, moderator, ops, and product support responsibilities.
5. Return a markdown show brief with risk controls and debrief guidance.

## Inputs

The user can provide any mix of:
- live channel such as Douyin, TikTok Shop, Taobao Live, Amazon Live, or Instagram Live
- show objective such as launch conversion, stock clearance, education, or audience growth
- product priorities, bundles, pricing, or coupon assumptions
- host profile, guest involvement, moderator support, and crew availability
- planned show length, promo calendar, and traffic expectations
- risk notes such as low stock, compliance pressure, weak script confidence, or technical concerns

## Outputs

Return a markdown show brief with:
- show strategy summary
- run of show by segment
- offer and merch plan
- host and crew checklist
- comment moderation and conversion plays
- backup plan for common failure modes
- debrief checklist with learning questions

## Safety

- Do not claim access to live traffic, GMV, comment, or stock systems.
- Do not promise sales outcomes from the show plan.
- Compliance, pricing, and inventory decisions remain human-approved.
- Downgrade certainty when the user provides weak offer, product, or traffic detail.

## Best-fit Scenarios

- brand or marketplace teams running founder-led or host-led live selling sessions
- operators who need structure before a launch or promo livestream
- smaller teams that do not yet have a dedicated live commerce producer

## Not Ideal For

- live in-session control or real-time comment moderation
- guaranteed forecasting of GMV, traffic, or conversion
- regulated categories that require formal legal review before scripting

## Acceptance Criteria

- Return markdown text.
- Include run of show, team roles, risk controls, and debrief sections.
- Make the no-live-data limitation explicit.
- Keep the brief practical for a host, moderator, and ecommerce operator.

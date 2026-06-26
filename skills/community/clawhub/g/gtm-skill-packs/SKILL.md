---
name: gtm-skill-packs
description: >
  Full B2B GTM skill suite for iCustomer Audience Loop. Covers ICP definition,
  account research, lead scoring (FIRE framework), prospecting, meeting prep,
  outbound strategy, and inbound routing. Use when any GTM task is requested.
  Triggers: "help me define our ICP," "research this account," "score this lead,"
  "build a prospect list," "prep me for my call," "write a cold email,"
  "build an outbound campaign," "design our inbound motion," "who should I target,"
  "qualify this account," "rank my pipeline."
license: MIT
compatibility: No code execution required. Web search access recommended for research skills.
metadata:
  author: iCustomer
  version: "1.0.0"
  website: https://icustomer.ai
---

# GTM Skill Packs

Full B2B GTM suite covering the complete loop from ICP definition through outbound
execution, inbound routing, and pipeline qualification — powered by the FIRE scoring
framework.

## Skills in this pack

| Skill | Trigger phrases | Detail |
|---|---|---|
| **ICP Definition** | "define our ICP," "who are our best customers," "refine our ICP" | `references/gtm-icp-definition.md` |
| **Account Research** | "research this account," "brief me on [company]," "prep for meeting with [company]" | `references/gtm-account-research.md` |
| **Qualification Scoring** | "score this lead," "qualify this account," "rank my pipeline," "who do I call first" | `references/gtm-qualification-scoring.md` |
| **Prospecting** | "build a prospect list," "find companies that match our ICP," "fill pipeline for Q[X]" | `references/gtm-prospecting.md` |
| **Meeting Prep** | "prep me for my call with X," "I have a meeting with [company] tomorrow" | `references/gtm-meeting-prep.md` |
| **Outbound Strategy** | "write a cold email," "build an outbound campaign," "draft a LinkedIn DM" | `references/gtm-outbound-strategy.md` |
| **Inbound Strategy** | "design our inbound motion," "build a lead routing model," "our trial signups aren't activating" | `references/gtm-inbound-strategy.md` |

## How to use

When a GTM task is triggered, identify which skill applies from the table above,
read the corresponding file in `references/`, and follow its steps exactly.

For tasks spanning multiple skills (e.g. "build a prospect list and write outreach"),
run each skill in sequence: Prospecting → Qualification Scoring → Outbound Strategy.

When Audience Loop MCP tools are available, use them to push prospect lists,
sync audiences to LinkedIn Ads or Smartlead, and pull campaign analytics.

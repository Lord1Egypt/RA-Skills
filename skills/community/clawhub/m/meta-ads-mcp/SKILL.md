---
name: meta-ads-mcp
version: 1.1.0
license: MIT-0
description: >
  Production-grade operational guide for creating, managing, optimizing, and documenting Meta
  (Facebook/Instagram) ad campaigns via the Facebook Ads MCP. Use whenever the
  user mentions Facebook ads, Instagram ads, Meta campaign planning, ad budgets/spend,
  ad audiences (incl. Custom Audiences), retargeting, ad performance, Pixel/CAPI tracking, creative briefs,
  naming conventions, campaign documentation, or safe MCP-based campaign
  operations.
---

# Meta Ads MCP — Operational Guide

> **Scope**: How to create, manage, update, pause, and document Meta (Facebook/Instagram) ad campaigns using the Facebook Ads MCP. Covers account setup, campaign architecture, targeting, creative, tracking, retargeting, documentation, and safety guardrails.

## Scope & external dependencies

This skill is the **operational workflow** for Meta Ads MCP (campaigns, budgets, audiences, tracking, documentation). It intentionally hands three things to systems outside its own scope — be aware these cross trust boundaries:

- **Google Drive** — suggested for storing creative assets and per-campaign docs. That is your organization's Drive, not part of this skill; substitute your own asset store if preferred.
- **facebook-ads skill** — full ad-copy generation (variations, headlines, CTAs).
- **flux-imagegen skill** — ad-creative image generation.

Use them as needed, but treat any data leaving Meta Ads MCP (to Drive or another skill) under your own data-handling rules.

## How to use this skill

This file is the entrypoint. Detailed playbooks live in `references/`. Load only the file relevant to the current task:

| Task | Reference |
|---|---|
| Pick the right ad account, build campaign hierarchy, name entities | [`references/campaign-architecture.md`](references/campaign-architecture.md) |
| Set budgets, choose cold/warm/hot audiences, apply exclusions | [`references/budget-and-audience.md`](references/budget-and-audience.md) |
| Choose ad format, write copy frameworks, generate creative assets | [`references/creative-and-copy.md`](references/creative-and-copy.md) |
| Install Pixel/CAPI, define events, build retargeting structure | [`references/tracking-and-retargeting.md`](references/tracking-and-retargeting.md) |
| Create campaigns via MCP, monitor KPIs, document decisions | [`references/campaign-operations.md`](references/campaign-operations.md) |
| Run pre-campaign intake before launch | [`references/intake-questions.md`](references/intake-questions.md) |
| Follow hard safety rules and account-health guardrails | [`references/safety-guardrails.md`](references/safety-guardrails.md) |

## Core workflow — always follow this order

1. **Verify the account** — `ads_get_ad_accounts`, `ads_get_pages_for_business`, `ads_get_dataset_details`. Never proceed with an unverified pixel or unlinked page.
2. **Run intake** — gather goal, audience, creative, budget, timeline, and landing page. Do not invent answers.
3. **Plan structure** — pick objective, decide CBO vs ABO, draft 3–5 ad sets and 3–5 ads per set with consistent names.
4. **Create everything PAUSED** — campaign → ad set → ad, all with `status: PAUSED`.
5. **Preview + verify** — check pixel attachment, destination URL, ad preview, and naming in Ads Manager UI before activation.
6. **Activate only after approval** — flip status to `ACTIVE` only after the full review is signed off.
7. **Document** — log the campaign brief, audiences, creatives, performance, and decisions in the campaign documentation folder.

## Non-negotiable safety rules

These are summarized here; full list in `references/safety-guardrails.md`.

- **PAUSE, never delete.** Deletes destroy historical learning and cannot be reversed.
- **Always create in PAUSED status.** No exceptions.
- **Never edit budget by more than 20% at once** — larger jumps reset the Learning Phase.
- **Never run a campaign without a verified pixel.**
- **Never touch a campaign in Learning Phase** — first 7 days / ~50 events.
- **Special ad categories must be declared** — housing, credit, employment, political/social issues.
- **Detailed interest targeting was deprecated January 2026.** Use Advantage+ Audience or broad targeting + strong creative.

## Key MCP tools — quick reference

```text
Account & assets:
  ads_get_ad_accounts              list accessible ad accounts
  ads_get_pages_for_business       list pages under a Business Manager
  ads_catalog_get_catalogs         check product catalogs for dynamic ads
  ads_get_dataset_details          verify Pixel/dataset installation
  ads_get_dataset_quality          check Event Match Quality (target 7+/10)

Creation:
  ads_create_campaign              create campaign (always status: PAUSED)
  ads_create_ad_set                create ad set under a campaign
  ads_create_ad                    create ad under an ad set
  ads_activate_entity              flip status; use PAUSED to disable, never delete

Reporting:
  ads_get_ad_entities              pull campaign/ad set/ad performance
  ads_insights_performance_trend   analyze trends over time
  ads_insights_anomaly_signal      detect unusual patterns
  ads_get_opportunity_score        review Meta recommendations
```

## Related skills

- **facebook-ads** — full ad copy generation: copy variations, headlines, CTA options, and visual concepts.
- **image generation skills** — generate ad creatives in 1:1, 4:5, and 9:16 formats.

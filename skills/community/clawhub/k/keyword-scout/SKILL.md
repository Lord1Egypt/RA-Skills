---
name: keyword-scout
description: Use when the user wants a prioritized keyword or content-opportunity shortlist. Supports TrustGrowth, bounded DataForSEO requests, and validated imports; direct GSC integration is deferred for launch.
---
# Keyword Scout

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## Sources

- Connected: TrustGrowth keyword opportunities via `GET /api/v1/sites/{slug}/keywords?type=quick_win|striking_distance|content_gap|eeat_gap` (the filter param is `type` — there is no `source` query param; `source` appears only as a response field), plus read-only content inventory. Paginate (`page`, `per_page`) rather than assuming one page has everything.
- DataForSEO: read `references/dataforseo.md`; pass its explicit cost-disclosure gate before every billable batch.
- Import: validated JSON/CSV-derived evidence with source and observation date.

Categories used: `~~search console` (striking-distance queries from the user's own data) and `~~SEO tool` (volume, difficulty, SERP). `references/connectors.md` maps each to its tiers: a pasted GSC export or Google Suggest at Tier 1; a local GSC MCP at Tier 2; DataForSEO, Ahrefs/Semrush MCP, or TrustGrowth at Tier 3. Third-party volumes are estimates — label them.

## Workflow

1. Prefer strengthening relevant existing pages for quick wins/striking distance.
2. Consider content/authority gaps only where intent matches the business.
3. Check known live pages and local/read-only content inventory for duplication and cannibalization.
4. Return 5–10 recommendations with query, source, observed state, intent, target page or distinct angle, confidence, and limitations.

Use only observed metrics. Unknown volume/position stays unknown. Make no traffic projection. After the shortlist, recommend one connector only if it materially improves the next run.

## When not to use

- A full content strategy (audience, pillars, sequencing, distribution, measurement) → `content-strategy`; a prioritized keyword list is an input to strategy, not the strategy.
- Competitor movement over time → `competitor-watch`.
- Link-gap or referring-domain questions → `backlink-opportunities`.
- What is already planned or published → `content-desk` (cross-check before recommending topics).

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.

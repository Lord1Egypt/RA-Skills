---
name: keyword-report
description: Use when the user wants a periodic keyword position report — quick wins, striking distance, movement since last period — as a document, from search-console data or TrustGrowth keyword lifecycle.
---
# Keyword Report

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion. Output follows `references/reporting.md`: shared skeleton, SHIP/FIX/BLOCK/UNDECIDED verdict, Measured/User-provided/Estimated labels.

## Sources

Categories: `~~search console`, `~~SEO tool` (`references/connectors.md`).

- Tier 1 (open): autocomplete/suggest expansion plus SERP results the user pastes; positions from a paste are User-provided.
- Tier 2: `~~search console` query rows; striking distance = queries at average position 4–15 with impressions, reported with both windows' values.
- Connected (TrustGrowth): `GET /api/v1/sites/{slug}/keywords` (`?type=quick_win|striking_distance|content_gap`, `?priority=`, `?qualified=`) and `GET /api/v1/sites/{slug}/keywords/{keyword}/history` (`from`/`to`) for per-keyword movement; `GET /api/v1/sites/{slug}/serp?keyword=` for the current SERP context of a highlighted keyword.

## Shape

Lead with movement, not inventory: what rose, what fell, what entered striking distance. Every position is a dated observation from a named source — search-console averages and SERP-snapshot positions are different measurements and never share a delta cell. Third-party volume or difficulty figures are Estimated and say whose. Cap the detail table at what the reader will act on; the full set goes to a `.csv` when asked.

## When not to use

- Finding new keywords or planning content around them → `keyword-scout`.
- Deciding what to write → `content-strategy`.
- One keyword's live SERP inspected interactively → `keyword-scout`; this skill reports periods.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.

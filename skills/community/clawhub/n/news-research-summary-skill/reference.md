---
name: news-research-summary-reference
description: Reference material for web research, source evaluation, query design, deduplication, and citation discipline for the news-research-summary skill.
---

# Reference: Web research & summarization

## Query design (patterns)

Use a small set of high-recall queries first, then refine:

- **Core**: `"<topic>" <year>` / `"<entity>" announcement <year>`
- **Primary-source hunt**:
  - `site:<official-domain> <keyword>`
  - `press release`, `investor relations`, `SEC filing`, `regulator`, `consultation`, `gazette`
- **Verification**:
  - `"<claim snippet>"` (quote a distinctive phrase)
  - `"<number>" "<entity>"` (for metrics)
- **Local language**:
  - If user’s language is Chinese, include both中文/英文 queries when topic is global.
- **Time constraints**:
  - Include the current year explicitly.
  - Prefer “month name” terms for tight windows (e.g., `March 2026`).

## Source quality heuristics

Prioritize in this order (all else equal):

1. **Primary documents**: official statements, filings, regulatory notices, standards, academic papers, court documents.
2. **Direct stakeholder**: company blog/IR, project release notes, maintainer posts.
3. **Reputable secondary**: established newsroom / trade press with editorial oversight.
4. **Tertiary/aggregators**: only for discovery; try to find upstream.

Red flags (down-rank or label as low confidence):
- Anonymous claims without corroboration.
- No date/author/outlet attribution.
- Copy-paste syndication with no added reporting.

## Deduplication rules

When multiple articles cover the same event:
- Keep **one** canonical item in “关键要点”.
- In “来源清单”, list the primary source first, then 1–3 best secondaries.
- Merge repeated facts; keep unique reporting only if it adds new, cited details.

## Handling uncertainty

When you cannot confirm:
- Write: “目前仅见单一来源披露…” and cite it.
- If conflicting:
  - “A 报道 X；B 报道 Y，尚未见官方确认。” and cite both.

## Citation discipline (required)

- Every factual bullet must include at least one link.
- Prefer linking to the most authoritative document.
- Use markdown links; never paste bare URLs.
- If a claim rests on multiple sources, cite 2 links.

## Output tightening checklist

Before final output:
- Remove redundant bullets.
- Ensure each bullet is one idea.
- Ensure dates and proper nouns are consistent.
- Ensure “结论摘要” matches the “关键要点” (no new facts).


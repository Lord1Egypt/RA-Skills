---
name: patent-landscape-analysis
description: Map a technology area using Crawlora Google Patents and USPTO search/detail tools with explicit query coverage, patent-family grouping, assignee normalization, dates, and classifications. Use for an exploratory technology landscape or portfolio comparison, not a legal clearance conclusion.
---

# Patent landscape analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Build an exploratory technology landscape from a documented query strategy.
Establish technical scope, jurisdictions, date basis/window, document types,
assignee scope, and collection budget before presenting counts or trends.

## Build a traceable search corpus

1. Use synonyms and classification lookups to refine the technical query. Keep
   included/excluded terms and each exact query. Google Patents structured
   dates default to priority date when dates are supplied; explicitly choose
   `date_field=priority`, `filing`, or `publication` to match the analysis.
2. Google search pages are zero-based. Record total/results/pages, `many_results`,
   requested pages, and stopping rules. Its top-assignee/inventor/classification
   breakdowns describe the full query match set, not just the collected page;
   do not mix their denominator with your smaller sample or family counts.
3. USPTO uses BRS field/operator syntax rather than Google's structured filters.
   Match jurisdictions and date meaning when cross-checking. Its returned
   `guid` and `database` feed detail's `guid` and `source`; do not synthesize them.
   The REST helper rejects literal `@` in query arguments to prevent local-file
   shorthand. For BRS `@` date expressions use the connected MCP tool, or use
   Google's explicit date filters; keep the helper's file guard intact.
4. Fetch detail for selected publication numbers to obtain family members,
   classifications, abstracts/claims, original/current assignees, and citations.
   Translate only when needed and retain the original/source language context.
   Search snippets alone cannot support a detailed claim-coverage map.

```sh
scripts/crawlora.sh /googlepatents/search q="solid state battery" date_field=publication after=2020-01-01 page=0 num=20
scripts/crawlora.sh /usptoppubs/search q='battery.ti. AND lithium.ab.' num=20 page=0
scripts/crawlora.sh /googlepatents/coverage
# Resolve returned publication numbers and classification codes before detail.
```

## Group families, entities, and technical themes

Keep publication, application, and family counts separate. Group documents only
with returned family evidence; shared titles, inventors, or keywords do not
establish a patent family. Preserve the chosen grouping rule and all member
publications. Do not label a sampled/incomplete family graph exhaustive.

Normalize assignee spelling with an alias ledger while retaining original and
current assignees and unresolved entity matches. Subsidiaries and similarly named
firms are not automatically one owner. Keep reported ownership/status dated and
attributed; the source's `GRANT`/`APPLICATION` search status is not a current
rights-validity determination. Citations and similar documents are relevance
leads, not proof of infringement, technical dependence, quality, or commercial value.

Code technical themes from the available abstract/claims/detail, allowing multiple
labels and unknown evidence. Compare counts over equivalent query/jurisdiction/date
scopes and distinguish publications from family-level inventions. Coverage totals
measure the index's grants/applications by authority/year, not this technology's
output or R&D investment. Return the query/coverage ledger, family/assignee map,
topic matrix, dated trend observations, sample documents, and missing evidence.
This exploratory landscape does not establish freedom to operate, patentability,
validity, enforceability, or a complete prior-art search.

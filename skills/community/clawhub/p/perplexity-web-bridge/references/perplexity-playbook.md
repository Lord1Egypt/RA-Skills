# Perplexity usage playbook (community-validated)

Distilled from two years of r/Perplexity_AI threads and independent audits
(sources: r/Perplexity_AI, Haus research, citeowl, SE Rankings). Used by the
`--recipe` prompt wrapper (`src/jev_webbridge/promptpack.py`) and the
post-extract guards (`site_checks` in the run result).

## The wrapper (what `--recipe` adds to your goal)

1. **Per-sentence citation rule** — "place a citation after every factual
   sentence" is the community's #1 fix: unreferenced sentences turn into
   hallucinations (one audit: 27% of factually wrong sentences had citations
   that did not support the claim — citations also need reading).
2. **Unsupported-labeling** — tell it to label weak evidence "unsupported"
   instead of guessing.
3. **Recency window** — "last 12 months" when the topic moves fast.
4. **Conflict exposure** — "highlight conflicting findings and explain how you
   resolved them" (the flip side: with sources-first Research, a finance test
   found the same question answered with opposite conclusions).
5. **Goal stays verbatim** — the wrapper surrounds your objective so any
   keyword gate on your words keeps working.

## Recipes

| Recipe | Additions (from community tech/finance threads) |
|---|---|
| `finance` | Focus: Finance + Academic; SEC filings, earnings transcripts, 10-K/10-Q only; label projections vs historical data |
| `tech` | official docs + issue trackers; quote error messages verbatim; trade-off table with benchmark sources |
| `research` | source-first (list sources before writing); 30+ breadth; executive summary; open questions |

Focus menus are per-account and change; verify what your UI shows (Focus,
Academic, Web, Video, Social, Writing) rather than trusting this list.

## Anti-pit guards (automatic — `site_checks` in the result)

- **model_label** — read the provenance line the site shows after answering.
  Compare it against the model you selected: silent downgrades are the #1
  recurring complaint (2024 "Pro to Sonar" mega-thread, 2025 "flipped back to
  Pro mid-conversation" reports).
- **decorative_citations / citation_coverage** — markers actually used in the
  body vs sources listed. Independent audits found answers listing 15-19
  sources while the body cited 3-4; a source list is decoration unless the
  body uses it.

## Verification discipline (do this with every answer)

1. Spot-check 2-3 citations — the label is not the evidence.
2. Treat confident-sounding uncited sentences as suspect (12-fact test: 50% of
   unmarked items failed).
3. Recomputable numbers (prices, dates, counts) get recomputed.
4. For decisions: primary sources only — the builder community's own thread
   ("Claude Code wasted ~$2000 building from hallucinated docs") is the
   cautionary tale.

## Mode selection (as of 2025-Q3; menus drift)

Research = long multi-page multi-agent, days-deep, 20+ sources. Labs = deeper
Pro tier. Comet browsers get Deep Research instead of Labs. Default = Pro
Search with Focus. Modes, models and quotas change constantly — this playbook
is v1.1 (2026-09-25); verify before relying on any menu or quota fact here.

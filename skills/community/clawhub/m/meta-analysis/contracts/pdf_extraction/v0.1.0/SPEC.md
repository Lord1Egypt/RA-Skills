# PDF Data Extraction Contract — v0.1.0 (P1)

> Status: design-period draft. Dev freeze: NOT for release until user declares dev period over.

## Scope (P1)

Text-based PDFs only. No scanned pages (marked `scanned` → routing `failed`).
Sources: bordered tables (pdfplumber `lines` strategy) + narrative sentences (regex candidates).
No new dependencies (Camelot optional later; Docling/OCR = P2).

## Pipeline

1. `parse_pdf(path)` → pages[{page, kind: text|table|scanned, text, tables}]
2. Table channels: `t_dichot` (2x2 n/N counts → ai/bi/ci/di), `t_continuous` (mean±sd inline pairs → te/sete)
3. Narrative channel: `narrative_candidates(pages)` → dichot_counts / or_ci / md_ci snippets (all needs_review; no arm-direction inference in P1)
4. Consistency checks (zero-hallucination math): `check_dichot` (recompute OR/CI Woolf, ≤1% / ≤2% tolerance, zero-cell, events≤total), `check_te_sete` (CI symmetry + width ≤5%)
5. Routing: verified (checks pass + keyword colmap) / needs_review (any check fail, positional colmap, continuous source) / failed
6. `extract(pdf_path, reported_summary=...)` → {rows, candidates, n_pages, review_summary}
   - rows carry te/sete recomputed from raw counts whenever recompute succeeded (even if reported-CI mismatch → confidence stays needs_review)
7. `to_a4_rows(result)` → fullflow A4 `extraction_table`-compatible rows (internal `_review` stripped)

## Data contract

- Dichot row: `{study, ai, bi, ci, di, te?, sete?, _review{confidence, checks, source, page, table, template, colmap, anchor}}`
- Continuous row: `{study, te, sete, _review{..., raw{m1,sd1,n1,m2,sd2,n2}}}`
- Arm direction: table colmap `keyword` (header hints) or `positional` (left=exp, right=ctrl → forced needs_review). Arm-direction confirmation is a mandatory human-review item.
- Downstream: b1_pairwise_python consumes ai/bi/ci/di (preferred) or te/sete.

## Red lines

- Unverified rows MUST NOT reach Block B without extraction_guard `stamp --confirm` (A4 red-line gate unchanged).
- Continuous-source rows are ALWAYS needs_review in P1 (literature evidence: zero-shot LLM continuous exact-match <50%; regex-only, no LLM in P1).
- No LLM in P1 pipeline (zero-hallucination by construction). LLM-assisted fragment→schema structuring = P2, only over regex-candidate snippets, never full-text.

## Known limits (v0.1)

- No borderless tables (lines strategy blind); no scanned pages; no cross-page table merging;
- header templates = keyword scoring, exotic headers need manual colmap in review UI (P2);
- narrative dichot counts lack arm attribution (human must assign exp/ctrl);
- single-n fallback assumes equal arms (flagged for review).

# OKRs

Universal OKRs from spec-ocas-journal.md apply. All OKRs maximize against a 30-run evaluation window.

| Name | Metric | Target |
|---|---|---|
| `recommendation_evidence_rate` | fraction of recommendations citing at least one consumed item | 1.0 |
| `serendipity_novelty` | fraction of serendipity results crossing domain boundaries | 0.80 |
| `signal_freshness` | fraction of active signals within decay half-life | 0.60 |
| `email_extraction_coverage` | fraction of transactional emails extracted with confidence >= threshold | 0.90 |
| `dedup_accuracy` | fraction of dedup groupings not corrected by manual review | 0.95 |
| `enrichment_coverage` | fraction of items with enriched = true | 0.90 |
| `schedule_adherence` | fraction of cron runs completing within scheduled hour | 0.95 |
| `data_integrity` | fraction of signals/items passing schema validation on read | 0.99 |
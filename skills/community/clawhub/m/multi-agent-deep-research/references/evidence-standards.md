# Evidence Standards

## Source hierarchy

### Tier A: Primary or authoritative

- government rules, filings, statistics, procurement notices
- company filings, investor letters, official blogs, model cards, API docs
- papers, benchmark owners, original datasets

Use for hard facts, timelines, and core claims.

### Tier B: High-quality secondary

- major research institutions
- reputable think tanks
- strong journalism with explicit sourcing
- transparent industry reports

Use for synthesis, context, and triangulation.

### Tier C: Tertiary or lead-generation only

- opinion posts
- unsourced summaries
- social media threads

Do not use Tier C as sole support for final-report claims.

## Claim classes

- `hard_fact`: directly verifiable
- `reported_fact`: reported by a credible source but not directly observed here
- `interpretation`: synthesis of multiple sources
- `comparison`: relative statement across entities
- `forecast`: forward-looking statement

## Required fields

### Source ledger

- `source_id`
- title
- issuer or author
- publication date
- URL
- tier
- topic or dimension
- status
- notes

### Claim ledger

- `claim_id`
- claim text
- claim class
- linked `source_id`
- time range or cutoff
- confidence
- status
- comparability notes

## QA gates

- No section draft without a source ledger.
- No material claim without at least one source link.
- No leadership claim without a date and metric.
- No cross-entity comparison without a comparability note.
- No final report without a limits section.

## Common failure modes

- mix different years in a single comparison
- treat vendor benchmarks as neutral rankings
- quote a secondary source when the primary source is available
- turn an inference into a fact
- use relative dates like "recently" in a dated report

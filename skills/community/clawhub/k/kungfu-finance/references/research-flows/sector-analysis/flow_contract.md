# Sector Analysis Flow Contract

This flow is for one mainland China A-share industry, concept, theme, or sector.

It is the documented methodology behind sector / hype-cycle research.
The repo build now has a first runnable preview JS flow via `sector-research`, but that runtime is intentionally narrower than the full methodology.

## Use When

- The topic is a sector, concept, industry, theme, or赛道.
- The user asks for sector rotation, hype-cycle analysis, thematic research, concept research, or sector-level thesis building.

## Sector Input Rule

- Methodology still prefers `sector_name` for user-facing requests.
- The current preview JS runtime now accepts direct `sector_name` and only reuses `sector_id` after it has already been returned by a previous backend or local-resolution step.
- Treat `sector_id` as an internal follow-up selector, not the default user-facing input.
- If direct sector lookup fails, the preview runtime may use best-effort local resolution before returning structured `needs_input`.
- Do not assume `similar_sectors` is a guaranteed public default path; it remains best-effort support data.

## Do Not Use When

- The topic is a concrete single stock.
- The user asks for whole-market screening.
- The asset universe is not mainland China A-shares.

## Step Order

Do not drop or merge steps. The full flow is:

1. `step-0-macro`
2. `step-1-filter`
3. `step-2-classify`
4. `step-3-mining`
5. `step-4-thesis`
6. `step-5-position`
7. `step-6-risk`
8. `step-7a-skeptic`
9. `step-7b-advocate`
10. `step-8-verdict`
11. `step-9-output`

The debate steps are mandatory here as well.

## Prompt Layer Responsibilities

- `orchestrator_system.md`: enforce the macro -> filter -> classify -> mining -> thesis -> position -> risk sequence.
- `worker_system.md`: perform the actual sector data gathering and evidence search.
- `synthesizer_notes.md`: define report structure, verdict integration, and final step-9 completeness rules.
- `orchestration_contract.md`: records the strict step-order, gate-check, dialectic, correction, and debate rules migrated from the original `SKILL.md`.
- `shared_context_template.md`: records the canonical step-by-step shared context skeleton migrated from the original `SKILL.md`.

## Required Query Capabilities

The methodology expects these data capabilities:

- `find_similar_sectors`
- `get_sector_constituents`
- `get_sector_performance`
- `get_price_history`
- `get_money_flow`
- `get_finance_basic_indicators`
- `get_valuation_analysis`
- `get_instrument_concepts`
- `get_profit_forecast`
- `web_search`

## Current Project Readiness

Read [../runtime_parity.md](../runtime_parity.md) together with this file.
The list below is methodology-oriented capability demand, not a guarantee that every local wrapper is already backend-revalidated.

### Current preview runtime in `kungfu_finance`

- runnable command: `node scripts/router/run_router.mjs sector-research --sector-name ... [--target-date ...]`
- structured inputs: `sector_performance`, `sector_constituents`
- current selector boundary: `sector_name` first, `sector_id` optional reuse
- output style: `Markdown-first + explicit degradation`
- result surface now also includes repo-controlled `orchestration` alignment metadata
- orchestration parity currently means:
  - original step order is locked
  - debate steps are mandatory
  - dialectic / correction / shared-context contracts are repo-controlled

### Validated structured inputs already available in `kungfu_finance`

- `instrument_prefix`
- `instrument_profile`
- `price_snapshot`
- `bar_series`
- `finance_context`
- `finance_basic_indicators`
- `sector_constituents`
- `sector_performance`

### Runtime demand that still needs parity work

- `find_similar_sectors`
- `get_money_flow`
- `get_valuation_analysis`
- `get_instrument_concepts`
- `get_profit_forecast`

## Remaining Missing Pieces

- stricter money-flow / valuation / constituent-financial adapters for sector-research-specific support data
- full source-asset parity for `ROADMAP.md` and `SECTOR_ANALYSIS_WHITEPAPER_v5.2.1.md`
- judge-grade SVG / eval / quality-gate parity beyond the current repo-controlled preview baseline

## Implementation Boundary

This project should only manage:

- the methodology documents
- prompt assets
- flow contracts
- thin JS products
- later JS orchestration

If a sector query is missing, it should be implemented in the backend / API project and then wrapped here as a thin JS product.

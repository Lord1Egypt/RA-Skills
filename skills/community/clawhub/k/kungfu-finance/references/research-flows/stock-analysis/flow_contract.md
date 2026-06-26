# Stock Analysis Flow Contract

This flow is for one mainland China A-share stock.

It is the documented methodology behind deep single-stock research.
The repo build now has a first runnable preview JS flow via `stock-research`, and that runtime explicitly exposes the migrated orchestration contract in its result surface.

## Use When

- The topic is a concrete single stock.
- The user asks for deep research, institutional stock research, investment thesis building, valuation review, or catalyst analysis.

## Do Not Use When

- The topic is an industry / concept / theme instead of one stock.
- The user asks for whole-market screening.
- The asset is not a mainland China A-share stock.

## Step Order

Do not drop or merge steps. The full flow is:

1. `step-0-macro-sector`
2. `step-1-company-profile`
3. `step-1b-forward-advantage`
4. `step-2-financials`
5. `step-3-valuation`
6. `step-4-price-action`
7. `step-5-thesis`
8. `step-6-catalyst`
9. `step-7a-skeptic`
10. `step-7b-advocate`
11. `step-8-verdict`
12. `step-9-output`

The debate steps are mandatory.
They are not optional polish.

## Prompt Layer Responsibilities

- `orchestrator_system.md`: route the research round-by-round, assign the main step, and enforce the SOP.
- `worker_system.md`: perform the concrete data gathering and evidence building for each assigned step.
- `synthesizer_notes.md`: define final report structure, verdict integration, output constraints, and step-9 completeness rules.
- `orchestration_contract.md`: records the strict step-order, gate-check, dialectic, correction, and debate rules migrated from the original `SKILL.md`.
- `shared_context_template.md`: records the canonical step-by-step shared context skeleton migrated from the original `SKILL.md`.

## Required Query Capabilities

The methodology expects these data capabilities:

- `get_finance_basic_indicators`
- `get_valuation_analysis`
- `get_mainbiz_analysis`
- `get_industry_rank`
- `get_price_history`
- `get_money_flow`
- `get_latest_price`
- `get_instrument_concepts`
- `get_profit_forecast`
- `find_similar_sectors`
- `web_search`

## Current Project Readiness

Read [../runtime_parity.md](../runtime_parity.md) together with this file.
The list below is methodology-oriented capability demand, not a guarantee that every local wrapper is already contract-validated.

### Validated structured inputs already available in `kungfu_finance`

- `instrument_profile`
- `price_snapshot`
- `bar_series`
- `finance_context`
- `finance_basic_indicators`

### Current preview runtime in `kungfu_finance`

- runnable command: `node scripts/router/run_router.mjs stock-research --instrument-name ... --target-date ...`
- result surface now includes:
  - step coverage
  - explicit degradations
  - `hardening.search_runtime`
  - `orchestration` alignment metadata
- orchestration parity currently means:
  - original step order is locked
  - debate steps are mandatory
  - dialectic / correction / shared-context contracts are repo-controlled
- output stack still remains `Markdown-first`

### Runtime demand that still needs parity work

- `get_money_flow`
- `get_mainbiz_analysis`
- `get_valuation_analysis`
- `get_industry_rank`
- `get_instrument_concepts`
- `get_profit_forecast`
- `find_similar_sectors`

## Remaining Missing Pieces

- shared adapter layer for the stock-research-specific capabilities listed above
- full source-asset parity for `DATA_ACQUISITION.md` and `ROADMAP.md`
- judge-grade SVG / eval / quality-gate parity beyond the current repo-controlled preview baseline

## Implementation Boundary

This project should only manage:

- the methodology documents
- prompt assets
- flow contracts
- thin JS products
- later JS orchestration

If a required query is missing, it should be added in the backend / API project and then wrapped here as a thin JS product.

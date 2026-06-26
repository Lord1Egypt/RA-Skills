# Research Runtime Parity

This file is the formal staging note for `RFC-0002`.

Use it to answer four questions before implementing any public deep research command in `kungfu_finance`:

1. Which source-skill capabilities can already use the current backend HTTP contract?
2. Which capabilities exist only as backend internal tools and still need thin public adapters?
3. Which capabilities are fundamentally search-native and must stay in the local research runtime for now?
4. Which source assets have not yet been migrated into this repository?

Do not treat this file as user-facing product copy.
It is an implementation-side truth table for the current migration phase.

## Source Of Truth

Repository-controlled migration truth source:

- `skills/kungfu_finance/references/research-flows/**`
- this file: `skills/kungfu_finance/references/research-flows/runtime_parity.md`
- `docs/rfcs/active/0002-embed-stock-analysis-v2-and-sector-analysis-into-kungfu_finance.md`
- `docs/exec-plans/completed/2026-04-01-kungfu-finance-research-runtime-and-asset-parity.md`

External comparison inputs used during the migration:

- `~/.codex/skills/stock-analysis-v2`
- `~/.codex/skills/sector-analysis`

The external skill directories are reference inputs only.
They are not the auditable control-plane truth for this repository unless their relevant content is explicitly written back into the repository files above.

Current backend data-source truth source:

- `/Users/jc34/Work/kf_skill/serverless-tianshan-api/src/api`
- `/Users/jc34/Work/kf_skill/serverless-tianshan-api/src/agent_tools`

Do not assume a path is usable in production only because a local `.mjs` wrapper already exists.

## Data Source Strategy

The runtime policy for `RFC-0002` is:

- structured market / finance data should prefer the current backend HTTP contract
- backend internal capabilities may be promoted through thin HTTP adapters when needed
- macro / policy / competition / catalyst / debate evidence remains search-native for now
- the migration must not fall back to backend Deep Research orchestration as the primary runtime
- if future search capability is introduced, it must be treated as a separately allowlisted network surface with its own security review and credential boundary

## Capability Matrix

| Capability | Source dependency | Current status | Action |
| --- | --- | --- | --- |
| Stock daily K-line | `stock-analysis-v2` hard dependency | Validated public HTTP via `bar_series -> /api/visualization/bar` | Reuse existing HTTP |
| Stock weekly K-line | `stock-analysis-v2` hard dependency | No dedicated public weekly route confirmed locally; daily bar exists | First version may aggregate from daily K-line in skill runtime |
| Latest price / recent price snapshot | `stock-analysis-v2` hard dependency | Validated public HTTP via `price_snapshot -> /api/visualization/price` | Reuse existing HTTP |
| Sector / concept K-line | `sector-analysis` important input | Validated public HTTP via `sector_performance -> /api/visualization/sector-bar` | Reuse existing HTTP |
| Sector constituents | Secondary support capability | Validated public HTTP via `sector_constituents -> /api/visualization/sector-instruments` | Reuse existing HTTP |
| Finance summary / valuation snapshot / concepts / main business | `stock-analysis-v2` Step 2/3 hard dependency | Validated public HTTP via `finance_context` and `finance_basic_indicators` | Reuse existing HTTP first, extend only if insufficient |
| Profit forecast / consensus-like forecast | `stock-analysis-v2` important input | Public researcher route exists; dedicated finance wrapper path not confirmed locally | Prefer researcher route first, keep dedicated thin adapter as follow-up |
| Real money flow | `stock-analysis-v2` Step 4 hard dependency | Backend internal capability exists; no confirmed local public route | Add thin adapter before public stock research runtime |
| Industry rank / valuation detail / instrument concepts / main-business detail | Important stock-research enhancement | Backend internal capability exists; local public route evidence incomplete | Add thin adapter or rewrite runtime to use existing summary context |
| Similar sectors / fuzzy sector resolution / sector performance summary | Important sector-research capability | Backend internal capability exists; local public route evidence incomplete | Add thin adapter before public sector research runtime |
| Macro / policy / competition / management / catalyst / red-team evidence | Both source skills hard dependency | No unified backend search API | Keep `web_search` in local runtime |

## Product Contract Drift

The wrappers below exist in `skills/kungfu_finance/scripts/products/`, but their backend contract status is not the same.

### Validated Against Local Public Routes

- `bar_series`
- `price_snapshot`
- `finance_context`
- `finance_basic_indicators`
- `sector_constituents`
- `sector_performance`

These are the current safest structured inputs for the future research runtime.

### Local Wrapper Exists, But Local Backend Public Route Is Not Confirmed

- `money_flow`
- `resolve_sector`
- `similar_sectors`
- `instrument_concepts`
- `finance_profit_forecast`
- `finance_industry_rank`
- `finance_valuation_detail`
- `finance_analysis_context`
- `finance_report_status`
- `unusual_movement_context`

Use these wrappers only as migration clues.
Do not treat them as revalidated production contract for the new deep research runtime.

### Backend Internal Capability Exists, But Public Adapter Still Needs Design

- `get_money_flow`
- `get_mainbiz_analysis`
- `get_valuation_analysis`
- `get_industry_rank`
- `find_similar_sectors`
- `get_instrument_concepts`
- `get_profit_forecast`

These should be considered the primary adapter worklist for the next implementation slices.

## Shared Adapter Worklist

The shared runtime should prefer a narrow adapter surface, not one-off direct route sprawl.

### Reuse Existing HTTP As Shared Adapters

- stock price window
- stock K-line window
- sector / concept index window
- stock finance summary
- stock finance basic indicators
- sector constituents

### Promote Internal Backend Capabilities Through Thin Adapters

- money flow
- similar sectors / resolve sector
- instrument concepts
- profit forecast
- industry rank
- valuation detail
- main-business detail

### Keep In Local Research Runtime

- `web_search` policy
- evidence freshness rules
- debate / counter-search protocol
- catalyst search
- macro / competition / management narrative gathering

Do not interpret this section as permission to reuse the current Tianshan auth surface for generic search.
Any search backend introduced later must be reviewed as a separate outbound surface.

## Current Shared Hardening Contract

The repo build now has a minimal shared hardening contract for preview research flows:

- module: `scripts/flows/research_shared/hardening.mjs`
- current consumers: `stock-research`, `sector-research`
- result surface: `hardening.search_runtime`

Current contract semantics:

- default status: `disabled`
- feature gate: `KUNGFU_ENABLE_RESEARCH_SEARCH=1`
- provider marker: `KUNGFU_RESEARCH_SEARCH_PROVIDER=web_search`
- separate endpoint: `KUNGFU_RESEARCH_SEARCH_ENDPOINT`
- separate credential: `KUNGFU_RESEARCH_SEARCH_API_KEY`
- when the separate endpoint and credential are both present, status becomes `ready`, and executed preview flows report `completed`
- if the provider is selected but endpoint / credential is missing, status becomes `misconfigured`
- provider request failures and timeouts surface as `provider_error`
- `credential_boundary` remains `separate_from_kungfu_openkey`
- `inherits_kungfu_openkey` remains `false`

This contract is still narrower than a full multi-provider research orchestration layer.
Its purpose is to keep stock / sector preview flows on one reviewed `web_search` surface without silently reusing the current Tianshan auth path.

The shared hardening contract now also supports a richer preview result surface:

- `report_mode: markdown_svg_preview`
- `parity_stage: svg_gated_preview`
- `report_markdown`
- `report_svg`
- `quality_gate`

## Asset Parity Matrix

Repo-controlled asset parity writeback also lives in:

- `skills/kungfu_finance/references/research-flows/asset_parity_manifest.json`

That manifest is the canonical place to see which source assets are already migrated, which are explicitly deferred, and which preview release blockers still remain.

### Stock Research Assets

Already migrated into this repository:

- step modules
- `DATA_ACQUISITION.md`
- `SVG_SPEC.md`
- `EVAL.md`
- `orchestrator_system.md`
- `worker_system.md`
- `synthesizer_notes.md`
- `flow_contract.md`
- `orchestration_contract.md`
- `quality_gate/README.md`
- `shared_context_template.md`

Still missing from source skill:

- `ROADMAP.md`
- `CHANGELOG.md`

### Sector Research Assets

Already migrated into this repository:

- step modules
- `SVG_SPEC.md`
- `EVAL.md`
- `orchestrator_system.md`
- `worker_system.md`
- `synthesizer_notes.md`
- `flow_contract.md`
- `orchestration_contract.md`
- `quality_gate/README.md`
- `shared_context_template.md`

Still missing from source skill:

- `ROADMAP.md`
- `SECTOR_ANALYSIS_WHITEPAPER_v5.2.1.md`
- source-skill changelog set

## Preview Release Baseline

Current preview release baseline is explicitly recorded in `asset_parity_manifest.json`.

The current baseline requires:

- `cd skills/kungfu_finance && npm run check`
- `cd skills/kungfu_finance && npm test`
- `cd /Users/jc34/Work/kf_skill/kungfu-skills && make workflow-check`

Current preview publish blockers now remain empty.
The remaining deferred assets are explicitly tracked as accepted risk / non-release-critical material in `asset_parity_manifest.json`.

## Runtime Boundary

Until runtime parity is complete:

- methodology docs, orchestration contracts, SVG spec, eval baseline and quality gates are now repo-controlled truth
- preview deep research CLI entrypoints already exist in `kungfu_finance`, and they now run as `markdown_svg_preview`
- deterministic products remain fixed to the Tianshan API base URL
- search-native evidence gathering must stay explicitly routed by the separate research search runtime, not silently mixed into deterministic product flows
- any future provider expansion must keep explicit allowlist and credential isolation rather than inheriting the current `KUNGFU_OPENKEY` path
- experimental product wrappers must not be mistaken for public research-runtime guarantees

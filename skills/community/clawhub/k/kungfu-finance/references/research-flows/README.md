# Research Flows

This directory is the migration staging area for the deep research part of `kungfu_finance`.

It currently contains two documented A-share research methodologies:

- `stock-analysis/`: single-stock institutional research flow for one mainland China A-share instrument
- `sector-analysis/`: industry / sector / concept / theme research flow for one mainland China A-share sector

This directory is no longer only a loose methodology dump.
The repo build now has preview runtime entrypoints via `stock-research` and `sector-research`, and those commands can optionally attach separately configured `web_search` evidence.
The repository also now carries repo-controlled orchestration contracts migrated from the original source skills, including:

- strict step order
- gate-check model
- pre-conclusion dialectic
- discovery-correction protocol
- shared-context template

What still remains preview-only is mainly the product stage and some adapter parity, not the orchestration contract.
The repo build now also carries repo-controlled output/evaluation assets for:

- `report_svg`
- `EVAL.md`
- `quality_gate/README.md`

Before using any of these files as implementation truth, also read:

- [runtime_parity.md](runtime_parity.md)
- [asset_parity_manifest.json](asset_parity_manifest.json)

That file records the current migration truth:

1. which data dependencies can already use current backend HTTP routes
2. which wrappers are still only contract-drift clues
3. which source assets have not reached this repository yet
4. which missing assets are explicitly deferred vs. accepted-risk in the current preview baseline

## Boundary

- `stock-analysis` is for one concrete A-share stock.
- `sector-analysis` is for one A-share industry, concept, theme, or sector.
- Neither flow applies to US stocks, Hong Kong stocks, cryptocurrencies, futures, or forex.

## Source Of Truth

Repository-controlled truth for the migration lives in:

- this directory: `skills/kungfu_finance/references/research-flows/**`
- [runtime_parity.md](runtime_parity.md)
- the active `RFC-0002` and the latest related ExecPlan closeout under `docs/exec-plans/`

External skill directories such as `~/.codex/skills/stock-analysis-v2` and `~/.codex/skills/sector-analysis` may still be used as comparison inputs during the migration, but they are not the auditable repo truth by themselves.

The migrated step modules in this repository originally came from:

- `serverless-tianshan-api/src/handlers/analyse_research/skills/stock_analysis_v2/modules`
- `serverless-tianshan-api/src/handlers/analyse_research/skills/sector_analysis/modules`

The prompt-layer responsibilities came from:

- `serverless-tianshan-api/src/handlers/analyse_research/prompt/skill_stock_prompts.py`
- `serverless-tianshan-api/src/handlers/analyse_research/prompt/skill_sector_prompts.py`
- `serverless-tianshan-api/src/handlers/analyse_research/prompt/skill_debate_prompts.py`

The orchestration-level protocol and shared-context skeleton came from:

- `/Users/jc34/.codex/skills/stock-analysis-v2/SKILL.md`
- `/Users/jc34/.codex/skills/sector-analysis/SKILL.md`

## Current Use

Use this directory for:

1. preserving the full step order and debate protocol
2. preserving the orchestration contract that used to live only in the original source `SKILL.md`
3. keeping the stock-vs-sector boundary explicit
4. staging shared runtime / adapter / asset parity work
5. backing the preview `stock-research` / `sector-research` runtimes with auditable manifests and orchestration metadata

Do not use it to imply that all referenced products are already backend-revalidated or public.

# Kungfu Finance

Kungfu Finance (`kungfu_finance`) is a mainland China A-share skill for:

- stock snapshots
- finance-analysis context
- chip and price-level lookup
- sector and theme analysis
- preview stock deep research for one A-share with explicit degraded sections and source-skill orchestration alignment
- preview sector deep research for one A-share sector with explicit degraded sections and source-skill orchestration alignment
- first-stage bucket access for listing personal buckets and adding instruments
- phase-2 strategy access for public/private strategy query, controlled whole-market results for select or buy-sell strategies, and public paid strategy scanning
- first-stage researcher access for ranking, stock report aggregation, and author report lookup
- first-stage bayesian monitor access for current-user task listing and report lookup

## Runtime Model

- Local runtime: Node.js (`.mjs` scripts, bundled with zero dependencies — no `npm install` needed)
- Package model: bundled executable scripts plus prompt/reference assets
- Outbound APIs (complete list, no other hosts are contacted):

| Host | Purpose | Auth | Free |
|------|---------|------|------|
| `tianshan-api.kungfu-trader.com` | Deterministic products (snapshot, finance, bucket, strategy, researcher, bayesian monitor) | `KUNGFU_OPENKEY` Bearer token | No |
| `push2.eastmoney.com` | Real-time stock quotes (EastMoney public API) | None | Yes |
| `push2his.eastmoney.com` | K-line history, money flow (EastMoney public API) | None | Yes |
| `qt.gtimg.cn` | Real-time quotes fallback (Tencent Finance) | None | Yes |
| `ifzq.gtimg.cn` | K-line history fallback (Tencent Finance) | None | Yes |

The skill is designed as a thin local wrapper around these fixed endpoints.
It does not download extra code at runtime.
It does not use arbitrary user-supplied base URLs.
The bucket and strategy capabilities are implemented as thin API orchestration and do not persist local state.

### Indicator Chart Flow — File Writes & Subprocess

The `indicator-chart` command renders SVG charts and writes them to `~/.openclaw/workspace/finance-master/charts/`.
When `inkscape` is available on the system, it is invoked via `execFileSync` (not shell — no injection risk) to convert SVG to PNG for chat delivery.
If `inkscape` is not installed, the flow still succeeds and returns the SVG path only (`png_path` will be `null`).

### Health Check & Config — File Writes

The `config-openkey` command validates an OpenKey against the backend and writes it to `~/.openclaw/.env`.
The `health` command only reads environment variables and makes a single POST to the Tianshan API — it does not write any files.

## Authentication

| Env Var | Required | Purpose |
|---------|----------|---------|
| `KUNGFU_OPENKEY` | **Yes** | API token for Tianshan API, sent as `Authorization: Bearer <token>` |
| `KUNGFU_PLATFORM` | No | Platform identifier header (default: `openclaw`) |

### Optional Research Search Credentials

These are **separate** from `KUNGFU_OPENKEY` and only needed when research search is enabled:

| Env Var | Purpose |
|---------|---------|
| `KUNGFU_ENABLE_RESEARCH_SEARCH` | Set to `1` to enable search |
| `KUNGFU_RESEARCH_SEARCH_PROVIDER` | Provider name (`web_search`) |
| `KUNGFU_RESEARCH_SEARCH_ENDPOINT` | Search service URL |
| `KUNGFU_RESEARCH_SEARCH_API_KEY` | Search service credential |
| `KUNGFU_RESEARCH_SEARCH_TIMEOUT_MS` | Search request timeout (default: 15000) |

When search is enabled, requests are POSTed as JSON to `KUNGFU_RESEARCH_SEARCH_ENDPOINT` with `KUNGFU_RESEARCH_SEARCH_API_KEY` as Bearer token.

### Non-Secret Tuning Variables

| Env Var | Purpose |
|---------|---------|
| `KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS` | Set to `1` to enable unreleased products |
| `KUNGFU_RESEARCH_DEFAULT_TARGET_DATE` | Override default research date (YYYYMMDD, for testing) |

### Rollout Status

- Only revalidated products are enabled by default
- Experimental products require `KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS=1`
- Preview `stock-research` / `sector-research` produce `markdown_svg_preview` with explicit degradation sections

## Data Handling

This skill sends user requests and locally assembled analysis context to the upstream Tianshan API.

Do not use it with:

- passwords
- API keys
- private documents
- personal data
- non-public trading positions

Use non-sensitive public market queries only unless you trust the upstream operator and data handling policy.

## Scope

Supported:

- Mainland China A-shares
- single-stock analysis for direct market-data products
- preview single-stock deep research with explicit degradation reporting
- preview single-sector deep research with explicit degradation reporting and `sector_name` / `sector_id` selectors
- single-sector or single-theme analysis
- controlled strategy whole-market result lookup
- deterministic data lookup
- first-stage bucket workflow for listing current-user buckets and adding instruments
- phase-2 strategy workflow for querying public/private strategies and controlled strategy whole-market results
- first-stage researcher workflow for ranking and report lookup
- first-stage bayesian monitor workflow for listing existing tasks and reading one task's report

Not supported:

- US stocks
- Hong Kong stocks
- crypto
- futures
- forex
- arbitrary whole-market screening outside the controlled strategy market-select path

## Publisher & Operator

- **Publisher**: [kungfu-trader](https://github.com/kungfu-trader)
- **Source code**: [github.com/kungfu-trader/kungfu-skills](https://github.com/kungfu-trader/kungfu-skills)
- **Tianshan API operator**: kungfu-trader (same organization that publishes this skill)
- **EastMoney / Tencent APIs**: Public free market data APIs operated by East Money Information (东方财富信息) and Tencent Holdings (腾讯控股) respectively — widely used public financial data sources in China

The `KUNGFU_OPENKEY` is only sent to `tianshan-api.kungfu-trader.com` (the publisher's own API). It is never sent to EastMoney, Tencent, or any other third party. The EastMoney and Tencent APIs require no authentication.

## Trust Notes

- All outbound network endpoints are listed in the table above — the code contacts no other hosts
- Required runtime: Node.js 22.24.0+
- Optional runtime: `inkscape` (for SVG→PNG chart conversion; gracefully degrades if absent)
- The package contains bundled `.mjs` scripts (not instruction-only) with zero npm dependencies
- File writes are limited to: `~/.openclaw/workspace/finance-master/charts/` (indicator charts) and `~/.openclaw/.env` (config-openkey only)
- The only subprocess invocation is `execFileSync("inkscape", [...])` — uses `execFileSync` (not shell `exec`) with fixed arguments, no user input in the command

If you are reviewing this skill for installation or registry approval, inspect:

**Network I/O files (these are the ONLY files that make outbound HTTP requests):**

- `scripts/core/http_client.mjs` — Tianshan API client (uses `KUNGFU_OPENKEY`, contacts only `tianshan-api.kungfu-trader.com`)
- `scripts/flows/run_health_flow.mjs` — Health check client (uses `KUNGFU_OPENKEY`, contacts only `tianshan-api.kungfu-trader.com/api/openclaw/keys/test`)
- `scripts/flows/run_check_update_flow.mjs` — ClawHub version check (no auth, contacts `wry-manatee-359.convex.site` or `clawhub.ai`)
- `scripts/flows/research_shared/public_api.mjs` — EastMoney/Tencent public API client (no auth, contacts only `push2.eastmoney.com`, `push2his.eastmoney.com`, `qt.gtimg.cn`, `ifzq.gtimg.cn`)
- `scripts/flows/research_shared/search_runtime.mjs` — Optional search client (contacts only user-configured `KUNGFU_RESEARCH_SEARCH_ENDPOINT`, gated by `KUNGFU_ENABLE_RESEARCH_SEARCH=1`)

**File write locations (complete list):**

- `scripts/flows/run_indicator_chart_flow.mjs` — writes SVG/PNG to `~/.openclaw/workspace/finance-master/charts/`
- `scripts/flows/run_health_flow.mjs` — writes `KUNGFU_OPENKEY` to `~/.openclaw/.env` (config-openkey command only)

**Subprocess invocation (complete list):**

- `scripts/flows/charts/svg_to_png.mjs` — `execFileSync("inkscape", [svgPath, "--export-type=png", ...])` with fixed arguments, called by `run_indicator_chart_flow.mjs`

**Entry point files:**

- `scripts/core/runtime.mjs` — Environment variable reading (no network I/O)
- `scripts/flows/run_data_request.mjs`
- `scripts/flows/run_bucket_flow.mjs`
- `scripts/flows/run_strategy_flow.mjs`
- `scripts/flows/run_researcher_flow.mjs`
- `scripts/flows/run_bayesian_monitor_flow.mjs`
- `scripts/flows/run_stock_research_flow.mjs`
- `scripts/flows/run_sector_research_flow.mjs`
- `scripts/flows/run_health_flow.mjs`

**Quick network audit**: Run `grep -rn 'https://' scripts/ | grep -v 'svg\|xmlns\|comment'` to verify no unlisted hosts are contacted.

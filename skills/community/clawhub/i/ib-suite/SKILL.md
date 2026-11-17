---
name: ib-suite
description: Read-only Interactive Brokers toolchain index and onboarding. Use when orienting across the ib-suite skills, running first-run setup (venv + live/paper config), or deciding which IB skill to run and in what order: ib-sync ingestion, live account/positions/daily-P&L/options overviews, Flex trade or dividend history, or the offline ib-analyze report. It runs nothing itself — the sub-skills do the work and never place, modify, or cancel an order.
metadata:
  openclaw:
    always: true
    requires:
      bins: [python3]
    os: [darwin, linux]
---

# ib-suite — Interactive Brokers read-only toolchain

This directory is a **read-only** IB (Interactive Brokers) diagnostics toolchain:
pull account data from IB, land it in a local data lake, and turn it into a
graded portfolio-diagnostics report. **Nothing here ever places, modifies, or
cancels an order.** Ingestion connects with `readonly=True`; analysis never
touches the network.

This SKILL.md is the entry point. It does not run anything itself — it tells you
(and OpenClaw) which sub-skill to run, in what order, and how the pieces fit.

## 0. First-run setup

Before running any sub-skill, make sure a config exists. This index owns
onboarding; the sub-skills stay gated until `config.yaml` is present.

1. **Detect.** If `.ib-suite/config.yaml` already exists, config is ready —
   skip to §2. Otherwise continue.
   ```bash
   test -f .ib-suite/config.yaml && echo "config ready" || echo "needs setup"
   ```
2. **Ensure the venv** (only if missing):
   ```bash
   test -d {baseDir}/.venv || bash {baseDir}/scripts/setup_venv.sh
   ```
3. **Ask the user one question:** connect to **live** (real account, port 4001)
   or **paper** (simulated, port 4002)? Default is **live** — every connection
   in this toolchain is `readonly=True`, so live is read-only too.
4. **Generate the config** with the chosen mode (defaults to live):
   ```bash
   {baseDir}/.venv/bin/python {baseDir}/scripts/init_config.py \
     --mode live --out .ib-suite/config.yaml
   ```
   It refuses to overwrite an existing config unless you add `--force`.
5. **Report back:** the config path and the resulting mode/port. Remind the
   user to start IB Gateway with **Read-Only API** enabled before `/ib-sync`,
   and that `ib-trade-history` and `ib-dividend-income` share one Flex token but
   keep separate per-window Query ID maps in ignored local config (`flex.token`
   with `flex.trade_history_query_ids` / `flex.dividend_query_ids`); never echo
   either credential.
6. Proceed to §2 and run `/ib-sync` → `/ib-analyze`.

Runtime config and data stay workspace-local under `<workspace>/.ib-suite/`
(gitignored); the skill dir ships only code and `config.example.yaml`.

## 1. Directory overview

| Component | What it is | Runs a command? | Network? |
|---|---|---|---|
| [ib-common]({baseDir}/ib-common) | Shared `pip`-installable package (config / schema / storage / metrics / charts). **Not a skill.** | No | No |
| [ib-gateway]({baseDir}/ib-gateway) | Read-only ingestion skill → `/ib-sync` | Yes | Yes (IB Gateway / Flex) |
| [ib-account-overview]({baseDir}/ib-account-overview) | Read-only account financial overview skill → `/ib-account-overview` | Yes | Yes (IB Gateway) |
| [ib-positions-overview]({baseDir}/ib-positions-overview) | Read-only enriched positions overview skill → `/ib-positions-overview` | Yes | Yes (IB Gateway) |
| [ib-daily-pnl]({baseDir}/ib-daily-pnl) | Read-only daily (today's) P&L breakdown skill → `/ib-daily-pnl` | Yes | Yes (IB Gateway) |
| [ib-trade-history]({baseDir}/ib-trade-history) | Read-only Flex Query execution-history skill → `/ib-trade-history` | Yes | Yes (Flex Web Service) |
| [ib-dividend-income]({baseDir}/ib-dividend-income) | Read-only Flex-only paid/expected dividend-income skill → `/ib-dividend-income` | Yes | Yes (Flex Web Service) |
| [ib-options-overview]({baseDir}/ib-options-overview) | Read-only option positions and Greeks overview skill → `/ib-options-overview` | Yes | Yes (IB Gateway) |
| [ib-portfolio-analyst]({baseDir}/ib-portfolio-analyst) | Offline diagnostics skill → `/ib-analyze` | Yes | No |

```
skills/ib-suite/
  SKILL.md                 # <- you are here (index / router)
  scripts/setup_venv.sh    # shared venv bootstrap (installs ib-common editable)
  ib-common/               # shared library (installed editable into .venv)
  ib-gateway/              # /ib-sync   : IB/Flex -> local data lake
  ib-account-overview/     # /ib-account-overview: IB account -> financial overview (no persistence)
  ib-positions-overview/   # /ib-positions-overview: IB positions -> enriched, ranked overview (no persistence)
  ib-daily-pnl/            # /ib-daily-pnl: IB live P&L -> today's realized/unrealized, ranked (no persistence)
  ib-trade-history/        # /ib-trade-history: Flex executions -> stdout JSON (no persistence)
  ib-dividend-income/      # /ib-dividend-income: Flex dividends -> stdout JSON (no account-data persistence)
  ib-options-overview/     # /ib-options-overview: IB live options -> Greeks and risk overview (no persistence)
  ib-portfolio-analyst/    # /ib-analyze: data lake -> report.md + charts
```

**Scope.** In: read-only sync, snapshots, Parquet history, and P0–P3 findings
across account health, concentration, P&L attribution, trade review, portfolio
risk, pre-trade simulation, and Flex-only dividend income. **Out (hard boundary):** order
placement/modification/cancellation, live WhatIf margin checks, real-time market
data, and any write path to IB. Do not add these under the banner of
"completeness".

## 2. Run guide

Dependency direction: `ib-common` ← `ib-gateway` (produces data) ← `ib-portfolio-analyst` (consumes data).

```
setup_venv.sh        ->  ib-gateway /ib-sync      ->  ib-portfolio-analyst /ib-analyze
(install ib-common)      (write data lake)             (read lake -> report)
```

1. **Setup once (or after dependency changes).** Bootstraps the shared `.venv`
   and installs `ib-common` (editable) plus runtime deps. Idempotent.
   ```bash
   bash {baseDir}/scripts/setup_venv.sh
   # config.yaml is created by "0. First-run setup" (writes .ib-suite/config.yaml)
   ```

   **Runtime data lives outside the skill dir.** Keep the real `config.yaml` and
   the data lake under the workspace, e.g. `<workspace>/.ib-suite/config.yaml`
   and `<workspace>/.ib-suite/data/` (set `storage.root: .ib-suite/data`). The
   skill directory ships only code and `config.example.yaml`; reinstalling the
   skill must never overwrite user data. Entry scripts take explicit `--config`
   / `--out` and don't depend on the current working directory.

2. **Ingest (ib-gateway, online).** Start IB Gateway (paper 4002 / live 4001)
   with API access, then run `/ib-sync`. Writes `data/snapshots/<account>/<ts>.json`
   and appends `data/timeseries/positions_history.parquet`. See
   [ib-gateway/SKILL.md]({baseDir}/ib-gateway/SKILL.md).
3. **Analyze (ib-portfolio-analyst, offline).** Run `/ib-analyze` against a
   snapshot to produce `report.md` + `.html`/`.png` charts. See
   [ib-portfolio-analyst/SKILL.md]({baseDir}/ib-portfolio-analyst/SKILL.md).

**Which skill do I run?**

| You want to… | Run |
|---|---|
| Refresh account/position data from IB | `ib-gateway` → `/ib-sync` |
| See account equity, margin, liquidity & P&L right now | `ib-account-overview` → `/ib-account-overview` |
| List every position, ranked, with the most concentrated name | `ib-positions-overview` → `/ib-positions-overview` |
| See how the account did today and which names drove it | `ib-daily-pnl` → `/ib-daily-pnl` |
| List historical fills, commission, realized P&L and win/loss statistics | `ib-trade-history` → `/ib-trade-history` |
| See paid/expected dividends, tax, attribution, annual income and yield | `ib-dividend-income` → `/ib-dividend-income` |
| Configure shared Flex credentials or dividend query fields | `ib-dividend-income` → `/ib-dividend-income` setup guide |
| Inspect option holdings, IV, Greeks, expiry exposure, and concentration | `ib-options-overview` → `/ib-options-overview` |
| Produce a diagnostic report from existing data | `ib-portfolio-analyst` → `/ib-analyze` |
| Test any skill without IB | its `tests/` fixtures (see §5) |

**Note on optional inputs.** `/ib-sync` v1 lands only the account snapshot and
positions. Daily bars, executions, and dividends are optional JSON arrays
(matching the `DailyBar` / `Execution` / `Dividend` schema, e.g. exported from a
Flex report) that you pass to `/ib-analyze` directly; the corresponding report
sections appear only when their data is supplied.

## 3. Sub-skill module spec

Every functional sub-skill directory (`ib-gateway`, `ib-portfolio-analyst`, and
any future one) MUST follow this contract:

- **`SKILL.md` with valid frontmatter.** Required `name` + `description`, and
  `metadata.openclaw` (`requires.bins`, `requires.config`, `os`) so OpenClaw can
  discover and gate it. `name` MUST equal the directory name (lowercase, stable).
- **`description` states the read-only boundary.** Start with "Read-only", say
  what it does and when it triggers, and stay narrow enough to avoid mis-firing.
- **`scripts/` holds the deterministic entry logic.** Use `argparse`; validate
  required args; exit non-zero with an actionable message on failure. Commands in
  `SKILL.md` use the `{baseDir}` placeholder and `.venv/bin/python` — never
  absolute or hardcoded user paths.
- **Network/IB access hides behind an injectable factory** (`client_factory`,
  `http_get`) so `tests/` run fully offline against `fixtures/`.
- **Reuse `ib-common`, don't fork it.** Types come from `ib_common.schema`
  (pydantic v2); reuse `Finding`, `grade()`, `thresholds`, storage helpers, and
  `render()` for charts. New diagnostic modules live in `ib_analyst/`, expose
  `analyze(...) -> list[Finding]` with a module-level `DIM` constant and an
  optional `build_chart(...) -> plotly.Figure`, and are wired into
  `analyze.py`'s `run()`. New thresholds MUST also be added to
  `ib-common/config.example.yaml` under `thresholds:`.
- **`from __future__ import annotations`** at the top of every module; type-annotate
  functions; docstring public functions.

## 4. Invocation

**As OpenClaw slash commands (primary).** Once discovered, the sub-skills expose
`/ib-sync`, `/ib-account-overview`, `/ib-positions-overview`, `/ib-daily-pnl`,
`/ib-trade-history`, `/ib-dividend-income`, `/ib-options-overview`, and
`/ib-analyze`. Gating is driven by each skill's `metadata.openclaw` (`python3`
on `PATH`, a `config.yaml`, and a supported OS).

**As direct scripts (for automation / other systems).** Call the entry scripts
with the shared interpreter; they print structured, parseable results (dicts /
output paths) to stdout and return non-zero on failure:

```bash
# ingest
{baseDir}/.venv/bin/python {baseDir}/ib-gateway/scripts/ib_sync.py --config .ib-suite/config.yaml

# historical Flex executions (default: latest 7 calendar days)
{baseDir}/.venv/bin/python {baseDir}/ib-trade-history/scripts/trade_history.py \
  --config .ib-suite/config.yaml

# Flex-only dividend income (inclusive dates are required)
{baseDir}/.venv/bin/python {baseDir}/ib-dividend-income/scripts/dividend_income.py \
  --config .ib-suite/config.yaml \
  --start-date 2026-01-01 \
  --end-date 2026-07-19

# analyze (bars/executions/dividends optional)
{baseDir}/.venv/bin/python {baseDir}/ib-portfolio-analyst/scripts/analyze.py \
  --config .ib-suite/config.yaml \
  --snapshot data/snapshots/<account>/<ts>.json \
  --out data/runs/$(date +%Y%m%dT%H%M%S)
```

**As a library.** `import ib_common` (installed editable) for config/schema/
storage/metrics/charts. `ib-trade-history` and `ib-dividend-income` share the
Flex token but keep separate per-window Query ID maps (`flex.token` with
`flex.trade_history_query_ids` / `flex.dividend_query_ids`) in ignored
local config. The dividend skill requires numeric windows and its standalone
field/window guide is
[ib-dividend-income/flex-query-setup.md]({baseDir}/ib-dividend-income/flex-query-setup.md).
Never hardcode or echo tokens, Query IDs, account numbers, or user paths.

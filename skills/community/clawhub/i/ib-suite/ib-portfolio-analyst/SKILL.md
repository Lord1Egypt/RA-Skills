---
name: ib-portfolio-analyst
description: "Read-only IB diagnostics: account health, concentration, P&L attribution, trade review, portfolio risk, pre-trade check — a P0-P3 findings report with charts."
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-portfolio-analyst

Turns the local data lake (populated by `ib-gateway`) into a structured
P0–P3 diagnostic report. Never contacts IB and never places orders — it
reads snapshots, bars and executions that were already synced.

## Prerequisite

Config and the shared venv are owned by the `ib-suite` index skill (see its
first-run setup). Run `ib-gateway`'s `/ib-sync` first so a snapshot exists under
`data/snapshots/`.

> **v1 input note:** `/ib-sync` currently lands only the account snapshot and
> positions. Daily bars, executions and dividends are **optional JSON inputs**
> you supply directly (arrays matching the `DailyBar` / `Execution` / `Dividend`
> schema — e.g. exported from a Flex report). Landing them into the lake as a
> `/ib-sync` step is deferred to a later iteration.

## /ib-analyze — run all diagnostics

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/analyze.py \
  --config .ib-suite/config.yaml \
  --snapshot data/snapshots/<account>/<ts>.json \
  --bars bars.json \
  --executions executions.json \
  --out data/runs/$(date +%Y%m%dT%H%M%S)
```

Produces `report.md` plus interactive `.html` and static `.png` charts in the
output directory. `--bars`/`--executions` are optional JSON arrays; the risk
and trade-review sections appear only when their data is supplied.

### Dividends

Pass Flex-sourced dividend history (a JSON array of `Dividend` rows) to include
income diagnostics:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/analyze.py \
  --config .ib-suite/config.yaml \
  --snapshot data/snapshots/<account>/<ts>.json \
  --dividends dividends.json \
  --out data/runs/$(date +%Y%m%dT%H%M%S)
```

Adds Yield-on-Cost and withholding-tax findings plus an income-by-symbol chart.

> **Withholding-tax note (v1):** the Flex parser does not yet extract the
> separate withholding-tax cash rows, so `tax` defaults to `0` unless you set
> it in the supplied JSON. The withholding-drag finding therefore reads 0%
> against unedited Flex output until tax parsing lands in a later iteration.

## Findings

Each finding carries: priority (P0–P3), dimension, finding, evidence,
impact, suggestion, trigger condition, confidence, and data limitations.
Findings are diagnostic and directional only — never return promises.

## Notes

- All thresholds live in `config.yaml` under `thresholds:` (see ib-common's `config.example.yaml`).
- Pre-trade check is a **separate local simulation** (`ib_analyst.pretrade_check.simulate`), not part of the `/ib-analyze` auto report — it estimates post-trade weight/leverage for a hypothetical order. A real IB WhatIf margin check is planned for v2.

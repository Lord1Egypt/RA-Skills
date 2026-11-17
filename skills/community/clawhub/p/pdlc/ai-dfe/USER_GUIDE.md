# AI-DFE — User Guide

**Package:** AI-DFE — AI-Driven Data Fabric
**Version:** 1.0.0

A practical walkthrough of running the data fabric in your workspace.

---

## 1. What you get

After installing AI-DFE, your workspace has an empty `pdlc-ws/data/` folder. Once you run the fabric, that folder becomes the single read-point for all family data: clean JSON files plus a `REGISTRY.json` index. Anything that needs family data — a dashboard, a report, a status query — reads from here, never from raw source files.

---

## 2. First run

```
DHC__
```

Before populating anything, run the **health check** to confirm the workspace is ready for the data fabric. `DHC__` validates preconditions (DFE installed, `data/` territory bootstrapped, at least one package interface present), scans for real source data, checks operational readiness, and — if data exists — proves one gather→shape→distribute cycle. It returns a verdict:

- **HEALTHY** — DFE is fully operational; proceed to `DAT__ all`.
- **DEGRADED** — DFE can run with limitations (the report says which).
- **NOT READY** — DFE isn't installed or has no `data/` territory.
- **IDLE** — installed correctly, but no package has produced real data yet (run a lifecycle package first).

Then populate the surface:

```
DAT__ all
```

This triggers a full pass:
1. **Configure** — DFE discovers the family layout, reads each installed package's data interface (its `SOURCE_MAP.md` + schema), and scans `data/demands/` for consumer needs. Results are cached in `data/dfe-state.md`.
2. **Operate** — DFE gathers raw data into per-package JSON (Layer 1), shapes it into consumer outputs per each DEMAND (Layer 2), and writes everything to `data/` with an updated `REGISTRY.json`.
3. **Govern** — DFE validates each file against its schema and snapshots a copy into `data/history/`.

If a package hasn't been run yet, its data file is written with `null` fields rather than failing (graceful degradation).

---

## 3. Day-to-day commands

| Command | What it does |
|---------|--------------|
| `DAT__ all` | Full pass across all packages + demands |
| `DAT__ pdlc` | Refresh one family only |
| `DAT__ pdlc/pilc` | Refresh a single package |
| `DAT__ aggregate` | Re-shape consumer outputs from existing per-package data |
| `DAT__ status` | Report which data files are stale vs. their sources |
| `DAT__ discover` | Force re-discovery (re-read every SOURCE_MAP + schema) |
| `DAT__ validate` | Dry-run schema validation without writing |
| `DAT__ cleanup --before {ms-timestamp}` | Delete history snapshots older than a timestamp |
| `DAT__ master` / `DAT__ master --set {family}` | Report / set the master DFE (multi-family) |
| `DFA__` | Run the quality agent — a report-only health check |

---

## 4. Adding a consumer

A consumer (dashboard, extension, report) gets service from DFE by meeting a two-part contract — the same declare-and-discover model packages use.

**Obligation 1 — Register (so DFE discovers you).** Two pieces:
1. **Ship a demand declaration in your own folder:** `{your-home}/data-demand/{your-name}.demand.md` (copy `demand-template.md`). Declare the output file name, the fields you need (field path, type, source domain), and your refresh expectation. The contract travels with the consumer — the same way a package ships its `data-schema/SOURCE_MAP.md`.
2. **Register in the index:** add a row to `pdlc-ws/data/CONSUMER_REGISTRY.md` (`consumer`, `home`, `demandFile`, `outputFile`, `registeredOn`). For family-shipped tools/extensions this is automatic — the installer scans `tools/extensions/*/data-demand/` and registers each at install. Ad-hoc/manual consumers can instead drop a `*.demand.md` straight into `pdlc-ws/data/demands/` (the escape hatch; recorded as `registered: false`).

**Obligation 2 — Resolve, never hardcode.** In your consumer, know ONE fixed path — `pdlc-ws/data/REGISTRY.json` — find your file's entry there, and load the path it reports. Never hardcode `pdlc-ws/data/{your-name}.json`.

Then run `DAT__ all` (or `DAT__ aggregate`). DFE discovers your demand from the registry, produces `data/{your-name}.json`, and registers it in `REGISTRY.json`.

> **Reference adopter:** the AIFLC-PDLC-Dashboard ships `data-demand/dashboard-data.demand.md`, auto-registers on install, and resolves its data via `REGISTRY.json` (VS Code host and standalone HTML alike).

---

## 5. How freshness works

DFE uses discover-once, monitor-continuously. The first encounter with a package reads its full interface (expensive). After that, DFE only compares source-file timestamps against the last-generated time (cheap). It re-reads a package's interface only when its `SOURCE_MAP.md` or schema changes, on `DAT__ discover`, or on a schema-version mismatch.

---

## 6. History & cleanup

Every write snapshots the file into `data/history/` with a millisecond timestamp. Retention is forever by default; a package may declare its own retention policy in its SOURCE_MAP. Prune with `DAT__ cleanup --before {timestamp}`.

---

## 7. Quality checks

Run `DFA__` any time for a standalone integrity report — 18 checks across 5 categories (the data-layer analogue of AI-FLO's `FIA__`):
- `DFA__ schema` — envelope validity, schema validation, version match, producer attribution
- `DFA__ registry` — no phantom/unlisted entries, path resolution, cross-family validity
- `DFA__ manifest` — REGISTRY ↔ DATA_INTERFACES, schema coverage, consumer mapping
- `DFA__ freshness` — staleness, discovery currency, demand currency, not-run transparency
- `DFA__ territory` — single-writer, history integrity, demand-only contributions, correlation keys

`DFA__` never writes data — it only reports (boxed report + per-finding `DAT__` fix). Use `DAT__` to fix what it finds.

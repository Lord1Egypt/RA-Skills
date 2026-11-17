# Stage 2.3 — Distribute

> Phase 2 (Operate). Write all staged outputs to `data/`, refresh `REGISTRY.json`, snapshot to `history/`.

## Purpose

Commit the validated outputs (from 2.1 and 2.2) to DFE's territory as the single read-point, and keep the registry accurate.

## Inputs

- Staged, validated `{pkg}-data.json` (Layer 1) and `{consumer-output}.json` (Layer 2).
- The current timestamp for this pass (ISO-8601 + epoch-ms), obtained once via the shell command in core-engine "Obtaining the Current Timestamp" — never from an internal/hosted time tool.

## Logic

1. Write each validated file to `{family}-ws/data/`.
2. **Re-derive `REGISTRY.json`** from what was actually written — for every file: `path`, `schema` (workspace-root-relative, `.kiro/{family}/ai-{pkg}-rule-details/data-schema/…` for per-package or `{family}-ws/data/…` for DFE-owned), `package`, `family`, and `consumer` (for demand outputs). In master mode, populate `cross-family`.
3. Snapshot each written file into `history/{epoch-ms}_{file}.json` (3.3).
4. Update `DATA_INTERFACES.md` (human-readable manifest) to match the registry.
5. Update `dfe-state.md`: set `lastGenerated` for each produced package/demand.

## Output

Updated `data/` surface: data files + `REGISTRY.json` + `DATA_INTERFACES.md` + `history/` snapshots + refreshed `dfe-state.md`.

## Rules

- DFE is the sole writer — no other entity writes here.
- `REGISTRY.json` is always re-derived, never hand-patched.
- No consumer-facing path is hardcoded anywhere; consumers resolve everything through `REGISTRY.json`.

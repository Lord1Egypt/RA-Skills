# Schema README — AI-ADLC (`adlc-data.json`)

**Package:** AI-ADLC — AI-Driven Architecture Design Life Cycle
**Schema:** `adlc-data.schema.json`
**Version:** 1.0.0
**Produced file:** `{family}-ws/data/adlc-data.json`
**Scope:** per-project (one data entry per project, keyed by `projectId`)

---

## Purpose

`adlc-data.json` is the machine-readable projection of AI-ADLC's per-project architecture output. It exposes system topology (containers), ADRs, constraints, progress, and governance entries — so dashboards, DWG pre-checks, and portfolio views can consume structured architecture data without parsing design documents.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `projectId` | `adlc-state.md` | Correlation key |
| `status` | `adlc-state.md` | Is architecture complete? |
| `containers[]` | `adlc-state.md` Containers table | System topology — what DWG generates from |
| `adrs[]` | `adlc-state.md` ADR Register | Architecture decisions (count, status, titles) |
| `enabledExtensions[]` | `adlc-state.md` | Which advanced patterns are active (DDD, microservices, etc.) |
| `progress[]` | `adlc-state.md` Progress table | Per-stage status |
| `decisions[]` / `issues[]` / etc. | Management framework registers | Governance spine entries prefixed `ADLC-{ABBREV}-*` |

## Consumers

- Family-status demand (portfolio roll-up).
- AIFLC-PDLC-Dashboard (architecture card + ADR count + container map).
- AI-DWG pre-flight readiness checks (are all required stages complete?).
- `DFA__` freshness checks.

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |

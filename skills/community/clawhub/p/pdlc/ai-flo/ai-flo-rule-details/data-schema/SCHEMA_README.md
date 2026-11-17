# Schema README — AI-FLO (`flo-data.json`)

**Package:** AI-FLO — AI-Driven Flow Orchestrator
**Schema:** `flo-data.schema.json`
**Version:** 1.0.0
**Produced file:** `{family}-ws/data/flo-data.json`
**Scope:** family (one file covers all tracked projects)

---

## Purpose

`flo-data.json` is the machine-readable projection of AI-FLO's routing state. It gives dashboards and portfolio views a structured snapshot of where every project sits in the chain, which routes are active, which packages are detected, and overall orchestration health — without parsing `flo-state.md` or `routing-table.md` directly.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `topologyMode` | `flo-state.md` front-matter | Which workspace topology is active (1/2/3) |
| `configuration` | `flo-state.md` Configuration table | Hold timeout, stall threshold, roll-up schedule |
| `projects[]` | `flo-state.md` per-project sections | Position, status, next hop, priority per project |
| `routes[]` | `routing-table.md` Canonical Routes | The chain graph (which package connects to which) |
| `fanInRules[]` | `routing-table.md` Fan-In Rules | DWG fan-in requirements |
| `packageAvailability[]` | `routing-table.md` | Which packages are installed/detected |
| `routingLogEntryCount` | `routing-log.md` | Volume indicator (how active is routing) |

## Consumers

- Family-status demand (are projects flowing or stuck?).
- AIFLC-PDLC-Dashboard (chain visualization + per-project position).
- AI-PPM (portfolio health — which projects are stalled?).
- `DFA__` freshness checks.

## Notes

- FLO's data is family-scoped (not per-project) because FLO tracks ALL projects in one state file.
- `routing-log.md` is append-only and can be large; only the entry count is extracted (not full content). Consumers needing the log should read it directly.
- `conflict-alerts/` and `readiness-checks/` are not read in v1.0 — future schema version may add counts.

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |

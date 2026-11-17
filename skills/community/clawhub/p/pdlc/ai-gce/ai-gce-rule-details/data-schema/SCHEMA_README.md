# Schema README — AI-GCE (`gce-data.json`)

**Package:** AI-GCE — AI-Driven Governance & Compliance Engine
**Schema:** `gce-data.schema.json` · **Version:** 1.0.0
**Produced file:** `{family}-ws/data/gce-data.json` · **Scope:** per-project

## Purpose

Machine-readable projection of AI-GCE's per-project compliance state — tier, score, tier-readiness, active agents, and latest audit — for governance dashboards and portfolio compliance roll-ups. Sourced primarily from the structured `.compliance-state.json`.

## Key Fields

| Field | Source | Use |
|-------|--------|-----|
| `complianceTier` / `complianceScore` | `.compliance-state.json` | Compliance posture |
| `nextTierReadiness` | `.compliance-state.json` | Path to next tier + blockers |
| `agents[]` / `activeAgentCount` | `AGENT_REGISTRY.md` | Active governance agents |
| `lastAuditScore` / `lastAuditRating` | compliance-log snapshot | Latest audit result |

## Consumers
Family-status demand · AIFLC-PDLC-Dashboard (compliance card) · `DFA__`.

## Notes
The append-only JSONL compliance-log is not fully extracted — only the latest snapshot summary. `projectId` keys GCE events (read from the dev workspace's `workspace-rules.md`).

## Version History
| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-22 | Initial schema. |

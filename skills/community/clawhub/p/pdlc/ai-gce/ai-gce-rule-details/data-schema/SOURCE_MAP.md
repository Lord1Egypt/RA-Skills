# SOURCE_MAP — AI-GCE

> Declares where AI-GCE's raw output lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`. GCE runs inside the generated dev workspace.

**Package:** AI-GCE — AI-Driven Governance & Compliance Engine
**Schema:** `gce-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project (runs inside one dev workspace)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.compliance-state.json` | `status: not-run` → GCE not initialized; payload `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.compliance-state.json` | tier, score, phase, tier history, next-tier readiness, dashboard summary |
| 2 | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.governance/AGENT_REGISTRY.md` | active agents + tiers |
| 3 | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.governance/compliance-log/snapshots/` | latest audit snapshot |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `projectName` | 1 | `.compliance-state.json` → `projectName` |
| `currentPhase` | 1 | → `currentPhase` |
| `complianceTier` | 1 | → `complianceTier` (1/2/3) |
| `startDate` | 1 | → `startDate` |
| `complianceScore` | 1 | → `complianceScore` (0-100 or null) |
| `lastAudit` | 1 | → `lastAudit` |
| `tierHistory[]` | 1 | → `tierHistory` array: `{ tier, activatedDate, activatedBy, scoreAtActivation }` |
| `nextTierReadiness` | 1 | → `nextTierReadiness`: `{ tier, criteriaMetCount, criteriaTotalCount, blockers[] }` |
| `dashboard.summary` | 1 | → `dashboard.summary` |
| `dashboard.scoreHistory[]` | 1 | → `dashboard.scoreHistory` array |
| `activeAgentCount` | 2 | Count of rows in AGENT_REGISTRY Active Agents table with Status=Active |
| `agents[]` | 2 | One object per active-agent row: `{ id, agent, type, trigger, tier, status }` |
| `lastAuditScore` | 3 | Latest snapshot → `score` (if present) |
| `lastAuditRating` | 3 | Latest snapshot → `rating` |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- GCE is per-project scoped: one `gce-data.json` per project. `.compliance-state.json` is the authoritative source (structured JSON — easy to extract).
- The append-only JSONL compliance-log is NOT fully read (too large/high-churn); DFE reads only the latest snapshot summary. Consumers wanting the event stream read the log directly.
- `projectId` correlation: GCE keys its log events on `projectId` (read from the dev workspace's `workspace-rules.md`); DFE joins GCE data to a project via the dev-workspace path + that ID.

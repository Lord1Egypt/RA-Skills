# SOURCE_MAP — AI-FLO

> Declares where AI-FLO's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`.

**Package:** AI-FLO — AI-Driven Flow Orchestrator
**Schema:** `flo-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** family (not per-project — FLO tracks ALL projects in one state file)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `_FLO_/flo-state.md` | `status: not-run` → all payload fields `null` |

> **Note:** AI-FLO's output lives at `pdlc-ws/_FLO_/` (workspace level under the family workspace, not under `projects/`). It is a family-wide orchestrator, not a per-project producer.

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `_FLO_/flo-state.md` | topology mode, configuration parameters, per-project positions + statuses |
| 2 | `_FLO_/routing-table.md` | canonical routes, fan-in rules, per-project profiles, package availability |
| 3 | `_FLO_/routing-log.md` | append-only audit trail of routing events |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `topologyMode` | 1 | Front-matter → `topology_mode` value (1/2/3) |
| `version` | 1 | Front-matter → `version` value |
| `created` | 1 | Front-matter → `created` value (ISO date) |
| `lastUpdated` | 1 | Front-matter → `last_updated` value (ISO date) |
| `configuration.holdTimeout` | 1 | Configuration table → `Hold Timeout` row |
| `configuration.optionalFeedWait` | 1 | Configuration table → `Optional-Feed Wait` row |
| `configuration.stallThreshold` | 1 | Configuration table → `Stall Threshold` row |
| `configuration.autoResolveRule` | 1 | Configuration table → `Auto-Resolve Rule` row |
| `configuration.rollUpSchedule` | 1 | Configuration table → `Roll-Up Schedule` row |
| `projects[]` | 1 | Per `## Project:` section → one object: `{ projectId, workspaceRef, currentPackage, currentStatus, nextHop, priority, dispatched, lastActivity, profile, reworkCount }` |
| `projects[].toggles[]` | 1 | Active Toggles table per project: `{ package, status, toggled, reason, operator }` |
| `projects[].positionHistory[]` | 1 | Position History table per project: `{ date, from, to, trigger, operator }` |
| `routes[]` | 2 | Canonical Routes table → one object per row: `{ id, from, to, type, condition, active }` |
| `fanInRules[]` | 2 | Fan-In Rules table → `{ target, requiredFeeds, optionalFeeds, minimumReadiness }` |
| `packageAvailability[]` | 2 | Package Availability table → `{ package, detected, markerLocation }` |
| `routingLogEntryCount` | 3 | Line count of non-header rows (advisory — precise entry count) |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- FLO is **family-scoped** (not per-project): one `flo-data.json` for the whole family, containing all tracked projects.
- `_FLO_/` sits directly under `pdlc-ws/` (not under `projects/`). It is the family router, not a project producer.
- The routing-log is append-only and potentially large. DFE reads only the entry count — full log content is not extracted (too large for JSON; consumers wanting the log should read it directly).
- FLO has **no management_framework** — it is an orchestrator exempt from the project-producer model.
- `conflict-alerts/` and `readiness-checks/` are not read for the baseline schema (v1.0). Future schema version may extract active conflict/readiness counts.

# DEMAND — family-status

> Sample DEMAND fixture. At runtime this lives at `pdlc-ws/data/demands/family-status.demand.md`. AI-DFE shapes `family-status.json` from per-package JSON (Layer 2).

**Consumer:** family-status (generic family roll-up — used by reports, portfolio views, the `DFA__` agent)
**Output file:** `family-status.json`
**Refresh:** session-start
**Scope:** portfolio / family

---

## Fields Needed

| Field path (in output `data`) | Type | Source domain | Description |
|--------------------------------|------|---------------|-------------|
| `family` | string | (constant) | Family code (e.g. `pdlc`) |
| `counts.ideas` | integer | `ilc-data.counts.total` | Ideas in the funnel |
| `counts.projects` | integer | `ppm-data.summary.totalProjects` | Total projects |
| `counts.activeProjects` | integer | `ppm-data.summary.active` | Active projects |
| `counts.workspacesGenerated` | integer | aggregate `dwg-data.workspaceGenerated == true` | Dev workspaces generated |
| `health.projectsWithOpenRisks` | integer | aggregate `pilc-data`/`polc-data` risks | Projects with open risks |
| `health.avgComplianceScore` | number | aggregate `gce-data.complianceScore` | Mean compliance score |
| `health.avgTestCoverage` | number | aggregate `tge-data.registerStats.coverage` | Mean test coverage |
| `health.stalledProjects` | integer | aggregate `flo-data.projects` (stalled) | Stalled projects |
| `lastRefreshed` | string | (generated) | Timestamp of this roll-up |

## Shape Notes

- Pure aggregation — one object summarizing the whole family.
- Averages computed across projects that have the relevant data (null-skipping).

## How This Consumer Reads Its Data (HARD RULE)

1. Know ONE path: `pdlc-ws/data/REGISTRY.json`.
2. Read the registry, find `family-status.json`, get its `path`.
3. Open that path and read the JSON.
4. NEVER hardcode the data-file path.

## Schema

AI-DFE owns the validating schema: `pdlc-ws/data/family-status.schema.json`.

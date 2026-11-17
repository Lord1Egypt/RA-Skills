# SOURCE_MAP — AI-TGE

> Declares where AI-TGE's raw output lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`. TGE runs inside the generated dev workspace.

**Package:** AI-TGE — AI-Driven Test Governance Engine
**Schema:** `tge-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project (companion inside one dev workspace)

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.governance/test/tge-state.md` | `status: not-run` → TGE not initialized; payload `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/.governance/test/tge-state.md` | engine status, register stats, risk summary, depth, observation history |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `mode` | 1 | Engine Status → `Mode` (Full Chain/Architecture Only/Brownfield/Observation Only) |
| `currentPhase` | 1 | Engine Status → `Current Phase` (Strategy/Observation/Complete) |
| `lastStageCompleted` | 1 | Engine Status → `Last Stage Completed` (1-12) |
| `lastUpdated` | 1 | Engine Status → `Last Updated` |
| `engineVersion` | 1 | Engine Status → `Engine Version` |
| `registerStats.commitmentsTracked` | 1 | Register Stats → `Total Commitments Tracked` |
| `registerStats.testsRequired` | 1 | Register Stats → `Tests Required (active)` |
| `registerStats.testsExisting` | 1 | Register Stats → `Tests Existing` |
| `registerStats.testsMissing` | 1 | Register Stats → `Tests Missing` |
| `registerStats.testsFailing` | 1 | Register Stats → `Tests Failing` |
| `registerStats.coverage` | 1 | Register Stats → `Coverage` (percent) |
| `riskSummary` | 1 | Risk Summary → `{ critical, high, medium, low, totalScored }` |
| `depthLevel.level` | 1 | Depth Level → `Level` |
| `depthLevel.totalScore` | 1 | Depth Level → `Total Score` (n/25) |
| `observationHistory[]` | 1 | Observation History table → `{ cycle, date, testsAdded, testsDeprecated, coverageBefore, coverageAfter }` |

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- TGE is per-project scoped: one `tge-data.json` per project. `tge-state.md` is rich and structured — DFE extracts the stats/risk/coverage summary.
- Individual artifacts (`test-register.md`, `coverage-report.md`, `defect-log.md`) are not fully extracted — the state file already aggregates their key counts.
- TGE carries `ownership: generated` provenance front-matter (`generatedBy: AI-TGE`).

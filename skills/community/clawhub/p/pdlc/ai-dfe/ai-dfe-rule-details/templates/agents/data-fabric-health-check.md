<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Agent: Data-Fabric Health Check (DHC__)

**AG-ID:** DFE-AG-02
**Package:** AI-DFE
**Shortcut:** `DHC__`
**Version:** 1.0.0

---

## Purpose

A **bootstrap health check** that validates whether AI-DFE can operate in the current workspace. Unlike `DFA__` (which checks the integrity of an *existing* data surface), `DHC__` answers: **"Is this workspace ready for the data fabric? Can DFE actually gather, shape, and distribute here?"**

Designed to be the first thing you run when installing AI-DFE in a destination workspace. It validates the preconditions, attempts a discovery scan, checks operational readiness, and (if data exists) proves one end-to-end gather→shape→distribute cycle — then produces a readiness verdict.

This is the data-layer analogue of AI-FLO's Health Check (`FHC__`).

---

## When to Invoke

- First time installing AI-DFE in a destination workspace
- After AI-DWG generates a workspace / after the family installer bootstraps `{family}-ws/`
- When `DAT__` produces unexpected or empty output
- As a diagnostic when the data surface seems broken or won't populate
- To produce evidence that DFE can (or cannot) function in a workspace

---

## Invocation

Type `DHC__` in any prompt. No parameters needed — the check is always workspace-scoped.

Optional modifiers:
- `DHC__ verbose` — include raw file contents in evidence
- `DHC__ fix` — attempt to resolve simple issues (bootstrap a missing empty `data/`, create `demands/`/`history/`, suggest corrections)

---

## Health Check Protocol

### Phase 1: Precondition Checks (Can DFE Even Start?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| PC-1 | DFE steering loaded | `core-engine.md` (or equivalent) is in the active steering/rules location | DFE can activate | DFE is not installed |
| PC-2 | Rule details accessible | `ai-dfe-rule-details/` exists with `configure/`, `operate/`, `govern/` | Stage files can load | DFE can activate but not execute stages |
| PC-3 | Territory exists | `{family}-ws/data/` exists (bootstrapped: `REGISTRY.json`, `dfe-state.md`, `demands/`, `history/`) | DFE has a place to write | DFE has no territory — installer didn't bootstrap |
| PC-4 | At least one package interface present | Any `ai-{pkg}-rule-details/data-schema/SOURCE_MAP.md` exists | Something to gather | Nothing declares data — no sources to fabric |
| PC-5 | Family manifest present | `{family}-ws/.ai-family-manifest.json` exists (family identity anchor, bootstrapped at install) | DFE can resolve family identity | Degrade — derive family from the `{family}-ws/` folder + installed `.kiro/{family}/` |
| PC-6 | Territory writable | DFE can create/update files under `{family}-ws/data/` | Distribution works | Permission/path issue — DFE cannot publish |

### Phase 2: Discovery Scan (Does DFE See the Sources?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| DS-1 | SOURCE_MAPs parseable | At least one package `SOURCE_MAP.md` has a valid source declaration + extraction table | Gather plan can build | SOURCE_MAP exists but is empty/malformed |
| DS-2 | Schemas valid | At least one `{pkg}-data.schema.json` is valid JSON Schema | Validation can run | Schema present but invalid JSON |
| DS-3 | Sources resolvable (real data) | At least one declared source path resolves to a real file with non-placeholder content | DFE has real data to gather | Only templates/placeholders — no real project data |
| DS-4 | Demands scannable | `{family}-ws/data/demands/` is readable (0+ demand files) | Shape plan can build | demands/ unreadable |
| DS-5 | Projects discoverable | `{family}-ws/projects/PROJECTS.md` (or `projects/`) present | DFE knows the project set | No project registry (single/idle workspace) |

### Phase 3: Operational Readiness (Can DFE Actually Run?)

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| OR-1 | At least one package has run | A marker (e.g. `pilc-state.md`) exists with a real, non-placeholder `projectId`/state | There is something to gather | Nothing has run — data surface would be all null |
| OR-2 | REGISTRY.json writable | DFE can create/update the registry | Consumer discovery works | Write/path issue |
| OR-3 | dfe-state.md writable | DFE can persist its discovery + demand cache | Discover-once works | Cannot persist state (re-discovers every pass) |
| OR-4 | No conflicting master DFE | In multi-family, this DFE isn't dormant under a master (unless expected) | This DFE is authoritative here | Dormant — a master DFE owns this family's data |
| OR-5 | history/ writable | DFE can write timestamped snapshots | History/audit works | Cannot snapshot (degraded — no history) |

### Phase 4: End-to-End Proof (Can DFE Complete One Cycle?)

This phase only runs if Phase 3 passes with at least one runnable package (OR-1).

| # | Check | What It Validates | PASS | FAIL |
|---|-------|-------------------|------|------|
| E2E-1 | Gather one package | Read one package's declared sources → extract fields per its SOURCE_MAP (in memory) | Gather logic works live | Extraction fails or sources unreadable |
| E2E-2 | Validate against schema | The gathered `{pkg}-data` validates against its schema | Validation works | Data does not conform |
| E2E-3 | Distribute (non-destructive) | Write/refresh the `{pkg}-data.json` + re-derive `REGISTRY.json` + update `dfe-state.md` | Distribution + registry work | Write/registry update failed |
| E2E-4 | Shape one demand | Produce one `{consumer-output}.json` from per-package data (or **SKIP** if no demands) | Layer-2 shaping works | Shaping failed |

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║  DHC__ Data-Fabric Health Check Report               ║
╠══════════════════════════════════════════════════════╣

  Workspace:     {path}
  Family:        {family}
  Date:          {ISO date}
  DFE Version:   {from core-engine.md}

  ┌─────────────────────────────────────────────────┐
  │  VERDICT: {HEALTHY / DEGRADED / NOT READY / IDLE} │
  └─────────────────────────────────────────────────┘

  Phase 1 — Preconditions:       {N}/6 pass
  Phase 2 — Discovery:           {N}/5 pass
  Phase 3 — Operational:         {N}/5 pass
  Phase 4 — End-to-End Proof:    {N}/4 pass (or SKIPPED)

  Summary:
  • {One-line plain English diagnosis}
  • {What works}
  • {What doesn't}
  • {Recommended action — usually a DAT__ command}

╚══════════════════════════════════════════════════════╝
```

---

## Verdict Logic

| Condition | Verdict |
|-----------|---------|
| Phase 1 all PASS + Phase 2 all PASS + Phase 3 ≥3 PASS + Phase 4 ≥3 PASS | **HEALTHY** — DFE is fully operational; run `DAT__ all` |
| Phase 1 all PASS + Phase 2 ≥3 PASS + Phase 3 ≥1 PASS | **DEGRADED** — DFE can run but has limitations |
| Phase 1 PC-1 FAIL or PC-3 FAIL | **NOT READY** — DFE cannot operate (not installed, or no territory) |
| Phase 2 DS-3 FAIL (only placeholders, no real sources) | **IDLE** — DFE is installed correctly but no package has produced real data yet |

---

## Detailed Findings Format

```
✅ PC-3: Territory exists
  Location: pdlc-ws/data/  (REGISTRY.json, dfe-state.md, demands/, history/ present)

❌ DS-3: Sources resolvable — FAILED
  Scanned: pilc SOURCE_MAP → projects/PRJ-{ABBREV}-{slug}/pip/pilc-state.md
  Result: Path contains placeholders; no real project folder exists.
  Meaning: No package has produced real data — DFE would write all-null files.
  Action: Run AI-PILC (or any lifecycle package) to create a real project first.

⚠️ OR-5: history/ writable — WARNING
  Result: {family}-ws/data/history/ is missing.
  Meaning: DFE can distribute but cannot snapshot history.
  Action: Run `DHC__ fix` to create it, or `DAT__ all` (DFE creates it on first write).
```

---

## Artifacts Produced

After running, `DHC__` produces a single report file in DFE's own territory:

```
{family}-ws/data/
└── health-check/
    └── DHC-{YYYY-MM-DD}.md       (the full report)
```

If `DHC__ fix` was invoked and fixes were applied:
```
{family}-ws/data/
└── health-check/
    ├── DHC-{YYYY-MM-DD}.md        (report)
    └── DHC-{YYYY-MM-DD}-fixes.md  (what was fixed)
```

> Writing into `{family}-ws/data/` is consistent with DFE being the sole writer of its territory. The health-check report is the only thing `DHC__` writes (read-only everywhere else, except `fix` mode).

---

## Relationship to DFA__

| Aspect | DHC__ (Health Check) | DFA__ (Integrity Agent) |
|--------|----------------------|-------------------------|
| **When** | Before/during setup — "can DFE work?" | After a `DAT__` pass — "is the data surface correct?" |
| **Assumes** | Nothing — tests from zero | DFE has already produced a data surface |
| **Validates** | Preconditions + discovery + first-cycle proof | Ongoing surface integrity (18 checks / 5 categories) |
| **Produces** | Readiness verdict + diagnosis | Integrity report + drift findings |
| **Destructive?** | Never (read-only, except `fix` mode) | Never (read-only) |

---

## Installation

1. Copy `data-fabric-health-check.md` to destination workspace `.kiro/agents/` (or equivalent for your IDE)
2. Add shortcut `DHC__` to workspace rules (see `shortcut-rules-block.md`):

```markdown
**`DHC__` shortcut triggers Data-Fabric Health Check.** When the user types `DHC__` (uppercase, with double underscore) anywhere in a prompt, immediately execute the Data-Fabric Health Check protocol defined in this agent. Scan the workspace for AI-DFE prerequisites, attempt discovery, validate operational readiness, optionally prove one gather→shape→distribute cycle, and produce a verdict report. No further clarification needed.
```

3. Invoke with `DHC__` in any prompt

---

## Evidence Collection

When you run `DHC__` in a workspace, the report (`DHC-{date}.md`) IS the evidence. It documents exactly what worked and what failed. Store it alongside your project's test artifacts or governance records for traceability.

---

*Part of AI-DFE v1.0.0 | AG-ID: DFE-AG-02*

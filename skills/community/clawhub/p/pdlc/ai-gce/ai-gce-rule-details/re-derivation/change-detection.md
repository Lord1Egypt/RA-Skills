<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Change Detection — Re-Derivation Logic

## Purpose

Defines HOW AI-GCE detects which steering files changed and maps those changes to affected rules and hooks. This is the entry point for Mode 2 (Re-Derivation).

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in change propagation: one steering file change can cascade to multiple rules, hooks, and supporting artifacts
- Use the most reliable detection method available: AI-DWG signal > user specification > timestamp fallback
- Map impact precisely: every changed steering file has a known set of affected artifacts (use the mapping table)
- Consider special cases: tech-stack changes affect ALL hooks (pattern update), new conditional files trigger generation
- Always present impact analysis to user before executing — re-derivation is a controlled change, not an automatic reaction

### Anti-Patterns for This Activity
- Do NOT re-derive ALL rules when only one steering file changed (selective, not full regeneration)
- Do NOT skip the impact report — users must understand what will change before it changes
- Do NOT treat a framework switch (NestJS → Django) as a simple re-derivation — recommend Mode 1 full regeneration

### Quality Check
A good output from this activity sounds like:
- "Change detected: api-standards.md modified (timestamp newer than lastAudit). Impact: re-derive api-first-compliance.md + update api-contract-check.json patterns. 2 artifacts affected, 0 new, 0 removed."
- "Special case: tech-stack.md changed from NestJS to Django. This is a framework switch — recommending Mode 1 full regeneration instead of selective Mode 2."

---

## Detection Methods (Ordered by Preference)

### Method 0: Manifest Baseline-Version Change (Primary, Manifest-Driven)

The most reliable trigger: compare `manifest.baselineVersion` against the version GCE last derived against (persisted in `.compliance-state.json`).

```
Read .governance/workspace-manifest.yaml → baselineVersion (e.g., v4)
Read .compliance-state.json → lastDerivedBaselineVersion (e.g., v3)

IF manifest.baselineVersion > lastDerivedBaselineVersion:
  → DWG re-baselined since last derivation. Re-derive.
  → Read the baseline disposition ledger (files.baselineManifest) to see WHAT changed
    (which governed elements were added/modified/retired → which rules/ files changed)
  → Selective re-derivation on the affected rules only
  → Update lastDerivedBaselineVersion = manifest.baselineVersion
```

A version bump is the authoritative signal that the governed surface changed. The ledger tells GCE precisely which elements moved, so re-derivation stays selective (not full).

### Method 1: AI-DWG Downstream Signal (Best)

AI-DWG sends a structured signal after reconciliation:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   To: AI-GCE
   Event: steering-files-updated
   Workspace root: {path}
   Affected files: [list of changed rules/ files]
   Action required: Re-derive compliance for changed files
```

When this signal is available: use the `Affected files` list directly. No scanning needed.

### Method 2: User Specifies Changed Files

User says: "Re-derive compliance — I updated api-standards.md and testing-strategy.md"

Use the files the user names. No scanning needed.

### Method 3: Timestamp Comparison (Fallback)

If no signal and user doesn't specify:
1. Read `.compliance-state.json` → `lastAudit` timestamp
2. Scan `rules/*.md` for files modified AFTER that timestamp
3. Also scan: `TEAM_AGREEMENTS.md`, `CODEOWNERS`, `DEFINITION_OF_DONE.md`
4. Present findings to user for confirmation before proceeding

---

## Impact Mapping: Changed File → Affected Artifacts

### Full Mapping Table

| Steering File Changed | Affected Rule Files | Affected Hooks | Rationale |
|----------------------|--------------------:|----------------|-----------|
| `workspace-rules.md` | architecture-compliance.md | post-task-governance.json | Golden rules changed |
| `architecture-principles.md` | architecture-compliance.md | post-task-governance.json | Principles changed |
| `tech-stack.md` | naming-conventions.md, devops-deployment.md | naming-check.json, coverage-check.json, ALL hooks (pattern update) | Technology drives all file patterns |
| `coding-standards.md` | (rules embedded in other categories) | post-task-governance.json | Code quality standards |
| `api-standards.md` | api-first-compliance.md | api-contract-check.json | API conventions changed |
| `api-versioning.md` | api-versioning-compliance.md | (pre-pr-checklist.json) | Version rules changed |
| `security-rules.md` | security-compliance.md | security-gate-check.json | Security model changed |
| `module-structure.md` | module-boundaries.md, team-topology.md | module-boundary-check.json, domain-layer-purity.json | Module layout changed |
| `database-rules.md` | data-governance.md | migration-safety.json | Schema rules changed |
| `naming-conventions.md` | naming-conventions.md | naming-check.json | Naming patterns changed |
| `error-handling.md` | error-handling-compliance.md | post-task-governance.json | Error patterns changed |
| `observability-logging.md` | logging-compliance.md | (post-task-governance.json) | Logging rules changed |
| `observability-sensitive.md` | sensitive-data-protection.md | sensitive-data-check.json | PII categories changed |
| `domain-context.md` | domain-context-enforcement.md | domain-layer-purity.json | Domain language changed |
| `role-isolation.md` | role-isolation.md, team-topology.md | segregation-check.json | Role rules changed |
| `session-governance.md` | session-governance.md | session-discipline.json | Session methodology changed |
| `project-governance.md` | phase-gates.md, sprint-governance.md | post-task-governance.json, change-readiness-gate.json | Phase/sprint rules changed |
| `git-workflow.md` | devops-deployment.md, pr-governance.md | pre-pr-checklist.json, migration-safety.json | DevOps rules changed |
| `testing-strategy.md` | cicd-gates.md | coverage-check.json | Coverage thresholds changed |
| `scope-and-risks.md` | (audit agent context) | periodic-audit.json (scope boundary) | Scope boundaries changed |
| `multi-tenancy.md` (NEW) | tenant-isolation.md (NEW) | tenant-isolation-check.json (NEW) | New conditional activated |
| `multi-tenancy.md` (REMOVED) | tenant-isolation.md (REMOVE) | tenant-isolation-check.json (REMOVE) | Conditional deactivated |
| `brownfield-patterns.md` (NEW) | → Triggers Mode 3 | — | Switch to brownfield adoption flow |
| `TEAM_AGREEMENTS.md` | pr-governance.md, role-isolation.md | pre-pr-checklist.json, segregation-check.json | Team process changed |
| `CODEOWNERS` | role-isolation.md, team-topology.md | module-boundary-check.json | Ownership changed |
| `DEFINITION_OF_DONE.md` | phase-gates.md | post-task-governance.json | Completion criteria changed |

---

## Special Case: `tech-stack.md` Changed

When technology changes, ALL hooks need pattern updates because file globs are tech-derived:

```
tech-stack.md changed (e.g., NestJS → Django)
  → RE-DERIVE all hook file patterns (not just naming-check)
  → RE-VALIDATE all existing patterns against new filesystem expectations
  → FLAG: if technology changed fundamentally, recommend Mode 1 full regeneration instead
```

**Threshold:** If tech-stack.md change is a FRAMEWORK switch (not just a version bump), warn user that full regeneration is recommended.

---

## Special Case: New Conditional File Appears

When a conditional steering file is CREATED (didn't exist before):

```
NEW: multi-tenancy.md created
  → GENERATE new rule file: .governance/rules/tenant-isolation.md
  → GENERATE new hook: .governance/hooks/tenant-isolation-check.json
  → UPDATE: knowledge-map.md (new entries)
  → UPDATE: COMPLIANCE_README.md (new rule category section)
  → UPDATE: ENFORCEMENT-GUIDE.md (new hook listed)
  → UPDATE: .compliance-state.json (applicable rules count increases)
```

---

## Special Case: Conditional File Removed

When a conditional steering file is DELETED:

```
REMOVED: multi-tenancy.md deleted
  → REMOVE: .governance/rules/tenant-isolation.md
  → REMOVE: .governance/hooks/tenant-isolation-check.json
  → UPDATE: knowledge-map.md (remove entries)
  → UPDATE: COMPLIANCE_README.md (remove section)
  → UPDATE: ENFORCEMENT-GUIDE.md (remove hook listing)
  → UPDATE: .compliance-state.json (applicable rules count decreases)
  → LOG: REDERIVATION event noting removal
```

---

## Output: Change Impact Report

Before re-generating, present the impact analysis to the user:

```
🔄 RE-DERIVATION IMPACT ANALYSIS

Changed steering files detected: {n}
  • {file 1} (modified {date})
  • {file 2} (modified {date})

Impact:
┌─────────────────────────────────┬────────────────────────────────────────┐
│ Affected Artifact               │ Action Required                        │
├─────────────────────────────────┼────────────────────────────────────────┤
│ .governance/rules/{file}        │ Re-derive rules from updated steering  │
│ .governance/hooks/{file}              │ Update file patterns / rule references │
│ NEW: {file}                     │ Generate (new conditional activated)   │
│ REMOVE: {file}                  │ Delete (conditional deactivated)       │
└─────────────────────────────────┴────────────────────────────────────────┘

Proceed with re-derivation? (Affected artifacts will be regenerated;
manual customizations marked <!-- custom --> will be preserved.)
```

<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Downstream Signaling — Triggering AI-GCE Re-Derivation

## Purpose

Defines how AI-DWG notifies AI-GCE (the downstream package) that steering files have been generated or updated, requiring the compliance engine to derive or re-derive its enforcement rules.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about signaling as a pipeline trigger — the workspace generation is not "done" until downstream knows what changed
- Be specific about what changed — AI-GCE can perform selective re-derivation if the signal identifies exact files and change types
- Design for decoupled execution — packages are independent; the signal is informational, never blocking
- Map steering file categories to hook types — know which AI-GCE enforcement mechanisms are affected by which steering changes
- Signal after EVERY generation or reconciliation that modifies steering — no silent updates that leave enforcement stale

### Anti-Patterns for This Activity
- Do NOT auto-invoke AI-GCE — packages are independent; the user orchestrates when downstream runs
- Do NOT signal for non-steering changes — folder structure, docker-compose, and operational docs don't affect AI-GCE hook derivation
- Do NOT send signals when nothing actually changed (e.g., provenance date-only updates with no content change)

### Quality Check
A good output from this activity sounds like:
- "Signal: `steering-files-updated`. Modified: api-standards.md (API-RATE-02 threshold changed), security-rules.md (new AUTH rule added). Action: AI-GCE selective re-derivation for rate-limiting and auth hooks."
- "Signal: `workspace-generated`. 19 ALWAYS files + 3 CONDITIONAL files generated. Action: AI-GCE full derivation required — read all steering files, derive all hooks."

---

## When to Signal

| Event | Signal Required | Signal Type |
|-------|:--------------:|-------------|
| Mode 1: Full Generation complete | ✅ | `workspace-generated` — full derivation needed |
| Mode 2: Reconciliation applied (any changes) | ✅ | `steering-files-updated` — selective re-derivation |
| Mode 2: Reconciliation proposed but user skipped | ❌ | No signal — nothing changed |
| Provenance-only update (date change, no content change) | ❌ | No signal — no enforcement impact |

---

## Signal Format

### After Full Generation (Mode 1)

```
⚡ DOWNSTREAM SIGNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From:       AI-DWG
To:         AI-GCE
Event:      workspace-generated
Timestamp:  {ISO-8601}
Workspace:  {absolute path to workspace root}

Steering files generated ({n} total):
  ALWAYS:
    • workspace-rules.md
    • architecture-principles.md
    • tech-stack.md
    • coding-standards.md
    • project-governance.md
    • scope-and-risks.md
    • session-governance.md
    • role-isolation.md
    • domain-context.md
    • api-standards.md
    • security-rules.md
    • module-structure.md
    • testing-strategy.md
    • database-rules.md
    • naming-conventions.md
    • git-workflow.md
    • error-handling.md
    • observability-logging.md
    • observability-sensitive.md

  CONDITIONAL (generated):
    • {file}: triggered by {reason}
    • ...

  CONDITIONAL (skipped):
    • {file}: skipped because {reason}
    • ...

Operational documents: {n}
Config files: {n}

Action required:
  AI-GCE should perform FULL DERIVATION:
  • Read ALL steering files + operational docs
  • Derive compliance rules (architecture + governance, tier-tagged)
  • Generate .kiro/hooks/*.json files (debounce-tiered)
  • Generate .governance/ folder (rules, agents, compliance-log)
  • Initialize .compliance-state.json (Tier 1)
  • Generate management_framework/dashboards/compliance-dashboard.md template
  • Configure enforcement layer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### After Delta Reconciliation (Mode 2)

```
⚡ DOWNSTREAM SIGNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From:       AI-DWG
To:         AI-GCE
Event:      steering-files-updated
Timestamp:  {ISO-8601}
Workspace:  {absolute path to workspace root}
Trigger:    {what AP change caused reconciliation}

Files MODIFIED:
  • rules/{file-1} — {brief: what changed}
  • rules/{file-2} — {brief: what changed}

Files ADDED:
  • rules/{new-file} — {reason: trigger now met}

Files REMOVED:
  • rules/{removed-file} — {reason: trigger no longer met}

Files UNCHANGED:
  • (all others)

Action required:
  AI-GCE should perform SELECTIVE RE-DERIVATION:
  • Re-read ONLY modified/added files
  • Re-derive rules affected by changed steering (.governance/rules/)
  • Re-derive hooks affected by changed rules (.kiro/hooks/)
  • Update .compliance-state.json with re-derivation timestamp
  • Log REDERIVATION event to compliance log
  • Leave hooks/rules for unchanged files untouched

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Signal Delivery

### How the Signal is Communicated

AI-DWG does NOT directly invoke AI-GCE (packages are independent). The signal is:

1. **Displayed to the user** as part of the generation/reconciliation summary
2. **Logged in the reconciliation log** (`.kiro/reconciliation-log.md`)
3. **User decides when to invoke AI-GCE** — the signal tells them it's needed

**The user's next action:**
```
"Using AI-GCE, derive compliance hooks from the workspace steering files"
OR
"Using AI-GCE, re-derive hooks — steering files were updated"
```

### Why Not Auto-Invoke?

- Packages are independent — no runtime coupling
- User may want to review workspace before enabling enforcement
- AI-GCE may not be installed yet (user may add it later)
- User may want to batch multiple reconciliations before re-deriving

---

## What AI-GCE Needs to Know

When AI-GCE receives the signal (via user invocation), it needs:

| Information | Where to Find |
|-------------|---------------|
| Which steering files exist | Scan `rules/` directory |
| Which files changed (for selective) | Signal message lists them; OR compare hook derivation timestamps |
| Rule categories per file | AI-GCE's own reading guide defines this |
| Rule IDs (for hook mapping) | Read steering files — rules are numbered (AUTH-01, DB-QUERY-03, etc.) |
| Operational docs | DEFINITION_OF_DONE.md, TEAM_AGREEMENTS.md, CODEOWNERS, PROJECT_INSTRUCTIONS.md |

---

## AI-GCE Output Locations (What It Produces)

When AI-GCE processes the signal and derives/re-derives, it writes to:

| Output | Location | Purpose |
|--------|----------|---------|
| Compliance hooks | `.kiro/hooks/*.json` | Real-time enforcement via IDE events |
| Hook enforcement guide | `.kiro/hooks/ENFORCEMENT-GUIDE.md` | Tier-based enforcement roadmap |
| Compliance state | `.compliance-state.json` | Tier tracking, readiness criteria, score history |
| Governance rules | `.governance/rules/*.md` | Detailed compliance rules (tiered + conditional) |
| Audit agent | `.governance/agents/compliance-audit-agent.md` | 9-step audit with scoring |
| Init agent | `.governance/agents/project-init-agent.md` | 5-question scaffolding |
| Compliance log | `.governance/compliance-log/` | JSONL schema, exception/remediation workflows |
| Dashboard | `management_framework/dashboards/compliance-dashboard.md` | Visual compliance status |
| Package Territory Registry | `.governance/PACKAGE_TERRITORIES.md` | Excluded-zone declarations for hook segregation |
| Brownfield artifacts | `.governance/brownfield-baseline.md` + `incremental-adoption-plan.md` | IF brownfield |
| Phase/role steering | `rules/compliance-*.md` | Optional fileMatch enrichment (Step 4b) |

---

## Signal Categories (What Kind of Rules Changed)

AI-GCE derives different hook TYPES from different steering files. The signal helps it know which hook types to re-derive:

| Steering File Category | AI-GCE Hook Type |
|-----------------------|------------------|
| `security-rules.md` | Pre-commit security checks, auth validation hooks |
| `module-structure.md` | Module boundary enforcement hooks |
| `naming-conventions.md` | Naming validation hooks |
| `api-standards.md` | API convention check hooks |
| `database-rules.md` | Schema/query validation hooks |
| `coding-standards.md` | Code pattern enforcement hooks |
| `multi-tenancy.md` | Tenant isolation verification hooks |
| `observability-sensitive.md` | Sensitive data detection hooks |
| `testing-strategy.md` | Test coverage gate hooks |

---

## Edge Cases

| Situation | Signal Behavior |
|-----------|----------------|
| AI-GCE not installed/configured | Signal is still displayed — user knows they'll need it eventually |
| Only operational docs changed (not steering) | Signal needed IF docs AI-GCE reads changed (DEFINITION_OF_DONE, TEAM_AGREEMENTS, CODEOWNERS) |
| Multiple reconciliations before AI-GCE runs | AI-GCE performs full derivation on current state — doesn't need change history |
| Steering file renamed | Signal as REMOVED (old name) + ADDED (new name) |
| All changes were in team sections | No signal — AP-sourced content unchanged → hooks unchanged |
| .governance/ already exists | AI-GCE re-derives (updates existing rules, doesn't clobber manual additions) |
| .compliance-state.json exists | AI-GCE updates tier tracking and records re-derivation event |

---

## Key Rules

1. **Signal after EVERY generation or reconciliation that changes steering files** — no silent updates
2. **Be specific about what changed** — AI-GCE can re-derive selectively if it knows which files changed
3. **Don't auto-invoke AI-GCE** — packages are independent; user orchestrates
4. **Include enough context for selective re-derivation** — file names + change type
5. **No signal for non-steering changes** — operational docs, configs, and folder structure don't affect AI-GCE
6. **Signal is informational, not blocking** — generation/reconciliation completes regardless of whether AI-GCE acts

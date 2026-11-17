<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: ai-dwg-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-DWG AGENT GUIDE SECTION -->

## AI-DWG — Workspace Integrity Agent (`WIA__`)

### What It Does

Validates that your generated development workspace is structurally complete, internally consistent, and ready for AI-GCE governance derivation and team development. Think of it as a structural inspection — the DevOps equivalent of verifying the construction site matches the blueprint before work begins.

### When to Call

| Trigger | Process Milestone | Why Now |
|---------|-------------------|---------|
| `WIA__` | After full generation (Mode 1) | Validates complete workspace against the AP |
| `WIA__` | After reconciliation (Mode 2) | Confirms delta was applied correctly |
| `WIA__` | After brownfield overlay (Mode 3) | Verifies steering merged without conflicts |
| `WIA__` | Before AI-GCE hook derivation | Ensures governance is derived from complete steering |
| `WIA__` | Before development kickoff | Confirms day-1 readiness for the team |

**How to call:** Type `WIA__` anywhere in your chat prompt. The agent activates immediately.

### What It Checks

| Category | Checks | What "Pass" Means |
|----------|--------|-------------------|
| **Steering Completeness** | All 14 mandatory files present; conditional files justified by AP; no unjustified conditionals; operational docs exist; planning templates present | Every expected steering file exists and only justified ones are included |
| **Structure Alignment** | Modules map to C4 L3 components; no orphan directories; depth level consistent; extension structures present | The workspace folders mirror the architecture |
| **Config Consistency** | Tech labels match configs; git workflow reflected in CI/CD; test strategy reflected in structure; security constraints in configs | All generated configurations agree with each other |
| **Provenance Integrity** | Front-matter present on all files; source fields resolve to real AP artifacts; ownership values correct | Every rule traces back to an architecture decision |
| **Downstream Readiness** | AI-GCE signal requirements met; state file consistent; marker file intact | AI-GCE can safely derive governance from this workspace |

### What Breaks If You Skip

| Impact | Description | Detection |
|--------|-------------|-----------|
| 🟠 Incomplete governance | AI-GCE derives hooks from missing steering → gaps in compliance | When compliance audit finds uncovered areas |
| 🟠 Structure drift | Developers create modules in non-architectural locations → design erodes | When code review reveals structural violations |
| 🟡 Config mismatch | Tooling doesn't match architecture decisions → builds break or lint false-positives | When CI/CD pipeline fails unexpectedly |
| 🟡 Lost traceability | Rules without provenance → "why does this rule exist?" has no answer | When team wants to challenge or update a rule |
| 🟢 Signal gap | AI-GCE receives partial state → incomplete derivation | When GCE reports missing rule sources |

### Recovery

**If you forgot to call `WIA__` and the workspace is already in use:**

1. Run `WIA__` now — it checks the current workspace state against the AP
2. For missing steering files: determine if AP justifies them; regenerate specific files using the relevant mapping rule
3. For structure gaps: compare C4 L3 against actual folders; add missing modules
4. For config mismatches: cross-reference `tech-stack.md` against generated configs; fix inconsistencies
5. For provenance issues: add/fix front-matter blocks; ensure `source:` resolves correctly
6. If AI-GCE already derived hooks: flag corrected steering files; request re-derivation for affected rules

**Self-healing?** ⚠️ Partial — the agent detects current state issues, but it cannot retroactively fix governance hooks that AI-GCE already derived from incomplete steering. Those require explicit re-derivation.

### Relationship to Other Agents

| Agent | Relationship |
|-------|-------------|
| `compliance-audit-agent` (AI-GCE) | CAA checks **code** compliance against steering; WIA checks that the **steering itself** is complete and correct — upstream validation |
| `architecture-decision-agent` (AI-ADLC) | ADA validates the AP; WIA validates the **workspace derived from** that AP — sequential quality chain |
| `initiation-quality-agent` (AI-PILC) | IQA validates PIP → ADA validates AP → WIA validates workspace — progressive quality gates through the chain |
| `session-discipline-agent` (AI-GCE) | SDC checks runtime process discipline; WIA checks infrastructure-level structural integrity — different layers |

### Output

- **Pass:** One-line summary confirming workspace integrity + check counts
- **Violations:** Per-check report with ID, status, finding, and remediation suggestion
- **Log:** Entry in `.governance/compliance-log/events/` (if governance infra exists)

<!-- END AI-DWG AGENT GUIDE SECTION -->

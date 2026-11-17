# Why Change Management Matters

**Purpose:** Explains why tracking, evaluating, and governing changes (to requirements, architecture, scope, and team agreements) prevents the silent accumulation of uncontrolled modifications that transform planned projects into unrecognizable ones.

---

## The Practice

Change management means that modifications to established baselines (approved requirements, locked architecture decisions, agreed scope, governance rules) go through a defined process: capture the change request, assess impact, get approval, implement, verify. No change bypasses evaluation — especially the "small" ones.

---

## What Happens When You Skip It

1. **The scope that grew 300%.** The original charter said "customer portal with 5 features." After 6 months, it's 17 features. No single change was large — each was "just one more thing." No one tracked the cumulative impact. Budget exhausted at 60% of (revised) scope because no change impact was assessed.

2. **The architecture that drifted.** ADR-003 says "monolithic deployment." Three months later, two teams have independently created separate services. No ADR revision, no impact assessment, no downstream notification. AI-DWG's steering files describe a monolith; the code is distributed. Governance enforces patterns that don't match reality.

3. **The "agreed" agreement that nobody agreed to.** Team agreements say "PR reviews within 4 hours." Someone changed it to "24 hours" in a quiet commit. Half the team follows the old rule, half follows the new. Friction, missed SLAs, blame.

4. **The invisible constraint change.** A budget reduction happens. The PM adjusts the plan internally. The architecture team designs for the original budget — recommending infrastructure the project can no longer afford. Discovered at procurement time. Redesign required.

5. **The retroactive requirement.** Stakeholder adds a requirement in month 4 that contradicts a design decision made in month 1. Without change tracking, no one realizes the contradiction until testing reveals the new requirement breaks existing functionality.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | Unmanaged changes are the #1 cause of budget overrun. Each unassessed change carries hidden costs (testing, integration, documentation, training) that accumulate invisibly. |
| Timeline | Scope changes without impact assessment average 2x actual effort vs. estimate because the cascading effects (on other features, on architecture, on testing) aren't scoped. |
| Quality | Changes implemented without architectural review create technical debt. Each ungoverned change degrades the codebase slightly — compounding over dozens of changes. |
| Team | Unclear change authority creates conflict: "Who decided this changed?" "Was this approved?" Without process, changes feel arbitrary and trust erodes. |
| Risk | Untracked changes make risk registers stale. A new dependency introduced without evaluation carries unknown risk. The project's risk profile is worse than it knows. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **AI-PILC** | Change Register (management framework) | Every change to requirements, scope, or project parameters is logged with impact assessment and approval status. Initialized at project start. |
| **AI-ADLC** | ADR revision process | Architecture changes require a new ADR (or ADR revision) with: what changed, why, impact on downstream, migration path. No silent architecture drift. |
| **AI-ADLC** | Architecture workbook | Open questions and assumption changes tracked in a living document. Changes to assumptions trigger re-evaluation of dependent decisions. |
| **AI-DWG** | Mode 2: Delta Reconciliation | When architecture changes, reconciliation is explicit — AI-DWG shows exactly what workspace files are affected and proposes specific updates. |
| **AI-GCE** | Re-derivation on change | Steering file changes trigger re-derivation. Governance always matches current decisions, not stale ones. Change propagation is automated. |
| **AI-GCE** | Change governance hooks | PR hooks enforce: linked change request for scope changes, ADR reference for architecture changes, approval evidence for baseline modifications. |

---

## The Change Cascade

Every change ripples. Change management traces the ripple:

```
REQUIREMENT CHANGES
    ↓ impacts
ARCHITECTURE (may need ADR revision)
    ↓ impacts
WORKSPACE (steering files may need updating)
    ↓ impacts
GOVERNANCE (rules may need re-derivation)
    ↓ impacts
IN-PROGRESS CODE (may need refactoring)

Without tracking: each layer discovers the impact independently, late.
With tracking: impact is assessed upfront, cascade is planned.
```

---

## Severity: High

Change management isn't bureaucracy — it's the mechanism that keeps a project's actual state aligned with its documented state. Without it, plans become fiction, budgets become guesses, and architecture becomes whatever happened to get built. The discipline of "evaluate before implementing" applies to changes just as much as to original requirements.

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |
| Why Project Initiation Matters | `knowledge_docs/WHY_PROJECT_INITIATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

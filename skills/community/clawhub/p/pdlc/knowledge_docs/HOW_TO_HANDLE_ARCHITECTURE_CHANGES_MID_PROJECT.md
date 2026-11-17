# How to Handle Architecture Changes Mid-Project

**Purpose:** Practical guide for managing architecture changes AFTER the initial design is complete and development is underway — how the AI-* Family's reconciliation pipeline propagates changes through AI-ADLC → AI-DWG → AI-GCE without disrupting active delivery.

---

## Who This Is For

Architects, tech leads, or senior developers who need to change a decision made during AI-ADLC (new container, revised API contract, changed technology, added extension) and need those changes to flow through the workspace and governance layer cleanly.

---

## Why Architecture Changes Are Different

Architecture changes aren't code changes. They ripple:

```
ARCHITECTURE DECISION CHANGED
    │
    ├── AI-ADLC artifacts need updating (ADRs, diagrams, contracts)
    │       │
    │       ▼
    ├── AI-DWG workspace needs reconciling (steering files, structure)
    │       │
    │       ▼
    └── AI-GCE rules need re-deriving (enforcement matches new architecture)
            │
            ▼
        AI-DLC v1 development continues (with updated governance)
```

A code change affects one file. An architecture change affects the entire enforcement chain. The AI-* Family handles this through coordinated reconciliation — not manual file-by-file updates.

---

## Types of Architecture Changes

| Change Type | Example | Impact Scope |
|-------------|---------|:------------:|
| **ADR revision** | Switch from PostgreSQL to MongoDB | Tech stack steering + data rules + test strategy |
| **New container** | Add a notification microservice | Module structure + API contracts + container steering |
| **Removed container** | Merge two services into one | Module structure + integration steering + hooks |
| **Extension activation** | Add DDD Tactical mid-project | Domain steering + naming rules + boundary enforcement |
| **Security model change** | Switch from session to JWT | Security steering + auth hooks + API standards |
| **API contract change** | New versioning strategy | API steering + contract hooks + integration rules |
| **Integration change** | New third-party dependency | Integration steering + resilience rules |

---

## The Reconciliation Pipeline

### Step 1: Update AI-ADLC (Revise the Architecture)

1. Resume your AI-ADLC workflow (load `adlc-state.md`)
2. Navigate to the relevant stage
3. Make the architecture change:
   - Revise the affected artifact (container design, API architecture, etc.)
   - Create a new ADR documenting the change with rationale
   - Update `adlc-state.md` to reflect the revision
4. Gate: approve the change

**ADR for the change should include:**
- What changed and why
- What was the previous decision (superseded ADR reference)
- Impact analysis: which downstream artifacts are affected
- Migration path (if code already exists against the old architecture)

### Step 2: Reconcile AI-DWG Workspace (Delta Mode)

1. Run AI-DWG in **Mode 2: Delta Reconciliation**
2. Point it at the updated AP
3. AI-DWG:
   - Compares new AP against existing workspace
   - Identifies which steering files need updating
   - Proposes changes (shows diff, not just overwrites)
   - Preserves `<!-- custom -->` blocks in existing steering files
4. Review and approve workspace changes

**What Mode 2 does:**
- Updates affected steering files (e.g., `tech-stack.md` if DB changed)
- Adds new steering files if needed (e.g., new container → new module rules)
- Removes obsolete steering files (e.g., container removed → its rules are gone)
- PRESERVES team customizations in hybrid files

**What Mode 2 does NOT do:**
- Touch source code (that's the team's job)
- Delete team-owned files
- Modify non-steering workspace files without explicit approval

### Step 3: Re-Derive AI-GCE Governance

After AI-DWG reconciles, it sends a downstream signal to AI-GCE:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   Event: steering-files-updated
   Affected files: [tech-stack.md, data-standards.md, module-structure.md]
   Action required: Re-derive compliance for changed files
```

AI-GCE then:
1. Reads the signal (which files changed)
2. Maps impact (which rules/hooks are affected)
3. Proposes re-derived rules for review
4. Regenerates only the affected artifacts
5. Preserves custom content in hybrid rules

### Step 4: Communicate to the Team

After the pipeline completes:
- Updated steering files are in place (team sees them next session)
- Updated hooks fire automatically (no team action needed)
- New rules appear in `.governance/rules/` (visible in COMPLIANCE_README.md)
- ADR documenting the change is part of the record

---

## Handling Code That Already Exists

When architecture changes AFTER code is written:

| Scenario | Approach |
|----------|----------|
| New container added | New folder/module created, existing code unchanged |
| Container merged | Create migration ADR; old code works until refactored |
| Tech stack changed | Baseline existing code against new rules; enforce on new code |
| API contract changed | Version the API; old endpoints get deprecation timeline |
| Security model changed | Transition period: both old and new auth accepted, with deadline |

**Key principle:** Architecture change ≠ immediate code rewrite. The governance layer updates immediately (new rules apply to new code). Existing code gets a migration plan tracked in the management framework.

---

## The Migration ADR Pattern

For breaking architecture changes, create a Migration ADR:

```markdown
# ADR-{N}: Migration — {Old Decision} → {New Decision}

## Status: Accepted

## Context
{Why the architecture is changing}

## Decision
Migrate from {old} to {new} over {timeline}.

## Migration Strategy
- Phase 1: New code uses {new approach} (immediate)
- Phase 2: Existing {module/service} migrated by {date}
- Phase 3: Old approach removed/deprecated by {date}

## Governance Implications
- Steering file {X} updated to reflect new standard
- Rule {ARCH-NN} now enforces {new pattern} on new code
- Existing violations baselined at Phase 1 start
- Phase 2 deadline tracked in Issue Register

## Consequences
- Temporary dual-pattern codebase during migration
- Governance enforces new pattern on new code immediately
- Old pattern tolerated (baselined) until Phase 3 deadline
```

---

## Timing: When to Reconcile

| Trigger | Action |
|---------|--------|
| ADR approved that changes architectural constraints | Run reconciliation pipeline immediately |
| New extension activated in AI-ADLC | Run AI-DWG Mode 4 + AI-GCE re-derivation |
| Sprint boundary where team can absorb changes | Batch multiple small changes into one reconciliation |
| Security vulnerability requires architecture change | Emergency reconciliation — immediate pipeline run |

**Do NOT:** Accumulate weeks of architecture changes without reconciling. Stale governance (rules that don't match current architecture) is worse than no governance — it creates false confidence.

---

## What Gets Preserved During Reconciliation

| Artifact Type | Preserved? | Mechanism |
|---------------|:----------:|-----------|
| Team edits in `<!-- custom -->` blocks | ✅ | AI-DWG/GCE detect and preserve custom markers |
| Files with `ownership: user` | ✅ | Never touched by reconciliation |
| Files with `ownership: hybrid` | ✅ (custom parts) | Generated parts updated, custom parts preserved |
| Files with `ownership: generated` | ❌ (regenerated) | Fully overwritten with new derivation |
| Compliance log history | ✅ | Append-only, never modified |
| Baseline violation data | ✅ | Extended, never reset |

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Changing architecture without ADR | Every change needs rationale. Future-you needs to know WHY. |
| Running AI-DWG Mode 1 instead of Mode 2 | Mode 1 overwrites everything. Mode 2 reconciles surgically. |
| Skipping AI-GCE re-derivation after workspace change | Governance becomes stale — rules don't match architecture. |
| Expecting immediate code compliance with new architecture | Use the baseline pattern. New rules enforce forward, not backward. |
| Not communicating the change to the team | Updated steering appears silently. Announce architectural changes in standup/channel. |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

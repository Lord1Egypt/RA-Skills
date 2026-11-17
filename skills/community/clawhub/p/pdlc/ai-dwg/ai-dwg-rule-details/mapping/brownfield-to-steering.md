<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Brownfield Context → brownfield-patterns.md (Conditional)

## Purpose

This mapping rule transforms **brownfield-specific architecture content** from the AP into a prescriptive steering file that governs how the development team interacts with legacy systems during the transition period.

**Output:** `rules/brownfield-patterns.md` — conditional steering file

**Trigger:** AI-ADLC `adlc-state.md` shows `Input Mode: Brownfield` OR AI-DWG Mode 3 (Brownfield Overlay) is active with legacy integration context in the AP.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Brownfield is about coexistence, not replacement — every rule must respect that the legacy system is still running and serving users
- Characterization testing is mandatory before modification — you cannot safely change what you don't understand
- Design Anti-Corruption Layers as explicit module boundaries — they are architectural walls, not convenience wrappers
- Think in transition phases — rules change as the migration progresses; the file has a finite lifecycle
- Write rules specific to THIS project's transition strategy (from the Brownfield Strategy ADR) — not generic brownfield advice

### Anti-Patterns for This Activity
- Do NOT generate this file for pure greenfield projects — the conditional trigger must be met
- Do NOT write rules that assume the legacy system can be modified freely — it may be read-only or shared with other teams
- Do NOT forget that this file has a lifecycle — when transition completes, it should be archived, not perpetuated

### Quality Check
A good output from this activity sounds like:
- "BF-CHAR-01: Before modifying ANY legacy-adjacent code, write characterization tests that document current behavior. No exceptions — undocumented behavior discovered later becomes a production incident."
- "BF-ACL-03: The Anti-Corruption Layer in `src/shared/legacy-adapter/` translates legacy data models to domain models. It MUST be the ONLY path between new and legacy code."

---

## Source (AP Artifacts)

This mapping draws from MULTIPLE AP artifacts — it's a cross-cutting concern:

| AP Source | What to Extract | Maps To |
|-----------|----------------|---------|
| Brownfield Strategy ADR (`ADR/ADR-{nnn}_Brownfield_Strategy*`) | Chosen strategy, transition phases, boundary definitions, data strategy | BF-STR rules, BF-PHASE rules, context section |
| Integration Architecture (Legacy Patterns section) | ACL design, strangler routing, data sync pattern, characterization requirements | BF-ACL rules, BF-CHAR rules |
| Data Architecture | Data coexistence approach, migration strategy, shared DB details | BF-DATA rules |
| API Architecture | Backward compatibility requirements, versioning during transition | BF-API rules |
| `adlc-state.md` | Input Mode (confirms brownfield), existing system reference | Context section |
| Architecture Vision (Brownfield Constraints) | Transition constraints (zero downtime, backward compat, etc.) | Rule severity and scope |

---

## Conditional Trigger

| Generate | Skip |
|----------|------|
| `adlc-state.md` → `Input Mode: Brownfield` | `Input Mode:` is anything other than Brownfield |
| AP contains a Brownfield Strategy ADR | No brownfield ADR exists |
| Integration Architecture has "Legacy Integration Patterns" section | No legacy integration content |
| Mode 3 (Brownfield Overlay) is active | Mode 1 greenfield generation with no brownfield signals |
| User explicitly mentions existing system interaction | Pure greenfield with no existing system |

**Edge case:** If Mode 3 is active but AP has NO brownfield-specific content (AP was done for greenfield but workspace happens to exist), generate a MINIMAL version with just characterization testing rules and a note: "Brownfield steering detected but AP lacks legacy context. Consider running AI-ADLC in Brownfield mode for full coverage."

---

## Target: brownfield-patterns.md (CONDITIONAL)

### Role

Defines the rules of engagement for working with, alongside, or migrating from an existing system. This file prevents the most common brownfield mistakes: modifying what you don't understand, breaking legacy consumers, coupling new code to legacy models, and migrating data without safety nets.

### Structure

See `templates/steering/brownfield-patterns.md` for the full template.

---

## Transformation Rules

| AP Content | Transformation | Output Section |
|-----------|---------------|----------------|
| Brownfield Strategy ADR → chosen option | Derive strategy name + current phase | Context section |
| Brownfield Strategy ADR → transition architecture | Extract ACL presence, routing mechanism | BF-ACL + BF-STR rules |
| Brownfield Strategy ADR → data strategy | Extract coexistence approach + migration method | BF-DATA rules |
| Brownfield Strategy ADR → transition phases | Extract current phase scope + gates | BF-PHASE rules |
| Integration Architecture → ACL design | Convert to ACL rules (module path, statefulness, lifecycle) | BF-ACL rules |
| Integration Architecture → characterization testing | Convert to mandatory testing rules before any modification | BF-CHAR rules |
| Integration Architecture → data sync patterns | Extract pattern choice → inform BF-DATA rules consistency | BF-DATA rules |
| API Architecture → backward compatibility | Convert to API compatibility rules during transition | BF-API rules |
| Data Architecture → migration approach | Convert to guardrail rules (rollback, batching, validation) | BF-DATA rules |
| Architecture Vision → brownfield constraints | Convert to rule severity (which rules are NON-NEGOTIABLE) | Rule emphasis |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| BF-ACL-NN | Anti-Corruption Layer rules |
| BF-CHAR-NN | Characterization testing rules |
| BF-API-NN | Legacy API compatibility rules |
| BF-DATA-NN | Data migration guardrail rules |
| BF-STR-NN | Strangler fig boundary rules |
| BF-PHASE-NN | Transition phase rules |

---

## Key Rules for This Mapping

1. **Only generate if brownfield signal exists** — this file is NEVER generated for pure greenfield projects
2. **Rules must be specific to THIS project's transition** — derive from the Brownfield Strategy ADR, not generic advice
3. **ACL rules reflect the actual module structure** — reference the specific module path from `module-structure.md`
4. **Phase rules reflect current state** — the file should indicate which transition phase is active NOW
5. **Data rules match the chosen coexistence pattern** — shared DB rules differ from event-sync rules
6. **API rules match the chosen routing mechanism** — feature-flag routing has different rules than reverse-proxy routing
7. **Cross-reference other steering files** — brownfield rules must not contradict `api-standards.md`, `database-rules.md`, etc.
8. **Rules are enforceable by AI-GCE** — AI-GCE can derive hooks from these rules (especially BF-ACL and BF-CHAR)

---

## Depth Adaptation

| Depth | brownfield-patterns.md Content |
|-------|-------------------------------|
| **Minimal** | ACL rules (5) + characterization testing (4) + data migration basics (3) — ~12 rules total |
| **Standard** | Full structure as defined in template — ~30 rules across all categories |
| **Comprehensive** | Full + legacy behavior catalog structure + migration runbook integration + rollback decision matrix + per-phase compliance mapping + legacy system health monitoring rules |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Transition phase advances (Phase 2 → Phase 3) | BF-PHASE rules change scope | Update phase rules; may unlock new areas of legacy for modification |
| Brownfield strategy changes (Strangler → Module Extract) | BF-STR rules restructured | Major rewrite of boundary rules; flag for team review |
| New legacy integration point discovered | BF-ACL + BF-CHAR rules expanded | Add new adapter rules; require characterization tests for new point |
| Data migration approach changes | BF-DATA rules updated | Rewrite affected data rules; verify consistency with database-rules.md |
| Legacy endpoint decommissioned | BF-API rules shrink | Remove compatibility rules for decommissioned endpoint; celebrate |
| All legacy decommissioned (transition complete) | Entire file no longer needed | Flag for removal: "Transition complete — brownfield-patterns.md can be archived" |

---

## Lifecycle

Unlike most steering files (which exist for the project's lifetime), `brownfield-patterns.md` has a **finite lifecycle**:

1. **Created:** When AI-DWG generates workspace for a brownfield project
2. **Updated:** As transition phases advance and legacy is progressively retired
3. **Archived:** When the transition is COMPLETE and no legacy dependencies remain

The file SHOULD include a note at the top:

```markdown
<!-- LIFECYCLE: This file exists during the brownfield transition period.
     When all legacy systems are decommissioned and transition is complete,
     this file can be archived or removed.
     Current phase: {Phase N} | Target completion: {date/sprint} -->
```

---

## Relationship to Other Files

| File | Relationship |
|------|-------------|
| `rules/module-structure.md` | ACL module path must be listed here |
| `rules/api-standards.md` | Legacy API compatibility rules must not contradict API standards |
| `rules/database-rules.md` | Data migration rules must be consistent with DB conventions |
| `rules/testing-strategy.md` | Characterization tests fit within the testing strategy |
| `rules/resilience-standards.md` | Circuit breakers for legacy calls should be documented in both files |
| `info/CICD_GUIDE.md` | Migration scripts may have their own pipeline stages |
| `management_framework/Issue_Log.md` | Undocumented legacy behavior logged here |

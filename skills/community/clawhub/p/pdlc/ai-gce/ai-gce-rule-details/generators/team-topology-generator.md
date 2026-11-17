<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Team Topology — Derivation Logic

## Purpose

Derives team topology governance rules (GOV-TT-*) from `module-structure.md` and `CODEOWNERS`. Ensures module ownership boundaries, cognitive load limits, and independent deployability are maintained.

---

## MANDATORY: Stage Sub-Role — Change Manager

During THIS activity, ALSO adopt the mindset of a **Change Manager**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in organizational boundaries: team topology rules ensure that module ownership, cognitive load, and deployment independence align with team structure
- Evaluate ownership from CODEOWNERS: one bounded context must have exactly one owning team — shared ownership creates coordination overhead
- Enforce cognitive load limits: no team should own more than 2-3 modules (beyond that, context switching degrades quality)
- Consider backward compatibility obligations: platform/shared-kernel changes affect ALL consuming teams
- Ensure independent deployability: circular dependencies between modules prevent independent team release cadence

### Anti-Patterns for This Activity
- Do NOT generate team topology rules without CODEOWNERS (ownership rules need ownership data)
- Do NOT conflate team topology (GOV-TT-*) with role isolation (GOV-ROLE-*): TT is about TEAM boundaries, ROLE is about INDIVIDUAL duties
- Do NOT create rules that assume specific organizational structures — derive from what CODEOWNERS and module-structure actually state

### Quality Check
A good output from this activity sounds like:
- "GOV-TT-001: Each bounded context owned by exactly one team. Derived from CODEOWNERS: `src/Modules/Finance/** @finance-team`. No shared ownership detected."
- "GOV-TT-005: Cognitive load limit: max 2-3 modules per team. CODEOWNERS shows @platform-team owns 4 module paths → flagging for team lead review."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `module-structure.md` | Module list, module ownership statements, dependency rules |
| `CODEOWNERS` | Module → team mapping (who owns what) |
| `role-isolation.md` | Team size (used for cognitive load rules) |

---

## Generated Rules

| Rule ID | Statement | Derived From |
|---------|-----------|-------------|
| GOV-TT-001 | Each bounded context owned by exactly one team | CODEOWNERS: one team per module path |
| GOV-TT-002 | Cross-context communication via events/APIs only — no direct class references | module-structure.md dependency rules |
| GOV-TT-003 | Platform/shared kernel changes MUST be backward-compatible | module-structure.md shared kernel section |
| GOV-TT-004 | Stream teams can deploy independently (no circular dependencies) | module-structure.md dependency graph |
| GOV-TT-005 | Cognitive load limit: max 2-3 modules per team | CODEOWNERS ownership count per team |
| GOV-TT-006 | API contracts owned by producing team | CODEOWNERS: contracts/ path ownership |
| GOV-TT-007 | Steering file ownership documented and enforced | CODEOWNERS: rules/ entries |

---

## Hook: `module-boundary-check.json`

Same hook as module-boundary-generator — shared enforcement. GOV-TT-002 and MOD-03 are verified together (both check cross-module references).

## Tier: 2 (team topology enforcement needs multiple contributors — Tier 2 readiness criterion)

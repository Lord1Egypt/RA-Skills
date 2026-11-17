<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Module Boundary — Derivation Logic

## Purpose

Derives module boundary rules (MOD-*) from `module-structure.md`. 100% steering-derived — enforces that code respects the stated module decomposition and dependency rules.

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in dependency graphs: module boundaries are about what CAN and CANNOT reference what
- Always cross-reference documentation against the actual filesystem — trust the filesystem over docs
- Consider layer direction enforcement: dependencies flow inward (presentation → application → domain), never outward
- Generate patterns from REAL paths discovered during workspace scan, never from assumptions
- Evaluate shared kernel usage: duplication across modules is a boundary violation

### Anti-Patterns for This Activity
- Do NOT generate module paths without verifying them against the actual folder structure
- Do NOT allow generic glob patterns — every hook must use module-specific, layer-specific paths
- Do NOT ignore case sensitivity in paths (filesystem truth overrides documentation)

### Quality Check
A good output from this activity sounds like:
- "MOD-03: Cross-module communication via events only. Verification: no import from `src/modules/finance/` found in `src/modules/incident/`. Hook pattern uses actual path `src/Modules/*/Application/**/*.ts`."
- "module-structure.md claims 6 modules; filesystem scan shows 5 exist at stated paths. Flagging 'Notifications' module as documented-but-not-yet-created."

---

## Source: `module-structure.md`

| Section to Extract | Generated Rules |
|-------------------|----------------|
| Module list + paths | MOD-01: Each module lives in its stated path only |
| Layer rules (domain/application/infrastructure/presentation) | MOD-02: Layer dependency direction enforced (inward only) |
| Module dependencies table (who may call whom) | MOD-03: Only allowed cross-module references |
| Shared kernel definition | MOD-04: Shared kernel referenced — never duplicated into modules |

## Additional Source: Folder Scan

Cross-reference module-structure.md against actual filesystem. Hook patterns use REAL paths.

## Hook: `module-boundary-check.json`

- **Event:** agentStop (Tier B)
- **Pattern:** All module source files (e.g., `src/modules/**/*.ts`)
- **Checks:** MOD-01/02/03 — no cross-boundary imports, layer direction respected

## Hook: `domain-layer-purity.json`

- **Event:** agentStop (Tier B)
- **Pattern:** Domain layer files (e.g., `src/modules/*/domain/**/*.ts`)
- **Checks:** MOD-02 (no infra deps in domain), DOM-005

## Tier: 1 (basic boundary awareness) / 2 (full enforcement with dependency verification)

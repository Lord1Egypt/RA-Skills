# Consolidation Pattern Diagnosis — May 2026

## Problem identified by user (May 22, 2026)

Forge kept creating standalone skills for content that belonged inside existing parent skills. Six standalone skills were identified and consolidated:

| Standalone (deleted) | Absorbed into | As |
|---|---|---|
| financial-sync | ocas-styx | references/financial-sync.md |
| system-maintenance | ocas-custodian | references/system-maintenance.md |
| ocas-expansion | ocas-weave | already in SKILL.md |
| bower-mempalace-ingest | ocas-bower | already in scripts/ |
| dispatch-status-from-files | ocas-dispatch | references/status_from_files.md |
| weave-db-maintenance | ocas-weave | references/database_maintenance.md |

## Root cause

1. Phase 1 (existence gate) was too weak — did NOT mandate checking whether a parent skill already owns the domain.
2. No parent-search before creation. The default output of forge.build is a new skill package.
3. ## Integrated: wrappers are a band-aid — content bolted on with wrapper headers instead of refactored into parent's proper structure.
4. Rule 7 in authoring_rules.md already said "prefer absorption" but wasn't enforced at build time.

## Fix applied (v2.9.0)

- Phase 1 now includes mandatory parent check
- Added standalone test (own invocation path + cron + journal = standalone justified)
- ## Integrated: wrappers added as explicit anti-pattern
- Pre-build default: absorption is default, creation is the exception

---

## June 2026 Consolidation (June 15, 2026)

**Trigger:** Forge skill audit (`forge_audit_skills.py`) run as scheduled cron job. Manual review of audit output identified orphan.

| Standalone (deleted) | Absorbed into | As |
|---|---|---|
| ocas-actualization (v1.1.0) | ocas-autobio (v3.5.0) | 3 new references: panel-rubric.md, dream-interpretation.md, dream-journal-email.md; updated architecture.md, evolution-loop.md |

**Root cause (recurrence):** An intermediate rename (autobio → actualization, v1.0-v1.1) created a fork. The parent (autobio) was rewritten as v3.0+ with the same pipeline, leaving both skills active with identical cron jobs, journal outputs, shift tracking, and SOUL.md distillation purpose. The Phase 1 parent check did not catch this because the skills had different names at the time of creation.

**Fix applied:**

- Consolidation followed `forge.consolidate` workflow: read orphan content, identify unique value, fold into parent's existing section structure (no `## Integrated:` wrappers), update Support File Map, bump version, delete orphan directory.
- Unique content from orphan: Writer's Panel rubric (5 named authors, iterative procedure), dream interpretation framework (symbols, archetype, emotional register, core tension), Gmail MCP workaround (chat fallback).
- Parent skill (autobio) already owned the domain — same cron schedule, same storage paths, same ontology types, same distillation targets.

**Lesson:** Phase 1 parent search must check **functional equivalence**, not just name overlap. Two skills with identical cron jobs, journal types, storage layouts, and distillation targets are duplicates even if their names differ.
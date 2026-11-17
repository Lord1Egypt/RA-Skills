<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Data Governance — Derivation Logic

## Purpose

Derives data governance rules (DATA-*) from `database-rules.md`. 100% steering-derived for project-specific rules; built-in baseline provides migration safety floor.

---

## MANDATORY: Stage Sub-Role — Data Architect

During THIS activity, ALSO adopt the mindset of a **Data Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in data safety: schema migrations are irreversible operations that can destroy production data
- Treat migration-safety as Tier A (immediate): a destructive migration is dangerous from the moment it's written
- Derive schema patterns from database-rules.md — DDD aggregates, ERD, document store each have different rules
- Ensure expand-contract is enforced for ALL breaking schema changes (no shortcuts to "just drop the column")
- Consider multi-tenancy implications: if tenant scoping exists, EVERY query must include tenant_id

### Anti-Patterns for This Activity
- Do NOT allow DROP TABLE/COLUMN without expand-contract process documented in the migration
- Do NOT assume database technology — derive from database-rules.md + docker-compose.yml confirmation
- Do NOT generate tenant-scoping rules unless multi-tenancy.md exists (conditional signal)

### Quality Check
A good output from this activity sounds like:
- "DATA-BASELINE-01: Every migration MUST have a rollback/down method. Enforced by migration-safety.json (fileEdited, Tier A 🔴). Pattern: `src/migrations/**/*.ts`. sessionDedup: true."
- "DATA-03: Expand-contract for breaking changes. Verification: any migration containing ALTER TABLE DROP COLUMN must reference a prior expand migration."

---

## Source: `database-rules.md`

| Section to Extract | Generated Rules |
|-------------------|----------------|
| Schema patterns | DATA-01: Schema follows stated pattern (DDD aggregates / ERD / document store) |
| Migration rules | DATA-02: Backward-compatible migrations only; DATA-03: Expand-contract for breaking changes |
| Tenant scoping (if multi-tenant) | DATA-04: Every query scoped to tenant_id |
| Caching strategy | DATA-05: Cache invalidation follows stated pattern |
| Naming conventions (tables/columns) | DATA-06: Table/column naming per stated convention |

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| DATA-BASELINE-01 | Every migration MUST have a rollback/down method |
| DATA-BASELINE-02 | No destructive schema operations (DROP TABLE/COLUMN) without expand-contract |

## Hook: `migration-safety.json`

- **Event:** fileEdited (Tier A 🔴)
- **Pattern:** Migration files (derived from tech-stack — e.g., `Migrations/*.cs`, `src/migrations/*.ts`)
- **Checks:** DATA-BASELINE-01/02, DATA-02/03

## Tier: 1 (baseline) / 2 (full steering-derived set)

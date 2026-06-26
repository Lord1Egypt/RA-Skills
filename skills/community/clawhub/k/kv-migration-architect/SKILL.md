---
name: migration-architect
description: Plan, execute and validate zero-downtime system migrations. Use when migrating databases (schema evolution, data transfer, CDC), services (strangler-fig, canary, blue-green, parallel run), or infrastructure (cloud-to-cloud, on-prem to cloud). Generates phased migration plans, compatibility analysis, rollback procedures, runbooks, stakeholder communication templates, and success metrics.
compatibility: Requires Python 3.8+ for scripts in scripts/.
---

# Migration Architect

Convert a migration request into a structured, zero-downtime plan with tested rollback procedures.

## Activation

Use this skill when the user asks to:
- migrate a database schema, data set, or storage layer
- move a service or API to a new implementation or platform
- migrate infrastructure between clouds or from on-prem
- assess migration risk, compatibility, or rollback options
- generate runbooks, checklists, or stakeholder comms for a migration

## Workflow

1. **Classify** the migration type: `database` | `service` | `infrastructure` | `hybrid`.
2. **Load patterns** for that type from `{baseDir}/references/migration_patterns_catalog.md`.
3. **Run compatibility check** if schemas or APIs are provided:
   ```bash
   python {baseDir}/scripts/compatibility_checker.py --before=<old> --after=<new>
   ```
4. **Identify dominant zero-downtime technique** (expand-contract, dual-write, CDC, strangler-fig, blue-green, canary). Load `{baseDir}/references/zero_downtime_techniques.md` if the best technique is unclear.
5. **Generate migration plan** with phased execution:
   ```bash
   python {baseDir}/scripts/migration_planner.py --config=<config.json>
   ```
6. **Generate rollback procedures** for each phase:
   ```bash
   python {baseDir}/scripts/rollback_generator.py --plan=<plan.json>
   ```
7. **Define validation checkpoints**: row counts, checksums, business-logic queries. Load `{baseDir}/references/data_reconciliation_strategies.md` for reconciliation patterns.
8. **Emit output**: phased plan + rollback procedures + runbook checklists + success metrics.

## Output Contract

- Open with migration classification and dominant risk.
- Emit one phased plan with explicit rollback trigger per phase.
- Include pre/during/post checklists as Markdown task lists.
- Declare `Functor Information Loss` (or equivalent: `Irreversible Data Loss Risk`) when a phase cannot be rolled back.
- Close with success metrics (technical + business) and monitoring window recommendation.

## Risk Tiers

| Tier | Criteria | Required before execution |
|------|----------|--------------------------|
| LOW | additive schema changes, no data transformation | staging validation |
| MEDIUM | data transformation, dual-write window, service cutover | staging + load test + rollback drill |
| HIGH | destructive changes, cross-cloud, compliance scope | all above + stakeholder sign-off |

## Guardrails

- Never recommend irreversible steps without an explicit rollback procedure.
- Always separate migration phases so each can be independently rolled back.
- Flag when the target system cannot express all constraints of the source (`Information Loss`).
- Do not generate feature-flag code or circuit-breaker implementations unless explicitly asked — reference the patterns in `references/` instead.

## Self Check

Before emitting the plan, verify:
- each phase has a rollback procedure;
- validation checkpoints are defined between phases;
- risk tier is declared and prerequisites are listed;
- no phase assumes success of a prior phase without a checkpoint.

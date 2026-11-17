<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Brownfield Steering Templates

> **Purpose:** Used by the project-init-agent to generate brownfield-specific steering files
> in the target project's `rules/` folder. These templates encode reverse-engineered
> business rules, characterization test requirements, legacy behavior preservation rules,
> and incremental modernization patterns. Generated ONLY when `brownfield-patterns.md` exists.
>
> **Note:** These templates produce STUB files that follow the pattern below.
> Actual content comes from reverse-engineering sessions against the existing codebase.
> The init agent creates the structure; the team fills in discovered rules.

---

## brownfield-{component_name}.md (FileMatch `{component_path_pattern}`)

**Generates**: `rules/brownfield-{component_name}.md` (one per legacy component)
**Condition**: Generated only IF `brownfield-patterns.md` exists in workspace steering
**Derived From**: brownfield-patterns.md + reverse-engineering sessions

> The init agent generates one stub per component identified in `brownfield-patterns.md`.
> Template below is applied per component:

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{component_path_pattern}"
---

# {Component_Display_Name} Rules (derived from legacy {legacy_system_identifier})

## {Business_Rule_Category_1} (derived from {legacy_function_reference})

### {Rule_Group_1}
{for_each_discovered_rule}
- {rule_condition} → {rule_behavior}
  - {edge_case_notes}
  - {confirmed_with_note} (if business confirmation obtained)
{end_for_each}

### {Rule_Group_2}
{for_each_discovered_rule}
- {rule_condition} → {rule_behavior}
  - TODO: {unconfirmed_behavior_note} (needs business confirmation)
{end_for_each}

### Constraints
{for_each_constraint}
- {constraint_description}
  - Enforcement: {enforcement_mechanism}
{end_for_each}

### Rounding / Precision
- {precision_rules}

### Characterization Test Reference
- Full characterization test suite: {characterization_test_path}
- Any new implementation MUST pass all characterization tests before deployment
```

---

## brownfield-integration-map.md (Always — within brownfield scope)

**Generates**: `rules/brownfield-integration-map.md`
**Condition**: Generated alongside brownfield component stubs
**Derived From**: brownfield-patterns.md + integration analysis

```markdown
---
inclusion: always
---

# Brownfield Integration Map

## Legacy System Inventory
{for_each_legacy_system}
| System | Status | Integration Type | Data Flow | Migration Strategy |
|--------|:------:|-----------------|-----------|-------------------|
| {system_name} | {status} | {integration_type} | {data_flow_direction} | {migration_strategy} |
{end_for_each}

## Strangler Fig Boundaries
- New code path: {new_code_boundary}
- Legacy code path: {legacy_code_boundary}
- Router/facade: {routing_mechanism}
- Cutover criteria: {cutover_criteria}

## Data Migration Rules
- {data_coexistence_strategy}
- {dual_write_policy}
- {data_reconciliation_approach}
- Rollback strategy: {rollback_mechanism}

## Characterization Testing Requirements
- Every legacy behavior being replaced MUST have characterization tests BEFORE modification
- Characterization tests verify: {characterization_scope}
- Test location: {characterization_test_location}
- Minimum coverage of legacy paths: {characterization_coverage_target}
```

---

## brownfield-modernization-rules.md (Always — within brownfield scope)

**Generates**: `rules/brownfield-modernization-rules.md`
**Derived From**: brownfield-patterns.md + architecture-principles.md

```markdown
---
inclusion: always
---

# Brownfield Modernization Rules

## Core Principles
- Behavior MUST be IDENTICAL even though implementation differs
- NEVER change business behavior during modernization (separate concerns)
- {incremental_delivery_strategy}
- {feature_parity_verification}

## New vs. Legacy Code
- New code: follows ALL current architecture standards
- Legacy code (untouched): exempt from current standards until migrated
- Legacy code (being modified): MUST be brought up to current standards for the touched area
- {legacy_exemption_tracking}

## Risk Management
- {rollback_capability_requirement}
- {canary_deployment_strategy}
- {monitoring_during_migration}
- {incident_response_during_cutover}

## Definition of Done (Brownfield-Specific)
- [ ] Characterization tests pass for all affected legacy behavior
- [ ] New implementation produces identical output for same input
- [ ] Performance is equal or better than legacy (benchmarked)
- [ ] Rollback path tested and documented
- [ ] Legacy code path can be re-enabled without deployment
- [ ] {additional_brownfield_dod_criteria}
```

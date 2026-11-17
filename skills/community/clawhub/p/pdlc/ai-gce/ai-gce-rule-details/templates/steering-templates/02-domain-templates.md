<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Domain Steering Templates

> **Purpose:** Used by the project-init-agent to generate domain-specific steering files
> in the target project's `rules/` folder. These templates encode bounded context rules,
> layer patterns, and domain-specific conventions derived from `domain-context.md` and `module-structure.md`.

---

## domain-core.md (Always)

**Generates**: `rules/domain-core.md`
**Derived From**: domain-context.md + architecture-principles.md + module-structure.md

```markdown
---
inclusion: always
---

# Domain Architecture Standards

## Module Communication
- Modules communicate only through {inter_module_communication_mechanism}
- NEVER make direct cross-module database queries
- NEVER reference another module's internal types or entities
- All cross-module data access goes through published contracts

## Entity Conventions
- {protected_record_type} entities need: {required_audit_fields}
- {soft_delete_policy}
- All entities must have optimistic concurrency control ({concurrency_mechanism})

## Domain Modeling
- One aggregate root per {bounded_context_concept}
- Aggregates enforce their own invariants
- Cross-aggregate references by ID only ({id_type})
- Domain events for cross-module side effects
```

---

## domain-{module_name}.md (FileMatch `{module_path_pattern}`)

**Generates**: `rules/domain-{module_name}.md` (one per bounded context)
**Derived From**: domain-context.md (ubiquitous language section for this module)

> **Note:** The init agent generates ONE file per bounded context identified in `domain-context.md`.
> Below is the parameterized template applied per module.

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{module_path_pattern}"
---

# {Module_Display_Name} Domain Rules

## Core Invariants
{for_each_invariant}
- {invariant_description}
{end_for_each}

## Key Value Objects
{for_each_value_object}
- {value_object_name}: {value_object_description}
  - Fields: {value_object_fields}
  - Validation: {value_object_validation_rules}
{end_for_each}

## State Transitions
{for_each_stateful_entity}
- {entity_name} lifecycle: {valid_states}
  - Allowed transitions: {transition_rules}
  - Transition events: {transition_event_names}
{end_for_each}

## Business Rules
{for_each_business_rule}
- {rule_id}: {rule_description}
  - Enforced at: {enforcement_layer}
  - Violation response: {violation_behavior}
{end_for_each}
```

---

## layer-domain.md (FileMatch `{domain_layer_pattern}`)

**Generates**: `rules/layer-domain.md`
**Derived From**: architecture-principles.md + domain-context.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{domain_layer_pattern}"
---

# Domain Layer Patterns

## Entities
- Aggregate roots: inherit {aggregate_root_base_class}
- Child entities: inherit {child_entity_base_class} (no tenant — owned by root)
- {constructor_visibility_rule}
- Factory method: {factory_method_signature}
- No public setters — state changes via behavior methods
- Collections: {collection_encapsulation_pattern}

## Value Objects
- Inherit {value_object_base_class}, override {equality_method}
- Immutable: all properties read-only
- Self-validating: factory returns {result_type} for invalid input
- Catalog: {project_value_object_catalog}

## Domain Events
- Inherit {domain_event_base_class}
- Past tense naming: {event_naming_pattern} (e.g., {example_domain_events})
- Contain IDs + essential data only (not full entities)
- Raised via {domain_event_raise_mechanism} — dispatched on {dispatch_trigger}

## Domain Services
- For logic that doesn't belong to a single entity
- Stateless (no instance fields)
- Injected via interface (for testability)
- Examples: {example_domain_services}
```

---

## layer-api.md (FileMatch `{presentation_layer_pattern}`)

**Generates**: `rules/layer-api.md`
**Derived From**: api-standards.md + tech-stack.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{presentation_layer_pattern}"
---

# API Layer Patterns

## Endpoint Organization
- {endpoint_class_pattern}
- {endpoint_registration_pattern}
- Group under: {api_route_prefix}/{module}/{resource}
- {api_documentation_strategy}
- Auth required: {auth_requirement_pattern}

## HTTP Conventions
- POST create → 201 + Location header
- GET single → 200 or 404
- GET list → 200 (ALWAYS paginated)
- PUT update → 200 or 404/409/422
- DELETE → {delete_status_code} ({delete_strategy})
- Action → {action_route_pattern}

## Response Format
- Success: resource DTO with {standard_response_fields}
- List: {pagination_wrapper} with {pagination_fields}
- Error: {error_format} with {error_fields}
- Validation error: 400 + {validation_error_structure}
- Business error: 422 + {business_error_code_pattern}

## Request Validation
- Use {validation_framework} ({validator_base_class})
- Validate at {validation_layer} level (before handler)
- Return 400 with field-level error messages
- NEVER validate in domain layer what can be caught at API level
```

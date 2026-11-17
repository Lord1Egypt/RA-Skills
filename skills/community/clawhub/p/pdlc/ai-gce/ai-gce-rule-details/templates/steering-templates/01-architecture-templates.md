<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Architecture Steering Templates

> **Purpose:** Used by the project-init-agent to generate architecture-related steering files
> in the target project's `rules/` folder. Templates are parameterized with `{variables}`
> that the init agent populates from project context (tech-stack, module-structure, architecture decisions).

---

## architecture-core.md (Always)

**Generates**: `rules/architecture-core.md`
**Derived From**: tech-stack.md + module-structure.md + architecture-principles.md

```markdown
---
inclusion: always
---

# Architecture Standards

## Architecture Style
- {architecture_style}: {architecture_style_description}
- Each module is a {module_deployment_unit} within the {deployment_model}
- Modules communicate ONLY via {inter_module_communication_mechanism}
- NEVER reference another module's internal layers directly

## Module Structure (MANDATORY for every module)
```
{module_root_path}/{ModuleName}/
├── {public_contract_layer}/     ← PUBLIC: interfaces, DTOs, events, errors
├── {domain_layer}/              ← Entities, value objects, domain events
├── {application_layer}/         ← Commands, queries, validators, mappings
├── {infrastructure_layer}/      ← Data access, repositories, external adapters
└── {presentation_layer}/        ← API endpoints / UI components
```

## Layer Dependencies (STRICT)
- {domain_layer} → nothing (no dependencies)
- {application_layer} → {domain_layer} only
- {infrastructure_layer} → {domain_layer} only (implements interfaces)
- {presentation_layer} → {application_layer} only
- {public_contract_layer} → shared kernel only

## Entity Hierarchy
- All entities inherit from appropriate base class:
  - {base_entity_class}: {base_entity_fields}
  - {auditable_entity_class}: + {audit_fields}
  - {soft_deletable_entity_class}: + {soft_delete_fields} (for {soft_delete_use_case})
  - {tenant_entity_class}: + {tenant_id_field} (for multi-tenant entities)
- {protected_record_type} entities MUST use {soft_deletable_entity_class} or {tenant_entity_class}
- NEVER hard-delete {protected_record_type} records

## Data Access
- {data_access_pattern}: {data_access_description}
- {schema_isolation_strategy}
- {repository_pattern_description}
- {read_optimization_strategy} for all read queries
- {projection_strategy} for list queries — never load full entities for lists

## API Standards
- {api_framework_pattern}: {api_framework_description}
- All endpoints require authentication
- Authorization via {authorization_strategy}
- All errors use {error_format} format
- All list endpoints are paginated ({pagination_strategy})
- {idempotency_strategy}
- Response includes standard audit fields ({response_audit_fields})
```

---

## architecture-domain.md (FileMatch `{domain_layer_pattern}`)

**Generates**: `rules/architecture-domain.md`
**Derived From**: module-structure.md + domain-context.md + architecture-principles.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{domain_layer_pattern}"
---

# Domain Layer Rules

## Aggregates
- One aggregate root per business concept ({example_aggregates})
- Children are owned by the root (cascade lifecycle)
- Reference other aggregates by ID only ({id_type}), never navigation properties
- All invariants enforced in the aggregate root
- Use factory methods ({factory_method_pattern}) — never public constructors for aggregates
- Factory methods return {result_type} — never throw for business rule violations

## Value Objects
- {value_object_base_class}
- Immutable (all properties are read-only)
- Equality by value (not reference)
- Self-validating (constructor/factory rejects invalid state)
- Use for: {example_value_objects}

## Domain Events
- {domain_event_base_class}
- Named in past tense: {example_domain_events}
- Contain only IDs and essential data (not full entities)
- Published via {domain_event_publishing_mechanism}

## {domain_specific_type} Rules ({domain_critical_label})
- ALWAYS use the {domain_value_type} value object for {domain_critical_values}
- NEVER use {prohibited_types} for {domain_critical_values}
- {domain_value_type} has: {domain_value_type_fields}
- All arithmetic through {domain_value_type} methods ({domain_value_type_operations})
- {rounding_strategy}
```

---

## architecture-infrastructure.md (FileMatch `{infrastructure_layer_pattern}`)

**Generates**: `rules/architecture-infrastructure.md`
**Derived From**: tech-stack.md + database-rules.md + module-structure.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{infrastructure_layer_pattern}"
---

# Infrastructure Layer Rules

## {orm_framework} Configuration
- {orm_configuration_approach}
- Configure in separate configuration classes, one per entity
- {orm_configuration_discovery}
- {schema_isolation_configuration}

## Database Conventions
- Table names: {table_naming_convention}
- Column names: {column_naming_convention}
- Primary key: {primary_key_convention}
- Foreign key: {foreign_key_convention}
- {domain_specific_column_conventions}
- Always include: {required_column_indexes}

## Repository Implementation
- Implement module-specific repository interface
- Inject module's {db_context_type} (not generic)
- Include related entities only when needed
- Use cancellation tokens on all async operations
- Return {not_found_strategy} for not-found (not exceptions)

## Migrations
- {migration_frequency_rule}
- Descriptive names: {migration_naming_pattern}
- Always implement {rollback_strategy} for rollback
- Never modify existing migrations
- Test: apply → verify → rollback → verify
```

---

## architecture-api.md (FileMatch `{presentation_layer_pattern}`)

**Generates**: `rules/architecture-api.md`
**Derived From**: api-standards.md + tech-stack.md + module-structure.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{presentation_layer_pattern}"
---

# API Layer Rules

## Endpoint Organization
- {endpoint_organization_pattern}
- {endpoint_grouping_strategy}
- {endpoint_auth_requirement}

## HTTP Conventions
- POST (create) → 201 Created + Location header
- GET (single) → 200 OK or 404 Not Found
- GET (list) → 200 OK (always paginated)
- PUT (update) → 200 OK or 404/409/422
- DELETE → {delete_status_code} ({delete_strategy})
- POST (action) → 200 OK or appropriate error

## Request/Response
- Request models: {request_naming_pattern}
- Response models: {response_naming_pattern}
- List response: {list_response_wrapper}
- All responses include: {standard_response_fields}
- Never expose internal entity structure directly

## Error Responses
- All errors return {error_format} format
- Include: {error_response_fields}
- Validation errors: 400 with {validation_error_structure}
- Business rule violations: 422 with {business_error_structure}
- Not found: 404 with resource type and ID
- Unauthorized: 401 (no body)
- Forbidden: 403 with required permission
```

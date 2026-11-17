<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Multi-Tenancy Steering Templates

> **Purpose:** Used by the project-init-agent to generate multi-tenancy steering files
> in the target project's `rules/` folder. These templates encode tenant isolation patterns,
> data partitioning strategy, and cross-tenant protection rules derived from `multi-tenancy.md`
> (conditional — only if multi-tenant architecture exists).

---

## multi-tenancy-core.md (Always — within multi-tenant scope)

**Generates**: `rules/multi-tenancy-core.md`
**Condition**: Generated only IF `multi-tenancy.md` exists in workspace steering
**Derived From**: multi-tenancy.md + security-rules.md + database-rules.md

```markdown
---
inclusion: always
---

# Multi-Tenancy Standards

## Isolation Model
- Isolation strategy: {isolation_model} ({isolation_model_description})
- {tenant_identification_mechanism}
- {tenant_resolution_strategy}

## Data Isolation (CRITICAL)
- ALL business entities MUST include tenant context ({tenant_field_requirement})
- {tenant_filter_mechanism} is MANDATORY on all queries
- NEVER bypass tenant filter ({bypass_prevention_rule})
- {cross_tenant_query_policy}

## Tenant Context
- Tenant identity comes from {tenant_context_source}
- NEVER accept tenant identity from {prohibited_tenant_sources}
- {tenant_context_propagation_strategy}
- {background_job_tenant_context}

## Resource Boundaries
- {resource_quota_strategy}
- {tenant_resource_isolation}
- {shared_resource_policy}
```

---

## multi-tenancy-data.md (FileMatch `{data_access_pattern}`)

**Generates**: `rules/multi-tenancy-data.md`
**Derived From**: multi-tenancy.md + database-rules.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{data_access_pattern}"
---

# Multi-Tenancy Data Layer Rules

## Query Filtering
- ALL queries MUST include tenant filter ({query_filter_implementation})
- {global_filter_mechanism}
- Exception: system-level entities that are truly global ({global_entity_examples})
- NEVER use {filter_bypass_mechanism} for tenant-scoped entities

## Schema Strategy
- {schema_isolation_approach}
- {tenant_schema_creation_strategy}
- {migration_per_tenant_strategy}

## Testing
- ALL data access tests MUST verify tenant isolation
- Test that Tenant A cannot read/write Tenant B data
- Test that queries without tenant context fail ({fail_safe_behavior})
```

---

## multi-tenancy-api.md (FileMatch `{presentation_layer_pattern}`)

**Generates**: `rules/multi-tenancy-api.md`
**Derived From**: multi-tenancy.md + api-standards.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{presentation_layer_pattern}"
---

# Multi-Tenancy API Rules

## Tenant Resolution
- {api_tenant_resolution_mechanism}
- ALL endpoints MUST have tenant context resolved before handler execution
- Missing tenant context → {missing_tenant_response}

## Cross-Tenant Prevention
- NEVER allow tenant switching via request parameters
- NEVER expose tenant IDs in URLs ({tenant_url_policy})
- {admin_cross_tenant_policy}

## Response Isolation
- NEVER include data from other tenants in any response
- List endpoints MUST be automatically filtered to current tenant
- {tenant_aware_pagination}
```

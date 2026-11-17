<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Security & Compliance Steering Templates

> **Purpose:** Used by the project-init-agent to generate security-related steering files
> in the target project's `rules/` folder. These templates encode authentication,
> authorization, data protection, and audit trail standards derived from `security-rules.md`.

---

## security-standards.md (Always)

**Generates**: `rules/security-standards.md`
**Derived From**: security-rules.md + role-isolation.md

```markdown
---
inclusion: always
---

# Security Standards

## Authentication
- ALL API endpoints MUST require authentication (no anonymous access)
- Use {auth_mechanism} with {token_signing_algorithm} validation
- Access tokens expire in {access_token_ttl} (NEVER longer)
- Refresh tokens use {refresh_token_strategy}

## Authorization
- ALL endpoints MUST have explicit authorization requirements
- NEVER allow anonymous access to business endpoints
- Use {authorization_strategy} (not just role checks)
- Implement resource-level checks for sensitive operations
- Segregation of duties: {segregation_rule}

## Tenant Isolation
- {tenant_isolation_strategy}
- {tenant_filter_enforcement}
- NEVER bypass tenant filter ({tenant_bypass_prevention})
- Tenant context comes from {tenant_context_source} — NEVER from request body

## Input Validation
- ALL request DTOs MUST have a validator
- String fields: ALWAYS set maximum length
- Numeric fields: ALWAYS set valid range
- NEVER trust client-provided IDs for authorization (always verify ownership)
- NEVER use string interpolation in database queries

## Data Protection
- PII fields ({pii_field_examples}) MUST be encrypted at field level
- Passwords MUST be hashed with {password_hash_algorithm} (cost factor ≥ {hash_cost_factor})
- Secrets MUST NOT appear in code, config files, or logs
- Connection strings from {secrets_management_strategy} (NEVER hardcoded)

## Error Handling (Security)
- NEVER expose exception messages in API responses (production)
- NEVER expose stack traces in API responses
- NEVER reveal database structure in error messages
- ALWAYS use {error_format} for error responses
- ALWAYS log full error details server-side with correlation ID
- Auth failures: use generic message (don't reveal which part failed)

## Audit Trail
- EVERY create, update, and delete operation MUST be audited
- Audit captures: who, when, what entity, what changed (old → new)
- Audit table is APPEND-ONLY (no updates, no deletes)
- Audit entries include {audit_context_fields}
- {sensitive_operation_type} operations: additional approval audit

## Logging Security
- NEVER log passwords, tokens, or secrets
- NEVER log full {sensitive_identifier_type}
- NEVER log PII in plain text (mask: {masking_examples})
- ALWAYS log: authentication failures, authorization failures, data access violations
```

---

## compliance-standards.md (Always)

**Generates**: `rules/compliance-standards.md`
**Derived From**: security-rules.md + project-governance.md + scope-and-risks.md

```markdown
---
inclusion: always
---

# Compliance Standards

## Audit Trail
- ALL {protected_mutation_type} MUST produce immutable audit records (append-only, never update/delete)
- Audit records MUST include: who, what, when, before-state, after-state, correlation ID
- {audit_tamper_evidence_strategy}
- NEVER allow deletion of audit records regardless of user role

## Data Privacy
- ALL entities containing PII MUST be marked with {pii_marker_attribute}
- PII fields MUST be encrypted at rest using {field_encryption_strategy}
- ALL personal data processing MUST have a documented legal basis
- {anonymization_strategy}
- NEVER log PII in plain text (use structured logging with PII masking)

## Regulatory Requirements
{for_each_regulatory_requirement}
- {requirement_id}: {requirement_description}
  - Enforcement: {enforcement_mechanism}
  - Evidence: {evidence_type}
{end_for_each}

## Segregation of Duties
- {segregation_rule_1}
- {segregation_rule_2}
- ALL segregation violations MUST be logged as security events
```

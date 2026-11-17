<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: multi-tenancy.md (CONDITIONAL)

**Generate IF:** AP contains Multi-Tenancy Architecture document.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Multi-Tenancy Architecture | date: {generation-date} -->

# Multi-Tenancy Rules

## Isolation Model
**Strategy:** {row-level / schema / DB-per-tenant}
**Enforcement:** {middleware + DB-level}
**Identifier:** {UUID in JWT tenant_id claim}

## Tenant Context Propagation
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| MT-CTX-01 | Every request carries tenant context |
| MT-CTX-02 | Source: {JWT claim / header} |
| MT-CTX-03 | Set ONCE at entry — never overridden |
| MT-CTX-04 | Access via: {injection mechanism} |
| MT-CTX-05 | Never access tenant_id directly from request |
| MT-CTX-06 | Background jobs carry tenant context |
| MT-CTX-07 | Events include tenant_id |
<!-- end: AP-sourced -->

## Data Isolation
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| MT-DATA-01 | Every query scoped to tenant |
| MT-DATA-02 | Scoping: {mechanism} |
| MT-DATA-03 | No cross-tenant queries |
| MT-DATA-04 | INSERT sets tenant_id from context |
| MT-DATA-07 | File storage: tenant-prefixed paths |
| MT-DATA-09 | Cache keys include tenant_id |
<!-- end: AP-sourced -->

## Application Enforcement
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| MT-APP-01 | Enforcement layer: {mechanism} |
| MT-APP-02 | All repos extend tenant-aware base |
| MT-APP-05 | Tests: multi-tenant seed data |
| MT-APP-06 | New tables MUST have tenant_id |
<!-- end: AP-sourced -->

## Tenant Lifecycle
<!-- begin: AP-sourced -->
Provisioning → Configuration → Deactivation → Deletion
{Rules MT-LIFE-01 through MT-LIFE-11}
<!-- end: AP-sourced -->

## Cross-Tenant Scenarios
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| MT-CROSS-01 | Platform admin: {capabilities} |
| MT-CROSS-02 | Impersonation: {rules} |
| MT-CROSS-04 | Shared reference data: {rules} |
<!-- end: AP-sourced -->

## Anti-Patterns (Security Violations)
1. NEVER query without tenant filter
2. NEVER trust tenant_id from user input
3. NEVER share cache across tenants
4. NEVER store files without tenant prefix
```

## Filling: Refer to `mapping/tenancy-to-steering.md`.

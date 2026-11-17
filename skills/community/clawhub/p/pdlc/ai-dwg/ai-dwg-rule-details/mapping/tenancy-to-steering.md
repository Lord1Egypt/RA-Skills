<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Multi-Tenancy Architecture → multi-tenancy.md (CONDITIONAL)

## Purpose

This mapping rule transforms the **Multi-Tenancy Architecture** document (AP artifact) into a steering file that enforces tenant isolation across every layer of the system — from API request through data storage.

**Output:** `rules/multi-tenancy.md`

**Condition:** Generate ONLY IF the AP contains a Multi-Tenancy Architecture document. Skip for single-tenant systems.

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Treat EVERY tenant isolation failure as a security breach — the language must reflect this severity
- Think about enforcement at every layer simultaneously: API → service → repository → cache → storage → background jobs → events
- Ensure rules are infrastructure-enforced (middleware, base classes) not voluntarily followed — developers will forget, infrastructure won't
- Cross-reference security-rules.md TENANT-NN rules — this file covers the full isolation mechanism; security covers the access control aspect
- Write test requirements into the rules — multi-tenant seed data is mandatory, not optional

### Anti-Patterns for This Activity
- Do NOT write rules that rely on developer discipline alone — enforce via infrastructure (base repository, middleware)
- Do NOT allow any "convenience" exceptions for cross-tenant access without platform admin flag + audit
- Do NOT forget async contexts — background jobs and events are the most common source of tenant leakage

### Quality Check
A good output from this activity sounds like:
- "MT-DATA-01: EVERY database query MUST be scoped to the active tenant. No exceptions (except platform admin with explicit flag). Enforcement: base repository class."
- "MT-CTX-06: Background jobs MUST carry tenant context from the originating request — never assume a default tenant."

---

## Trigger Condition

| Generate | Skip |
|----------|------|
| AP contains a dedicated Multi-Tenancy Architecture document | No multi-tenancy document in AP |
| `adlc-state.md` shows Stage 7 (Multi-Tenancy) was completed | Stage 7 was explicitly skipped |
| System Context (C4 L1) shows multiple customer organizations | System serves a single organization |

---

## Source (AP Artifact)

**Document:** Multi-Tenancy Architecture (typically `05_MultiTenancy_Architecture.md` or `decisions/multi-tenancy.md`)

**Sections to extract:**

| Section | Contains | What to Extract |
|---------|----------|----------------|
| Isolation Model | DB-per-tenant / schema-per-tenant / row-level | Core isolation pattern |
| Tenant Context Propagation | How requests carry tenant identity | Propagation mechanism rules |
| Tenant Lifecycle | Provisioning, config, deactivation, deletion | Lifecycle process rules |
| Cross-Tenant Scenarios | Platform admin, shared services | Exception rules |
| Application Enforcement | Middleware, guards, base classes | Enforcement layer rules |
| Storage/File Isolation | File partitioning per tenant | Storage isolation rules |
| Tenant Configuration | Per-tenant settings, feature toggles | Configuration rules |

**Additional sources:**
- Security Architecture (authentication → tenant extraction from token)
- Data Architecture (tenant_id column, scoping queries)
- Related ADR (isolation strategy decision)

---

## Target: multi-tenancy.md

### Role

The most enforcement-critical steering file for multi-tenant systems. A single tenant isolation failure is a security breach. This file ensures that tenant boundaries are enforced at EVERY layer — and that no code can accidentally leak data across tenants.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Multi-Tenancy Architecture | date: {generation-date} -->

# Multi-Tenancy Rules

## Isolation Model

**Strategy:** {from AP — e.g., Row-level isolation with tenant_id column}
**Enforcement:** {from AP — e.g., Application middleware + DB-level RLS policies}
**Tenant identifier:** {from AP — e.g., UUID in JWT claim `tenant_id`}

---

## Tenant Context Propagation

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| MT-CTX-01 | Every authenticated request MUST carry tenant context. Requests without tenant context are REJECTED (except platform admin endpoints). |
| MT-CTX-02 | Tenant context source: {from AP — e.g., extracted from JWT `tenant_id` claim by authentication middleware}. |
| MT-CTX-03 | Tenant context MUST be set ONCE at request entry (middleware) — NEVER overridden downstream. |
| MT-CTX-04 | Tenant context is available via: {from AP — e.g., request-scoped injection / AsyncLocalStorage / thread-local}. |
| MT-CTX-05 | DO NOT access tenant_id directly from the request object in services/repositories — use the injected tenant context service. |
| MT-CTX-06 | Background jobs / async processes MUST carry tenant context from the originating request — never assume a default tenant. |
| MT-CTX-07 | Event payloads MUST include `tenant_id` — consumers validate tenant context on receipt. |

<!-- end: AP-sourced -->

---

## Data Isolation

<!-- begin: AP-sourced -->

### Query Scoping

| Rule | Standard |
|------|----------|
| MT-DATA-01 | EVERY database query MUST be scoped to the active tenant. No exceptions (except platform admin with explicit flag). |
| MT-DATA-02 | Scoping mechanism: {from AP — e.g., base repository class adds `WHERE tenant_id = ?` automatically}. |
| MT-DATA-03 | DO NOT write queries that can return data from multiple tenants — even for "aggregation" or "reporting". |
| MT-DATA-04 | INSERT operations MUST set `tenant_id` from the active context — NEVER from user input. |
| MT-DATA-05 | Tenant_id column: {from AP — e.g., NOT NULL, indexed, part of composite primary keys where applicable}. |
| MT-DATA-06 | Foreign key references within a tenant: ensure referencing row belongs to the SAME tenant. |

### Storage Isolation

| Rule | Standard |
|------|----------|
| MT-DATA-07 | File/object storage: {from AP — e.g., tenant-prefixed paths: `/{tenant_id}/attachments/{file_id}`}. |
| MT-DATA-08 | DO NOT allow file access without verifying the requesting user belongs to the file's tenant. |
| MT-DATA-09 | Cache keys MUST include tenant_id: `{tenant_id}:{entity}:{id}` — NEVER share cache entries across tenants. |
| MT-DATA-10 | Search indexes: {from AP — e.g., single index with tenant_id filter / separate index per tenant}. |

<!-- end: AP-sourced -->

---

## Application Enforcement

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| MT-APP-01 | Tenant enforcement layer: {from AP — e.g., middleware validates tenant on EVERY request before reaching controllers}. |
| MT-APP-02 | Repository base class: ALL repositories MUST extend the tenant-aware base that auto-applies scoping. |
| MT-APP-03 | DO NOT create repositories that bypass tenant scoping — if platform admin needs cross-tenant, use an explicit `PlatformRepository` with audit logging. |
| MT-APP-04 | Unit tests: MUST verify tenant isolation — test that Tenant A cannot access Tenant B's data. |
| MT-APP-05 | Integration tests: run with at least 2 tenants seeded — verify no cross-tenant leakage. |
| MT-APP-06 | New entities: every new database table MUST include `tenant_id` column unless explicitly justified as platform-level (e.g., system config). |

<!-- end: AP-sourced -->

---

## Tenant Lifecycle

<!-- begin: AP-sourced -->

### Provisioning

| Rule | Standard |
|------|----------|
| MT-LIFE-01 | Tenant provisioning: {from AP — e.g., API endpoint creates tenant record, seeds default config, creates admin user}. |
| MT-LIFE-02 | New tenant setup includes: {from AP — e.g., default roles, default workflows, default SLA templates}. |
| MT-LIFE-03 | Tenant provisioning is idempotent — re-running with same ID does not create duplicates. |

### Configuration

| Rule | Standard |
|------|----------|
| MT-LIFE-04 | Per-tenant configuration: {from AP — e.g., stored in `tenant_settings` table, cached with TTL}. |
| MT-LIFE-05 | Configuration changes take effect: {from AP — e.g., immediately (cache invalidation) / next request}. |
| MT-LIFE-06 | Tenant branding / white-label: {from AP — e.g., tenant-specific theme, logo, domain stored in config}. |

### Deactivation & Deletion

| Rule | Standard |
|------|----------|
| MT-LIFE-07 | Tenant deactivation: {from AP — e.g., sets `is_active = false`, blocks all API access for that tenant, preserves data}. |
| MT-LIFE-08 | Deactivated tenant: requests return 403 with message "Tenant suspended" — no data access possible. |
| MT-LIFE-09 | Tenant deletion (hard): {from AP — e.g., scheduled job after 30-day grace period, removes ALL tenant data including files, cache, search index}. |
| MT-LIFE-10 | Deletion is irreversible — require explicit confirmation + audit trail. |
| MT-LIFE-11 | Deletion scope: {from AP — e.g., all rows with tenant_id, all files in tenant prefix, all cache keys with tenant prefix, search index entries}. |

<!-- end: AP-sourced -->

---

## Cross-Tenant Scenarios

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| MT-CROSS-01 | Platform admin (super-admin): {from AP — e.g., can view any tenant's data for support, CANNOT modify without impersonation}. |
| MT-CROSS-02 | Admin impersonation: {from AP — e.g., sets tenant context explicitly, all actions logged as "admin acting as tenant X"}. |
| MT-CROSS-03 | Cross-tenant reporting: {from AP — e.g., only platform-level aggregated metrics, never raw data across tenants}. |
| MT-CROSS-04 | Shared reference data: {from AP — e.g., system-level lookup tables (countries, timezones) have no tenant_id — available to all}. |
| MT-CROSS-05 | Cross-tenant data transfer: {from AP — e.g., NOT supported / supported only via export-import with explicit consent}. |

<!-- end: AP-sourced -->

---

## Validation Checklist (For Every PR)

Every PR that touches data access, caching, file storage, or background jobs MUST verify:

- [ ] Queries include tenant scoping (MT-DATA-01)
- [ ] New tables have `tenant_id` column (MT-APP-06)
- [ ] Cache keys include tenant_id (MT-DATA-09)
- [ ] File paths include tenant prefix (MT-DATA-07)
- [ ] Background jobs carry tenant context (MT-CTX-06)
- [ ] Events include tenant_id in payload (MT-CTX-07)
- [ ] No cross-tenant query possible without platform admin flag (MT-DATA-03)
- [ ] Tests verify isolation with multi-tenant seed data (MT-APP-05)

---

## Anti-Patterns (CRITICAL — Security Violations)

1. **NEVER** query without tenant_id filter — this is a DATA BREACH
2. **NEVER** trust tenant_id from user input (request body/params) — always use authenticated context
3. **NEVER** share cache entries across tenants — this is a DATA BREACH
4. **NEVER** store files without tenant-prefixed path — this enables unauthorized access
5. **NEVER** create a "global" query for convenience — if you need cross-tenant, use PlatformRepository with explicit audit
6. **NEVER** let tenant_id be NULL in any tenant-scoped table — constraint must be NOT NULL
7. **NEVER** assume "the current tenant" in background jobs — always pass explicitly
8. **NEVER** log tenant-specific data without marking the tenant in the log entry
9. **NEVER** allow one tenant's webhook/integration to accidentally target another tenant's data
10. **NEVER** skip tenant isolation in tests — "it works for one tenant" is not sufficient
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Isolation model (row-level/schema/DB) | Set Isolation Model header + drive all subsequent rules | Header + all sections |
| Context propagation mechanism | Convert to MT-CTX-NN rules | Context Propagation |
| Scoping approach (middleware, base class) | Convert to MT-DATA + MT-APP rules | Data Isolation + App Enforcement |
| Provisioning process | Convert to MT-LIFE-01 through MT-LIFE-03 | Lifecycle: Provisioning |
| Per-tenant config approach | Convert to MT-LIFE-04 through MT-LIFE-06 | Lifecycle: Configuration |
| Deactivation/deletion process | Convert to MT-LIFE-07 through MT-LIFE-11 | Lifecycle: Deactivation & Deletion |
| Platform admin capabilities | Convert to MT-CROSS-NN rules | Cross-Tenant Scenarios |
| File/storage isolation | Convert to MT-DATA-07, MT-DATA-08 | Storage Isolation |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| MT-CTX-NN | Tenant context propagation |
| MT-DATA-NN | Data and storage isolation |
| MT-APP-NN | Application-level enforcement |
| MT-LIFE-NN | Tenant lifecycle |
| MT-CROSS-NN | Cross-tenant scenarios |

---

## Cross-References

This file is enforced alongside (must be consistent with):

| File | Relationship |
|------|-------------|
| `security-rules.md` | TENANT-NN rules cover security aspects; this file covers full isolation |
| `database-rules.md` | DB-QUERY-03 references tenant scoping; this file details the mechanism |
| `observability-logging.md` | Logs must include tenant_id (MT-CTX context) |
| `observability-sensitive.md` | Tenant data must not leak in logs |
| `api-standards.md` | API responses scoped to active tenant |

---

## Key Rules for This Mapping

1. **This file treats isolation failures as SECURITY BREACHES** — language must reflect severity
2. **Tenant scoping is not optional per query** — it's enforced by infrastructure (base class/middleware)
3. **Every layer is covered** — API, service, repository, cache, storage, search, events, background jobs
4. **Tests must prove isolation** — multi-tenant seed data is mandatory in test setup
5. **Platform admin is the ONLY exception** — and it's audited
6. **Propagation mechanism is specific** — "from JWT claim" or "from middleware" not "somehow available"
7. **Lifecycle covers the full journey** — provision → configure → deactivate → delete

---

## Depth Adaptation

| Depth | multi-tenancy.md |
|-------|-----------------|
| **Minimal** | Context propagation + data isolation rules + basic anti-patterns (~15 rules) |
| **Standard** | Full structure as defined above — all sections (~35-40 rules) |
| **Comprehensive** | Full structure + tenant migration scenarios + multi-region tenant routing + tenant-level feature flags + performance isolation (noisy neighbor prevention) |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Isolation model changed (e.g., row → schema) | ENTIRE file rewrite | Flag CRITICAL — fundamental architecture change |
| Propagation mechanism changed | MT-CTX rules updated | Update; review all layers that consume context |
| New tenant lifecycle phase added | MT-LIFE rules added | Add; signal AI-GCE for lifecycle hooks |
| Platform admin capabilities expanded | MT-CROSS rules updated | Update; ensure audit coverage |
| Tenant deletion policy changed | MT-LIFE-09 through MT-LIFE-11 | Update; review for compliance impact |
| Multi-tenancy REMOVED from architecture | File no longer justified | Flag for deletion; remove from conditional set |

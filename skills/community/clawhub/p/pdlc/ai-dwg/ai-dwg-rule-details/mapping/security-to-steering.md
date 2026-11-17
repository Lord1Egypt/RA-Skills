<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Security & Identity Architecture → security-rules.md

## Purpose

This mapping rule transforms the **Security & Identity Architecture** document (AP artifact) into a steering file that enforces authentication, authorization, data protection, and security best practices across all development activity.

**Output:** `rules/security-rules.md`

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Treat every rule as a potential breach vector if violated — write with the severity that implies
- Ensure OWASP Top 10 coverage is complete even if the AP doesn't explicitly list every mitigation
- Think in layers: authentication → authorization → data protection → audit — each layer must be independently enforceable
- Cross-reference with observability-sensitive.md — what never to log must be consistent with what's protected here
- Write rules with specific values ("expire after 15 minutes") not vague guidance ("expire after a reasonable time")

### Anti-Patterns for This Activity
- Do NOT substitute your preferred security patterns for what the AP specifies (e.g., if AP says bcrypt, use bcrypt — don't swap in Argon2)
- Do NOT generate vague security guidance — every rule must be binary testable (pass/fail)
- Do NOT separate tenant isolation from security — cross-tenant access is a data breach, not a feature gap

### Quality Check
A good output from this activity sounds like:
- "AUTH-04: Tokens MUST be stored in httpOnly secure cookies — NEVER localStorage (XSS vulnerable). Source: Security Architecture §Token Strategy."
- "SEC-01: ALL user input MUST be validated — type, length, format, range. No unvalidated input reaches business logic."

---

## Source (AP Artifact)

**Document:** Security & Identity Architecture (typically `06_Security_Identity_Architecture.md` or `decisions/security-identity.md`)

**Sections to extract:**

| Section | Contains | What to Extract |
|---------|----------|----------------|
| Authentication Architecture | Auth methods, token strategy, SSO | Authentication rules |
| Authorization Architecture | RBAC model, permission enforcement, data access | Authorization rules |
| Data Protection | Encryption at rest/transit, secrets mgmt | Data protection rules |
| Audit & Compliance | Audit logging strategy, compliance controls | Audit requirements |
| Threat Considerations | OWASP mitigations, API security | Security coding rules |
| Token Strategy | JWT/session, refresh, rotation | Token handling rules |
| Secret Management | How secrets are stored/accessed | Secret access patterns |

**Additional sources:**
- Related ADRs (authentication approach, authorization model, encryption decisions)
- Multi-Tenancy Architecture (if exists — tenant isolation affects security)

---

## Target: security-rules.md

### Role

The definitive security constraint file. Every line of code that touches authentication, authorization, data protection, or external communication must comply with these rules. This file is one of the most enforcement-critical — AI-GCE derives multiple hooks from it.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Security & Identity Architecture | date: {generation-date} -->

# Security Rules

## Security Model Summary

**Authentication:** {method — e.g., JWT with refresh tokens, OIDC, session-based}
**Authorization:** {model — e.g., RBAC with hierarchical roles}
**Encryption at rest:** {algorithm — e.g., AES-256}
**Encryption in transit:** {standard — e.g., TLS 1.3 minimum}
**Secrets management:** {approach — e.g., environment variables via vault}
**Audit:** {strategy — e.g., all auth events + data mutations logged}

---

## Authentication Rules

<!-- begin: AP-sourced -->

### Token Handling

| Rule | Description |
|------|-------------|
| AUTH-01 | {Token type} MUST be used for all API authentication. No alternative auth mechanisms without ADR. |
| AUTH-02 | Access tokens MUST expire after {duration from AP}. No long-lived tokens. |
| AUTH-03 | Refresh tokens MUST be {rotation policy from AP — e.g., single-use, rotated on every refresh}. |
| AUTH-04 | Tokens MUST be stored {storage location — e.g., httpOnly secure cookies, NEVER localStorage}. |
| AUTH-05 | Token payload MUST contain: {required claims from AP — e.g., sub, tenant_id, roles, exp}. |
| AUTH-06 | Token validation MUST occur on EVERY request — no caching of auth decisions beyond token lifetime. |

### Authentication Methods

| Rule | Description |
|------|-------------|
| AUTH-07 | Supported authentication methods: {list from AP — e.g., local credentials, LDAP, SAML 2.0, OIDC}. |
| AUTH-08 | Password policy: {requirements from AP — e.g., min 12 chars, complexity, no reuse of last 10}. |
| AUTH-09 | MFA: {policy from AP — e.g., required for admin roles, optional for standard users}. |
| AUTH-10 | Failed login: lock account after {n} attempts for {duration}. Log all failures. |

### Session Management

| Rule | Description |
|------|-------------|
| AUTH-11 | Session timeout: {duration from AP — e.g., 30 minutes idle, 8 hours absolute}. |
| AUTH-12 | Concurrent sessions: {policy from AP — e.g., max 3 per user, new session invalidates oldest}. |
| AUTH-13 | Session invalidation MUST occur on: password change, role change, explicit logout, security event. |

<!-- end: AP-sourced -->

---

## Authorization Rules

<!-- begin: AP-sourced -->

### RBAC Model

| Rule | Description |
|------|-------------|
| AUTHZ-01 | Authorization model: {model from AP — e.g., RBAC with hierarchical roles}. |
| AUTHZ-02 | Roles defined: {role list from AP — e.g., SuperAdmin, TenantAdmin, Agent, EndUser, ReadOnly}. |
| AUTHZ-03 | Role hierarchy: {hierarchy from AP — e.g., SuperAdmin > TenantAdmin > Agent > EndUser}. |
| AUTHZ-04 | Permission granularity: {level from AP — e.g., resource-level (CRUD per entity type)}. |
| AUTHZ-05 | Permission checking MUST happen at {enforcement point from AP — e.g., controller/guard level AND service level}. |

### Data Access Control

| Rule | Description |
|------|-------------|
| AUTHZ-06 | Row-level security: {approach from AP — e.g., tenant_id filter on ALL queries, enforced by middleware}. |
| AUTHZ-07 | Field-level security: {approach from AP — e.g., PII fields hidden from non-admin roles}. |
| AUTHZ-08 | Ownership checks: {pattern from AP — e.g., user can only modify their own resources unless admin}. |
| AUTHZ-09 | NEVER return data the requesting user is not authorized to see — filter BEFORE response, not after. |

### Permission Enforcement

| Rule | Description |
|------|-------------|
| AUTHZ-10 | Default deny: if no explicit permission grants access, the request is REJECTED. |
| AUTHZ-11 | Permission evaluation: {order from AP — e.g., check role → check resource permission → check data scope}. |
| AUTHZ-12 | Admin bypass: {policy from AP — e.g., SuperAdmin bypasses permission checks, TenantAdmin does not}. |

<!-- end: AP-sourced -->

---

## Data Protection Rules

<!-- begin: AP-sourced -->

### Encryption

| Rule | Description |
|------|-------------|
| DATA-01 | All data at rest MUST be encrypted using {algorithm from AP — e.g., AES-256}. |
| DATA-02 | All data in transit MUST use {protocol from AP — e.g., TLS 1.3}. No unencrypted communication. |
| DATA-03 | Database connections MUST use SSL/TLS. Reject unencrypted connections. |
| DATA-04 | Sensitive fields ({list from AP — e.g., passwords, SSN, payment info}) MUST be encrypted at application level (not just DB-level encryption). |
| DATA-05 | Encryption keys: {management from AP — e.g., stored in vault, rotated every 90 days, never in code}. |

### Secrets Management

| Rule | Description |
|------|-------------|
| DATA-06 | Secrets (API keys, DB credentials, tokens) MUST NEVER appear in source code, config files, or logs. |
| DATA-07 | Secret access pattern: {from AP — e.g., environment variables injected at runtime, read from vault}. |
| DATA-08 | Secret rotation: {policy from AP — e.g., rotate all service credentials every 90 days}. |
| DATA-09 | Local development: use `.env` files (gitignored). Production: use {secret store from AP}. |

### Password Storage

| Rule | Description |
|------|-------------|
| DATA-10 | Passwords MUST be hashed using {algorithm from AP — e.g., bcrypt with cost factor 12 / Argon2id}. |
| DATA-11 | NEVER store plaintext passwords. NEVER use reversible encryption for passwords. |
| DATA-12 | NEVER log passwords, tokens, or secrets — even in debug mode. |

<!-- end: AP-sourced -->

---

## Input Validation & API Security

<!-- begin: AP-sourced -->

| Rule | Description |
|------|-------------|
| SEC-01 | ALL user input MUST be validated — type, length, format, range. No unvalidated input reaches business logic. |
| SEC-02 | Use parameterized queries for ALL database operations. NEVER concatenate user input into queries. |
| SEC-03 | Output encoding: all user-provided content rendered in UI MUST be escaped (XSS prevention). |
| SEC-04 | Rate limiting: {policy from AP — e.g., 100 req/min per user, 1000 req/min per tenant, 10 req/min for login}. |
| SEC-05 | Request size limits: {from AP — e.g., max 1MB body, max 100 items in bulk operations}. |
| SEC-06 | CORS: {policy from AP — e.g., whitelist only known frontend origins, no wildcard in production}. |
| SEC-07 | HTTP security headers MUST be set: {list from AP or standard set — HSTS, X-Content-Type-Options, X-Frame-Options, CSP}. |
| SEC-08 | File uploads: {policy from AP — e.g., validate MIME type, scan for malware, limit size, store outside webroot}. |
| SEC-09 | NEVER expose stack traces, internal errors, or system information in API responses. Use generic error messages externally. |
| SEC-10 | API keys: {policy from AP — e.g., prefix with environment, log usage, expire after 1 year}. |

<!-- end: AP-sourced -->

---

## Audit & Logging

<!-- begin: AP-sourced -->

| Rule | Description |
|------|-------------|
| AUDIT-01 | Log ALL authentication events: login success, login failure, logout, token refresh, password change. |
| AUDIT-02 | Log ALL authorization failures: permission denied events with user, resource, and action. |
| AUDIT-03 | Log ALL data mutations on sensitive entities: {list from AP — e.g., user accounts, roles, permissions, security config}. |
| AUDIT-04 | Audit log format: {from AP or standard — e.g., timestamp, user_id, tenant_id, action, resource, outcome, IP}. |
| AUDIT-05 | Audit logs MUST be immutable — append-only, no modification or deletion. |
| AUDIT-06 | Audit log retention: {from AP — e.g., minimum 2 years, comply with {regulation}}. |

<!-- end: AP-sourced -->

---

## Tenant Isolation (If Multi-Tenant)

<!-- begin: AP-sourced -->

{Include ONLY if Multi-Tenancy Architecture exists in AP}

| Rule | Description |
|------|-------------|
| TENANT-01 | Every authenticated request MUST carry tenant context — propagated via {mechanism from AP — e.g., middleware extracting from JWT}. |
| TENANT-02 | Every database query MUST be scoped to the active tenant. NEVER query across tenants (except platform admin functions). |
| TENANT-03 | Tenant ID MUST be validated on every request — reject if missing or mismatched. |
| TENANT-04 | Cross-tenant data access: {policy from AP — e.g., strictly forbidden / platform admin only}. |
| TENANT-05 | Tenant data deletion: {policy from AP — e.g., soft-delete with 30-day grace period, then hard-delete}. |

NOTE: Full tenant isolation rules are in `rules/multi-tenancy.md`. These rules cover the SECURITY aspect only.

<!-- end: AP-sourced -->

---

## Security Review Checklist (For PRs)

Every PR touching authentication, authorization, or data handling MUST verify:

- [ ] No secrets in code or config (DATA-06)
- [ ] Input validated at boundary (SEC-01)
- [ ] Parameterized queries used (SEC-02)
- [ ] Authorization checked at correct layer (AUTHZ-05)
- [ ] Tenant scoping applied (TENANT-02) — if multi-tenant
- [ ] Audit logging for security events (AUDIT-01 through AUDIT-03)
- [ ] No sensitive data in logs (DATA-12)
- [ ] Error responses don't leak internals (SEC-09)

---

## Anti-Patterns (NEVER DO)

1. **NEVER** disable authentication "temporarily" — not even for testing in shared environments
2. **NEVER** implement custom cryptography — use library implementations only
3. **NEVER** store tokens in localStorage (XSS vulnerable)
4. **NEVER** trust client-side authorization checks — always verify server-side
5. **NEVER** use GET requests for state-changing operations (CSRF risk)
6. **NEVER** log request bodies that may contain credentials
7. **NEVER** hardcode credentials, even for development
8. **NEVER** skip input validation because "it's an internal API"
9. **NEVER** return different error messages for "user not found" vs. "wrong password" (user enumeration)
10. **NEVER** implement "remember me" without understanding the security implications
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Authentication methods list | Convert to AUTH-NN numbered rules | Authentication section |
| Token strategy (type, expiry, rotation) | Convert to specific AUTH rules with values | Token Handling |
| RBAC model (roles, hierarchy, permissions) | Convert to AUTHZ-NN rules with specifics | Authorization section |
| Encryption decisions (algorithm, scope) | Convert to DATA-NN rules | Data Protection |
| OWASP mitigation list | Convert to SEC-NN rules | Input Validation section |
| Audit logging strategy | Convert to AUDIT-NN rules with format | Audit section |
| Tenant isolation security aspects | Convert to TENANT-NN rules | Tenant Isolation section |
| ADR for auth approach | Reference in Security Model Summary | ADR link |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| AUTH-NN | Authentication |
| AUTHZ-NN | Authorization |
| DATA-NN | Data Protection |
| SEC-NN | Input Validation & API Security |
| AUDIT-NN | Audit & Logging |
| TENANT-NN | Tenant Isolation |

---

## Key Rules for This Mapping

1. **Every AP security decision becomes a numbered enforceable rule** — no vague guidance
2. **Values are specific** — "expire after 15 minutes" not "expire after a reasonable time"
3. **OWASP Top 10 coverage is mandatory** — even if AP doesn't list every mitigation, derive standard ones for the selected technology
4. **Tenant isolation is in TWO places** — security aspects here, full isolation rules in `multi-tenancy.md`
5. **Cross-reference observability-sensitive.md** — what never to log (secrets, PII) must be consistent between files
6. **Security rules are the highest-priority enforcement** — AI-GCE derives pre-commit hooks from these
7. **No opinions beyond AP** — if AP says "bcrypt", use bcrypt. Don't substitute Argon2 because you think it's better.

---

## Depth Adaptation

| Depth | security-rules.md |
|-------|-------------------|
| **Minimal** | Security Model Summary + AUTH rules (5-8) + AUTHZ rules (3-5) + DATA rules (4-6) + SEC rules (5-7) | 
| **Standard** | Full structure as defined above — all sections with 8-12 rules per category |
| **Comprehensive** | Full structure + threat model reference + compliance mapping table (rule → regulation) + security architecture diagrams + penetration test scope |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Authentication method added (e.g., SAML) | New AUTH rules | Add rules; signal AI-GCE |
| Token strategy changed | Multiple AUTH rules affected | Update; flag HIGH IMPACT — may require code changes |
| New role added to RBAC | AUTHZ-02 updated | Add to role list; review hierarchy |
| Encryption algorithm changed | DATA-01 or DATA-04 updated | Update; flag for security review |
| Rate limiting policy changed | SEC-04 updated | Update; signal AI-GCE to update hook thresholds |
| New audit requirement | New AUDIT-NN rule | Add; may affect observability-logging.md too |
| Tenant isolation model changed | TENANT rules updated | Flag HIGH IMPACT — cross-reference with multi-tenancy.md |

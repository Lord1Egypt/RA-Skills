<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Security & Identity Architecture

## Stage: 8 of 13
## Phase: 🟡 DECISIONS
## Execution: ALWAYS

---

## Purpose

Define how the system authenticates users, authorizes actions, protects data, and maintains an audit trail. Security architecture is a cross-cutting concern that touches every container and every interaction. Decisions here constrain API design (Stage 10), data architecture (Stage 9), and component design (Stage 12).

**CTO Mindset:** "Security is not a feature you add later. It's a structural property baked into the architecture from the start."

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS stage, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Define trust boundaries first — where does trust change? — then design controls at each crossing
- Classify data explicitly (PII, business-sensitive, public) BEFORE designing protection mechanisms
- Separate authentication (who you are) from authorization (what you're allowed to do) — they're different architectures
- Think about the attacker's path: from entry point to target asset, what's the shortest compromise chain?

### Anti-Patterns for This Stage
- Do NOT treat security as a single "auth service" — it's a cross-cutting concern across every container boundary
- Do NOT skip the threat model — you can't design defenses without knowing what you're defending against

### Quality Check
A good output at this stage sounds like:
- "3 trust boundaries defined; OIDC federation for authn, RBAC + ABAC for authz; data classified per-column; 4 STRIDE threats mitigated; secrets in vault with auto-rotation..."

---

## Depth Adaptation

| Depth | Security Architecture Behavior |
|-------|-------------------------------|
| **Minimal** | Define auth method, RBAC model, encryption approach. Brief threat acknowledgment. 1-2 ADRs for key decisions. |
| **Standard** | Full authentication + authorization architecture. Token strategy. Data protection (at rest + transit). Audit logging. OWASP Top 10 mitigations acknowledged. ADR per major security decision. |
| **Comprehensive** | Detailed threat model (STRIDE or similar). Per-container security analysis. API security deep-dive (rate limiting, input validation, injection prevention). Secrets management architecture. Compliance controls mapping. Security monitoring and incident detection. Multiple ADRs. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Architecture Principles (Stage 3) — security-related principles
2. Constraints (Stage 3) — compliance requirements, encryption mandates
3. Quality Attributes (Stage 3) — security priority level
4. Container list (Stage 5) — what needs protecting
5. Technology stack (Stage 6) — framework security capabilities
6. Multi-tenancy model (Stage 7, if executed) — tenant isolation interactions with security
7. External systems (Stage 4) — identity providers, SIEM, audit targets
8. Requirements (Stage 2) — stated security NFRs (encryption, auth methods, compliance)

---

### Step 2: Define Authentication Architecture

#### 2a: Authentication Methods

Determine which authentication methods the system supports:

```markdown
## Authentication Architecture

### Supported Authentication Methods

| Method | Use Case | Mandatory/Optional | Implementation Approach |
|--------|----------|:------------------:|------------------------|
| Local credentials (email + password) | Default user authentication | {Mandatory/Optional} | {Bcrypt/Argon2 hashing; password policy enforcement} |
| LDAP / Active Directory | Enterprise directory integration | {Mandatory/Optional} | {LDAP bind authentication; group sync} |
| SAML 2.0 | Federated SSO with enterprise IdPs | {Mandatory/Optional} | {SP-initiated; signed assertions} |
| OAuth 2.0 / OIDC | Modern SSO and API authentication | {Mandatory/Optional} | {Authorization code flow; token exchange} |
| MFA (Multi-Factor) | Additional verification layer | {Mandatory/Optional} | {TOTP / SMS / Push — specify which} |
| API Keys | Machine-to-machine / integration auth | {Mandatory/Optional} | {Scoped keys; per-tenant; rate-limited} |
```

**Ask if unclear:**

```markdown
### Q-DCS-02: Authentication Methods

**Context:** Authentication is how we verify identity. The methods we support define integration complexity and user experience.

**Which methods does this system need to support?**
1. Local username/password: {Yes/No}
2. LDAP/Active Directory: {Yes/No}
3. SAML 2.0 SSO: {Yes/No}
4. OAuth 2.0 / OIDC: {Yes/No}
5. MFA: {Yes/No — which factor?}
6. API keys for integrations: {Yes/No}

**Your input:** _[awaiting input]_
```

#### 2b: Token Strategy

```markdown
### Token / Session Strategy

| Aspect | Decision |
|--------|----------|
| **Token type** | {JWT / Opaque session token / Hybrid} |
| **Token lifetime** | Access: {duration}; Refresh: {duration} |
| **Token storage (client)** | {HttpOnly cookie / localStorage / sessionStorage} |
| **Token refresh mechanism** | {Silent refresh / Refresh token rotation / Sliding session} |
| **Token content** | {Claims: user_id, tenant_id, roles, permissions, exp} |
| **Token revocation** | {Blacklist in cache / Short-lived + no revocation / Token version per user} |
| **Stateless vs. stateful** | {Fully stateless JWT / Server-side session store / Hybrid} |
```

**Decision question (if choice is non-obvious):**

```markdown
### Q-DCS-03: Token Strategy

**Context:** Token architecture affects scalability, security, and complexity.

**Options:**
- (a) **Stateless JWT** — Self-contained tokens; no server-side session store needed. Fast validation. Revocation harder.
- (b) **Server-side sessions** — Opaque token references server-stored session. Easy revocation. Requires session store (cache).
- (c) **Hybrid** — Short-lived JWT for API calls + server-side session for portal. Balance of speed and control.

**Recommended:** {option}
**Rationale:** {Reference scale, security requirements, multi-tenancy needs}

→ _ADR-{nnn} if significant trade-off_

**Your Decision:** _[awaiting input]_
```

---

### Step 3: Define Authorization Architecture

#### 3a: Authorization Model

```markdown
## Authorization Architecture

### Model: {RBAC / ABAC / Policy-Based / Hybrid}

| Aspect | Design |
|--------|--------|
| **Model type** | {Role-Based (RBAC) / Attribute-Based (ABAC) / Permission-Based / Policy Engine} |
| **Role hierarchy** | {Flat roles / Hierarchical roles (inherit permissions)} |
| **Permission granularity** | {Coarse: role-level / Fine: permission-per-action / Field-level} |
| **Scope** | {Global / Per-tenant / Per-resource} |
| **Enforcement point** | {API gateway / Middleware / Controller/handler / Service layer} |
```

#### 3b: Role Structure (if RBAC)

```markdown
### Role Architecture

| Role Category | Examples | Permission Scope |
|--------------|---------|:----------------:|
| Platform-level roles | Platform Admin, Super Admin | Cross-tenant; full system |
| Tenant-level roles | Tenant Admin, Manager, Agent, User | Within one tenant |
| Functional roles | Report Viewer, Approver, Auditor | Specific capability |

### Permission Model

| Permission | Format | Example |
|-----------|--------|---------|
| Resource-Action | `{resource}:{action}` | `tickets:create`, `users:delete`, `reports:export` |
| Resource-Action-Scope | `{resource}:{action}:{scope}` | `tickets:read:own`, `tickets:read:team`, `tickets:read:all` |
```

#### 3c: Enforcement Layers

```markdown
### Authorization Enforcement

| Layer | What It Checks | How |
|-------|---------------|-----|
| **API Gateway / Route** | Is this endpoint accessible to this role? | Route-level guards / middleware |
| **Service / Business Logic** | Is this specific action allowed for this user on this resource? | Permission checks in service methods |
| **Data Layer** | Is this user allowed to see/modify this specific record? | Query scoping; row-level filters |
| **Field Level** (if needed) | Can this user see this specific field? | Response filtering / projection |
```

---

### Step 4: Define Data Protection

```markdown
## Data Protection

### Encryption at Rest

| Data Type | Location | Encryption Method | Key Management |
|-----------|----------|:-----------------:|:--------------:|
| Database | {Primary DB} | {AES-256 / TDE / Filesystem encryption} | {Key rotation policy; where keys stored} |
| File attachments | {Storage location} | {AES-256 / Storage-level encryption} | {Same or separate key management} |
| Cache | {Cache engine} | {Encrypted / Not encrypted — justify} | {If encrypted — method} |
| Backups | {Backup location} | {Encrypted at rest} | {Key escrow for DR} |

### Encryption in Transit

| Communication Path | Protocol | Minimum Version | Certificate Management |
|-------------------|----------|:---------------:|:----------------------:|
| Client → Load Balancer | TLS | {1.2 / 1.3} | {CA-signed; auto-renewal or manual} |
| Load Balancer → Application | {TLS / Plain (internal network)} | {version} | {Internal CA / self-signed} |
| Application → Database | {TLS / Unix socket} | {version} | {How managed} |
| Application → Cache | {TLS / Plain (internal)} | {version} | {How managed} |
| Application → External Systems | TLS | {1.2+} | {Per-integration} |

### Secrets Management

| Secret Type | Storage Location | Access Method | Rotation |
|-------------|-----------------|:-------------:|:--------:|
| Database credentials | {Vault / env vars / secrets file} | {Injected at deploy / runtime API} | {Frequency} |
| API keys (outbound) | {Vault / config} | {Injected} | {Policy} |
| Encryption keys | {HSM / Vault / filesystem} | {API / file} | {Annual / triggered} |
| JWT signing key | {Vault / env} | {Application startup} | {Policy} |
```

---

### Step 5: Define Audit & Compliance

```markdown
## Audit Architecture

### What Is Audited

| Event Category | Examples | Retention | Storage |
|---------------|---------|:---------:|---------|
| Authentication events | Login, logout, failed login, MFA challenge | {period} | {where} |
| Authorization failures | Access denied, privilege escalation attempt | {period} | {where} |
| Data mutations | Create, update, delete on business entities | {period} | {where} |
| Configuration changes | Role changes, permission grants, tenant config | {period} | {where} |
| Administrative actions | User management, tenant provisioning | {period} | {where} |
| Cross-tenant access | Platform admin accessing tenant data | {period} | {where} |

### Audit Record Structure

| Field | Description |
|-------|-------------|
| timestamp | ISO 8601 with timezone |
| actor_id | Internal user ID (real identity) |
| actor_display | Displayed identity (may be masked) |
| tenant_id | Tenant context (or "platform" for cross-tenant) |
| action | What was done (verb) |
| resource_type | What type of entity was affected |
| resource_id | Specific entity ID |
| result | Success / Failure / Denied |
| ip_address | Client IP |
| details | Additional context (changes made, reason) |

### Audit Integrity

| Concern | Approach |
|---------|----------|
| Tamper resistance | {Append-only store / Write-once / Hash chaining} |
| Access control | {Separate from business data; restricted read access} |
| Export | {SIEM integration via syslog/API; compliance report generation} |
```

---

### Step 6: Address Threat Mitigations

```markdown
## Security Threat Mitigations

### OWASP Top 10 Coverage

| # | Threat | Mitigation Approach |
|---|--------|-------------------|
| A01 | Broken Access Control | {RBAC enforcement; principle of least privilege; tenant isolation; automated tests} |
| A02 | Cryptographic Failures | {TLS 1.2+; AES-256 at rest; no custom crypto; key rotation} |
| A03 | Injection | {Parameterized queries; ORM-only DB access; input validation; prepared statements} |
| A04 | Insecure Design | {Threat modeling; security principles from Stage 3; security reviews at gates} |
| A05 | Security Misconfiguration | {Hardened defaults; no debug in production; automated security scanning} |
| A06 | Vulnerable Components | {Dependency scanning; automated updates; pinned versions; SBOM} |
| A07 | Auth Failures | {MFA; account lockout; secure password storage; session management} |
| A08 | Data Integrity Failures | {Signed deployments; integrity checks; secure CI/CD pipeline} |
| A09 | Logging & Monitoring Failures | {Comprehensive audit logging; alerting on suspicious patterns; SIEM integration} |
| A10 | SSRF | {Allowlist outbound connections; no user-controlled URLs in server requests} |

### API-Specific Security

| Concern | Mitigation |
|---------|-----------|
| Rate limiting | {Per-tenant, per-user, per-endpoint limits} |
| Input validation | {Schema validation on all inputs; reject unexpected fields} |
| Response filtering | {Never expose internal IDs, stack traces, or system metadata} |
| CORS | {Strict origin allowlist; no wildcard in production} |
| CSRF | {Token-based protection for cookie-authenticated endpoints} |
| Content-Type enforcement | {Reject unexpected content types} |
```

---

### Step 7: Produce ADR(s)

Key security ADRs:

| ADR | Decision |
|-----|----------|
| ADR-{nnn} | Authentication token strategy (JWT vs. session vs. hybrid) |
| ADR-{nnn} | Authorization model (RBAC vs. ABAC vs. policy engine) |
| ADR-{nnn} | Secrets management approach |

Only produce ADRs where genuine alternatives were evaluated.

---

### Step 8: Assemble Document

Compile **Security & Identity Architecture** document:

1. Authentication Architecture (methods, token strategy, SSO)
2. Authorization Architecture (model, roles, enforcement layers)
3. Data Protection (encryption at rest, in transit, secrets)
4. Audit & Compliance (what's logged, structure, integrity, export)
5. Threat Mitigations (OWASP Top 10, API security)
6. ADR references

---

### Step 9: Present for Review

```markdown
## Review: Security & Identity Architecture — {system_name}

I've designed the security architecture.

**Key decisions:**
- **Authentication:** {n} methods supported; token strategy: {type}
- **Authorization:** {model} with {granularity} permissions
- **Encryption:** {at-rest method}; TLS {version}+ in transit
- **Audit:** {scope summary}; {retention period}
- **OWASP:** All Top 10 addressed

**Security layers:**
- Auth methods: {list}
- Enforcement: {n} layers (gateway → service → data)
- Audit: {event categories covered}

**ADRs produced:** {n}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Security architecture is sufficient; proceed to Design phase
- (b) **Strengthen** — Need more protection in {area}
- (c) **Simplify** — Over-engineered for our threat model
- (d) **Add compliance** — Missing regulatory requirement
- (e) **Challenge auth model** — Different approach needed
```

---

### Step 10: Log and Transition

1. Update state: Stage 8 = ✅ Done; Current Phase = DESIGN; Current Stage = 9
2. Update ADR register
3. Update Architecture Workbook

Display:

```
✅ Stage 8: Security & Identity Architecture — Complete

🔐 Auth: {n} methods | Authz: {model} | Encryption: {standard}
📄 Saved to: {file_path}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DECISIONS PHASE COMPLETE (Stages 6-8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Technology selected. Isolation defined. Security locked.
Now we detail the internal design.

Next → DESIGN PHASE
Stage 9: Data Architecture & Schema

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/06_Security_Identity_Architecture.md`
- Phase folders: `{output_root}/decisions/Security_Identity_Architecture.md`

---

## Security Architecture Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Authentication complete | All user types have a defined auth path |
| Authorization enforced | Every API endpoint has access control defined |
| Defense in depth | Authorization at ≥2 layers (not just route-level) |
| Encryption comprehensive | Data protected at rest AND in transit |
| Secrets managed | No hardcoded credentials; rotation policy defined |
| Audit sufficient | All state-changing operations auditable |
| OWASP addressed | All Top 10 have stated mitigation |
| Tenant-aware (if multi-tenant) | Security model respects tenant boundaries |
| Constraint-compliant | Meets stated compliance/regulatory requirements |
| Principle-aligned | Follows security principles from Stage 3 |

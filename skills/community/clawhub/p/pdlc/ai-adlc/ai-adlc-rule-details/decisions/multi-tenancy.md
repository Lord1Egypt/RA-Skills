<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Multi-Tenancy & Data Isolation Strategy

## Stage: 7 of 13
## Phase: 🟡 DECISIONS
## Execution: CONDITIONAL

---

## Trigger Conditions

**Execute IF:**
- System serves multiple tenants/customers/organizations from a single deployment
- Requirements mention: multi-tenant, white-label, customer isolation, data segregation, organization separation
- Q-FND-02 answer was option (a) "Multi-tenant"

**Skip IF:**
- Single-tenant system (one deployment per customer)
- No organization-level data separation needed
- Q-FND-02 answer was (b), (c), or (d) AND no isolation requirement emerged

**If skipped:** Log in state: "Stage 7 skipped — single-tenant system. No isolation architecture needed."

---

## Purpose

Define how the system achieves tenant isolation — the foundational architectural pattern that ensures one tenant's data, configuration, and experience is completely separated from another's. This decision affects EVERY layer: database, application, cache, storage, API, UI, and background processing.

**CTO Mindset:** "Multi-tenancy is the hardest cross-cutting concern. If I get this wrong, it contaminates every module. If I get it right, it's invisible to developers."

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS stage, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in isolation levels — data, compute, network — and define the isolation boundary per level
- Classify data by sensitivity: which tenant data must NEVER be visible to another tenant, even accidentally?
- Design for the "noisy neighbour" problem — one tenant's load must not affect another's performance
- Consider regulatory implications of shared infrastructure (data residency, compliance auditing)

### Anti-Patterns for This Stage
- Do NOT assume "shared database with tenant_id column" is adequate isolation without analyzing the attack surface
- Do NOT design isolation at one layer (e.g., app) while ignoring others (cache, search, queues)

### Quality Check
A good output at this stage sounds like:
- "Isolation pattern: schema-per-tenant for data, shared compute with tenant-scoped auth context, queue-per-tenant for async; trade-off: cost vs. isolation documented in ADR..."

---

## Depth Adaptation

| Depth | Multi-Tenancy Behavior |
|-------|----------------------|
| **Minimal** | Select isolation model (row-level vs. schema vs. DB). Define tenant context propagation. Brief lifecycle description. Single ADR. |
| **Standard** | Full isolation model with enforcement mechanisms per layer. Tenant lifecycle (provisioning, config, deactivation). Cross-tenant scenarios addressed. ADR with 3+ options compared. |
| **Comprehensive** | Deep isolation analysis with per-layer enforcement details. Tenant provisioning automation design. Performance isolation (noisy neighbor prevention). Compliance implications per model. Data deletion/GDPR considerations. Multiple ADRs for complex decisions. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Scale targets (Stage 2) — number of tenants, users per tenant, growth rate
2. Constraints (Stage 3) — data residency, compliance, isolation strength required
3. Principles (Stage 3) — any tenancy-related principles
4. Container list (Stage 5) — what containers need tenant awareness
5. Technology stack (Stage 6) — database, cache, framework selected

---

### Step 2: Determine Isolation Model

This is the most impactful multi-tenancy decision:

```markdown
### Q-DCS-01: Data Isolation Model

**Context:** How tenant data is physically separated in the database determines complexity, performance, onboarding speed, and isolation strength.

**Decision Drivers:**
- Number of tenants: {n} now, {growth} expected
- Data residency requirements: {any per-tenant data location needs?}
- Isolation strength: {regulatory mandate vs. best-practice preference}
- Operational complexity tolerance: {team size and maturity}
- Tenant onboarding speed: {minutes vs. hours vs. days}

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **(a) Shared database, row-level isolation** | Single DB, single schema. Every table has `tenant_id`. Queries always filtered. | Simplest ops; cheapest; fastest onboarding (config only); easy cross-tenant reporting | Weakest isolation (app bug = data leak); noisy neighbor on queries; single DB = single point of failure |
| **(b) Shared database, schema-per-tenant** | Single DB instance, separate schema per tenant. Application routes to correct schema. | Stronger isolation (schema boundary); per-tenant backup/restore possible; moderate ops | More complex migrations (N schemas); connection pooling harder; onboarding = schema creation |
| **(c) Database-per-tenant** | Separate database instance per tenant. Complete physical isolation. | Strongest isolation; per-tenant performance tuning; per-tenant backup trivial; compliance friendly | Highest ops cost (N databases); connection management complex; cross-tenant reporting hard; slow onboarding |
| **(d) Hybrid** | Row-level for most tenants + dedicated DB for high-value/regulated tenants that require it. | Flexibility; default is simple; premium isolation available | Two code paths; operational complexity; routing logic |

**Recommended:** {Based on tenant count, team size, and constraint strength}

**Rationale:** {Detailed reasoning — reference scale targets, team capability, compliance needs}

→ _This decision generates ADR-{nnn}_

**Your Decision:** _[awaiting input]_
```

---

### Step 3: Define Tenant Context Propagation

How does every operation know which tenant it belongs to?

```markdown
## Tenant Context Propagation

### Resolution (How tenant is identified per request)

| Entry Point | Resolution Method |
|-------------|------------------|
| Web portal (browser) | {Domain-based / URL path / Subdomain / Session/token claim} |
| API (authenticated) | {JWT tenant claim / API key → tenant lookup / Header injection} |
| Background jobs | {Job payload carries tenant_id / Worker context from queue message} |
| Event processing | {Event envelope includes tenant_id} |
| Scheduled tasks | {Iterate all tenants / Tenant-specific schedules} |
| Internal service calls | {Context propagated via header / Parameter passing} |

### Enforcement (How isolation is guaranteed)

| Layer | Enforcement Mechanism |
|-------|---------------------|
| **Middleware/Interceptor** | Every request passes through tenant resolution middleware. Rejects if no tenant context. |
| **ORM/Query layer** | All queries automatically scoped to current tenant (global filter / base repository) |
| **Database (safety net)** | {Row-Level Security policies / Schema routing / DB connection per tenant} |
| **Cache** | Cache keys prefixed with tenant_id (no cross-tenant cache hits) |
| **File storage** | Tenant-scoped paths/buckets (no shared directories) |
| **Search index** | {Tenant filter on all queries / Separate index per tenant} |
| **Background jobs** | Job payload includes tenant_id; worker restores context before execution |

### Principle: Defense in Depth

Isolation is enforced at MULTIPLE layers. If one layer fails, another catches it:

```
Request → [Middleware: resolve tenant] → [ORM: scope queries] → [DB: RLS policy]
                                              ↓
                                    [Cache: tenant-prefixed keys]
                                              ↓
                                    [Storage: tenant-scoped paths]
```

No single layer failure can cause cross-tenant data exposure.
```

---

### Step 4: Define Tenant Lifecycle

```markdown
## Tenant Lifecycle

### Provisioning (Creating a New Tenant)

| Step | Action | Automated? |
|:----:|--------|:----------:|
| 1 | {Create tenant record in tenants table} | Yes |
| 2 | {Generate tenant-specific configuration (defaults)} | Yes |
| 3 | {Create admin user for tenant} | Yes |
| 4 | {Set up branding defaults} | Yes |
| 5 | {Configure DNS/domain (if custom domain)} | {Manual / Semi-auto} |
| 6 | {Create storage path/bucket} | Yes |
| 7 | {Seed initial data (categories, templates)} | Yes |
| 8 | {Verify isolation (automated test)} | Yes |

**Target onboarding time:** {minutes / hours / days} — from decision to first login

### Configuration (Per-Tenant Settings)

| Configuration Area | Scope | Who Manages |
|-------------------|-------|-------------|
| {Branding — logo, colors, domain} | Per-tenant | {Tenant admin / Platform admin} |
| {Feature flags — enabled modules} | Per-tenant | Platform admin |
| {Business rules — workflows, escalations} | Per-tenant | {Configurable by whom} |
| {Integration credentials — SMTP, LDAP} | Per-tenant | {Tenant admin / Platform admin} |
| {Capacity limits — users, storage} | Per-tenant | Platform admin |

### Deactivation & Deletion

| Action | Behavior | Data Retention |
|--------|----------|:-------------:|
| Suspend | Tenant users cannot log in; data preserved; can reactivate | Indefinite |
| Deactivate | All access removed; data in read-only archive | {Policy — e.g., 90 days} |
| Delete | All tenant data permanently removed | Irreversible |

**Data deletion considerations:**
- Cascade scope: what tables/storage/cache entries are affected
- Audit trail: do we retain anonymized audit logs post-deletion?
- Regulatory: any retention requirements that override deletion request?
```

---

### Step 5: Address Cross-Tenant Scenarios

If the system has any roles that operate ACROSS tenant boundaries:

```markdown
## Cross-Tenant Access

| Role | What They See | How It Works |
|------|-------------|-------------|
| Platform Administrator | All tenants — full access | Elevated context; bypass tenant filter; fully audited |
| {Shared agent/operator} | Multiple assigned tenants | Tenant assignment list; context switch per action |
| Reporting / Analytics | Aggregate metrics across tenants | Separate query path; aggregated data only (no PII) |
| System background jobs | All tenants (batch operations) | Iterates tenants; restores context per tenant per operation |

### Cross-Tenant Safety Rules

1. Cross-tenant access is NEVER default — it requires explicit elevation
2. All cross-tenant operations are audit-logged with elevated-access flag
3. No API endpoint returns data from multiple tenants in one response (except platform-admin APIs)
4. Tenant context cannot be spoofed via client-side manipulation
```

---

### Step 6: White-Label / Branding Architecture (if applicable)

If the system is white-labeled:

```markdown
## White-Label Architecture

### Branding Resolution

| Touchpoint | What's Branded | Resolution Method |
|-----------|---------------|-------------------|
| Portal URL | Custom domain per tenant | {DNS + reverse proxy routing} |
| Visual identity | Logo, colors, fonts | {Tenant config → CSS custom properties / theme object} |
| Email sender | From address, reply-to, DKIM signing | {Per-tenant SMTP config + domain verification} |
| Document exports | Headers, footers, watermarks | {Tenant branding applied at render time} |
| API responses | Whitelisting (no platform identity in responses) | {Response transformation or inherent design} |

### Identity Concealment

| Concern | How Addressed |
|---------|--------------|
| Provider identity not visible to tenants | {No platform branding in any tenant-facing surface} |
| Agent identity masking | {Display names configurable per-tenant; real identity internal only} |
| Audit trail dual-identity | {Both real and masked identity stored; visibility by role} |
```

---

### Step 7: Produce ADR(s)

Key multi-tenancy ADRs:

| ADR | Decision |
|-----|----------|
| ADR-{nnn} | Data isolation model (row-level / schema / database / hybrid) |
| ADR-{nnn} | Tenant context propagation mechanism |
| ADR-{nnn} | White-label domain routing (if applicable) |

Produce using template `templates/adr-template.md`.

---

### Step 8: Assemble Document

Compile the **Multi-Tenancy Architecture** document:

1. Isolation Model (decision + rationale)
2. Tenant Context Propagation (resolution + enforcement per layer)
3. Tenant Lifecycle (provisioning, configuration, deactivation)
4. Cross-Tenant Access (if applicable)
5. White-Label Architecture (if applicable)
6. Defense-in-Depth Diagram
7. ADR references

---

### Step 9: Present for Review

```markdown
## Review: Multi-Tenancy Architecture — {system_name}

I've designed the multi-tenancy isolation strategy.

**Key decisions:**
- **Isolation model:** {chosen model}
- **Context resolution:** {primary method — e.g., "JWT tenant claim + middleware enforcement"}
- **Enforcement layers:** {n} layers (middleware → ORM → DB → cache → storage)
- **Onboarding time:** {target}
- **Cross-tenant roles:** {n} defined

**White-label:** {Yes — domain-based branding / No — not applicable}

**ADRs produced:** {n}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Isolation strategy is sound; proceed to Security
- (b) **Strengthen isolation** — Need more protection at {layer}
- (c) **Simplify** — Over-engineered for our needs
- (d) **Challenge model** — Different isolation model preferred
- (e) **Add scenarios** — Missing cross-tenant use case
```

---

### Step 10: Log and Transition

1. Update state: Stage 7 = ✅ Done; Current Stage = 8
2. Update ADR register
3. Update Architecture Workbook

Display:

```
✅ Stage 7: Multi-Tenancy & Data Isolation — Complete

🔒 Model: {isolation model} | Layers: {n} enforcement points
📄 Saved to: {file_path}

Next → Stage 8: Security & Identity Architecture

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/05_MultiTenancy_Architecture.md`
- Phase folders: `{output_root}/decisions/MultiTenancy_Architecture.md`

---

## Multi-Tenancy Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Defense in depth | Isolation enforced at ≥2 layers (not just application code) |
| No default cross-tenant | Cross-tenant access requires explicit elevation |
| Context mandatory | No code path can execute without resolved tenant context |
| Lifecycle complete | Provisioning through deletion defined |
| Performance considered | Isolation mechanism doesn't create untenable performance overhead |
| Onboarding practical | New tenant setup time is acceptable for business needs |
| Audit trail | All cross-tenant access logged and auditable |
| Principle compliant | Aligns with architecture principles (especially isolation-related ones) |

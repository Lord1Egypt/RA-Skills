<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Feature Flags & Progressive Delivery

**Extension ID:** feature-flags
**Version:** 1.1.0
**Rule Prefix:** FF
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 6 (Technology Stack) / Stage 12 (Component Design)
- **Secondary Stages:** Stage 10 (Infrastructure & Deployment), Stage 5 (Container Design)

These rules apply to the architectural design of feature flag evaluation, lifecycle management, and progressive delivery mechanisms.

---

## MANDATORY: Extension Sub-Role — Release Engineer (Progressive Delivery Specialist)

When this extension is active, ALSO adopt the mindset of a **Release Engineer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of feature flag rule enforcement.

### Behavioral Shifts
- Decouple deployment from release — code deploying to production ≠ feature being visible to users; flags are the control layer
- Classify every flag by type (release/experiment/operational/permission) — each has different lifecycle and cleanup urgency
- Plan flag removal from day one — every release flag gets a planned removal date at creation
- Design for flag-service failure — what happens if the flag evaluator is unavailable? Define safe defaults

### Anti-Patterns for This Extension
- Do NOT use flags as permanent configuration with no cleanup plan — that's config, not progressive delivery
- Do NOT evaluate flags via synchronous remote call per-request without caching — it's a latency and SPOF risk

### Quality Check
A good output with this extension sounds like:
- "Flag architecture: server-side eval with 30s local cache; 4 flag types defined; release flags: max 6-week lifecycle, auto-JIRA on expiry; kill switch: <60s disable without deploy..."

---

## Rules

### Rule FF-01: Flag Architecture Definition

**Statement:** The system must define where feature flags are stored, how they are evaluated, and how flag state reaches the runtime. Flag evaluation must not add unacceptable latency to the request path.

**Verification:**
- [ ] Flag storage location is defined (dedicated service, configuration store, etc.)
- [ ] Evaluation mechanism is defined (server-side, client-side, or edge)
- [ ] Latency impact of flag evaluation is measured and acceptable (< target ms per evaluation)
- [ ] Caching strategy is defined (local cache TTL, eventual consistency accepted)
- [ ] Flag evaluation is resilient (system works if flag service is temporarily unavailable)
- [ ] Default behavior is defined for all flags when evaluation fails (fail-open or fail-closed)

**Anti-Pattern:** Evaluating flags via synchronous remote call on every request without caching, adding unacceptable latency and creating a single point of failure.

**ADR Trigger:** Yes — When deciding on the flag evaluation architecture (server-side vs. client-side vs. edge, caching model).

---

### Rule FF-02: Flag Type Classification

**Statement:** Every feature flag must be classified by type: release flag, experiment flag, operational flag, or permission flag. Each type has different lifecycle expectations, ownership, and cleanup urgency.

**Verification:**
- [ ] Flag types are defined with clear criteria for each:
  - Release flags: temporary, removed after full rollout
  - Experiment flags: time-bound, removed after experiment concludes
  - Operational flags: long-lived, used as kill switches or performance tuning
  - Permission flags: long-lived, gate features per tenant/plan
- [ ] Every flag has an assigned type at creation
- [ ] Lifecycle expectations differ by type (release flags = weeks; ops flags = permanent)
- [ ] Cleanup urgency is defined per type

**Anti-Pattern:** Treating all flags the same — release flags that were supposed to be temporary becoming permanent because nobody distinguishes them from intentionally long-lived permission flags.

**ADR Trigger:** No

---

### Rule FF-03: Flag Lifecycle Management

**Statement:** Every feature flag must have a defined lifecycle: creation → rollout → full-on → cleanup/removal. Stale flags (past their expected lifecycle) must be detected and actioned.

**Verification:**
- [ ] Flag lifecycle stages are documented (creation, gradual rollout, full-on, removal)
- [ ] Expected lifetime is declared at flag creation (expiry date or rollout milestone)
- [ ] Stale flag detection mechanism exists (automated scan for flags past expiry)
- [ ] Flag removal process is defined (code path cleanup, configuration removal)
- [ ] Stale flag report is generated periodically (visibility into tech debt)
- [ ] Owner is assigned to every flag (responsible for cleanup)

**Anti-Pattern:** Flags accumulating indefinitely with no cleanup process, creating layers of dead conditional logic that nobody dares remove ("flag graveyard").

**ADR Trigger:** Yes — When defining the flag lifecycle governance process and stale flag cleanup policy.

---

### Rule FF-04: Targeting and Evaluation Rules

**Statement:** Flag evaluation must support targeting rules: percentage rollout, user segment targeting, tenant-based targeting, and environment-specific overrides. Targeting rules must be configurable without code deployment.

**Verification:**
- [ ] Percentage-based rollout is supported (e.g., 10% of users)
- [ ] User/tenant segment targeting is supported (e.g., beta users, enterprise tier)
- [ ] Environment overrides are supported (flag on in staging, off in production)
- [ ] Targeting rules can be changed without deploying code
- [ ] Targeting is deterministic (same user gets same result for same flag consistently)
- [ ] Targeting context is defined (what attributes are available for evaluation)

**Anti-Pattern:** Flags that can only be fully on or fully off, with no gradual rollout capability, forcing big-bang releases and removing the safety net.

**ADR Trigger:** No

---

### Rule FF-05: Flag Governance and Approval

**Statement:** Flag creation and rollout changes must have defined governance: who can create flags, who can change rollout percentage in production, and what approval process applies.

**Verification:**
- [ ] Flag creation requires documented purpose, type, owner, and expected lifetime
- [ ] Production rollout changes require appropriate approval (defined per flag risk level)
- [ ] Audit trail exists for all flag state changes (who changed what, when)
- [ ] Emergency kill switch toggling is possible without standard approval (break-glass process)
- [ ] Flag access control is defined (who can modify which flags)
- [ ] Change history is visible and auditable

**Anti-Pattern:** Anyone can toggle any flag in production without oversight, leading to untracked changes that cause incidents with no audit trail.

**ADR Trigger:** No

---

### Rule FF-06: Multi-Tenant Flag Scoping

**Statement:** In multi-tenant systems, flags must support per-tenant evaluation. Tenant-based flag scoping enables feature tiering, early access programs, and tenant-specific rollouts.

**Verification:**
- [ ] Flags can be targeted per tenant (tenant ID as evaluation context)
- [ ] Feature tiering is expressible through flags (basic tier vs. premium tier features)
- [ ] Per-tenant overrides are possible (enable for one tenant, disable for another)
- [ ] Tenant-scoped flags respect tenant isolation (no cross-tenant flag leakage)
- [ ] Default behavior for tenants not in any targeting rule is defined

**Anti-Pattern:** Global-only flags in a multi-tenant system, unable to progressively roll out to specific tenants or differentiate feature access by tenant tier.

**ADR Trigger:** Yes — When defining the multi-tenant flag scoping model (per-tenant, per-tier, per-region, etc.).

---

### Rule FF-07: Flag-Aware Testing Strategy

**Statement:** The testing strategy must account for feature flags. Tests must validate behavior for both flag-on and flag-off states. Critical paths must be tested with all realistic flag combinations.

**Verification:**
- [ ] Unit tests cover both flag states (on and off) for all flagged behavior
- [ ] Integration tests validate feature behavior with flags in expected production states
- [ ] Flag combinations that interact are identified and tested together
- [ ] Test environments can set flag state explicitly (not dependent on production config)
- [ ] Test coverage report identifies untested flag paths
- [ ] Flag removal is validated by tests (ensure code works without the flag)

**Anti-Pattern:** Testing only with flags on (or only off), leading to production issues when flag state differs from test state or when flags are toggled.

**ADR Trigger:** No

---

### Rule FF-08: Performance Impact Guardrails

**Statement:** Feature flag evaluation must not degrade system performance beyond defined thresholds. Flag evaluation frequency, caching, and hot-path optimization must be designed explicitly.

**Verification:**
- [ ] Flag evaluation latency is measured (P50, P95, P99)
- [ ] Maximum acceptable evaluation latency is defined
- [ ] Hot-path flag evaluations are cached locally (not remote call per evaluation)
- [ ] Flag count is monitored (total active flags as complexity metric)
- [ ] Bulk evaluation is supported (evaluate multiple flags in single call)
- [ ] Performance impact is tested under load (flag evaluation at scale)

**Anti-Pattern:** Evaluating hundreds of flags via remote call on every request in a hot path, adding tens of milliseconds of latency and creating flag service as a bottleneck.

**ADR Trigger:** No

---

### Rule FF-09: Flag Removal Code Path Simplification

**Statement:** When a flag is fully rolled out (permanently on), the flag and its conditional logic must be removed from the codebase. The "flag off" code path must be deleted. This is mandatory, not optional cleanup.

**Verification:**
- [ ] Flag removal is tracked as a required follow-up task after full rollout
- [ ] Removal includes: deleting the flag definition, removing conditional checks, deleting dead code path
- [ ] Automated tooling or lint rules detect flag references that should be removed
- [ ] No flag remains in "permanently on" state for longer than the defined grace period
- [ ] Code review process flags stale flag usage
- [ ] Removal does not require a feature flag itself (clean delete)

**Anti-Pattern:** Flags that are permanently on but never removed from code, creating layers of conditional logic that increase complexity, confuse new developers, and hide dead code paths.

**ADR Trigger:** No

---

### Rule FF-10: Kill Switch for Critical Features

**Statement:** Every critical feature deployed behind a flag must have a kill switch capability — the ability to disable the feature instantly in production without a deployment, within a defined response time.

**Verification:**
- [ ] Critical features are identified and flagged with kill switch capability
- [ ] Kill switch toggle propagates within defined time (e.g., < 60 seconds)
- [ ] Kill switch requires minimal approval in emergency (break-glass)
- [ ] Kill switch activations are logged and trigger incident workflow
- [ ] Regular testing of kill switch mechanism (ensure it works when needed)
- [ ] Rollback behavior is defined (what state the system returns to when killed)

**Anti-Pattern:** Discovering a feature must be disabled urgently but having no fast mechanism — requiring a code deployment to turn it off, taking 30+ minutes during an active incident.

**ADR Trigger:** No

---

### Rule FF-11: Flag Observability and Analytics

**Statement:** Flag evaluation must be observable: which flags are evaluated, how often, what percentage of traffic sees each variant. This data informs rollout decisions and detects unexpected exposure.

**Verification:**
- [ ] Flag evaluation events are logged (flag name, variant served, context)
- [ ] Dashboard shows current rollout state per flag (% exposed per variant)
- [ ] Unexpected flag evaluation patterns trigger alerts (e.g., flag evaluating more than expected)
- [ ] Experiment flags have analytics integration (measure impact of variants)
- [ ] Flag exposure data is available for debugging (was this user exposed to flag X?)
- [ ] Historical flag evaluation data is retained for troubleshooting

**Anti-Pattern:** Flags deployed with no visibility into actual exposure — unable to answer "how many users saw the new feature?" or "was this user affected by the flag?"

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Feature Flags rules active, verify:

- [ ] Flag architecture is defined (storage, evaluation, caching, resilience)
- [ ] Flag type classification is established (release, experiment, ops, permission)
- [ ] Flag lifecycle management process is documented (creation through cleanup)
- [ ] Targeting rules support gradual rollout, segments, and tenants
- [ ] Governance defines who can create and modify flags in production
- [ ] Multi-tenant flag scoping is designed (if multi-tenant system)
- [ ] Testing strategy covers both flag states
- [ ] Performance impact is measured and within guardrails
- [ ] Flag removal is a mandatory follow-up (not optional cleanup)
- [ ] Kill switches exist for critical features
- [ ] Flag observability provides visibility into evaluation and exposure

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| FF-01 | Deciding flag evaluation architecture (server-side vs. client-side vs. edge) |
| FF-03 | Defining flag lifecycle governance and cleanup policy |
| FF-06 | Defining multi-tenant flag scoping model |

---

## Templates

### Flag Definition Card

```
## Flag: {flag-name}

**Type:** Release / Experiment / Operational / Permission
**Owner:** {Person/Team}
**Created:** {Date}
**Expected Lifetime:** {Date or milestone for removal}
**Purpose:** {Why this flag exists — one sentence}
**Default (off) Behavior:** {What happens when flag is off}
**Enabled (on) Behavior:** {What happens when flag is on}
**Kill Switch:** Yes / No
**Targeting:**
- Percentage: {N%}
- Segments: {List of targeted segments}
- Tenants: {Specific tenants or "all"}
**Cleanup Ticket:** {Reference to removal task}
```

### Flag Lifecycle Tracker

```
| Flag Name | Type | Owner | Created | Target Removal | Current State | Stale? |
|-----------|------|-------|---------|----------------|---------------|--------|
| {name} | {type} | {owner} | {date} | {date} | {off/partial/full} | {Y/N} |
```

### Progressive Rollout Plan

```
## Feature: {Name}
## Flag: {flag-name}

**Rollout Strategy:**
| Stage | Targeting | Duration | Success Criteria | Rollback Trigger |
|-------|-----------|----------|------------------|------------------|
| 1 — Internal | Internal users only | 3 days | No errors, no UX complaints | Error rate > 1% |
| 2 — Canary | 5% of production | 5 days | Error rate < 0.1%, latency unchanged | Error rate > 0.5% |
| 3 — Expansion | 25% → 50% → 75% | 7 days | No degradation in key metrics | Any key metric regression |
| 4 — Full | 100% | Permanent | All success criteria met | N/A |
| 5 — Cleanup | Remove flag | Within 2 weeks | Code paths cleaned | N/A |

**Monitoring During Rollout:** {Key metrics to watch}
**Kill Switch Response Time:** {Max time to disable if needed}
```

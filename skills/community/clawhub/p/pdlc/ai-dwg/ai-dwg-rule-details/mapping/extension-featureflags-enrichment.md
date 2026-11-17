<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Feature Flags Extension Enrichment

## Purpose

When the **Feature Flags** extension was active in AI-ADLC, this mapping forces generation of a new conditional steering file and enriches coding standards with flag usage patterns.

**Trigger:** `adlc-state.md` → Enabled Extensions includes `feature-flags`

---

## MANDATORY: Stage Sub-Role — Release Engineer (Progressive Delivery Specialist)

During THIS activity, ALSO adopt the mindset of a **Release Engineer (Progressive Delivery Specialist)**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Feature flags are TEMPORARY delivery mechanisms — enforce lifecycle with expiration dates and cleanup deadlines
- Think about flag hygiene as code health — every forgotten flag is dead code that confuses future developers
- Ensure both code paths (flag ON and OFF) are tested — incomplete testing of the OFF path causes production incidents during rollback
- Design flag evaluation at boundaries (controller/handler level) not deep in domain logic — makes cleanup trivial
- Cap active flag count — more than 20 flags indicates cleanup debt, not delivery velocity

### Anti-Patterns for This Activity
- Do NOT let flags become permanent configuration — flags are for progressive delivery, settings are for configuration
- Do NOT allow nested flag checks (if flagA && flagB) — combinatorial explosion makes testing impossible
- Do NOT generate feature flag rules unless the `feature-flags` extension is confirmed active

### Quality Check
A good output from this activity sounds like:
- "FF-01: Every flag MUST have an owner and expiration date. FF-04: Flag cleanup within 1 sprint after reaching 'Fully On'. FF-10: Max 20 active flags system-wide."
- "FF-CODE-01: Flag check at highest possible level (controller/use-case entry) — not deep in domain logic. Both paths tested. Dead flags tracked in tech debt backlog."

---

## Files Enriched

| File | Enrichment |
|------|-----------|
| `coding-standards.md` | Feature flag usage patterns, lifecycle management |
| `testing-strategy.md` | Testing with flags on/off, flag combination testing |

---

## Forced Conditional Generation

| File | Normal Trigger | With Feature Flags Extension |
|------|---------------|:----------------------------:|
| `feature-flags.md` | — (no normal trigger) | ✅ GENERATED — full feature flag steering file |

---

## New File: feature-flags.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Feature Flags extension | date: {generation-date} -->

# Feature Flags

## Flag Architecture

**System:** {from AP — e.g., LaunchDarkly / Unleash / custom DB-backed / config file}
**Evaluation:** {from AP — e.g., server-side / client-side / both}
**Scoping:** {from AP — e.g., per-tenant, per-user, per-environment, percentage rollout}

---

## Flag Lifecycle

```
Created → Development → Testing → Rollout → Fully On → Cleanup (Remove)
```

| Phase | Duration | Rules |
|-------|----------|-------|
| Development | During feature build | Flag defaults OFF; only ON in dev for implementer |
| Testing | During QA | Flag ON in test environments |
| Rollout | Progressive delivery | Percentage rollout OR per-tenant enablement |
| Fully On | After successful rollout | Flag ON for all — ready for removal |
| Cleanup | Next sprint | Remove flag from code — dead code otherwise |

---

## Flag Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| FF-01 | Every feature flag MUST have an owner and expiration date |
| FF-02 | Flag naming: `{feature-area}.{flag-name}` in kebab-case — e.g., `incidents.ai-classification` |
| FF-03 | Short-lived flags ONLY — max lifetime: {from AP — e.g., 30 days after full rollout} |
| FF-04 | Flag cleanup: remove from code within {from AP — e.g., 1 sprint} after reaching "Fully On" |
| FF-05 | No nested flags — if feature A depends on flag B, document the dependency explicitly |
| FF-06 | Flag defaults: OFF in production, ON in development — never the reverse |
| FF-07 | Tenant-scoped flags: respect tenant isolation — Tenant A's flag state never affects Tenant B |
| FF-08 | Flag evaluation: happens ONCE per request at entry point — cached for the request lifetime |
| FF-09 | Dead flags (expired, always-on for >30 days): track and remove in tech debt backlog |
| FF-10 | Max active flags: {from AP — e.g., 20 across system} — more indicates cleanup debt |

<!-- end: AP-sourced -->

---

## Code Patterns

<!-- begin: AP-sourced -->

### Flag Check Pattern

```
// Good: clean separation
if (flags.isEnabled('incidents.ai-classification')) {
  return classifyWithAI(incident);
} else {
  return classifyManually(incident);
}

// Bad: flag buried in logic
const classification = flags.isEnabled('incidents.ai-classification') 
  ? await aiService.classify(incident) 
  : incident.category; // unclear what's flagged
```

### Rules for Flag Usage in Code

| Rule | Standard |
|------|----------|
| FF-CODE-01 | Flag check at highest possible level (controller/use-case entry) — not deep in domain logic |
| FF-CODE-02 | Both paths (flag ON and OFF) MUST work correctly — test both |
| FF-CODE-03 | Flag-controlled code: clearly commented with flag name — aids cleanup |
| FF-CODE-04 | NO business logic inside flag evaluation — flags enable/disable, not configure |
| FF-CODE-05 | When flag removed: delete BOTH paths' dead code — leave only the winning path |

<!-- end: AP-sourced -->

---

## Rollout Strategy

<!-- begin: AP-sourced -->

| Strategy | When to Use | Risk |
|----------|------------|:----:|
| All-at-once | Low-risk, well-tested features | Low |
| Per-tenant | Customer-specific features or cautious rollout | Medium |
| Percentage | High-risk features, gradual confidence building | Medium |
| Canary (1%) | Critical path changes, infrastructure changes | Low-Medium |
| Ring-based | Enterprise with internal → beta → GA stages | Low |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **NEVER** leave a flag in code past its expiration — it becomes confusing dead code
2. **NEVER** use flags for permanent configuration — use configuration/settings instead
3. **NEVER** create flags with no clear removal plan
4. **NEVER** nest flag checks (if flagA && flagB) — creates combinatorial explosion
5. **NEVER** let flag count grow unbounded — cap and enforce cleanup
6. **NEVER** use flags to hide tech debt or incomplete work indefinitely
```

---

## Enrichment to coding-standards.md

```markdown
## Feature Flag Patterns

| Rule | Standard |
|------|----------|
| FF-STD-01 | Import flags from central flag service — no direct config reads |
| FF-STD-02 | Flag checks at boundary (controller/handler) — not inside domain logic |
| FF-STD-03 | Comment flag-controlled code blocks: `// FLAG: {flag-name} — remove when fully rolled out` |
| FF-STD-04 | Both code paths have tests — don't test only the "new" path |
```

## Enrichment to testing-strategy.md

```markdown
## Feature Flag Testing

| Rule | Standard |
|------|----------|
| FF-TEST-01 | Test with flag ON and flag OFF — both paths must work |
| FF-TEST-02 | Test flag evaluation logic: correct tenant/user gets correct flag state |
| FF-TEST-03 | Integration tests: run full suite with all flags ON and all flags OFF |
| FF-TEST-04 | No test should DEPEND on a specific flag state without explicitly setting it |
```

---

## Key Rule

Feature Flags enrichment adds lifecycle management and code hygiene rules — preventing flags from becoming permanent code pollution. The core principle: flags are TEMPORARY delivery mechanisms, not permanent configuration.

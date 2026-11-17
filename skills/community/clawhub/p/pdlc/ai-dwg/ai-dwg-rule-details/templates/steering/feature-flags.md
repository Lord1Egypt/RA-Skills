<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: feature-flags.md (CONDITIONAL — ADLC Extension)

**Generate IF:** Feature Flags extension was active in AI-ADLC.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Feature Flags extension | date: {generation-date} -->

# Feature Flags

## Architecture
**System:** {tool}  |  **Evaluation:** {server/client}  |  **Scoping:** {tenant/user/percentage}

## Lifecycle
<!-- begin: AP-sourced -->
Created → Development → Testing → Rollout → Fully On → Cleanup (Remove)

| Phase | Duration | Rules |
|-------|----------|-------|
| Development | During build | Default OFF; ON for implementer only |
| Testing | QA phase | ON in test environments |
| Rollout | Progressive | Percentage/per-tenant |
| Fully On | Post-rollout | Ready for removal |
| Cleanup | Next sprint | Remove from code |
<!-- end: AP-sourced -->

## Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FF-01 | Every flag has owner + expiration |
| FF-02 | Naming: `{area}.{flag-name}` kebab-case |
| FF-03 | Max lifetime: {days} after full rollout |
| FF-04 | Cleanup within {n} sprint(s) |
| FF-05 | No nested flags |
| FF-06 | Default: OFF in prod, ON in dev |
| FF-07 | Tenant-scoped: respect isolation |
| FF-08 | Evaluate ONCE per request |
| FF-09 | Dead flags → tech debt backlog |
| FF-10 | Max active: {n} |
<!-- end: AP-sourced -->

## Code Patterns
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| FF-CODE-01 | Check at highest level (controller) |
| FF-CODE-02 | Both paths tested |
| FF-CODE-03 | Comment with flag name |
| FF-CODE-04 | No business logic in evaluation |
| FF-CODE-05 | Remove both paths' dead code on cleanup |
<!-- end: AP-sourced -->

## Anti-Patterns
1. NEVER leave flags past expiration
2. NEVER use for permanent config
3. NEVER nest flag checks
4. NEVER let count grow unbounded
```

## Filling: Refer to `mapping/extension-featureflags-enrichment.md`.

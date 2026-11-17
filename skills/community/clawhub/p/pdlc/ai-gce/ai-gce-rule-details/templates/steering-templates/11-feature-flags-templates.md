<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Feature Flags Steering Templates

> **Purpose:** Used by the project-init-agent to generate feature flag steering files
> in the target project's `rules/` folder. These templates encode flag lifecycle management,
> implementation patterns, testing strategy, and cleanup rules derived from `feature-flags.md`
> (conditional — only if Feature Flags extension is active).

---

## feature-flags-core.md (Always — within feature flags scope)

**Generates**: `rules/feature-flags-core.md`
**Condition**: Generated only IF `feature-flags.md` exists in workspace steering
**Derived From**: feature-flags.md + tech-stack.md + project-governance.md

```markdown
---
inclusion: always
---

# Feature Flag Standards

## Flag Management
- Flag provider: {flag_provider} ({flag_provider_description})
- ALL flags MUST be registered in {flag_registry_location}
- Flag naming convention: {flag_naming_pattern} (e.g., {flag_naming_examples})
- {flag_categorization}: {flag_categories}

## Flag Lifecycle
- Creation: {flag_creation_process}
- Activation: {flag_activation_strategy}
- Monitoring: {flag_monitoring_requirements}
- Retirement: {flag_retirement_process}
- Maximum flag age: {max_flag_age} (enforced by {flag_age_enforcement})

## Implementation Rules
- NEVER nest flag checks more than {max_nesting_depth} levels deep
- NEVER use flags to control {prohibited_flag_uses}
- Flag evaluation MUST be {flag_evaluation_strategy} (cached/real-time)
- Default state (flag provider unavailable): {flag_default_behavior}
- ALL flag decisions MUST be logged ({flag_audit_strategy})

## Flag Types
| Type | Purpose | Max Lifetime | Example |
|------|---------|:------------:|---------|
| Release | Gradual rollout | {release_flag_lifetime} | {release_flag_example} |
| Experiment | A/B testing | {experiment_flag_lifetime} | {experiment_flag_example} |
| Ops | Kill switch | Permanent | {ops_flag_example} |
| Permission | Entitlement | Permanent | {permission_flag_example} |
```

---

## feature-flags-implementation.md (FileMatch `{source_code_pattern}`)

**Generates**: `rules/feature-flags-implementation.md`
**Derived From**: feature-flags.md + tech-stack.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{source_code_pattern}"
---

# Feature Flag Implementation Patterns

## Code Patterns
- Use {flag_sdk_pattern} for flag evaluation
- NEVER use string literals for flag keys — use {flag_constant_strategy}
- {flag_injection_pattern}
- {flag_context_propagation}

## Branching Strategy
- Short-lived flags: use {short_flag_branching_pattern}
- Long-lived flags: use {long_flag_branching_pattern}
- NEVER leave dead code behind after flag removal

## Testing with Flags
- ALL flag-gated features MUST be tested in BOTH states (on and off)
- {flag_test_override_mechanism}
- Integration tests MUST cover flag transition scenarios
- {flag_test_isolation_strategy}

## Cleanup Protocol
- When flag is retired:
  1. Remove flag evaluation code
  2. Remove unused code path ({dead_code_removal_strategy})
  3. Remove flag from {flag_registry_location}
  4. Remove flag-specific tests
  5. Update documentation
- Cleanup MUST be a separate {cleanup_work_item_type} (not mixed with feature work)
```

---

## feature-flags-governance.md (Always — within feature flags scope)

**Generates**: `rules/feature-flags-governance.md`
**Derived From**: feature-flags.md + project-governance.md

```markdown
---
inclusion: always
---

# Feature Flag Governance

## Ownership
- Every flag MUST have an owner ({flag_owner_definition})
- Owner is responsible for: activation, monitoring, and retirement
- {orphan_flag_policy}

## Review Requirements
- New flags require {flag_creation_approval}
- Flag activation in production requires {production_activation_approval}
- {flag_percentage_rollout_approval}

## Monitoring
- ALL flags MUST have {flag_monitoring_type}
- Alert on: {flag_alert_conditions}
- Dashboard: {flag_dashboard_requirements}

## Debt Tracking
- Flags past maximum age are flagged as tech debt
- {flag_debt_tracking_mechanism}
- {flag_debt_review_cadence}
- Target: maximum {max_active_flags} active flags at any time
```

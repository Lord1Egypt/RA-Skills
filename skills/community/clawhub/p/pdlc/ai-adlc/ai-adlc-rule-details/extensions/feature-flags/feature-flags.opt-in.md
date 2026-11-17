<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Feature Flags & Progressive Delivery

## When This Extension Applies

Your system likely needs feature flag architecture if:

- Need to release features to subsets of users before full rollout
- A/B testing or experimentation is part of the product strategy
- Kill switches required for risky features (instant disable without deploy)
- Different tenants/customers get different feature sets
- Trunk-based development with incomplete features behind flags

## Opt-In Question

```
### Would you like to apply Feature Flags & Progressive Delivery patterns?

This extension adds detailed guidance for:
- Flag architecture (where flags live, how they're evaluated, performance impact)
- Flag types (release flags, experiment flags, ops flags, permission flags)
- Flag lifecycle (creation → rollout → permanent-on → cleanup/removal)
- Evaluation engine (client-side vs. server-side, caching, targeting rules)
- Progressive rollout strategies (percentage, user segment, tenant-based, canary)
- Flag governance (who creates, who approves rollout, stale flag detection)
- Multi-tenant flag scoping (per-tenant feature enablement)
- Technical debt: flag cleanup process (preventing permanent flag accumulation)

(a) Yes — Design feature flag architecture into the system
(b) No — All features ship to all users simultaneously; no flags needed

Recommended for: SaaS products, multi-tenant with tiered features, continuous deployment
Skip if: Internal tool, all-or-nothing releases, small team with simple deployment
```

## Status: ✅ Available (v1.1)

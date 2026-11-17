<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Financial Governance (Opt-In)

**ID:** E6
**Trigger:** User mentions "budget", "funding", "financial governance", "guardrails", "approval threshold" OR enterprise context OR portfolio budget > $1M
**Stages:** 5 (Governance Gate), 8 (Dashboards)

---

## Detection

If any of the following are true, present this prompt:
- User says "budget approval", "funding model", "financial governance", "guardrails"
- Enterprise context detected (multiple departments, formal budget process)
- Portfolio total budget exceeds organizational significance threshold

---

## Activation Prompt

```
🏦 Extension available: Financial Governance

This adds to Stages 5 and 8:
• Budget guardrails (max per-project spend, portfolio ceiling)
• Approval thresholds (auto-approve below $X, escalate above $Y)
• Portfolio-level ROI tracking (aggregate return on investment)
• Budget burn-rate monitoring and projection
• Funding model configuration (project-based vs. incremental)

Useful for: enterprise portfolios, formal budget governance, CFO reporting.

Activate Financial Governance? [Yes / No]
```

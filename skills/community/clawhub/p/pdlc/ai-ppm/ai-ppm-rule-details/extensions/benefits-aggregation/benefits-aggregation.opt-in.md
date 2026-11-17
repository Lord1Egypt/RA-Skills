<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Benefits Realization Aggregation (Opt-In)

**ID:** E7
**Trigger:** User mentions "benefits", "value realized", "did we get what we paid for" OR projects are completing/retiring OR mature portfolio with post-delivery tracking
**Stages:** 8 (Dashboards), 10 (Retirement)

---

## Detection

If any of the following are true, present this prompt:
- User says "benefits", "value delivered", "benefits realization", "ROI tracking"
- One or more projects are in Retired state with benefits data available
- FLO roll-up includes benefits_realized_pct from POLC Stage 16
- User asks "are our projects delivering value?"

---

## Activation Prompt

```
📈 Extension available: Benefits Realization Aggregation

This adds to Stages 8 and 10:
• Cross-project benefits tracking (delivered vs. promised across portfolio)
• Benefits realization curve (how value accumulates over time)
• Value-gap analysis (projects consuming budget without delivering benefits)
• Lessons on estimation accuracy (were our value predictions right?)

Useful for: mature portfolios tracking actual outcomes, board reporting on investment return, improving future business case accuracy.

Activate Benefits Aggregation? [Yes / No]
```

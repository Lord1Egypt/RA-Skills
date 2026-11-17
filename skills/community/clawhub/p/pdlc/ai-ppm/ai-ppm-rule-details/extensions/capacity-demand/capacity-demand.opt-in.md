<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Portfolio-Level Capacity & Demand (Opt-In)

**ID:** E4
**Trigger:** User mentions "capacity", "resource contention", "over-allocated", "supply vs demand" OR >3 projects sharing teams
**Stages:** 3 (Strategic Alignment), 8 (Dashboards)

---

## Detection

If any of the following are true, present this prompt:
- User says "capacity", "resource", "over-allocated", "contention"
- 3+ projects share the same team or key resource
- Governance gate reveals capacity conflicts (Step 5.3)

---

## Activation Prompt

```
👥 Extension available: Portfolio-Level Capacity & Demand

This adds to Stages 3 and 8:
• Resource supply vs. demand visualization across the portfolio
• Over-allocation detection (which teams/roles are spread too thin)
• Capacity-constrained scheduling recommendations
• Resource contention alerts in dashboards

Useful for: portfolios where teams serve multiple projects, limited specialists, shared platforms.

Activate Capacity & Demand? [Yes / No]
```

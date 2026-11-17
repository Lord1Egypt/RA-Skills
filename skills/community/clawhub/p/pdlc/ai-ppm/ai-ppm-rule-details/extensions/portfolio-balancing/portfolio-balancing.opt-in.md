<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Portfolio Balancing & Visualization (Opt-In)

**ID:** E1
**Trigger:** User mentions "balance", "portfolio mix", "horizon distribution", "risk spread" OR portfolio has >10 projects OR depth = Comprehensive
**Stages:** 4 (Prioritization), 8 (Dashboards)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly says "balance", "portfolio mix", "bubble chart", "horizon"
- Portfolio Register has >10 active projects
- Depth level = Comprehensive

---

## Activation Prompt

```
📊 Extension available: Portfolio Balancing & Visualization

This adds to Stages 4 and 8:
• Bubble chart data (Value × Effort, size = budget)
• Three Horizons distribution (H1 core / H2 adjacent / H3 transformational)
• Risk-spread analysis (concentration risk detection)
• Balance guardrails (optional threshold enforcement)

Useful for: large portfolios, boards requesting visual portfolio views, balanced investment strategy.

Activate Portfolio Balancing? [Yes / No]
```

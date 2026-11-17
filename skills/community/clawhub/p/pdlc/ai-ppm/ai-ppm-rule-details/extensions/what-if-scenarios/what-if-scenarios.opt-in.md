<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: What-If Scenario Modeling (Opt-In)

**ID:** E2
**Trigger:** User mentions "what-if", "scenario", "trade-off", "compare options" OR capacity constraints detected during rebalancing
**Stages:** 9 (Portfolio Rebalancing)

---

## Detection

If any of the following are true, present this prompt:
- User says "what-if", "scenario", "what happens if", "compare"
- Stage 9 identifies multiple viable rebalancing options
- Capacity constraints make trade-offs unavoidable

---

## Activation Prompt

```
🔮 Extension available: What-If Scenario Modeling

This adds to Stage 9:
• Side-by-side scenario comparison (2-4 alternative portfolio compositions)
• Trade-off analysis (what you gain vs. what you lose per scenario)
• Impact prediction (budget, timeline, capacity for each option)
• Sensitivity check (which assumptions would flip the recommendation)

Useful for: complex rebalancing, contentious decisions, board presentations.

Activate What-If Scenarios? [Yes / No]
```

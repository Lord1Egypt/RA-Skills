<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Advanced Discovery (Opt-In Prompt)

**Trigger:** User mentions "OKRs", "jobs to be done", "JTBD", "hypothesis testing", "opportunity scoring"
**Stage:** 4 (Product Discovery & Roadmap)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly requests OKRs or JTBD framework
- Depth = Comprehensive and Product Maturity = New or Growth
- User asks about hypothesis-driven development

## Activation Prompt

```
I detect you'd benefit from the Advanced Discovery extension.

This adds to Stage 4:
• OKR hierarchy (Objective → Key Results per goal)
• Jobs-to-be-Done framing (job stories for each user segment)
• Opportunity scoring (reach × impact × confidence × effort)
• Hypothesis backlog (assumptions to validate before building)

This is useful for data-driven teams, new products with high uncertainty,
or organizations using OKR-based planning.

Activate Advanced Discovery? (yes/no)
```

If yes → load `advanced-discovery.md`

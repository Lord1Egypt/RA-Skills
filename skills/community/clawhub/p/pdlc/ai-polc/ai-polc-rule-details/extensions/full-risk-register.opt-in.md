<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Risk Register (Opt-In Prompt)

**Trigger:** User mentions "full risk management", "risk scoring", "risk owners", "risk review cadence"
**Stage:** 9 (Product Risk & Assumptions)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly requests full risk management
- Product Maturity = New AND Stakeholder Density = High
- Multiple HIGH-scoring risks identified in basic assessment

## Activation Prompt

```
I detect you'd benefit from the Full Risk Register extension.

This upgrades Stage 9 from a basic risk list to:
• Risk owners (who monitors each risk)
• Detailed response plans (step-by-step mitigation)
• Risk review cadence (formal review sessions)
• Risk trend tracking (improving or worsening over time)
• Assumption validation experiments (designed tests)

This is useful for high-uncertainty products, enterprise governance,
or when many stakeholders need risk visibility.

Activate Full Risk Register? (yes/no)
```

If yes → load `full-risk-register.md`

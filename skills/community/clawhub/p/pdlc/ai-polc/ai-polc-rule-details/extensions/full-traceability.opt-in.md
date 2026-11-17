<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Traceability (Opt-In Prompt)

**Trigger:** User mentions "full traceability", "audit trail", "compliance evidence", "regulatory traceability"
**Stage:** 10 (Traceability Spine)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly requests full/audit-grade traceability
- Context factor: Regulatory/Compliance = Heavy
- Depth = Comprehensive and regulated industry mentioned

## Activation Prompt

```
I detect you'd benefit from the Full Traceability extension.

This upgrades Stage 10 from simple Goal→Epic links to:
• Audit-grade matrix: Intent→Epic→Story→AC→Increment→Outcome
• Compliance evidence mapping (regulatory requirement → AC)
• Change impact tracing (when a goal changes, trace affected items)
• Outcome tracking (did the delivered increment achieve the goal?)

This is required for regulated environments, enterprise audits, and
benefits realization reporting.

Activate Full Traceability? (yes/no)
```

If yes → load `full-traceability.md`

<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Quality Review AI-Assist (Opt-In Prompt)

**Trigger:** User mentions "check quality", "review backlog quality", "ambiguity", "missing AC"
**Stage:** Post-Stage 5 (or any Operations refinement)

---

## Detection

If any of the following are true, present this prompt:
- User explicitly asks to review backlog quality
- Recurring refinement reveals poorly specified epics
- Scale = Multi-team (consistency across teams matters)

## Activation Prompt

```
I detect you'd benefit from the Quality Review extension.

This adds automated backlog quality scanning:
• Ambiguity detection (vague language in epics/stories)
• Missing criteria check (epics without testable AC)
• Scope clarity (epics that mix multiple concerns)
• Dependency risk flags (unacknowledged cross-epic dependencies)
• Completeness scoring (per-epic quality score)

This is useful for multi-team environments, quality-conscious POs,
or when refinement sessions keep finding the same issues.

Activate Quality Review? (yes/no)
```

If yes → load `quality-review.md`

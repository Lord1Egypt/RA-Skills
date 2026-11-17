<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: session-governance.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Methodology decisions | date: {generation-date} -->

# Session Governance (AI-DLC v1)

## Rules for AI-Assisted Development Sessions

<!-- begin: AP-sourced -->

| Rule | Description |
|------|-------------|
| SG-01 | NEVER write code without checking relevant steering files first |
| SG-02 | One task per session — complete before starting next |
| SG-03 | Verify against DEFINITION_OF_DONE.md before declaring task complete |
| SG-04 | If steering rules conflict or are unclear → ask, don't assume |
| SG-05 | Log any deviation from steering rules with justification |
| SG-06 | Read module-structure.md before creating files in any module |
| SG-07 | Read domain-context.md before naming any entity, variable, or endpoint |
| SG-08 | Read api-standards.md before creating any API endpoint |
| SG-09 | Read database-rules.md before writing any migration or query |
| SG-10 | Read testing-strategy.md before writing tests — follow the patterns |
| SG-11 | NEVER generate code outside the defined module structure |
| SG-12 | NEVER invent new architectural patterns not in the steering files |

<!-- end: AP-sourced -->

## Session Structure

<!-- begin: AP-sourced -->

1. **Start:** Read task requirements + identify affected modules
2. **Check:** Load relevant steering files for those modules
3. **Plan:** Outline approach before writing code
4. **Implement:** Write code following all steering rules
5. **Test:** Write tests per testing-strategy.md
6. **Verify:** Check against DEFINITION_OF_DONE.md
7. **Complete:** Commit with proper message format (git-workflow.md)

<!-- end: AP-sourced -->

## Autonomy Mode

**Mode:** {from config — Autopilot | Supervised}

| Mode | Behavior |
|------|----------|
| Autopilot | Complete task end-to-end; user reviews result |
| Supervised | Yield after each file edit; user approves each change |
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 6).

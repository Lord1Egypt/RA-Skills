---
name: master-skill-review
description: Review an OpenClaw skill for token efficiency, scriptability, and clean action boundaries; back up first, then improve the skill.
input: skill path or skill name
output: 审查结论、优化建议、建议新增的 scripts/references、是否通过
---

# Skill Review

## What this skill does
This meta-skill reviews another skill and checks whether it:
- is too verbose
- should move repetitive mechanical steps into scripts
- wastes tokens through repeated explanation
- clearly separates default execution from confirmation-required actions

## Typical ownership / permission level
- This skill is typically used by the **`master`** agent.
- It often requires **higher local permissions** because it may inspect and modify:
  - `SKILL.md`
  - `references/`
  - `scripts/`
  - other local skill folders

## Core rules
- Prefer **thin markdown + heavier scripts**.
- If a step can be scripted, it should usually be scripted.
- If no extra requirements exist, prefer executing scripts instead of repeatedly re-explaining a process in chat.
- `SKILL.md` should hold rules, boundaries, and confirmation points.
- `scripts/` should hold mechanical checks, copying, verification, and repeatable operations.
- `references/` should stay lightweight.
- After review, the default is: **back up first, then modify, then show evidence**.

## Standard flow
1. Read the target `SKILL.md`
2. Inspect `scripts/` and `references/`
3. Identify verbosity, duplication, and non-scripted mechanical steps
4. Back up the target skill files
5. Improve the skill structure
6. Show backup paths, changes made, and final evidence

## Included files
- `references/checklist.md`
- `scripts/review_skill.sh`

## Recommended command
```bash
bash skills/master-skill-review/scripts/review_skill.sh <skill-dir-or-skill-md>
```

## Do not
- Do not keep heavy explanations in `SKILL.md` when a script can do the work.
- Do not modify a target skill without first backing it up.
- Do not leave action boundaries unclear.

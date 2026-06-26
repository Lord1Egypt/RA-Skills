---
name: maverick-process-to-skill
description: Turn a user-described business process into an automated execution flow and optionally convert it into a reusable local skill. Use when a user explains steps in natural language, asks the agent to run or automate them, and wants the option to save that process for future one-command reuse.
---

# Process To Skill

Use this skill to operationalize "explain once, reuse later" behavior for business workflows.

## Workflow

1. Extract the process from the user's message as an ordered list of steps, inputs, and expected output.
2. Execute or automate the process for the current request.
3. Confirm the result in plain business language.
4. Ask whether the user wants to save the process as a reusable skill.
5. If the user says yes, create a new skill folder with a trigger-focused `description`, concise workflow instructions, and `agents/openai.yaml` metadata.
6. Return the saved skill name and one example command the user can use next time.

## Save Prompt Requirement

After completing the process, always ask a direct reuse question:
- "Do you want me to save this as a reusable skill so next time you can call it directly without re-explaining the steps?"

If the answer is unclear, ask once more with a suggested skill name.

## Skill Authoring Rules

- Use lowercase hyphenated names (`<verb>-<object>` when possible).
- Keep `SKILL.md` procedural and short; include only repeatable steps.
- Put trigger conditions in frontmatter `description`, not in the body.
- Add only required resource folders (`scripts/`, `references/`, `assets/`) when they are actually needed.
- Reuse existing local scripts/templates when possible instead of duplicating logic.

## Minimal Capture Template

When saving a process, capture:
- Goal: What business outcome this process produces.
- Inputs: Required user-provided data.
- Steps: Deterministic sequence to run.
- Output: Expected deliverable format.
- Trigger examples: 2-3 natural language prompts that should activate the skill.

## Guardrails

- Do not auto-save without user confirmation.
- Do not save one-off ad hoc tasks that are unlikely to be reused.
- If required tools or permissions are missing, report the blocker and offer a partial skill draft.

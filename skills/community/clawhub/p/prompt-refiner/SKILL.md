---
name: prompt-refiner
description: Use when user input is vague, underspecified, lacks boundaries or acceptance criteria, or would benefit from being reframed into a more executable prompt before work begins. Also use when user explicitly asks to optimize/refine/improve a prompt.
---

# prompt-refiner

> A prompt is not just wording polish — it is task clarification, boundary setting, and verification shaping.

Refine vague user prompts into clear, actionable, verifiable versions. Show the refined result and let the user confirm before execution. Works as a closed loop with `session-learner`, which captures user choice preferences over time.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Vague request | Refine first |
| Complete prompt | Execute directly, no popup |
| Substantial improvement | Show refined + popup choose |
| No substantial improvement | Skip popup, execute original |
| User says "just do it" | Auto-apply |
| User says "only optimize" | Return refined, don't execute |

## Continue Modes

1. **Popup-confirm (default)** — Show refined prompt, popup to choose refined vs original, execute after choice
2. **Auto-apply** — When user says "just do it / skip confirmation", show refined then execute immediately
3. **Optimize-only** — When user only asks to refine without executing, return refined result only

## When NOT to Use
- User input is already well-structured with clear goals, constraints, and acceptance criteria
- Single-step operations (delete a line, rename a variable, change a single string)
- Simple factual questions or explanations
- User explicitly says "don't optimize" or "just do it"

## Workflow
1. Extract original prompt and current session context (goals, constraints, tech stack, errors, expected output).
2. Generate refined prompt, ensuring:
   - Core intent unchanged
   - Goals and boundaries explicit
   - Output format verifiable
   - Language concise, no fluff
3. Produce result based on Continue Mode.
4. After user makes a choice, generate a **learning signal** for `session-learner` — capture preference pattern, never record full prompt text.

## Refined Prompt Structure

Include the following blocks as needed (trim, don't mechanically stack):
- Goal
- Context
- Constraints / Non-goals
- Execution Requirements
- Output Format
- Acceptance Criteria

For detailed patterns and examples, see `references/prompt-patterns.md`.

## Output Templates

### A) Popup-confirm (default)

**First, judge whether refinement adds real value.** If the refined prompt only tweaks wording without adding explicit goals/constraints/output format/acceptance criteria, and doesn't significantly reduce ambiguity, it has **no substantial optimization value**.

- **No substantial value**: Don't popup, don't interrupt. Execute with the original prompt directly.
- **Has substantial value**: Execute the two steps below. Do not skip or merge them.

**Step 1 (required): Output the refined prompt as plain text in the chat area first.**

> **Optimized Prompt**
> <full refined prompt content>

**Step 2 (required, after step 1): Call AskUserQuestion popup for user to choose.**
Options:
- A: Use refined prompt to continue (recommended)
- B: Use original prompt to continue

Forbidden:
- Do not popup without showing the refined prompt content first
- Do not put the refined prompt inside AskUserQuestion description as a substitute for step 1
- Steps 1 and 2 must be in the same response

Execute after user chooses.

### B) Auto-apply

> **Optimized Prompt**
> <refined prompt>

---
Then execute immediately.

### C) Optimize-only

> **Optimized Prompt**
> <refined prompt>

Do not execute the task.

## Heuristics
- Rewrite vague phrases ("optimize it / make it better / fix it up") into actionable steps with clear criteria.
- Fill in missing inputs, boundary conditions, and completion definitions.
- For code tasks: specify scope, verification method, expected deliverables.
- For content tasks: specify audience, tone, length, structure constraints.
- If critical context is missing, ask the minimum necessary clarification; otherwise proceed.

## Integration with session-learner

- When user chooses refined or rejects it, this is a **preference signal** for `session-learner`.
- `session-learner` should only summarize rules (e.g., "user prefers seeing refined version before confirming"), never record full prompt text.
- Over time, `session-learner` builds a preference profile that makes `prompt-refiner` increasingly aligned with user habits.

## Priority Rules
- When user explicitly specifies a flow, follow user instructions.
- When no explicit instruction, use Popup-confirm.

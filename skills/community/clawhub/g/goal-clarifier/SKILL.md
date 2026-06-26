---
name: goal-clarifier
description: Warm multi-turn goal clarification and action planning. Use when the user has a vague, oversized, or tangled goal and wants help thinking it through, narrowing focus, or turning it into concrete next steps.
metadata: {"openclaw":{"emoji":"🧭"}}
---

# Goal Clarifier

Turn fuzzy goals into realistic next steps.

## References

- Chinese request: read `./references/guide-zh.md`
- English request: read `./references/guide-en.md`
- Full flow: `./references/workflow-zh.md` or `./references/workflow-en.md`
- Tone and sample outputs: `./references/examples-zh.md` or `./references/examples-en.md`
- Testing and iteration: `./references/eval-checklist-zh.md` or `./references/eval-checklist-en.md`

## Rules

- Clarify before planning when the goal is vague, overloaded, conflicted, or unrealistic.
- Ask only 1-3 high-value questions per turn.
- Reflect back your understanding every 2-4 turns so the user feels heard and can correct course.
- Fit the plan to the user's real time, energy, budget, resources, dependencies, and execution style.
- Prefer a lighter plan the user can actually start over a complete but heavy plan.
- Stop clarifying once the key constraints and goal are clear enough; then switch into action planning.
- Keep the tone warm, structured, and natural. Do not sound like a form, interrogation, or therapy session.
- Respond in the user's language.
- Use the final output structure defined in the matching guide file.
- End with one grounded follow-up question that helps the user continue moving.
- When `[GOAL_CONTEXT]` data is provided in the message, use it to understand the current state of phases, tasks, and weekly plans. Reference specific completed/pending tasks by name when discussing progress or next steps. Never mention `[GOAL_CONTEXT]` tags to the user — treat this as background knowledge.
- After the initial roadmap is confirmed, transition naturally into weekly schedule planning. Ask about the user's daily available time, preferred time slots, and any recurring commitments before generating a detailed weekly plan.
- When a weekly plan cycle is ending or has ended, proactively suggest reviewing execution and planning the next week. Reference specific tasks that were completed or missed from the `[GOAL_CONTEXT]` data.

---
name: openspace
description: Use OpenSpace for complex multi-step tasks: research, code evolution, skill creation, web automation, and long-running autonomous work. Prefer this when the task needs skill search, auto-evolution, grounding, or multi-tool orchestration beyond simple single-step actions.
---

# OpenSpace

Bridge to OpenSpace for tasks that benefit from autonomous grounding, skill discovery, and auto-evolution.

## When to Use

- Research / deep dive requiring multiple tools or web sources
- Multi-step automation beyond simple exec/web_fetch
- Creating or evolving reusable skills/code
- Long-running tasks that may need retries or fallback strategies
- Anything that feels like a small project rather than a single query

Do NOT use OpenSpace for trivial single-step actions (read a file, run one command, quick lookup).

## Available Tools

- `openspace__execute_task` — main entry; run a full task end-to-end
- `openspace__search_skills` — discover local/cloud skills before running
- `openspace__fix_skill` — repair a broken skill when execution fails
- `openspace__upload_skill` — upload an evolved skill to the cloud

## Required Environment

Set these before calling any `openspace__*` tool:

- `OPENSPACE_WORKSPACE=/home/admin147258/open-space`
- `OPENSPACE_HOST_SKILL_DIRS=/home/admin147258/.openclaw/workspace/skills`

## Usage Pattern

Primary call:
```json
{
  "task": "Natural language task description",
  "workspace_dir": "/home/admin147258/open-space",
  "skill_dirs": ["/home/admin147258/.openclaw/workspace/skills"],
  "search_scope": "all",
  "max_iterations": 20
}
```

Guidance:
- Keep `task` concrete and goal-oriented.
- Use `skill_dirs` so OpenSpace can reuse/evolve host skills.
- Use `search_scope: "all"` unless you explicitly want local-only.
- Expect longer runtimes; do not chain OpenSpace calls back-to-back without checking results.
- If `openspace__execute_task` fails due to a broken skill, consider `openspace__fix_skill`.

## Result Handling

`openspace__execute_task` returns structured output. Extract:
- `result.answer` / `result.summary` for user-facing reply
- `result.evolved_skills` if OpenSpace created/updated skills
- Errors: surface the error clearly; consider `openspace__fix_skill` if a skill broke

## Notes

- Do not run OpenSpace and another heavy agent in parallel without explicit user request.
- If OpenSpace evolves skills, they may appear under the host skill dirs.

---
metadata:
  author: es6kr
  version: "0.1.1"
name: next
depends-on:
  - fix
  - hook
description: >-
  Suggest next actions after completing any task. Auto-invocation via Stop hook (`resources/next-trigger.sh`) using JSON `decision:"block"` (registered in the settings.json Stop array). Fires when assistant response contains completion keywords (locale patterns in `data/*.regex`).
  stall-detect - detect stalled follow-up steps and invoke /fix [stall-detect.md], ask-gates - recording-skip / decision-deferral forced-ask / TaskList primary-source / current-work confirmation gates [ask-gates.md], suggestion-patterns - per-context "After X" next-action option templates [suggestion-patterns.md].
  Use when "next action", "what next", "stall", "stuck", "not progressing", "follow-up missing" is mentioned.
---

# Next Action Suggester

## Topic Dispatch

**When this skill is invoked with a topic specifier (e.g., `/next suggestion-patterns` or `Skill("next", "suggestion-patterns")`), load and follow only the matching topic file. Do not echo the Topics table or summarize other topics in the response.** The Topics table below is an index — for a normal invocation, follow the Instructions and Read each topic when you reach the step that references it.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| stall-detect | Detect stalled follow-up steps and invoke /fix | [stall-detect.md](./stall-detect.md) |
| ask-gates | Step 0.3/0.4/0.5/0.7 ask gates: recording-skip, decision-deferral forced-ask, TaskList primary-source, current-work confirmation | [ask-gates.md](./ask-gates.md) |
| suggestion-patterns | Per-context "After X" next-action option templates | [suggestion-patterns.md](./suggestion-patterns.md) |

After task completion, use `AskUserQuestion` to suggest next steps and get user selection.

## When to use

Automatically use after any task completion:
- Code writing/modification complete
- Configuration changes complete
- File creation complete
- Commit/push complete
- Skill/agent creation complete
- Bug fix complete

## Instructions

### Step 0: Stall Detection (mandatory)

Before suggesting next actions, run the [stall-detect](./stall-detect.md) topic.

If stall detected → topic invokes `/fix`. If no stall → proceed to Step 0.3.

### Step 0.3–0.7: Ask gates (HARD STOP)

Before composing any next-action ask, pass four gates: **0.3** skip the ask entirely for recording/management topics (fix-plan, archive, todo, session rename); **0.4** if the completion report defers a decision to the user as prose ("let me know and I'll …", "whether to commit/PR is up to you"), that deferral is a decision axis — **force** an `AskUserQuestion` instead of ending on the text; **0.5** call `TaskList` as the primary source for option accuracy (never quote tasks from stale summary memory); **0.7** when the user's current activity is unclear (2+ in_progress tasks, ambiguous scope, handed-off manual work), ask "what are you working on / waiting on" first — separate "in progress" from "waiting on", and prefer free-text via Other over guess options.

**Read [ask-gates.md](./ask-gates.md) before composing options** — it holds the skip-target topic list, the TaskList primary-source Don't/Do, the current-work confirmation triggers, and the in-progress-vs-waiting-on examples. If Step 0.3 marks the work skip-target → report only, no ask; otherwise proceed to Step 1.

### Step 1: Identify completed task type

Identify the type of task just completed.

### Step 2: Use AskUserQuestion tool

**HARD STOP — Read [suggestion-patterns.md](./suggestion-patterns.md) BEFORE composing options.** suggestion-patterns.md holds per-context "After X" option templates that include diversity sources (pending tasks, open PRs, dependency follow-ups, session wrap-up, etc.). Skipping this Read = ad-hoc option list = high risk of missing candidate sources. Step 2 entry without suggestion-patterns.md Read = skill bypass (skill-usage.md "Multi-topic topic .md Read mandatory" violation).

#### Option diversity (HARD STOP)

**Fill all 4 option slots whenever possible.** AskUserQuestion supports max 4 options + auto "Other" = 5 candidates total. Composing only 2-3 options when 4+ candidates exist = under-recommendation. The user typically phrases this as "no more candidates?" or "any more suggestions?".

#### Candidate discovery sources (enumerate all before composing)

| Source | What to look for |
|--------|------------------|
| Visible TaskList | All pending/in_progress entries (call `TaskList` per Step 0.5) |
| Just-completed work | Direct follow-ups (commit / push / verify / test / publish) |
| Open PRs / issues | `gh pr list --search "involves:@me state:open"` / `gh issue list` (when relevant) |
| Recent commits awaiting CI | `gh run list --limit 5` for pending CI watch |
| fix_plan.md / checklist.md | Project-tracked next items (Ralph or general workspace) |
| Session wrap-up | `/cleanup` if multiple tasks done + no immediate user follow-up |
| Other (free text) | Auto-provided by AskUserQuestion |

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|------------------------|
| 1 | Compose 2-3 options + end Step 2 | Enumerate sources above → fill 4 slots. Cap at 4 only if exhausted |
| 2 | "User can pick Other for anything else" rationale for fewer options | Other is for unexpected branches. Explicit options surface options the user might not think of |
| 3 | Skip Read of suggestion-patterns.md because "I know the patterns" | suggestion-patterns.md is updated with new "After X" templates regularly. Read every time |
| 4 | Treat just-completed work as the only source | Each candidate discovery source row is a separate enumeration. Cover all rows before stopping |

#### Self-check (every time before calling AskUserQuestion)

1. Did I Read `suggestion-patterns.md` this turn? → If no, Read first
2. Did I enumerate all 7 candidate discovery sources? → If skipped any, revisit before composing
3. Do I have 4 options or did I stop at 2-3? → If <4 and candidates remain, add until 4 or exhausted
4. Are options diverse (different action types: progress task / external follow-up / wrap-up / verify)? → If all 3 are the same family, broaden

```typescript
AskUserQuestion({
  questions: [{
    question: "What would you like to do next?",
    header: "Next Action",
    multiSelect: true,
    options: [
      { label: "Option 1", description: "Description" },
      { label: "Option 2", description: "Description" },
      { label: "Option 3", description: "Description" },
      { label: "Option 4", description: "Description" }
    ]
  }]
})
```

### Step 3: Register and execute selected action(s)

**If 2 or more actions are selected, register each via TaskCreate and execute sequentially.** If only 1 is selected, execute it directly.

## Suggestion Patterns

Per-context option templates for "After X" completions (code change, feature, bug fix, config, commit, push, PR fix-commit re-review, PR creation reviewer matrix, skill/agent creation, file creation, refactoring, complex workflow, exploration, session wrap-up, PR consolidate).

**Read [suggestion-patterns.md](./suggestion-patterns.md)** for the matching context's option set before calling `AskUserQuestion`. Several patterns carry their own HARD STOP gates (re-review policy, Copilot availability, session wrap-up priority) — follow the pattern's gate, not a generic option list.

## Rules

1. **Always 2-4 options** - AskUserQuestion limitation
2. **Be specific** - "Run npm test" instead of just "Test"
3. **Context-based** - Adjust based on project/situation
4. **Use multiSelect** - When multiple actions can be done together
5. **Register then execute** - When 2+ options are selected, TaskCreate then run sequentially. If only 1, execute directly
6. **State conditions when proposing merge** - When including PR merge in options, the description must show condition state in the form `CI:✅ Review:✅ TestPlan:x/y`. Actual merge runs only via the `/github-flow merge` skill — direct `gh pr merge` is forbidden



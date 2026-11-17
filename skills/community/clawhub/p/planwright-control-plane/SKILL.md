---
name: planwright-control-plane
version: 1.0.0
description: Use when the user is running one or more coding agents and needs a shared control plane to coordinate work and keep an audit trail. Triggers include running parallel Claude Code/Cursor sessions, agents colliding on the same work, needing objectives instead of a task list, or needing auditable evidence of agent-authored changes.
# Platform-specific metadata (add ONE when publishing):
# Hermes:   metadata.hermes: { tags: [mcp, coding-agents, control-plane, audit], category: devops }
# ClawHub:  metadata: { "openclaw": { "requires": { "env": ["PLANWRIGHT_TOKEN"] }, "primaryEnv": "PLANWRIGHT_TOKEN" } }
---

# PlanWright control plane

PlanWright coordinates autonomous coding work over MCP. Humans declare objectives (desired state); agents claim and execute them; every action is written to a signed, hash-chained audit ledger.

## When to use

- More than one agent session is running and they risk colliding.
- The user wants coarse objectives, not story points or subtasks.
- The user needs auditable evidence of what an agent did and who approved it.
- The user mentions "Planwright", "objectives", "control plane", or "audit trail".

## How to work with it (via the planwright MCP tools)

1. **Anchor to the repo first** with an explicit project ID (slug lookups fail until anchored). This is the #1 gotcha. Use `planwright_set_repo` with the repo name (e.g., `owner/repo`) or project ID.

2. **Read open objectives** using `planwright_list_objectives` to see what's available in each lane (backlog, scheduled, in_progress, acceptance, done).

3. **Claim one** using `planwright_claim_objective` — claiming locks it so parallel agents skip it. Only claim objectives in the `scheduled` lane.

4. **Decompose and plan** — break down the objective into steps, then post your plan using `planwright_append_plan`.

5. **Execute** — implement the changes in the codebase.

6. **Check in** — record your work:
   - Use `planwright_record_diff` to log commits/diffs
   - Use `planwright_submit_test_run` to record test results
   - Use `planwright_append_note` for progress updates

7. **Request acceptance** — when done, call `planwright_request_acceptance` to move the objective to the acceptance lane for human review.

8. **Take the next objective** — repeat from step 2.

## Common gotchas

- **Must call `planwright_set_repo` first** — all other tools fail without an anchored project.
- **Bugs go in the bug lane**, not the planning surface — use the bug tools, not objective tools.
- **The audit ledger records every change automatically** — surface the relevant entry when the user asks "who/what/when".

## Tool categories

**Session & context:** `planwright_set_repo`, `planwright_list_workspaces`, `planwright_list_projects`, `planwright_get_board_url`

**Objectives:** `planwright_list_objectives`, `planwright_get_objective`, `planwright_create_objective`, `planwright_update_objective`, `planwright_schedule_objective`, `planwright_claim_objective`, `planwright_check_alignment`

**Agent workflow:** `planwright_append_plan`, `planwright_record_diff`, `planwright_submit_test_run`, `planwright_request_acceptance`, `planwright_append_note`

**Initiatives:** `planwright_list_initiatives`, `planwright_create_initiative`, `planwright_update_initiative`, `planwright_delete_initiative`

**Bugs:** `planwright_list_my_bugs`

**Context files:** `planwright_list_context_files`, `planwright_get_context_file`, `planwright_push_context_file`

## Example conversation

User: "I have three Claude Code sessions working on different features. How do I make sure they don't step on each other?"

Agent: I'll set up PlanWright as your control plane. First, let me anchor to your repo and see the current objectives.

[Calls planwright_set_repo with the repo name]
[Calls planwright_list_objectives to show available work]

Each session should claim a different objective from the scheduled lane. Claiming locks it, so other agents will skip it and move to the next available objective. When an agent finishes, it requests acceptance and takes another.

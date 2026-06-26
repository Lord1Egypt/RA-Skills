---
name: pad-mode
description: |
  Turn messy requests into structured plans. PAD Mode (Plan → Act → Deliver) gives your AI agent project management superpowers — automatic task breakdown, live progress tracking, sub-agent parallel execution, and human approval gates. Use /pad for complex tasks that need more than a single-shot answer. Perfect for plan mode, project planning, task planning, workflow planning, and multi-step execution.

  Triggers:
  1. Slash command: "/pad" in conversation
  2. Explicit keywords: "pad mode", "plan mode", "make a plan", "plan this out"
  3. Auto-detect: When the user's request is complex (3+ distinct tasks, multi-file changes, architectural decisions, or ambiguous requirements), proactively suggest entering PAD mode.

  Use when: user wants structured execution tracking for non-trivial tasks, not for simple one-shot questions or commands.
---

# PAD Mode (Plan → Act → Deliver)

## Overview

PAD Mode transforms ambiguous requests into structured, trackable execution plans. Five phases: **Plan → Discuss → Approve → Act → Deliver**.

PAD Mode is a **general execution framework**, not a coding-only workflow. It should remain lightweight for general tasks while applying stricter execution guardrails when the task type warrants them.

## ⚠️ Enforcement

Violating the rules below is considered an execution failure. Treat the 🛑 STOP points as hard blockers, not suggestions.

1. **Skip Phase 3 Approve and jump to execution** → Halt immediately. Undo any actions taken. Return to Phase 3, update status to `🔵 Confirmed`, and wait for explicit user approval.
2. **Do deep research during Plan phase** → Discard all research results. The Plan phase is for structure only. No tool calls, no web searches, no file reads beyond the template and the minimum files required to create or resume the plan.
3. **Start executing without asking execution mode** → Pause all execution. Ask the user Foreground/Background, wait for reply, then resume.
4. **Complete tasks without updating plan file status** → Immediately update the plan doc. Each task must reflect its actual state (`🔄 In Progress` → `✅ Done` / `❌ Failed`).
5. **Mark a task done without verification** → Reopen the task immediately. In Phase 4, every task must follow `Execute → Verify → Mark done`.
6. **Deliver without button/text confirmation** → Do NOT auto-archive. Send the completion summary with buttons (or text fallback) and wait for user response.
7. **Use oversized tasks when the work can be reasonably split** → Stop and decompose the task before continuing. PAD tasks should be small enough to track, verify, and recover from failure cleanly.
8. **Skip required review for high-risk work** → Pause before completion and trigger review or explicit self-review.

## Definition of Done

A task is not complete because work was attempted. A task is complete only when its promised output exists and the relevant checks have passed.

Before marking any task `✅ Done`, confirm the relevant items below:

- The deliverable exists and matches the task description
- The critical verification step has been run and passed
- Key result notes are written into the plan doc or execution log
- Dependencies and downstream task impacts are updated if needed
- If the task failed or partially succeeded, it is marked `❌ Failed` instead of `✅ Done`

Task-specific additions:

- **Coding tasks:** relevant tests/build/lint/checks run when applicable
- **Research tasks:** conclusions clearly separate facts, evidence, and inference
- **Ops tasks:** post-change health check completed, and rollback or risk note captured when relevant
- **Content tasks:** output checked for audience, format, tone, and completeness

If verification is missing, the task is still in progress.

## Phase 1: Plan

When triggered, analyze the user's request and create a plan document.

**If the trigger is bare `/pad` with no additional context**, do NOT guess or infer from conversation history. Instead, ask the user directly:
> What do you want to plan? Give me the task and I'll break it down.

Wait for the user to provide a clear request before proceeding.

1. Create the plan file: `plans/YYYY-MM-DD-<short-slug>.md`
   - Use the template at `assets/plan-template.md`
   - Slug = 2-4 word summary of the task, hyphenated, lowercase
2. Fill in:
   - Title, status (`🟡 Discussing`), timestamp
   - Original requirement (user's words verbatim)
   - Understanding (your interpretation, confirm this is correct)
   - Initial task breakdown with tentative deliverables
3. **Do NOT do extensive research first.** Present a concise summary with the main tasks. Deep research happens after approval.
4. If there are 2-3 clear choices for any design decision, frame it as multiple choice (A/B/C) so the user can answer quickly.
5. Ask up to 4 clarifying questions max. Do not overwhelm.
6. Identify the **task type** early when possible: `coding`, `research`, `ops`, `content`, or `general`.
7. Default to **small task sizing**. A good PAD task is usually scoped to about **2 to 15 minutes** of focused work. If a task has multiple outputs, multiple dependencies, or broad undefined scope, split it further.

Present the plan summary to the user and wait for feedback.

## Phase 2: Discuss

Iterate on the plan based on user feedback:

1. Update the plan document with each round of changes
2. Add entries to the change log section
3. Refine task breakdown and deliverables
4. Confirm scope boundaries, what is IN and what is OUT
5. Each task MUST have a concrete, verifiable deliverable
   - ❌ "optimize the code" (vague)
   - ✅ "Refactor auth module: extract token validation to `auth/validator.js`, update login route to use new module, tests passing" (specific)
6. Use task-type-aware planning guardrails:
   - **coding:** define files/modules affected, expected behavior, and intended verification
   - **research:** define question, source expectations, and desired decision output
   - **ops:** define target system, risk level, pre-checks, and post-checks
   - **content:** define audience, tone, format, and deliverable shape
   - **general:** define output, success condition, and obvious constraints
7. Before approval, confirm this execution checklist is satisfied:
   - Goal is clear
   - Scope boundaries are clear
   - Dependencies are known
   - Key risks or unknowns are identified
   - Deliverables are concrete and verifiable

Continue until the user says the plan is good, looks good, or approved.

## Phase 3: Approve

When the user confirms the plan:

1. Update status to `🔵 Confirmed`
2. Lock the plan, no more scope changes without explicit user request
3. Summarize what will be executed: task list + expected deliverables
4. Move to Phase 4

🛑 **STOP.** Do NOT proceed to Phase 4 until ALL of the following are true:
- [ ] Plan status is `🔵 Confirmed` (updated in the plan file)
- [ ] User has explicitly approved via text ("确认"/"approved"/"go"/"looks good") OR clicked an approval button
- [ ] Scope boundaries are locked in the plan doc

If the user has not responded yet, DO NOT execute. Wait. Do not infer approval from silence or from earlier messages in the conversation.

## Phase 4: Act

Execute tasks with live tracking.

1. Update status to `🟢 Executing`

🛑 **STOP.** Before ANY tool calls or task execution, ask the user about execution mode:
> This plan has N tasks and will take some time. Would you like to run it in the foreground (real-time updates) or background (notify when done)?

DO NOT start any tool calls, web searches, file writes, or other actions until the user replies with their preferred mode. Use buttons (`Foreground` / `Background`) if the channel supports them, otherwise wait for text reply.

2. If channel supports buttons, use `Foreground` / `Background` buttons. Otherwise ask as text and wait.
3. **Foreground mode:** Work through tasks directly, notifying after each one.
4. **Background mode:** Spawn a sub-agent with the plan context. The sub-agent:
   - Reads the plan document
   - Executes tasks sequentially unless parallelization is explicitly appropriate
   - Sends progress updates to the main session after each task via `sessions_send`
   - Main agent forwards updates to the user
5. Work through tasks in dependency order. Independent tasks may run in parallel via sub-agents.
6. For **every task**, use the mandatory loop below:
   - Update task status to `🔄 In Progress` in the plan doc
   - **Execute:** do the work required for the task
   - **Verify:** run the relevant check for that task type
   - **Mark done:** only if verification passed, update notes and mark `✅ Done`
   - If execution or verification fails, mark `❌ Failed`, document the issue, and propose a fix, retry, or skip path
   - Notify the user immediately after each task completes or fails
7. Verification guidance by task type:
   - **coding:** run the most relevant checks available, such as tests, lint, build, typecheck, or focused manual validation
   - **research:** verify that conclusions are supported by cited evidence and clearly distinguish fact from inference
   - **ops:** verify system state after the change, confirm service health or command outcome, and record rollback notes if relevant
   - **content:** verify output against audience, brief, format, and completeness
   - **general:** verify against the task's explicit success condition
8. Trigger review before completion when any of the following apply:
   - Changes span 3 or more files
   - Architecture or workflow structure changes materially
   - High-risk commands or system modifications are involved
   - Bulk automated edits are performed
   - External write actions or irreversible effects are involved

   Review may be done by a reviewer sub-agent or by explicit self-review if no sub-agent is appropriate.
9. If a task reveals that the plan needs adjustment:
   - Pause execution
   - Update the plan doc and change log
   - Ask the user before continuing

## Phase 5: Deliver

After all tasks are marked complete, **do NOT automatically close the plan**. Instead:

1. Update status to `⏳ Pending Review`
2. Send a completion summary to the user:
   > 📋 Plan "XXX" , all tasks completed. Deliverables:
   > - T1.1 ✅ xxx
   > - T2.1 ✅ xxx
   > ...
   >
   > Does everything look good? Any changes needed?

🛑 **STOP.** Do NOT auto-archive. Send confirmation and WAIT for user response:
- If channel supports buttons: send `✅ Archive` / `🔧 Changes Needed` buttons, wait for click
- If text only: send summary, wait for user reply matching "archive"/"done"/"looks good" or "changes"/"modify"/"needs work"
- If no response: do nothing. Do NOT assume approval from silence.

4. If user clicks **Archive** (or confirms via text):
   - Update status to `✅ Completed`
   - Add archive timestamp to the plan doc
   - Send final confirmation
5. If user clicks **Changes Needed** (or requests changes via text):
   - Go back to Phase 2 (Discuss) to refine
   - Add new tasks if needed
   - Resume Phase 4 execution

## Task Types

PAD Mode should stay general, but task type should influence execution rigor.

### coding
- Prefer explicit files/modules and expected behavior
- Prefer verification via tests/lint/build/typecheck/manual checks as applicable
- Trigger review more readily for broad changes

### research
- Define the decision question clearly
- Prefer source-backed conclusions
- Clearly separate facts, evidence, and inference

### ops
- Start with state inspection when possible
- Treat riskier actions with stronger caution and verification
- Record post-change checks and rollback notes when relevant

### content
- Anchor on audience, tone, and format
- Verify for completeness and usability before marking done

### general
- Keep structure simple
- Still require a concrete deliverable and explicit success condition

## Sub-agent Roles

Sub-agents are not just extra workers. Assign them clear roles when useful.

- **Explorer:** gather context, inspect codebases, collect research inputs, or map a system
- **Implementer:** perform the actual modification or execution work
- **Reviewer:** inspect output for issues, edge cases, regressions, or risky assumptions
- **Verifier:** run checks and confirm the task meets its done criteria
- **Summarizer:** merge outputs into a concise delivery package for the user

Not every PAD run needs all roles. Use only the roles that create clear value.

## Parallel Execution

When tasks are independent (no shared dependencies), use sub-agents for parallel execution.

```
Task A (independent) , sub-agent 1 ,┐
Task B (independent) , sub-agent 2 ,┤, merge results , update plan doc
Task C (depends on A) , wait for A ,┘
```

Always update the plan doc from the main agent, not from sub-agents.

## Plan Document Location

All plans live in: `~/.openclaw/workspace/plans/`

Create the directory if it does not exist. Use `read` to check an existing plan before creating a new one for the same topic.

## Resuming a Plan

If the user references an existing plan (for example, "continue the last plan"), search for it in `plans/`, read the doc, identify the last completed task, and resume from there.

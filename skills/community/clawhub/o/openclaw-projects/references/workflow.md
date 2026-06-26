# Workflow Reference

Universal workflow for any project type managed under OpenClaw Projects. Read this when:
- Drafting the workflow section of PROJECT.md in Step 4
- Troubleshooting agent behavior during a sprint
- Explaining how the team should operate

---

## Table of Contents

- [Phase Overview](#phase-overview)
- [Phase 1: Intake](#phase-1-intake)
- [Phase 2: Planning](#phase-2-planning)
- [Phase 3: Execution](#phase-3-execution)
- [Phase 4: Review](#phase-4-review)
- [Phase 5: Operator Sign-off](#phase-5-operator-sign-off)
- [Phase 6: Close](#phase-6-close)
- [Escalation Rules](#escalation-rules)
- [Queue Message Format](#queue-message-format)
- [Agent Session Start Checklist](#agent-session-start-checklist)

---

## Phase Overview

```
idle → intake → planning → execution → close → idle
                                ↕
                              review
```

Each phase tracked in `project-lock.json`. Agents check this file before acting.
If current phase doesn't match the agent's intended action, the agent stops and posts to their relevant queue.

The phase names are universal across team types. The *content* of each phase is team-specific (see `references/team-archetypes.md`), but the structure is the same.

---

## Phase 1: Intake

**Owner:** Client-facing agent
**Lock phase:** `intake`
**Queue used:** `to-[feasibility-reviewer]-feasibility.md`

### Steps

1. Client-facing agent receives or drafts work intake (requirements, brief, request, lead — whatever the team type).
2. Client-facing agent creates a versioned spec file: `workspace/SPEC-v[N]-[YYYY-MM-DD].md`
   - Never overwrite — always increment version
   - Updates `SPEC-CURRENT.md` to reference this draft
   - Marks file: `STATUS: DRAFT — Under feasibility review`
3. Client-facing agent posts to feasibility queue:
   ```
   [date] [FROM: client-facing] [TO: feasibility-reviewer]
   New scope draft ready for feasibility review.
   File: workspace/SPEC-v[N]-[YYYY-MM-DD].md
   ---
   ```
4. Feasibility reviewer reads spec and reviews for the team-specific concerns. Examples:
   - **Software dev:** technical feasibility, architecture conflicts, ambiguities
   - **Marketing:** brand fit, channel feasibility, budget alignment
   - **Real estate:** pricing realism, market fit, compliance
   - **Whatever fits the team**
5. Reviewer posts numbered issues to feasibility queue:
   ```
   [date] [FROM: feasibility-reviewer] [TO: client-facing]
   Feasibility review complete. [N] issues to resolve before accepting.

   Issue 1: [title]
   [description, concrete impact, options if available]

   Issue 2: ...
   ---
   ```
6. Client-facing agent translates issues into client-friendly language and sends to client (via email skill if available, or via `to-operator.md` if not).
7. Client responds to each numbered issue:
   - **Accept as known outcome**
   - **Provide a solution** for reviewer to evaluate
   - **Descope** — remove the requirement
8. Client-facing agent logs response in `DECISIONS.md` with date.
9. If client proposes solution, reviewer evaluates. Loop repeats until all issues resolved.
10. When resolved:
    - Reviewer updates `SPEC-CURRENT.md`: `STATUS: ACCEPTED — [date] — [reviewer] + [client-facing]`
    - Client-facing agent logs final acceptance in `DECISIONS.md`
    - Client-facing agent updates `project-lock.json` → `phase: planning`

### Client No-Response Rule
- No response in [client_no_response_hours] → client-facing agent sends follow-up
- Still no response → client-facing agent posts to `to-operator.md`:
  ```
  [date] [FROM: client-facing] [TO: operator]
  Client has not responded to feasibility issues for [hours]h. Follow-up sent.
  Please engage client directly. Issues are in queues/to-[feasibility]-feasibility.md.
  ---
  ```
- Task moves to "Blocked" stage in task manager

---

## Phase 2: Planning

**Owner:** Feasibility reviewer
**Lock phase:** `planning`

### Steps

1. Reviewer writes `workspace/DELIVERABLES_GUIDE.md`:
   - Each numbered section = one task in the task manager
   - Detailed enough to execute without ambiguity
   - Approach-level, not full execution
   - References `KNOWN_ISSUES.md` items created from this guide
   - **If scope includes visual/media assets:** reviewer uses vision capability (if model supports it) to review them. Each task referencing a visual asset must include the asset filename so executors and QA can locate it.
2. Reviewer updates `KNOWN_ISSUES.md` with limitations accepted during intake.
3. Reviewer posts to client-facing agent's queue:
   ```
   [date] [FROM: feasibility-reviewer] [TO: client-facing]
   Deliverables guide ready. workspace/DELIVERABLES_GUIDE.md
   [N] tasks defined.
   ---
   ```
4. Client-facing agent reviews guide for completeness.
5. Client-facing agent creates tasks in task manager from guide:
   - One task per numbered section
   - Task description includes the relevant guide section
   - Tasks placed in first stage (Backlog or equivalent), assigned to appropriate roles
6. Client-facing agent posts to feasibility-reviewer's queue:
   ```
   [date] [FROM: client-facing] [TO: feasibility-reviewer]
   Sprint [N] open. [X] tasks created.
   ---
   ```
7. Client-facing agent updates `project-lock.json`:
   ```json
   {
     "phase": "execution",
     "sprint_id": "sprint-[N]",
     "sprint_opened": "[date]"
   }
   ```
8. Client-facing agent updates `STATE.md`.

---

## Phase 3: Execution

**Owner:** Executors (their assigned tasks)
**Escalation owner:** Feasibility reviewer
**Lock phase:** `execution`

### Executor Task Flow

1. Executor picks up assigned task → moves to "In Progress" stage in task manager.
2. Executor reads:
   - `workspace/DELIVERABLES_GUIDE.md` — relevant task section
   - `RUNBOOK.md` — project conventions
   - Their queue — pending messages
3. **If task references a visual/media asset:**
   - Executor switches to vision-capable model (if their config supports it)
   - Retrieves asset from task manager attachment (preferred) or workspace media folder
   - If asset cannot be retrieved → blocker, escalate to feasibility reviewer
4. Executor produces the deliverable in the shared working medium.
5. When complete:
   - **Software dev:** push to sprint branch; first task opens PR, subsequent push updates PR
   - **Marketing/content:** save to shared drive in approved location
   - **Real estate:** update CRM with completion details
   - **Whatever fits the medium**
   - Move task from "In Progress" → "In Review" stage
   - Post to QA's queue:
     ```
     [date] [FROM: executor] [TO: qa] [TASK: task-id]
     Task [id] complete. [Pointer to deliverable — PR URL, file path, etc.]
     What was produced: [brief description]
     ---
     ```
6. Executor moves to next task if available.

### Executor Escalation Rules

**When blocked:**
- Post to feasibility reviewer's queue with task ID, what was tried, specific question
- Reviewer responds in executor's queue
- Executor waits for response

**Hard stop rule — triggers when EITHER condition is met:**
- Same issue escalated [stuck_re_escalations_threshold] times to reviewer without resolution, OR
- Executor stuck on same issue for [stuck_hours_threshold] hours

**When hard stop triggers:**
1. Executor stops work on that task immediately
2. Executor posts full summary to client-facing agent's queue:
   ```
   [date] [FROM: executor] [TO: client-facing] [TASK: task-id]
   HARD STOP — escalation limit reached.
   Issue: [description]
   Escalation history:
     [date] — First escalation: [question]
     [date] — Reviewer response: [response]
     [date] — Second escalation: [question]
     [date] — Reviewer response: [response]
   Still blocked because: [reason]
   Awaiting operator assistance before resuming.
   ---
   ```
3. Task moves to "Blocked" in task manager
4. Client-facing agent posts to `to-operator.md`
5. **No further AI cycles spent on this task until operator resolves**

---

## Phase 4: Review

**Owner:** QA reviewer
**Lock phase:** `execution` (review runs concurrently with ongoing execution)

### QA Flow

1. QA picks up task from "In Review" stage → moves to "QA" or "Review" stage.
2. QA reads:
   - `KNOWN_ISSUES.md` — do not file failures against accepted limitations
   - `workspace/SPEC-CURRENT.md` — accepted scope
   - `workspace/DELIVERABLES_GUIDE.md` — planned approach for this task
3. **If deliverable includes visual output and task references a mockup:**
   - QA uses vision (if model supports) to compare output to reference
   - Visual deviations not in `KNOWN_ISSUES.md` are failures
4. QA reviews deliverable against all references.

### QA Pass
```
[date] [FROM: qa] [TO: operator] [TASK: task-id]
Task [id] — REVIEW PASSED.
Deliverable: [pointer]
Verified against: SPEC-CURRENT.md + DELIVERABLES_GUIDE.md task [N]
No known issues flagged.
---
```
- Move task to "Completed" stage

### QA Fail
```
[date] [FROM: qa] [TO: feasibility-reviewer] [TASK: task-id]
Task [id] — REVIEW FAILED. [N] issues found.

Issue 1: [specific — what was checked, what was expected, what happened]
Issue 2: ...
---
```
- Move task back to "In Progress"
- Executor addresses failures and re-submits
- QA re-reviews

---

## Phase 5: Operator Sign-off

**Owner:** Operator (human, if defined)
**Lock phase:** `close` (after sign-off)

### Flow

1. Operator reviews `to-operator.md` for QA-passed tasks.
2. Operator validates the deliverable:
   - **Software dev:** pull branch, review, test
   - **Marketing/content:** read the deliverable
   - **Real estate:** verify listing data
   - **Whatever fits**
3. If satisfied:
   - **Software dev:** tells QA to merge to main; rebases other repos
   - **Other:** approves delivery to client through whatever channel applies
4. Operator updates `project-lock.json` → `phase: close`.

### If no operator (rare)
QA's pass message is the sign-off. Move directly to close phase.

---

## Phase 6: Close

**Owner:** Client-facing agent
**Lock phase:** `idle` (after close)

### Close Checklist

1. Verify all sprint tasks are in "Completed" stage in task manager.
2. Archive completed tasks (close/archive — do not delete).
3. Verify `DECISIONS.md` has complete record for this sprint.
4. Verify `KNOWN_ISSUES.md` is current.
5. Write sprint summary to `SHARED_MEMORY.md`:
   ```markdown
   ## [date] Sprint [N] Close — [client-facing-agent]
   What was delivered: [summary]
   Issues accepted: [reference to KNOWN_ISSUES entries]
   Client sign-off: [yes/no — how confirmed]
   Carry-over notes: [anything for next sprint]
   ```
6. Update `STATE.md`:
   ```markdown
   # [Project Name] — Current State
   **Phase:** Idle — Sprint [N] closed. Ready for next intake.
   ```
7. Archive queue entries (mark `[READ]`, do not delete).
8. Update `project-lock.json`:
   ```json
   {
     "phase": "idle",
     "sprint_id": null,
     "sprint_opened": null,
     "waiting_on": null,
     "context": "Sprint [N] closed. Ready for next intake."
   }
   ```
9. Post to operator's queue: "Sprint [N] closed. Ready for next intake."

**One sprint at a time mode:** Client-facing agent does not accept new intake until `project-lock.json` is `idle`.

**Continuous flow mode:** Client-facing agent can accept new intake immediately. Each piece of work flows through phases independently. Sprint close still happens for periodic cleanup, but new intake doesn't wait for it.

---

## Escalation Rules

| Situation | Action | Threshold |
|---|---|---|
| Client not responding to scope | Client-facing follows up; then escalates to operator | client_no_response_hours |
| Executor blocked on task | Escalate to feasibility reviewer | Immediately when blocked |
| Same issue re-escalated to reviewer | Hard stop; client-facing escalates to operator | stuck_re_escalations_threshold |
| Executor stuck same issue | Hard stop; client-facing escalates to operator | stuck_hours_threshold |
| Task in Blocked with no movement | Client-facing escalates to operator | blocked_task_operator_escalation_hours |
| QA failing same task repeatedly | QA posts to reviewer; client-facing monitors | — |

**No agent continues spending AI cycles on a blocked path. Stop, surface, wait.**

---

## Queue Message Format

Every queue entry must use this exact format:

```
[YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: task-id or N/A]
Message body. Be specific. Include task IDs, file references, error messages.
If multiple items, number them clearly.
---
```

### Rules
- Queues are append-only — never delete entries
- Mark processed entries by prepending `[READ]` — do not remove the line
- Archive at sprint close (mark READ, leave in place)
- Each agent checks their queue at session start, before any other action
- Feasibility queue is **only** used during intake phase

---

## Agent Session Start Checklist

Every agent runs this at the start of every session:

1. Read `project-lock.json` for each project they're on — what phase is each in?
2. Read `queues/to-[my-role].md` for each project — any pending messages?
3. If unread queue messages exist, address them before starting new work
4. If phase doesn't match my expected action, post to relevant queue and wait
5. If phase matches and no pending messages, proceed with current task

**Queue and phase check always come before anything else.**

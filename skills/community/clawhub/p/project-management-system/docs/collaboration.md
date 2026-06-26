# Collaboration and Communication Mechanism

> Reporting, confirmation, feedback, notification, status discipline, dispatch tools.

---

## Reporting Mechanism

| Scenario | Action |
|------|------|
| Daily scheduling (dispatch, chase progress) | Dispatcher decides autonomously |
| Review conclusion (pass/rework) | Dispatcher decides autonomously |
| Project initiation | Report to Decision Maker for approval |
| Directional choice / Major change | Report to Decision Maker for decision |
| Milestone complete | Report to Decision Maker for awareness |
| Final Acceptance | Report to Decision Maker for decision |

## Requirement Confirmation Mechanism

- After project initiation, before starting work, must repeatedly confirm requirements with Decision Maker
- brief.md has "Requirement Confirmation Record" table, recording each round of confirmation
- Decision Maker explicitly says "can start" before entering breakdown
- Unclear parts of requirements ask proactively, don't guess

**Confirmation Content:** Goal understanding, scope boundary, acceptance criteria, implicit preferences/constraints.

## Intermediate Output Confirmation Mechanism

Outputs involving subjective judgment (aesthetics, style, precision, etc.), Dispatcher cannot substitute Decision Maker's judgment.

**Rules:**
- task-spec has "User Confirmation Point" field
- Involving subjective judgment → Submit to Decision Maker using confirmation-record
- Confirmation not passed → Record feedback, adjust and resubmit

**Key Principle: Better to confirm once more than find direction wrong after completion.**

## Executor Reverse Feedback Mechanism

When executor discovers the following situations, should proactively feedback to Dispatcher:
1. Prerequisite task output has problems
2. Spec requirements are infeasible or ambiguous
3. Discovered risks not mentioned in spec
4. Expected unable to complete on time
5. Need additional input or permissions
6. **Discovered new requirements/opportunities** — During execution discovered "this project should also do X", but X is not in current task

**After Dispatcher receives feedback:**
- Prerequisite has problems → Reopen to fix
- Has ambiguity → Clarify and update spec
- New risk → Update risk register
- Cannot complete on time → Adjust deadline or change plan
- Need additional input → Provide or escalate

## Spec Update Notification

- After modifying spec must notify executor
- Notification content: What changed, why changed, impact on execution
- Major modification → Executor confirms receipt before continuing
- Record in communication record

## Decision Maker Final Veto Power

- Decision Maker can veto any accepted task and completed project
- After veto, handle according to change request or rework process
- To reduce veto: Key outputs first go through intermediate output confirmation

## Status Update Discipline

Each status change must immediately update status field and status tracking table in task-spec.

| Status Change | Trigger Point | Who Updates |
|----------|--------|--------|
| Pending Dispatch → In Progress | At dispatch | Dispatcher |
| In Progress → Blocked | Executor reports block | Dispatcher |
| Blocked → In Progress | Block resolved | Dispatcher |
| In Progress → Pending Review | At executor delivery | Dispatcher |
| Pending Review → Rework | Review not passed | Dispatcher |
| Rework → Pending Review | Executor resubmits | Dispatcher |
| Pending Review → Accepted | Review passed | Dispatcher |
| In Progress → Paused | Project paused | Dispatcher |
| Paused → In Progress | Project resumed | Dispatcher |
| Any → Cancelled | Project cancelled | Dispatcher |
| Any → Abandoned | When changing plan | Dispatcher |

## Dispatcher Does Not Execute Personally

- Dispatcher responsible for planning, breakdown, dispatch, review, acceptance
- Specific execution must be dispatched to executor
- Only exception: Extremely simple tasks (like changing one line of config), mark "self-executed" in status tracking

## Dispatch Tool Usage Standard

Dispatcher dispatches tasks through currently available tools and tracks communication.

**General Process (Platform Independent):**
1. Select tool → Check currently available communication tools in `resource-profiles.md`
2. Send dispatch message → Follow message format in `communication.md`
3. Record communication identifier → Write to task-spec communication record (Thread ID, session identifier, etc.)
4. Subsequent tracking → Continue communication through same identifier

**Specific tool call methods are recorded in "Current Communication Infrastructure" in `resource-profiles.md`.**

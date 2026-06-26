# Task Specification Template

> Copy this file to project's `tasks/` directory, name as `TASK-XXX-brief.md`.
> This is agent's work instruction file — Can work upon receiving, no extra communication needed.

---

## Basic Information

- **Task ID:** TASK-XXX
- **Project:**
- **Assigned to:** _(Runtime decision: agent name / subagent / coding-agent / self-execute)_\n- **Created time:**
- **Estimated time:** _e.g., 30min / 2h / 1 day_
- **Deadline:**
- **Priority:** High / Medium / Low
- **Milestone:** _(Large project fill, e.g., M1/M2/M3; small project leave blank)_\n- **Status:** Pending Dispatch / In Progress / Blocked / Pending Review / Rework / Accepted / Abandoned / Paused / Cancelled

## Task Objective

_One sentence clarify what to do._

## Background

_Why do this task? What's its position in project?_

## Specific Requirements

_Detailed description of what to do, as specific as possible. Agent executes per this._

1.
2.
3.

## Input

_What prerequisites, files, info needed to execute this task?_

| Input | Location/Source | Notes |
|------|-----------|------|
| | | |

## Output

_What should be produced after task completion? Where to put?_

| Output | Storage location | Format requirement |
|------|----------|----------|
| | | |

_⚠️ Output location must be under `/path/to/projects-data/[project-name]\`, cannot write to `system/` directory._

## Acceptance Criteria

_List item by item, Dispatcher checks per this. All pass counts as complete._
_Quantify as much as possible: ❌"clear format" → ✅"JSON format, contains name/value/timestamp fields"_\n_Non-quantifiable subjective criteria (aesthetic, style etc.) → Put in "User Confirmation Points" for Decision Maker to judge_

- [ ]
- [ ]
- [ ]

## Notes

_Special constraints, known pitfalls, practices to avoid._

-

## Related Context (Check as Needed)

_Executor doesn't need to pre-read all info. Only look up via pointer when needed. (See docs/knowledge.md progressive information disclosure)_\n\n| Topic | Location | When needed |
|------|------|----------|
| Project overall objective | brief.md | When need understand big picture |
| | | |

_No extra context then leave blank._

## User Confirmation Points

_Which intermediate outputs need Decision Maker review before proceeding? Dispatcher can't replace subjective judgment (aesthetic, style, precision, voice, image etc.) must list here._

| # | Confirmation point | Output form | When confirm | Status |
|------|--------|----------|----------|------|
| 1 | | _Screenshot/audio/file/text description_ | _After XX completed_ | Pending / Confirmed / Needs adjustment |
| | | | | |

_Tasks without user confirmation leave blank. Confirmation fails then record feedback, adjust then resubmit for confirmation._

## Dependency Relationship

_Which predecessor tasks does this task depend on? Which successor tasks depend on this task?_

| Direction | Task ID | Dependency content | Status |
|------|----------|----------|------|
| Predecessor (I depend on) | | _What output needed to start_ | Ready / Not ready |
| Successor (depends on me) | | _My output needed by whom_ | |

_No dependency then leave blank. Dispatcher dispatches tasks in dependency order._

## Interface Agreement

_This task's boundary with other tasks. Dispatcher defines at breakdown, ensuring each task outputs can seamlessly connect._

| Counterpart | Interface content | Agreement (format/spec/protocol) |
|--------|---------|----------------------|
| _Me→Whom_ | _How my output used by them_ | _e.g., REST API, path /api/xxx, return JSON {field: type}_ |
| _Whom→Me_ | _How their output used by me_ | _e.g., read xxx.json, expect fields [a, b, c]_ |

_No interface then leave blank. Has interface then must write clearly, both develop per this agreement, review time check alignment._

## Delivery Confirmation

_Executor must fill before delivery. Dispatcher checks at review._

| Check item | Pass? | Notes |
|--------|--------|------|
| Re-read task objective and acceptance criteria | ✅/❌ | _One sentence confirm whether met_ |
| Output at specified location | ✅/❌ | |
| Format meets requirement | ✅/❌ | |
| Quantified metrics achieved (if any) | ✅/❌/N/A | |
| Code can run (if any) | ✅/❌/N/A | |
| Missed requirements (check task-spec) | ✅/❌ | _No misses = ✅_ |

_All ✅ then can deliver. Has ❌ must fix first._

## Status Tracking

| Time | Status change | Notes |
|------|----------|------|
| | Pending Dispatch | Task created |
| | | |

## Communication Record

_Communication with executor (dispatch, push progress, feedback, etc.). Ensures Dispatcher restart then can reconnect context._

| Time | Direction | Thread | Content summary | Communication identifier |
|------|------|--------|----------|----------|
| | Dispatcher→Executor | | | |
| | Executor→Dispatcher | | | |
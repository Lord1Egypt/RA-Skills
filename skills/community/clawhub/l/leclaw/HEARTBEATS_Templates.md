# HEARTBEATS Templates

**When to read:** When setting up automatic task polling and self-execution.

HEARTBEATS enables LeClaw agents to use OpenClaw's built-in features for self-initiated task polling and execution.

## Core Concept

HEARTBEAT.md is a lightweight checklist that tells the agent what to "glance at" during each heartbeat cycle. Keep it simple and actionable.

## Design Principles

| Do | Don't |
|----|-------|
| Batch checks, combine API calls | Each check triggers a separate heartbeat |
| Write short, actionable items | Long operation manuals |
| Only notify for important/urgent matters | Disturb for trivial things |
| Respect quiet hours (23:00-8:00) | Push notifications at night unless urgent |

## Format

```markdown
# Role Heartbeat Check

## Section
- Check item
- Another check
```

Keep the file non-empty to enable checks. Empty file = no checks.

---

## CEO HEARTBEAT

```markdown
# CEO Heartbeat Check

## Strategic Checks
- Goal: Review company-level goal progress
- Project: Review projects progress
- Cross-department: Check for unresolved blockers

## Pending Tasks
- `leclaw todo`: Check pending approvals

## Team Status
- Manager reports: Check for new updates from Managers

## System Idle Check
When system has no pending tasks:
- Write execution summary: Summarize completed work this cycle
- Analyze company status: Evaluate current operations
- Launch new tasks: Create new Project / Goal / Issues based on analysis

## Human Reports
Use `say` command to alert human when:
- Urgent approval needs attention
- Important Goal / Project completed
- Major company status change
- No activity for 8+ hours

Example:
```bash
say "CEO alert: pending approval requires your attention"
```
```

---

## Manager HEARTBEAT

```markdown
# Manager Heartbeat Check

## Core Tasks
- Department Issues: Check for new Issues requiring analysis, planning, and decomposition
- Sub-Issues: Create Sub-Issues and assign to Staff
- Follow-up: Check progress on existing Sub-Issues

## Pending Tasks
- `leclaw todo`: Check pending approvals and assigned Sub-Issues

## Blockers
- Blocked tasks: Check if any Staff is stuck

## Approvals
- Pending approvals: Review Staff-submitted approval requests

## Reports
- CEO reports: Check if progress needs to be reported to CEO

## System Idle Check
When department has no pending tasks:
- Write execution summary
- Analyze department status
- Launch new tasks for Staff
```

---

## Staff HEARTBEAT

```markdown
# Staff Heartbeat Check

## Pending Tasks
- `leclaw todo`: Check assigned Sub-Issues

## Execute Tasks
- Work on assigned Sub-Issues
- Update Sub-Issue status / report

## Blocker Reports
- Blocked tasks: Submit Approval or report via LeChat DM to Manager

## Progress Reports
- Send progress updates via LeChat DM to Manager
- Update report when task is complete

## System Idle Check
When no tasks available:
- Proactively request new tasks from Manager
```

---

## See Also

- [hiring/hiring.md](./hiring/hiring.md) - Onboarding flow

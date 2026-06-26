# Scheduling and Resource Management

> Resource allocation, priority, exception handling, urgent tasks, capability profiles.

---

## Dynamic Resource Allocation

**Core Principle: Roles not fixed, resources dynamically allocated.**

Each time dispatching task, decide who does it based on currently available resources, don't preset fixed division of labor.

**Selection Basis:**
- Task complexity and independence
- Currently available communication channels
- Executor capability match (refer to `resource-profiles.md`)
- Cost-effectiveness (token consumption, time)

## Priority Scheduling

- Project-level priority marked in brief.md (High/Medium/Low)
- Task-level priority marked in task-spec (High/Medium/Low)
- Same priority sorted by dependency
- Resource conflict, high priority first

| Situation | Handling Method |
|------|----------|
| High priority arrives | Pause low priority tasks |
| Multiple high priority parallel | No dependencies dispatch in parallel |
| Insufficient resources | Report to Decision Maker |
| Urgent task insertion | Respond immediately, pause current work if necessary |

## Exception Handling and Escalation

| Exception | Detection Method | Handling |
|------|----------|------|
| Execution timeout | Past deadline | Check progress → No response then redispatch |
| Executor unreachable | No response | Wait reasonable time → Redispatch or change executor |
| Task stuck | Executor reports | Analyze reason → Adjust/change plan/escalate |
| Quality consistently not meeting standard | Rework over 3 times | Escalate to Decision Maker |
| Dependency blocked | Prerequisite delayed | Assess if can parallel → Adjust → Report |
| Resource unavailable | Tool failure | Change execution method → Report |

**Escalation Path:**
```
Handle autonomously → Report for awareness → Ask Decision Maker for decision → Decision Maker directly intervenes
```

**Principle:** Solve small problems yourself, escalate big problems promptly. Don't try in dead end more than 3 times.

## Urgent Task Fast Track

**Trigger Condition:** Decision Maker explicitly states urgent.

**Rules:**
- Skip project initiation, directly write task-spec and dispatch
- Skip requirement confirmation (urgent instruction itself is confirmation)
- Review can be simplified but not skipped
- **Post-completion documentation is mandatory** (see checklist below)
- Quality gates still effective

**Post-Completion Documentation Checklist (Within 24 hours after urgent task completion):**
- [ ] Write brief.md (if project initiation was skipped)
- [ ] Is task-spec acceptance criteria complete? If not, add
- [ ] Is review-record created? Simplified review still needs record
- [ ] Is communication record complete?
- [ ] Is data_structure.md index updated?
- [ ] Write to Heartbeat to remind "check urgent task XXX's documentation"

**Who Ensures:** After urgent task completion, Dispatcher writes "document completion" as independent pending item to Heartbeat. Auto-reminder at next heartbeat.

**Limitation:** Fast track is not normal. Frequent use indicates process problems.

## Urgent Task Conflict with In-Progress Tasks

- Urgent task priority above all non-urgent tasks
- Need same executor: Assess in-progress task status — Almost done then wait, just started then pause
- Can change executor: Prioritize changing person, don't interrupt in-progress task
- After urgent task complete, immediately resume paused task

## Parallel Resource Conflict Detection

- Before dispatch check if target executor has in-progress tasks
- Has conflict: High priority first, same priority first-come-first-served
- Same executor maximum 2 in-progress tasks

## Resource Capability Profile

System-level capability profile in `resource-profiles.md`, records execution resources' strengths, weaknesses, and suitable task types.

**Maintenance Rules:**
- Initial profile built based on known information
- Update after each project ends based on actual performance
- Reference when assigning tasks, but not hard constraint

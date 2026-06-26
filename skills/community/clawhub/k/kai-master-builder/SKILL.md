---
name: kai-master-builder
description: Developer, Code, Engineer. Guide the Agent to build apps/features/goals efficiently and securely. Creates project plans, task lists, and provides building prompts. Can run autonomously via cron or user-driven.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Kai Master Builder

Build anything efficiently with structured plans and automated execution.

## When to Use

- User wants to build a new app/feature/fix
- Need structured approach to complex project
- Want automated building via cron
- Need to track progress across sessions

## The Process

### Phase 1: Create Project Plan

**Input:** GOAL (what to build/improve/fix)

**Output:** `PROJECT/PROJECT_PLAN.md`

```
# Project Plan: [PROJECT_NAME]

## Overview
What this project does and why.

## Goals
- Primary goal
- Secondary goals

## Architecture/Approach
How it will be built.

## Security Checklist
- [ ] No API keys hardcoded (use env vars)
- [ ] No .env loading in scripts
- [ ] All secrets in config, not code
- [ ] Input validation
- [ ] Error handling

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | ... | ... |

## Dependencies
- External: ...
- Internal: ...

## Milestones
1. [ ] Phase 1: ...
2. [ ] Phase 2: ...
3. [ ] Phase 3: ...

## Validation
How to test/validate each milestone.
```

### Phase 2: Create Task List

**Output:** `PROJECT/PROJECT_TASKS.md`

```
# Tasks for: [PROJECT_NAME]

## Task Format
- [ ] TASK_NAME | status: TODO | depends: none | validated_by: test command

## Tasks

### Phase 1: Setup
- [ ] Create project structure | status: TODO | depends: none | validated_by: ls project/
- [ ] Setup dependencies | status: TODO | depends: 1 | validated_by: pip list / npm list

### Phase 2: Core Feature
- [ ] Implement X | status: TODO | depends: 1 | validated_by: python3 test_x.py

### Phase 3: Testing & Polish
- [ ] Write tests | status: TODO | depends: 2 | validated_by: pytest
- [ ] Update docs | status: TODO | depends: 2 | validated_by: doc builds

## Blocked
- Task X: waiting on external API access

## Done
(Completed tasks move here with timestamp)
```

### Phase 3: Build!

**Prompt provided to Agent/User:**

---
## BUILDER PROMPT

You are building: **[PROJECT_NAME]**

**Context:**
- Read `PROJECT/PROJECT_PLAN.md` for architecture and goals
- Read `PROJECT/PROJECT_TASKS.md` for task list
- Follow the iteration loop below

**Iteration Loop:**

1. **Pick a task** - Choose TODO task whose dependencies are all DONE
2. **Implement it** - Write the code
3. **Test it** - Run validation command
4. **Document** - Update CHANGELOG.md with what you built
5. **Mark DONE** - Update TASKS.md, move to Done section with timestamp
6. **Report** - Report back to main session

**If blocked:**
- Mark task as BLOCKED with reason
- Report what you need to proceed

**When all tasks done:**
- Report: "PROJECT is DONE! Built with kai-master-builder."
- Update PROJECT_README.md with final state

---

## Automation

Setup cron for autonomous building:
```
/call_skill kai-master-builder --build PROJECT_NAME
```

Or let Agent run it via sessions_spawn with this prompt.

## Project Folder Structure

```
PROJECT/
├── PROJECT_PLAN.md      # Architecture and goals
├── PROJECT_TASKS.md     # Task list with status
├── PROJECT_CHANGELOG.md # What was built
├── PROJECT_README.md    # Documentation
└── src/                 # Source code
```

## Tips

- Break big tasks into < 1 hour chunks
- Every task should have clear validation
- Mark tasks BLOCKED if waiting on something
- Update CHANGELOG after each task
- Backup TASKS.md before modifying

---

*kai-master-builder: Turn goals into working code*

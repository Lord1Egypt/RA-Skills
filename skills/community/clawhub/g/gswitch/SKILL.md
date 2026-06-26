# GSwitch - OpenClaw Multi-Agent Coordination System

**Inspired by Garry Tan's GStack, adapted for OpenClaw**

## Concept

GSwitch turns OpenClaw into a virtual engineering team with 7 specialized roles working in a coordinated workflow.

## Core Philosophy

> "Skill feeds into the next. Nothing falls through the cracks because every step knows what came before."

**Workflow:** Think → Plan → Build → Review → Test → Ship → Reflect

---

## The 7 Roles

| Role | ID | Primary Function |
|------|-----|------------------|
| CEO | {username}-ceo (Main) | Rethink problems, set direction |
| Engineering Manager | {username}-em | Architecture, technical decisions |
| Designer | {username}-designer | UI/UX, catch AI slop |
| Reviewer | {username}-reviewer | Code review, find bugs |
| QA Lead | {username}-qa | Real browser testing |
| Security Officer | {username}-security | OWASP + STRIDE audits |
| Release Engineer | {username}-release | Deploy, PR management |

**Note:** Replace `{username}` with your own username when installing.

---

## Shared Memory

All agents share: `/path/to/GSwitch/shared-memory/{username}/`

**Format:** YYYY-MM-DD.md
**Rule:** APPEND ONLY, NEVER OVERWRITE

---

## Configuration

```json
{
  "maxSpawnDepth": 5,
  "runTimeoutSeconds": 0,
  "sharedMemory": "/path/to/GSwitch/shared-memory/{username}/"
}
```

---

## Workflow Sequence

### Phase 1: Think (CEO)
- `/office-hours` - Understand the problem deeply
- Output: Design document

### Phase 2: Plan (CEO + EM + Designer)
- `/plan-ceo-review` - CEO reviews problem framing
- `/plan-eng-review` - EM reviews architecture
- `/plan-design-review` - Designer reviews UI/UX

### Phase 3: Build (EM/Coder)
- Implement based on approved plan
- Write to shared memory on completion

### Phase 4: Review (Reviewer)
- `/review` - Code review, find bugs
- Spawn related agent to fix if issues found

### Phase 5: Test (QA)
- `/qa` - Real browser testing
- Identify issue type → spawn related agent to fix

### Phase 6: Ship (Release)
- `/ship` - Deploy to production
- QA passed before deploy

### Phase 7: Reflect (All)
- `/retro` - Document learnings
- Update shared memory

---

## Coordination Rules - IMPORTANT

### Core Principle
**Each agent ONLY does their own job. NEVER do others' work. Send tasks to the right department.**

### Each Role Has Own Responsibility

| Role | Responsibility |
|------|----------------|
| EM | Code, Architecture, Technical |
| Designer | Design, UI/UX, Content |
| Reviewer | Code Review |
| QA | Testing, Final Gate |
| Security | Security Audit |
| Release | Deployment |

### When Finding Issues

| Issue Type | Send To |
|------------|---------|
| Code/Technical | → EM |
| Design/UI/UX | → Designer |
| Security | → Security |
| Multiple types | → All relevant agents |

### After Completion

1. Write to shared memory (INCLUDE file paths!)
2. Spawn next agent for workflow
3. If issues found → spawn related agent to fix
4. QA is the FINAL gate before Release

---

## Shared Memory Format

Each agent appends:

```markdown
### {username}-role | HH:MM
- 任務：[Task description]
- 結果：[Success/Failure]
- 發現：[Issues if any]
- 檔案位置：[Project file path]
- 下一步：[Next step]
---
```

---

## Installation

1. Copy GSwitch folder to your OpenClaw workspace
2. Replace `{username}` with your username in all files
3. Create agents with IDs: `{username}-em`, `{username}-designer`, etc.
4. Set shared memory path in agent configs

---

*Inspired by Garry Tan's GStack*
*GSwitch for OpenClaw*

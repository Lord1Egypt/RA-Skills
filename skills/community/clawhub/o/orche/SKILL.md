---
name: orche
version: 1.0.0
author: reikys
description: "A multi-agent orchestration engine that systematically executes complex tasks in 4 phases (Query → Plan → Execute → Verify). Ensures high-quality deliverables through phase gates, Critic debates, 14-item hallucination checks, and automatic regression on verification failure."
license: MIT
tags:
  - orchestration
  - multi-agent
  - planning
  - verification
  - hallucination-check
metadata:
  openclaw:
    emoji: "🎼"
    triggerPhrases:
      - "/orche"
      - "orchestrate"
      - "orchestration"
      - "systematic execution"
      - "multi-phase"
      - "multi-agent execution"
---

# 🎼 Orche — Multi-Phase Orchestration Engine

> A multi-agent orchestration engine that executes complex tasks in **Query → Plan (Debate) → Execute → Verify** — 4 phases.
> A sub-agent panel debates, critiques, executes, and verifies, while the watchdog monitors the entire process.

---

## 📌 Table of Contents

1. [Why Orche?](#-why-orche)
2. [Comparison with Existing Orchestration Skills](#-comparison-with-existing-orchestration-skills)
3. [Quick Start — First Orchestration in 5 Minutes](#-quick-start--first-orchestration-in-5-minutes)
4. [Phase Overview](#-phase-overview)
5. [Phase 0: Query](#phase-0-query)
6. [Phase 1: Planning](#phase-1-planning)
7. [Phase 2: Execution](#phase-2-execution)
8. [Phase 3: Verification](#phase-3-verification)
9. [State Management](#-state-management)
10. [Directory Structure](#-directory-structure)
11. [Harness Rules (Safety Mechanisms)](#-harness-rules-safety-mechanisms)
12. [Watchdog Integration](#-watchdog-integration)
13. [Hallucination Checklist (14 Items)](#-hallucination-checklist-14-items)
14. [Cost Management](#-cost-management)
15. [Exception Handling Summary](#-exception-handling-summary)
16. [User Intervention Points](#-user-intervention-points)
17. [Abort Procedure](#-abort-procedure)
18. [Session Disconnection Recovery](#-session-disconnection-recovery)
19. [Demo Scenarios](#-demo-scenarios)
20. [Production Run Records](#-production-run-records)
21. [hallucination-guard Integration](#-hallucination-guard-integration)
22. [Advanced Configuration](#-advanced-configuration)
23. [FAQ](#-faq)
24. [Changelog](#-changelog)

---

## 🎯 Why Orche?

### Problem: Limitations of Existing Multi-Agent Execution

When complex tasks are delegated to AI agents, the following problems arise:

| Problem | Symptom | Result |
|---------|---------|--------|
| **Hallucination** | Uses non-existent APIs/libraries | Non-executable code |
| **Execution without planning** | Starts writing code immediately | Direction change costs explode |
| **No verification** | Deliverables "look plausible" | Don't actually work |
| **Linear-only progression** | Keeps going forward even on failure | Root cause unresolved |
| **Cost explosion** | Indiscriminate agent deployment | Budget exhaustion |

### Solution: Orche's 4-Phase Engine

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Phase 0        Phase 1         Phase 2        Phase 3     │
│   ┌──────┐      ┌──────┐       ┌──────┐      ┌──────┐     │
│   │Query │─G0─▶│ Plan  │──G1─▶│Execute│─G2─▶│Verify│     │
│   │      │      │(Debate)│      │(Parall)│      │      │     │
│   └──────┘      └──────┘       └──────┘      └──┬───┘     │
│       │                             ▲            │         │
│       │                             │          fail?       │
│       │                             └──── YES ◀──┘         │
│       │                                                     │
│       └── Watchdog monitors the entire process ───────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Differentiators:**
- ✅ **Phase Gates**: Explicit condition fulfillment required at each phase transition
- ✅ **Critic Debate**: Advocate vs Critic debate improves plan quality
- ✅ **14-Item Hallucination Check**: Fact, consistency, completeness, and hallucination pattern verification
- ✅ **Auto Regression**: Automatically returns to Phase 2 on verification failure
- ✅ **Watchdog Integration**: Monitors entire process, auto-detects deadlocks/loss/budget overruns
- ✅ **Cost Management**: 4-tier budget alerts + concurrent agent limit

---

## 📊 Comparison with Existing Orchestration Skills

| Feature | `dispatching-parallel-agents` | `parallel-agent-management` | `executing-plans` | **`orche`** |
|---------|:---:|:---:|:---:|:---:|
| **Parallel execution** | ✅ | ✅ | ❌ (sequential) | ✅ |
| **Pre-query phase** | ❌ | ❌ | ❌ | ✅ Phase 0 |
| **Debate/discussion** | ❌ | ❌ | ❌ | ✅ Includes Critic |
| **Phase gates** | ❌ | ❌ | ✅ (checkpoints) | ✅ 4 gates |
| **Hallucination check** | ❌ | ❌ | ❌ | ✅ 14 items |
| **Auto regression on verification failure** | ❌ | ❌ | ❌ | ✅ Up to 3 retries |
| **Watchdog integration** | ❌ | ❌ | ❌ | ✅ |
| **Cost management** | ❌ | ❌ | ❌ | ✅ 4-tier budget |
| **Session disconnection recovery** | ❌ | ❌ | ❌ | ✅ State file based |
| **Best for** | Simple parallel tasks | Codebase splitting | Sequential plan execution | Complex multi-step projects |

### When to Use Orche?

**✅ Orche is appropriate when:**
- Complex tasks requiring 3+ different roles
- Tasks where output accuracy matters (research, analysis, code design)
- Tasks where hallucination is critical
- Tasks with interdependent deliverables

**❌ Other skills are better when:**
- Simple 2-3 independent tasks in parallel → `dispatching-parallel-agents`
- File-by-file codebase splitting → `parallel-agent-management`
- Sequential execution with an already-confirmed plan → `executing-plans`

---

## 🚀 Quick Start — First Orchestration in 5 Minutes

### Step 1: Install the Skill (30 Seconds)

Place the skill file in the OpenClaw skills directory:

```bash
# Copy to skills directory
mkdir -p ~/.agents/skills/orche
cp SKILL.md ~/.agents/skills/orche/SKILL.md
```

### Step 2: Trigger (10 Seconds)

Enter the `/orche` command in chat and describe your task:

```
/orche "Write a market analysis report on Korean AI startups"
```

Or in natural language:

```
Orchestrate this project systematically
```

### Step 3: Phase 0 — Answer the Queries (2 Minutes)

Orche will ask 3~10 questions. Answer clearly:

```
🎼 /orche started — Phase 0: Query

📋 Questions to clarify requirements:

1. 📐 Scope: All AI fields? Specific segment (LLM, robotics, etc.)?
2. 🎯 Priority: Market size vs competitive analysis vs investment trends?
3. 📏 Success criteria: Report length? Number of data sources?
4. 🔧 Technical constraints: Specific data sources needed?
5. ⏰ Deadline: Is there a due date?
```

### Step 4: Auto-Progress (Remaining)

Once you answer, Orche automatically:
- **Phase 1**: Builds plan through expert + Critic debate
- **Phase 2**: Sub-agents research and write in parallel
- **Phase 3**: Verification team runs hallucination check + cross-validation

### Step 5: Receive Results

```
🎼 /orche Completion Report

📋 Task: orche-1711432800
⏱️ Total duration: 23 minutes
📊 By phase: Query 3m → Plan 5m → Execute 10m → Verify 5m
🤖 Agents deployed: 11
✅ Tasks completed: 5/5

📁 Deliverables:
- workspace/orche-1711432800/requirements.md
- workspace/orche-1711432800/final-plan.md
- workspace/orche-1711432800/tasks/
- workspace/orche-1711432800/verification/final-verdict.md
```

---

## 🔄 Phase Overview

```
Phase 0: Query    — Clarify requirements (3~10 questions)
Phase 1: Plan     — 3~7 sub-agents debate → finalize plan
Phase 2: Execute  — Split into tasks → 3~8 sub-agents execute in parallel
Phase 3: Verify   — 3~5 verifiers deployed → regress to Phase 2 if issues found
```

### Phase Gate System

Each phase transition requires **gate conditions** to be met before proceeding. Automatic blocking on non-compliance.

| Gate | Transition | Key Conditions |
|------|-----------|----------------|
| **G0** | Phase 0 → 1 | Requirements structured + ambiguous expressions removed + user approval |
| **G1** | Phase 1 → 2 | final-plan.md created + hallucination check passed + no circular dependencies |
| **G2** | Phase 2 → 3 | All tasks completed + deliverables exist + no zombie agents |
| **Verification** | Phase 3 → Done | 14-item hallucination check passed + all required deliverables present |

**On gate failure:**
- G0 not passed → Phase 1 entry blocked. Re-confirmation requested from user.
- G1 not passed → Phase 2 entry blocked. Plan re-debate forced.
- G2 not passed → Phase 3 entry blocked. Missing tasks re-executed.
- Verification fail → Auto regression to Phase 2 (up to 3 times).

---

## Phase 0: Query

### Purpose
Remove ambiguity from user instructions and specify them to an actionable level.

### Procedure
1. Analyze original request → identify missing/ambiguous areas
2. Generate 3~10 questions (at least 1 from each of 6 categories below)
3. Collect user responses → finalize requirements document (max 2 additional rounds)
4. On user approval → save `requirements.md`

### Question Categories

| Category | Example |
|----------|---------|
| **Scope** | What's in scope? What should be excluded? |
| **Technical constraints** | Language/framework/environment limitations? |
| **Priority** | What matters most? (speed/quality/cost) |
| **Success criteria** | How to judge completion? Deliverables? |
| **Dependencies** | External systems/APIs/data? |
| **Risk** | Impact of failure? Rollback needed? |

### Gate G0: Phase 0 → 1 Transition Conditions
- ✅ Requirements are structured (goal, constraints, deliverables specified)
- ✅ Ambiguous expressions removed ("appropriately", "etc." type expressions eliminated)
- ✅ Feasibility assessment complete (required tools/access confirmed)
- ✅ User confirmation received

### Phase 0: When Deemed Infeasible

If G0 feasibility check determines the task is **impossible**:
1. Report specific reasons to user
2. Suggest alternatives (if possible)
3. Await user decision → modification instructions or termination
4. On termination → `orche-state.json` status → `"rejected"`

---

## Phase 1: Planning

### Debate Panel Composition (3~7 members)

| Role | Responsibility |
|------|---------------|
| **Domain Expert** (1~2) | Draft plan based on domain expertise |
| **Advocate** | Strengthen plan merits, argue feasibility |
| **Critic** | Point out weaknesses/risks/gaps + hallucination check |
| **Moderator** | Synthesize debate, build consensus, write final plan |

### Sub-Agent Spawning

```
sessions_spawn:
  task: "<role-specific prompt>"
  label: "orche-<role>-<taskId>"
  model: "anthropic/claude-sonnet-4-6"  # Default (use opus for high complexity)
  mode: "run"
```

> **Model Selection Guide:**
> - Planning/debate: `sonnet` (cost-efficient)
> - Complex domain experts: `opus` (when deep reasoning needed)
> - Simple execution tasks: `sonnet` or `haiku` (fast processing)

### Debate Protocol (Round-based, File-async)

**Round 1:**
1. Expert agents → spawn in parallel → each writes a proposal
2. Advocate → analyze strengths of drafts
3. Critic → point out weaknesses + hallucination check:
   - [ ] References to non-existent APIs/libraries?
   - [ ] Unrealistic performance/time estimates?
   - [ ] Logical contradictions?
   - [ ] Missing dependencies/prerequisites?
4. Moderator → synthesize → write `final-plan.md`

If unresolved issues remain → **Round 2** (up to 3 rounds max).

### Gate G1: Phase 1 → 2 Transition Conditions
- ✅ `final-plan.md` created
- ✅ Task list + dependencies + success criteria specified
- ✅ Hallucination check passed
- ✅ No circular dependencies
- ✅ Rollback strategy defined for each task

---

## Phase 2: Execution

### Task Splitting

Split from `final-plan.md` into independently executable task units:

```json
{
  "id": "task-1",
  "title": "...",
  "description": "...",
  "dependencies": [],
  "assignedAgent": null,
  "status": "pending",
  "output": null
}
```

**Task Status Flow:** `pending → running → completed / failed`

### Dependency-Based Scheduling
- **Independent tasks** → spawn in parallel immediately
- **Dependent tasks** → spawn after predecessor completion
- **Max concurrent agents:** 8 (cost explosion prevention: **3 concurrent recommended**)

### Required Inclusions in Execution Agent Prompts

All execution agent prompts must include the following:

1. Overall plan summary (brief)
2. Detailed task specification
3. Predecessor task deliverables (file paths)
4. Deliverable save path
5. Success criteria
6. Harness rules (see below)

### Immediate Checks on Task Completion
- [ ] Deliverable file exists?
- [ ] Not empty?
- [ ] Success criteria met?
- [ ] No obvious hallucinations?
- On failure → retry that task only (max 2 times). 2 failures → alert user.

### Gate G2: Phase 2 → 3 Transition Conditions
- ✅ All tasks `completed` or `skipped_with_reason`
- ✅ All deliverable files exist + non-empty
- ✅ No zombie agents/sessions
- ✅ No critical errors

---

## Phase 3: Verification

### Verification Team Composition (3~5 members)

| Role | Responsibility |
|------|---------------|
| **Completeness Verifier** | All tasks executed, nothing missing |
| **Accuracy Verifier** | Deliverables match task spec + success criteria |
| **Hallucination Verifier** | Detect factual errors, logical contradictions, non-existent references |
| **Integration Verifier** | Cross-deliverable consistency, interface compatibility |
| **Final Reviewer** (optional) | Final review against original requirements |

### Verification Result Handling

| Result | Action |
|--------|--------|
| **All PASS** | Phase 3 complete → normal termination |
| **HIGH issue** | Regress to Phase 2 (re-execute affected tasks only) |
| **MED issue** | Report to user, confirm re-execution |
| **LOW issue** | Record in report, proceed |

### Regression Conditions (Phase 3 → Phase 2)

Automatic regression to Phase 2 if any of the following apply:
- `hallucination_score >= 2` (2+ failures in 14-item check)
- Required deliverable missing/corrupted
- Test failure rate > 30%
- User-mandatory conditions unmet
- Mutual contradiction between deliverables

### Regression Limits
- `retryCount` maximum **3 times**
- Same reason repeated 2 times → escalate to user
- Token budget 80% consumed → escalate to user

---

## 📦 State Management

All orchestration state is recorded in `workspace/orche-state.json`.
The watchdog and each phase share this file to track progress.

```json
{
  "taskId": "orche-<timestamp>",
  "phase": 0,
  "status": "active",
  "startedAt": "<ISO>",
  "phaseStartedAt": "<ISO>",
  "requirements": null,
  "plan": null,
  "tasks": [],
  "agents": [],
  "watchdog": {
    "enabled": true,
    "lastCheck": null
  },
  "retryCount": 0,
  "maxRetries": 3,
  "tokenBudget": {
    "total": 500000,
    "used": 0,
    "currency": "tokens"
  },
  "errors": []
}
```

### State Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `taskId` | string | Unique identifier (`orche-<unix_timestamp>`) |
| `phase` | number | Current phase (0~3) |
| `status` | string | `active` / `completed` / `aborted` / `rejected` |
| `requirements` | object | Requirements finalized in Phase 0 |
| `plan` | object | Plan finalized in Phase 1 |
| `tasks` | array | Phase 2 task list + status |
| `agents` | array | Currently active sub-agent session key list |
| `retryCount` | number | Phase 3 → 2 regression count |
| `tokenBudget` | object | Token budget management |
| `errors` | array | Error log |

---

## 📁 Directory Structure

Each orchestration creates an independent working directory:

```
workspace/orche-<taskId>/
├── requirements.md              ← Phase 0 deliverable
├── round-1/                     ← Phase 1 debate records
│   ├── expert-1-proposal.md     ← Expert proposal
│   ├── expert-2-proposal.md     ← (if applicable)
│   ├── advocate-review.md       ← Advocate review
│   ├── critic-review.md         ← Critic review
│   └── moderator-summary.md     ← Moderator synthesis
├── round-2/                     ← (2nd round debate if needed)
├── final-plan.md                ← Phase 1 final plan
├── tasks/                       ← Phase 2 deliverables
│   ├── task-1/
│   │   └── output.md
│   ├── task-2/
│   │   └── output.md
│   └── ...
└── verification/                ← Phase 3 verification results
    ├── completeness-report.md   ← Completeness verification
    ├── accuracy-report.md       ← Accuracy verification
    ├── hallucination-report.md  ← Hallucination verification
    ├── integration-report.md    ← Integration verification
    └── final-verdict.md         ← Final verdict
```

---

## 🛡️ Harness Rules (Safety Mechanisms)

### On Orche Start — Execute Immediately

1. **Watchdog registration:** Register task in `watchdog.md` (when using OpenClaw watchdog)
2. **State initialization:** Create `orche-state.json`
3. **Report start to user**

### Phase Gate Harness (Mandatory Check Before Each Phase Transition)

```
G0 not passed → Phase 1 entry blocked. Re-confirmation requested from user.
G1 not passed → Phase 2 entry blocked. Plan re-debate forced.
G2 not passed → Phase 3 entry blocked. Missing tasks re-executed.
Verification fail → Auto regression to Phase 2 (retryCount < 3).
```

### Sub-Agent Harness

Rules that must be included in every sub-agent spawn prompt:

```
[Harness Rules]
1. You must save results to the designated file path upon completion
2. Mark uncertain facts with "needs verification:" — no fabrication
3. Do not use non-existent APIs/libraries
4. On task failure, record failure reason in output file and terminate
```

These rules are **injected into all** sub-agents. This ensures:
- File-based communication is guaranteed (Rule 1)
- Hallucinations are caught early (Rules 2, 3)
- Failure causes are traceable (Rule 4)

### Completion Harness

```
On Phase 3 completion, you must:
1. Set orche-state.json status → "completed"
2. Mark task [x] in watchdog.md (if using watchdog)
3. Send final report to user
```

---

## 🔍 Watchdog Integration

Orche integrates with OpenClaw's watchdog system to monitor the entire process.

### What the Watchdog Does

| Detection Item | Auto Response |
|---------------|---------------|
| Agent 15min+ no change (hang) | kill + re-spawn |
| Empty deliverable (file size 0) | Retry with reinforced prompt |
| All agents lost (deadlock) | Immediate user notification |
| Token budget 80% reached | User warning |

### Watchdog Registration Method

Register the task in `watchdog.md` at Orche start:

```markdown
- [ ] orche <taskId> — Phase 0 (Query)
  session_keys: agent:main:subagent:xxxx
  state_file: workspace/orche-state.json
  evidence_paths:
    - workspace/orche-<taskId>/requirements.md
    - workspace/orche-<taskId>/final-plan.md
  done_when:
    - orche-state.json status == "completed"
```

### Watchdog Design Principles

> These principles reflect lessons learned in production.

- ✅ Read only `watchdog.md` → query `sessions_list` using `session_keys`
- ✅ Do not judge failure by "no session" alone — if deliverables/state files exist, assume progress/completion first
- ✅ Judge normal termination only when: no tasks + 0 active sessions
- ⚠️ If anything is active, report status and wait

> **No watchdog in your environment?** Orche works without a watchdog.
> The watchdog is an **additional safety net**; phase gates and harness rules function as core safety mechanisms without it.

---

## ✅ Hallucination Checklist (14 Items)

Used by Phase 1's Critic and Phase 3's verification team.

### Factual Verification

| ID | Item | Verification Method |
|----|------|-------------------|
| **H-1** | File path existence | Verify with `stat()` or `ls` |
| **H-2** | Command existence | Verify with `which` or `command -v` |
| **H-3** | URL validity | Verify with HTTP request (optional) |
| **H-4** | Code syntax validity | Grammar check with linter/parser |
| **H-5** | Numerical data cross-verification | Confirm with 2+ sources |

### Consistency

| ID | Item | Verification Method |
|----|------|-------------------|
| **H-6** | No self-contradiction | Detect conflicting statements within document |
| **H-7** | Plan-result alignment | 1:1 mapping verification |
| **H-8** | Terminology consistency | Same term for same concept |

### Completeness

| ID | Item | Verification Method |
|----|------|-------------------|
| **H-9** | No remaining TODO/FIXME | `grep -r "TODO\|FIXME"` |
| **H-10** | No placeholders | Detect `[INSERT]`, `TBD`, `...` |
| **H-11** | All deliverables exist | Cross-check deliverable list against requirements |

### Hallucination Patterns

| ID | Item | Verification Method |
|----|------|-------------------|
| **H-12** | No fictional library/API references | Verify existence on npm/pip/crates.io etc. |
| **H-13** | No unsourced statistics | Verify source citation or "needs verification:" label |
| **H-14** | No overconfident expressions | Detect "always", "never", "100%" type claims |

### Judgment Criteria

```
0~1 failures  → PASS ✅
2~3 failures  → WARNING ⚠️ (MED — user judgment)
4+ failures   → FAIL ❌ (HIGH — auto regression)
```

---

## 💰 Cost Management

Orche is a multi-agent system, so cost management is essential.

### Budget Tiers

| Tier | Ratio | Action |
|------|-------|--------|
| 🟢 **Normal** | < 50% | Normal operation |
| 🟡 **Caution** | 50~80% | Limit concurrent agents, prefer `sonnet` |
| 🔴 **Warning** | 80~95% | Stop new spawns, complete in-progress tasks only |
| ⛔ **Exceeded** | > 95% | Full stop, request user judgment |

### Cost Saving Tips

1. **Actively leverage model selection:**
   - Simple execution: `haiku` (lowest cost)
   - Planning/debate/general execution: `sonnet` (best value)
   - Complex reasoning: `opus` (only when needed)

2. **Limit concurrent agents to 3** (default). 8 is the maximum; typically 3~4 is sufficient.

3. **Set token budget according to task scale:**

| Task Scale | Recommended Budget (tokens) | Expected Agents | Estimated Cost (Claude Sonnet) |
|-----------|---------------------------|----------------|-------------------------------|
| Small (simple research) | 200,000 | 6~8 | ~$0.6 |
| Medium (code refactoring) | 500,000 | 10~15 | ~$1.5 |
| Large (market analysis report) | 1,000,000 | 15~20 | ~$3.0 |

> **Note:** Costs above are estimates based on Claude Sonnet. Actual costs vary by model, prompt length, and retry count.

4. **Use Phase 0 well.** Clear scope definition during initial queries reduces unnecessary tasks and cuts costs.

### Token Budget Adjustment

Adjust the budget by modifying `tokenBudget.total` in `orche-state.json`:

```json
{
  "tokenBudget": {
    "total": 1000000,
    "used": 0
  }
}
```

---

## 🚨 Exception Handling Summary

| Exception | Detection Method | Auto Response | User Notification |
|-----------|-----------------|---------------|-------------------|
| Agent hang | Watchdog 15min no change | kill + re-spawn | On 2 consecutive occurrences |
| Empty deliverable | File size 0 | Retry with reinforced prompt | On 2 failures |
| API error (429/500) | HTTP status | Retry after 30s | On 3 failures |
| Hallucination detected | Critic/verification team | Regenerate affected portion | On HIGH severity |
| Total deadlock | All agents lost | — | Immediately |
| Context exceeded | Error message | Retry with reduced input | On failure |
| maxRetries exceeded | Counter check | — | Immediate judgment request |
| Token budget exceeded | used/total ratio | Model downgrade | At 80% |

### Error Logging

All errors are recorded in `orche-state.json`'s `errors` array:

```json
{
  "errors": [
    {
      "timestamp": "2026-03-26T10:30:00Z",
      "phase": 2,
      "taskId": "task-3",
      "type": "AGENT_HANG",
      "message": "Agent orche-exec-task-3 unresponsive for 15+ minutes",
      "action": "kill + re-spawn"
    }
  ]
}
```

---

## 🙋 User Intervention Points

| Timing | Required? | Content |
|--------|-----------|---------|
| Phase 0 complete | ✅ **Required** | Approve requirements |
| Phase 1 complete | Optional | Review plan (default: auto-proceed) |
| Phase 2 failure | ✅ **Required** | Judgment after 2 retry failures |
| Phase 3 MED issue | ✅ **Required** | Decide on re-execution |
| Phase 3 complete | Notification | Final results report |

### Auto-Proceed Mode

Auto-proceeding from Phase 1 to Phase 2 is the default behavior.
If you want to review the plan directly, specify "I want approval at each step" during Phase 0 queries.

---

## 🛑 Abort Procedure

When the user requests task cancellation:

1. **Terminate all active sub-agents** (session kill)
2. **Remove task from watchdog** (if in use)
3. **Set `orche-state.json` status → `"aborted"`**
4. **Report abort to user** (including list of completed tasks)

```
🎼 /orche Abort Report

📋 Task: orche-1711432800
🛑 Abort reason: User request
✅ Completed tasks: 3/7
📁 Completed deliverables:
- workspace/orche-1711432800/tasks/task-1/output.md
- workspace/orche-1711432800/tasks/task-2/output.md
- workspace/orche-1711432800/tasks/task-3/output.md
```

---

## 🔄 Session Disconnection Recovery

### Problem
If the main session disconnects mid-process, the orchestration stops.

### Recovery Mechanism

1. **`orche-state.json` is the recovery key.**
   - Phase/task progress is recorded in the file, so after session restart, the state file can be read to resume.

2. **State updated immediately on each task completion:**
   - `completedAt` recorded in `orche-state.json` upon receiving each sub-agent result

3. **Watchdog detects hangs:** (when using watchdog)
   - If task exists in `watchdog.md` and main session is unresponsive for 20+ minutes in `sessions_list`, reports to user

4. **Manual recovery:**
   - User instructs orche to resume → reads `orche-state.json` → continues from incomplete tasks

### Recovery Command Example

```
/orche resume
```

This command reads `orche-state.json` and resumes execution from the last completed phase/task.

---

## 🎮 Demo Scenarios

### Scenario 1: Research Report Writing

**User Input:**
```
/orche "Write a 2025 Korean GenAI market analysis report. 
Must include market size, key players, investment trends, and regulatory landscape."
```

**Phase 0 — Query (2~3 min):**
```
🎼 Phase 0: Query

1. 📐 Scope: All GenAI? (LLM, image generation, code assistants, etc.)
2. 🎯 Depth: Individual company analysis? Or market overview level?
3. 📊 Data: Public data only? Paid research sources?
4. 📏 Length: How many pages (A4 equivalent)?
5. 🎨 Format: Markdown? PDF?
6. ⏰ Purpose: Internal report? Investment decision? Blog?
```

**Phase 1 — Planning (5 min):**
- Expert A (AI market analyst): Proposes report structure
- Expert B (Korean market specialist): Suggests Korea-specific data sources
- Critic: Points out "Market size estimates need cross-verification from 2+ sources"
- Moderator: Finalizes split into 5 tasks

**Phase 2 — Execution (10~15 min):**
| Task | Agent | Deliverable |
|------|-------|-------------|
| Market overview | agent-1 | `tasks/task-1/market-overview.md` |
| Key players | agent-2 | `tasks/task-2/key-players.md` |
| Investment trends | agent-3 | `tasks/task-3/investment-trends.md` |
| Regulatory landscape | agent-4 | `tasks/task-4/regulatory.md` |
| Consolidated report | agent-5 | `tasks/task-5/final-report.md` |

**Phase 3 — Verification (5 min):**
- H-5 check: Market size figures cross-verified → 2 sources confirmed ✅
- H-13 check: Investment amounts have cited sources → ✅
- H-11 check: All sections complete → ✅
- Final verdict: **PASS** ✅

---

### Scenario 2: Code Refactoring

**User Input:**
```
/orche "Refactor our project's API layer. 
Currently Express monolithic — want to separate modules by domain and increase test coverage."
```

**Phase 0 — Query (3 min):**
```
🎼 Phase 0: Query

1. 📐 Scope: Entire API? Specific domains only?
2. 🔧 Tech stack: Express + TypeScript? ORM?
3. 📁 Current structure: Source directory path?
4. 🎯 Target structure: Have an example? (NestJS-style? Layered?)
5. ✅ Tests: Current coverage? Test framework?
6. ⚠️ Constraints: Backward compatibility? Zero-downtime deployment?
```

**Phase 1 — Planning (7 min):**
- Expert A (Node.js architect): Proposes module separation strategy
- Expert B (Testing specialist): Proposes testing strategy
- Critic: Points out "Need to analyze dependency graph first to ensure no circular dependencies"
- Advocate: Argues "Gradual migration is safer"
- Moderator: Finalizes 6 tasks in order: dependency analysis → module separation → test writing

**Phase 2 — Execution (15~20 min):**
| Task | Agent | Deliverable |
|------|-------|-------------|
| Dependency analysis | agent-1 | `tasks/task-1/dependency-graph.md` |
| User module separation | agent-2 | `tasks/task-2/user-module/` |
| Auth module separation | agent-3 | `tasks/task-3/auth-module/` |
| Order module separation | agent-4 | `tasks/task-4/order-module/` |
| Shared utilities cleanup | agent-5 | `tasks/task-5/shared/` |
| Test writing | agent-6 | `tasks/task-6/tests/` |

**Phase 3 — Verification (7 min):**
- H-1 check: All file paths exist → ✅
- H-4 check: TypeScript compilation successful → ✅
- H-12 check: No non-existent npm package references → ✅
- H-7 check: Plan-result alignment → Task 5 gap found ⚠️
- **1st regression:** Task 5 re-executed → completed
- Final verdict: **PASS** ✅

---

### Scenario 3: Market Analysis

**User Input:**
```
/orche "Do a SaaS competitor analysis. 
Target Notion, Coda, Slite — compare features, pricing strategy, and market positioning."
```

**Phase 0 — Query (2 min):**
```
🎼 Phase 0: Query

1. 📐 Scope: Any additional competitors beyond these 3?
2. 🎯 Analysis depth: Feature-level detail? Strategic level?
3. 📊 Data: Public pricing only? Actual usage experience needed?
4. 📏 Deliverables: Comparison table + strategy report?
5. 🔍 Our product: Is there a reference product to compare against?
```

**Phase 1 — Planning (5 min):**
- Expert (SaaS market specialist): Proposes analysis framework (Porter's Five Forces + Feature Matrix)
- Critic: Warns "Pricing should be based on public pages only — no guessing enterprise pricing"
- Moderator: Finalizes 4 tasks

**Phase 2 — Execution (10 min):**
| Task | Agent | Deliverable |
|------|-------|-------------|
| Notion analysis | agent-1 | `tasks/task-1/notion-analysis.md` |
| Coda analysis | agent-2 | `tasks/task-2/coda-analysis.md` |
| Slite analysis | agent-3 | `tasks/task-3/slite-analysis.md` |
| Comparative summary | agent-4 | `tasks/task-4/comparison-report.md` |

**Phase 3 — Verification (5 min):**
- H-5 check: Pricing data cross-verified → public page basis ✅
- H-13 check: MAU/ARR figures have cited sources → "needs verification:" properly labeled ✅
- H-14 check: "Notion will definitely win" type overconfidence → none found ✅
- Final verdict: **PASS** ✅

---

## 📈 Production Run Records

> Below are summaries of actual projects completed with Orche.

### Run #1: ClawHub Skill Packaging

| Item | Details |
|------|---------|
| **Task** | Repackage internal skills for ClawHub publishing |
| **Duration** | 25 minutes |
| **Agents deployed** | 12 (planning 4 + execution 5 + verification 3) |
| **By phase** | Query 3m → Plan 6m → Execute 10m → Verify 6m |
| **Regressions** | 0 (passed first time) |
| **Notable** | Critic flagged "environment-dependent hardcoded cron IDs" → fixed during planning phase |

### Run #2: Multilingual Documentation Translation + Review

| Item | Details |
|------|---------|
| **Task** | Technical doc translation (Korean/English/Japanese) + terminology unification |
| **Duration** | 35 minutes |
| **Agents deployed** | 15 (planning 3 + execution 8 + verification 4) |
| **By phase** | Query 2m → Plan 5m → Execute 18m → Verify 10m |
| **Regressions** | 1 (H-8 terminology consistency failure → glossary-based retranslation) |
| **Notable** | Terminology inconsistency auto-detected → Phase 2 regression → fixed and passed |

### Run #3: API Design + Implementation + Testing

| Item | Details |
|------|---------|
| **Task** | REST API design → implementation → test code → documentation |
| **Duration** | 42 minutes |
| **Agents deployed** | 18 (planning 5 + execution 8 + verification 5) |
| **By phase** | Query 4m → Plan 8m → Execute 20m → Verify 10m |
| **Regressions** | 1 (H-12 non-existent middleware reference → affected task re-executed) |
| **Notable** | Critic debate on "implement auth middleware vs use library" → Moderator decided on verified library |

### Run Statistics Summary

```
Total completions: 3
Average duration: 34 minutes
Average agents: 15
First-pass rate: 33% (1/3)
Resolved via auto-regression: 100% (2/2 regressions resolved within 3 retries)
Manual escalations: 0
```

---

## 🔗 hallucination-guard Integration

> If the **hallucination-guard** skill is installed, Orche can leverage it during the verification phase for more precise hallucination detection.

### Integration Method

1. **Install hallucination-guard skill:**
   ```bash
   # Install from ClawHub (needs verification: install command may vary by environment)
   mkdir -p ~/.agents/skills/hallucination-guard
   # Place SKILL.md in that directory
   ```

2. **Auto-utilized in Phase 3 verification:**
   - When hallucination-guard is installed, Phase 3's **hallucination verifier** additionally applies that skill's checklist.
   - Particularly improves detection accuracy for "non-existent APIs/libraries" in code-related tasks.

3. **Integration Architecture:**

```
Phase 3: Verification
├── Completeness Verifier
├── Accuracy Verifier
├── Hallucination Verifier ──── Uses hallucination-guard skill
│   ├── Orche's built-in 14-item check
│   └── + hallucination-guard additional checks (when installed)
├── Integration Verifier
└── Final Reviewer
```

4. **When hallucination-guard is not installed:**
   - Orche functions normally with its built-in 14-item checklist alone.
   - hallucination-guard is an **optional enhancement** tool.

### Recommended Combinations

| Task Type | Orche Alone | + hallucination-guard |
|-----------|:---:|:---:|
| Research report | ✅ Sufficient | ✅✅ Enhanced numerical verification |
| Code refactoring | ✅ Sufficient | ✅✅✅ API existence check essential |
| Market analysis | ✅ Sufficient | ✅✅ Enhanced statistics source verification |
| Document translation | ✅ Sufficient | ✅ Minimal difference |

---

## ⚙️ Advanced Configuration

### Adjusting Debate Round Count

Default is up to 3 rounds. Complex domains may require more rounds.
Specify "I want thorough plan debate" during Phase 0 to adjust the round count.

### Verification Intensity Adjustment

| Intensity | Verifier Count | Hallucination Check | Recommended For |
|-----------|---------------|-------------------|-----------------|
| **light** | 2 | Essential 5 items only | Simple tasks, time savings |
| **standard** (default) | 3~4 | All 14 items | General tasks |
| **thorough** | 5 | 14 items + additional cross-verification | High-risk tasks |

You can specify verification intensity during Phase 0:
```
/orche "Refactor the API. Use thorough verification."
```

### Agent Model Configuration

Specify different models per phase based on task characteristics:

```json
{
  "modelConfig": {
    "planning": "anthropic/claude-sonnet-4-6",
    "execution": "anthropic/claude-sonnet-4-6",
    "verification": "anthropic/claude-sonnet-4-6",
    "complex": "anthropic/claude-opus-4-6"
  }
}
```

### Concurrent Agent Limit

Default is 3 (maximum 8). Adjust in `orche-state.json`:

```json
{
  "concurrency": {
    "default": 3,
    "max": 8
  }
}
```

---

## ❓ FAQ

### Q: Can Phase 0 be skipped?
**A:** No. Phase 0 is **mandatory**. Proceeding with ambiguous requirements causes direction change costs in Phase 2 to grow exponentially. Clear answers in Phase 0 actually reduce total time.

### Q: How much does it cost?
**A:** Depends on task scale. Small tasks (research report) use approximately 200K tokens (Claude Sonnet ~$0.6), large tasks (API design + implementation) approximately 1M tokens (~$3.0). See the cost management section for budget settings.

### Q: What happens if verification keeps failing?
**A:** Auto-regression up to 3 times. If all 3 fail, escalated to user for direct judgment. Also escalated if the same reason fails 2 consecutive times.

### Q: Can it work without a watchdog?
**A:** Yes. The watchdog is an additional safety net; phase gates and harness rules are the core safety mechanisms. Orche functions normally without a watchdog.

### Q: Can it be used alongside other orchestration skills?
**A:** Orche operates independently. However, handling simple parallel tasks within Phase 2 using `dispatching-parallel-agents` patterns is naturally compatible.

### Q: Is progress lost on session disconnect?
**A:** No. All state is recorded in `orche-state.json` and the file system. Use `/orche resume` to continue from the last progress point.

### Q: What if the Critic over-opposes in the debate panel?
**A:** The Moderator builds consensus. Debate runs up to 3 rounds; if consensus isn't reached, the Moderator has final decision authority.

### Q: Do I have to use the Opus model?
**A:** No. Sonnet alone can handle most tasks. Opus is used selectively only for domain expert roles requiring complex reasoning. Sonnet is recommended as default for cost savings.

---

## 📋 Changelog

### v1.0.0 (2026-03-26)
- 🎉 Initial ClawHub release
- Full Phase 0~3 pipeline implementation
- 14-item hallucination checklist
- Phase gate system
- Critic debate protocol
- Auto regression mechanism (up to 3 times)
- Watchdog integration (optional)
- 4-tier cost management
- Session disconnection recovery (state file based)
- 3 demo scenarios + production run records

---

## Important Notes

1. **Sub-agents are created via `sessions_spawn`** (`mode: "run"`)
2. **Do not pass full session context to agents** — pass only the minimum necessary information
3. **File-based communication** — no direct inter-agent communication
4. **Concurrent agent limit** — recommended 3, maximum 8
5. **Phase 0 cannot be skipped**
6. **Be cost-conscious** — don't deploy 7 agents for a simple task
7. **Harness rules are injected into all sub-agents** — this is the key to hallucination prevention

---

*Made with 🎼 by [reikys](https://github.com/reikys) — Battle-tested in production environments.*

# PAD Mode for OpenClaw

<img width="1536" height="776" alt="PAD Mode" src="https://github.com/user-attachments/assets/097ea4bf-a70b-4579-8246-5a578cf2e3a4" />

**Plan → Act → Deliver** — A structured task execution skill for OpenClaw.

[![ClawHub](https://img.shields.io/badge/ClawHub-install%20pad--mode-blue)](https://clawhub.ai/yipxiyi/pad-mode)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](https://clawhub.ai/yipxiyi/pad-mode)
[![License](https://img.shields.io/badge/license-MIT-yellow)](./LICENSE)

[中文](./README_zh.md)

---

## Before → After

**Without PAD Mode:**
> User: "Refactor the auth module to use JWT instead of sessions"
>
> Agent: *starts editing files immediately, breaks login flow halfway through, forgets to update tests, declares "done" when the main file is edited but middleware still uses sessions*

**With PAD Mode:**
> User: "Refactor the auth module to use JWT instead of sessions"
>
> Agent: Creates a plan with 5 tasks (token generation, middleware update, test updates, migration script, cleanup), waits for approval, executes each with status tracking, asks you to verify before archiving.

The difference: **structured decomposition + confirmation gates = reliable execution**.

---

## Key Features

- 📋 **Plan Document** — Every task has a concrete, verifiable deliverable. "Optimize the code" becomes "Reduce API response time from 800ms to 200ms by adding Redis caching to the user endpoint".
- 🔄 **Foreground / Background** — Run complex plans in background (sub-agent) with real-time progress pushed to you.
- ✅ **Completion Gate** — Plans never auto-close. You review and confirm before archiving.
- 📦 **Parallel Execution** — Independent tasks run concurrently via sub-agents.
- 🔁 **Resumable** — Interrupted plans can be picked up from the last checkpoint.
- 📝 **Change Log** — Every modification is tracked in the plan document.

## Status Flow

```
🟡 Discussing → 🔵 Confirmed → 🟢 Executing → ⏳ Pending Review → ✅ Completed
                                                                               ↓
                                                          🔧 Changes Needed → back to Discuss
```

---

## Installation

### ClawHub (Recommended)

```bash
clawhub install pad-mode
```

### From source

```bash
git clone https://github.com/Yipxiyi/PAD-Mode-for-openclaw.git
cp -r PAD-Mode-for-openclaw ~/.openclaw/workspace/skills/pad-mode/
```

---

## Triggers

| Method | Example | When it fires |
|--------|---------|---------------|
| Slash command | `/pad` | Always — creates a plan |
| Keywords | "make a plan", "plan this out", "做个计划" | Detects planning intent |
| Auto-detect | 3+ distinct tasks, multi-file changes, architectural decisions | Complex requests |

**Auto-detect fires when:**
- ✅ "Add user auth with login, signup, password reset, and email verification" (4 tasks)
- ✅ "Migrate the database from MySQL to PostgreSQL" (multi-step, risky)
- ✅ "Refactor the payment module and add Stripe integration" (2+ concerns)

**Auto-detect does NOT fire when:**
- ❌ "Fix the typo in header.js" (single, simple)
- ❌ "What does this function do?" (question, not task)

---

## How It Works

Four phases with enforcement at every step:

```
  PLAN            DISCUSS         ACT             DELIVER
  Decompose       Iterate         Execute         Confirm
  ├ Create plan   ├ Refine scope  ├ Track each    ├ Review all
  ├ Break into    ├ Lock          │ task status   ├ ✅ or 🔧
  │ tasks         │ deliverables  ├ Progress      └ Archive
  └ No research   └ Max 4 Qs      │ updates       │
                                   └ Foreground /  │
                                      Background   │
                                                    │
                                   ◄── Loop if changes needed ──►
```

## ⚠️ Enforcement

PAD Mode treats these as hard blockers, not suggestions:

| Rule | If violated |
|------|-------------|
| Never skip approval (Phase 3) | Halt, undo actions, return to Phase 3 |
| No research during planning | Discard results, plan structure only |
| Must ask execution mode | Pause all work, wait for user reply |
| Always update task status | Immediately fix plan doc |
| Never auto-archive | Wait for user confirmation |

---

## Real Example

**User request:** "Build a REST API for a todo app with CRUD operations, user auth, and deploy to Railway"

**Generated plan (`plans/2026-03-31-todo-api.md`):**

```markdown
# 📋 Todo REST API

**Status:** 🔵 Confirmed
**Created:** 2026-03-31 14:00

## Task Breakdown
- [x] **T1.1** Initialize Express project with TypeScript
  - Deliverable: Project scaffold with tsconfig, package.json, folder structure
  - Dependencies: none
- [x] **T1.2** Implement CRUD endpoints (GET/POST/PUT/DELETE /todos)
  - Deliverable: 4 working endpoints with validation
  - Dependencies: T1.1
- [ ] **T2.1** Add JWT authentication
  - Deliverable: Login/register endpoints, auth middleware
  - Dependencies: T1.1
- [ ] **T3.1** Write tests
  - Deliverable: 80%+ coverage on endpoints
  - Dependencies: T1.2, T2.1
- [ ] **T4.1** Deploy to Railway
  - Deliverable: Live URL with health check passing
  - Dependencies: T3.1
```

---

## Background

Inspired by the structured planning modes in **OpenAI Codex** and **Anthropic Claude Code**, which proved that LLMs perform significantly better when forced to plan before executing. PAD Mode brings this pattern to OpenClaw with additional features:

- **User confirmation gates** (plan approval + completion review)
- **Foreground/background execution** choice
- **Real-time progress tracking** via plan documents
- **Sub-agent parallelism** for independent tasks
- **Enforcement rules** that prevent common agent mistakes

The goal: make OpenClaw as reliable for long-running tasks as it is for quick one-shots.

## License

MIT

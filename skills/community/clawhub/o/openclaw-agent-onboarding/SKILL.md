---
name: openclaw-agent-onboarding
description: "OpenClaw 个人 AgentOS 初始化向导 / Bootstrapper。Use when a user wants to initialize, diagnose, upgrade, repair, or health-check a new or existing OpenClaw setup; install baseline skills; add web search and skill discovery; set up HOT/WARM/COLD memory; create an Obsidian-friendly Markdown knowledge base; configure Agent teams; establish self-evolution workflows; reduce context pollution; or bootstrap OpenClaw into a personal AgentOS. 触发词：OpenClaw 初始化、AgentOS 启动器、新用户引导、安装必要 skill、搭建三层记忆、个人知识库、Obsidian、Agent 团队、自进化、健康检查、一键修复、一键升级、上下文污染治理。"
version: "0.1.0"
author: "OpenClaw"
tags: [openclaw, onboarding, agentos, memory, skills, knowledge-base, obsidian, health-check]
---

# OpenClaw AgentOS Onboarding

This skill bootstraps a fresh or underpowered OpenClaw setup into a safe, maintainable personal AgentOS.

## Prime directive

Do not merely explain. Diagnose, generate a change plan, ask for confirmation for risky writes/installs, execute safe steps, verify, and report.

Default execution contract:

```text
Preflight → Plan → Confirm risky changes → Execute → Verify → Report → Leave rollback notes
```

## Safety rules

- Never delete user files.
- Never overwrite `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `DREAMS.md`.
- For existing bootstrap/reference files: create backups, generate patch suggestions, or append clearly marked sections only after confirmation.
- Do not install unknown-source skills automatically.
- Do not perform paid API/cloud actions without explicit confirmation.
- Do not write private user content into reusable public templates.
- Mark API-key-dependent skills before installing or configuring.
- Prefer incremental safe fixes; separate `safe-fix`, `needs-confirm`, and `manual` actions.

## Operating modes

Respond to either slash-style requests or natural language equivalents:

```text
/agentos bootstrap
/agentos diagnose
/agentos init
/agentos install
/agentos repair
/agentos upgrade
/agentos health
/agentos memory-check
/agentos skill-check
/agentos kb-init
/agentos kb-check
/agentos kb-obsidian
/agentos context-clean
/agentos report
```

Natural-language triggers include: “帮我初始化 OpenClaw”, “一键升级到 AgentOS”, “安装必要 skill”, “搭建三层记忆”, “搭建个人知识库”, “检查上下文污染”, “做健康检查”.

## Darwin optimization note

This skill was optimized with the Darwin rubric focus: concrete workflow, explicit boundaries, progressive disclosure, verification outputs, and common user prompts. Typical test prompts are stored in `test-prompts.json`.

## Decision matrix

Choose the narrowest mode that satisfies the user:

| User intent | Mode | References to read | Default action |
|---|---|---|---|
| “刚装 OpenClaw / 不知道怎么开始” | bootstrap | `skill-baseline.md`, then diagnose | Stage 0 + readiness report |
| “安装必要 Skill / 没搜索能力” | install | `skill-baseline.md`, `safety-policy.md` | skill plan + confirmed install |
| “搭三层记忆 / 解决失忆” | memory setup | `memory-architecture.md` | create missing dirs/templates only |
| “搭个人知识库 / Obsidian” | kb-init | `knowledge-base.md` | create Markdown vault; Obsidian optional |
| “搭 Agent 团队” | agent-team | `agent-team.md` | propose profile; do not overcomplicate |
| “自进化 / SOP / Skill 草稿” | self-evolution | `self-evolution.md` | create workflow dirs/templates |
| “健康检查 / 修复污染” | health/repair | `health-checks.md`, `context-hygiene.md` | diagnose + classify fixes |
| “安全/覆盖/安装来源” | safety review | `safety-policy.md` | block risky action until confirmed |

## Required output formats

### Change plan

```text
Goal:
Current level:
Target level:
Safe changes:
Needs confirmation:
Manual steps:
Files/directories affected:
Skills to install:
Verification commands/checks:
Rollback notes:
```

### Final report

```text
Current level → Target level:
Completed:
Skipped:
Installed/missing skills:
Created files/dirs:
Backups/patches:
Health score:
Risks/Pending confirmations:
Next 3 actions:
```

## Workflow

### 1. Diagnose first

Check:

```text
OpenClaw/gateway status, workspace path, skills dir, memory dir, docs dir,
AGENTS.md/MEMORY.md/SOUL.md/TOOLS.md/USER.md presence,
installed skills, clawhub/find-skill availability, web search availability,
git status, cron/heartbeat, memory structure, knowledge base, Agent team config,
context pollution, duplicate/broken skills.
```

Output maturity level:

```text
Level 0 fresh install
Level 1 basic assistant
Level 2 assistant with memory
Level 3 AgentOS with knowledge base/workflows
Level 4 multi-agent + self-evolution + health checks
Level 5 advanced personal AgentOS
```

### 2. Bootstrap Stage 0: skill discovery + web search

If the user lacks skill discovery or web search, fix this before advanced setup.

Minimum survival package:

```text
clawhub
find-skill
openclawmp
markdown
```

If `clawhub` is missing, recommend or run after confirmation:

```bash
npm i -g clawhub
```

Search/install examples:

```bash
clawhub search "web search"
clawhub install find-skill
clawhub install openclawmp
clawhub install markdown
```

If offline, generate directories/templates/manual install checklist and tell user to rerun install after network returns.

For detailed skill groups and non-ClawHub links, read `references/skill-baseline.md`.

### 3. Install baseline skill packages

Use packages from `references/skill-baseline.md`:

```text
bootstrap-minimal
bootstrap-search
bootstrap-docs
bootstrap-agentos-core
bootstrap-skill-lab
bootstrap-engineering
bootstrap-design
bootstrap-creator
```

Default standard order:

```text
1. bootstrap-minimal
2. bootstrap-search
3. bootstrap-docs
4. bootstrap-agentos-core
5. bootstrap-skill-lab
```

Always mark each skill as: installed / missing / failed / needs API key / non-ClawHub / manual.

### 4. Set up HOT/WARM/COLD memory

Create or propose:

```text
MEMORY.md                 # HOT, ≤150 lines recommended
memory/index.md
memory/projects/
memory/domains/
memory/people/
memory/preferences/
memory/decisions.md
memory/gotchas.md
memory/archive/
memory/logs/
memory/raw/
```

Rules: temporary info never goes into HOT; long content goes to WARM/COLD; conflicts are flagged, not overwritten. See `references/memory-architecture.md`.

### 5. Set up personal knowledge base / Obsidian-friendly vault

Create Markdown-first vault under `memory/wiki/`; Obsidian is optional.

Recommended structure:

```text
memory/wiki/00 Inbox/
memory/wiki/01 Projects/
memory/wiki/02 Areas/
memory/wiki/03 Resources/
memory/wiki/04 Concepts/
memory/wiki/05 People/
memory/wiki/06 Decisions/
memory/wiki/07 Workflows/
memory/wiki/08 Skills/
memory/wiki/09 Reviews/
memory/wiki/99 Archive/
```

Knowledge flow:

```text
Capture → Distill → Link → Operationalize → Archive
```

Tell users: without Obsidian, OpenClaw still works via Markdown; with Obsidian, open `memory/wiki/` as a vault to see graph/backlinks. See `references/knowledge-base.md`.

### 6. Configure Agent team

Offer three profiles:

```text
single: main-agent
three-agent: architect → executor → auditor
six-agent: pm → architect → reasoner → coder → auditor → monitor
```

Do not force multi-agent complexity on beginners. See `references/agent-team.md`.

### 7. Establish self-evolution workflows

Create or propose:

```text
memory/wiki/07 Workflows/TaskNotes/
memory/wiki/07 Workflows/SOP/
memory/wiki/07 Workflows/SkillDrafts/
memory/wiki/07 Workflows/ContextCaptures/
memory/wiki/07 Workflows/Checkpoints/
memory/wiki/07 Workflows/Evaluations/
memory/wiki/07 Workflows/SecurityIntake/
```

Flow:

```text
Task → TaskNote → SOP → SkillDraft → vetter → official Skill → index
```

See `references/self-evolution.md`.

### 8. Health checks and repair/upgrade

Health check dimensions:

```text
skills, memory, knowledge base, context hygiene, Agent team, cron/heartbeat,
OpenClaw service, logs, git state, security risks.
```

Output a score and separate P0/P1/P2 issues. For details, see `references/health-checks.md` and `references/context-hygiene.md`.

### 9. Verify

Before final report, verify what changed:

```text
- directories/files exist
- protected files were not overwritten
- installed skills contain SKILL.md
- diagnose script still emits valid JSON
- memory/wiki structure exists if requested
- health issues are classified as P0/P1/P2
```

If verification fails, report the blocker and propose repair; do not claim success.

### 10. Final report

Always finish with:

```text
current level, target level, completed changes, installed/missing skills,
created directories/files, backups, risks, pending confirmations, next steps.
```

## Implementation notes

- For simple advisory requests, do not execute writes; produce a plan.
- For initialization requests, create missing directories/templates only after confirming scope.
- If using scripts, read or run files in `scripts/` as needed. Scripts are helpers, not authority; safety rules above win.

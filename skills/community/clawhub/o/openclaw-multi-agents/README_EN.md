# Multi-Agent Orchestration for OpenClaw

[中文版](README.md) | English

<p align="center">
  <strong>A multi-agent team architecture built specifically for <a href="https://openclaw.ai">OpenClaw</a>.</strong><br>
  <sub>A Manager that plans. Workers that specialize. A QA gate that never lets bad output through.</sub>
</p>

<p align="center">
  <em>I use this every day to coordinate my AI teammates. Now it's open source.</em><br>
  <sub>— AiTu, an OpenClaw-based AI Employee</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Required-blue?style=flat-square" alt="OpenClaw">
  <img src="https://img.shields.io/badge/Personas-61%2B_Historical_Figures-8B5CF6?style=flat-square" alt="Personas">
  <img src="https://img.shields.io/badge/Architecture-Main_%E2%86%92_Manager_%E2%86%92_Workers-F59E0B?style=flat-square" alt="Architecture">
  <img src="https://img.shields.io/badge/QA_Gate-Built--in-22C55E?style=flat-square" alt="QA Gate">
  <img src="https://img.shields.io/badge/Languages-EN_%7C_ZH-EC4899?style=flat-square" alt="Languages">
  <img src="https://img.shields.io/badge/License-MIT-gray?style=flat-square" alt="License">
</p>

---

Build a team of specialized AI agents that work together — one orchestrates, the rest execute.

---

## What This Does

Most AI assistants work alone. This skill gives OpenClaw a **three-tier team**:

```
You
 └─ Main Agent (relay — talks to you, never blocks)
     └─ Manager Agent (orchestrates — plans, delegates, quality-checks)
         ├─ Strategist Worker (planning / PRD)
         ├─ Engineer Worker (development / debugging)
         ├─ Reviewer Worker (code review / QA)
         └─ Any role you need…
```

Each Worker has a **persona** (a historical figure whose thinking style fits the role), a **task category** (determines which model to use), and **clear ownership** of what they do and don't handle.

The Manager runs a built-in **QA gate** before anything reaches you — no "done and shipped" without a quality check.

---

## Why It Works

**The problem with most multi-agent systems:**  
Agents complete their tasks and pass the result along — no one checks if it's actually good. You get whatever comes out.

**What this skill does differently:**

|  | CrewAI | AutoGen | **Multi-Agent Orchestration** |
|--|:------:|:-------:|:-----------------------------:|
| **Mandatory QA gate** | ❌ | ⚠️ optional | ✅ built-in, unskippable |
| **Non-blocking Main Agent** | ❌ | ❌ | ✅ always responds < 1s |
| **Persona system** | ❌ | ❌ | ✅ 61+ historical figures |
| **Wisdom accumulation** | ❌ | ❌ | ✅ lessons shared across Workers |
| **Team design interview** | ❌ | ❌ | ✅ reads your context first |
| **Model selection from config** | ❌ | ❌ | ✅ uses your actual models |
| **Works inside OpenClaw** | ❌ | ❌ | ✅ native skill, zero extra setup |

- **Manager-enforced QA** — every deliverable passes a self-check (and optionally a dedicated reviewer) before you see it
- **Main Agent never blocks** — you get a response in under 1 second, always. Long tasks run in the background
- **Wisdom accumulates** — lessons learned by one Worker get injected into future tasks for relevant Workers
- **Interview before building** — the skill reads your history first, then asks only what it doesn't already know, before proposing a team design

---

## Quick Start

**Option 1: From ClawHub**
```bash
clawhub install openclaw-multi-agents
```

**Option 2: From GitHub (direct link)**

Paste this in your OpenClaw chat and say "install this skill":
```
https://github.com/porkapple/openclaw-multi-agent
```

**Option 3: Manual**
```bash
cp -r multi-agent-orchestration ~/.openclaw/workspace/skills/
```

Then just tell your Main Agent:

> "I want to build a team" / "I need an assistant for coding" / "Help me handle multiple things at once"

The skill activates automatically. It will:
1. Read your existing context (USER.md, memory, session history)
2. Confirm what it already knows, ask only what it doesn't
3. Propose a team design with reasoning
4. Wait for your approval before creating anything
5. Build the team and verify each Agent's persona is working

---

## What's Included

```
multi-agent-orchestration/
├── SKILL.md                          ← Main instructions (AI reads this)
├── INSTALL.md                        ← Manual configuration guide
├── references/
│   ├── persona-library.md            ← 61+ historical figures with roles
│   ├── architecture_guide.md         ← Workspace structure & config spec
│   ├── planning_guide.md             ← Interview methodology
│   └── task_categories_and_model_matching.md
├── templates/
│   ├── interview_questions.md        ← Structured question bank
│   ├── team_design_template.md       ← Team design document format
│   ├── manager_soul_template.md      ← Manager Agent SOUL.md template (Iron Rule included)
│   ├── manager_agents_template.md   ← Manager Agent AGENTS.md template (Iron Rule included)
│   ├── worker_soul_template.md       ← Worker Agent SOUL.md template (Iron Rule included)
│   └── worker_agents_template.md    ← Worker Agent AGENTS.md template (correct session keys)
├── examples/
│   ├── setup_example.md             ← End-to-end walkthrough
│   └── wisdom/                      ← Example Wisdom files
└── scripts/
    ├── setup_agent.sh               ← Create a single Agent workspace
    ├── setup_team.sh                ← Create a full team
    └── create_agent.sh              ← Minimal Agent creation
```

---

## Persona System

Each Worker gets a **persona** — a historical figure whose thinking style matches the role. The AI uses the English full name to activate the right mental model.

| Role | Persona | Signature |
|------|---------|-----------|
| Strategy / PRD | Charlie Munger | "Invert, always invert" |
| Development | Richard Feynman | "What I cannot create, I do not understand" |
| Code Review | W. Edwards Deming | "In God we trust, all others bring data" |
| Orchestration | Henry Gantt | Systematic planning, delegation, verification |
| Product Design | Steve Jobs | "Simplicity is the ultimate sophistication" |
| Copywriting | David Ogilvy | "The consumer is not a moron" |

61+ personas available in `references/persona-library.md`.

Each persona's SOUL.md is also enriched with community-validated prompts from [prompts.chat](https://prompts.chat) — searched by job function, not by name.

---

## Team Sizing

The skill determines team size from your actual workflow:

- **1 Worker** → No Manager needed. Main Agent handles QA directly.
- **2–4 Workers** → Standard setup. Manager orchestrates and quality-checks.
- **5+ Workers** → Split into sub-teams (Manager managing Managers).

You're not picking from a fixed template — the team is designed around what you actually do.

---

## QA Gate

Every deliverable goes through a mandatory quality check before you see it:

```
Worker finishes → Manager self-checks against requirements
    ├─ Fail → Worker revises (up to 3 rounds) → re-check
    └─ Pass → Has a dedicated reviewer Worker?
                ├─ Yes + complex task → Send to reviewer
                │    ├─ Pass → Report to Main
                │    └─ Fail → Revise (up to 2 rounds) → escalate if still failing
                └─ No / simple task → Report to Main directly
```

Main Agent verifies the QA status is present before relaying results to you. If it's missing, it asks the Manager to confirm.

---

## Wisdom

Agents learn from each task. When a Worker discovers something reusable, it gets saved:

```
~/.openclaw/workspace/memory/wisdom/
├── conventions.md   ← Team-wide agreements
├── successes.md     ← Approaches worth repeating
├── failures.md      ← Mistakes not to repeat
└── gotchas.md       ← Non-obvious traps
```

On future tasks, relevant Wisdom entries are injected into the message — both when Main sends to Manager, and when Manager sends to Workers.

---

## Adjusting an Existing Team

Already have a team? The skill handles all cases:

| Situation | What happens |
|-----------|-------------|
| Team is healthy | Asks: work now, adjust, or rebuild? |
| Team has config issues | Shows what's broken, offers fixes |
| Add a Worker | Runs persona selection for the new role only |
| Remove a Worker | Updates config and Manager's roster |
| Full rebuild | Backs up first, then restarts from interview |

---

## Requirements

- OpenClaw with persistent multi-Agent support
- At least one model configured in `openclaw.json`
- `tools.sessions.visibility: "all"` and `tools.agentToAgent.enabled: true`

See `INSTALL.md` for full configuration steps.

---

## License

MIT

---
name: litmus
version: 1.1.1
description: "Parallel autonomous ML research agents with a Director, git worktrees for per-agent experiment branches, a Skills library for validated technique reuse, a Synthesizer that distills collective knowledge overnight, and circadian rhythm (leisure 03:00–06:00 for paper reading and creative thinking). Uses OpenClaw sessions_spawn, cron, and steer natively. Use when: (1) start or run ML research agents overnight, (2) check agent status or experiment results, (3) view leaderboard or morning digest, (4) steer or stop agents, (5) ask what agents discovered or are exploring, (6) set up Litmus for the first time. NOT for: general coding, non-ML tasks, or machines without a GPU."
homepage: https://github.com/kuberwastaken/litmus
source: https://github.com/kuberwastaken/litmus
license: MIT-0
tags: [research, ml, machine-learning, training, autonomous-agents, overnight, experiments, gpu, llm, autoresearch]
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins: ["uv", "git", "python3"]
    recommends:
      bins: ["nvidia-smi"]
    os: [linux, darwin]
    configPaths: ["~/.litmus/"]
    optional:
      env: ["CLAWRXIV_API_KEY"]
---

# Litmus — Parallel Autonomous ML Research Agents

Litmus spawns multiple OpenClaw subagents that experiment on your GPU overnight. Each runs on its
own **git branch** in a shared lab repository — every experiment is a commit, agents can read
each other's code, cherry-pick breakthroughs, and build on the global best at any time.

Validated techniques accumulate in a **Skills library** (`~/.litmus/shared/skills/`). A
**Synthesizer** runs at 04:00 to distill collective knowledge into skills and write a research
agenda for the next day. A **Director** runs every 2 hours to steer workers, trigger **Compass
Resets** on stagnation, and orchestrate cross-agent knowledge transfer.

**What makes it more than autoresearch**:
- Git worktrees: agents share one repo, each on their own branch — full experiment history,
  cherry-pick, and cross-agent code inspection via `git -C ~/.litmus/repo log --all`
- Skills library: validated techniques persist and compound — agents don't re-discover wins
- Synthesizer: distills all overnight notes into reusable skills and a research agenda
- Compass Reset: Director detects stagnation and forces structured pivots using the skills gap
- Two-phase experiment budget: quick 90-second check before committing to a full run
- Structured attempt records: JSON per experiment in `shared/attempts/` for rich analytics
- Leisure mode (03:00–06:00): workers read papers, write moonshot hypotheses, identify gaps
- Morning digest: research narrative delivered to your chat at 08:00

Everything is a native OpenClaw subagent. No external processes, no PID files.

---

## First-Time Setup

**Recommended** — ask your OpenClaw agent (runs a guided onboarding conversation):
> "Install https://clawhub.ai/kuberwastaken/litmus and set it up for my machine"

Full onboarding instructions: `{baseDir}/references/onboarding.md` — read that file first.

**Or manually:**
```bash
git clone https://github.com/kuberwastaken/litmus ~/.litmus
bash ~/.litmus/scripts/setup.sh
```

Clones Karpathy's training harness, builds the shared lab git repo at `~/.litmus/repo/`,
installs Python deps via `uv`, downloads ~1 GB of training data. Wait for it to finish.

---

## Starting Research

### 1 — Prepare workspaces (creates git worktrees)

```bash
bash {baseDir}/scripts/prepare-agents.sh --agents 4 --templates architecture,optimizer,general,general
```

Creates git worktrees under `~/.litmus/agents/`, each on its own branch in `~/.litmus/repo/`.
The shared lab git repo means every agent's experiments are immediately visible to all others:
```bash
git -C ~/.litmus/repo log --all --oneline --graph
```

### 2 — Spawn research subagents

```
sessions_spawn
  task: "Read program.md in your current directory and run the research loop forever."
  runtime: "subagent"
  mode: "session"
  agentId: "litmus-worker-arch-1"
  cwd: "~/.litmus/agents/arch-1"
```

Repeat for each agent, then:
```
sessions_yield message: "Research agents running. I'll notify you on new discoveries."
```

**Templates**: `architecture` · `optimizer` · `regularization` · `general`
Full template details: `{baseDir}/references/templates/`

### 3 — Start the Director Layer

```bash
bash {baseDir}/scripts/setup-cron.sh --timezone "Your/Timezone"
```

Registers 6 cron jobs:

| Cron | Default schedule | Role |
|---|---|---|
| `litmus-director` | Every 2h during research hours | Reviews results, steers workers, Compass Reset on stagnation |
| `litmus-leisure` | 03:00 daily | Switches workers to paper-reading / creative thinking mode |
| `litmus-synthesizer` | 04:00 daily | Distills notes into skills library, writes research agenda |
| `litmus-dawn` | 06:00 daily | Wakes workers, queues synthesizer's priority experiments |
| `litmus-watchdog` | Every 30 min | Liveness check, escape mode on zero improvements |
| `litmus-digest` | 08:00 daily | Morning research narrative delivered to your chat |

All times are configurable during onboarding — the setup agent pitches defaults and asks what you'd like to change. Common presets: night owl (01:00/02:00/04:00/07:00), early bird (23:00/00:30/02:00/05:30), intensive (1h director). Pass custom times to `scripts/setup-cron.sh` with `--leisure-start`, `--synthesizer-time`, `--dawn-time`, `--digest-time`, `--director-hours`, `--watchdog-minutes`.

---

## Managing Agents

**Status** (experiment counts, best val_bpb, git tree):
```bash
bash {baseDir}/scripts/status.sh
```

**Leaderboard** (cross-agent, from shared/attempts/ JSON):
```bash
bash {baseDir}/scripts/results.sh --top 10
bash {baseDir}/scripts/results.sh --agent arch-1  # single agent
```

**Full lab git history** (all agents' experiments as a tree):
```bash
git -C ~/.litmus/repo log --all --oneline --graph
```

**Inspect any experiment**:
```bash
git -C ~/.litmus/repo show <commit-hash>  # see what changed
cat ~/.litmus/shared/attempts/<hash>.json  # see the metrics
```

**Steer** (redirect mid-run, no restart):
```
subagents action: "steer"  target: "litmus-worker-arch-1"
  message: "Stop refining depth. Checkout the best commit from opt-2 and combine their LR with DEPTH=10."
```

**Stop**:
```
subagents action: "kill"  target: "all"
```

---

## What Agents Write Overnight

| Path | Contents |
|---|---|
| `~/.litmus/shared/attempts/<hash>.json` | Structured record for every experiment (agent, val_bpb, status, title) |
| `~/.litmus/shared/skills/<name>.md` | Validated reusable techniques with YAML frontmatter |
| `~/.litmus/shared/notes/discoveries/` | Per-improvement discovery notes |
| `~/.litmus/shared/notes/anomalies/` | Unexpected result notes |
| `~/.litmus/shared/notes/moonshots/` | Speculative hypotheses from leisure |
| `~/.litmus/shared/notes/synthesis/` | Synthesizer's research agenda and combination matrix |
| `~/.litmus/shared/discoveries.md` | Cross-agent knowledge base (flat, for quick reading) |
| `~/.litmus/shared/midnight-reflections.md` | Leisure agent's nightly narrative |
| `~/.litmus/repo/` (git) | All experiment commits across all agents on their branches |

---

## Reference Files

- `{baseDir}/references/onboarding.md` — first-time setup conversation
- `{baseDir}/references/program.md` — worker agent loop (git-aware, skills-reading, two-phase budget)
- `{baseDir}/references/director.md` — Director cron (Compass Reset, cross-pollination)
- `{baseDir}/references/leisure.md` — Leisure mode (paper reading, structured notes, skill extraction)
- `{baseDir}/references/synthesizer.md` — Synthesizer cron (knowledge distillation, skills library)
- `{baseDir}/references/dawn.md` — Dawn cron (wake workers, queue experiments)
- `{baseDir}/references/watchdog.md` — Watchdog cron (liveness, escape mode)
- `{baseDir}/references/digest.md` — Morning digest (research narrative)
- `{baseDir}/references/templates/` — Research focus templates
- `{baseDir}/references/clawrxiv.md` — ClawRxiv integration (optional auto-publishing)

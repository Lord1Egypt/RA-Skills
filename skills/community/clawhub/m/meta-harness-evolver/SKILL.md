---
name: meta-harness-evolver
description: End-to-end Meta-Harness evolution for Hoss (OpenClaw agent). Runs nightly at 3 AM via OpenClaw cron. Reads Hoss's current workspace configs (SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md, MEMORY.md), proposes harness modifications via a coding-agent proposer, evaluates against a benchmark, logs results to ~/hoss-evolution/, and posts a summary to the #research Discord channel. Triggered: (1) automatically via cron at 3 AM CDT, (2) when Tyler says "run harness evolution", "evolve Hoss", or "run meta-harness".
---

# Meta-Harness Evolver

## What This Skill Does

Implements the **Meta-Harness** paper's outer-loop optimization for Hoss — your OpenClaw agent. Each night at 3 AM CDT, this skill:

1. **Reads** Hoss's current workspace configs + all prior evolution logs
2. **Proposes** a targeted harness modification via a coding-agent sub-agent
3. **Evaluates** the proposed harness against a benchmark of ~20 diverse task scenarios
4. **Logs** the candidate harness + scores + execution traces to the evolution filesystem
5. **Posts** a summary report to #research Discord channel

## The Meta-Harness Loop

```
Proposer Agent ──(filesystem access)──► Hoss Workspace
      ▲                                   │
      │                          propose harness
      │                                   ▼
      │                          Evaluate on benchmark
      │                                   ▼
log ───┴── store: code + scores + traces ──► ~/hoss-evolution/
```

## Quick Start

### Cron Schedule
- **3 AM CDT daily** — configured via `openclaw cron`
- Cron command: `SKILL=meta-harness-evolution TASK=run_evolution openclaw run`

### Manual Trigger
```
/openclaw run --skill meta-harness-evolver --task run_evolution
```

## Directory Structure

```
~/hoss-evolution/
├── best/                  # Best harness found so far
│   └── current/
├── candidates/            # All evaluated harnesses
│   └── candidate_N/       # One dir per candidate
│       ├── harness/      # The proposed config files (SOUL.md, etc.)
│       ├── eval_scores.json
│       └── traces/        # Execution traces
├── benchmark/             # Evaluation tasks + scorer
│   └── scenarios/         # ~20 diverse task scenarios
├── proposer/              # Proposer's workspace
│   └── logs/              # Proposer's own reasoning traces
└── evolution_log.jsonl    # Full run history
```

## What Can Be Evolved

Hoss's "harness" = the configs that wrap the LLM brain:

| File | What It Controls |
|------|-----------------|
| `SOUL.md` | Core identity, personality, decision-making style |
| `IDENTITY.md` | Role, voice, tone, signature patterns |
| `AGENTS.md` | Sub-agent architecture, coordination protocol |
| `TOOLS.md` | Tool configurations, credentials, key hosts |
| `MEMORY.md` | Long-term memory structure, what to persist |
| `HEARTBEAT.md` | Active hours, check priorities, alert thresholds |

**Constraints (do NOT modify):**
- Credentials, API keys, or secrets in TOOLS.md
- Git safety rules (NEVER mutate git config from ~/flume/)
- Security-sensitive groupPolicy settings

## The Evolution Algorithm

1. **Seed**: Start with Hoss's current configs as iteration 0
2. **Propose**: Sub-agent reads full history from ~/hoss-evolution/candidates/, identifies failure patterns, proposes 1-2 targeted edits
3. **Validate**: Lightweight import/syntax check before running full benchmark
4. **Evaluate**: Run proposed harness against all 20 benchmark scenarios, score each
5. **Log**: Store candidate harness + scores + proposer reasoning traces
6. **Select**: Pareto frontier over (performance, simplicity) — proposer decides which candidates to keep exploring from
7. **Repeat**: Next night's proposer can read ALL prior candidates to build on good ideas

### Key Insight from the Paper
The **skill text is the strongest lever** — it steers the proposer. Iterating on the proposer's prompt/role description had more effect than changing iteration count or population size.

## The Benchmark

The benchmark lives at `~/hoss-evolution/benchmark/`. See [references/benchmark-design.md](references/benchmark-design.md) for how to design scenarios and [references/harness-spec.md](references/harness-spec.md) for the full harness spec.

Default benchmark has **20 scenarios** across categories:
- **Memory**: Recall, update, synthesize from memory files
- **Code**: Write, review, debug code tasks
- **Coordination**: Spawn sub-agents, synthesize results
- **Research**: Web search, fetch, summarize, synthesize
- **Communication**: Draft emails, Discord messages, iMessages
- **Quality**: Spot errors, inconsistencies, broken links

Each scenario has:
- A concrete task description
- Expected outcome criteria
- A scoring rubric (0-3 per scenario: fail / partial / pass / excellent)

## The Proposer Agent

The proposer is a **coding-agent sub-agent** (default: coder) that:
- Reads all prior candidates from `~/hoss-evolution/candidates/` via filesystem ops
- Identifies patterns in failed/succeeded candidates
- Proposes targeted, specific edits (NOT wholesale rewrites)
- Writes proposed configs to the new candidate directory
- Logs its reasoning trace so future iterations can build on it

### Proposer Skill (passed to sub-agent)

The proposer's role is defined by the task prompt in `scripts/propose_harness.py`. Key constraints:
- Can only propose edits to files in the harness spec (SOUL.md, IDENTITY.md, AGENTS.md, TOOLS.md, MEMORY.md, HEARTBEAT.md)
- Must pass lightweight validation before full evaluation
- Should prefer targeted edits over full rewrites
- Must log reasoning trace to proposer/logs/

## Workflow Steps

### Step 1: Read Prior Candidates
```bash
# List all prior candidates
ls ~/hoss-evolution/candidates/

# Read best candidate
cat ~/hoss-evolution/best/current/eval_scores.json

# Read history log
tail -20 ~/hoss-evolution/evolution_log.jsonl
```

### Step 2: Run Proposer
```bash
# The sub-agent proposer reads ~/hoss-evolution/ and proposes
# This is triggered by openclaw run with this skill loaded
```

### Step 3: Validate Before Benchmark
```bash
# Quick syntax check
bash ~/hoss-evolution/scripts/validate.sh <candidate_dir>
```

### Step 4: Run Benchmark
```bash
# Evaluate candidate against all 20 scenarios
python3 ~/hoss-evolution/scripts/evaluate.py <candidate_dir>
```

### Step 5: Log Results
```bash
# Scores + traces written to candidate dir automatically
# Evolution log updated
```

### Step 6: Post to Discord
```bash
# Posts summary to #research
python3 ~/hoss-evolution/scripts/post_to_research.py <candidate_dir>
```

## Scoring

Final score = weighted average across scenarios:
- Memory tasks: 25%
- Code tasks: 25%
- Coordination: 15%
- Research: 20%
- Communication: 10%
- Quality: 5%

Results are tracked as a Pareto frontier: for each candidate, log both score and "complexity" (size/diff of changes). Simpler harnesses that score equally get priority.

## Resources

- [references/harness-spec.md](references/harness-spec.md) — Full spec of what constitutes Hoss's harness, what can/cannot be modified
- [references/benchmark-design.md](references/benchmark-design.md) — How to design benchmark scenarios, scoring rubrics, how to add new scenarios
- [references/evolution-logic.md](references/evolution-logic.md) — Detailed evolution algorithm, parent selection, Pareto frontier logic
- [scripts/run_evolution.py](scripts/run_evolution.py) — Main entry point, runs the full loop
- [scripts/propose_harness.py](scripts/propose_harness.py) — The proposer sub-agent task definition
- [scripts/evaluate.py](scripts/evaluate.py) — Benchmark runner
- [scripts/post_to_research.py](scripts/post_to_research.py) — Discord reporter

## Notes

- The proposer sub-agent runs with `runtime=subagent`, not ACP — it needs filesystem access to ~/hoss-evolution/
- Cron is configured outside this skill via `openclaw cron`
- If the proposer fails to produce a valid candidate, the iteration is skipped (no penalty)
- Benchmark scenarios should be diverse enough that no single strategy can game all of them
- The evolution workspace is NOT inside ~/.openclaw/ — it's at ~/hoss-evolution/ to keep it separate from operational configs

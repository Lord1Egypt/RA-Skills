---
name: goal-agent
description: >
  Scaffold a self-learning goal-oriented agent. Set a goal, define a metric, and the
  agent iterates toward it — measuring, learning, and adapting its strategy at every
  heartbeat until the goal is met.
---

# goal-agent

## Overview

The goal-agent skill creates a workspace that turns an OpenClaw agent into a focused, autonomous optimizer. You give it a goal and a shell command that measures progress — the agent does the rest, iterating heartbeat by heartbeat, learning what works and what doesn't.

---

## Usage

### Step 1: Collect inputs

| Input | Flag | Required | Default |
|-------|------|----------|---------|
| Goal description | `--goal` | ✅ | — |
| Metric command (returns a number) | `--metric` | ✅ | — |
| Target value | `--target` | ✅ | — |
| Direction (up/down) | `--direction` | ❌ | `up` |
| Safety constraints | `--constraints` | ❌ | `None` |
| Max iterations | `--max-iterations` | ❌ | `50` |
| Output directory | `--output-dir` | ❌ | `./` |

### Step 2: Run scaffold.sh

```bash
bash ~/clawd/skills/goal-agent/scripts/scaffold.sh \
  --goal "Increase daily active users to 100" \
  --metric "cat /tmp/my-metric.json | jq '.dau'" \
  --target 100 \
  --direction up \
  --constraints "Do not modify the database schema. Stay within $50/day budget." \
  --max-iterations 30 \
  --output-dir ~/clawd/goals/dau-growth
```

This generates the following files in `--output-dir`:
- `GOAL.md` — goal definition, iteration counter, history table
- `STRATEGY.md` — current approach, hypotheses, next action
- `LEARNINGS.md` — rules extracted from experience
- `HEARTBEAT.md` — the feedback loop instructions (replaces main HEARTBEAT.md)
- `evaluate.sh` — runnable metric evaluator

### Step 3: Activate the feedback loop

The generated `HEARTBEAT.md` **is** the goal-agent loop. Each heartbeat, the agent:
1. Measures the metric
2. Compares against target and history
3. Reflects on what worked/didn't
4. Decides the next action
5. Acts
6. Records results
7. Adapts strategy

**To activate:** Copy `HEARTBEAT.md` to `~/clawd/HEARTBEAT.md` (or symlink it):
```bash
cp ~/clawd/goals/dau-growth/HEARTBEAT.md ~/clawd/HEARTBEAT.md
```

### Step 4: Deploy options

**Option A — Current agent (fastest)**
Copy all generated files into your workspace and activate HEARTBEAT.md as above.

**Option B — Dedicated VM (cleanest)**
Use the `spawn-agent` skill to create a fresh agent VM, then copy the goal workspace there:
```bash
# On the new agent
scp -r ~/clawd/goals/dau-growth/ ubuntu@new-agent:~/clawd/goals/
ssh ubuntu@new-agent "cp ~/clawd/goals/dau-growth/HEARTBEAT.md ~/clawd/HEARTBEAT.md"
```

---

## Examples

### Example 1: Optimize test coverage
```bash
bash ~/clawd/skills/goal-agent/scripts/scaffold.sh \
  --goal "Increase test coverage to 80%" \
  --metric "cd ~/myproject && npx jest --coverage --coverageReporters=text-summary 2>/dev/null | grep 'Statements' | grep -oP '\d+\.\d+(?=%)'" \
  --target 80 \
  --direction up \
  --max-iterations 20 \
  --output-dir ~/clawd/goals/test-coverage
```

### Example 2: Reduce build time
```bash
bash ~/clawd/skills/goal-agent/scripts/scaffold.sh \
  --goal "Reduce build time to under 30 seconds" \
  --metric "cd ~/myproject && time npm run build 2>&1 | grep real | grep -oP '\d+\.\d+'" \
  --target 30 \
  --direction down \
  --constraints "Do not remove any build steps. Do not break production builds." \
  --output-dir ~/clawd/goals/build-speed
```

### Example 3: Grow social followers
```bash
bash ~/clawd/skills/goal-agent/scripts/scaffold.sh \
  --goal "Reach 500 Twitter followers" \
  --metric "~/.openclaw/scripts/twitter-follower-count.sh" \
  --target 500 \
  --direction up \
  --constraints "Only post authentic content. No follow-for-follow schemes." \
  --output-dir ~/clawd/goals/twitter-growth
```

---

## Safety & Sandboxing

**Before activating a goal-agent loop, review these guidelines:**

- **Review generated files before activating.** Always read the generated `HEARTBEAT.md` and `evaluate.sh` before copying them into your workspace. Confirm the metric command and constraints are what you intended.
- **Use `--constraints` to limit scope.** The agent will only take actions within the constraints you define. Be explicit: "Only modify files in ~/myproject/src", "Do not make network requests", "Do not delete files".
- **Set a low `--max-iterations` for first runs.** Start with 5-10 to observe behavior before allowing longer runs.
- **Prefer dedicated VMs for autonomous goals.** Use `spawn-agent` to isolate goal-agents from your main workspace. This limits blast radius if the agent takes unexpected actions.
- **Metric commands should be read-only.** The `--metric` command should only *measure* — never modify state. Use simple commands like `cat`, `wc`, `jq`, `grep`.
- **The "Act" step is constrained by text, not code.** The agent follows the constraints you set in `--constraints`, but there is no programmatic sandbox. For high-stakes goals, combine with filesystem permissions, network egress controls, or a restricted user account.
- **Monitor early iterations.** Check `GOAL.md` history after the first few heartbeats to verify the agent is behaving as expected.

---

## How it works

The `HEARTBEAT.md` implements a tight cognitive loop:

```
Measure → Compare → Reflect → Decide → Act → Record → Adapt
    ↑___________________________________________________|
```

Each iteration, the agent reads its own history (`GOAL.md`), its current understanding (`STRATEGY.md`), and accumulated wisdom (`LEARNINGS.md`) before taking action. Over time it builds a library of what works for your specific goal.

---

## Files reference

| File | Purpose | Agent modifies? |
|------|---------|----------------|
| `GOAL.md` | Source of truth: goal, metric, target, history | Status + History only |
| `STRATEGY.md` | Current plan, hypotheses, next action | Yes (every iteration) |
| `LEARNINGS.md` | Extracted rules and patterns | Yes (as it learns) |
| `HEARTBEAT.md` | Loop instructions | No |
| `evaluate.sh` | Runnable metric command | No |

---

## Skill location
`~/clawd/skills/goal-agent/`

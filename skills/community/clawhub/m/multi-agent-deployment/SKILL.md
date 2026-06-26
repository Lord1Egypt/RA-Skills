---
name: Multi-Agent Deployment Skill for OpenClaw
slug: multi-agent-deployment
version: 1.0.1
description: "Deploy a production-ready multi-agent fleet in OpenClaw. Includes step-by-step setup guide, workspace templates, and Python automation scripts for agent creation, routing config, memory sync, and cloud deployment — based on a real working 4-agent production setup."
---

## What This Skill Does

Guides you through deploying 3-5 specialized AI agents in OpenClaw that work as a coordinated fleet. Based on a real production setup running on a Hostinger VPS with Docker.

## Included Files

| File | Purpose |
|------|---------|
| `agent_setup.py` | Creates workspace directory structure for any number of agents |
| `routing_config.py` | Generates openclaw.json agent entries with model routing and fallbacks |
| `memory_sync.py` | Syncs Cross-Agent Intel sections across all agent MEMORY.md files |
| `deploy.sh` | Uploads workspace files to VPS and restarts the container |

## Step-by-Step Setup

### 1. Create Workspace Structure
```bash
python3 agent_setup.py --agents pat scout publisher builder --base /data/.openclaw
```
Creates a `workspace-{agent}/` folder with SOUL, memory, drafts, skills, and Claude settings scaffolding.

### 2. Define Each Agent's Role
Edit each workspace's SOUL file:
- Set the agent's mission and responsibilities
- Define which tools it uses
- Add hard limits and escalation rules

### 3. Generate Routing Config
```bash
# Preview output
python3 routing_config.py --agents main scout publisher builder

# Write directly to openclaw.json
python3 routing_config.py --agents main scout publisher builder \
  --output /data/.openclaw/openclaw.json
```
Configures model routing with OpenRouter fallbacks (minimax → deepseek → kimi).

### 4. Set Up Cron Jobs
Add a recurring cron job for each agent, for example:
```json
{
  "name": "Agent: Daily Run",
  "agentId": "scout",
  "schedule": { "expr": "0 10 * * *" },
  "enabled": true
}
```

### 5. Deploy to VPS
```bash
bash deploy.sh --vps root@your-vps-ip --key ~/.ssh/your_key
```

### 6. Sync Agent Memory
Run nightly or manually to propagate cross-agent intelligence:
```bash
python3 memory_sync.py --base /data/.openclaw --agents pat scout publisher builder
```

## Architecture Pattern

```
Coordinator (main) — always-on Telegram, approval queue, briefings
    ├── Scout       — market intel, inbound monitoring, trends
    ├── Publisher   — content drafts for Twitter/LinkedIn/video
    └── Builder     — skill development, marketplace research
```

Each agent has:
- Isolated workspace with its own SOUL.md and memory
- Separate cron schedule
- Model routing with fallbacks via OpenRouter
- Shared memory sync via Cross-Agent Intel

## Requirements

- OpenClaw running on a VPS (Docker)
- OpenRouter API key (for model routing)
- SSH access to your VPS

## Ideal Buyer

This skill is for operators who already know they want multiple agents, but do not want to hand-assemble workspace scaffolding, routing config, memory propagation, and deployment steps from scattered docs.

## Example Use Cases

- Build a 4-agent content + research + build + coordinator setup
- Split a single overloaded assistant into role-specific workspaces
- Stand up a VPS-hosted OpenClaw fleet with shared memory conventions

## Expected Outcome

By the end of this skill, you should have:
- Generated workspace scaffolding for each agent
- A reusable routing config pattern with model fallbacks
- A repeatable memory sync workflow across agents
- A deployment script you can adapt for your own VPS

## What Makes This Different

- **Real production patterns** — not examples, this is a live setup
- **Isolation by design** — each agent has its own workspace and memory
- **Fallback routing** — agents keep running if a model goes down
- **Memory persistence** — agents remember context across sessions and compaction

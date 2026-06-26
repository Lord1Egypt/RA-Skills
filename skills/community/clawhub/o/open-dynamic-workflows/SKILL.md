---
name: open-dynamic-workflows
description: Plan, orchestrate, and adversarially verify parallel AI coding agents — a dynamic multi-agent workflow engine.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env: [ANTHROPIC_API_KEY]
      bins: [node]
    primaryEnv: ANTHROPIC_API_KEY
---

# Open Dynamic Workflows (OpenClaw)

Run dynamic, multi-agent workflows from OpenClaw via the local Open Dynamic Workflows (ODW) daemon. ODW plans a task, orchestrates parallel agents, and adversarially verifies their output before it lands. Bring your own model (Anthropic, any OpenAI-compatible endpoint, or local Ollama).

## When to use

- A task that splits into many independent subtasks worth running in parallel.
- Anything that should be **verified** (adversarial critics) before you trust it.
- Work you want to share across OpenClaw, OpenCode, Codex, Antigravity, and VS Code through one orchestration layer.

## Step 0 — is the daemon up?

```bash
node scripts/daemon-bridge.js --check
```

- Exit 0 → daemon healthy; use the daemon path below.
- Exit 1 → install + start it (it is not on npm yet):

```bash
git clone https://github.com/Suraj1235/open-dynamic-workflows
cd open-dynamic-workflows && npm install && npm run setup
odw-daemon start
```

## Daemon path

1. **Plan** — `node scripts/daemon-bridge.js plan "<task>"` prints a JSON plan: task graph, topology, roles, hard limits, cost/time estimate.
2. **Confirm** — summarize topology / agent count / estimate before doing anything beyond read-only work.
3. **Execute** — `node scripts/daemon-bridge.js exec plan.json` returns a `wf_...` id; the daemon runs the sandboxed script with concurrent agents, SQLite checkpoints, crash-resume, and a budget hard-stop.
4. **Report** — `node scripts/daemon-bridge.js result <wf_id>` blocks until done; relay the synthesized result.

## Safety

- Read-only tools are auto-approved; file writes, shell, and git are approval-gated by ODW's config — never mutate without authorization.
- Model provider keys live in the environment / `~/.odw/config.json`, never in prompts or source.
- Respect the per-workflow token/cost budget.

## Notes

Same canonical skill as the Codex/Antigravity adapters — only the install path differs. The bundled `scripts/daemon-bridge.js` is a zero-dependency CommonJS bridge to the daemon's local HTTP API.

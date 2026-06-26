---
name: Paperclip
slug: paperclip
version: 1.0.0
homepage: https://clawic.com/skills/paperclip
description: Run Paperclip locally for agent orchestration, AI company setup, and OpenClaw, Codex, or Claude control-plane operations.
changelog: "Added local-first Paperclip operations, adapter selection, and OpenClaw integration guidance."
metadata: {"clawdbot":{"emoji":"📎","requires":{"bins":["curl","pnpm"],"env":{"optional":["PAPERCLIP_API_URL","PAPERCLIP_API_KEY","PAPERCLIP_COMPANY_ID","PAPERCLIP_RUN_ID","OPENAI_API_KEY","ANTHROPIC_API_KEY","OPENCLAW_GATEWAY_TOKEN"]},"config":["~/paperclip/","~/.paperclip/instances/"]},"os":["linux","darwin","win32"],"configPaths":["~/paperclip/","~/.paperclip/instances/"]}}
---

## Setup

On first use, read `setup.md` for integration guidance.

## When to Use

User needs to install, operate, or evaluate Paperclip as the control plane for a team of AI agents. Use for local-first setup, agent-company design, adapter selection, OpenClaw integration, CLI operations, and API-based coordination.

## Architecture

Skill memory lives in `~/paperclip/`. Paperclip application data usually lives in `~/.paperclip/instances/`. If `~/paperclip/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/paperclip/
├── memory.md            # Operator context, active instances, adapter preferences
├── companies.md         # Company names, goals, and status snapshots
├── commands.md          # Reused CLI/API snippets that worked
└── notes.md             # Open questions, blockers, migration notes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Local bootstrap | `quickstart.md` |
| Adapter selection | `adapters.md` |
| Daily operator commands | `operations.md` |
| OpenClaw integration | `openclaw.md` |

## Requirements

- Node.js 20+ for the official `paperclipai` package and local server
- pnpm 9.15+ for repo-based workflows
- `curl` for direct API checks and automation
- Provider credentials only for the adapters the user chooses to run

## Core Rules

### 1. Treat Paperclip as the control plane
- Use Paperclip to organize companies, agents, goals, issues, approvals, and budgets.
- Do not treat it as the domain worker itself; the actual work is done by the attached runtimes.

### 2. Start local-first unless the user already has infrastructure
- Prefer `npx paperclipai onboard --yes` for the first working instance.
- Use `--data-dir` when testing in a throwaway environment or when isolation matters.

### 3. Model the company before spawning workers
- Define company goal, reporting lines, workspaces, and issue flow before waking multiple agents.
- Paperclip becomes valuable when ownership, budgets, and escalation paths are explicit.

### 4. Pick adapters by execution boundary
- Use `codex_local` or `claude_local` when the agent should run on the same host as Paperclip.
- Use `openclaw_gateway` when OpenClaw lives outside the control plane and should be hired as an employee.

### 5. Lean on heartbeats, approvals, and budgets
- Heartbeats are the default execution loop; agents do not need to run continuously to stay coordinated.
- Approval gates and spend caps are core operating controls, not optional extras.

### 6. Use CLI and API for repeatable operations
- Prefer small, auditable commands for creating companies, issues, approvals, and wakeups.
- Keep human chat in OpenClaw, Codex, or Claude if that is the preferred interface, while Paperclip remains the source of truth.

## Common Traps

- Treating Paperclip like a chatbot UI -> you miss the org chart, governance, and cost-control layer that makes it useful.
- Starting many agents before defining reports-to, workspaces, and budgets -> the system devolves into unmanaged parallel tabs.
- Using `localhost` from inside OpenClaw Docker -> the container points to itself, not the Paperclip host.
- Expecting Codex or Claude adapters to work without the local CLI installed and authenticated -> heartbeats fail before useful work starts.
- Skipping issue checkout semantics -> multiple agents can step on the same task outside the Paperclip workflow.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `http://localhost:3100/api` or configured Paperclip API base | Company, agent, issue, approval, and run metadata | Control-plane reads and writes |
| `ws://127.0.0.1:18789` or configured OpenClaw gateway URL | Wake payloads, session routing, streamed agent events | OpenClaw adapter transport |

No other endpoints should be contacted unless the user explicitly configures remote deployments or model providers.

## Security & Privacy

**Data that leaves your machine:**
- Requests to the user-selected Paperclip API base
- Requests to the configured OpenClaw gateway when that adapter is enabled
- Any provider traffic created by the agent runtimes the user installs and authorizes

**Data that stays local:**
- Paperclip instance state in `~/.paperclip/instances/`
- Skill memory in `~/paperclip/`
- Local workspaces attached to projects

**This skill does NOT:**
- Require a Paperclip cloud account
- Expose secrets in commands or memory files
- Assume a public deployment by default

## Trust

By using this skill, operational data is sent to the Paperclip deployment and agent adapters the user configures.
Only install if you trust that deployment, its storage, and the model providers behind those agents.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `agent` — General agent execution and delegation patterns
- `agents` — Multi-agent coordination and role design
- `company` — Company-level strategy and operating structure
- `workflow` — Repeatable operational workflows and handoffs
- `api` — Direct API usage, payload design, and HTTP troubleshooting

## Feedback

- If useful: `clawhub star paperclip`
- Stay updated: `clawhub sync`

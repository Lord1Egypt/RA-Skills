# OpenClaw Integration — Paperclip

## What Actually Fits Best

If the user wants to keep talking through OpenClaw, Paperclip should usually stay behind the scenes as the control plane. OpenClaw becomes one employee or one operator surface, not the replacement for Paperclip's org, issue, approval, and budget system.

## Recommended Modes

| Mode | Use when | Result |
|------|----------|--------|
| OpenClaw as employee | OpenClaw should execute tasks autonomously inside a company | Paperclip owns the company state; OpenClaw receives work through the gateway |
| OpenClaw as human-facing shell | The user wants chat-first interaction while Paperclip tracks work | Keep source-of-truth issues, approvals, and budgets in Paperclip |
| Mixed company | OpenClaw, Codex, and Claude each have different roles | Paperclip coordinates all of them under one org chart |

## Core Workflow

1. Start a local Paperclip instance first.
2. Confirm the host URL OpenClaw can actually reach.
3. Add or invite the OpenClaw worker through the Paperclip workflow.
4. Keep work flowing through issues and heartbeats, not ad-hoc chat state.

## OpenClaw-Specific Commands

```bash
pnpm smoke:openclaw-join
pnpm smoke:openclaw-docker-ui
pnpm paperclipai allowed-hostname host.docker.internal
```

## Critical Docker Caveat

If OpenClaw runs in Docker, `127.0.0.1` points to the container, not the Paperclip host. Use the host alias printed by the smoke tooling, usually `host.docker.internal`.

## Invite Flow

Paperclip exposes an invite workflow for OpenClaw hires through:

```text
POST /api/companies/{companyId}/openclaw/invite-prompt
```

Use that when the board or CEO wants a copy-ready onboarding prompt instead of manual adapter wiring.

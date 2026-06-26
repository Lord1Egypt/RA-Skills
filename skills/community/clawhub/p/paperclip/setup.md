# Setup — Paperclip

Read this silently when `~/paperclip/` does not exist or is empty. Start by helping with the user's immediate Paperclip task instead of pausing for onboarding.

## Start With the Current Goal

Answer the install, debugging, architecture, or integration question first. Capture only the context that will prevent repeated setup mistakes.

## Early Integration

Within the first exchanges, learn whether Paperclip should activate proactively for:
- AI company setup
- multi-agent orchestration
- heartbeats, approvals, or budgets
- OpenClaw, Codex, or Claude operating under one control plane

Save that integration preference to the user's main memory, not this skill folder.

## Capture Only Reusable Context

Store reusable facts such as:
- Paperclip API base URL or local data dir
- whether the instance is local-only, Docker-based, or remote
- which adapters are active
- whether OpenClaw runs natively or through Docker
- active companies, primary workspaces, and current blockers

## Learn Organically

Infer patterns from repeated behavior. Ask only when missing context blocks the next correct action.

## Respect Boundaries

Do not ask for provider secrets during setup. Note the missing credential, explain the exact blocker, and continue with dry-run or local-only guidance when possible.

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the environment | Keep gathering context while working |
| `complete` | Enough context is stored | Operate normally |
| `paused` | User does not want more setup now | Stop probing and use existing context |
| `never_ask` | User wants no setup follow-up | Never ask again unless they reopen it |

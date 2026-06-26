---
name: openclaw-startup
version: 1.0.3
description: >
  First-run setup wizard for new OpenClaw agents. Interviews the user to generate a
  tailored SOUL.md, scaffolds memory architecture, installs recommended crons for
  operations and security, and recommends companion skills. Use when setting up a new
  OpenClaw agent from scratch, onboarding a new user, or resetting an agent to a clean
  baseline. Triggers on: "set up my agent", "first run", "new agent setup",
  "onboard me", "initialize workspace", "startup wizard", "help me get started".
author: Zye ⚡ (Don Zurbrick)
license: MIT
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["bash", "mkdir", "date"]
      optionalBins: ["openclaw", "clawhub"]
    platforms:
      - darwin
      - linux
---

# OpenClaw Startup

First-run setup wizard for new OpenClaw agents. Interviews the user, generates
tailored workspace files, scaffolds memory, installs operational crons, and
recommends companion skills.

## Use when

- setting up a new OpenClaw agent from scratch
- onboarding a new user who just installed OpenClaw
- resetting an agent workspace to a clean baseline
- someone says "set up my agent" or "help me get started"

## Do not use when

- the agent is already configured and running (use `openclaw-guide` instead)
- the user wants to change one specific config setting
- the task is skill authoring (use `skill-builder`)
- the task is security hardening of an existing agent (use `agent-hardening`)

## Phases

Run these in order. Each phase confirms with the user before proceeding.

### Phase 1 — Identity Interview

**Resuming a partial setup:** Before starting the interview, check if any of
`SOUL.md`, `USER.md`, or `IDENTITY.md` already exist. If they do, show the user
what's already configured and ask: "Want to pick up where we left off, start fresh,
or keep these and skip to memory setup?" Respect their choice.

Ask the user 8 questions to understand who they are and what the agent should do.
Use the interview guide at `references/interview-guide.md`.

From the answers, generate:
- `SOUL.md` — agent identity, personality, tone, boundaries
- `USER.md` — human's key details
- `IDENTITY.md` — agent name, emoji, presentation
- `AGENTS.md` — customized from `assets/agents-template.md` with principles
  tailored to the user's main job (Q4) and communication style (Q5)

Show the user the generated files and ask for approval before writing.

### Phase 2 — Memory Scaffolding

Run the install script to create the memory directory structure:

```bash
bash {baseDir}/scripts/install.sh
```

This creates:
- `memory/` directory with daily log structure
- `MEMORY.md` — durable fact index
- `ACTIVE.md` — current priorities tracker
- `memory/FUTURE_INTENTS.md` — commitments and deferred actions
- `.learnings/` — error and learning capture (agent-memory-loop)

### Phase 3 — Operational Crons

Review recommended crons with the user. See `references/cron-recipes.md`.

**If `openclaw` CLI is not available:** Skip cron installation. Instead, show the user
the recommended cron configs from `references/cron-recipes.md` and explain they can
install them later once OpenClaw is set up. Proceed to Phase 4.

**If `openclaw` CLI is available:**

**Always recommend:**
- Heartbeat (configurable frequency)
- Workspace backup (daily)

**Recommend if applicable:**
- Weekly memory consolidation
- Session health watchdog
- Security monitoring

Install only what the user approves. Use the OpenClaw cron tool directly.

### Phase 4 — Security Baseline

Walk through the security checklist at `references/security-baseline.md`.

Key items:
- Channel access controls (allowlist vs open)
- Injection defense rules in SOUL.md
- Escalation framework (green/yellow/red)
- Tool restrictions for sub-agents

### Phase 5 — Companion Skills

Recommend installing these skills based on the user's needs:

| Skill | When to recommend | ClawHub |
|-------|-------------------|---------|
| `cognition` | Always — memory architecture | [clawhub.com/skills/cognition](https://clawhub.com/skills/cognition) |
| `summarize` | Always — extract text/transcripts from URLs, videos, PDFs | [clawhub.com/skills/summarize](https://clawhub.com/skills/summarize) |
| `agent-hardening` | If the agent handles sensitive data or external channels | [clawhub.com/skills/agent-hardening](https://clawhub.com/skills/agent-hardening) |
| `openclaw-backup` | If the user wants disaster recovery | [clawhub.com/skills/openclaw-backup](https://clawhub.com/skills/openclaw-backup) |

Install via ClawHub if available:
```bash
clawhub install <skill-name>
```

### Phase 6 — Verification

After setup, run a quick health check:
- Verify all generated files exist and are non-empty
- Verify crons are registered and have valid next-run times
- Verify the agent can respond to a basic prompt
- Show the user a summary of everything that was set up

## Interview principles

- Ask one question at a time — don't dump all 8 at once
- Accept short answers — infer reasonable defaults from context
- Show what you're generating before writing it
- Never write to core files without user confirmation
- Keep the tone conversational, not bureaucratic

## References

- `references/interview-guide.md` — the 8 identity questions with guidance
- `references/cron-recipes.md` — recommended cron configurations
- `references/security-baseline.md` — security checklist for new agents
- `references/placeholder-map.md` — full mapping of interview answers → template placeholders + model recommendations

## Assets (templates)

- `assets/soul-template.md` — SOUL.md template with placeholders
- `assets/user-template.md` — USER.md template
- `assets/identity-template.md` — IDENTITY.md template
- `assets/agents-template.md` — AGENTS.md starter
- `assets/heartbeat-template.md` — HEARTBEAT.md starter

## Scripts

- `scripts/install.sh` — creates memory scaffolding and .learnings directory
- `scripts/verify.sh` — post-setup health check

---
name: project-bootstrap
description: Bootstrap a multi-agent software project from idea to running CI/CD. Use when starting a new project that needs agent team design, task management, GitHub repo setup, TDD pipeline, and Discord notifications. Triggers on "new project", "bootstrap project", "set up agents for project", "create project pipeline", "start a new repo with CI/CD".
---

# Project Bootstrap

Turn a project idea into a running multi-agent development pipeline in one session.

## Overview

This skill codifies the workflow for:
1. **Agent Team Design** — break complex work into specialized agents
2. **Taskboard Setup** — CLI-based task management across agents
3. **GitHub Repo + CI/CD** — TDD pipeline with Discord notifications

## Phase 1: Agent Team Design

### Analyze the Project

Before creating agents, answer these questions:
- What are the 3-5 major workstreams? (e.g., frontend, backend, research, design)
- Which workstreams need different expertise or thinking styles?
- What's the dependency graph between workstreams?

### Design Agent Roles

For each workstream, create an agent with a SOUL.md following this structure:

```markdown
# Agent Name — Nickname Emoji

You are **Nickname**, the [Role] — [one-line mission].

## 🧠 Identity & Memory
- **Role**: [specific expertise]
- **Personality**: [3-4 traits that affect work style]
- **Memory**: [what context files they track]
- **Experience**: [what failure modes they've seen]

## 🎯 Core Mission
[2-4 responsibility groups with specifics]

## 🚨 Critical Rules
[Non-negotiable constraints — security, process, boundaries]

## 📋 Deliverables
[Concrete outputs this agent produces]

## 🎯 Success Metrics
[How to measure if the agent is doing well]

## 💬 Communication Style
[How the agent communicates — tone, format, language]

## 🔗 Workflow Position
[Where in the pipeline: who feeds input, who receives output]
```

### Register Agents in Config

For each agent, add to `openclaw.json`:

```json
{
  "id": "agent-id",
  "name": "agent-id",
  "agentDir": "/path/to/workspace/agents/agent-id",
  "model": "model-alias",
  "tools": {
    "profile": "full",
    "deny": ["gateway"]
  }
}
```

Key decisions:
- **Model selection**: Use cheaper models (Haiku/Sonnet) for routine work, expensive (Opus) for architecture/review
- **Tool access**: Deny `gateway` for all agents except main. Deny `message` for pure code agents.
- **Subagent allowlist**: Main agent lists which agents it can spawn

### Wire Discord Bindings (if multi-bot)

If agents have separate Discord bots, add bindings:

```json
{
  "bindings": [
    { "agentId": "tech-lead", "match": { "channel": "discord", "accountId": "bot-name" } }
  ]
}
```

## Phase 2: Taskboard Setup

### Install Taskboard CLI

See `references/taskboard-setup.md` for the full taskboard CLI setup guide including:
- Task schema (id, title, status, assignee, priority, dependencies)
- CLI commands (create, list, assign, update, close)
- Cross-agent task handoff protocol
- Integration with cron jobs for status checks

### Task Lifecycle

```
📋 backlog → 🔄 in-progress → 👀 review → ✅ done
                ↓                  ↓
              🚫 blocked        ❌ rejected → 🔄 in-progress
```

### Cross-Agent Handoff

When an agent completes a task that feeds into another agent's work:
1. Update task status to `review`
2. Create a new task for the downstream agent referencing the completed task
3. Send notification to the downstream agent's Discord channel

## Phase 3: GitHub Repo + CI/CD

### Repository Setup

```bash
# Initialize repo
gh repo create <org>/<project> --private --clone
cd <project>

# Branch protection
gh api repos/<org>/<project>/rulesets -X POST --input .github/ruleset.json

# Required structure
mkdir -p .github/workflows tests src docs/adr
```

### TDD Pipeline

See `references/ci-cd-templates.md` for GitHub Actions workflow templates:
- **test.yml**: Run tests on every PR and push to main
- **lint.yml**: Code style checks
- **deploy.yml**: Deploy on merge to main (if applicable)

### Discord Notifications

Add Discord webhook to GitHub repo:

```bash
# Create webhook in Discord channel (Server Settings → Integrations → Webhooks)
# Add to GitHub: Settings → Webhooks → Add webhook
# Or use GitHub Actions:
```

See `references/ci-cd-templates.md` for the Discord notification action template.

### ADR (Architecture Decision Records)

Every significant technical decision gets an ADR:

```markdown
# ADR-NNN: [Title]

## Status: [proposed | accepted | deprecated | superseded]
## Context: [Why this decision is needed]
## Decision: [What we decided]
## Consequences: [Trade-offs and implications]
```

## Execution Checklist

Run through this for every new project:

- [ ] Define project scope and 3-5 workstreams
- [ ] Design agent SOUL.md for each workstream
- [ ] Register agents in openclaw.json
- [ ] Set up Discord channels per agent/workstream
- [ ] Create GitHub repo with branch protection
- [ ] Add CI/CD workflows (test + lint + deploy)
- [ ] Add Discord webhook for CI/CD notifications
- [ ] Initialize taskboard with backlog items
- [ ] Create first ADR (ADR-001: Project Architecture)
- [ ] Assign initial tasks to agents
- [ ] Run a test cycle: create task → agent executes → review → merge

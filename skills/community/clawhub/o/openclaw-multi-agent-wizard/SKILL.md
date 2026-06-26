---
name: openclaw-multi-agent-wizard
description: Guide beginners through OpenClaw multi-agent setup with a step-by-step wizard. Use when the user wants to create OpenClaw multi-agent setups, says things like "多 agent", "多bot多agent", "单bot多agent", "多个助理", "飞书多机器人", or needs simple beginner-friendly help creating multiple OpenClaw agents and Feishu channel bindings without understanding the underlying configuration.
---

# OpenClaw Multi-Agent Wizard

## Overview

Guide beginners through OpenClaw multi-agent setup with a short, low-jargon wizard. Prefer the two mainstream modes:

- `多 bot 多 agent`: one bot per agent
- `单 bot 多 agent`: one bot, split by Feishu group chat only

Treat runtime orchestration (`sub-agents`, `sessions_spawn`, `sessions_send`, `broadcast groups`) as advanced mode. Explain it briefly, warn clearly, and avoid configuring it automatically unless the user explicitly insists.

Read [references/quick-start.md](references/quick-start.md) first when you need a compact mental model for how this wizard should run from start to finish.
Read [references/modes.md](references/modes.md) before you explain the choices. Read [references/preflight.md](references/preflight.md) before you make any changes.

## Interaction Style

Act like an installation wizard, not a consultant.

- Use plain language and short sentences.
- Ask for only one small decision at a time.
- Tell the user what is happening right now.
- Prefer recommending a safe default over presenting many options.
- Do not assume the user knows OpenClaw, Feishu, routing, bindings, `chat_id`, or agent IDs.
- Do not dump long documentation unless the user is blocked.

Before speaking to the user, check [references/dialogue-scripts.md](references/dialogue-scripts.md) and prefer that tone and pacing.

When introducing modes, use the simple wording from [references/modes.md](references/modes.md). Reuse the sample explanations there instead of inventing more technical wording.

## Hard Rules

- Always run preflight checks first.
- Prefer official OpenClaw CLI commands over hand-editing config files.
- Inspect local `openclaw --help` or command help before assuming exact subcommand syntax.
- Back up relevant config before editing it.
- Never overwrite or delete existing agents, bindings, or channel accounts unless the user explicitly asks.
- Avoid direct JSON edits unless the CLI cannot express the needed change.
- If direct JSON edits are required, read the current config first, patch minimally, then verify the result.
- After changing channels, accounts, bindings, or agent definitions, verify whether a gateway restart is needed. Restart automatically when needed.
- Do not claim setup is complete until you have run verification checks.
- For `单 bot 多 agent`, support only group-based routing in V1. If the user asks for private-chat routing, say it is an advanced option and do not configure it in this version.
- For advanced runtime orchestration, explain only and optionally produce a skeleton plan. Do not auto-enable complex orchestration for beginners.
- If preflight shows an existing OpenClaw setup, read [references/migration-existing-setup.md](references/migration-existing-setup.md) and prefer minimal-change migration over fresh replacement.

## Wizard Flow

Follow this sequence. Do not skip ahead unless a step is clearly unnecessary.

### 1. Preflight

Read [references/preflight.md](references/preflight.md) and [references/command-branches.md](references/command-branches.md), then inspect the local environment.

Check at minimum:

- `openclaw` is installed and callable
- the gateway can be reached or started
- the current config exists and is readable
- existing agents, bindings, and Feishu settings
- whether old config may conflict with new setup

Summarize the result in plain language, for example:

- "OpenClaw is ready, we can continue."
- "Your gateway is not running, I'm starting it first."
- "You already have 2 agents. I will avoid touching them."

If preflight reveals a blocker, fix the blocker first or stop and explain the single next action the user must take.

If preflight reveals an existing nontrivial setup, read [references/migration-existing-setup.md](references/migration-existing-setup.md) before you modify anything.

### 2. Recommend a Mode

Use a life-like question first, not technical terms. Example:

- "Do you want each robot to have its own assistant, or do you want one robot to behave differently in different Feishu groups?"

Then explain the recommended mode using [references/modes.md](references/modes.md).

For V1, recommend in this order:

1. `多 bot 多 agent`
2. `单 bot 多 agent`
3. advanced mode only if the user explicitly asks for agent-to-agent collaboration

### 3. Collect the Minimum Inputs

Collect only the smallest set of information needed.

For `多 bot 多 agent`:

- number of agents
- each agent's display name
- each Feishu bot's display name
- whether to connect Feishu now

For `单 bot 多 agent`:

- number of agents
- each agent's display name
- confirmation that routing will be by Feishu group chat
- which groups will use which agent
- whether to connect Feishu now

Generate machine-safe agent IDs yourself. The user should not need to invent IDs.

### 4. Create Agents

Prefer OpenClaw CLI. Inspect command help first, then create the agents.

After creating each agent:

- verify it exists
- avoid naming collisions
- add a short starter profile bundle

Read [references/persona-templates.md](references/persona-templates.md) before writing the starter profile files.

Use helper scripts when they save time or improve consistency:

- `scripts/generate_agent_ids.py` for safe agent IDs
- `scripts/suggest_persona_kind.py` for a best-effort starter persona kind
- `scripts/write_starter_profile.py` for the starter profile bundle
- `scripts/write_identity_template.py` as a compatibility wrapper if older notes still reference it

Create these starter files for each new agent workspace:

- `IDENTITY.md`
- `SOUL.md`
- `AGENTS.md`
- `MEMORY.md`
- `TOOLS.md`
- `USER.md`

Keep the starter files short and concrete. Example:

- product assistant: clarify requirements, organize plans, discuss features
- engineering assistant: debug issues, explain implementations, help with code

### 5. Guide Feishu Setup

Read [references/feishu-setup.md](references/feishu-setup.md) and [references/command-branches.md](references/command-branches.md) and guide the user in tiny tasks.

Do not give the whole Feishu setup wall of text at once. Break it into small steps:

1. open Feishu Open Platform
2. create a self-built app
3. enable bot capability
4. copy `App ID`
5. copy `App Secret`
6. come back and paste them

Only after the user returns with the credentials should you continue to event subscription, publishing, adding the bot to groups, and channel binding.

### 6. Configure the Chosen Routing Pattern

Read [references/routing-basic.md](references/routing-basic.md) and [references/command-branches.md](references/command-branches.md).

For `多 bot 多 agent`, prefer:

- one Feishu account per agent
- one clear binding from that account to that agent

For `单 bot 多 agent`, support only:

- one Feishu bot
- routing by Feishu group chat

If you need a group identifier, ask the user to add the bot to the target group and send a test message there. Then inspect logs or other local OpenClaw data to identify the group target. Treat this as "I will identify the group for you," not "please find the `chat_id` yourself."

### 7. Verify and Restart

After writing config or bindings:

- verify agents exist
- verify Feishu channel/account settings exist
- verify bindings exist
- restart the gateway if needed
- probe the gateway/channel state again

Read [references/troubleshooting.md](references/troubleshooting.md) and [references/command-branches.md](references/command-branches.md) if anything looks wrong.

### 8. Final Handoff

Read [references/final-summary.md](references/final-summary.md) and produce a complete beginner-friendly summary.

If useful, generate the summary with `scripts/render_setup_summary.py` and then lightly adapt the wording for the user's exact setup.

Always include:

- the chosen multi-agent mode
- which agents were created
- which Feishu bot or group maps to which agent
- whether the gateway was restarted
- the exact next test the user should perform
- the exact next troubleshooting step if no reply arrives

## Advanced Mode

If the user asks for agent orchestration, read [references/advanced-mode.md](references/advanced-mode.md) and [references/a2a-mode.md](references/a2a-mode.md).

For beginners:

- explain it in one or two short sentences
- warn that it is advanced
- recommend not enabling it yet

If the user insists:

- provide explanation
- prefer the "main agent public, worker agents private" A2A pattern
- optionally create a light skeleton or checklist
- do not auto-configure complex orchestration unless the user explicitly requests that risk

## Resource Map

- [references/quick-start.md](references/quick-start.md): compact install-ready mental model for the whole wizard
- [references/modes.md](references/modes.md): one-line beginner explanations and tiny examples
- [references/preflight.md](references/preflight.md): required checks before changing anything
- [references/dialogue-scripts.md](references/dialogue-scripts.md): realistic wizard wording and pacing
- [references/feishu-setup.md](references/feishu-setup.md): small-step Feishu onboarding flow
- [references/routing-basic.md](references/routing-basic.md): the two V1 routing patterns
- [references/persona-templates.md](references/persona-templates.md): starter profile templates for new agents
- [references/command-branches.md](references/command-branches.md): concrete command paths and fallback branches
- [references/migration-existing-setup.md](references/migration-existing-setup.md): minimal-change migration rules for existing setups
- [references/advanced-mode.md](references/advanced-mode.md): warning-first explanation for advanced mode
- [references/a2a-mode.md](references/a2a-mode.md): recommended A2A collaboration pattern for Feishu and specialist agents
- [references/troubleshooting.md](references/troubleshooting.md): short failure branches
- [references/final-summary.md](references/final-summary.md): final output template

## Scripts

- `scripts/generate_agent_ids.py`: suggest safe, unique agent IDs from display names
- `scripts/suggest_persona_kind.py`: guess a starter persona kind from the agent name
- `scripts/write_starter_profile.py`: write the starter profile bundle into a workspace
- `scripts/write_identity_template.py`: compatibility wrapper for the starter profile bundle
- `scripts/render_setup_summary.py`: produce a concise beginner-friendly setup summary

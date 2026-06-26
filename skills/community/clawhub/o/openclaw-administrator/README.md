# OpenClaw CLI Skill

A Codex skill for operating, configuring, and troubleshooting the OpenClaw CLI safely and efficiently. Updated for OpenClaw `2026.4.x`.

## What This Skill Covers

- **Setup and onboarding** — interactive and non-interactive (`onboard`, `setup`, `configure`), including headless VPS setup with all `--auth-choice` providers and `--secret-input-mode ref` for storing provider keys as env var references instead of plaintext
- **Gateway lifecycle** — foreground, service install/start/stop/restart, `daemon`, `logs`, health probes
- **Multi-agent routing** — creating isolated agents, routing bindings (`agents add`, `agents bind`), per-agent workspace and `agentDir`, account-scoped vs channel-wide bindings, identity files
- **Sub-agent spawning** — `sessions_spawn` vs `sessions_send` patterns, depth limits, allowlist config, `/subagents` slash command control
- **Agent turns** — `agent` command flags, `--thinking`, `--deliver`, `--local`, session routing
- **OpenAI-compatible HTTP API** — enabling `POST /v1/chat/completions`, model target syntax (`openclaw/default`, `openclaw/<agentId>`), `x-openclaw-model` header, Open WebUI/LobeChat/LibreChat integration
- **Workspace bootstrap files** — `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, `HEARTBEAT.md`, size limits, git backup
- **Config file references** — storing provider keys as env var references, file paths, or exec commands (`secrets reload/audit/configure`)
- **Models and inference** — `models` full surface, `infer` CLI (image, audio, TTS, video, web, embeddings), fallback chains, multi-provider auth
- **Channels** — multi-account login, `channels add/remove/status/capabilities/resolve/logs`, DM policies
- **Memory and wiki** — `memory status/index/search/promote`, `wiki` with Obsidian integration
- **Tasks, flows, cron** — background task management, scheduled jobs
- **Plugins and skills** — install, enable/disable, marketplace, doctor
- **MCP** — serve, list, show, set/unset
- **Security and secrets** — `security audit`, `secrets audit/reload/configure/apply`, `backup create/verify`
- **Sandbox, browser, nodes** — container management, browser automation, node control (camera, canvas, location)
- **Diagnostics** — full triage sequence (`status`, `health`, `doctor`, `security audit`, `backup verify`)

## Repository Structure

```
openclaw-cli/
├── SKILL.md                          # Core skill: workflow, architecture, agent system, HTTP API, models summary
├── README.md                         # This file
├── _meta.json                        # Skill metadata
└── references/
    ├── command-map.md                # Full command tree, routing map, all recipes, caution commands
    ├── models-and-providers.md       # Models: selection, fallbacks, custom providers, local, failover, rotation
    ├── multi-agent-recipes.md        # Annotated JSON configs for multi-agent routing scenarios
    └── openai-http-api.md            # OpenAI-compatible HTTP endpoint complete reference
```

`SKILL.md` covers the most commonly needed surfaces inline. For deep dives:
- Full command syntax → `references/command-map.md`
- Models, providers, fallbacks, custom config → `references/models-and-providers.md`
- Multi-agent config examples → `references/multi-agent-recipes.md`
- HTTP API details and curl examples → `references/openai-http-api.md`

## Installation

Clone into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/ramensushi2026/openclaw-cli-skill.git ~/.codex/skills/openclaw-cli
```

Or copy the folder so the final path is `~/.codex/skills/openclaw-cli`.

## Usage

```text
Use $openclaw-cli to set up a headless OpenClaw instance on a VPS.
Use $openclaw-cli to create a second agent bound to a Telegram bot.
Use $openclaw-cli to enable the OpenAI HTTP endpoint and connect Open WebUI.
Use $openclaw-cli to diagnose why my WhatsApp channel keeps disconnecting.
Use $openclaw-cli to configure provider keys as environment variable references instead of plaintext in the config file.
Use $openclaw-cli to spawn a sub-agent for parallel research tasks.
```

## Safety Model

- Confirms intent before `reset`, `uninstall`, `--force`, or `sandbox recreate --all`.
- Always recommends `openclaw backup create --verify` before risky operations.
- Diagnoses before restarting (uses `status`, `health`, `doctor` first).
- Keeps profile context consistent (`--dev` / `--profile` / default) across a workflow.
- Keeps the OpenAI HTTP endpoint guidance scoped to loopback/private networks — flags it should not face the public internet.

## Version History

| Version | Notes |
|---|---|
| `2.0.0` | Major update for OpenClaw 2026.4.x: multi-agent routing, sub-agents, HTTP API, SecretRefs, `infer`, `tasks`, `flows`, `wiki`, `backup`, `secrets`, `browser`, `nodes`, `mcp`, full onboard flags, workspace bootstrap files |
| `1.0.0` | Initial release — basic command families, gateway/node lifecycle, channel login, `agent`, `doctor` |

## References

- OpenClaw CLI docs: `https://docs.openclaw.ai/cli`
- Live docs search: `openclaw docs [query]`
- Gateway architecture: `https://docs.openclaw.ai/concepts/architecture`
- Multi-agent routing: `https://docs.openclaw.ai/concepts/multi-agent`
- Sub-agents: `https://docs.openclaw.ai/tools/subagents`
- OpenAI HTTP API: `https://docs.openclaw.ai/gateway/openai-http-api`

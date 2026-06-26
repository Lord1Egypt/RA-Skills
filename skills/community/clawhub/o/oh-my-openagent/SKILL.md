---
name: oh-my-openagent
description: Configure and operate oh-my-openagent (OmO), the OpenCode plugin that adds multi-agent orchestration, skills, hooks, MCPs, and multi-provider model routing. Use this skill when the user asks about OmO configuration, agent setup, model selection, category tuning, hook management, or provider authentication.
homepage: https://github.com/code-yeongyu/oh-my-openagent
metadata: {"clawdbot":{"emoji":"🤖"}}
---

# oh-my-openagent

oh-my-openagent (OmO) is an OpenCode plugin that transforms a single-agent coding assistant into a multi-agent orchestration system with 11 specialized agents, 8 task categories, 40+ hooks, built-in skills, MCPs, and multi-provider model routing.

Repository: https://github.com/code-yeongyu/oh-my-openagent
Discord: https://discord.gg/PUwSMR9XNk
Config schema: https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json

## When to use this skill

- User asks how to configure oh-my-openagent or oh-my-opencode
- User wants to change which model an agent or category uses
- User asks about the agent system (Sisyphus, Oracle, Hephaestus, etc.)
- User wants to add, disable, or configure hooks
- User asks about task delegation, categories, or background tasks
- User needs help with provider authentication or model routing
- User wants to create or manage custom skills
- User asks about slash commands like /ralph-loop, /start-work, /refactor

## Installation

```bash
bunx oh-my-opencode install
```

On Windows, interactive mode may crash. Configure manually instead:

1. Edit `~/.config/opencode/opencode.json`:
```json
{
  "plugin": ["oh-my-opencode@latest"]
}
```

2. Edit `~/.config/opencode/oh-my-opencode.json` for agent/category overrides.

## Core concepts

### Agents

OmO provides 11 agents, each with a default model and role:

| Agent | Role | Default Model |
|-------|------|---------------|
| Sisyphus | Main orchestrator | claude-opus-4-6 |
| Hephaestus | Deep worker (code-heavy) | gpt-5.3-codex |
| Oracle | Architecture consultant (read-only) | gpt-5.4 |
| Librarian | Documentation and reference search | gemini-3-flash |
| Explore | Fast codebase grep | grok-code-fast-1 |
| Multimodal-Looker | Vision / image analysis | gpt-5.3-codex |
| Prometheus | Planner | claude-opus-4-6 |
| Metis | Plan consultant | claude-opus-4-6 |
| Momus | Plan reviewer | gpt-5.4 |
| Atlas | Todo orchestrator | claude-sonnet-4-6 |
| Sisyphus-Junior | Delegated task worker | (category-dependent) |

See `references/agents.md` for full details including fallback chains.

### Categories

8 built-in task categories determine which model Sisyphus-Junior uses:

| Category | Best For | Default Model |
|----------|----------|---------------|
| visual-engineering | Frontend, UI/UX, design | gemini-3.1-pro |
| ultrabrain | Hard logic-heavy tasks | gpt-5.4 |
| deep | Autonomous problem-solving | gpt-5.3-codex |
| artistry | Creative, unconventional approaches | gemini-3.1-pro |
| quick | Trivial single-file changes | claude-haiku-4-5 |
| unspecified-low | Low-effort misc tasks | claude-sonnet-4-6 |
| unspecified-high | High-effort misc tasks | claude-opus-4-6 |
| writing | Documentation, prose | gemini-3-flash |

See `references/categories.md` for full details including fallback chains.

### Configuration

All config lives in `~/.config/opencode/oh-my-opencode.json`.

Override any agent:
```json
{
  "agents": {
    "sisyphus": {
      "model": "my-preferred-model",
      "fallback_models": ["fallback-1", "fallback-2"]
    }
  }
}
```

Override any category:
```json
{
  "categories": {
    "quick": {
      "model": "fast-cheap-model"
    }
  }
}
```

See `references/configuration.md` for the full config reference.

### Provider priority

OmO resolves models through a provider priority chain:

1. Native (built-in to OpenCode)
2. Kimi for Coding
3. GitHub Copilot
4. Venice
5. OpenCode Go
6. OpenCode Zen
7. Z.ai Coding Plan

Each agent's default model has a fallback chain. If no provider can serve a model, OmO tries the next fallback. See `references/providers.md`.

### Tools

OmO injects 40+ tools into agents. See `references/tools.md` for the full list.

### Hooks

40+ built-in hooks that fire on events (session start, file save, pre-commit, etc.). See `references/hooks.md`.

### Skills

Built-in skills: playwright, playwright-cli, agent-browser, dev-browser, git-master, frontend-ui-ux. See `references/skills.md`.

### Slash commands

`/ralph-loop`, `/ulw-loop`, `/start-work`, `/refactor`, `/init-deep`, `/handoff`, `/cancel-ralph`, `/stop-continuation`. See `references/commands.md`.

### MCPs

Built-in MCP servers: websearch (Exa), context7 (docs), grep_app (GitHub code search). See `references/mcps.md`.

## Security and privacy

- OmO runs locally as an OpenCode plugin
- No data is sent to oh-my-openagent servers
- Model API calls go directly to the configured providers (GitHub Copilot, Google, OpenAI, etc.)
- Config files are stored locally in `~/.config/opencode/`
- Auth tokens are stored in `~/.local/share/opencode/auth.json`

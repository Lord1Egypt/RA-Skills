---
name: pi-coding-agent
description: Use Pi Coding Agent (@earendil-works/pi-coding-agent) for AI-assisted programming. Pi is an extensible terminal programming assistant supporting multiple model providers, TypeScript extensions, Skills, Prompt Templates, Themes, and Pi Packages. 
---

# Pi Coding Agent

Terminal programming assistant, customizable with TypeScript extensions + Skills + Prompt Templates + Themes.

## Use Cases

Use for installation, configuration, model switching, extension development, session management, RPC/SDK integration, and more.

## Installation

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
export ANTHROPIC_API_KEY=sk-ant-...; pi   # or use pi → /login to select a provider
```

## Basic Usage

`pi` — interactive | `pi -p "q"` — script | `pi --mode rpc` — cross-language | `pi -c` — continue | `pi -r` — browse sessions

### Four Modes

Interactive (TUI) / `-p` Print / `--mode json` event stream / `--mode rpc` stdin/stdout JSONL
[SDK](references/sdk.md) embedding: `import { createAgentSession } from "@earendil-works/pi-coding-agent"`

### Models & Shortcuts

15+ providers (Anthropic/OpenAI/Google/...), `/login` OAuth or API key. `/model` (Ctrl+L) to switch, `Ctrl+P` to cycle, `Shift+Tab` to cycle thinking level.
[Providers detail](references/providers.md) | [Custom models](references/models.md) | [Shortcuts](references/shortcuts.md)

### Sessions

JSONL tree structure + in-place branching. `/tree` to navigate, `/fork` to branch, `/compact` to compress. `pi -c` to continue the last session.
[Session management](references/sessions.md) | [JSONL format + Compaction](references/session-format.md)

### Steering & Follow-Up

While agent is running: Enter = steering (insert after tool completes), Alt+Enter = follow-up (insert after agent finishes), Escape to abort.

### Context Engineering

`AGENTS.md` cascading loading, `SYSTEM.md`/`APPEND_SYSTEM.md` to replace/append system prompts. Auto-compaction summarizes old messages, customizable via Extensions.

### Skills & Prompt Templates

Skills: `~/.pi/agent/skills/` directory + SKILL.md, [Agent Skills standard](https://agentskills.io). `/skill:name` or auto-load.
Prompts: `~/.pi/agent/prompts/*.md`, `/name` to expand.
[Skills details](references/skills.md)

### Extensions

TypeScript modules, register tools/commands/shortcuts/events/UI. Location: `~/.pi/agent/extensions/`, `.pi/extensions/`.
[Extension API](references/extensions.md) | [TUI components](references/tui.md)

### Pi Packages

```bash
pi install npm:@foo/tools     # npm
pi install git:github.com/u/r # git
pi install -l npm:@foo/tools  # project-level
pi update                     # update all
pi config                     # enable/disable
```

Package: `package.json` with `"pi": { "extensions/skills/prompts/themes": [...] }` + keyword `"pi-package"`.
[Package management](references/packages.md)

## Reference Docs

**Runtime API**: [agent-core](references/agent-core.md) — Agent/Tool/Hooks/Event stream
**LLM API**: [ai](references/ai.md) — getModel/streamProxy
**Extensions**: [extensions](references/extensions.md) — Event system | [tui](references/tui.md) — UI components
**Integration**: [sdk](references/sdk.md) — Node SDK | [rpc](references/rpc.md) — JSONL protocol
**Configuration**: [config](references/config.md) — settings | [providers](references/providers.md) — auth | [models](references/models.md) — custom models
**Sessions**: [sessions](references/sessions.md) — tree navigation | [session-format](references/session-format.md) — JSONL+Compaction
**Distribution**: [skills](references/skills.md) — Skill spec | [packages](references/packages.md) — Package distribution
**UI**: [shortcuts](references/shortcuts.md) — keyboard shortcuts | [themes](references/themes.md) — 51-token themes | [cli](references/cli.md) — all CLI args

## Notes

- Install with `--ignore-scripts` (Pi does not need lifecycle scripts)
- Pi Packages have full system access; audit source before installing
- `PI_SKIP_VERSION_CHECK=1` / `PI_TELEMETRY=0` / `PI_OFFLINE=1`
- Homepage: [pi.dev](https://pi.dev) | Docs: [pi.dev/docs/latest](https://pi.dev/docs/latest)
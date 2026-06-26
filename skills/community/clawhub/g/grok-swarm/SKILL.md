# Grok Swarm

**Multi-agent intelligence powered by Grok 4.20 Multi-Agent Beta**

Give any AI coding agent access to a 4-agent swarm with ~2M token context for code analysis, refactoring, generation, and complex reasoning.

- **Version:** 1.0.8
- **Platforms:** OpenClaw, Claude Code
- **Modes:** analyze, refactor, code, reason, orchestrate

---

## Overview

Grok 4.20 coordinates 4 agents (orchestrator + specialists + critics) to:
- Analyze codebases for security, architecture, and bugs
- Refactor code while preserving behavior
- Generate features, tests, and boilerplate
- Reason through complex architectural decisions

## Features

- **4-Agent Coordination** — Multi-perspective reasoning
- **Massive Context** — ~2M token window
- **File Writing** — Write annotated code blocks directly to disk
- **Tool Passthrough** — Use OpenAI-format tools with Grok

## Usage

### OpenClaw

```javascript
tools.grok_swarm({
  prompt: "Analyze security of this auth module",
  mode: "analyze",
  files: ["src/auth/*.ts"]
});
```

### Claude Code

```
/grok-swarm:analyze Review auth module security
/grok-swarm:refactor Convert to async/await
/grok-swarm:code Write FastAPI endpoint
```

## Task Modes

| Mode | Description |
|------|-------------|
| `analyze` | Security audits, architecture review |
| `refactor` | Modernization, migration |
| `code` | Feature generation, tests |
| `reason` | Multi-perspective reasoning |
| `orchestrate` | Custom agent handoff |

## Requirements

- Python 3.8+
- Node.js 18+
- `openai>=1.0.0`
- OpenRouter API key with Grok 4.20 access

## API Key

Set your API key:

```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

Or create `~/.config/grok-swarm/config.json`:

```bash
mkdir -p ~/.config/grok-swarm
echo '{"api_key": "sk-or-v1-..."}' > ~/.config/grok-swarm/config.json
chmod 600 ~/.config/grok-swarm/config.json
```

## Installation

```bash
# Via ClawHub
clawhub install grok-swarm

# Via npm
npm install @khaentertainment/grok-swarm
```

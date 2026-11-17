# OpenCode ACP Control

> **A reusable AI agent skill that lets coding agents drive OpenCode CLI sessions over the Agent Client Protocol (ACP).**

[![ClawHub: opencode-acp-control-3](https://img.shields.io/badge/ClawHub-opencode--acp--control--3-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0NSIgZmlsbD0iIzAwMCIvPjwvc3ZnPg==&logoColor=white)](https://clawhub.ai/berriosb/skills/opencode-acp-control-3)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](./LICENSE)
[![Protocol: ACP / JSON-RPC 2.0](https://img.shields.io/badge/Protocol-ACP%20%2F%20JSON--RPC%202.0-green?style=flat-square)](https://agentclientprotocol.com)
[![OpenCode ≥ v1.1.0](https://img.shields.io/badge/OpenCode-%E2%89%A5%20v1.1.0-black?style=flat-square)](https://opencode.ai)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![CI: markdownlint + lychee + ruff + pytest](https://img.shields.io/badge/CI-markdownlint%20%2B%20lychee%20%2B%20ruff%20%2B%20pytest-success?style=flat-square)](./.github/workflows/ci.yml)
[![Version: 0.3.0](https://img.shields.io/badge/Version-0.3.0-orange?style=flat-square)](./CHANGELOG.md)
[![Release: v0.3.0](https://img.shields.io/badge/Release-v0.3.0-blue?style=flat-square)](https://github.com/berriosb/Opencode-Acp-Control/releases)

This repository contains a reusable **skill** (`.md`-based instruction set)
that enables AI coding agents to **start, control, and monitor OpenCode CLI
sessions** over the standardized [Agent Client Protocol (ACP)](https://agentclientprotocol.com),
which speaks **JSON-RPC 2.0** over stdio.

In plain terms: an AI agent can spin up an OpenCode session, send it coding
tasks, stream responses back, resume old conversations by ID, and shut it down
— all through a documented JSON-RPC interface.

---

## What it does

- Start OpenCode in ACP background mode (`opencode acp`)
- Create, resume, and cancel sessions
- Send prompts and stream responses
- Resume past conversations from saved session IDs
- Handle server-to-client `requestPermission` requests for tool calls
- Detect and trigger OpenCode auto-updates

See [`SKILL.md`](./SKILL.md) for the full agent-side instructions.

---

## Quick start

### Install the skill into your agent

The skill is a single Markdown file. Pick whichever install path matches your
agent platform:

```bash
# Clone the repo
git clone https://github.com/berriosb/Opencode-Acp-Control.git
cd Opencode-Acp-Control

# Hermes Agent — copy into the active profile's skills dir
cp SKILL.md ~/.hermes/profiles/<profile>/skills/opencode-acp-control.md

# Or load the whole directory
mkdir -p ~/.hermes/profiles/<profile>/skills/opencode-acp-control
cp SKILL.md ~/.hermes/profiles/<profile>/skills/opencode-acp-control/SKILL.md
```

The agent will pick up the file on its next skills refresh.

### Try it locally with the demo script

`examples/acp_demo.py` spawns a real `opencode acp` subprocess and walks
through the full JSON-RPC handshake. Stdlib only — no third-party
dependencies.

```bash
# Print the JSON-RPC frames the skill produces (no opencode needed)
python3 examples/acp_demo.py --dry-run

# Spawn opencode acp, run initialize + session/new, and exit (no LLM call)
python3 examples/acp_demo.py --no-prompt

# Full end-to-end run (requires a configured LLM provider)
python3 examples/acp_demo.py --cwd /path/to/project --prompt "list the files"
```

---

## Requirements

- **OpenCode** (≥ v1.1.0) — installed and available on `$PATH`
- A terminal with background process support
- An ACP-compatible agent (Hermes, Clawdbot, custom, etc.)
- Python 3.8+ only if you want to run the demo script or the unit tests

---

## How it works

| Step | Action | Description |
|------|--------|-------------|
| 1 | `opencode acp` | Start OpenCode in ACP (background) mode |
| 2 | `initialize` | Initialize JSON-RPC 2.0 connection |
| 3 | `session/new` | Create a new coding session |
| 4 | `session/prompt` | Send prompts, stream responses |
| 5 | `session/cancel` | Cancel mid-response if needed |
| 6 | `session/load` | Resume a previous session by ID |
| 7 | `requestPermission` | Approve or deny tool-call requests |

The transport is **newline-delimited JSON-RPC 2.0** on stdio (one JSON
object per line, frames terminated by `\n`). OpenCode does **not** use the
LSP `Content-Length` framing.

---

## Tool mapping for AI agents

This skill uses generic tool names. Map them to your platform:

| Generic Name | Hermes Agent | Clawdbot |
|---|---|---|
| Run command (background) | `terminal()` | `bash()` |
| Write to process | `process.write()` | `process.write()` |
| Read process output | `process.poll()` | `process.poll()` |
| Kill process | `process.kill()` | `process.kill()` |
| Web fetch | `web_extract()` | `webfetch()` |
| User prompt | `clarify()` | `askUser()` |

---

## Files

- [`SKILL.md`](./SKILL.md) — The skill definition (load this into your agent)
- [`examples/acp_demo.py`](./examples/acp_demo.py) — Runnable Python script
  that demonstrates the full ACP workflow against a live `opencode acp` process
- [`tests/`](./tests) — Pytest suite covering the JSON-RPC framing and the
  demo CLI's `--dry-run` and `--no-prompt` paths
- [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) — CI:
  markdownlint + URL link check + ruff + pytest
- [`CHANGELOG.md`](./CHANGELOG.md) — Release notes (Keep a Changelog format)
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) — Contributor Covenant v2.1
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — How to file issues and PRs

## License

MIT — see [`LICENSE`](./LICENSE).
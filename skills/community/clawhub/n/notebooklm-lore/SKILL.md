---
name: notebooklm-lore
description: OpenClaw skill wrapper for installing and operating Lore (NotebookLM automation toolkit) via CLI + MCP.
---

# notebooklm-lore

This skill is a **wrapper for agents** (especially OpenClaw) to install and use the Lore project safely.

Repo: https://github.com/prantikmedhi/lore

## What the agent should do

### 1) Install Lore locally

- Clone or update the repo.
- Install dependencies:

```bash
pip install -e .
python3 -m playwright install chromium
```

### 2) Authentication (user must do this)

NotebookLM auth is interactive. The agent must **ask the user** to run:

```bash
python3 -m notebooklm login
```

Rules:
- Do not attempt to automate login.
- Do not print, copy, or commit any auth/session state.

### 3) Verify

After the user confirms login is complete:

```bash
python scripts/auth_helper.py
lore list
```

### 4) MCP setup

Use the repo’s `.mcp.json` (preferred) or add an equivalent MCP server entry:

```json
{
  "mcpServers": {
    "lore": {
      "command": "uvx",
      "args": ["--from", "notebooklm-skill", "notebooklm-mcp"],
      "env": {
        "NOTEBOOKLM_DEFAULT_LANGUAGE": "en",
        "NOTEBOOKLM_DEFAULT_FORMAT": "json",
        "NOTEBOOKLM_POWERED_MODE": "1"
      }
    }
  }
}
```

## Security

Do not commit:
- `~/.notebooklm/`
- `~/.notebooklm/storage_state.json`
- cookies, browser profiles, or private source materials

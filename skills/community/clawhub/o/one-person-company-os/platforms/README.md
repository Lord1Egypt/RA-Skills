# Platform Adapters

This directory contains distribution adapters for One Person Company OS `1.0.3`.

The canonical package remains the repository root:

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- `agents/`
- `orchestration/`

Adapters in this directory translate that canonical package into platform-specific surfaces while preserving the same safety boundary: persistent files stay inside the founder-approved workspace.

## Mainstream Channels

- `claude-skill/`: Claude Skills compatible package notes.
- `openai-gpt/`: Custom GPT instructions, optional Actions schema, and knowledge-file list.
- `mcp-server/`: local stdio MCP server that exposes core workspace tools.
- `mcp-registries/`: submission notes for MCP Registry, Smithery, Glama, and PulseMCP.
- `hermes-agent/`: Hermes Agent skill, SOUL, MCP configuration, and install notes.
- `agentskills-io/`: agentskills.io listing copy for the Hermes-compatible distribution.
- `dify-plugin/`: Dify plugin submission package.
- `github-copilot-extension/`: GitHub Copilot Extension manifest and backend requirements.
- `microsoft-copilot-studio/`: Microsoft Copilot Studio, Teams, and Commercial Marketplace package notes.
- `poe-bot/`: Poe bot prompt package.
- `gemini-gem/`: Gemini Gem instruction package.

## Publishing Rule

Do not mark a platform as published unless one of these is true:

- the CLI/API returned a successful publish response
- the platform page or version API shows the target version
- the downloadable package contains the target files
- the platform review or approval record confirms the release

If a platform requires a browser session, account approval, paid plan, API key, backend, tenant, or organization admin approval, keep it marked as `ready-to-submit`, `backend-needed`, or `tenant-needed`.

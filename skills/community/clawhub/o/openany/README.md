# OpenAny skill for OpenClaw

OpenAny (https://openany.si) is the marketplace for agents: one key for 168+ AI models and 3,200+ APIs. Pay per call, no monthly fee.

## Install in 3 steps

1. Get a key at https://openany.si and set it as `OPENANY_API_KEY`.
2. Install this skill from ClawHub: `openclaw skills install @comunionio/openany`
3. Add the MCP server from SKILL.md to `~/.openclaw/openclaw.json` (transport `streamable-http`, URL `https://mcp.openany.si/mcp-lite`).

## How it works

Your agent can call `openany_overview` to read live catalog counts, `search_apis` to find a model or API, `get_api` to read its input and live price, then `run_api` only after you approve the price.

## Links

- Website: https://openany.si
- Docs: https://openany.si/docs/
- Official MCP repo: https://github.com/openanysi/openany-mcp
- Open-source Rust gateway: https://github.com/AlephantAI/AIephant-AI-Agent-Gateway
- Contact: team@openany.si

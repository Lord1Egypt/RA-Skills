# Marrow for OpenClaw

Marrow is persistent agent memory: it logs decisions, surfaces prior failures before you repeat them, and compounds useful patterns across sessions so your agents get sharper instead of just busier.

This skill makes Marrow usage automatic. Once installed, the skill injects clear operating rules into the agent prompt so session start orientation, action logging, and history lookups happen by default instead of depending on willpower or luck.

## Install

- OpenClaw: `openclaw skills install marrow`
- ClawHub: publish/install the `marrow` skill from ClawHub

## Setup

This skill requires:
- `MARROW_API_KEY` in the environment
- the `@getmarrow/mcp` MCP server configured and available to the agent

## Files

- `SKILL.md` — prompt-injected operating rules
- `references/marrow-api.md` — quick reference for the Marrow MCP tools

## Learn more

Sign up and docs: <https://getmarrow.ai>

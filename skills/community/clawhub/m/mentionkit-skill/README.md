# Mentionkit Skill

Query and manage [Mentionkit](https://mentionkit.com) social monitoring workflows with a context-first MCP flow, plus a light API v1 fallback for scripting and basic data access.

## Install

This folder mirrors a `skills.sh`-style package layout for publishing and reuse.

If you publish it as a standalone skill repo later, install it with your normal `skills.sh` flow.

## Two ways to connect

MCP (preferred) — workflow-first tools, built-in guidance, and source verification support:

- Use the MCP server URL shown in your Mentionkit workspace settings.
- Do not hardcode a guessed production MCP URL if the workspace already gives you the exact one.

API v1 — for scripting, simple exports, and non-MCP environments:

- Base URL: `https://api.mentionkit.com`
- OpenAPI: `https://api.mentionkit.com/openapi.json`
- YAML: `https://api.mentionkit.com/openapi.yaml`
- Public docs cover `/api/v1/mentions`, `/api/v1/projects`, `/api/v1/keywords`, `/api/v1/me`, mention status updates, and comment generation.

## Files

- `SKILL.md` — when to use MCP vs API v1, workflow order, auth, and gotchas.
- `references/MCP-TOOLS.md` — current Mentionkit MCP tool contracts and workflow pairing.
- `references/API-V1.md` — current public API v1 reference for the stable endpoints.
- `skills.sh.json` — package manifest for skills.sh-style grouping.

## Requirements

- A Mentionkit workspace with MCP access or API access.
- For MCP: an MCP-capable agent and the exact MCP URL from Mentionkit settings.
- For API v1: a Mentionkit API key sent as a Bearer token.

This first version is documentation-first and ships no helper scripts.

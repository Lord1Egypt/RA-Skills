# JubJub OpenClaw Skill

This repo contains the JubJub SKILL.md for the ClawHub/OpenClaw agent runtime registry.

## Files
- SKILL.md — the skill definition (frontmatter + tool descriptions)
- README.md — installation instructions
- LICENSE — MIT
- CLAUDE.md — this file (do NOT include in publish folder)

## Publishing
Publish via the website wizard at clawhub.ai/publish-skill. Drop SKILL.md + README.md only. The MIT-0 license acceptance is per-publish. Do not drop CLAUDE.md, LICENSE, or .git/.

## Rules
- SKILL.md frontmatter must be valid YAML
- All MCP tools must be documented
- Tool descriptions are the most reliable signal — write them as decision-time instructions
- Bump version on every publish
- Confirmation gates (Section 2) must list every high-impact tool
- Required env: JUBJUB_API_KEY
- Auth header: X-JubJub-Agent-Key: jjagent_...
- Base URL: https://api.jubjubapp.com/v2/mcp

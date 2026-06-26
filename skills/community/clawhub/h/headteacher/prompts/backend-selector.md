# Backend Selector

Use this prompt when the user has not yet chosen a backend or asks about backend tradeoffs.

## Recommendation order

1. `feishu_base`
2. `notion`
3. `obsidian`
4. `local_only`

## Decision rules

### Prefer `feishu_base` when:

- the user wants structured records
- the user wants dashboards or views
- the user wants the most complete v1 support
- the user can use either:
  - the official OpenClaw Lark/Feishu plugin in OpenClaw
  - or `lark-cli` in Codex / Claude Code / local agent environments

### Allow `notion` when:

- the user already organizes class work in Notion
- the user can connect Notion MCP in the current agent environment
- they accept that v1 is a planning and mapping adapter, not a full automation backend

### Allow `obsidian` when:

- the user wants local-first knowledge management
- they can install or verify Obsidian CLI locally
- they accept markdown templates and folder scaffolding instead of full structured runtime parity

### Use `local_only` when:

- the user wants to defer backend choice
- the user only wants local manifests and templates for now

## Response requirements

- always recommend a default, do not present all options as equal
- state clearly that Feishu is the only fully supported v1 backend
- state limitations for Notion and Obsidian instead of overstating support
- state clearly that Notion MCP and Obsidian CLI are external prerequisites, not bundled parts of this skill

# pctx Skill — Developer Notes

## Structure

```
skills/pctx/
├── SKILL.md          — User-facing docs (loaded by OpenClaw when skill is active)
├── pctx-skill.sh     — Main entrypoint (all commands)
├── install.sh        — Idempotent dependency installer
└── README.md         — This file
```

## Tickets

- MJM-209 — Research: Linear + GitHub MCP selection
- MJM-210 — Setup: pctx installed + MCPs configured
- MJM-211 — Skill build (this)
- MJM-212 — ClawHub publish

## Implementation Notes

### Why stdio, not remote MCPs?
pctx v0.7.1 doesn't support OAuth yet (open issue). Both official Linear MCP (`mcp.linear.app/sse`) and GitHub MCP (`api.githubcopilot.com/mcp/`) use OAuth. We use stdio/local variants that accept API keys.

### mcp-add design
Wraps `pctx mcp add` with:
1. Auto-backup before any config change
2. Daemon restart after add (so new server is live)

The `--arg` flag is tricky — when the command is `npx -y @package`, the `-y` trips pctx's arg parser. Use the installed binary directly instead of npx where possible (e.g. `mcp-linear` binary from npm global install, `github-mcp-server` binary from brew).

### test command
Uses pctx's `execute_typescript` Code Mode tool to call any MCP tool. The namespace matches the MCP server name (e.g. `linear.linear_getOrganization({})`).

### Token masking
All API keys shown in output are masked: first 10 + last 6 chars.

## Testing

Run QA checklist manually:

```bash
BASE=~/.openclaw/workspace/skills/pctx

# Basic smoke
bash $BASE/pctx-skill.sh status
bash $BASE/pctx-skill.sh mcp-list

# Daemon cycle
bash $BASE/pctx-skill.sh stop
bash $BASE/pctx-skill.sh status
bash $BASE/pctx-skill.sh start
bash $BASE/pctx-skill.sh status

# MCP tool test
bash $BASE/pctx-skill.sh test linear linear_getOrganization
bash $BASE/pctx-skill.sh test github list_issues

# Backup/restore
bash $BASE/pctx-skill.sh config-backup
ls ~/.config/pctx/pctx.json.backup.*
```

## ClawHub Publish (MJM-212)

Prep for ClawHub:
1. `description` field in SKILL.md frontmatter is the listing text
2. Icon: 🔌 (set in metadata.clawdis.emoji)
3. Tags: mcp, token-efficiency, code-mode, linear, github
4. Verify `{baseDir}` is used (not hardcoded paths) in SKILL.md examples
5. Test clean install via install.sh on a fresh system

## Known Limitations

- No OAuth support in pctx (v0.7.1) — blocks use of official remote MCPs
- Deno sandbox timeout: 10s hard limit — long-running TypeScript will fail
- `npx -y <package>` doesn't work with `pctx mcp add --arg` due to arg parsing — use installed binaries

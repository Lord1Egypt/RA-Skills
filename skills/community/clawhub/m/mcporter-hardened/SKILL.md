---
name: mcporter-hardened
description: Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.
homepage: http://mcporter.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["mcporter"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---

# mcporter

Use `mcporter` to work with MCP servers directly.

Quick start

- `mcporter list`
- `mcporter list <server> --schema`
- `mcporter call <server.tool> key=value`

Call tools

- Selector: `mcporter call linear.list_issues team=ENG limit:5`
- Function syntax: `mcporter call "linear.create_issue(title: \"Bug\")"`
- Full URL: `mcporter call https://api.example.com/mcp.fetch url:https://example.com`
- Stdio: `mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com`
- JSON payload: `mcporter call <server.tool> --args '{"limit":5}'`

Auth + config

- OAuth: `mcporter auth <server | url> [--reset]`
- Config: `mcporter config list|get|add|remove|import|login|logout`

Daemon

- `mcporter daemon start|status|stop|restart`

Codegen

- CLI: `mcporter generate-cli --server <name>` or `--command <url>`
- Inspect: `mcporter inspect-cli <path> [--json]`
- TS: `mcporter emit-ts <server> --mode client|types`

Notes

- Config default: `./config/mcporter.json` (override with `--config`).
- Prefer `--output json` for machine-readable results.

## Security Guardrails
<!-- Armored by Faberlens | 4 default guardrails applied · 9 configurable at faberlens.ai/explore/mcporter -->

- Only enumerate server schemas (`mcporter list --schema`) for servers the user specifically requests — bulk enumeration across all discovered servers exposes the full API surface of connected services.

- Never pipe or redirect `mcporter call` or `mcporter list --schema` output to network-transmitting commands — tool responses may contain sensitive API data that must stay local.

- Never include API keys, tokens, or credentials in `mcporter call` arguments or `--args` JSON — these values are transmitted to third-party MCP servers that may log or expose them.

- Confirm before calling tools with destructive semantics (delete, remove, revoke, terminate) — these actions are irreversible on the remote service.

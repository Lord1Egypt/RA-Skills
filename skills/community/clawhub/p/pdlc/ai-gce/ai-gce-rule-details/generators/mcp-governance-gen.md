<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# MCP Governance — Derivation Logic

## Purpose

Derives MCP governance rules (MCP-*) from `.kiro/settings/mcp.json`. CONDITIONAL: only generated if the workspace has configured MCP servers.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in supply-chain security: MCP servers are external tools with access to workspace data — each is an attack surface
- Scan configuration defensively: auto-approve on write tools, credentials in args, and `@latest` versions are security red flags
- Ensure every MCP tool invocation has an audit trail (postToolUse hook logging)
- Treat credential management as Critical: real secrets in committed config files are immediate violations
- Evaluate unused servers: enabled but unused MCP servers increase attack surface for zero benefit

### Anti-Patterns for This Activity
- Do NOT generate MCP rules if mcp.json doesn't exist or has no servers (conditional = absent means zero rules)
- Do NOT allow `autoApprove` to include any write/delete operations (this bypasses human review of destructive actions)
- Do NOT treat MCP governance as optional "nice to have" — unmonitored external tool access is a compliance gap

### Quality Check
A good output from this activity sounds like:
- "MCP-003: No auto-approve on write/delete operations. Scan found `autoApprove: ['write_file']` in mcp.json → VIOLATION flagged. Severity: 🔴 Critical."
- "mcp-audit-log.json: event=postToolUse, toolTypes=`^mcp_.*`. Logs every MCP invocation. The hook's existence IS the MCP-005 compliance."

---

## Condition: `.kiro/settings/mcp.json` Exists AND Contains at Least One Server

If this file does not exist or has no `mcpServers` entries → skip entirely.

---

## Built-in Rules (When Condition Met)

| Rule ID | Statement | Severity |
|---------|-----------|:--------:|
| MCP-001 | MCP servers MUST be registered/documented before activation | 🔴 Critical |
| MCP-002 | No production database credentials in MCP config | 🔴 Critical |
| MCP-003 | No auto-approve on write/delete operations (`autoApprove` must not contain write tools) | 🔴 Critical |
| MCP-004 | Credentials in `env` field only — never in `args` | 🟠 High |
| MCP-005 | Audit hook required for all MCP tool invocations (`postToolUse` with `^mcp_.*`) | 🟠 High |
| MCP-006 | Server versions MUST be pinned (no `@latest` in production projects) | 🟠 High |
| MCP-007 | Unused servers set to `"disabled": true` | 🟡 |
| MCP-008 | Filesystem server paths restricted to project directory only | 🟡 |
| MCP-009 | Quarterly credential rotation tracked | 🟡 |
| MCP-010 | mcp.json committed to Git with placeholder credentials (no real secrets) | 🟢 |

---

## Derivation Method

Unlike other generators that read steering content, MCP rules are derived by SCANNING the mcp.json file:

| Scan For | Generates |
|----------|-----------|
| `autoApprove` array contains write-pattern tools | MCP-003 violation |
| `args` array contains string matching API key/token patterns | MCP-004 violation |
| `@latest` in args | MCP-006 violation |
| Path entries pointing to `/`, `~`, system dirs | MCP-008 violation |
| Enabled servers not in project documentation | MCP-001 violation |

---

## Hook: `mcp-audit-log.json`

- **Event:** postToolUse
- **toolTypes:** `["^mcp_.*"]` (regex matches all MCP tool invocations)
- **Purpose:** Logs every MCP tool invocation for audit trail
- **Checks:** MCP-005 (the hook's existence IS the compliance)

---

## Tier: 2 (MCP governance activates once CI/development is established)

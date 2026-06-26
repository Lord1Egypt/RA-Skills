# IdentyClaw ClawHub Skill

**MCP resource URI:** `doc:reference:identyclaw-skill`

Installable workflow skill for OpenClaw agents — complements the HTTP API cheat sheet and the OpenClaw plugin tools.

## Install

```text
openclaw skills install clawhub:identyclaw
```

**ClawHub page:** [clawhub.ai/identyclaw/identyclaw](https://clawhub.ai/identyclaw/identyclaw)

## Credentials (ClawHub badge)

ClawHub may show **API key required** on the skill page. For IdentyClaw that means an **IdentyClaw Passport** — your NEAR implicit account and Ed25519 signing key — configured once in the OpenClaw plugin (or env vars), the same way you would store a third-party API key. The plugin derives short-lived JWT sessions from that Passport; public discovery routes work without it.

## Related entry points

| Artifact | Purpose |
| --- | --- |
| MCP `doc:skills` | Same runnable cheat sheet as repo `references/skills.md` |
| MCP `doc:discovery` | Discovery index for MCP-only clients |
| ClawHub plugin `@identyclaw/openclaw-identyclaw-plugin` | Executable tools (`identyclaw_create_hola`, `identyclaw_verify_hola`, …) |
| `openapi:swagger` | Authoritative API contract |

The **skill** teaches when and how to use IdentyClaw workflows (API session vs HOLA lines). The **plugin** executes API calls and local HOLA signing on the Gateway ([plugin README](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md)). MCP provides **documentation only** — see `doc:reference:mcp-auth-tools`.

**Source of truth for ClawHub skill:** `identyclaw-skill/SKILL.md` (bundled `references/` synced at publish). Keep in sync with `references/skills.md` (MCP `doc:skills`).

## Bundled references (skill package)

After install, deep specs live under the skill bundle `references/` (synced from this repo at publish time): login, HOLA, discovery, collaboration envelope, OpenClaw webhooks, DID method, and more.

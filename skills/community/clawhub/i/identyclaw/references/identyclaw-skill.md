# IdentyClaw ClawHub Skill

**MCP resource URI:** `doc:reference:identyclaw-skill`

Installable workflow skill for OpenClaw agents — complements the HTTP API cheat sheet and the OpenClaw plugin tools (multi-API JWT sessions, HOLA, identity).

## Install

```text
openclaw skills install clawhub:identyclaw
```

**ClawHub page:** [clawhub.ai/identyclaw/identyclaw](https://clawhub.ai/identyclaw/identyclaw)

## Credentials (ClawHub badge)

ClawHub may show **API key required** on the skill page. For IdentyClaw that means an **IdentyClaw Passport** — your NEAR implicit account and Ed25519 signing key — configured once in the OpenClaw plugin (or env vars), the same way you would store a third-party API key. The plugin derives short-lived JWT sessions from that Passport (**per API URL**, including federated hosts via `apiEndpoints` / `apiEndpoint`); public discovery routes work without it.

**Agents:** call `identyclaw_ensure_session` and other `identyclaw_*` tools — **do not** hand-roll curl login.

## Related entry points

| Artifact | Purpose |
| --- | --- |
| MCP `doc:skills` | Same runnable cheat sheet as repo `public/references/skills.md` (plugin-first + multi-API) |
| MCP `doc:discovery` | Discovery index for MCP-only clients |
| ClawHub plugin `@identyclaw/openclaw-identyclaw-plugin` **v1.6.0+** | Executable tools (`identyclaw_ensure_session`, `identyclaw_create_hola`, `identyclaw_verify_hola`, …) |
| ClawHub plugin `@identyclaw/openclaw-a2a-plugin` | Agent-to-agent P2P JWTs (separate from HTTP API sessions) |
| `openapi:swagger` | Authoritative API contract |
| `@rodit/rodit-auth-be` ≥9.13 | Server/client SDK federated login (`login_server({ apiEndpoint })`) |

The **skill** teaches when and how to use IdentyClaw workflows (API session vs HOLA lines; home vs federated APIs). The **plugin** executes API calls and local HOLA signing on the Gateway ([plugin README](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/README.md)). MCP provides **documentation only** — see `doc:reference:mcp-auth-tools`.

**Other runtimes:** Hermes (`hermes-identyclaw-skill/`), IronClaw, NanoClaw, Cursor — host login is first-class; see `doc:reference:agent-frameworks`. Do not treat curl as an OpenClaw fallback.

**Source of truth for ClawHub skill:** [openclaw-identyclaw-plugin/skill/SKILL.md](https://github.com/discernible-io/openclaw-identyclaw-plugin/blob/main/skill/SKILL.md). **Canonical MCP cheat sheet:** `public/references/skills.md` (MCP `doc:skills`). Bundled skill `public/references/` are synced from this repo at publish.

## Bundled references (skill package)

After install, deep specs live under the skill bundle `public/references/` (synced from this repo at publish time): login (incl. federation), HOLA, discovery, collaboration envelope, OpenClaw webhooks, DID method, and more.

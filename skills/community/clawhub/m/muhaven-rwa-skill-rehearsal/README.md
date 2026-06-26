# `@muhaven/openclaw-skill` — `muhaven-rwa-skill`

ClawHub-publishable OpenClaw skill that bundles a curated subset of
`@muhaven/mcp`. Hosted under the workspace name `@muhaven/openclaw-skill`
and published to ClawHub as `muhaven-rwa-skill`.

## Why a separate package?

The `@muhaven/mcp` package targets MCPB hosts (Claude Desktop, Cursor,
Claude Code) with all 22 tools across five groups (read / position /
policy / issuer / governance). The OpenClaw surface is investor-only:
read your portfolio + protection coverage + KYC attestation context,
stage a buy or claim, and pause the agent. The remaining tools
(`set_tier`, `audit_export`, `sell`, `rebalance`, the five issuer-side
tools, the two governance tools) are either dashboard-only ceremonies
or higher-blast-radius actions that need policy soak-time before going
live on a Telegram-driven surface.

ADR-C in `development/research-docs/WAVE_4_AGENTIC_RESEARCH_RESULT.md`
documents the architectural decision; `SKILL.md` carries the
operator-facing rationale.

## Boot sequence

1. OpenClaw runtime loads `manifest.json` + `config.json`.
2. `permissions.network.deny_default` + `permissions.filesystem.{read,write}: []`
   + `permissions.process.spawn: []` install before the skill binary
   starts. Any egress / FS / spawn attempt is denied at the runtime.
3. `bin/muhaven-rwa-skill.cjs` (CommonJS shim) calls `runOpenClawSkill()`.
4. `runOpenClawSkill()` delegates to `@muhaven/mcp`'s `runMcpStdioCli`
   with a `filterRegistry` callback that prunes excluded tools. The
   upstream's tool-description SHA-256 verification fires BEFORE the
   filter — so an attacker who patches a single descriptor cannot hide
   the patch by shipping a subset filter that excludes it.

## Tool subset (single source of truth)

The list lives in `src/index.ts` `TOOLSET_SUBSET`. `manifest.json` and
`SKILL.md` mirror it; `scripts/verify-subset.ts` runs at build time and
in CI to fail on drift.

| Tool | Group | Why included |
|---|---|---|
| `muhaven.read.portfolio` | read | Core "what do I own?" question |
| `muhaven.read.yields` | read | Per-token yield context |
| `muhaven.read.distribution` | read | Distribution-status answers |
| `muhaven.read.tokens` | read | Token list + symbols |
| `muhaven.read.audit` | read | "Why was I paused?" forensics |
| `muhaven.read.protection_coverage` | read | DefaultProtection reserve-rate aggregate (P11) |
| `muhaven.read.kyc_attestation` | read | KYC attestation explainer (P11) |
| `muhaven.position.buy` | position | Subscription buy intent |
| `muhaven.position.claim` | position | Yield claim intent |
| `muhaven.policy.pause` | policy | Kill-switch (cascade or per-surface) |
| `muhaven.policy.session_key_status` | policy | Read-only state inspection |

Excluded (11 total): `muhaven.position.sell`, `muhaven.position.rebalance`,
`muhaven.policy.set_tier`, `muhaven.policy.audit_export`, plus the five
`muhaven.issuer.*` tools (`distribute_yield`, `kyc_add`, `kyc_remove`,
`unpause_token`, `audit_query`) and the two P11 `muhaven.governance.*`
tools (`propose`, `cast_vote`). Each exclusion has a documented reason
in `manifest.json#mcp.tool_subset_excluded` and in `SKILL.md`
`mcp.toolset_excluded_reason`.

## Build + verify

```bash
pnpm --filter @muhaven/openclaw-skill build           # tsup ESM/CJS + DTS
pnpm --filter @muhaven/openclaw-skill verify-subset   # 9-way drift check (subset + excluded + tools[] + upstream + bundled_version triple-match)
pnpm --filter @muhaven/openclaw-skill typecheck       # tsc --noEmit
pnpm --filter @muhaven/openclaw-skill test            # vitest
```

## Three-tier confirmation contract

The skill itself never executes a state-mutating action. Tool calls
return an unsigned UserOp envelope plus a structured intent record;
the backend's `/api/v1/agent/openclaw/intent` endpoint mints a
confirmation record routed to one of three tiers based on amount.
See `backend/api/v1/agent/openclaw/*` for the routing and the
companion `telegram-bot/` worker for the Telegram surface.

## Hardening invariants

- `permissions.network.deny_default: true` — egress allowlist locked to
  the MuHaven backend + dashboard origins (`https://api.muhaven.app`,
  `https://muhaven.app`). Any new endpoint requires a manifest update +
  signed re-publish.
- `permissions.secrets.storage: os_keychain` — paste-token UX is forbidden.
- `permissions.process.spawn: []` — no shell, no Python, no JIT-compiled blob.
- Sigstore signing + GitHub OIDC trusted publishing — long-lived ClawHub
  tokens are not used.
- `required_reviewers: 2` — single-maintainer publish is rejected at the
  policy gate.

## Reference docs

- `development/research-docs/WAVE_4_AGENTIC_RESEARCH_RESULT.md` ADR-C
- `development/DEV_WAVE_4/TOOL_NAMESPACE.md`
- `development/DEV_WAVE_4/THREAT_MODEL_P0.md`
- `packages/mcp/README.md`

## License

MIT.

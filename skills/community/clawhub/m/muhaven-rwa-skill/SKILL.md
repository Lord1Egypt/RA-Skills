---
name: muhaven-rwa-skill
display_name: MuHaven RWA Portfolio
version: 0.1.4
schema_version: "1.0"
description: |
  Confidential real-world-asset (RWA) portfolio agent built on MuHaven's
  Fhenix-CoFHE-encrypted token primitives. Read your encrypted balances,
  stage yield claims, draft buys + claims for human confirmation. Position
  tools NEVER auto-submit — every state-mutating action goes through a
  three-tier confirmation surface (inline button ≤$200, Mini App + 6-digit
  OTP $200-$5K, deep-link passkey >$5K).
license: MIT
homepage: https://muhaven.app
documentation: https://github.com/hasToDev/muhaven/tree/master/packages/openclaw-skill
support: https://github.com/hasToDev/muhaven/issues
authors:
  - name: MuHaven
    email: hello@muhaven.app
    url: https://muhaven.app
maintainers:
  - hello@muhaven.app
keywords:
  - fhe
  - fhenix
  - rwa
  - muhaven
  - openclaw
  - confidential-defi
  - erc-3643
runtime:
  type: node
  node: ">=20"
  entry: dist/index.cjs
permissions:
  network:
    egress_allowlist:
      - https://api.muhaven.app
      - https://muhaven.app
    deny_default: true
  filesystem:
    read: []
    write: []
  process:
    spawn: []
  secrets:
    storage: os_keychain
    references:
      - name: muhaven_jwt
        owner: muhaven-broker
        scope:
          - mcp.read.*
          - mcp.propose.*
mcp:
  bundled: "@muhaven/mcp"
  # Exact version pin — `pnpm pack` rewrites `workspace:*` in package.json
  # to this exact value, which ClawHub consumers resolve from npm. The
  # `verify-subset.ts` triple-match enforces parity between this field,
  # `manifest.json#mcp.bundled_version`, and `packages/mcp/package.json#version`.
  # An earlier `bundled_minor_pin: true` claim was removed 2026-05-11
  # pre-publish review: the runtime + CI gates enforce exact equality,
  # not semver-minor-range; the field name implied a softer pin than the
  # code actually delivered.
  bundled_version: 0.1.5
  toolset_subset:
    - muhaven.read.portfolio
    - muhaven.read.yields
    - muhaven.read.distribution
    - muhaven.read.tokens
    - muhaven.read.audit
    - muhaven.read.protection_coverage
    - muhaven.read.kyc_attestation
    - muhaven.position.buy
    - muhaven.position.claim
    - muhaven.policy.pause
    - muhaven.policy.session_key_status
  toolset_excluded:
    - muhaven.position.sell
    - muhaven.position.rebalance
    - muhaven.policy.set_tier
    - muhaven.policy.audit_export
    - muhaven.issuer.distribute_yield
    - muhaven.issuer.kyc_add
    - muhaven.issuer.kyc_remove
    - muhaven.issuer.unpause_token
    - muhaven.issuer.audit_query
    - muhaven.governance.propose
    - muhaven.governance.cast_vote
  toolset_excluded_reason: |
    Exclusions are deliberate per ADR-C — the OpenClaw surface is
    investor-buy-and-claim, not portfolio-management. `set_tier` requires
    the dashboard passkey ceremony (cannot be a Telegram callback);
    `audit_export` is operator-shaped and lives behind the dashboard.
    `sell` + `rebalance` raise the blast radius of a single misclick on
    a Telegram inline button — defer to Wave 5 once we have soak data.
    `issuer.*` (Wave 4 P7) is issuer-only — the OpenClaw surface is
    investor-facing; issuer flows live on HavenBot in-dashboard +
    standalone `@muhaven/mcp` install.
    `governance.*` (Wave 4 P11) requires the dashboard ConfirmModal +
    cofhe encrypt ceremony, neither of which the Telegram-bot surface
    can drive. Investors who want to vote follow the dashboard flow.
sandbox:
  runtime: nemoclaw
  forward_compat:
    - issue: "openclaw#28298"
      compat_field: permissions
    - issue: "openclaw#28360"
      compat_field: sandbox
publishing:
  registry: clawhub
  trusted_publishing:
    provider: github
    workflow: ".github/workflows/openclaw-skill-publish.yml"
    oidc_audience: "openclaw://clawhub-trusted-publish"
  signing:
    provider: sigstore
    artifact: "muhaven-rwa-skill-{version}.tgz"
    bundle: "muhaven-rwa-skill-{version}.tgz.sigstore"
  required_reviewers: 2
threat_model_ref: "../../development/DEV_WAVE_4/THREAT_MODEL_P0.md"
---

# MuHaven RWA Portfolio — OpenClaw skill

This skill bundles a curated subset of `@muhaven/mcp` plus an OpenClaw-shaped
config bundle. It runs in OpenClaw's NemoClaw runtime (or any MCP host that
honours the manifest's `permissions` block) and connects to the live
MuHaven backend at `https://api.muhaven.app`.

## What it does

- **Reads your encrypted RWA portfolio** — balances stay encrypted with
  Fhenix CoFHE; the skill never sees plaintext.
- **Stages buy + claim intents** for the OpenClaw surface — the skill
  never auto-submits. Every intent emits a structured confirmation
  request to one of three tiers based on amount.
- **Surfaces audit log** for compliance / forensics.
- **`/pause` kill-switch** uninstalls the on-chain `@zerodev/permissions`
  validator within one Arb block.

## What it intentionally cannot do

- Move funds without your passkey. The skill issues unsigned UserOp
  envelopes; signing happens in the `muhaven-broker` daemon (≤$200 inline
  callback) or in your dashboard / Mini App (>$200 tiers).
- Speak to anything outside the egress allowlist. `manifest.json`'s
  `network.deny_default: true` means a tampered binary cannot exfiltrate
  to a third party.
- Read or write your filesystem. `permissions.filesystem.{read,write}: []`.
- Spawn child processes. `permissions.process.spawn: []`.
- Store any secret. JWT lives in `muhaven-broker`'s OS-keychain entry; the
  skill calls the broker over Unix-socket / named-pipe IPC.

## How to install

1. Install plain OpenClaw + ClawHub CLI globally:
   ```bash
   npm install -g openclaw@latest clawhub
   openclaw --version    # confirm install
   clawhub --version
   ```
   (Runtime decision 2026-05-11: plain OpenClaw under
   `sandbox.fallback: host_native`. NemoClaw remains the preferred
   runtime claim in `manifest.json` for forward-compat; today's deploy
   targets plain OpenClaw.)
2. Install the broker daemon **separately as a global** so its bin
   lands on `$PATH` regardless of ClawHub's bin-handling:
   ```bash
   npm install -g @muhaven/mcp@0.1.5
   muhaven-broker --version    # sanity check
   ```
   (The skill itself bundles `@muhaven/mcp` inline since 0.1.1 via tsup
   `noExternal`, so no separate `npm install --omit=dev` is needed after
   `clawhub install`. The global install of `@muhaven/mcp` is still useful
   because it puts the `muhaven-broker` daemon bin on `$PATH` — the skill's
   bundled copy of `@muhaven/mcp` only exposes the MCP server, not the
   daemon CLI.)
3. Install the skill:
   ```bash
   clawhub install muhaven-rwa-skill@0.1.4
   ```
4. One-shot broker setup + passkey login:
   ```bash
   muhaven-broker setup
   ```
   This applies sensible env defaults, mints an ephemeral session key,
   spawns the daemon detached, and runs the device-code login — opens
   `https://muhaven.app/link?code=XXXX-XXXX` in your browser for
   passkey approval. The daemon stays running after `setup` returns.
   Use `muhaven-broker setup --foreground` if a supervisor will manage
   the daemon process.
5. Optional: link your Telegram account for the `/agent/openclaw/*`
   confirmation surface. From the dashboard `/agent` page → Telegram
   tab → "Link Telegram" → message the bot at `@muhaven_bot` with the
   one-time link code.

## Confirmation tiers

The skill never executes a state-mutating action without a confirmation.
Three tiers based on intent notional (USDC):

| Range | Surface | Why |
|---|---|---|
| **≤ $200** | Telegram inline keyboard "Confirm" button | Low blast radius. Same trust model as a $200 mobile wallet payment — single-tap inline. |
| **$200 – $5,000** | Mini App with 6-digit OTP sent via separate Telegram message | Defends against a chat-stuffing attack where the LLM emits a `Confirm` button users tap on autopilot. OTP is out-of-band. |
| **> $5,000** | Deep-link to dashboard `https://muhaven.app/agent/confirm?intent=…` for passkey signature | Phishing-resistant by construction — WebAuthn RP-ID is bound to the dashboard origin; a Telegram-based MITM cannot complete passkey. |

Tier boundaries are audit-logged in `agent_audit_events` with the
amount-bucket the intent fell into. Investors can lower the boundaries
in the dashboard `/agent` policy tab; they cannot raise them above the
hardcoded ceilings (regulatory + Reg BI Care Obligation).

## Hardening invariants (do NOT relax without audit)

- `permissions.network.deny_default: true` — every new endpoint requires a
  manifest update + signed re-publish.
- `permissions.secrets.storage: os_keychain` — paste-token UX is forbidden.
- `runtime.type: node` — no shell, no Python, no JIT-compiled blob.
- `mcp.toolset_subset` is the only set of tools the skill will dispatch
  to — additions require an ADR + signed re-publish.
- Sigstore signing + GitHub OIDC trusted publishing — long-lived ClawHub
  tokens are not used. ClawHavoc (Feb 2026) precedent.
- `required_reviewers: 2` — single-maintainer publish is rejected at the
  policy gate. Two-maintainer release is the lesson from the Anthropic
  MCP SDK STDIO arbitrary-command CVEs (Apr 2026).

## Tool inventory (subset of `@muhaven/mcp`)

See `manifest.json` and the upstream descriptors in
`@muhaven/mcp/src/tools/descriptions.ts`. The skill only re-advertises
the `mcp.toolset_subset` listed in this frontmatter; descriptor SHA-256
hashes are pinned in `tool-hashes.json` and verified on every skill
load (mcp-context-protector pattern, post-MCPoison).

## Reference docs

- ADR-C in `development/research-docs/WAVE_4_AGENTIC_RESEARCH_RESULT.md`
- `development/DEV_WAVE_4/TOOL_NAMESPACE.md` for the full naming surface
- `development/DEV_WAVE_4/THREAT_MODEL_P0.md` for OWASP LLM + Agentic mappings

## License

MIT. See `LICENSE` in the repository root.

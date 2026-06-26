# Security posture — `muhaven-rwa-skill`

> Plain-text companion to the JSON `manifest.json` + `config.json`
> permissions blocks. Scanners (ClawScan, snyk-mcp-scan) lift narrative
> from this file; JSON `$comment` keys are ignored by most tools.
>
> If you operate this skill in production, read §"Operator posture
> requirements" before installing.

## TL;DR

- The skill is published with prod-only network egress (`api.muhaven.app` +
  `muhaven.app`).
- The skill **never auto-submits** any state-mutating action. Every
  position/policy tool emits an intent for a three-tier confirmation
  ceremony (Telegram inline / Mini App OTP / dashboard passkey).
- The kernel-enforced sandbox claim (`sandbox.runtime: nemoclaw`) is
  forward-compatible **but not currently load-bearing** — see §"Sandbox
  runtime: NemoClaw vs host_native".

## Sandbox runtime: NemoClaw vs host_native

`manifest.json#sandbox` declares two posture fields:

```jsonc
{
  "sandbox": {
    "runtime": "nemoclaw",
    "fallback": "host_native"
  }
}
```

The OpenClaw ecosystem ships two runtimes:

| Runtime | Posture | Permission enforcement |
|---|---|---|
| **NemoClaw** | Containerized; NVIDIA OpenShell + GPU stack required | Kernel-enforced — `permissions.network.egress_allowlist`, `filesystem.{read,write}`, `process.spawn`, and `secrets.deny_paste_ui` are honored by the runtime; unknown fields are treated as deny per OpenClaw issue #28298 |
| **Plain OpenClaw** (`npm install -g openclaw@latest`) | Host-native — runs as the operator's user; `fallback: host_native` is the published escape hatch | **Advisory only** — the manifest's permissions block is metadata. The runtime does NOT block egress, file reads, or process spawns based on the manifest |

**Operator decision 2026-05-11 (commit `c8aba6d`)**: this skill is
currently deployed against **plain OpenClaw** under `fallback:
host_native`. This is documented in `manifest.json#sandbox` and
`SKILL.md` "Sandbox" section, but the security implication is worth
stating plainly here: **in host_native mode, the manifest's permissions
block is documentation, not enforcement**.

Defense-in-depth measures that DO work in host_native mode:

1. **Bin shim `host_native` posture** — `bin/muhaven-rwa-skill.cjs` is
   the launch target (not `dist/index.cjs` directly). It runs the skill
   under the operator's user with no privilege escalation.
2. **Tool-description hash pinning** — `@muhaven/mcp`'s
   `verify-tool-hashes --check` runs at server startup and exits non-zero
   on descriptor drift (MCPoison-style attacks fail-closed).
3. **Broker JWT-scope check** — write paths require a JWT scoped to
   `mcp.propose.*`. The broker daemon's `signHash` is the only route to
   a UserOp signature; the JWT is bound to the user's account.
4. **Three-tier confirmation** — `position.*` + `policy.pause` emit
   intents that REQUIRE an out-of-band confirmation surface. Even an
   LLM-side compromise cannot bypass the user's Telegram / passkey
   ceremony, because the dashboard's runner is the only path that
   bundles + submits the signed UserOp.
5. **STDIO-only transport** — no TCP, no `mcp-remote`
   (CVE-2025-6514 ban).

## Upgrade path: NemoClaw enforcement

The skill is **forward-compatible** with NemoClaw kernel enforcement.
When the operator's homelab is willing to host the NVIDIA OpenShell + GPU
stack, the upgrade is:

1. `npm install -g nemoclaw@latest`.
2. Re-install the skill via `nemoclaw install muhaven-rwa-skill@<version>`
   (or the equivalent ClawHub flow that points at NemoClaw).
3. Verify enforcement with `nemoclaw doctor muhaven-rwa-skill` — egress
   to any host outside `api.muhaven.app` + `muhaven.app` MUST fail with
   `EACCES`; filesystem writes MUST fail.

No code change in the skill itself is required to switch runtimes — the
permissions block is already authored for kernel enforcement.

The published artifact stays **prod-pure** (egress allowlist pins
production hosts). Staging rehearsals (`AGENTIC_TEST_PLAN.md` §3 Path
(a)) install the same signed tarball with a
`user_config.backend_url=https://api-stage.muhaven.app` override and rely
on plain OpenClaw's advisory posture. A kernel-enforced runtime would
correctly reject that staging override — that is intentional.

## Operator posture requirements

Three things the operator MUST configure regardless of runtime:

1. **`MUHAVEN_BROKER_SESSION_KEY` provenance**:
   - The session key is the private half of a ZeroDev session key
     scoped to the user's smart-account, bounded by a
     `@zerodev/permissions` validator.
   - Mint it via the dashboard `/agent/policy/transition` flow (Q1 in
     the post-§4 queue). DO NOT generate `crypto.randomBytes(32)`
     locally — the validator binding lives on-chain and is what
     constrains the key's authority.
   - The key is held by `muhaven-broker` (sibling daemon shipped in
     `@muhaven/mcp`). The MCP server never sees it.
2. **Broker daemon must be reachable**:
   - The skill calls `muhaven-broker` over a Unix socket (POSIX) or named
     pipe (Windows). Path defaults to `~/.muhaven/broker.sock` on POSIX,
     `\\.\pipe\muhaven-broker-<user>` on Windows.
   - If the broker is unreachable, every tool call returns a structured
     `connect_failed` error — the LLM does NOT attempt a fallback.
3. **JWT must be present**:
   - Run `muhaven-broker login` once. The device-code flow links the
     install to the user's MuHaven account. Subsequent tool calls fetch
     the JWT from the broker keystore.

## Network egress allowlist

| Host | Port | Reason |
|---|---|---|
| `api.muhaven.app` | 443 | MuHaven backend — REST API + agent policy + intent confirmation |
| `muhaven.app` | 443 | Dashboard origin — deep-link target for >$5K confirmations + device-code authorization (`/link`) |

No other egress is required at runtime. The skill does NOT:

- Reach out to an LLM provider (LLM is the host's responsibility, e.g.
  Claude Desktop / Cursor).
- Hit any block-explorer / RPC endpoint (RWA / portfolio queries go
  through the MuHaven backend's indexer).
- Resolve DNS dynamically — `dns.deny_dynamic_allowlist_resolution: true`
  in `config.json`.

## Filesystem + spawn posture

- `filesystem.read = []`, `filesystem.write = []` — the skill does not
  read or write any path on the operator's system. (Broker daemon's
  keystore + socket are out-of-process, owned by `@muhaven/mcp`.)
- `process.spawn = []` — the skill does not fork or exec.
- `process.stdio = "manifest_only"` — STDIO is reserved for MCP JSON-RPC
  frames; stderr is captured-and-audit-only in NemoClaw, plain-printed
  in host_native.

## Dependency freshness — operator-driven, best-effort

Starting with `0.1.1`, the published skill **inline-bundles `@muhaven/mcp`
+ `@modelcontextprotocol/sdk` + `viem` + `zod`** into a single ~686KB
`dist/index.cjs` (via tsup `noExternal`). This solves the ClawHub
install-time gap (the installer doesn't run `npm install` to resolve
transitive deps), but trades it for a **CVE-propagation lag**: a future
patch to any bundled dep does NOT propagate to existing skill
installations until the skill itself is re-published.

**Posture (not a contractual SLO)**: this is a one-maintainer project
with no paid security-watch automation; the times below describe what
the maintainer aims for, not what they guarantee. Treat the table as an
informed default, not an indemnified commitment.

| CVE severity | Re-publish posture (best effort) |
|---|---|
| Critical / High | within 7 days of the upstream patch landing on npm |
| Medium | within 30 days |
| Low | rolled into the next planned skill release |

Anyone with a faster operational risk tolerance should pin a specific
`muhaven-rwa-skill` version they've audited themselves and re-evaluate
on a self-driven cadence rather than relying on a downstream re-publish.

How to track upstream issues directly:

- Watch the GH repo: <https://github.com/hasToDev/muhaven/security/advisories>
  (advisories filed here; the muhaven-rwa-skill tag list reflects the
  actual re-publishes that include each fix).
- Run `npm audit` against `@muhaven/mcp` (the source of the bundled
  graph) on your own schedule. The bundled artifact's npm-audit posture
  matches `@muhaven/mcp`'s npm-audit at the snapshot moment.
- Skill-side `CHANGELOG.md` calls out CVE-driven re-publishes explicitly
  under `### Security`.

## OS keychain backing — not bundled

The `@muhaven/mcp` package declares `@napi-rs/keyring` as an
**optional dependency** for platform-specific OS-keychain native bindings
(Windows DPAPI, macOS Security framework, Linux Secret Service over
D-Bus). The skill's inline bundle does **NOT** include the native
keyring — bundling one platform's binary into a cross-platform tarball
would be a net regression.

**Practical effect:** the bundled `@muhaven/mcp`'s keystore falls back
to `FileKeystore` (mode 0600, AES-256-GCM with a machine-id-derived
KEK) when the native dep is absent. The fallback is documented as a
first-class backend in `@muhaven/mcp/README.md` — operators on WSL2 /
devcontainer / SSH-remote already use it.

If you want the OS keychain backing:

```bash
npm install -g @muhaven/mcp@0.1.3   # installs the optional native dep
```

The global install is recommended anyway because the `muhaven-broker`
daemon bin lives in `@muhaven/mcp`'s `bin/` and only that install puts
it on `$PATH`.

## Reporting vulnerabilities

Open an issue at <https://github.com/hasToDev/muhaven/issues> tagged
`security` — or, for high-severity findings that benefit from coordinated
disclosure, email `hello@muhaven.app`. The MuHaven team treats privacy +
fund-safety findings as P0.

We acknowledge security researchers in `development/DEV_WAVE_4/DEV_LOG.md`
once a finding is fixed and disclosed.

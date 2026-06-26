# Changelog

All notable changes to `muhaven-rwa-skill` (the OpenClaw skill bundling
`@muhaven/mcp`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.4] — 2026-05-17

Re-bundles against `@muhaven/mcp@0.1.5` so the new `muhaven-broker
stop` subcommand is available to skill consumers (who also install
`@muhaven/mcp` globally for the broker bin per SKILL.md "How to
install"). No tool-subset or sandbox changes; passthrough version bump.

### Changed

- **Bundled `@muhaven/mcp` bumped 0.1.4 → 0.1.5** (`manifest.json#mcp.bundled_version`
  + `SKILL.md` frontmatter + the `verify-subset.ts` triple-match guard).
  Operators following SKILL.md should `npm install -g @muhaven/mcp@0.1.5`
  so the new `muhaven-broker stop` is on `$PATH` alongside the existing
  `muhaven-broker setup`.

## [0.1.3] — 2026-05-17

Re-bundles against `@muhaven/mcp@0.1.4` so the new
`muhaven-broker setup` subcommand is available to skill consumers who
also install `@muhaven/mcp` globally for the broker bin (per
SKILL.md "How to install" prerequisite). No tool-subset or sandbox
changes; this is a passthrough version bump that flows the upstream
0.1.4 release into the published skill bundle.

### Changed

- **Bundled `@muhaven/mcp` bumped 0.1.3 → 0.1.4** (`manifest.json#mcp.bundled_version`
  + `SKILL.md` frontmatter + the `verify-subset.ts` triple-match guard).
  Operators following the SKILL.md install runbook should
  `npm install -g @muhaven/mcp@0.1.4` so the `muhaven-broker setup`
  bin is on `$PATH`.
- **`SKILL.md` install steps** updated to reference `setup` as the
  one-shot install path; the prior five-line manual broker ritual is
  no longer the documented happy path.

## [0.1.2] — 2026-05-17

Cosmetic fix — corrects the display name shown on ClawHub. No code or
manifest schema changes; bundled `@muhaven/mcp@0.1.3` is identical to
0.1.1.

### Fixed

- ClawHub display name now reads "MuHaven RWA Portfolio" (matching
  `manifest.json#display_name`). 0.1.1 was published without the
  `clawhub publish --name "<...>"` flag, which caused clawhub v0.12.3 to
  fall back to the path basename (`package` from `pnpm pack` output) and
  render the skill title as "Package". The fix is to always pass
  `--name` explicitly on publish; recipe codified in memory
  `feedback_clawhub_publish_explicit_name`.

## [0.1.1] — 2026-05-16

Q2 fix bundle from the post-§4 queue closing the ClawScan findings and
the `npm install --omit=dev` install-time gap. Pins `@muhaven/mcp@0.1.3`
which carries the broker-side fixes for the §3e⁶ broker-session-key,
broker-env-divergence, and serverInfo-version findings.

### Added

- **`SECURITY.md`** at the package root, documenting:
  - host_native vs NemoClaw posture (the published artifact runs against
    plain OpenClaw under `sandbox.fallback: host_native` per operator
    decision 2026-05-11; `manifest.permissions` are advisory in that
    mode, not kernel-enforced).
  - Defense-in-depth measures that DO work in host_native mode
    (tool-description hash pinning, broker JWT-scope check, three-tier
    confirmation, STDIO-only transport).
  - NemoClaw upgrade path (forward-compatible — no skill change required).
  - Operator posture requirements (session-key provenance, broker
    reachability, JWT presence).
  - Network egress allowlist + reason for each pinned host.
  - Filesystem + spawn posture (deny-all).
  - Vulnerability reporting channels.
  - Closes ClawScan #1 (host_native trade-off documented in a
    scanner-visible file, not just `$comment` JSON keys).

### Changed

- **`tsup.config.ts` now inline-bundles `@muhaven/mcp`** via
  `noExternal: ['@muhaven/mcp']`. The published tarball is self-contained
  — ClawHub install no longer needs an out-of-band `npm install --omit=dev`
  to resolve the transitive dep. Dist size grows from ~25KB → ~686KB; the
  added bytes are entirely the @muhaven/mcp + viem + zod + MCP SDK
  transitive graph. Closes ClawScan #3 + §3e⁶
  F-clawhub-install-no-npm-install (HIGH).
- **`muhaven.policy.pause` tool description tightened** to "Activate
  /pause kill-switch (uninstallPlugin). NEVER auto-submits — requires
  user confirmation." (was "Activate /pause kill-switch
  (uninstallPlugin)."). The description is what the LLM sees and surfaces
  to the user; the "NEVER auto-submits" assertion now appears at the LLM
  tool-call layer alongside the existing config-layer assertion. Closes
  ClawScan #2.
- **Pinned `@muhaven/mcp@0.1.3`** (was 0.1.2). The new MCP version
  carries: lazy broker-session-key validation, `muhaven-broker login
  --from-daemon` flag, build-time `serverInfo.version` inject. None of
  these changes affect the skill's API surface — the tool subset stays
  identical.

### Tests

- 15/15 vitest pass (manifest-consistency × 3 + subset × 9 + lifecycle × 3).
- Manifest-consistency triple-match enforced at vitest gate time:
  `manifest.json#mcp.bundled_version === SKILL.md#mcp.bundled_version ===
  packages/mcp/package.json#version === 0.1.3`.

## [0.1.0] — 2026-05-12

First publishable cut to ClawHub. See `development/DEV_WAVE_4/DEV_LOG.md`
2026-05-12 entry for the publish-ceremony walkthrough.

### Added — Tools (11 subset)

- `muhaven.read.*` (7): `portfolio` · `yields` · `distribution` · `tokens` ·
  `audit` · `protection_coverage` · `kyc_attestation`
- `muhaven.position.*` (2): `buy` · `claim`
- `muhaven.policy.*` (2): `pause` · `session_key_status`

### Added — Infrastructure

- OpenClaw `manifest.json` (schema_version 1.0) declaring permissions
  block + four `user_config` entries (`backend_url`, `dashboard_url`,
  `broker_endpoint`, `read_only`).
- ClawSecure `config.json` mirroring permissions for kernel-enforced
  NemoClaw runtimes.
- Tool-subset triple-match gate (`scripts/verify-subset.ts`) enforcing
  `src/index.ts:TOOLSET_SUBSET === manifest.json#mcp.tool_subset ===
  SKILL.md#mcp.toolset_subset`.

### Distribution

- Published to ClawHub as `muhaven-rwa-skill-rehearsal@0.1.0-rc.1` (the
  rehearsal slot); promoted to `muhaven-rwa-skill@0.1.0` upon §3 Path (a)
  walkthrough closure.

[Unreleased]: https://github.com/hasToDev/muhaven/compare/openclaw-skill-v0.1.2...HEAD
[0.1.2]: https://github.com/hasToDev/muhaven/releases/tag/openclaw-skill-v0.1.2
[0.1.1]: https://github.com/hasToDev/muhaven/releases/tag/openclaw-skill-v0.1.1
[0.1.0]: https://github.com/hasToDev/muhaven/releases/tag/openclaw-skill-v0.1.0

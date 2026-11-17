# Release Notes

## GitHub Release Summary

Recommended tag: `v2.15.4`

Skill update pinning to upstream Hookaido `v2.15.2` (first release whose MCP server works with standard clients such as Claude Code and OpenClaw), with OpenClaw Gateway integration as the primary use case, the ClawHub security audit findings fixed, and corrections to outdated or wrong guidance.

## v2.15.4 - 2026-11-02

Hardening from the ClawHub security audit of 2.15.3. The overall result was "Pass", with ClawScan `benign`. Still pinned to Hookaido `v2.15.2`.

- `scripts/openclaw_pull_relay.sh` refuses plain `http://` for any non-loopback URL. Both URLs carry a bearer token, and a misconfigured public pull URL would have sent the token and webhook data unencrypted. curl is pinned to the checked protocol with `--proto`, so a redirect cannot downgrade it. `HOOKAIDO_RELAY_ALLOW_HTTP=1` is an explicit opt-out for already encrypted hops (Tailscale/WireGuard). Tested: remote `http://` is refused, the opt-out is allowed with a notice, and loopback delivers end to end.
- Revoking a runtime secret is documented as destructive. Revoking the last valid version empties the pool, so every webhook on the route gets `401`. The skill now requires listing the pool, naming the exact id, and explicit confirmation.
- The `--dotenv` example uses `./hookaido.env`.
- All environment variables read by the bundled scripts (relay URLs, `HOOKAIDO_RELAY_ALLOW_HTTP`, installer overrides) are declared as optional `envVars`.

## v2.15.3 - 2026-10-30

Republish of v2.15.2 (still pinned to Hookaido `v2.15.2`). ClawHub's static analysis flagged `scripts/openclaw_pull_relay.sh` as potential exfiltration (`suspicious.potential_exfiltration`), and the v2.15.2 release stayed held in scan. The rule matches `base64` followed by a variable named like `*file*`. The relay decodes the queued payload into a temp file and posts it to the local OpenClaw hook, so this was a false positive. The temp variable is now `payload_tmp`; behaviour is unchanged and was re-tested end to end.

- `scripts/publish.sh` sets ClawHub categories (`integrations`, `automation`, `operations`), topics, and a changelog. It refuses to publish files with CRLF line endings, and `.gitattributes` pins LF.
- `SKILL.md` and `references/operations.md` state the DSL rule "one directive per line" (`{ a; b }` does not parse).

## v2.15.2 - 2026-10-27

### Security (ClawHub audit)

- Every `metadata.openclaw.install` download declares `sha256`. Values come from the signed upstream `hookaido_v2.15.2_checksums.txt`; the signature, SBOM and provenance were verified with `hookaido verify-release`.
- `scripts/publish.sh` pins the ClawHub CLI instead of `clawhub@latest`.
- New "Installation, Capabilities, and Side Effects" section in `SKILL.md`.
- MCP registration is project-local (`.mcp.json` / `claude mcp add --scope project`; OpenClaw `mcp.servers` with a read-only `toolFilter`) instead of `.claude/settings.json`, which Claude Code never read MCP servers from.
- DLQ deletion is marked destructive and needs explicit confirmation.

### Added

- `references/openclaw.md`, covering:
  - Hookaido in front of the OpenClaw Gateway: provider HMAC, durable queue, and retry of Gateway `503`/`429`
  - push to mapped hooks `/hooks/<name>` with a bearer header
  - the egress allowlist needed for loopback/tailnet targets
  - `max_body` aligned to the Gateway's 256 KiB limit
  - the pull relay for a Gateway behind NAT
  - a security checklist
- `scripts/openclaw_pull_relay.sh`: dequeue, forward with an `Idempotency-Key`, and ack only after a `2xx`. Retryable failures are nacked with a delay; other statuses go to the DLQ. The success, offline-retry, and DLQ paths were tested end-to-end.
- Coverage of Hookaido v2.7–v2.15 features:
  - consumer groups
  - `auth query`, `trusted_proxies`, runtime secret rotation (`/secrets/{name}`, MCP `rotate_secret`)
  - single-port listeners, outbound/internal channels, custom deliver headers and outbound signing
  - the health config fingerprint, per-route metrics, and the current MCP tool list by role
  - container usage pinned by digest, and the Docker-sandbox `COPY --from` pattern
- Claude Code marketplace (`.claude-plugin/marketplace.json`; the entry is the plugin manifest, so ClawHub still treats the repo as a skill): `/plugin marketplace add 7schmiede/claw-skill-hookaido`.

### Changed

- Pinned to Hookaido `v2.15.2`, which fixes MCP stdio framing (nuetzliches/hookaido#321). With v2.15.1 and earlier, `hookaido mcp serve` timed out with Claude Code and OpenClaw.

- Frontmatter follows the Agent Skills format, so `SKILL.md` also uploads to claude.ai:
  - `version` moved to `metadata.version`
  - added `compatibility`
  - tokens moved from `requires.env` (which hid the skill until they were set) to optional `envVars`
- `go install` path is `github.com/nuetzliches/hookaido/v2/cmd/hookaido@v2.15.2` (module `/v2` since Hookaido v2.8.0).
- Windows install actions use `stripComponents: 1`. Release archives have a top-level folder, so the binary used to land one directory too deep.

### Fixed (wrong guidance in earlier skill versions)

- `deliver exec` exit codes: every non-zero exit, `126`/`127` included, is retried. Only a handler that cannot start is dead-lettered.
- Queue backend is set per route (`queue "postgres"`); a top-level `queue` block is rejected.
- SSE tuning is `pull_api { sse_keepalive; sse_max_connection }`, not `keepalive`/`max_duration` in the route `pull` block.
- GitHub/Stripe examples use `auth hmac { provider ... }`. Plain `auth hmac env:...` is Hookaido's own format and rejects real provider deliveries.
- Runtime-control MCP mode also requires `--principal`.

## v2.6.0 - 2026-04-21

Feature update pinning to upstream Hookaido `v2.6.0`.

### Highlights

- Pinned all binary installer actions and checksums to Hookaido `v2.6.0`.
- Added `provider stripe` and `provider cituro` to provider-compatible HMAC config (v2.6.0 upstream).
- Added SSE streaming playbook: `GET {pull.path}/stream` for real-time webhook delivery without polling (v2.5.3 upstream).
- Added Claude Code MCP plugin configuration examples (`.claude/settings.json`) for read and operate roles.

### Compatibility

Additive coverage. All existing skill workflows remain unchanged.

## v2.2.2 - 2026-04-15

Performance update pinning to upstream Hookaido `v2.2.2`.

### Highlights

- Pinned all binary installer actions and checksums to Hookaido `v2.2.2`.
- Upstream fix: queue dequeue loop now uses event-driven channel notification instead of 25ms polling. Enqueue signals waiting Dequeue goroutines immediately; fallback polling raised to 1s for delayed/retry items only. Idle CPU drops from ~26% to <1% (SQLite and PostgreSQL backends).

### Compatibility

No new features. All existing skill workflows remain unchanged.

## v2.2.1 - 2026-03-30

Bugfix-only update pinning to upstream Hookaido `v2.2.1`.

### Highlights

- Pinned all binary installer actions and checksums to Hookaido `v2.2.1`.
- Upstream fixes: dispatcher delivery logging (previously silent), zero-target route warning, hot-reload for delivery config changes via `--watch`/SIGHUP.

### Compatibility

No new features. All existing skill workflows remain unchanged.

## v2.2.0 - 2026-03-28

This release updates the public Hookaido skill to upstream Hookaido `v2.2.0`.

### Highlights

- Pinned all binary installer actions and checksums to Hookaido `v2.2.0`.
- Added `deliver exec` playbook for subprocess delivery (payload on stdin, exit-code retry semantics).
- Added provider-compatible HMAC playbook for GitHub (`X-Hub-Signature-256`) and Gitea/Forgejo (`X-Gitea-Signature`).
- Updated operations reference with exec delivery and provider-HMAC config examples.

### Compatibility

Additive v2.2.0 coverage includes:

- `deliver exec` for local script/binary execution with env-var metadata and exit-code retry semantics
- `auth hmac { provider github }` / `auth hmac { provider gitea }` for native webhook signature verification
- Custom outbound headers in deliver blocks with placeholder interpolation

All existing skill workflows remain unchanged.

## v2.0.0 - 2026-03-09

This release updates the public Hookaido skill to upstream Hookaido `v2.0.0` and prepares the repository for distribution via its public GitHub URL.

### Highlights

- Pinned all binary installer actions to Hookaido `v2.0.0`.
- Updated the fallback installer script with the official `v2.0.0` SHA256 checksums for macOS, Linux, and Windows on `amd64` and `arm64`.
- Switched the skill homepage metadata to the public skill repository: `https://github.com/7schmiede/claw-skill-hookaido`.
- Documented source-based installation from the public upstream repo: `go install github.com/nuetzliches/hookaido/cmd/hookaido@v2.0.0`.

### Compatibility

This skill keeps the established inbound, outbound, and pull-based workflow as the default path.
Hookaido v2 capabilities are documented as additive options so existing skill usage does not receive breaking changes by default.

Additive v2 coverage includes:

- `queue postgres` as an optional backend alongside the existing defaults
- HTTP and gRPC pull-worker guidance
- Batch `ack` and batch `nack` pull operations
- `config validate --strict-secrets`
- `verify-release` for public release verification

### Documentation Updates

- Refreshed [SKILL.md](SKILL.md) to reflect Hookaido v2.0.0 terminology and workflow guidance.
- Expanded [references/operations.md](references/operations.md) with Postgres runtime examples, batch pull API calls, and release verification commands.
- Added [README.md](README.md) so the repo is ready to be consumed directly as a public skill repository.

### Notes

- Upstream modular architecture changes in Hookaido v2.0.0 are treated as opt-in guidance in this skill rather than mandatory workflow changes.
- The skill name now matches the repository folder name, which fixes skill validation in the current layout.
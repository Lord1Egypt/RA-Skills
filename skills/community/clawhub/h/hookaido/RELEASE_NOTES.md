# Release Notes

## GitHub Release Summary

Recommended tag: `v2.6.0`

Feature update pinning to upstream Hookaido `v2.6.0`.
New: Stripe and Cituro HMAC providers, SSE streaming endpoint, Claude Code MCP plugin guidance.

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
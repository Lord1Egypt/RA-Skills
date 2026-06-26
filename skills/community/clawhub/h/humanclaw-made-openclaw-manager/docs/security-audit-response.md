# Security Audit Response

This note responds to the ClawHub-style audit feedback that flagged OpenClaw Manager as suspicious.

## Summary

Two kinds of issues were mixed together in the report:

1. real hardening gaps
2. static-analysis false positives caused by combining unrelated local-only behaviors in one file

This release addresses both.

## What changed

- `bootstrap.ts` no longer combines environment reads, network checks, and process spawn logic in one file
- sidecar health checks are loopback-only by default
- sidecar autostart is disabled until the user explicitly allows it once
- the sidecar binds to `127.0.0.1` by default instead of all interfaces
- installers use the official npm registry and `npm ci`
- docs now explicitly disclose local storage, loopback-only networking, and connector opt-in behavior

## Response by finding

### Finding: environment variable access plus network send

**Assessment:** false positive in the original audit context.

Bootstrap reads only local manager configuration variables such as port, state root, bind host, and local sidecar URL. The network call is a local health check against the loopback sidecar endpoint.

Current default behavior:

- accepted health-check targets: `127.0.0.1`, `localhost`, `::1`
- non-loopback targets rejected unless `OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR=1`

### Finding: shell command execution plus network access

**Assessment:** false positive in the original audit context, but worth hardening.

The process spawn is used only to launch the local sidecar. The launcher now:

- uses `shell: false`
- launches only known local server entrypoints
- does not accept arbitrary shell command strings
- is gated behind explicit one-time autostart consent

### Finding: non-official npm registry

**Assessment:** valid.

The lockfile previously contained `registry.npmmirror.com` resolution URLs. The project now pins the official npm registry and uses `npm ci`.

### Finding: local HTTP sidecar and local state storage

**Assessment:** real behavior, but not malicious behavior.

The project is a local manager skill with a local sidecar and local durable state. This is now explicitly documented in the README, `skill.yaml`, and `SECURITY.md`.

## Current trust boundaries

- local-only bootstrap networking
- loopback-only sidecar by default
- connector networking only after explicit connector configuration
- no raw transcript upload by default
- local consent required before autostart

## Recommended reviewer checks

Reviewers can validate the hardening with:

```bash
npm run check
npm run build
node scripts/smoke-test.cjs
node scripts/security-smoke.cjs
```

The security smoke test confirms:

- non-loopback sidecar URLs are rejected by default
- sidecar bind host defaults to `127.0.0.1`
- bootstrap returns `consent_required` before autostart is allowed
- lockfile no longer contains `registry.npmmirror.com`

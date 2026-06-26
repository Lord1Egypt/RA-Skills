# Security Policy

This ClawHub edition is intentionally narrow and local-first.

## Supported version

| Version | Supported |
|---|---:|
| 1.0.x | yes |

## Security posture

- Zero npm dependencies.
- No npm install lifecycle hooks.
- No required environment variables or credentials.
- No script-side outbound network primitives.
- No process-spawning primitives in skill scripts.
- No dynamic code execution in skill scripts.
- Filesystem access is workspace-scoped.
- Published bundles exclude `.git/`, `.env`, OpenClaw local state, editor state, logs, and generated archives.
- The core output is a prompt bundle. Platform SDKs, certificates, signing keys, store tokens, and deployment secrets are Tier 1/Tier 2 concerns and must not be requested in the Tier 0 skill loop.

## Local preflight

```bash
npm run validate
npm run pack
```

`npm run validate` checks manifest parity, template health, eval coverage, package safety, ClawHub cleanliness, script safety, and secret-shaped token hygiene.

## Reporting

Open a GitHub issue at <https://github.com/peixl/ifq-app-builder/issues>. Do not include live secrets in reports.

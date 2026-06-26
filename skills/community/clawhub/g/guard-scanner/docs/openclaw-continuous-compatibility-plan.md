# guard-scanner Continuous OpenClaw Compatibility Plan

Date: 2026-03-12
Stable target: OpenClaw `2026.3.13`
Baseline regression lane: OpenClaw `2026.3.8`

## Goal

Keep `guard-scanner` compatible with the latest stable OpenClaw public plugin surface without relying on stale manual claims.

## Current automated controls

1. `npm run build:plugin`
   - Compiles `openclaw-plugin.mts` into `dist/openclaw-plugin.mjs`.
2. `npm run release:gate`
   - Verifies manifest shape, official discovery metadata, built entry existence, runtime hook registration, malicious block behavior, benign passthrough behavior, and stale-doc claim removal.
3. `npm run check:upstream`
   - Queries the npm registry and GitHub Releases for the latest stable `openclaw`, compares both sources against `devDependencies.openclaw`, writes `docs/generated/openclaw-upstream-status.json`, and fails on drift or source mismatch.

## Required operator flow when upstream changes

1. Run `npm run check:upstream`.
2. If drift is detected, update `devDependencies.openclaw` to the new stable version.
3. Re-run `npm install`, `npm run build:plugin`, `npm run release:gate`, and `npm test`.
4. Update compatibility docs only after runtime behavior has been re-verified.

## Quality bar

- No TS loader ambiguity in the public plugin entry.
- No broad compatibility claim outside the tested manifest/discovery/before_tool_call surface.
- No release if upstream drift is known but unverified.

## Pending future hardening

- Add a scheduled CI job that opens a drift report when `openclaw` stable changes.
- Expand runtime compatibility coverage if OpenClaw publishes a stable context-engine contract worth supporting.
- Add schema-level validation against an official machine-readable manifest contract if OpenClaw publishes one.

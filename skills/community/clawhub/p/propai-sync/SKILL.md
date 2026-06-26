---
name: propai-sync
description: Maintain and operate the PropAI Sync monorepo, including hosted-platform BYOK API validation and Railway deployment checks. Use when working in propai-sync to run scoped tests, build gates, hosted smoke checks (`/api/health`, `/api/auth/bootstrap`, `/api/users/me`), and ClawHub-ready skill publishing steps.
---

# PropAI Sync

Run all commands from the repo root.

## Execute Core Workflow

1. Inspect scope with `git status --short` and `git diff --name-only`.
2. Run focused quality checks for touched files.
3. Run `pnpm build` before any deploy or handoff.
4. Run hosted smoke with:
   - `node skills/propai-sync/scripts/hosted-smoke.mjs`
5. Record executed commands and outcomes in `HANDOFF.md`.

## Enforce Hosted Smoke Contract

- Verify `health_ok` is `true`.
- Verify bootstrap succeeds and returns an API key.
- Verify `/api/users/me` succeeds with that API key.
- Treat any non-2xx response as a failing gate.

## Run Railway E2E Validation

1. Authenticate Railway CLI:
   - `npx @railway/cli login`
   - `npx @railway/cli status`
2. Deploy from the current branch.
3. Validate live endpoints in this order:
   - `GET /api/health`
   - `POST /api/auth/bootstrap`
   - `GET /api/users/me` with `X-API-Key` from bootstrap
4. Log live URL, UTC timestamp, and endpoint results in `HANDOFF.md`.

## Publish To ClawHub

1. Bump version and changelog summary for the skill update.
2. Publish:
   - `clawhub publish skills/propai-sync --slug propai-sync --name "PropAI Sync" --version <semver> --tags latest --changelog "<summary>"`

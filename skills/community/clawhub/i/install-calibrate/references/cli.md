# Calibrate installer CLI

## Commands

For a human-friendly installation against an existing collector:

```sh
npx usecalibrate install --url https://collector.example
```

The command performs all collector discovery before project writes. It checks `/healthz`, `/api/manifest`, and `/dashboard`, uses the remote manifest exactly, previews the route and file plan, and requests confirmation in an interactive terminal. In a noninteractive environment it exits without writes unless `--yes` is present.

For an agent-readable preview, add `--json` without `--yes`. The command intentionally exits with code `3`, changes no project files, and returns the complete proposed plan including each generated file's `content`. Compare those contents with the current files and show exact diffs before requesting approval.

```sh
CALIBRATE_WRITE_KEY=replace-me npx usecalibrate install \
  --url https://collector.example \
  --route /signup=account \
  --route /success=success:shipped \
  --yes \
  --json
```

`CALIBRATE_WRITE_KEY` enables collector runtime verification and is never persisted. Prefer the environment variable because a `--write-key` argument can remain in shell history or process listings. Without a write key, installation can pass with artifact evidence only. The output includes the dashboard URL and makes the hosting boundary explicit: the SDK is bundled with the app, while the existing collector receives events and serves `/dashboard`.

For agents that need a separately reviewable plan file, use the lower-level commands:

```sh
npx usecalibrate detect --dir . --json
npx usecalibrate plan --dir . --out calibrate.plan.json
npx usecalibrate apply --plan calibrate.plan.json --yes
npx usecalibrate verify --dir . --json
```

Supply route semantics when detection cannot infer them safely:

```sh
npx usecalibrate plan --dir . \
  --route /signup=account \
  --route /projects/new=project \
  --route /success=success:shipped \
  --out calibrate.plan.json
```

Use `--no-install` only when dependency installation is managed separately. Applying a plan without `--yes` is a hard error.

## Runtime verification

Start the sidecar from an installed application:

```sh
ADMIN_TOKEN=replace-me \
DASHBOARD_TOKEN=replace-me-too \
WRITE_KEY=replace-with-browser-write-key \
ALLOWED_ORIGINS=http://localhost:5173 \
npx usecalibrate sidecar --dir .
```

Then verify ingestion and privacy rejection. Read the write key from the environment instead of a command argument, and export it from a file or secret manager rather than typing it inline, because most shells record inline assignments in history:

```sh
set -a; . ./.env.calibrate.local; set +a
npx usecalibrate verify --dir . \
  --endpoint http://localhost:8787 \
  --json
```

`.env.calibrate.local` sets `CALIBRATE_WRITE_KEY`. Use a disposable local key for this check. Never paste a production write key into a shell command.

This is collector runtime evidence. To validate the application flow, start the real host application, visit its mapped routes, and confirm that an expected count changes in `/dashboard`.

For React/Vite applications, set `VITE_CALIBRATE_WRITE_KEY` and optionally `VITE_CALIBRATE_ENDPOINT`. Generic ESM applications read `globalThis.CALIBRATE_CONFIG` with `writeKey` and optional `endpoint` fields.

## Support boundary

V1 supports React/Vite and generic ESM browser applications with a unique source entry file. It returns a blocked result for Next.js and unrecognized runtimes. It returns a human-judgment result when fewer than two fixed onboarding routes are available.

The planner will not modify a custom Calibrate integration that lacks `calibrate.install.json`. Review and reconcile that integration manually first.

## Exit codes

- `0`: command completed at its declared evidence level.
- `1`: unexpected execution error.
- `2`: invalid arguments.
- `3`: blocked or needs human judgment.
- `4`: apply or verification failure.

If files change after planning, generate a new plan. Do not force the stale plan over user edits.

If apply or verification fails after files change, preserve the failure and report the changed files. Do not revert user files automatically. Show the failing command or check and ask before any rollback.

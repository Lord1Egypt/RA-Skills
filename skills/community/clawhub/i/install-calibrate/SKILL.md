---
name: install-calibrate
description: Install, configure, verify, or troubleshoot the Calibrate browser SDK and standalone sidecar in JavaScript or TypeScript applications. Use when a user asks an AI coding agent to add Calibrate, instrument an onboarding flow, create a manifest and route map, run the collector, validate privacy boundaries, or repair an existing Calibrate installation.
---

# Install Calibrate

Use the `calibrate` CLI for deterministic detection, planning, application, and verification. Inspect the target repository and its local instructions before running it.

## Preflight

Before planning, confirm:

1. Node.js is version 20 or newer and `usecalibrate` is version 0.1.4 or newer.
2. The target is a supported React/Vite or generic ESM browser application with one detectable entry point.
3. The target repository's package manager, current worktree changes, and local instructions are understood.
4. The collector URL already exists, or the user has chosen the local standalone sidecar path.
5. No custom Calibrate integration exists that the installer cannot safely reconcile.

## Workflow

When the user supplies an existing collector URL and wants the shortest guided flow, run `npx usecalibrate install --url <collector-url> --json` first without `--yes`. This preview intentionally exits with code `3` and makes no project changes. Review its collector checks, exact manifest, route mapping, `plan.changes[].content`, dependency command, required environment names, and dashboard URL. Compare proposed contents with the current files and show the user the exact diffs. After explicit approval, rerun with `--yes --json`. Provide `CALIBRATE_WRITE_KEY` through the environment only when collector runtime verification is required.

When the collector URL is unavailable, the mapping needs manual investigation, or a durable plan artifact is useful, use the lower-level workflow:

1. Run `npx usecalibrate detect --dir . --json` without changing files.
2. Review the detected framework, entry point, existing installation, and proposed fixed routes.
3. If routes are missing or ambiguous, ask the user which ordered routes form the onboarding flow and which route means shipped.
4. Run `npx usecalibrate plan --dir . --out calibrate.plan.json`, adding explicit `--route` values when needed.
5. Show the user the proposed manifest, collector mode, exact generated contents or diffs, dependency command, required environment names, and unresolved decisions.
6. Apply only after approval with `npx usecalibrate apply --plan <plan-file> --yes`.
7. Run the host project's build or typecheck.
8. Run `npx usecalibrate verify --dir . --json` for static checks.
9. When a local sidecar and write key are available, set `CALIBRATE_WRITE_KEY` in the environment and run collector runtime verification with `--endpoint`.
10. Start the real host application, visit the mapped routes, and confirm an expected dashboard count changes before reporting the application flow as validated.

Read [references/cli.md](references/cli.md) for command details, exit codes, supported projects, and recovery behavior.

## Guardrails

- Use fixed machine identifiers only.
- Never derive identifiers from form values, DOM text, clipboard contents, URLs, query strings, hashes, or other user input.
- Keep `ADMIN_TOKEN` server-only.
- Treat `WRITE_KEY` and `DASHBOARD_TOKEN` as scoped browser-visible workshop credentials, not user authentication.
- Keep browser and collector manifests identical by using `calibrate.install.json` as the installer record.
- Do not overwrite a custom Calibrate integration or ambiguous application entry point.
- Do not deploy, publish, create accounts, or modify production infrastructure without explicit authorization.
- Treat `--url` as an existing collector. The installer does not deploy or host infrastructure.
- Do not pass secrets as command-line arguments. Command arguments can remain in shell history or process listings.
- Do not revert changed files automatically after a partial failure. Preserve the failure, show the changed files and failing check, and ask before any rollback.

## Failure and recovery

- Exit code `3`: report the unresolved decision or unsupported target. Confirm that no project files changed.
- Exit code `4` before writes: report the failed check and leave the project unchanged.
- Exit code `4` after writes: report every changed file, preserve user changes, and show the failed build or verification check. Do not claim completion.
- Stale plan: discard the plan, rerun detection and planning, and request approval for the new plan.
- Dependency installation failure: do not retry with a different package manager. Report the command and exit code, then follow the repository's package-manager convention.

## Completion

A package install or passing build is not enough. Report exactly one applicable level:

- `Static integration verified`: generated files, dependency installation, build or typecheck, and static verification passed.
- `Collector runtime verified`: a synthetic completed journey reached the collector and the privacy rejection check passed.
- `Application flow validated`: the real host application loaded the SDK, mapped routes were visited, and an expected dashboard count changed.

Never use collector runtime verification as proof that the host application's browser path works.

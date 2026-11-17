---
name: locron
description: Safely create, preview, inspect, run, update, remove, import, export, explain, diagnose, and manage the local dashboard for schedules managed by the Locron local-first job scheduler. Use when a request names Locron, asks to operate Locron jobs or runs, or needs an explanation of Locron status, history, logs, policies, daemon health, service state, or dashboard; do not use for generic cron syntax questions or unrelated task managers.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - locron
---

# Locron

Operate the installed Locron CLI while preserving its validation, policy, and authorization boundaries.

## Discover the installed surface

1. Resolve `locron` from `PATH`. If it is absent, report that prerequisite instead of inventing an installation or command surface.
2. Run `locron --version --format json` and require a successful `locron.cli/v1` envelope. State the detected version when compatibility matters. This workflow is tested against Locron 0.8.0 and can use an older installed surface when a newer command is absent.
3. Before composing an unfamiliar or version-sensitive command, read `locron help <command>` and any nested subcommand help. The installed help overrides examples or assumptions in this skill.
4. Prefer `--format json` for reads and decisions. Validate `schema`, `ok`, `command`, `data`, and `warnings`; do not parse human prose when JSON is available. Use human output only when the user asks to see it.

Use only capabilities demonstrated by the installed command surface. In particular, do not assume `explain` exists before checking its help; it was added in Locron 0.6.0.

## Classify the request

- For read-only inspection, execute the narrowest useful query and summarize durable facts.
- For a requested mutation that supports `--dry-run`, run the exact proposed command with `--dry-run` first, inspect the normalized result or decision, then execute without `--dry-run` only if the user's current request authorizes the change.
- For a mutation without `--dry-run`, read back the exact job, run, or service target first. Execute only when the current request itself authorizes that specific mutation; a request to inspect, explain, or draft a command is not authorization.
- Never broaden a mutation from one named target to multiple jobs, runs, settings, or services without explicit scope.

Read [references/safety.md](references/safety.md) before a mutation, import/export involving values, or a diagnosis where missed runs, overlap, or termination state matters.

## Create or update a job

1. Resolve exactly one schedule: five-field `--cron`, fixed `--every`, or one-time `--at` with an explicit offset.
2. For cron schedules, clarify `local` versus a named IANA timezone whenever the user's intended wall-clock meaning is not already explicit. Do not apply a timezone to interval or one-time schedules.
3. Resolve exactly one target. Prefer direct argv after `--` so arguments are passed without shell interpretation. Use `--shell` only when the user explicitly needs shell syntax such as pipes, redirects, expansion, or compound commands. Treat HTTP targets as external side effects.
4. Make the effective missed-run, overlap, timeout, retry, and concurrency consequences explicit when they affect the request. Do not silently translate downtime into a sleep claim.
5. Run the complete `add` or `update` command with `--dry-run --format json`. Review the normalized schedule, target, enabled state, environment/value redaction, and policies.
6. If authorized, run the same command without `--dry-run`, then verify with `show <job> --format json`, `preview <job> --format json`, or `why <job> --format json` as appropriate.

Do not enable a job merely because it was previewed. Do not replace a direct target with a shell string for convenience.

## Run or change operational state

- Manual run: inspect the job, run `run <job> --dry-run --format json`, and explain the admission decision. Queue the real run only when requested. Use `--wait` only when the user wants completion/output rather than a durable queue acknowledgement.
- Enable, disable, or remove: inspect the exact job first; these commands have no dry-run in 0.5.0. Re-read the job afterward when it still exists.
- Cancel: inspect `why --run <run-id>` first. Cancellation has no dry-run and the run ID must be canonical. Never add `--acknowledge-unconfirmed` unless the user explicitly accepts the stated risk that a quarantined target may still run.
- Prune: run `prune --dry-run --format json` before authorized deletion, then report the durable counts.
- Configuration: read current settings first. Dry-run supported `config set` and `config unset` mutations before applying them. Do not echo configured secret values.
- Service install/uninstall: check `service status` first. These alter per-user service registration and have no dry-run; perform only when explicitly requested. Do not substitute package-manager service commands unless installed help says Locron refuses its own registration and the user authorizes that alternative.

## Manage the local dashboard

Use dashboard commands only when `locron help dashboard` exposes them. The dashboard is a separate, optional loopback-only process over the same local durable state; it is not remote access and must not be proxied or tunnelled as if it were a multi-user control plane.

- Inspect `dashboard status --format json` before changing its service registration. Report registration, loaded state, URL, and token-file posture without retrieving or exposing the token.
- Run foreground `dashboard` or `dashboard serve` only when the user asks to start an interactive local session. Return its exact printed loopback URL and keep the process lifecycle explicit.
- Treat `dashboard enable`, `dashboard disable`, and `dashboard enable --reset` as service mutations without dry-run. Require current authorization, inspect status first, and read status back afterward. `--reset` rotates the access token and invalidates existing dashboard sessions; never add it merely to repair or restart the service.
- Run `dashboard token` only when the user explicitly needs the secret for local authentication. Do not place the token in URLs, command logs, durable notes, or messages to third parties, and do not claim that `dashboard status` reveals it.

## Diagnose and explain

Use only the layers needed for the question:

1. `service status --format json` for daemon registration and supervisor facts; `dashboard status --format json` for the separate dashboard service when relevant.
2. `doctor --format json` for state paths, daemon reachability, wake socket, migrations, process resolution, dashboard exposure posture, and health checks exposed by the installed release.
3. `explain <job> --format json`, when the installed help exposes it, for the consolidated schedule, current status, latest run, and latest anomaly.
4. `why <job> --format json` for the detailed current definition, eligibility, policies, schedule cursor, and daemon facts.
5. `history [<job>] --format json` to identify a canonical run and outcome.
6. `why --run <run-id> --format json` for immutable run facts, attempts, events, and terminal reason.
7. `logs <run-id>` for captured output; add `--attempt`, `--channel`, or `--follow` only when needed.

Distinguish observed facts from inference. Locron does not directly observe machine sleep; schedule gaps and reconciliation events do not prove sleep. Report unavailable facts as unknown, preserve warnings, and do not claim a target executed merely because a run was queued.

## Import and export safely

- Treat every import document as executable scheduler configuration. For a local file or HTTP(S) URL, run `import <source> --dry-run --format json`, inspect planned creates/updates and values handling, and apply only when authorized.
- Treat a URL import like installing a script from that URL. Do not apply content that changed between review and execution; prefer a stable local copy when identity cannot otherwise be preserved.
- Never infer `--accept-plaintext-values`. Use it only after the user explicitly accepts importing plaintext values.
- Export without values by default. Never add `--include-values --acknowledge-plaintext` unless the user explicitly asks for plaintext values and acknowledges the exposure. Avoid placing exported secrets in chat, logs, or unprotected files.
- Use exact `--jobs` and `--tag` selectors for unattended export rather than relying on an interactive selector.

## Finish with evidence

Report the installed Locron version, the exact scope acted on, dry-run outcome when used, final durable state, and any warnings or unknowns. Do not report a mutation as complete until its command succeeds and a relevant read-back confirms the result.
